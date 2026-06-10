"""One module per tab. Each exposes `section(ctx) -> str` returning the tab's inner HTML.

ctx is the shared SiteContext (see src.site.build): .brief, .closes, .tl (timeline df).
Tabs reuse the framework-agnostic builders in src.dashboard.charts + the Stylers, plus the
analytics/engine modules — only the Streamlit render glue is replaced by render.py helpers.
"""
