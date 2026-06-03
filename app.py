"""market-story dashboard — daily global markets at a glance.

    python -m streamlit run app.py

Gathers market data, macro, and news (cached), displays them, and persists a
brief to data/briefs/ for Claude to narrate. The "Story" tab renders whatever
narrative Claude has written for the latest brief.

Figure/table builders are kept pure (no Streamlit calls) so they can be unit
tested; the st.* wrappers below just render what the builders return.
"""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src import brief as brief_mod
from src import (bls_data, calendar_data, cftc_data, config, edgar_data, eia_data,
                 formatting, history, macro_data, market_data, news, regime, signals)

LINE_COLOR = "#4C9AFF"
CHANGE_COLS = ["1D", "1W %", "YTD %"]


# --- Data (cached) -----------------------------------------------------------

@st.cache_data(ttl=900, show_spinner="Loading the latest brief...")
def get_data(nonce: int):
    """Return (brief_dict, {symbol: close Series}).

    Instant load: on first paint (nonce 0) serve the last saved/committed brief
    from disk — charts rebuilt from its embedded history, no live network pull.
    The 'Refresh data' button (nonce>0) does the live fetch.
    """
    if nonce == 0:
        saved = brief_mod.load_latest_brief()
        if saved and saved.get("markets"):
            return saved, brief_mod.closes_from_brief(saved)
    return _fetch_live()


def _fetch_live():
    """Live pull of everything (concurrent), persisted so the next load is instant."""
    with ThreadPoolExecutor(max_workers=3) as pool:
        fut_history = pool.submit(market_data.download_history, config.all_symbols())
        fut_macro = pool.submit(macro_data.fetch_macro)
        fut_news = pool.submit(news.fetch_news)
        history = fut_history.result()
        macro = fut_macro.result()
        news_items = fut_news.result()
    sections = market_data.build_market_sections(history)
    brief = brief_mod.build_brief(history, sections, macro, news_items,
                                  bls=get_bls(), energy=get_energy(),
                                  positioning=get_positioning(), fetch=False)
    closes = {symbol: frame["Close"] for symbol, frame in history.items()}
    return brief, closes


@st.cache_data(ttl=21600, show_spinner=False)
def get_bls() -> list[dict]:
    """BLS prints, cached 6h — monthly data, and keeps us under the keyless daily cap."""
    return bls_data.fetch_bls()


@st.cache_data(ttl=21600, show_spinner=False)
def get_energy() -> list[dict]:
    """EIA weekly inventories, cached 6h — the report only updates once a week."""
    return eia_data.fetch_eia()


@st.cache_data(ttl=21600, show_spinner=False)
def get_positioning() -> list[dict]:
    """CFTC speculative positioning, cached 6h — the COT report is weekly (Fri)."""
    return cftc_data.fetch_cftc()


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


@st.cache_data(ttl=21600, show_spinner="Fetching recent SEC filings...")
def get_filings(symbols: tuple) -> list[dict]:
    """Cached recent-EDGAR-filings lookup for the watchlist (6h)."""
    return edgar_data.recent_filings(list(symbols))


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
        {"Series": m["name"], "Latest": m.get("latest"), "Δ": m.get("change"),
         "1y %ile": m.get("pct_1y"), "As of": m.get("date") or "n/a"}
        for m in macro
    ])
    return (
        frame.style
        .format({"Latest": "{:,.2f}", "Δ": "{:+.2f}", "1y %ile": "{:.0f}"}, na_rep="—")
        .map(_color_changes, subset=["Δ"])
    )


def bls_styler(bls: list[dict]):
    frame = pd.DataFrame([
        {"Series": m["name"], "Latest": m.get("latest"), "MoM Δ": m.get("change"),
         "YoY %": m.get("yoy_pct"), "As of": m.get("date") or "n/a"}
        for m in bls
    ])
    return (
        frame.style
        .format({"Latest": "{:,.2f}", "MoM Δ": "{:+.2f}", "YoY %": "{:+.2f}"}, na_rep="n/a")
        .map(_color_changes, subset=["MoM Δ", "YoY %"])
    )


def energy_styler(energy: list[dict]):
    """EIA weekly inventories. No red/green on Δ: a draw (negative) is bullish for
    the commodity, so price-semantic colouring would mislead; the Flow column says
    draw/build in words instead."""
    def flow(change):
        if change is None:
            return "n/a"
        return "draw" if change < 0 else "build" if change > 0 else "flat"
    frame = pd.DataFrame([
        {"Series": m["name"], "Latest": m.get("latest"), "Δ wk": m.get("change"),
         "Flow": flow(m.get("change")), "Units": m.get("units") or "",
         "As of": m.get("date") or "n/a"}
        for m in energy
    ])
    return frame.style.format({"Latest": "{:,.0f}", "Δ wk": "{:+,.0f}"}, na_rep="n/a")


