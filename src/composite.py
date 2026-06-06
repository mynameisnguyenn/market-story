"""Composite risk-on/off 'danger' signal from a brief dict (bbrigmga-style).

Evaluates independent conditions drawn from the brief and returns a structured
verdict: danger flag, per-condition detail, raw score, and a regime label.
Pure; tolerates any missing fields — conditions silently skip when data is absent.
"""
from __future__ import annotations

# Number of aligned conditions required to raise the danger flag.
_DANGER_THRESHOLD = 3


# ---------------------------------------------------------------------------
# Helpers — safe field accessors
# ---------------------------------------------------------------------------

def _macro_row(brief: dict, series_id: str) -> dict | None:
    """First macro row whose 'id' matches series_id, or None."""
    for row in brief.get("macro") or []:
        if row.get("id") == series_id:
            return row
    return None


def _safe_float(value) -> float | None:
    """Return float(value) or None on any error / non-finite."""
    import math
    try:
        f = float(value)
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Individual condition evaluators — each returns (on: bool | None, detail: str)
# None means 'data absent; condition skipped'.
# ---------------------------------------------------------------------------

def _cond_yield_curve(brief: dict) -> tuple[bool | None, str]:
    """2s10s inversion: T10Y2Y < 0 -> risk-off."""
    row = _macro_row(brief, "T10Y2Y")
    if row is None:
        return None, "T10Y2Y not available"
    val = _safe_float(row.get("latest"))
    if val is None:
        return None, "T10Y2Y value missing"
    on = val < 0
    return on, f"2s10s = {val:+.2f} ({'inverted' if on else 'positive/flat'})"


def _cond_hy_widening(brief: dict) -> tuple[bool | None, str]:
    """HY OAS widening: day-over-day change > 0 OR 1y-percentile > 85 -> risk-off."""
    row = _macro_row(brief, "BAMLH0A0HYM2")
    if row is None:
        # try BAMLC0A0CM (IG OAS) as fallback — same logic
        row = _macro_row(brief, "BAMLC0A0CM")
    if row is None:
        return None, "HY OAS not available"
    chg = _safe_float(row.get("change"))
    pct = _safe_float(row.get("pct_1y"))
    latest = _safe_float(row.get("latest"))
    chg_on = chg is not None and chg > 0
    pct_on = pct is not None and pct > 85
    on = chg_on or pct_on
    parts = []
    if latest is not None:
        parts.append(f"OAS={latest:.2f}%")
    if chg is not None:
        parts.append(f"Δ{chg:+.3f}")
    if pct is not None:
        parts.append(f"{pct:.0f}th %ile")
    return on, "HY OAS " + (", ".join(parts) or "n/a") + (" (widening)" if on else " (stable)")


def _cond_sector_breadth(brief: dict) -> tuple[bool | None, str]:
    """Sector breadth: more decliners than advancers -> risk-off."""
    stats = brief.get("stats") or {}
    adv = _safe_float(stats.get("sector_advancers"))
    dec = _safe_float(stats.get("sector_decliners"))
    if adv is None or dec is None:
        return None, "Sector breadth not available"
    on = dec > adv
    return on, f"Sectors {int(adv)} up / {int(dec)} down ({'negative' if on else 'positive'} breadth)"


def _cond_vol_premium(brief: dict) -> tuple[bool | None, str]:
    """Vol premium (VIX - realized 20d) > 3 -> implied vol elevated vs realized,
    protection priced rich -> risk-off (the tape is paying up for hedges)."""
    vol = brief.get("vol") or {}
    prem = _safe_float(vol.get("premium"))
    if prem is None:
        return None, "Vol premium not available"
    vix = _safe_float(vol.get("vix"))
    rv = _safe_float(vol.get("realized_20d"))
    on = prem > 3
    parts = []
    if vix is not None:
        parts.append(f"VIX={vix:.1f}")
    if rv is not None:
        parts.append(f"RV={rv:.1f}")
    parts.append(f"prem={prem:+.1f}")
    return on, "Vol premium: " + ", ".join(parts) + (" (elevated — hedges expensive)" if on else " (normal)")


def _cond_stock_bond_corr(brief: dict) -> tuple[bool | None, str]:
    """Stock-bond correlation flipped positive -> hedge broken -> risk-off."""
    sb = brief.get("stock_bond") or {}
    flipped = sb.get("flipped")
    corr = _safe_float(sb.get("corr"))
    if flipped is None or corr is None:
        return None, "Stock-bond correlation not available"
    on = bool(flipped) and corr > 0
    window = sb.get("window", 30)
    return on, (f"Stock-bond corr={corr:+.2f} ({window}d)"
                + (" — flipped, hedge broken" if on else " — hedge intact" if corr < 0 else " — uncorrelated"))


def _cond_vix_level(brief: dict) -> tuple[bool | None, str]:
    """VIX above 25 -> fear elevated -> risk-off."""
    stats = brief.get("stats") or {}
    vix = _safe_float(stats.get("vix"))
    if vix is None:
        vol = brief.get("vol") or {}
        vix = _safe_float(vol.get("vix"))
    if vix is None:
        return None, "VIX level not available"
    on = vix >= 25
    label = "fear elevated" if vix >= 25 else "calm" if vix < 15 else "normal"
    return on, f"VIX={vix:.1f} ({label})"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_CONDITIONS: list[tuple[str, object]] = [
    ("Yield-curve inverted (2s10s<0)", _cond_yield_curve),
    ("HY OAS widening (Δ>0 or >85th %ile)", _cond_hy_widening),
    ("Sector breadth negative (decliners>advancers)", _cond_sector_breadth),
    ("Vol premium elevated (>3 pts)", _cond_vol_premium),
    ("Stock-bond correlation flipped positive", _cond_stock_bond_corr),
    ("VIX above 25", _cond_vix_level),
]


def evaluate(brief: dict, threshold: int = _DANGER_THRESHOLD) -> dict:
    """Composite risk-off danger signal from a brief dict.

    Returns {danger, conditions, score, regime}.
    """
    brief = brief or {}
    conditions: list[dict] = []
    score = 0

    for name, fn in _CONDITIONS:
        on, detail = fn(brief)
        if on is True:
            score += 1
        conditions.append({"name": name, "on": bool(on) if on is not None else False,
                            "detail": detail})

    danger = score >= threshold
    if danger:
        regime = "risk-off"
    elif score == 0:
        regime = "risk-on"
    else:
        regime = "neutral"

    return {"danger": danger, "conditions": conditions, "score": score, "regime": regime}
