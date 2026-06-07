"""market-story dashboard — daily global markets at a glance.

    python -m streamlit run app.py

Gathers market data, macro, and news (cached), displays them, and persists a brief to
data/briefs/ for Claude to narrate. The "Story" tab renders whatever narrative Claude
has written for the latest brief.

The view layer now lives in `src/dashboard/` (charts → widgets/data → panels.*); this
module is just wiring (page config, CSS, navigation) plus re-exports of the symbols the
test suite reaches as `app.X`. See src/dashboard/__init__.py for the layout.
"""

from __future__ import annotations

import os

import streamlit as st

from src import config
# Re-exported so tests (and any caller) keep reaching these as app.X after the split.
from src.dashboard.charts import (compute_correlations, correlation_fig, line_fig,  # noqa: F401
                                  macro_styler, section_records, section_styler,
                                  sector_treemap_fig, sparkline_fig, yield_curve_fig)
from src.dashboard.data import (get_bls_history, get_data, get_energy_history,  # noqa: F401
                                get_fred_history, get_ledger, get_running_thesis,
                                get_timeline_df, persist, row_for)
from src.dashboard.panels import (calendar_tab, equities_tab, headlines_tab,  # noqa: F401
                                  macro_tab, narrative_tab, overview_tab, trends_tab)
from src.dashboard.panels.headlines import filter_headlines  # noqa: F401
from src.dashboard.widgets import kpi_metric


def daily_brief_page() -> None:
    st.session_state.setdefault("nonce", 0)

    with st.sidebar:
        if st.button("Refresh data", use_container_width=True):
            st.session_state.nonce += 1
        st.caption("Scope: US equities & sectors + global macro")
        st.caption("Sources: yfinance · FRED · 12 RSS feeds")

    brief, closes = get_data(st.session_state.nonce)
    persist(brief)

    header_left, header_right = st.columns([6, 2], vertical_alignment="center")
    header_left.title("Global Markets Brief")
    header_right.caption(f"{brief.get('session_label', '')}  ·  generated "
                         f"{str(brief.get('generated_at_utc', ''))[11:19]} UTC")

    stats = brief.get("stats") or {}
    cols = st.columns(6)
    kpi_metric(cols[0], row_for(brief, "^GSPC"))
    kpi_metric(cols[1], row_for(brief, "^IXIC"))
    kpi_metric(cols[2], row_for(brief, "^TNX"), kind="yield")
    kpi_metric(cols[3], row_for(brief, "DX-Y.NYB"))
    kpi_metric(cols[4], row_for(brief, "GC=F"))
    kpi_metric(cols[5], row_for(brief, "^VIX"))
    spark_cols = st.columns(6)
    for col, sym in zip(spark_cols, ["^GSPC", "^IXIC", "^TNX", "DX-Y.NYB", "GC=F", "^VIX"]):
        fig = sparkline_fig(closes.get(sym))
        if fig is not None:
            col.plotly_chart(fig, use_container_width=True, theme=None,
                             config={"displayModeBar": False}, key="spark_" + sym)
    st.caption(
        f"Sector breadth: {stats.get('sector_advancers', 0)} up / "
        f"{stats.get('sector_decliners', 0)} down of {stats.get('sector_count', 0)}"
    )
    st.divider()

    # Story sits 2nd — the written read is the product, so it leads the data tabs.
    overview, story, equities, macro, trends, headlines, calendar = st.tabs(
        ["Overview", "Story", "Equities & Sectors", "Global & Macro", "Trends", "Headlines", "Calendar"]
    )
    with overview:
        overview_tab(brief, closes)
    with story:
        narrative_tab(brief)
    with equities:
        equities_tab(brief, closes)
    with macro:
        macro_tab(brief, closes)
    with trends:
        trends_tab()
    with headlines:
        headlines_tab(brief)
    with calendar:
        calendar_tab()


def learn_page() -> None:
    from src import learn
    learn.render()


def _load_cloud_secrets() -> None:
    """Bridge Streamlit Cloud secrets into os.environ so plain modules (edgar,
    macro, bls, eia) that read os.environ/.env pick them up on the hosted site."""
    try:
        for key in ("SEC_USER_AGENT", "FRED_API_KEY", "BLS_API_KEY", "EIA_API_KEY"):
            value = st.secrets.get(key)
            if value and not os.environ.get(key):
                os.environ[key] = str(value)
    except Exception:
        pass


def _load_css() -> str:
    """The dashboard's stylesheet, read fresh from styles.css so design iteration is a
    plain CSS-file edit (not a Python-string edit). Edit styles.css + save -> runOnSave
    reloads; or live-edit in DevTools and bank the winners. See style_lab.py / DESIGN.md."""
    try:
        return (config.PROJECT_ROOT / "styles.css").read_text(encoding="utf-8")
    except Exception:
        return ""


def main() -> None:
    st.set_page_config(page_title="Market Story", page_icon="📈", layout="wide",
                       initial_sidebar_state="auto")   # auto-collapses on mobile so content leads
    _load_cloud_secrets()
    st.markdown(f"<style>{_load_css()}</style>", unsafe_allow_html=True)
    st.sidebar.title("Market Story")
    pages = st.navigation([
        st.Page(daily_brief_page, title="Daily Brief", icon=":material/show_chart:", default=True),
        st.Page(learn_page, title="Learn the Markets", icon=":material/school:"),
    ])
    pages.run()


if __name__ == "__main__":
    main()
