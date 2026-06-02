"""Display helpers: percent formatting, directional arrows, and colors."""

from __future__ import annotations

import math

GREEN = "#26A69A"
RED = "#EF5350"
NEUTRAL = "#9AA0A6"


def is_missing(value) -> bool:
    """True for None or NaN."""
    return value is None or (isinstance(value, float) and math.isnan(value))


def fmt_pct(value, decimals: int = 2) -> str:
    """Signed percent string, e.g. +0.42%. Returns 'n/a' for missing."""
    if is_missing(value):
        return "n/a"
    return f"{value:+.{decimals}f}%"


def fmt_num(value, decimals: int = 2) -> str:
    """Plain number with thousands separators. Returns 'n/a' for missing."""
    if is_missing(value):
        return "n/a"
    return f"{value:,.{decimals}f}"


def fmt_bps(change_pct, decimals: int = 0) -> str:
    """Format a yield change given in percentage points as basis points."""
    if is_missing(change_pct):
        return "n/a"
    return f"{change_pct * 100:+.{decimals}f} bps"


def arrow(value) -> str:
    """Directional arrow for a change value."""
    if is_missing(value) or value == 0:
        return "→"
    return "▲" if value > 0 else "▼"


def color_for(value) -> str:
    """Risk-on/off color for a change value (green up, red down)."""
    if is_missing(value) or value == 0:
        return NEUTRAL
    return GREEN if value > 0 else RED
