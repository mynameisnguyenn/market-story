"""market-story dashboard — daily global markets at a glance.

    python -m streamlit run app.py

Gathers market data, macro, and news (cached), displays them, and persists a
brief to data/briefs/ for Claude to narrate. The "Story" tab renders whatever
narrative Claude has written for the latest brief.

Figure/table builders are kept pure (no Streamlit calls) so they can be unit
tested; the st.* wrappers below just render what the builders return.
"""

from __future__ import annotations

import html
import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src import brief as brief_mod
from src import (bls_data, calendar_data, cftc_data, config, edgar_data, eia_data, eras,
                 formatting, history, ledger, macro_data, market_data, news, regime, riskmetrics,
                 scorecard, signals, thesis, thirteenf, timeline)

LINE_COLOR = "#7beafb"   # electric cyan (Ellis accent); keep in sync with styles.css --accent
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


@st.cache_data(ttl=21600, show_spinner=False)
def get_energy_history() -> list[dict]:
    """Full committed EIA weekly history — cached so the Macro tab doesn't re-read the archive."""
    return eia_data.load_history()


@st.cache_data(ttl=21600, show_spinner=False)
def get_fred_history() -> list[dict]:
    """Full committed FRED history (data/history/macro.jsonl), cached per render."""
    return macro_data.load_fred_history()


@st.cache_data(ttl=21600, show_spinner=False)
def get_bls_history() -> list[dict]:
    """Full committed BLS history (data/history/labor.jsonl), cached per render."""
    return bls_data.load_bls_history()


@st.cache_data(ttl=900, show_spinner=False)
def get_running_thesis() -> str | None:
    """The standing cross-session running thesis (data/running_thesis.md), cached per render."""
    return thesis.load_running_thesis()


@st.cache_data(ttl=900, show_spinner=False)
def get_ledger():
    """The prediction ledger records + running track-record stats, cached per render."""
    return ledger.load(), ledger.stats()


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


@st.cache_data(ttl=21600, show_spinner=False)
def get_econ() -> list[dict]:
    """Upcoming key economic releases (FRED schedule), cached 6h."""
    return calendar_data.fetch_econ_releases()


@st.cache_data(ttl=86400, show_spinner="Pulling the 13F filing...")
def get_13f(name: str, cik: str) -> dict | None:
    """A manager's latest 13F holdings + Q/Q flow, cached 24h (filings are quarterly)."""
    return thirteenf.fetch_fund(name, cik)


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


def extremes_styler(extremes: list[dict]):
    """Where key markets sit in their ~1y range (percentile + z), most stretched first."""
    frame = pd.DataFrame([
        {"Anchor": e["name"], "Last": e.get("last"), "1y %ile": e.get("pct"), "z": e.get("z")}
        for e in extremes
    ])
    return (
        frame.style
        .format({"Last": "{:,.2f}", "1y %ile": "{:.0f}", "z": "{:+.2f}"}, na_rep="—")
        .map(_color_changes, subset=["z"])
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
        # on-palette diverging scale: loss-red -> warm-dark -> gain-green (no off-brand RdYlGn yellow)
        color_continuous_scale=[[0.0, formatting.RED], [0.5, "#1b1611"], [1.0, formatting.GREEN]],
        color_continuous_midpoint=0, range_color=[-span, span],
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
    color = formatting.GREEN if up else formatting.RED
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
                    # cyan-anchored: +1 corr glows accent-cyan (on-brand), -1 loss-red, 0 warm-dark
                    color_continuous_scale=[[0.0, formatting.RED], [0.5, "#16120f"], [1.0, "#7beafb"]],
                    aspect="auto", text_auto=".2f")
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

# One semantic palette for every up/down/warn/neutral cue (charts, dots, badges) — sourced
# from formatting so tables and signals share the exact same green/red. Mirrors styles.css.
_TONE_HEX = {"up": formatting.GREEN, "down": formatting.RED, "warn": "#F5A623", "neutral": formatting.NEUTRAL}


