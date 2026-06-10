"""Overview tab — the landing read: thesis hero, derived signal strip, day-over-day
deltas, movers, and the headline S&P chart. The worked example the other tabs follow.

Contract every tab module exposes: `section(ctx) -> str` returning the tab's inner HTML.
ctx has .brief (dict), .closes ({symbol: Series}), .tl (timeline DataFrame or None).
"""
from __future__ import annotations

from src import brief as brief_mod
from src import eras, formatting, history, signals
from src.dashboard import charts
from src.dashboard.panels.overview import _narrative_thesis
from src.dashboard.widgets import TONE_HEX

from ..render import caption, esc, fig_html, fmt, grid, hero, kpi_card, panel, tone_class, tone_of
from ..sections import row_for


def _thesis_hero(brief: dict) -> str:
    path = brief_mod.latest_narrative_path()
    if not path or not path.exists():
        return ""
    thesis = _narrative_thesis(path)
    if not thesis:
        return ""
    ndate = path.stem.replace("narrative_", "")
    stale = f" · from {ndate}, older than today's brief" if ndate < str(brief.get("date", "")) else ""
    return hero(f"Today's thesis{stale}", thesis, foot="Full read in the Story tab →")


def _signals(brief: dict) -> str:
    lead = signals.derive_lead(brief)
    sigs = signals.derive_signals(brief)
    out = []
    if lead:
        out.append(hero("Today's read", lead["text"], color=TONE_HEX.get(lead["tone"], "#7beafb")))
    if sigs:
        bullets = "".join(
            f'<div class="sig"><span class="dot {tone_class(s["tone"])}">●</span> {esc(s["text"])}</div>'
            for s in sigs)
        out.append(panel("⚡ Today's signal", f'<div class="grid grid-2">{bullets}</div>'))
    era = eras.era_for(brief.get("date", ""))
    if era:
        out.append(caption(f"📅 We're in the {era['name']} era ({era['regime']}). Fed: {era['fed']}. "
                           "See the Trends tab's time machine."))
    return "".join(out)


def _deltas(brief: dict) -> str:
    result = history.deltas(brief, ["^GSPC", "^IXIC", "^TNX", "DX-Y.NYB", "GC=F", "^VIX"])
    if result is None:
        return caption("📈 Day-over-day deltas appear once a prior session has been saved.")
    prior_date, rows = result
    if not rows:
        return ""
    cards = []
    for r in rows:
        if r["symbol"] == "^TNX":
            value = f"{fmt(r['last'], '.2f')}%"
            delta = formatting.fmt_bps(r["change"]) if r["change"] is not None else None
            tone = tone_of(r["change"])
        else:
            value = formatting.fmt_num(r["last"])
            chg = r["change_pct"]
            delta = formatting.fmt_pct(chg) if chg is not None else None
            tone = ("down" if (chg or 0) > 0 else "up" if (chg or 0) < 0 else "flat") \
                if r["symbol"] == "^VIX" else tone_of(chg)
        cards.append(kpi_card(r["name"], value, delta, tone))
    return panel(f"Since last session ({prior_date})", grid(cards, 6))


def _movers(brief: dict) -> str:
    movers = brief.get("movers") or {}

    def col(title, rows):
        items = "".join(
            f'<div class="mover"><b>{esc(m["name"])}</b> '
            f'<span class="{tone_of(m.get("change_pct"))}">{formatting.fmt_pct(m.get("change_pct"))}</span></div>'
            for m in rows)
        return f'<div><h3>{title}</h3>{items}</div>'
    body = (f'<div class="grid grid-2">{col("Leaders", movers.get("leaders", []))}'
            f'{col("Laggards", movers.get("laggards", []))}</div>')
    return panel("Movers", body)


def section(ctx) -> str:
    brief, closes = ctx.brief, ctx.closes
    parts = [
        _thesis_hero(brief),
        _signals(brief),
        _deltas(brief),
        _movers(brief),
        panel("S&P 500", fig_html(charts.line_fig(closes.get("^GSPC"), "S&P 500"))),
    ]
    return "".join(p for p in parts if p)
