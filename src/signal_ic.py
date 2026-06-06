"""Signal Information Coefficient (alphalens-style) — Spearman rank correlation
between a factor signal and its forward returns across horizons and quantiles."""
from __future__ import annotations

import numpy as np
import pandas as pd


def _rank_array(arr: np.ndarray) -> np.ndarray:
    """Return average ranks (0-based) for a 1-D array, matching scipy.stats.rankdata."""
    n = len(arr)
    tmp = arr.argsort()
    rank = np.empty(n, dtype=float)
    rank[tmp] = np.arange(n, dtype=float)
    # handle ties: average ranks
    i = 0
    while i < n:
        j = i + 1
        while j < n and arr[tmp[j]] == arr[tmp[i]]:
            j += 1
        rank[tmp[i:j]] = rank[tmp[i:j]].mean()
        i = j
    return rank


def _spearman(x: np.ndarray, y: np.ndarray) -> float | None:
    """Spearman rank correlation; uses scipy if available, falls back to numpy."""
    if len(x) < 3:
        return None
    try:
        from scipy.stats import spearmanr  # type: ignore
        result, _ = spearmanr(x, y)
        return float(result) if np.isfinite(result) else None
    except ImportError:
        rx, ry = _rank_array(x), _rank_array(y)
        std_x = rx.std()
        std_y = ry.std()
        if std_x == 0 or std_y == 0:
            return None
        return float(np.corrcoef(rx, ry)[0, 1])


def forward_returns(prices: pd.Series, horizon: int) -> pd.Series:
    """Percent return `horizon` days ahead; result is shift(-horizon) of pct_change(horizon)."""
    if prices is None or len(prices.dropna()) < horizon + 1:
        return pd.Series(dtype=float)
    clean = prices.dropna()
    return clean.pct_change(horizon).shift(-horizon)


def information_coefficient(
    signal: pd.Series,
    prices: pd.Series,
    horizon: int,
) -> float | None:
    """Spearman IC between signal and forward returns aligned on the date index."""
    if signal is None or prices is None:
        return None
    fwd = forward_returns(prices, horizon)
    combined = pd.concat([signal.rename("sig"), fwd.rename("fwd")], axis=1).dropna()
    if len(combined) < 3:
        return None
    return _spearman(combined["sig"].values, combined["fwd"].values)


def ic_by_horizon(
    signal: pd.Series,
    prices: pd.Series,
    horizons: list[int] | None = None,
) -> dict[int, float | None]:
    """IC for each horizon in `horizons`; default [1, 5, 21]."""
    if horizons is None:
        horizons = [1, 5, 21]
    return {h: information_coefficient(signal, prices, h) for h in horizons}


def quantile_spread(
    signal: pd.Series,
    prices: pd.Series,
    horizon: int,
    q: int = 5,
) -> float | None:
    """Mean forward return of the top quantile minus bottom quantile of the signal."""
    if signal is None or prices is None or q < 2:
        return None
    fwd = forward_returns(prices, horizon)
    combined = pd.concat([signal.rename("sig"), fwd.rename("fwd")], axis=1).dropna()
    if len(combined) < q * 2:
        return None
    try:
        combined["quantile"] = pd.qcut(combined["sig"], q=q, labels=False, duplicates="drop")
    except ValueError:
        return None
    actual_q = combined["quantile"].nunique()
    if actual_q < 2:
        return None
    top_mean = combined.loc[combined["quantile"] == combined["quantile"].max(), "fwd"].mean()
    bot_mean = combined.loc[combined["quantile"] == combined["quantile"].min(), "fwd"].mean()
    if not np.isfinite(top_mean) or not np.isfinite(bot_mean):
        return None
    return float(top_mean - bot_mean)
