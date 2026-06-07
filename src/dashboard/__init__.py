"""Dashboard view layer for app.py — split out of the former monolith.

- `charts`  : pure builders (DataFrames, plotly figures) — no Streamlit, unit-tested.
- `widgets` : thin st.* render wrappers over the builders.
- `data`    : cached loaders + the brief/closes plumbing.
- `panels.*`: one module per dashboard tab.

`app.py` is now just wiring (page config, CSS, navigation) plus re-exports of the symbols
the test suite reaches as `app.X`.
"""
