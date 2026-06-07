"""Equities & Sectors tab — sector treemap, RRG rotation, breadth internals, an
any-name price chart, and the US-equity / watchlist tables."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src import breadth, config, rotation
from src.dashboard.widgets import render_line, render_table, render_treemap


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


def _rrg_chart(closes: dict) -> None:
    """Sector Relative Rotation Graph vs the S&P 500 (rotation module)."""
    bench = closes.get("^GSPC")
    if bench is None:
        return
    names = dict(config.SECTORS)
    prices = {sym: closes[sym] for sym, _ in config.SECTORS if sym in closes}
    df = rotation.rrg(prices, bench, long=120, short=20, window=120)
    if df.empty:
        return
    df = df.assign(name=df["symbol"].map(lambda s: names.get(s, s)))
    fig = px.scatter(df, x="rs_ratio", y="rs_momentum", color="quadrant", text="name",
                     color_discrete_map={"Leading": "#36C26F", "Weakening": "#f5a623",
                                         "Lagging": "#FF5C6C", "Improving": "#7beafb"})
    fig.add_hline(y=0, line=dict(color="#241f1a", width=1))
    fig.add_vline(x=0, line=dict(color="#241f1a", width=1))
    fig.update_traces(textposition="top center", marker=dict(size=11))
    fig.update_layout(height=440, margin=dict(t=10, l=10, r=10, b=10),
                      xaxis_title="RS-Ratio (relative strength)", yaxis_title="RS-Momentum")
    st.subheader("Sector rotation (RRG)")
    st.caption("Relative strength vs momentum against the S&P 500 — Leading (green) / Weakening (amber) / "
               "Lagging (red) / Improving (cyan). Source: rotation.")
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", key="rrg")
    st.divider()


def _breadth_panel(closes: dict) -> None:
    """Breadth & internals across the GICS sectors (breadth module)."""
    prices = {sym: closes[sym] for sym, _ in config.SECTORS if sym in closes}
    if len(prices) < 3:
        return
    ad = breadth.advance_decline(prices)
    pa = breadth.pct_above_ma(prices, window=50)
    hl = breadth.new_highs_lows(prices, window=252)
    mc = breadth.mcclellan(prices)
    if not (ad or pa is not None or hl or mc is not None):
        return
    st.subheader("Sector breadth & internals")
    cols = st.columns(4)
    if ad:
        cols[0].metric("Advance / decline", f"{ad['advancers']} / {ad['decliners']}", f"net {ad['net']:+d}")
    if pa is not None:
        cols[1].metric("% above 50d MA", f"{pa:.0f}%")
    if hl:
        cols[2].metric("New highs / lows (1y)", f"{hl['new_highs']} / {hl['new_lows']}")
    if mc is not None:
        cols[3].metric("McClellan", f"{mc:+.1f}")
    st.caption("Internals across the 11 GICS sectors. Source: breadth.")
    st.divider()


def equities_tab(brief: dict, closes: dict) -> None:
    st.subheader("Sector map (1-day % change)")
    render_treemap(brief["markets"].get("sectors", []))
    st.divider()
    _rrg_chart(closes)
    _breadth_panel(closes)
    names = {sym: name for sym, name in config.US_EQUITIES + config.SECTORS + config.get_watchlist()}
    choice = st.selectbox("Chart an index, sector, or watchlist name", list(names), format_func=lambda s: names.get(s, s))
    render_line(closes, choice, names.get(choice, str(choice)), key="eq_pick")
    st.divider()
    st.subheader("US Equities")               # sectors already shown above as the treemap + RRG + breadth
    render_table(brief["markets"].get("us_equities", []), "equity", "% changes")
    st.subheader("Watchlist (growth)")
    render_table(brief["markets"].get("watchlist", []), "equity", "% changes")
    watchlist_editor()
