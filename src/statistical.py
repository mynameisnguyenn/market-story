"""Distribution shape + trend/mean-reversion flags for return series.

Pure numpy/pandas — no statsmodels, no sklearn. Degrades gracefully on short or
empty input by returning None rather than raising.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Minimum observations required before any stat is computed.
_MIN_OBS = 10


def _clean(rets: pd.Series) -> np.ndarray:
    """Drop NaN/Inf and return a float64 array."""
    arr = np.asarray(rets, dtype=float)
    return arr[np.isfinite(arr)]


def jarque_bera(rets: pd.Series) -> tuple[float, bool] | tuple[None, None]:
    """JB normality test on a return series; (stat, is_normal) or (None, None).

    Tries scipy.stats.jarque_bera first; falls back to the closed-form
    JB = n/6 * (S^2 + (K-3)^2/4) with chi-squared p-value at df=2.
    is_normal is True when p-value >= 0.05 (fail to reject H0).
    """
    arr = _clean(rets) if isinstance(rets, pd.Series) else _clean(pd.Series(rets))
    n = len(arr)
    if n < _MIN_OBS:
        return None, None

    try:
        from scipy.stats import jarque_bera as _scipy_jb
        stat, p = _scipy_jb(arr)
        if not (np.isfinite(stat) and np.isfinite(p)):
            return None, None
        return float(stat), bool(p >= 0.05)
    except Exception:
        pass

    # Closed-form fallback
    mean = arr.mean()
    diffs = arr - mean
    std = arr.std(ddof=0)
    if std == 0:
        return None, None
    s = float(np.mean(diffs ** 3) / std ** 3)          # skewness
    k = float(np.mean(diffs ** 4) / std ** 4)          # kurtosis (not excess)
    stat = float(n / 6.0 * (s ** 2 + (k - 3.0) ** 2 / 4.0))

    # Chi-squared CDF at df=2: p = exp(-stat/2) for the upper tail
    p = float(np.exp(-stat / 2.0))
    return stat, bool(p >= 0.05)


def variance_ratio(rets: pd.Series, k: int = 5) -> float | None:
    """Lo-MacKinlay variance ratio: Var(k-period) / (k * Var(1-period)).

    VR > 1 => momentum/trending; VR < 1 => mean-reverting; VR ~ 1 => random walk.
    Returns None when input is too short or variance is zero.
    """
    arr = _clean(rets) if isinstance(rets, pd.Series) else _clean(pd.Series(rets))
    n = len(arr)
    if n < max(k * 2, _MIN_OBS):
        return None

    var1 = float(np.var(arr, ddof=1))
    if var1 == 0:
        return None

    # Build non-overlapping k-period returns
    # Use the largest multiple of k that fits in n
    trunc = (n // k) * k
    k_rets = arr[:trunc].reshape(-1, k).sum(axis=1)
    if len(k_rets) < 2:
        return None

    vark = float(np.var(k_rets, ddof=1))
    vr = vark / (k * var1)
    return float(vr)


def summary(rets: pd.Series) -> dict | None:
    """Distribution + regime summary for a return series.

    Returns {normal: bool, jb: float, vr: float, regime: str} where
    regime is 'trending', 'mean-reverting', or 'random'. Returns None
    when the series is too short to compute any stat.
    """
    arr = _clean(rets) if isinstance(rets, pd.Series) else _clean(pd.Series(rets))
    if len(arr) < _MIN_OBS:
        return None

    jb_stat, is_normal = jarque_bera(pd.Series(arr))
    vr = variance_ratio(pd.Series(arr))

    if jb_stat is None and vr is None:
        return None

    regime: str
    if vr is None:
        regime = "random"
    elif vr > 1.05:
        regime = "trending"
    elif vr < 0.95:
        regime = "mean-reverting"
    else:
        regime = "random"

    return {
        "normal": bool(is_normal) if is_normal is not None else False,
        "jb": round(float(jb_stat), 4) if jb_stat is not None else None,
        "vr": round(float(vr), 4) if vr is not None else None,
        "regime": regime,
    }
