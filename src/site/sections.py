"""Shared section pieces used across tabs — currently the masthead KPI header.
Per-tab content lives in src.site.tabs.<id>.section(ctx)."""
from __future__ import annotations

from src import brief as brief_mod
from src import formatting
from src.dashboard import charts

from .render import fig_html, fmt, kpi_card, tone_of

# Header KPIs (symbol, label, kind) — the same six as the Streamlit masthead.
_KPIS = [("^GSPC", "S&P 500", "px"), ("^IXIC", "Nasdaq", "px"), ("^TNX", "10Y Yield", "yield"),
         ("DX-Y.NYB", "US Dollar Index", "px"), ("GC=F", "Gold", "px"), ("^VIX", "VIX", "vix")]


def row_for(brief: dict, sym: str) -> dict | None:
    """First market row matching `sym` (mirrors brief_access.market_row, no dep)."""
    for rows in (brief.get("markets") or {}).values():
        for r in rows:
            if r.get("symbol") == sym:
                return r
    return None


def header_html(ctx) -> str:
    """The masthead: six KPI tiles with sparklines + the sector-breadth line."""
    brief, closes = ctx.brief, ctx.closes
    cards = []
    for sym, label, kind in _KPIS:
        r = row_for(brief, sym) or {}
        last = r.get("last")
        if kind == "yield":
            value = f"{fmt(last, '.2f')}%"
            lc = r.get("level_change")
            delta = formatting.fmt_bps(lc) if lc is not None else None
            tone = tone_of(lc)
        else:
            value = fmt(last)
            chg = r.get("change_pct")
            delta = formatting.fmt_pct(chg) if chg is not None else None
            tone = ("down" if (chg or 0) > 0 else "up" if (chg or 0) < 0 else "flat") \
                if kind == "vix" else tone_of(chg)
        spark = fig_html(charts.sparkline_fig(closes.get(sym)), minimal=True)
        spark = f'<div class="spark">{spark}</div>' if spark else ""
        cards.append(kpi_card(label, value, delta, tone, spark))
    stats = brief.get("stats") or {}
    breadth = (f'<p class="cap">Sector breadth: {stats.get("sector_advancers", 0)} up / '
               f'{stats.get("sector_decliners", 0)} down of {stats.get("sector_count", 0)}</p>')
    _ = brief_mod  # (kept import parity with the rest of the package)
    return f'<div class="kpis">{"".join(cards)}</div>{breadth}'
