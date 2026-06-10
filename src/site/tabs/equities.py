"""Equities & Sectors tab — sector treemap, RRG rotation, breadth internals,
and the US-equity / sector / watchlist tables."""
from __future__ import annotations

import plotly.express as px

from src import breadth, config, rotation
from src.dashboard import charts

from ..render import caption, fig_html, fmt, grid, kpi_card, panel, styler_html, tone_of


# ---------------------------------------------------------------------------
# Sector treemap
# ---------------------------------------------------------------------------

def _treemap(brief: dict) -> str:
    """Sector 1-day % change treemap — the visual centrepiece of the tab."""
    rows = (brief.get("markets") or {}).get("sectors", [])
    fig = charts.sector_treemap_fig(rows)
    body = fig_html(fig)
    return panel("Sector map (1-day % change)", body)


# ---------------------------------------------------------------------------
# RRG rotation chart
# ---------------------------------------------------------------------------

def _rrg(closes: dict) -> str:
    """Sector Relative Rotation Graph vs the S&P 500 (rotation module)."""
    bench = closes.get("^GSPC")
    if bench is None:
        return ""
    names = dict(config.SECTORS)
    prices = {sym: closes[sym] for sym, _ in config.SECTORS if sym in closes}
    if not prices:
        return ""
    try:
        df = rotation.rrg(prices, bench, long=120, short=20, window=120)
    except Exception:
        return ""
    if df.empty:
        return ""
    df = df.assign(name=df["symbol"].map(lambda s: names.get(s, s)))
    try:
        fig = px.scatter(
            df, x="rs_ratio", y="rs_momentum", color="quadrant", text="name",
            color_discrete_map={
                "Leading": "#36C26F", "Weakening": "#f5a623",
                "Lagging": "#FF5C6C", "Improving": "#7beafb",
            },
        )
        fig.add_hline(y=0, line=dict(color="#241f1a", width=1))
        fig.add_vline(x=0, line=dict(color="#241f1a", width=1))
        fig.update_traces(textposition="top center", marker=dict(size=11))
        fig.update_layout(height=440, margin=dict(t=10, l=10, r=10, b=10),
                          xaxis_title="RS-Ratio (relative strength)",
                          yaxis_title="RS-Momentum")
    except Exception:
        return ""
    cap = ("Relative strength vs momentum against the S&P 500 — Leading (green) / "
           "Weakening (amber) / Lagging (red) / Improving (cyan). Source: rotation.")
    return panel("Sector rotation (RRG)", fig_html(fig), sub=cap)


# ---------------------------------------------------------------------------
# Breadth internals KPI strip
# ---------------------------------------------------------------------------

def _breadth(closes: dict) -> str:
    """Breadth & internals across the GICS sectors (breadth module)."""
    prices = {sym: closes[sym] for sym, _ in config.SECTORS if sym in closes}
    if len(prices) < 3:
        return ""
    try:
        ad = breadth.advance_decline(prices)
        pa = breadth.pct_above_ma(prices, window=50)
        hl = breadth.new_highs_lows(prices, window=252)
        mc = breadth.mcclellan(prices)
    except Exception:
        return ""
    if not any([ad, pa is not None, hl, mc is not None]):
        return ""
    cards = []
    if ad:
        net = ad["net"]
        cards.append(kpi_card("Advance / decline",
                               f"{ad['advancers']} / {ad['decliners']}",
                               delta=f"net {net:+d}", tone=tone_of(net)))
    if pa is not None:
        cards.append(kpi_card("% above 50d MA", f"{pa:.0f}%",
                               tone=("up" if pa >= 50 else "down")))
    if hl:
        cards.append(kpi_card("New highs / lows (1y)",
                               f"{hl['new_highs']} / {hl['new_lows']}",
                               tone=tone_of(hl["new_highs"] - hl["new_lows"])))
    if mc is not None:
        cards.append(kpi_card("McClellan", fmt(mc, "+.1f"), tone=tone_of(mc)))
    if not cards:
        return ""
    body = grid(cards, cols=4)
    cap = "Internals across the 11 GICS sectors. Source: breadth."
    return panel("Sector breadth & internals", body, sub=cap)


# ---------------------------------------------------------------------------
# Market tables
# ---------------------------------------------------------------------------

def _table(brief: dict, group: str, title: str, sub: str = "") -> str:
    """Styled table for a brief market group via charts.section_styler."""
    rows = (brief.get("markets") or {}).get(group, [])
    if not rows:
        return ""
    try:
        styler = charts.section_styler(rows, kind="equity")
    except Exception:
        return ""
    return panel(title, styler_html(styler), sub=sub)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def section(ctx) -> str:
    """Inner HTML for the Equities & Sectors tab."""
    brief, closes = ctx.brief, ctx.closes
    parts = [
        _treemap(brief),
        _rrg(closes),
        _breadth(closes),
        _table(brief, "us_equities", "US Equities", sub="% changes"),
        _table(brief, "sectors", "Sectors", sub="% changes"),
        _table(brief, "watchlist", "Watchlist (growth)", sub="% changes"),
    ]
    return "".join(p for p in parts if p)