def _tone_span(text: str, tone: str) -> str:
    """Inline HTML span colored by the shared semantic token (replaces Streamlit's :green[]/:red[],
    which use a different theme green/red and broke palette consistency)."""
    return f"<span style=\"color:{_TONE_HEX.get(tone, 'inherit')}\">{text}</span>"


def signals_strip(brief: dict) -> None:
    """Lead the Overview with the day's derived read — data turned into signal."""
    lead = signals.derive_lead(brief)
    sigs = signals.derive_signals(brief)
    if not lead and not sigs:
        return
    if lead:
        color = _TONE_HEX.get(lead["tone"], "#7beafb")
        st.markdown(
            f"""<div style="background:var(--surface);border:1px solid var(--border);border-left:4px solid {color};
            border-radius:10px;padding:16px 20px;margin:2px 0 12px;">
            <div style="font-family:'Space Grotesk',sans-serif;font-size:.66rem;text-transform:uppercase;
            letter-spacing:.13em;color:{color};margin-bottom:6px;">● Today's read</div>
            <div style="font-family:'Instrument Serif',Georgia,serif;font-size:1.5rem;line-height:1.3;
            color:var(--text);">{html.escape(lead['text'])}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    if sigs:
        st.subheader("⚡ Today's signal")
        cols = st.columns(2)
        for i, s in enumerate(sigs):
            cols[i % 2].markdown(_tone_span("●", s["tone"]) + "  " + html.escape(s["text"]),
                                 unsafe_allow_html=True)
    era = eras.era_for(brief.get("date", ""))
    if era:
        st.caption(f"📅 We're in the **{era['name']}** era ({era['regime']}). "
                   f"Fed: {era['fed']}. See the **Trends** tab's time machine, or run `/finance` to dig in.")
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
    st.subheader(f"Since last session ({prior_date})")
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


def _narrative_thesis(path) -> str | None:
    """The written read's one-line thesis: first content line under '## Today in one line'
    (or a 'thesis' header). None if not found — so the hero degrades to the derived lead."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None
    for i, ln in enumerate(lines):
        low = ln.strip().lower()
        if low.startswith("##") and ("one line" in low or "thesis" in low):
            for body in lines[i + 1:]:
                t = body.strip()
                if t and not t.startswith("#"):
                    return t.lstrip("*->•_ ").strip()
            break
    return None


def _thesis_hero(brief: dict) -> None:
    """Lead the Overview with the written narrative's thesis (the product is the read, not the
    data). Silent if there's no narrative — signals_strip's derived lead then carries the top."""
    path = brief_mod.latest_narrative_path()
    if not path or not path.exists():
        return
    thesis = _narrative_thesis(path)
    if not thesis:
        return
    ndate = path.stem.replace("narrative_", "")
    stale = f" · from {ndate}, older than today's brief" if ndate < str(brief.get("date", "")) else ""
    st.markdown(
        f"""<div style="background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--accent);
        border-radius:10px;padding:16px 20px;margin:2px 0 12px;">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:.66rem;text-transform:uppercase;
        letter-spacing:.13em;color:var(--accent);margin-bottom:6px;">● Today's thesis{stale}</div>
        <div style="font-family:'Instrument Serif',Georgia,serif;font-size:1.6rem;line-height:1.3;
        color:var(--text);">{html.escape(thesis)}</div>
        <div style="font-size:.78rem;color:var(--text-dim);margin-top:9px;">Full read in the <b>Story</b> tab →</div>
        </div>""",
        unsafe_allow_html=True,
    )


def overview_tab(brief: dict, closes: dict) -> None:
    _thesis_hero(brief)
    signals_strip(brief)
    deltas_panel(brief)
    movers = brief["movers"]
    left, right = st.columns(2)
    with left:
        st.subheader("Leaders")
        for m in movers["leaders"]:
            st.markdown(f"**{m['name']}**  " + _tone_span(formatting.fmt_pct(m["change_pct"]),
                        "up" if (m.get("change_pct") or 0) >= 0 else "down"), unsafe_allow_html=True)
    with right:
        st.subheader("Laggards")
        for m in movers["laggards"]:
            st.markdown(f"**{m['name']}**  " + _tone_span(formatting.fmt_pct(m["change_pct"]),
                        "up" if (m.get("change_pct") or 0) >= 0 else "down"), unsafe_allow_html=True)
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
        st.subheader("US Equities")
        render_table(brief["markets"].get("us_equities", []), "equity", "% changes")
    with col2:
        st.subheader("US Sectors")
        render_table(brief["markets"].get("sectors", []), "equity", "% changes")
    st.subheader("Watchlist (growth)")
    render_table(brief["markets"].get("watchlist", []), "equity", "% changes")
    watchlist_editor()


def regime_panel(brief: dict) -> None:
    """A quick risk-on/off read derived from the macro (FRED) series."""
    signals = regime.assess(brief.get("macro", []), vix=brief.get("stats", {}).get("vix"))
    if not signals:
        return
    st.subheader(f"Risk regime — {regime.overall(signals)}")
    tone_map = {"on": "up", "off": "down", "neutral": "neutral"}
    cols = st.columns(len(signals))
    for col, s in zip(cols, signals):
        col.caption(s["label"])
        col.markdown(_tone_span(s["reading"], tone_map.get(s["tone"], "neutral")), unsafe_allow_html=True)
    st.divider()


_RISK_ASSETS = [("^GSPC", "S&P 500"), ("^IXIC", "Nasdaq"), ("GC=F", "Gold"),
                ("CL=F", "WTI"), ("HG=F", "Copper"), ("DX-Y.NYB", "Dollar")]


def _risk_drawdown_panel(closes: dict) -> None:
    """Per-asset risk over the embedded ~1y history (riskmetrics): drawdown, ulcer, sortino, tail."""
    rows = []
    for sym, name in _RISK_ASSETS:
        p = closes.get(sym)
        if p is None or len(pd.Series(p).dropna()) < 30:
            continue
        rets = riskmetrics.returns(p)
        lb = riskmetrics.lookback_returns(p) or {}
        md = riskmetrics.max_drawdown(p)
        cd = riskmetrics.current_drawdown(p)
        rows.append({
            "Asset": name,
            "1Y %": (lb.get("1Y") * 100) if lb.get("1Y") is not None else None,
            "Max DD %": (md * 100) if md is not None else None,
            "Cur DD %": (cd[0] * 100) if cd else None,
            "DD days": cd[1] if cd else None,
            "Ulcer": riskmetrics.ulcer_index(p),
            "Sortino": riskmetrics.sortino(rets),
            "Tail": riskmetrics.tail_ratio(rets),
        })
    if not rows:
        return
    st.subheader("Risk & drawdown")
    st.caption("Per-asset over the embedded ~1y history — drawdown depth/duration, ulcer index, "
               "sortino, tail ratio. Source: riskmetrics (ffn/empyrical-style).")
    frame = pd.DataFrame(rows)
    st.dataframe(
        frame.style.format({"1Y %": "{:+.1f}", "Max DD %": "{:.1f}", "Cur DD %": "{:.1f}",
                            "Ulcer": "{:.1f}", "Sortino": "{:+.2f}", "Tail": "{:.2f}"}, na_rep="—")
        .map(_color_changes, subset=["1Y %"]),
        use_container_width=True, hide_index=True)


def macro_tab(brief: dict, closes: dict) -> None:
    regime_panel(brief)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Global Indices")
        render_table(brief["markets"].get("global_indices", []), "equity", "% changes")
        st.subheader("Rates (Treasury yields)")
        render_table(brief["markets"].get("rates", []), "yield", "Last in %, 1D in bps")
        st.subheader("FX")
        render_table(brief["markets"].get("fx", []), "fx", "% changes")
    with col2:
        st.subheader("Commodities")
        render_table(brief["markets"].get("commodities", []), "commodity", "% changes")
        st.subheader("Credit & Bonds")
        render_table(brief["markets"].get("credit", []), "credit", "% changes")
    st.divider()
    st.subheader("Macro (FRED)")
    if brief.get("macro"):
        st.dataframe(macro_styler(brief["macro"]), use_container_width=True, hide_index=True)
    if brief.get("bls"):
        st.subheader("Labor & Inflation (BLS)")
        st.caption("Release-day prints, YoY %")
        st.dataframe(bls_styler(brief["bls"]), use_container_width=True, hide_index=True)
    _macro_history_section()
    if brief.get("energy"):
        st.subheader("Energy inventories (EIA, weekly)")
        st.caption("Δ is the week-over-week draw/build")
        st.dataframe(energy_styler(brief["energy"]), use_container_width=True, hide_index=True)
        st.caption("A crude **draw** (negative Δ) is typically bullish for oil, a build bearish; "
                   "natural gas swings between summer injections and winter withdrawals. Source: EIA.")
        _energy_history_section()
    if brief.get("positioning"):
        st.subheader("Speculative positioning (CFTC, weekly)")
        st.caption("Leveraged-fund net & weekly change")
        st.dataframe(positioning_styler(brief["positioning"]), use_container_width=True, hide_index=True)
        st.caption("Leveraged funds = hedge-fund/spec money; asset managers = real money. A large "
                   "spec net-short with real money long is a classic squeeze setup. Source: CFTC TFF.")
    if brief.get("extremes"):
        st.subheader("Cross-asset extremes")
        st.caption("Where key markets sit in their ~1y range")
        st.dataframe(extremes_styler(brief["extremes"]), use_container_width=True, hide_index=True)
    vol = brief.get("vol")
    if vol:
        tag = "rich — complacency / cheap-looking hedges" if vol["premium"] > 3 \
            else "compressed — realized catching up" if vol["premium"] < 0 else "normal"
        st.caption(f"Vol risk premium: VIX {vol['vix']} vs {vol['realized_20d']} realized (20d) "
                   f"= {vol['premium']:+.1f} pts ({tag}).")
    _risk_drawdown_panel(closes)
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


def _econ_section() -> None:
    rows = get_econ()
    if not rows:
        return
    st.subheader("Economic releases")
    st.caption("The data the market trades around")
    frame = pd.DataFrame([
        {"Release": r["name"], "Date": r["date"],
         "In": ("tomorrow ⚠️" if r["days"] == 1 else "today ⚠️" if r["days"] == 0 else f"{r['days']} days")}
        for r in rows
    ])
    st.dataframe(frame, use_container_width=True, hide_index=True)


def _13f_section() -> None:
    st.subheader("Smart money (13F)")
    st.caption("What prominent managers hold, and last quarter's flow")
    st.caption("Quarterly SEC 13F-HR filings: **long US equities only**, ~45-day lag — positioning, not real-time.")
    names = [n for n, _ in thirteenf.FUNDS]
    choice = st.selectbox("Manager", names, key="f13_fund", label_visibility="collapsed")
    data = get_13f(choice, dict(thirteenf.FUNDS)[choice])
    if not data:
        st.caption("No 13F available for that manager right now.")
        return
    st.caption(f"As of {data['date']} · {data['positions']} positions · ${data['total_value'] / 1e9:,.1f}B reported")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("_Top holdings_")
        st.dataframe(pd.DataFrame([
            {"Holding": h["issuer"], "$B": round(h["value"] / 1e9, 2), "%": round(h["pct"], 1)}
            for h in data["top"]]), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("_Last quarter's moves (vs prior 13F)_")
        st.dataframe(pd.DataFrame([
            {"Move": c["action"], "Holding": c["issuer"], "Δ $B": round(c["delta"] / 1e9, 2)}
            for c in data["changes"]]), use_container_width=True, hide_index=True)


def calendar_tab() -> None:
    _econ_section()
    st.divider()
    _13f_section()
    st.divider()
    _earnings_section()
    st.divider()
    _filings_section()


def _watch_scorecard(brief: dict) -> None:
    """Grade the prior narrative's `watch` block against today's brief — the feedback
    loop that makes the read accountable. Quiet (an expander); skips if no prior."""
    prior = brief_mod.prior_narrative_path()
    if not prior or not prior.exists():
        return
    result = scorecard.score_prior(prior.read_text(encoding="utf-8"), brief)
    graded = result["graded"]
    if not graded:
        return
    s = result["summary"]
    icon = {"triggered": "🟠", "watching": "⚪", "unresolved": "·"}
    with st.expander(f"📋 Last session's watch — {s['triggered']}/{s['resolved']} triggered  ({prior.name})"):
        for g in graded:
            v = g.get("current")
            cur = (f"{v:g}" if isinstance(v, (int, float)) and not isinstance(v, bool)
                   else "n/a" if v is None else str(v))
            st.markdown(f"{icon.get(g['status'], '·')} **{g['status']}** — {g['claim']}  "
                        f"`{g.get('metric')} {g.get('trigger')}` (now {cur})")


TREND_METRICS = [
    ("ust10", "10Y Treasury yield (%)"),
    ("curve_2s10s", "2s10s curve (pp)"),
    ("hy_oas", "HY credit spread (%)"),
    ("vix", "VIX"),
    ("spx_spec_net", "S&P lev-fund net (contracts)"),
    ("vol_premium", "Vol risk premium (VIX − realized)"),
]


def _trend_fig(series):
    last = float(series.iloc[-1])
    fig = go.Figure(go.Scatter(x=series.index, y=series.values, mode="lines",
                               line=dict(color=LINE_COLOR, width=1.4),
                               fill="tozeroy", fillcolor="rgba(123,234,251,0.07)"))
    x0, x1 = series.index[0], series.index[-1]
    if getattr(x0, "tzinfo", None) is not None:        # band math compares against tz-naive era dates
        x0, x1 = x0.tz_localize(None), x1.tz_localize(None)
    for start, end, _name in eras.stress_bands():     # faint red over the crisis eras
        s = pd.Timestamp(start)
        e = pd.Timestamp(end) if end else x1
        if e >= x0 and s <= x1:
            fig.add_vrect(x0=max(s, x0), x1=min(e, x1), fillcolor="#FF5C6C",
                          opacity=0.07, line_width=0, layer="below")
    fig.add_hline(y=last, line=dict(color="#FF5C6C", width=1, dash="dot"), opacity=0.45)
    fig.add_trace(go.Scatter(x=[series.index[-1]], y=[last], mode="markers",
                             marker=dict(color="#FF5C6C", size=7), showlegend=False))
    fig.update_layout(height=230, margin=dict(l=8, r=8, t=8, b=8), showlegend=False,
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=True, gridcolor="#241f1a", zeroline=False))
    return fig


def _level_fig(series, height: int = 260):
    """Like _trend_fig but autoranged (not zero-anchored) — for level series where the
    interesting signal is the swing, not the distance from zero (e.g. inventory stocks)."""
    fig = go.Figure(go.Scatter(x=series.index, y=series.values, mode="lines",
                               line=dict(color=LINE_COLOR, width=1.4)))
    x0, x1 = series.index[0], series.index[-1]
    if getattr(x0, "tzinfo", None) is not None:
        x0, x1 = x0.tz_localize(None), x1.tz_localize(None)
    for start, end, _name in eras.stress_bands():
        s = pd.Timestamp(start)
        e = pd.Timestamp(end) if end else x1
        if e >= x0 and s <= x1:
            fig.add_vrect(x0=max(s, x0), x1=min(e, x1), fillcolor="#FF5C6C",
                          opacity=0.07, line_width=0, layer="below")
    fig.add_trace(go.Scatter(x=[series.index[-1]], y=[float(series.iloc[-1])], mode="markers",
                             marker=dict(color="#FF5C6C", size=7), showlegend=False))
    fig.update_layout(height=height, margin=dict(l=8, r=8, t=8, b=8), showlegend=False,
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=True, gridcolor="#241f1a", zeroline=False))
    return fig


