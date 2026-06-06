"""Relative Rotation Graph (RRG) math — pure numpy/pandas, no IO.

Axes: RS-Ratio (price relative, z-normalised) vs RS-Momentum (rate of change of
the relative). Quadrant labels follow the standard JdK convention:
  Leading   (+ratio, +momentum)
  Weakening (+ratio, -momentum)
  Lagging   (-ratio, -momentum)
  Improving (-ratio, +momentum)
"""
from __future__ import annotations

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean(s: pd.Series) -> pd.Series:
    """Drop NaN and return a float Series; empty if input is bad."""
    try:
        return pd.Series(s, dtype=float).dropna()
    except Exception:
        return pd.Series(dtype=float)


def _zscore(arr: np.ndarray, window: int = 252) -> np.ndarray | None:
    """Z-score the last element of *arr* relative to its trailing *window*."""
    if len(arr) < 30:
        return None
    tail = arr[-window:]
    mean = np.mean(tail)
    std = np.std(tail, ddof=0)
    if std == 0:
        return None
    return (tail[-1] - mean) / std


def _align(a: pd.Series, b: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Inner-join two DatetimeIndex series; return (a_aligned, b_aligned)."""
    combined = pd.concat([a, b], axis=1, join="inner").dropna()
    if combined.empty:
        return pd.Series(dtype=float), pd.Series(dtype=float)
    return combined.iloc[:, 0], combined.iloc[:, 1]


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def rs_ratio(prices: pd.Series, benchmark: pd.Series, window: int = 252) -> float | None:
    """Z-score of (prices/benchmark)*100 within a trailing *window*.

    Returns None when series are too short, misaligned, or denominator is zero.
    """
    p, b = _align(_clean(prices), _clean(benchmark))
    if len(p) < 30:
        return None
    if (b == 0).any():
        return None
    relative = (p / b) * 100.0
    result = _zscore(relative.values, window)
    if result is None:
        return None
    return float(round(result, 4))


def rs_momentum(
    prices: pd.Series,
    benchmark: pd.Series,
    long: int = 252,
    short: int = 21,
) -> float | None:
    """Momentum of log relative-strength: momentum_long minus momentum_short.

    momentum = log(RS[t] / RS[t-n]) for each look-back.
    Returns None when there is insufficient history.
    """
    p, b = _align(_clean(prices), _clean(benchmark))
    min_len = long + 1
    if len(p) < min_len:
        return None
    if (b == 0).any():
        return None
    rs = np.log((p / b).values)
    if len(rs) < long + 1:
        return None
    mom_long = rs[-1] - rs[-(long + 1)]
    mom_short = rs[-1] - rs[-(short + 1)] if len(rs) >= short + 1 else 0.0
    return float(round(mom_long - mom_short, 6))


def quadrant(ratio: float, momentum: float) -> str:
    """Map (rs_ratio, rs_momentum) onto one of four RRG quadrant labels.

    Axes cross at 0 (the z-score centre) for ratio, and 0 for momentum.
    """
    if ratio >= 0 and momentum >= 0:
        return "Leading"
    if ratio >= 0 and momentum < 0:
        return "Weakening"
    if ratio < 0 and momentum < 0:
        return "Lagging"
    return "Improving"


def rrg(
    prices_by_symbol: dict[str, pd.Series],
    benchmark: pd.Series,
    long: int = 252,
    short: int = 21,
    window: int = 252,
) -> pd.DataFrame:
    """Build a full RRG snapshot: one row per symbol with ratio, momentum, quadrant.

    Symbols that lack sufficient history are silently excluded.
    Returns a DataFrame[symbol, rs_ratio, rs_momentum, quadrant], empty if no symbols qualify.
    """
    rows = []
    bench = _clean(benchmark)
    for symbol, prices in (prices_by_symbol or {}).items():
        ratio = rs_ratio(prices, bench, window=window)
        if ratio is None:
            continue
        mom = rs_momentum(prices, bench, long=long, short=short)
        if mom is None:
            continue
        rows.append(
            {
                "symbol": symbol,
                "rs_ratio": ratio,
                "rs_momentum": mom,
                "quadrant": quadrant(ratio, mom),
            }
        )
    if not rows:
        return pd.DataFrame(columns=["symbol", "rs_ratio", "rs_momentum", "quadrant"])
    return pd.DataFrame(rows).reset_index(drop=True)
