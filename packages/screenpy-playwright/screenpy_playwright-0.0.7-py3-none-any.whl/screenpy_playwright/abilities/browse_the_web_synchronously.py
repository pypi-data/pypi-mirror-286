"""Enable an Actor to browse the web synchronously."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Callable

from playwright.sync_api import sync_playwright

from ..exceptions import NoPageError

if TYPE_CHECKING:
    from playwright.sync_api import (
        Browser,
        BrowserContext,
        ConsoleMessage,
        Error as PlaywrightError,
        Page,
        Playwright,
    )
    from typing_extensions import Self


class BrowseTheWebSynchronously:
    """Use a synchronous Playwright instance to browse the web.

    Examples::

        the_actor.can(BrowseTheWebSynchronously.using_firefox())

        the_actor.can(BrowseTheWebSynchronously.using_webkit())

        the_actor.can(BrowseTheWebSynchronously.using_chromium())

        the_actor.can(
            BrowseTheWebSynchronously.using(playwright, cust_browser)
        )
    """

    playwright: Playwright | None = None
    _current_page: Page | None
    pages: list[Page]
    console_logs: dict[Page, list[ConsoleMessage | PlaywrightError]]

    @classmethod
    def using(cls, playwright: Playwright, browser: Browser | BrowserContext) -> Self:
        """Supply a pre-defined Playwright browser to use."""
        cls.playwright = playwright
        return cls(browser)

    @classmethod
    def using_firefox(cls) -> Self:
        """Use a synchronous Firefox browser."""
        if cls.playwright is None:
            cls.playwright = sync_playwright().start()
        return cls(cls.playwright.firefox.launch())

    @classmethod
    def using_chromium(cls) -> Self:
        """Use a synchronous Chromium (i.e. Chrome, Edge, Opera, etc.) browser."""
        if cls.playwright is None:
            cls.playwright = sync_playwright().start()
        return cls(cls.playwright.chromium.launch())

    @classmethod
    def using_webkit(cls) -> Self:
        """Use a synchronous WebKit (i.e. Safari, etc.) browser."""
        if cls.playwright is None:
            cls.playwright = sync_playwright().start()
        return cls(cls.playwright.webkit.launch())

    def __init__(self, browser: Browser | BrowserContext) -> None:
        self.browser = browser
        self._current_page = None
        self.pages = []
        self.console_logs = defaultdict(list)

    @property
    def current_page(self) -> Page:
        """Get the current page.

        Raises a :class:`~screenpy_playwright.exceptions.NoPageError` if there
        is no current page.
        """
        if self._current_page is None:
            msg = "There is no current page. Did you forget to `Open` a page?"
            raise NoPageError(msg)
        return self._current_page

    @current_page.setter
    def current_page(self, page: Page) -> None:
        """Set the current page."""
        self._current_page = page

    def _add_console_log_factory(self, page: Page) -> Callable[[ConsoleMessage], None]:
        def _add_console_log(msg: ConsoleMessage) -> None:
            self.console_logs[page].append(msg)

        return _add_console_log

    def _add_page_error_factory(self, page: Page) -> Callable[[PlaywrightError], None]:
        def _add_page_error(err: PlaywrightError) -> None:
            self.console_logs[page].append(err)

        return _add_page_error

    def new_page(self) -> Page:
        """Create a new page and make it the current page."""
        page = self.browser.new_page()
        console_callback = self._add_console_log_factory(page)
        pageerror_callback = self._add_page_error_factory(page)
        page.on("console", console_callback)
        page.on("pageerror", pageerror_callback)

        self.current_page = page
        self.pages.append(page)

        return self.current_page

    def forget(self) -> None:
        """Forget everything you knew about being a playwright."""
        self.browser.close()
