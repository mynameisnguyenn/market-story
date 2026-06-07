"""Pure builders for the dashboard — DataFrames, Stylers, and plotly figures.

No Streamlit calls in here, so every function is unit-testable (see tests/test_app.py).
The st.* wrappers that render these live in `widgets.py`.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src import eras, formatting

LINE_COLOR = "#7beafb"   # electric cyan (Ellis accent); keep in sync with styles.css --accent
CHANGE_COLS = ["1D", "1W %", "YTD %"]


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


def color_changes(value) -> str:
    return f"color: {formatting.color_for(value)}"


def section_styler(rows: list[dict], kind: str):
    frame = section_records(rows, kind)
    return (
        frame.style
        .format({"Last": "{:,.2f}", "1D": "{:+.1f}", "1W %": "{:+.2f}", "YTD %": "{:+.2f}"}, na_rep="n/a")
        .map(color_changes, subset=CHANGE_COLS)
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
        .map(color_changes, subset=["Δ"])
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
        .map(color_changes, subset=["MoM Δ", "YoY %"])
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
        .map(color_changes, subset=["Δ wk"])
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
        .map(color_changes, subset=["z"])
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
    """Price line with range selector, or None if no history. No chart title — callers label the
    chart with an st.subheader (the app's convention), so the 1M/3M/6M/1Y range buttons own the top
    strip and never overlay a title. `name` stays on the trace for the hover tooltip."""
    if series is None or len(series) == 0:
        return None
    fig = go.Figure(go.Scatter(x=series.index, y=series.values, mode="lines",
                               line=dict(color=LINE_COLOR), name=name))
    fig.update_layout(
        height=380, margin=dict(t=34, l=10, r=10, b=10),   # top strip is the range buttons' space
        xaxis=dict(rangeselector=dict(buttons=[
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
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


def trend_fig(series):
    """Zero-anchored area sparkline with crisis-era bands + a marker on the latest point."""
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


def level_fig(series, height: int = 260):
    """Like trend_fig but autoranged (not zero-anchored) — for level series where the
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