def positioning_styler(positioning: list[dict]):
    """CFTC leveraged-fund (spec) net positioning. Δ wk is coloured by sign (more
    long = green); the Side column names the net direction in words."""
    def side(net):
        if net is None:
            return "n/a"
        return "net long" if net > 0 else "net short" if net < 0 else "flat"
    frame = pd.DataFrame([
        {"Contract": m["name"], "Lev-fund net": m.get("lev_net"), "Side": side(m.get("lev_net")),
         "Δ wk": m.get("lev_net_chg"), "Asset-mgr net": m.get("asset_net"),
         "As of": m.get("date") or "n/a"}
        for m in positioning
    ])
    return (
        frame.style
        .format({"Lev-fund net": "{:+,.0f}", "Δ wk": "{:+,.0f}", "Asset-mgr net": "{:+,.0f}"}, na_rep="n/a")
        .map(_color_changes, subset=["Δ wk"])
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


def sparkline_fig(series):
    """Tiny axis-less trend line for a KPI; green if the window rose, else red."""
    if series is None or len(series) < 2:
        return None
    s = series.tail(45)
    up = float(s.iloc[-1]) >= float(s.iloc[0])
    color = "#26A69A" if up else "#EF5350"
    fig = go.Figure(go.Scatter(x=list(range(len(s))), y=list(s.values), mode="lines",
                               line=dict(color=color, width=1.4)))
    pad = (float(s.max()) - float(s.min())) * 0.12 or 1.0
    fig.update_layout(height=42, margin=dict(t=2, l=0, r=0, b=2), showlegend=False,
                      xaxis=dict(visible=False),
                      yaxis=dict(visible=False, range=[float(s.min()) - pad, float(s.max()) + pad]),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


def yield_curve_fig(rates_rows: list[dict]):
    """US Treasury yield curve (level vs maturity), or None if too few points."""
    maturities = {"^IRX": 0.25, "^FVX": 5.0, "^TNX": 10.0, "^TYX": 30.0}
    labels = {"^IRX": "13W", "^FVX": "5Y", "^TNX": "10Y", "^TYX": "30Y"}
    points = [(maturities[r["symbol"]], r["last"], labels[r["symbol"]])
              for r in rates_rows if r.get("symbol") in maturities and r.get("last") is not None]
    if len(points) < 2:
        return None
    points.sort()
    fig = go.Figure(go.Scatter(
        x=[p[0] for p in points], y=[p[1] for p in points],
        mode="lines+markers+text", text=[p[2] for p in points],
        textposition="top center", line=dict(color=LINE_COLOR),
    ))
    fig.update_layout(height=300, margin=dict(t=36, l=10, r=10, b=10),
                      title="US Treasury yield curve",
                      xaxis=dict(title="Maturity (years)"), yaxis=dict(title="Yield (%)"))
    return fig


# Curated cross-asset set for the correlation matrix (all in config.all_symbols()).
CORR_INSTRUMENTS = [
    ("^GSPC", "S&P"), ("^IXIC", "Nasdaq"), ("^RUT", "Russell"),
    ("^TNX", "10Y"), ("DX-Y.NYB", "Dollar"), ("GC=F", "Gold"),
    ("CL=F", "WTI"), ("HYG", "HY Credit"), ("^VIX", "VIX"),
]


def compute_correlations(closes: dict, symbols: list[str], window: int = 60):
    """Correlation of daily returns over the last `window` sessions, or None.

    Returns a square DataFrame indexed/columned by the symbols that had data;
    None if fewer than two usable series.
    """
    cols = {}
    for sym in symbols:
        series = closes.get(sym)
        if series is not None and len(series) >= 2:
            cols[sym] = series.pct_change()
    if len(cols) < 2:
        return None
    returns = pd.DataFrame(cols).tail(window)
    corr = returns.corr()
    if corr.empty or bool(corr.isna().all().all()):
        return None
    return corr


def correlation_fig(closes: dict, instruments: list[tuple], window: int = 60):
    """Heatmap of cross-asset return correlations, or None if too little data."""
    corr = compute_correlations(closes, [s for s, _ in instruments], window)
    if corr is None:
        return None
    names = {s: n for s, n in instruments}
    labels = [names.get(s, s) for s in corr.columns]
    fig = px.imshow(corr.values, x=labels, y=labels, zmin=-1, zmax=1,
                    color_continuous_scale="RdBu_r", aspect="auto", text_auto=".2f")
    fig.update_layout(height=440, margin=dict(t=36, l=10, r=10, b=10),
                      title=f"Cross-asset return correlation (last {window}d)")
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

def signals_strip(brief: dict) -> None:
    """Lead the Overview with the day's derived read — data turned into signal."""
    sigs = signals.derive_signals(brief)
    if not sigs:
        return
    st.markdown("**⚡ Today's signal**")
    dot = {"up": "green", "down": "red", "warn": "orange", "neutral": "gray"}
    cols = st.columns(2)
    for i, s in enumerate(sigs):
        cols[i % 2].markdown(f":{dot[s['tone']]}[●]  {s['text']}")
    st.divider()


def deltas_panel(brief: dict) -> None:
    """Headline level changes since the prior saved session (day-over-day)."""
    key_syms = ["^GSPC", "^IXIC", "^TNX", "DX-Y.NYB", "GC=F", "^VIX"]
    result = history.deltas(brief, key_syms)
    if result is None:
        st.caption("📈 Day-over-day deltas appear here once you've run this on a prior day "
                   "— snapshots are saved automatically on every refresh.")
        return
    prior_date, rows = result
    if not rows:
        return
    st.markdown(f"**Since last session ({prior_date})**")
    cols = st.columns(len(rows))
    for col, r in zip(cols, rows):
        if r["symbol"] == "^TNX":
            delta = formatting.fmt_bps(r["change"]) if r["change"] is not None else None
            col.metric(r["name"], f"{r['last']:.2f}%", delta)
        else:
            delta = formatting.fmt_pct(r["change_pct"]) if r["change_pct"] is not None else None
            color = "inverse" if r["symbol"] == "^VIX" else "normal"
            col.metric(r["name"], formatting.fmt_num(r["last"]), delta, delta_color=color)
    st.divider()


def overview_tab(brief: dict, closes: dict) -> None:
    signals_strip(brief)
    deltas_panel(brief)
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


def regime_panel(brief: dict) -> None:
    """A quick risk-on/off read derived from the macro (FRED) series."""
    signals = regime.assess(brief.get("macro", []), vix=brief.get("stats", {}).get("vix"))
    if not signals:
        return
    st.markdown(f"**Risk regime — {regime.overall(signals)}**")
    tone_color = {"on": "green", "off": "red", "neutral": "gray"}
    cols = st.columns(len(signals))
    for col, s in zip(cols, signals):
        col.caption(s["label"])
        col.markdown(f":{tone_color[s['tone']]}[{s['reading']}]")
    st.divider()


def macro_tab(brief: dict, closes: dict) -> None:
    regime_panel(brief)
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
    if brief.get("bls"):
        st.markdown("**Labor & Inflation (BLS)** — release-day prints, YoY %")
        st.dataframe(bls_styler(brief["bls"]), use_container_width=True, hide_index=True)
    if brief.get("energy"):
        st.markdown("**Energy inventories (EIA, weekly)** — Δ is the week-over-week draw/build")
        st.dataframe(energy_styler(brief["energy"]), use_container_width=True, hide_index=True)
        st.caption("A crude **draw** (negative Δ) is typically bullish for oil, a build bearish; "
                   "natural gas swings between summer injections and winter withdrawals. Source: EIA.")
    if brief.get("positioning"):
        st.markdown("**Speculative positioning (CFTC, weekly)** — leveraged-fund net & weekly change")
        st.dataframe(positioning_styler(brief["positioning"]), use_container_width=True, hide_index=True)
        st.caption("Leveraged funds = hedge-fund/spec money; asset managers = real money. A large "
                   "spec net-short with real money long is a classic squeeze setup. Source: CFTC TFF.")
    curve = yield_curve_fig(brief["markets"].get("rates", []))
    if curve is not None:
        st.plotly_chart(curve, use_container_width=True, theme="streamlit", key="yield_curve")
    col3, col4 = st.columns(2)
    with col3:
        render_line(closes, "^TNX", "US 10Y Yield", key="mac_tnx")
    with col4:
        render_line(closes, "DX-Y.NYB", "US Dollar Index", key="mac_dxy")
    corr = correlation_fig(closes, CORR_INSTRUMENTS)
    if corr is not None:
        st.plotly_chart(corr, use_container_width=True, theme="streamlit", key="corr_matrix")
        st.caption("Daily-return correlation, last 60 sessions. Watch for regime shifts "
                   "(e.g. stock–bond decoupling, or everything → +1 in a selloff).")


def filter_headlines(items: list[dict], query: str) -> list[dict]:
    """Case-insensitive filter on title + source; empty query returns all."""
    q = query.strip().lower()
    if not q:
        return items
    return [it for it in items
            if q in it.get("title", "").lower() or q in it.get("source", "").lower()]


def headlines_tab(brief: dict) -> None:
    all_items = brief.get("news", [])
    query = st.text_input("Filter headlines", placeholder="e.g. Fed, oil, NVDA…", key="news_filter")
    items = filter_headlines(all_items, query)
    if query.strip():
        st.caption(f"{len(items)} of {len(all_items)} headlines matching “{query.strip()}”")
    else:
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


def _earnings_section() -> None:
    """Upcoming earnings for the watchlist + indices (button-triggered, cached)."""
    st.subheader("Upcoming earnings — watchlist + US indices")
    symbols = tuple(dict.fromkeys(s for s, _ in config.get_watchlist() + config.US_EQUITIES))
    if st.button("Load / refresh earnings dates", key="load_earnings"):
        st.session_state["earnings_rows"] = get_earnings(symbols)
    rows = st.session_state.get("earnings_rows")
    if rows is None:
        st.caption("Click to pull next earnings dates via yfinance (cached 1h). "
                   "Kept off the main load so the dashboard stays fast.")
    elif not rows:
        st.info("No upcoming earnings in the next 60 days, or the source is throttling — try again shortly.")
    else:
        frame = pd.DataFrame([
            {"Date": r["date"], "In (days)": r["days"], "Ticker": r["symbol"], "Company": r["name"]}
            for r in rows
        ])
        st.dataframe(frame, use_container_width=True, hide_index=True)
        st.caption(f"{len(rows)} names · earliest first · via yfinance")


def _filings_section() -> None:
    """Recent SEC EDGAR filings for the watchlist (button-triggered, cached)."""
    st.subheader("Recent SEC filings — watchlist")
    wl = tuple(s for s, _ in config.get_watchlist())
    if st.button("Load / refresh SEC filings", key="load_filings"):
        st.session_state["filings_rows"] = get_filings(wl)
    rows = st.session_state.get("filings_rows")
    if rows is None:
        st.caption("Click to pull recent 8-K / 10-Q / 10-K filings for your watchlist "
                   "via SEC EDGAR (keyless, cached 6h).")
    elif not rows:
        st.info("No recent filings found, or SEC is rate-limiting — try again shortly.")
    else:
        frame = pd.DataFrame([
            {"Date": r["date"], "Ticker": r["symbol"], "Form": r["form"],
             "Description": r["desc"], "Filing": r["link"]}
            for r in rows
        ])
        st.dataframe(
            frame, use_container_width=True, hide_index=True,
            column_config={"Filing": st.column_config.LinkColumn("Filing", display_text="open")},
        )
        st.caption(f"{len(rows)} filings · newest first · via SEC EDGAR")


def calendar_tab() -> None:
    _earnings_section()
    st.divider()
    _filings_section()


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


_POLISH_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');

.block-container { padding-top: 2rem; padding-bottom: 2.6rem; max-width: 1400px; }

/* Display font for headings — a designed, modern identity (legible, no gimmicks) */
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }
h1 { font-size: 2.6rem; font-weight: 700; letter-spacing: -.025em; }
h2 { font-size: 1.45rem; font-weight: 600; letter-spacing: -.01em; }
h3 { font-size: 1.05rem; font-weight: 600; color: #C7D2E0; }

/* Hero KPI numbers in mono for a terminal feel; tables keep aligned tabular figures */
[data-testid="stMetricValue"], [data-testid="stMetricDelta"] {
    font-family: 'IBM Plex Mono', monospace !important; font-variant-numeric: tabular-nums;
}
[data-testid="stDataFrame"], [data-testid="stTable"] { font-size: .84rem; font-variant-numeric: tabular-nums; }

/* KPI cards: accent bar + hover */
[data-testid="stMetric"] {
    background: #141923; border: 1px solid #232B3A; border-left: 3px solid #4C9AFF;
    border-radius: 10px; padding: 13px 16px 11px; transition: border-color .15s ease;
}
[data-testid="stMetric"]:hover { border-left-color: #6FB0FF; border-color: #2E3A4D; }
[data-testid="stMetricValue"] { font-size: 1.5rem; font-weight: 600; }
[data-testid="stMetricLabel"] {
    font-family: 'Space Grotesk', sans-serif !important;
    opacity: .6; font-size: .7rem; text-transform: uppercase; letter-spacing: .09em;
}

/* Tabs: heavier, accent active */
[data-testid="stTabs"] button[role="tab"] { font-size: .95rem; font-weight: 600; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #4C9AFF; }

hr { margin: .85rem 0; border-color: #1c2330; }
</style>
"""


def main() -> None:
    st.set_page_config(page_title="Market Story", layout="wide", initial_sidebar_state="expanded")
    _load_cloud_secrets()
    st.markdown(_POLISH_CSS, unsafe_allow_html=True)
    st.sidebar.title("Market Story")
    pages = st.navigation([
        st.Page(daily_brief_page, title="Daily Brief", icon=":material/show_chart:", default=True),
        st.Page(learn_page, title="Learn the Markets", icon=":material/school:"),
    ])
    pages.run()


if __name__ == "__main__":
    main()