def _energy_history_section() -> None:
    """Full weekly inventory history from the committed archive (petroleum back to 1982)."""
    hist = get_energy_history()
    if not hist:
        return
    names = {sid: name for _route, sid, name in eia_data.EIA_SERIES}
    with st.expander("📈 Inventory history — full weekly record (petroleum back to 1982)"):
        sid = st.selectbox("Series", list(names), format_func=lambda s: names.get(s, s),
                           key="energy_hist_sel")
        rows = [r for r in hist if r.get("series") == sid]
        if len(rows) < 5:
            st.caption("Not enough history for this series yet.")
            return
        idx = pd.to_datetime([r["date"] for r in rows])
        s = pd.Series([r["value"] for r in rows], index=idx).sort_index()
        units = rows[-1].get("units") or ""
        latest = float(s.iloc[-1])
        pct = round(float((s < latest).mean()) * 100)
        prior_yr = s[s.index <= s.index[-1] - pd.Timedelta(days=365)]
        line = (f"{names[sid]} · {len(s):,} weeks · {s.index[0].date()} → {s.index[-1].date()} · "
                f"latest {latest:,.0f} {units} · {pct}ᵗʰ %ile of the whole record")
        if len(prior_yr):
            line += f" · {latest - float(prior_yr.iloc[-1]):+,.0f} {units} YoY"
        st.caption(line)
        st.plotly_chart(_level_fig(s), use_container_width=True, theme="streamlit", key=f"enh_{sid}")
        st.caption("Inventory *levels* (not the weekly draw/build). Faint red = crisis eras. "
                   "The SPR drawdown since 2022 and the gasoline/distillate seasonal saw-tooth are "
                   "visible here. Source: EIA, committed archive `data/history/energy.jsonl`.")


