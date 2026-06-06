"""Market breadth / internals derived from a dict of daily close price Series.

All functions are pure (no I/O).  Every function returns None (or a safe default)
on empty, short, or all-NaN inputs — never raises.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _clean_series(s: pd.Series) -> pd.Series:
    """Drop NaN and return a float Series; empty if input is unusable."""
    try:
        return pd.Series(s, dtype=float).dropna()
    except Exception:
        return pd.Series(dtype=float)


def _ema(values: np.ndarray, span: int) -> np.ndarray:
    """Exponential moving average via the standard pandas-compatible alpha=2/(span+1)."""
    if len(values) == 0:
        return np.array([], dtype=float)
    alpha = 2.0 / (span + 1)
    out = np.empty(len(values), dtype=float)
    out[0] = values[0]
    for i in range(1, len(values)):
        out[i] = alpha * values[i] + (1.0 - alpha) * out[i - 1]
    return out


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------

def advance_decline(closes: dict) -> dict | None:
    """Count advancers, decliners, and net from the latest daily return of each series.

    Returns {advancers, decliners, net} or None when closes is empty / unusable.
    """
    if not closes:
        return None
    advancers = decliners = 0
    for s in closes.values():
        cs = _clean_series(s)
        if len(cs) < 2:
            continue
        ret = cs.iloc[-1] - cs.iloc[-2]
        if ret > 0:
            advancers += 1
        elif ret < 0:
            decliners += 1
    if advancers == 0 and decliners == 0:
        return None
    return {"advancers": advancers, "decliners": decliners, "net": advancers - decliners}


def pct_above_ma(closes: dict, window: int = 50) -> float | None:
    """Percentage of names whose latest close is above their N-day simple moving average.

    Returns a float in [0, 100] or None when no series has enough history.
    """
    if not closes or window < 1:
        return None
    total = above = 0
    for s in closes.values():
        cs = _clean_series(s)
        if len(cs) < window:
            continue
        ma = cs.iloc[-window:].mean()
        if ma == 0 or np.isnan(ma):
            continue
        total += 1
        if cs.iloc[-1] > ma:
            above += 1
    if total == 0:
        return None
    return round(above / total * 100.0, 1)


def new_highs_lows(closes: dict, window: int = 252) -> dict | None:
    """Count names making a new N-day high or low on their latest close.

    Returns {new_highs, new_lows} or None when no series has enough history.
    """
    if not closes or window < 1:
        return None
    new_highs = new_lows = eligible = 0
    for s in closes.values():
        cs = _clean_series(s)
        if len(cs) < 2:
            continue
        tail = cs.iloc[-window:] if len(cs) >= window else cs
        eligible += 1
        latest = cs.iloc[-1]
        if latest >= tail.max():
            new_highs += 1
        if latest <= tail.min():
            new_lows += 1
    if eligible == 0:
        return None
    return {"new_highs": new_highs, "new_lows": new_lows}


def mcclellan(closes: dict, fast: int = 19, slow: int = 39) -> float | None:
    """McClellan oscillator: EMA(net-advances, fast) - EMA(net-advances, slow).

    Net advances per day = count of rising issues minus count of falling issues.
    Returns the latest oscillator value or None when history is too short.
    """
    if not closes or fast < 1 or slow < 1 or fast >= slow:
        return None

    # Build a DataFrame of daily returns aligned on the common DatetimeIndex.
    series_list = []
    for s in closes.values():
        cs = _clean_series(s)
        if len(cs) >= 2:
            series_list.append(cs)

    if not series_list:
        return None

    # Align all series to a shared index via concat (inner join so we need common dates).
    df = pd.concat(series_list, axis=1)
    rets = df.diff()  # daily changes; first row will be NaN

    if len(rets.dropna(how="all")) < slow:
        return None

    # Daily net-advance count: columns where change > 0 minus columns where change < 0.
    up = (rets > 0).sum(axis=1)
    dn = (rets < 0).sum(axis=1)
    net = (up - dn).dropna().values.astype(float)

    if len(net) < slow:
        return None

    fast_ema = _ema(net, fast)
    slow_ema = _ema(net, slow)
    osc = fast_ema[-1] - slow_ema[-1]
    return round(float(osc), 4)
