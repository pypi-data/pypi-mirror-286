"""Actions enabled by the Abilities in ScreenPy: Playwright."""

from .click import Click
from .enter import Enter
from .open import Open
from .refresh_the_page import RefreshThePage
from .save_console_log import SaveConsoleLog
from .save_screenshot import SaveScreenshot
from .scroll import Scroll
from .select import Select

# Natural-language-enabling aliases
Clicks = Click
Enters = Enter
GoTo = GoesTo = Visit = Visits = Opens = Open
Refresh = Refreshes = RefreshesThePage = RefreshThePage
SavesConsoleLog = SaveConsoleLog
SavesScreenshot = SavesAScreenshot = SaveAScreenshot = SaveScreenshot
Scrolls = Scroll
Selects = Select


__all__ = [
    "Click",
    "Clicks",
    "Enter",
    "Enters",
    "GoesTo",
    "GoTo",
    "Open",
    "Opens",
    "RefreshesThePage",
    "RefreshThePage",
    "SaveAScreenshot",
    "SaveConsoleLog",
    "SavesAScreenshot",
    "SavesConsoleLog",
    "SaveScreenshot",
    "SavesScreenshot",
    "Scroll",
    "Scrolls",
    "Select",
    "Selects",
    "Visit",
    "Visits",
]