def _macro_history_section() -> None:
    """Deep history for any FRED or BLS series, straight from the committed archives —
    the same data the daily panels show, but back to inception (CPI/jobs to the 1940s,
    Treasury yields to the 1960s). The finance-history learning system reads from here too."""
    fred_rows, bls_rows = get_fred_history(), get_bls_history()
    fred_have = {r["series"] for r in fred_rows}
    bls_have = {r["series"] for r in bls_rows}
    options = {sid: f"{name}  ·  FRED {sid}" for sid, name in config.FRED_SERIES if sid in fred_have}
    options.update({sid: f"{name}  ·  BLS {sid}" for sid, name in bls_data.BLS_SERIES if sid in bls_have})
    if not options:
        return
    with st.expander("📈 Macro & labor history — full record (yields to the 1960s, CPI/jobs to the 1940s)"):
        sid = st.selectbox("Series", list(options), format_func=lambda s: options[s], key="macro_hist_sel")
        source = bls_rows if sid in bls_have else fred_rows
        rows = [r for r in source if r.get("series") == sid]
        if len(rows) < 5:
            st.caption("Not enough history for this series yet.")
            return
        s = pd.Series([r["value"] for r in rows],
                      index=pd.to_datetime([r["date"] for r in rows])).sort_index()
        latest = float(s.iloc[-1])
        pct = round(float((s < latest).mean()) * 100)
        st.caption(f"{options[sid]} · {len(s):,} obs · {s.index[0].date()} → {s.index[-1].date()} · "
                   f"latest {latest:,.2f} · {pct}ᵗʰ %ile of the whole record")
        st.plotly_chart(_level_fig(s), use_container_width=True, theme="streamlit", key=f"mh_{sid}")
        st.caption("Faint red = crisis eras (dotcom · GFC · Euro debt · COVID · 2022 inflation shock). "
                   "Source: committed archives `data/history/macro.jsonl` + `labor.jsonl`.")


