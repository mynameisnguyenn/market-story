"""One module per dashboard tab; this package re-exports each tab's entry point."""
from .calendar import calendar_tab
from .equities import equities_tab
from .headlines import headlines_tab
from .macro import macro_tab
from .narrative import narrative_tab
from .overview import overview_tab
from .trends import trends_tab

__all__ = ["overview_tab", "equities_tab", "macro_tab", "trends_tab",
           "headlines_tab", "calendar_tab", "narrative_tab"]
