"""Save a screenshot of the current page."""

from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING, Any

from screenpy import AttachTheFile, DeliveryError, beat

from ..abilities import BrowseTheWebSynchronously

if TYPE_CHECKING:
    from playwright.sync_api import ConsoleMessage
    from screenpy import Actor
    from typing_extensions import Self


class SaveConsoleLog:
    """Save the Actor's browser's console log.

    Use the :meth:`~SaveConsoleLog.and_attach_it` method to indicate that this
    file should be attached to all reports through the Narrator's adapters. This
    method also accepts any keyword arguments those adapters might require.

    Abilities Required:
        :class:`~screenpy_playwright.abilities.BrowseTheWebSynchronously`

    Examples::

        the_actor.attempts_to(SaveConsoleLog("consolelog.txt"))

        the_actor.attempts_to(SaveConsoleLog.as_(filepath))

        # attach file to the Narrator's reports (behavior depends on adapter).
        the_actor.attempts_to(SaveConsoleLog.as_(filepath).and_attach_it())

        # using screenpy_adapter_allure plugin!
        from allure_commons.types import AttachmentTypes
        the_actor.attempts_to(
            SaveConsoleLog.as_(filepath).and_attach_it_with(
                attachment_type=AttachmentTypes.TXT,
            ),
        )
    """

    attach_kwargs: dict | None
    path: Path
    filename: str

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Save browser console log as {self.filename}"

    @classmethod
    def as_(cls, path: str | Path) -> Self:
        """Supply the name and/or filepath for the console log.

        If only a name is supplied, the screenshot will appear in the current
        working directory.

        Args:
            path: The filepath for the screenshot, including its name.
        """
        return cls(path=path)

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.filename = self.path.name
        self.attach_kwargs = None

    def and_attach_it(self, **kwargs: Any) -> Self:  # noqa: ANN401
        """Indicate the screenshot should be attached to any reports.

        This method accepts any additional keywords needed by any adapters
        attached for :external+screenpy:ref:`Narration`.

        Aliases:
            - ``and_attach_it_with``

        Args:
            kwargs: keyword arguments for the adapters used by the narrator.
        """
        self.attach_kwargs = kwargs
        return self

    and_attach_it_with = and_attach_it

    @beat("{} saves their browser's console log as {filename}")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to save their browser's console log."""
        browse_the_web = the_actor.ability_to(BrowseTheWebSynchronously)
        all_logs: chain[ConsoleMessage] = chain.from_iterable(
            browse_the_web.console_logs.values()  # type: ignore[arg-type]
        )

        try:
            self.path.write_text("\n".join(str(log) for log in all_logs))
        except OSError as e:
            msg = (
                f"{the_actor} encountered an issue while attempting to "
                f"save their console log: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

        if self.attach_kwargs is not None:
            the_actor.attempts_to(AttachTheFile(str(self.path), **self.attach_kwargs))