def trends_tab() -> None:
    """Where the cross-asset anchors have been — the committed metrics timeline as charts."""
    df = timeline.load_df()
    if df.empty or len(df) < 5 or not isinstance(df.index, pd.DatetimeIndex):
        st.info("The metrics timeline is still accumulating — trend charts appear once a few "
                "sessions exist. Seed ~3 years of real history with `python -m src.backfill`.")
        return
    st.caption(f"{len(df)} sessions · {df.index[0].date()} → {df.index[-1].date()} — each anchor's "
               "path, with today's percentile over the whole window. Faint red = crisis eras "
               "(dotcom · GFC · Euro debt · COVID · the 2022 inflation shock).")
    cols = st.columns(2)
    for i, (col, title) in enumerate(TREND_METRICS):
        if col not in df.columns:
            continue
        series = df[col].dropna()
        if len(series) < 5:                        # skip a thinly-populated metric (no n=1 charts)
            continue
        with cols[i % 2]:
            latest = float(series.iloc[-1])
            pct = round(float((series < latest).mean()) * 100)
            st.markdown(f"**{title}** — {latest:,.2f}  ·  {pct}th %ile of {len(series)} sessions")
            st.plotly_chart(_trend_fig(series), use_container_width=True,
                            theme="streamlit", key=f"trend_{col}")
    _time_machine(df)


