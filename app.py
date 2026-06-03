"""market-story dashboard — daily global markets at a glance.

    python -m streamlit run app.py

Gathers market data, macro, and news (cached), displays them, and persists a
brief to data/briefs/ for Claude to narrate. The "Story" tab renders whatever
narrative Claude has written for the latest brief.

Figure/table builders are kept pure (no Streamlit calls) so they can be unit
tested; the st.* wrappers below just render what the builders return.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src import brief as brief_mod
from src import calendar_data, config, formatting, macro_data, market_data, news

LINE_COLOR = "#4C9AFF"
CHANGE_COLS = ["1D", "1W %", "YTD %"]


# --- Data (cached) -----------------------------------------------------------

@st.cache_data(ttl=900, show_spinner="Fetching markets, macro, and news...")
def get_data(nonce: int):
    """Pull everything once; return (brief_dict, {symbol: close Series})."""
    history = market_data.download_history(config.all_symbols())
    sections = market_data.build_market_sections(history)
    macro = macro_data.fetch_macro()
    news_items = news.fetch_news()
    brief = brief_mod.build_brief(history, sections, macro, news_items, fetch=False)
    closes = {symbol: frame["Close"] for symbol, frame in history.items()}
    return brief, closes


def persist(brief: dict) -> None:
    """Save the brief to disk once per refresh so Claude can read it."""
    stamp = brief.get("generated_at_utc")
    if st.session_state.get("_saved_stamp") != stamp:
        brief_mod.save_brief(brief)
        st.session_state["_saved_stamp"] = stamp


@st.cache_data(ttl=3600, show_spinner="Fetching upcoming earnings dates...")
def get_earnings(symbols: tuple) -> list[dict]:
    """Cached upcoming-earnings lookup for a set of symbols."""
    return calendar_data.fetch_earnings(list(symbols))


def row_for(brief: dict, symbol: str) -> dict | None:
    for rows in brief["markets"].values():
        for row in rows:
            if row["symbol"] == symbol:
                return row
    return None


# --- Pure builders (no Streamlit; unit-tested) -------------------------------

def section_records(rows: list[dict], kind: str) -> pd.DataFrame:
    """DataFrame for a market group; yields show 1D in basis points."""
    records = []
    for r in rows:
        if kind == "yield":
            level = r.get("level_change")
            one_day = level * 100 if level is not None else None   # pp -> bps
        else:
            one_day = r.get("change_pct")
        records.append({
            "Instrument": r["name"],
            "Last": r.get("last"),
            "1D": one_day,
            "1W %": r.get("change_1w_pct"),
            "YTD %": r.get("ytd_pct"),
        })
    return pd.DataFrame(records, columns=["Instrument", "Last", "1D", "1W %", "YTD %"])


def _color_changes(value) -> str:
    return f"color: {formatting.color_for(value)}"


def section_styler(rows: list[dict], kind: str):
    frame = section_records(rows, kind)
    return (
        frame.style
        .format({"Last": "{:,.2f}", "1D": "{:+.1f}", "1W %": "{:+.2f}", "YTD %": "{:+.2f}"}, na_rep="n/a")
        .map(_color_changes, subset=CHANGE_COLS)
    )


def macro_styler(macro: list[dict]):
    frame = pd.DataFrame([
        {"Series": m["name"], "Latest": m.get("latest"), "Δ": m.get("change"), "As of": m.get("date") or "n/a"}
        for m in macro
    ])
    return (
        frame.style
        .format({"Latest": "{:,.2f}", "Δ": "{:+.2f}"}, na_rep="n/a")
        .map(_color_changes, subset=["Δ"])
    )


def sector_treemap_fig(rows: list[dict]):
    """Treemap of sector 1-day moves, or None if no data.

    The % change is baked into each tile's label. Plotly's %{color} renders
    the mapped RGB string (e.g. "rgb(74,175,92)"), not the value, so it must
    not be used for the displayed number.
    """
    data = [r for r in rows if r.get("change_pct") is not None]
    if not data:
        return None
    frame = pd.DataFrame({
        "Sector": [f"{r['name']}<br>{r['change_pct']:+.2f}%" for r in data],
        "Change": [r["change_pct"] for r in data],
        "Size": [1] * len(data),
    })
    span = max(abs(frame["Change"]).max(), 0.5)
    fig = px.treemap(
        frame, path=["Sector"], values="Size", color="Change",
        color_continuous_scale="RdYlGn", color_continuous_midpoint=0, range_color=[-span, span],
    )
    fig.update_traces(texttemplate="%{label}", hovertemplate="%{label}<extra></extra>")
    fig.update_layout(height=360, margin=dict(t=10, l=10, r=10, b=10))
    return fig


def line_fig(series, name: str):
    """Price line with range selector, or None if no history."""
    if series is None or len(series) == 0:
        return None
    fig = go.Figure(go.Scatter(x=series.index, y=series.values, mode="lines",
                               line=dict(color=LINE_COLOR), name=name))
    fig.update_layout(
        height=380, margin=dict(t=30, l=10, r=10, b=10), title=name,
        xaxis=dict(rangeselector=dict(buttons=[
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(step="all", label="1Y"),
        ])),
    )
    return fig


# --- Streamlit render wrappers -----------------------------------------------

def kpi_metric(col, row: dict | None, kind: str = "equity") -> None:
    if row is None or row.get("last") is None:
        col.metric(row["name"] if row else "n/a", "n/a")
        return
    if kind == "yield":
        delta = formatting.fmt_bps(row.get("level_change")) if row.get("level_change") is not None else None
        col.metric(row["name"], f"{row['last']:.2f}%", delta)
    else:
        change = row.get("change_pct")
        delta = formatting.fmt_pct(change) if change is not None else None
        color = "inverse" if row["symbol"] == "^VIX" else "normal"
        col.metric(row["name"], formatting.fmt_num(row["last"]), delta, delta_color=color)


def render_table(rows: list[dict], kind: str, caption: str) -> None:
    if not rows:
        st.caption("No data available.")
        return
    st.dataframe(section_styler(rows, kind), use_container_width=True, hide_index=True)
    st.caption(caption)


def render_treemap(rows: list[dict]) -> None:
    fig = sector_treemap_fig(rows)
    if fig is None:
        st.info("No sector data available.")
    else:
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def render_line(closes: dict, symbol: str, name: str, key: str | None = None) -> None:
    fig = line_fig(closes.get(symbol), name)
    if fig is None:
        st.info(f"No price history for {name}.")
    else:
        st.plotly_chart(fig, use_container_width=True, theme="streamlit", key=key)


# --- Tabs --------------------------------------------------------------------

def overview_tab(brief: dict, closes: dict) -> None:
    movers = brief["movers"]
    left, right = st.columns(2)
    with left:
        st.subheader("Leaders")
        for m in movers["leaders"]:
            st.markdown(f"**{m['name']}**  :green[{formatting.fmt_pct(m['change_pct'])}]")
    with right:
        st.subheader("Laggards")
        for m in movers["laggards"]:
            st.markdown(f"**{m['name']}**  :red[{formatting.fmt_pct(m['change_pct'])}]")
    st.divider()
    st.subheader("S&P 500")
    render_line(closes, "^GSPC", "S&P 500", key="ov_sp500")


def watchlist_editor() -> None:
    """Edit the custom watchlist inline; saves to disk and triggers a refetch."""
    with st.expander("✏️ Edit watchlist"):
        current = pd.DataFrame(config.get_watchlist(), columns=["Symbol", "Name"])
        edited = st.data_editor(
            current, num_rows="dynamic", use_container_width=True, hide_index=True,
            key="watchlist_editor",
            column_config={
                "Symbol": st.column_config.TextColumn("Symbol", required=True, help="Yahoo Finance ticker, e.g. NVDA"),
                "Name": st.column_config.TextColumn("Name"),
            },
        )
        save = st.button("Save & refresh", key="save_watchlist")
        st.caption("Add or remove rows, then Save & refresh to re-fetch. Stored locally in data/watchlist.json.")
        if save:
            items = []
            for _, row in edited.iterrows():
                sym = str(row["Symbol"]).strip().upper() if pd.notna(row["Symbol"]) else ""
                if not sym:
                    continue
                name = str(row["Name"]).strip() if pd.notna(row["Name"]) else ""
                items.append((sym, name or sym))
            if items:
                config.save_watchlist(items)
                st.session_state.nonce = st.session_state.get("nonce", 0) + 1
                st.rerun()
            else:
                st.warning("Add at least one ticker before saving.")


def equities_tab(brief: dict, closes: dict) -> None:
    st.subheader("Sector map (1-day % change)")
    render_treemap(brief["markets"].get("sectors", []))
    st.divider()
    names = {sym: name for sym, name in config.US_EQUITIES + config.SECTORS + config.get_watchlist()}
    choice = st.selectbox("Chart an index, sector, or watchlist name", list(names), format_func=lambda s: names.get(s, s))
    render_line(closes, choice, names.get(choice, str(choice)), key="eq_pick")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**US Equities**")
        render_table(brief["markets"].get("us_equities", []), "equity", "% changes")
    with col2:
        st.markdown("**US Sectors**")
        render_table(brief["markets"].get("sectors", []), "equity", "% changes")
    st.markdown("**Watchlist (growth)**")
    render_table(brief["markets"].get("watchlist", []), "equity", "% changes")
    watchlist_editor()


def macro_tab(brief: dict, closes: dict) -> None:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Global Indices**")
        render_table(brief["markets"].get("global_indices", []), "equity", "% changes")
        st.markdown("**Rates (Treasury yields)**")
        render_table(brief["markets"].get("rates", []), "yield", "Last in %, 1D in bps")
        st.markdown("**FX**")
        render_table(brief["markets"].get("fx", []), "fx", "% changes")
    with col2:
        st.markdown("**Commodities**")
        render_table(brief["markets"].get("commodities", []), "commodity", "% changes")
        st.markdown("**Credit & Bonds**")
        render_table(brief["markets"].get("credit", []), "credit", "% changes")
    st.divider()
    st.markdown("**Macro (FRED)**")
    if brief.get("macro"):
        st.dataframe(macro_styler(brief["macro"]), use_container_width=True, hide_index=True)
    col3, col4 = st.columns(2)
    with col3:
        render_line(closes, "^TNX", "US 10Y Yield", key="mac_tnx")
    with col4:
        render_line(closes, "DX-Y.NYB", "US Dollar Index", key="mac_dxy")


def headlines_tab(brief: dict) -> None:
    items = brief.get("news", [])
    st.caption(f"{len(items)} headlines across {len(config.FEEDS)} feeds")
    with st.container(height=560):
        for item in items:
            link = item.get("link")
            head = f"[{item['title']}]({link})" if link else item["title"]
            st.markdown(f"**{head}**")
            meta = item.get("source", "")
            if item.get("published"):
                meta += f" · {item['published'][:16].replace('T', ' ')}"
            st.caption(meta)


def calendar_tab() -> None:
    """Upcoming earnings for the watchlist + indices (button-triggered, cached)."""
    st.subheader("Upcoming earnings — watchlist + US indices")
    symbols = tuple(dict.fromkeys(s for s, _ in config.get_watchlist() + config.US_EQUITIES))
    if st.button("Load / refresh earnings dates", key="load_earnings"):
        st.session_state["earnings_rows"] = get_earnings(symbols)
    rows = st.session_state.get("earnings_rows")
    if rows is None:
        st.caption("Click to pull next earnings dates via yfinance (cached 1h). "
                   "Kept off the main load so the dashboard stays fast.")
        return
    if not rows:
        st.info("No upcoming earnings in the next 60 days, or the source is throttling — try again shortly.")
        return
    frame = pd.DataFrame([
        {"Date": r["date"], "In (days)": r["days"], "Ticker": r["symbol"], "Company": r["name"]}
        for r in rows
    ])
    st.dataframe(frame, use_container_width=True, hide_index=True)
    st.caption(f"{len(rows)} names · earliest first · via yfinance")


def narrative_tab(brief: dict) -> None:
    path = brief_mod.latest_narrative_path()
    if path and path.exists():
        st.caption(f"Source: {path.name}")
        st.markdown(path.read_text(encoding="utf-8"))
    else:
        st.info(
            "No narrative yet. Open a terminal in this folder, run `claude`, and ask "
            "**“narrate today's brief”** (or `/narrate`). The story will appear here."
        )
        with st.expander("Show the raw facts brief"):
            st.markdown(brief_mod.render_markdown(brief))


# --- Main --------------------------------------------------------------------

def daily_brief_page() -> None:
    st.session_state.setdefault("nonce", 0)

    with st.sidebar:
        if st.button("Refresh data", use_container_width=True):
            st.session_state.nonce += 1
        st.caption("Scope: US equities & sectors + global macro")
        st.caption("Sources: yfinance · FRED · 12 RSS feeds")

    brief, closes = get_data(st.session_state.nonce)
    persist(brief)

    header_left, header_right = st.columns([6, 2])
    header_left.title("Global Markets Brief")
    header_right.caption(brief["session_label"])
    header_right.caption(f"Generated {brief['generated_at_utc'][11:19]} UTC")

    stats = brief["stats"]
    cols = st.columns(6)
    kpi_metric(cols[0], row_for(brief, "^GSPC"))
    kpi_metric(cols[1], row_for(brief, "^IXIC"))
    kpi_metric(cols[2], row_for(brief, "^TNX"), kind="yield")
    kpi_metric(cols[3], row_for(brief, "DX-Y.NYB"))
    kpi_metric(cols[4], row_for(brief, "GC=F"))
    kpi_metric(cols[5], row_for(brief, "^VIX"))
    st.caption(
        f"Sector breadth: {stats.get('sector_advancers', 0)} up / "
        f"{stats.get('sector_decliners', 0)} down of {stats.get('sector_count', 0)}"
    )
    st.divider()

    overview, equities, macro, headlines, calendar, story = st.tabs(
        ["Overview", "Equities & Sectors", "Global & Macro", "Headlines", "Calendar", "Story"]
    )
    with overview:
        overview_tab(brief, closes)
    with equities:
        equities_tab(brief, closes)
    with macro:
        macro_tab(brief, closes)
    with headlines:
        headlines_tab(brief)
    with calendar:
        calendar_tab()
    with story:
        narrative_tab(brief)


def learn_page() -> None:
    from src import learn
    learn.render()


def main() -> None:
    st.set_page_config(page_title="Market Story", layout="wide", initial_sidebar_state="expanded")
    st.sidebar.title("Market Story")
    pages = st.navigation([
        st.Page(daily_brief_page, title="Daily Brief", icon=":material/show_chart:", default=True),
        st.Page(learn_page, title="Learn the Markets", icon=":material/school:"),
    ])
    pages.run()


if __name__ == "__main__":
    main()
