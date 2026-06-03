"""Derive a few punchy 'what matters today' signal lines from the brief —
turning the raw tables into a read. Pure logic, no I/O, so it's unit-tested.
"""
from __future__ import annotations


def _row(brief: dict, sym: str):
    for rows in brief.get("markets", {}).values():
        for r in rows:
            if r.get("symbol") == sym:
                return r
    return None


def _macro(brief: dict, sid: str):
    for m in brief.get("macro", []):
        if m.get("id") == sid:
            return m.get("latest")
    return None


def _bls(brief: dict, sid: str):
    for m in brief.get("bls", []):
        if m.get("id") == sid:
            return m
    return None


def derive_signals(brief: dict, limit: int = 6) -> list[dict]:
    """Ranked list of {text, tone} (tone: up/down/warn/neutral) — the day's read."""
    out: list[dict] = []
    stats = brief.get("stats", {})

    vix = _row(brief, "^VIX")
    if vix and vix.get("last") is not None:
        ch, lvl = vix.get("change_pct"), vix["last"]
        if ch is not None and abs(ch) >= 4:
            out.append({"text": f"VIX {'jumped' if ch > 0 else 'eased'} {ch:+.1f}% to {lvl:.1f}"
                                f" — {'fear getting a bid' if ch > 0 else 'calm bid'}",
                        "tone": "down" if ch > 0 else "up"})
        else:
            tag = "elevated" if lvl >= 20 else "low" if lvl < 15 else "normal"
            out.append({"text": f"VIX {lvl:.1f} — {tag}",
                        "tone": "warn" if lvl >= 20 else "up" if lvl < 15 else "neutral"})

    movers = brief.get("movers", {})
    if movers.get("leaders"):
        m = movers["leaders"][0]
        out.append({"text": f"Top mover: {m['name']} {m['change_pct']:+.2f}%", "tone": "up"})
    if movers.get("laggards"):
        m = movers["laggards"][0]
        out.append({"text": f"Biggest drag: {m['name']} {m['change_pct']:+.2f}%", "tone": "down"})

    up, dn = stats.get("sector_advancers"), stats.get("sector_decliners")
    if up is not None and dn is not None and (up + dn) > 0:
        tag = "broad" if up >= 8 else "narrow" if up <= 3 else "mixed"
        out.append({"text": f"Sector breadth {up} up / {dn} down — {tag}",
                    "tone": "up" if up > dn else "down" if dn > up else "neutral"})

    curve = _macro(brief, "T10Y2Y")
    if curve is not None:
        state = "inverted" if curve < 0 else "flat" if curve < 0.5 else "positively sloped"
        out.append({"text": f"2s10s curve {curve:+.2f} — {state}",
                    "tone": "down" if curve < 0 else "neutral"})

    hy = _macro(brief, "BAMLH0A0HYM2")
    if hy is not None:
        state = "tight — no stress" if hy < 3 else "wide — stress" if hy >= 5 else "normal"
        out.append({"text": f"HY credit spread {hy:.2f}% — {state}",
                    "tone": "up" if hy < 3 else "down" if hy >= 5 else "neutral"})

    wti = _row(brief, "CL=F")
    if wti and wti.get("change_pct") is not None and abs(wti["change_pct"]) >= 2 and wti.get("last"):
        ch = wti["change_pct"]
        out.append({"text": f"WTI crude {ch:+.1f}% to ${wti['last']:.0f}", "tone": "up" if ch > 0 else "down"})

    cpi = _bls(brief, "CUUR0000SA0L1E")
    if cpi and cpi.get("yoy_pct") is not None:
        y = cpi["yoy_pct"]
        out.append({"text": f"Core CPI {y:+.1f}% YoY — {'sticky' if y >= 2.5 else 'cooling'}", "tone": "neutral"})

    return out[:limit]
