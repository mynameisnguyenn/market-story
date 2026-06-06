"""Kritzman financial turbulence index — a smooth probability-of-stress regime signal.

For each date t, the Mahalanobis-distance turbulence score is:
    d_t = (x_t - mu)^T * Sigma^-1 * (x_t - mu)
where mu and Sigma are estimated over a trailing `lookback` window of cross-asset
daily returns.  High d_t means today's return vector is unusual relative to its own
recent distributional history — the core of the Kritzman & Li (2010) turbulence index.

Public API
----------
turbulence(returns_df, lookback)    -> pd.Series of turbulence scores
stress_percentile(turb, window)     -> pd.Series, 0-1 rolling stress gauge
returns_from_timeline()             -> pd.DataFrame of cross-asset daily returns
from_closes(closes, ...)            -> dict with latest scalars + full series
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Minimum observations needed to estimate a stable covariance matrix.
_MIN_OBS = 30
# Columns from timeline.load_df() used as cross-asset returns inputs (best-effort;
# missing columns are silently dropped so older timeline files still work).
_TIMELINE_PRICE_COLS = ["spx", "vix", "ust10", "dxy", "wti", "copper", "gold"]


# ---------------------------------------------------------------------------
# Core turbulence score
# ---------------------------------------------------------------------------

def turbulence(returns_df: pd.DataFrame, lookback: int = 252) -> pd.Series:
    """Kritzman turbulence index over a rolling `lookback`-day window.

    Parameters
    ----------
    returns_df : DataFrame of daily cross-asset returns, DatetimeIndex.
                 NaN rows are dropped inside each window (not globally).
    lookback   : trailing window length (rows) for mu and Sigma estimation.

    Returns
    -------
    pd.Series aligned to returns_df.index; NaN where the window is too short
    or the covariance matrix is singular/degenerate.  Never raises.
    """
    if returns_df is None or returns_df.empty:
        return pd.Series(dtype=float)

    df = returns_df.copy()
    # Keep only numeric columns; drop all-NaN columns up front.
    df = df.select_dtypes(include=[np.number]).dropna(axis=1, how="all")
    if df.shape[1] == 0:
        return pd.Series(np.nan, index=returns_df.index, dtype=float)

    scores = np.full(len(df), np.nan)

    for i in range(len(df)):
        start = max(0, i - lookback + 1)
        window = df.iloc[start : i + 1].dropna(how="any")
        n, k = window.shape
        # Need _MIN_OBS rows of *estimation* history (window excludes today via [:-1]),
        # so require n-1 >= _MIN_OBS, and enough rows to estimate a k-variable covariance.
        if n < max(_MIN_OBS + 1, k + 1):
            continue
        mu = window.values[:-1].mean(axis=0)           # exclude today from estimation
        cov = np.cov(window.values[:-1], rowvar=False)
        if cov.ndim == 0:                              # scalar edge-case (k=1)
            cov = np.array([[float(cov)]])
        pinv = np.linalg.pinv(cov)                    # pseudo-inverse for stability
        x = window.values[-1] - mu                    # today's excess-return vector
        val = float(x @ pinv @ x)
        scores[i] = val if np.isfinite(val) else np.nan

    return pd.Series(scores, index=df.index, name="turbulence", dtype=float)


# ---------------------------------------------------------------------------
# Stress percentile gauge (0-1 rolling rank of turbulence)
# ---------------------------------------------------------------------------

def stress_percentile(turb: pd.Series, window: int = 252) -> pd.Series:
    """Rolling percentile of turbulence scores; output is in [0, 1].

    A value of 0.9 means today's turbulence exceeds 90 % of the trailing
    `window` observations — a compact, unit-less stress gauge.
    NaN-safe; returns NaN where fewer than 2 non-NaN values exist in window.
    """
    if turb is None or turb.empty:
        return pd.Series(dtype=float)

    def _pct(arr: np.ndarray) -> float:
        clean = arr[~np.isnan(arr)]
        if len(clean) < 2:
            return np.nan
        # Rank of the last element within the window (excluding itself).
        target = clean[-1]
        below = np.sum(clean[:-1] < target)
        denom = len(clean) - 1
        return float(below / denom) if denom > 0 else np.nan

    result = turb.rolling(window=window, min_periods=2).apply(_pct, raw=True)
    result.name = "stress_pct"
    return result


# ---------------------------------------------------------------------------
# Timeline helper — build returns_df from src.timeline.load_df()
# ---------------------------------------------------------------------------

def returns_from_timeline() -> pd.DataFrame:
    """Load timeline price levels and compute daily returns for turbulence input.

    Uses src.timeline.load_df(); returns an empty DataFrame if the timeline is
    absent or too short.  Only columns listed in _TIMELINE_PRICE_COLS that
    actually exist in the timeline are included (graceful degradation).
    """
    try:
        from src import timeline          # local import — no I/O at module load
        df = timeline.load_df()
    except Exception:
        return pd.DataFrame()

    if df is None or df.empty:
        return pd.DataFrame()

    cols = [c for c in _TIMELINE_PRICE_COLS if c in df.columns]
    if not cols:
        return pd.DataFrame()

    levels = df[cols].apply(pd.to_numeric, errors="coerce")
    rets = levels.pct_change()
    # Drop rows where ALL selected columns are NaN.
    rets = rets.dropna(how="all")
    return rets


# ---------------------------------------------------------------------------
# Convenience: compute both signals from a brief's closes dict
# ---------------------------------------------------------------------------

def from_closes(
    closes: dict,
    lookback: int = 252,
    pct_window: int = 252,
) -> dict | None:
    """Compute turbulence + stress_pct from a {symbol: price Series} closes dict.

    Converts closes to a returns DataFrame, runs turbulence() and
    stress_percentile(), and returns the latest scalar values.
    Returns None if data is insufficient.  Never raises.
    """
    if not closes:
        return None

    try:
        frames = {}
        for sym, series in closes.items():
            s = pd.Series(series).dropna()
            if len(s) > 1:
                frames[sym] = s.pct_change().dropna()

        if not frames:
            return None

        ret_df = pd.DataFrame(frames).dropna(how="all")
        if ret_df.empty:
            return None

        turb = turbulence(ret_df, lookback=lookback)
        stress = stress_percentile(turb, window=pct_window)

        last_turb = turb.dropna().iloc[-1] if not turb.dropna().empty else None
        last_stress = stress.dropna().iloc[-1] if not stress.dropna().empty else None

        return {
            "turbulence": round(float(last_turb), 4) if last_turb is not None else None,
            "stress_pct": round(float(last_stress), 4) if last_stress is not None else None,
            "turb_series": turb,
            "stress_series": stress,
        }
    except Exception:
        return None
