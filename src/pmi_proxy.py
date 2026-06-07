"""PMI-like diffusion index from FRED price/level series.

A synthetic PMI proxy: normalise each series' momentum by its own rolling
volatility, clip to [-3, 3], then scale into [0, 100] centred at 50.
>50 = expansion / acceleration; <50 = contraction / deceleration.
Pure numpy/pandas; no network or I/O.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _validate(series: pd.Series, window: int) -> pd.Series | None:
    """Return a clean (dropna) Series, or None if too short."""
    if series is None or not isinstance(series, pd.Series):
        return None
    s = series.dropna()
    if len(s) < window + 1:
        return None
    return s


def _rolling_std(values: np.ndarray, window: int) -> np.ndarray:
    """Pure-numpy rolling std (ddof=0); NaN for the first `window-1` positions."""
    n = len(values)
    out = np.full(n, np.nan)
    for i in range(window - 1, n):
        chunk = values[i - window + 1: i + 1]
        out[i] = chunk.std()
    return out


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def to_diffusion_index(
    series: pd.Series,
    window: int = 12,
) -> tuple[float | None, pd.Series | None]:
    """Convert a price/level series to a PMI-like diffusion index.

    Steps: pct_change -> clip(/ rolling_std, -3, 3) -> 50 + scaled*10 -> clip(0, 100).
    Returns (latest_value, full_series) or (None, None) on bad input.
    """
    s = _validate(series, window)
    if s is None:
        return None, None

    values = s.values.astype(float)

    # Percent changes (length = n-1)
    pct = np.diff(values) / np.where(values[:-1] != 0, values[:-1], np.nan)

    rstd = _rolling_std(pct, window)

    # Avoid division by zero / NaN std
    with np.errstate(invalid="ignore", divide="ignore"):
        scaled = np.where(
            (rstd > 0) & np.isfinite(rstd),
            pct / rstd,
            np.nan,
        )

    scaled = np.clip(scaled, -3.0, 3.0)
    diffusion = np.clip(50.0 + scaled * 10.0, 0.0, 100.0)

    # Align with the original index (pct_change loses one row)
    idx = s.index[1:]
    result = pd.Series(diffusion, index=idx, name="diffusion")

    # Drop leading NaNs produced by rolling warm-up
    result = result.dropna()
    if result.empty:
        return None, None

    latest = float(result.iloc[-1])
    return latest, result


def composite_pmi(
    series_by_name: dict[str, pd.Series],
    weights: dict[str, float] | None = None,
    window: int = 12,
) -> float | None:
    """Weighted-average diffusion index across multiple series.

    Equal weights by default. Returns None when no series yields a valid value.
    Missing or short series are silently dropped; remaining weights are renormalised.
    """
    if not series_by_name:
        return None

    names = list(series_by_name.keys())

    # Default: equal weights
    if weights is None:
        weights = {n: 1.0 for n in names}

    values: list[float] = []
    ws: list[float] = []

    for name in names:
        w = weights.get(name, 1.0)
        if w <= 0:
            continue
        latest, _ = to_diffusion_index(series_by_name[name], window)
        if latest is None:
            continue
        values.append(latest)
        ws.append(w)

    if not values:
        return None

    ws_arr = np.array(ws, dtype=float)
    ws_arr /= ws_arr.sum()                     # renormalise to 1
    return float(np.dot(ws_arr, values))


def composite_index(
    series_by_name: dict[str, pd.Series],
    invert: set[str] | None = None,
    window: int = 12,
) -> tuple[float | None, pd.Series | None]:
    """A composite PMI-proxy diffusion SERIES (not just the latest scalar) from a basket of
    level series — for charting the growth pulse over time.

    Each input is resampled to month-end (last obs in month, so weekly + monthly series align),
    converted to a diffusion index, and — for the 'bad-when-rising' members named in `invert`
    (e.g. jobless claims) — reflected around 50 (d -> 100 - d) so rising = contraction. The
    component diffusion series are then inner-joined on their common months and averaged.
    Returns (latest, composite_series) or (None, None) when nothing usable remains.
    """
    invert = invert or set()
    diffs: dict[str, pd.Series] = {}
    for name, s in series_by_name.items():
        if s is None or not isinstance(s, pd.Series) or s.empty:
            continue
        m = s.dropna()
        if not isinstance(m.index, pd.DatetimeIndex):
            continue
        # Month-end resample without depending on the "M"/"ME" alias churn across pandas versions.
        m = m.groupby(m.index.to_period("M")).last()
        m.index = m.index.to_timestamp()
        _, d = to_diffusion_index(m, window)
        if d is None:
            continue
        diffs[name] = (100.0 - d) if name in invert else d
    if not diffs:
        return None, None
    frame = pd.DataFrame(diffs).dropna()
    if frame.empty:
        return None, None
    comp = frame.mean(axis=1)
    return float(comp.iloc[-1]), comp
