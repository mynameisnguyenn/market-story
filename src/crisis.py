"""Crisis-window replay and move-percentile ranking.

Replays returns through named historical stress windows and reports
per-window risk stats: total return, max drawdown, historical VaR (5%),
and Expected Shortfall (5%). Also ranks today's move against its own
full history. Pure; no network, no I/O.
"""
from __future__ import annotations

import math
from typing import Optional

import numpy as np
import pandas as pd

# Built-in crisis windows: (ISO start, ISO end, label)
DEFAULT_WINDOWS: list[tuple[str, str, str]] = [
    ("2008-09-01", "2009-03-31", "GFC 2008-09"),
    ("2020-02-01", "2020-04-30", "COVID 2020"),
    ("2022-01-01", "2022-10-31", "Inflation shock 2022"),
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _max_drawdown(returns: pd.Series) -> Optional[float]:
    """Maximum peak-to-trough drawdown from a return series (0-1 scale, negative)."""
    if returns is None or len(returns) == 0:
        return None
    cum = (1.0 + returns).cumprod()
    roll_max = cum.cummax()
    dd = (cum - roll_max) / roll_max
    worst = float(dd.min())
    return round(worst, 6)


def _var95(returns: pd.Series) -> Optional[float]:
    """Historical 5th-percentile VaR (negative number = loss threshold)."""
    arr = returns.dropna().values
    if len(arr) < 5:
        return None
    return round(float(np.percentile(arr, 5)), 6)


def _es95(returns: pd.Series) -> Optional[float]:
    """Historical Expected Shortfall at 5% (mean of returns <= VaR95)."""
    arr = returns.dropna().values
    if len(arr) < 5:
        return None
    var = float(np.percentile(arr, 5))
    tail = arr[arr <= var]
    if len(tail) == 0:
        return None
    return round(float(tail.mean()), 6)


def _total_return(returns: pd.Series) -> Optional[float]:
    """Compound total return over the window."""
    arr = returns.dropna().values
    if len(arr) == 0:
        return None
    result = float(np.prod(1.0 + arr) - 1.0)
    return round(result, 6)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def crisis_replay(
    returns: pd.Series,
    windows: Optional[list[tuple[str, str, str]]] = None,
) -> list[dict]:
    """Replay `returns` through each named window and return per-window risk stats.

    Each output dict: {name, start, end, n_days, return, max_drawdown, var95, es95}.
    Any field that cannot be computed is None. Gracefully handles empty slices and
    windows outside the series range.
    """
    if windows is None:
        windows = DEFAULT_WINDOWS

    if returns is None or not isinstance(returns, pd.Series) or returns.empty:
        return [
            {"name": name, "start": start, "end": end,
             "n_days": 0, "return": None, "max_drawdown": None,
             "var95": None, "es95": None}
            for start, end, name in windows
        ]

    clean = returns.dropna().sort_index()
    results: list[dict] = []

    for start, end, name in windows:
        try:
            window_rets = clean.loc[start:end]
        except Exception:
            window_rets = pd.Series(dtype=float)

        n = len(window_rets)
        if n == 0:
            results.append({
                "name": name, "start": start, "end": end,
                "n_days": 0, "return": None, "max_drawdown": None,
                "var95": None, "es95": None,
            })
            continue

        results.append({
            "name": name,
            "start": start,
            "end": end,
            "n_days": n,
            "return": _total_return(window_rets),
            "max_drawdown": _max_drawdown(window_rets),
            "var95": _var95(window_rets),
            "es95": _es95(window_rets),
        })

    return results


def move_percentile(series: pd.Series, value: float) -> Optional[float]:
    """Rank `value` within `series` history; returns percentile in [0, 100].

    Answers "where does today's move rank in its own history?". Returns None
    when series has fewer than 5 observations or value is NaN/infinite.
    """
    if series is None or not isinstance(series, pd.Series):
        return None
    if value is None or not math.isfinite(value):
        return None

    arr = series.dropna().values
    if len(arr) < 5:
        return None

    n_below = int(np.sum(arr < value))
    pct = n_below / len(arr) * 100.0
    return round(pct, 2)
