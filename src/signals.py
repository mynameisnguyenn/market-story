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


def _macro_row(brief: dict, sid: str):
    for m in brief.get("macro", []):
        if m.get("id") == sid:
            return m
    return None


def _ord(n) -> str:
    """1 -> '1st', 3 -> '3rd', 21 -> '21st' (for percentile labels)."""
    n = int(round(n))
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


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
        ch = m["change_pct"]
        out.append({"text": f"Top mover: {m['name']} {ch:+.2f}%",
                    "tone": "up" if ch > 0 else "down" if ch < 0 else "neutral"})
    if movers.get("laggards"):
        m = movers["laggards"][0]
        ch = m["change_pct"]
        out.append({"text": f"Biggest drag: {m['name']} {ch:+.2f}%",
                    "tone": "up" if ch > 0 else "down" if ch < 0 else "neutral"})

    up, dn = stats.get("sector_advancers"), stats.get("sector_decliners")
    if up is not None and dn is not None and (up + dn) > 0:
        tag = "broad" if up >= 8 else "narrow" if up <= 3 else "mixed"
        out.append({"text": f"Sector breadth {up} up / {dn} down — {tag}",
                    "tone": "up" if up > dn else "down" if dn > up else "neutral"})

    curve_row = _macro_row(brief, "T10Y2Y")
    if curve_row and curve_row.get("latest") is not None:
        curve, pct = curve_row["latest"], curve_row.get("pct_1y")
        state = "inverted" if curve < 0 else "flat" if curve < 0.5 else "positively sloped"
        extra = " — 1y flattest" if (pct is not None and pct <= 5) \
            else " — 1y steepest" if (pct is not None and pct >= 95) else ""
        out.append({"text": f"2s10s curve {curve:+.2f} — {state}{extra}",
                    "tone": "down" if curve < 0 else "warn" if extra else "neutral"})

    hy_row = _macro_row(brief, "BAMLH0A0HYM2")
    if hy_row and hy_row.get("latest") is not None:
        hy, pct = hy_row["latest"], hy_row.get("pct_1y")
        ctx = f" ({_ord(pct)} %ile)" if pct is not None else ""
        state = "tight — no stress" if hy < 3 else "wide — stress" if hy >= 5 else "normal"
        out.append({"text": f"HY credit spread {hy:.2f}%{ctx} — {state}",
                    "tone": "up" if hy < 3 else "down" if hy >= 5 else "neutral"})

    sb = brief.get("stock_bond")
    if sb and sb.get("corr") is not None:
        c = sb["corr"]
        flip = " — flipped" if sb.get("flipped") else ""
        out.append({"text": f"Stock-bond corr {c:+.2f} ({sb.get('window', 30)}d) — {sb.get('state', '')}{flip}",
                    "tone": "down" if c > 0.1 else "up" if c < -0.1 else "neutral"})

    wti = _row(brief, "CL=F")
    if wti and wti.get("change_pct") is not None and abs(wti["change_pct"]) >= 2 and wti.get("last"):
        ch = wti["change_pct"]
        out.append({"text": f"WTI crude {ch:+.1f}% to ${wti['last']:.0f}", "tone": "up" if ch > 0 else "down"})

    cpi = _bls(brief, "CUUR0000SA0L1E")
    if cpi and cpi.get("yoy_pct") is not None:
        y = cpi["yoy_pct"]
        out.append({"text": f"Core CPI {y:+.1f}% YoY — {'sticky' if y >= 2.5 else 'cooling'}", "tone": "neutral"})

    return out[:limit]


def derive_lead(brief: dict) -> dict | None:
    """One synthesized 'read of the day' that classifies the cross-asset tape into a
    thesis — and names the evidence it rules out. Returns {text, tone, thesis} or None
    when no theme clears the (deliberately conservative) thresholds. The dashboard
    renders this as the headline above the signal lines."""
    def chg(sym):
        r = _row(brief, sym)
        return r.get("change_pct") if r else None

    spx = chg("^GSPC")
    hy = _macro_row(brief, "BAMLH0A0HYM2")
    hy_chg = hy.get("change") if hy else None          # day-over-day OAS change (pp)
    hy_pct = hy.get("pct_1y") if hy else None
    tnx = _row(brief, "^TNX")
    y_up = tnx.get("level_change", 0) > 0 if tnx and tnx.get("level_change") is not None else None
    oil, copper = chg("CL=F"), chg("HG=F")
    stats = brief.get("stats", {})
    up, dn = stats.get("sector_advancers"), stats.get("sector_decliners")

    # 1) Equity selloff — is credit confirming (de-risking) or calm (an unwind)?
    if spx is not None and spx <= -0.5:
        if hy_chg is not None and hy_chg >= 0.05:      # HY OAS widening >= ~5bp
            return {"tone": "down", "thesis": "de-risking",
                    "text": f"Risk-off with credit confirming — S&P {spx:+.1f}%, HY OAS widening. "
                            "Genuine de-risking, not just an equity wobble."}
        if hy_chg is not None and hy_chg <= 0.02:      # HY OAS ~flat -> not a solvency scare
            pct = f", {_ord(hy_pct)} %ile" if hy_pct is not None else ""
            dur = " (yields up — duration-led)" if y_up else ""
            return {"tone": "warn", "thesis": "unwind-not-stress",
                    "text": f"Duration unwind, not credit stress — S&P {spx:+.1f}% but HY OAS flat{pct}{dur}. "
                            "Flips to genuine de-risking if credit starts widening."}
    # 2) Broad risk-on — participation, not a narrow melt-up
    if spx is not None and spx >= 0.5 and up is not None and dn is not None and up >= 8:
        return {"tone": "up", "thesis": "risk-on",
                "text": f"Broad risk-on — S&P {spx:+.1f}% with {up}/{up + dn} sectors green. "
                        "Participation, not a narrow melt-up."}
    # 3) Oil up / copper down — a geopolitical premium, not reflation
    if oil is not None and copper is not None and oil >= 1.5 and copper <= -1.0:
        return {"tone": "warn", "thesis": "geopolitical-premium",
                "text": f"Oil's bid is a risk premium, not reflation — WTI {oil:+.1f}% while copper {copper:+.1f}%. "
                        "Geopolitical supply scare, not synchronized growth."}
    return None