def _time_machine(df) -> None:
    """Pick a historical date -> the era it falls in + each metric's level and percentile
    AS OF that date (vs its own history up to then)."""
    st.divider()
    st.subheader("🕰 Time machine")
    st.caption("Pick a date to see where markets stood, and which era it was")
    dmin, dmax = df.index[0].date(), df.index[-1].date()
    picked = st.date_input("As of", value=dmax, min_value=dmin, max_value=dmax, key="timemachine")
    upto = df[df.index <= pd.Timestamp(picked)]
    if upto.empty:
        st.caption("No data on or before that date.")
        return
    as_of = upto.index[-1]
    era = eras.era_for(as_of.date().isoformat())
    if era:
        st.markdown(f"**{as_of.date()} — {era['name']}**  ·  _{era['regime']}_. {era['blurb']}  \n"
                    f"Fed: {era['fed']}")
    snap = []
    for col, label in TREND_METRICS:
        if col not in upto.columns:
            continue
        series = upto[col].dropna()
        if len(series) < 5:
            continue
        val = float(series.iloc[-1])
        pct = round(float((series < val).mean()) * 100)
        snap.append({"Metric": label, "As-of value": round(val, 2),
                     "%ile (history to date)": pct})
    if snap:
        st.dataframe(pd.DataFrame(snap), use_container_width=True, hide_index=True)


