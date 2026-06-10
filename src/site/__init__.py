"""Static-site generator for market-story — turns the committed daily brief into a
self-contained HTML site (no Streamlit, no server). The daily data changes once a day,
so a static render is the honest fit: open it as a URL or a local file, install it as a
PWA on desktop or phone. The chart builders (src.dashboard.charts) and Stylers are reused
verbatim — only the Streamlit render glue is replaced by HTML/CSS/JS.
"""
