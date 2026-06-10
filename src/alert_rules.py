"""VIX-only dual-gated alert rules — pure, stdlib-only, no I/O.

Fires when VIX is both elevated in level AND in 1-year percentile rank.
No network, no side effects; safe to import anywhere.
"""
from __future__ import annotations

VIX_LEVEL_MIN = 25.0
VIX_PCT_MIN = 80.0

_HONESTY = (
    "Validated edge: elevated fear has historically preceded higher forward returns"
    " (28y study, gross of costs, not a timing signal)."
)


def _vix_row(extremes: list) -> dict | None:
    """Return the ^VIX row from extremes list, or None if absent."""
    for row in extremes:
        if isinstance(row, dict) and row.get("symbol") == "^VIX":
            return row
    return None


def _safe_float(value) -> float | None:
    """Coerce value to float; return None on None/NaN/non-numeric."""
    if value is None:
        return None
    try:
        import math
        f = float(value)
        return None if math.isnan(f) else f
    except (TypeError, ValueError):
        return None


def evaluate_alerts(brief: dict) -> list[dict]:
    """Evaluate VIX alert rule against the brief; return list of alert dicts.

    Returns empty list (never raises) when brief is malformed or thresholds unmet.
    """
    if not isinstance(brief, dict):
        return []
    extremes = brief.get("extremes") or []
    if not isinstance(extremes, list):
        return []

    row = _vix_row(extremes)
    if row is None:
        return []

    level = _safe_float(row.get("last"))
    pct = _safe_float(row.get("pct"))

    if level is None or pct is None:
        return []
    if level < VIX_LEVEL_MIN or pct < VIX_PCT_MIN:
        return []

    pct_int = round(pct)
    title = f"VIX {level:.1f} — {pct_int}th percentile of 1y"
    body = (
        f"VIX is at {level:.1f}, the {pct_int}th percentile of its trailing 1-year range. "
        f"{_HONESTY}"
    )
    return [{"title": title, "body": body, "priority": "high"}]