def narrative_tab(brief: dict) -> None:
    rt = get_running_thesis()
    if rt:
        with st.expander("📌 Running thesis — the standing cross-session view", expanded=False):
            st.markdown(rt)
        st.caption("The through-line, revised each session by `/narrate`. Today's dated read is below.")
    records, lstats = get_ledger()
    if records:
        hr = lstats["hit_rate"]
        st.subheader("Track record")
        cols = st.columns(3)
        cols[0].metric("Hit rate", f"{hr * 100:.0f}%" if hr is not None else "—")
        cols[1].metric("Resolved", lstats["graded"])
        cols[2].metric("Pending", lstats["pending"])
        with st.expander(f"Every watch call graded ({lstats['total']})"):
            st.dataframe(pd.DataFrame([
                {"Logged": r["logged"], "Status": r["status"], "Metric": r["metric"],
                 "Trigger": r["trigger"], "Resolved@": r.get("graded_value"), "Claim": r["claim"]}
                for r in records]), use_container_width=True, hide_index=True)
        st.caption("Every watch-block prediction, graded at its horizon against committed data — "
                   "the accountability the running thesis is built on.")
        st.divider()
    path = brief_mod.latest_narrative_path()
    if path and path.exists():
        st.caption(f"Source: {path.name}")
        _watch_scorecard(brief)
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

    header_left, header_right = st.columns([6, 2], vertical_alignment="center")
    header_left.title("Global Markets Brief")
    header_right.caption(f"{brief['session_label']}  ·  generated {brief['generated_at_utc'][11:19]} UTC")

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
