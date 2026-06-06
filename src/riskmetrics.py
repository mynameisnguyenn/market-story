"""Risk/return metric bank — pure functions on a price or returns Series.

All functions accept a pandas.Series with a DatetimeIndex (daily closes or daily returns).
Every function returns None (never raises) when data is empty, too short, or degenerate.
No network, no I/O. Annualisation constant: ann=252 trading days.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

_MIN_OBS = 2  # absolute floor before most calculations are meaningless


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------


def returns(prices: pd.Series) -> pd.Series | None:
    """Simple daily returns from a price series (dropna applied first)."""
    if prices is None:
        return None
    p = prices.dropna()
    if len(p) < _MIN_OBS:
        return None
    return p.pct_change().dropna()


def max_drawdown(prices: pd.Series) -> float | None:
    """Maximum peak-to-trough drawdown as a negative fraction (e.g. -0.35)."""
    if prices is None:
        return None
    p = prices.dropna()
    if len(p) < _MIN_OBS:
        return None
    roll_max = p.cummax()
    dd = (p - roll_max) / roll_max
    worst = dd.min()
    return float(worst) if np.isfinite(worst) else None


def current_drawdown(prices: pd.Series) -> tuple[float, int] | None:
    """Depth (negative fraction) and days since the most recent peak.

    Returns (depth, days_since_peak) or None when data is insufficient.
    """
    if prices is None:
        return None
    p = prices.dropna()
    if len(p) < _MIN_OBS:
        return None
    peak_idx = p.cummax().idxmax()
    peak_val = p[peak_idx]
    last_val = p.iloc[-1]
    if peak_val == 0:
        return None
    depth = float((last_val - peak_val) / peak_val)
    # days_since_peak: number of observations after the peak
    peak_pos = p.index.get_loc(peak_idx)
    if isinstance(peak_pos, slice):
        peak_pos = peak_pos.stop - 1
    days = int(len(p) - 1 - peak_pos)
    return depth, days


def ulcer_index(prices: pd.Series) -> float | None:
    """Ulcer Index = sqrt(mean(drawdown_pct ** 2)). Penalises deep, prolonged drawdowns."""
    if prices is None:
        return None
    p = prices.dropna()
    if len(p) < _MIN_OBS:
        return None
    roll_max = p.cummax()
    dd_pct = (p - roll_max) / roll_max * 100.0  # percent, so naturally negative
    ui = float(np.sqrt(np.mean(dd_pct ** 2)))
    return ui if np.isfinite(ui) else None


# ---------------------------------------------------------------------------
# Return-distribution metrics
# ---------------------------------------------------------------------------


def tail_ratio(rets: pd.Series) -> float | None:
    """abs(95th pctile / 5th pctile) — ratio of right tail to left tail magnitude."""
    if rets is None:
        return None
    r = rets.dropna()
    if len(r) < 20:
        return None
    q5 = np.percentile(r, 5)
    q95 = np.percentile(r, 95)
    if q5 == 0:
        return None
    ratio = float(abs(q95 / q5))
    return ratio if np.isfinite(ratio) else None


def gain_to_pain(rets: pd.Series) -> float | None:
    """Gain-to-Pain = sum(rets) / abs(sum(negative rets)).

    > 1 means gains consistently exceed losses; None when no negative returns exist.
    """
    if rets is None:
        return None
    r = rets.dropna()
    if len(r) < _MIN_OBS:
        return None
    neg_sum = float(r[r < 0].sum())
    if neg_sum == 0:
        return None
    gtp = float(r.sum() / abs(neg_sum))
    return gtp if np.isfinite(gtp) else None


# ---------------------------------------------------------------------------
# Risk-adjusted return metrics
# ---------------------------------------------------------------------------


def sharpe(rets: pd.Series, ann: int = 252) -> float | None:
    """Annualised Sharpe ratio (excess return over zero risk-free rate / ann. vol)."""
    if rets is None:
        return None
    r = rets.dropna()
    if len(r) < _MIN_OBS:
        return None
    std = float(r.std(ddof=1))
    if std == 0:
        return None
    s = float(r.mean() / std * np.sqrt(ann))
    return s if np.isfinite(s) else None


def sortino(rets: pd.Series, ann: int = 252) -> float | None:
    """Annualised Sortino ratio using downside deviation (negative returns only)."""
    if rets is None:
        return None
    r = rets.dropna()
    if len(r) < _MIN_OBS:
        return None
    neg = r[r < 0]
    if len(neg) == 0:
        return None
    downside_std = float(np.sqrt(np.mean(neg ** 2)))
    if downside_std == 0:
        return None
    s = float(r.mean() / downside_std * np.sqrt(ann))
    return s if np.isfinite(s) else None


def calmar(prices: pd.Series, ann: int = 252) -> float | None:
    """Calmar ratio = CAGR / abs(max_drawdown). None when drawdown is zero."""
    if prices is None:
        return None
    p = prices.dropna()
    if len(p) < _MIN_OBS:
        return None
    n_years = len(p) / ann
    if n_years == 0:
        return None
    cagr = float((p.iloc[-1] / p.iloc[0]) ** (1 / n_years) - 1)
    mdd = max_drawdown(p)
    if mdd is None or mdd == 0:
        return None
    c = cagr / abs(mdd)
    return float(c) if np.isfinite(c) else None


# ---------------------------------------------------------------------------
# Rolling metrics
# ---------------------------------------------------------------------------


def rolling_beta(
    asset_rets: pd.Series,
    bench_rets: pd.Series,
    window: int = 60,
) -> pd.Series | None:
    """Rolling beta of asset vs benchmark over a trailing window.

    Both series are aligned on their DatetimeIndex (inner join) before rolling.
    Returns a Series of the same aligned index, or None when data is insufficient.
    """
    if asset_rets is None or bench_rets is None:
        return None
    aligned = pd.concat(
        [asset_rets.rename("a"), bench_rets.rename("b")], axis=1, join="inner"
    ).dropna()
    if len(aligned) < window:
        return None

    # Rolling cov/var via pandas Series methods — clean and vectorised:
    roll_cov = aligned["a"].rolling(window).cov(aligned["b"])
    roll_var = aligned["b"].rolling(window).var(ddof=1)
    beta = roll_cov / roll_var
    beta = beta.where(roll_var != 0)
    return beta.dropna() if len(beta.dropna()) > 0 else None


# ---------------------------------------------------------------------------
# Lookback returns
# ---------------------------------------------------------------------------


def lookback_returns(prices: pd.Series) -> dict[str, float | None] | None:
    """Trailing total returns for common horizons: 1M, 3M, 6M, YTD, 1Y.

    Each value is a fractional return (e.g. 0.12 = +12 %) or None when there
    is insufficient history to compute the window.
    """
    if prices is None:
        return None
    p = prices.dropna()
    if len(p) < _MIN_OBS:
        return None

    last = p.iloc[-1]
    last_date = p.index[-1]

    def _ret(n_approx_days: int) -> float | None:
        """Return from the close ~n trading days ago to last."""
        idx = max(0, len(p) - 1 - n_approx_days)
        prior = p.iloc[idx]
        if prior == 0:
            return None
        r = float((last - prior) / prior)
        return r if np.isfinite(r) else None

    def _ytd() -> float | None:
        year_start = pd.Timestamp(last_date.year, 1, 1)
        candidates = p[p.index < year_start]
        if candidates.empty:
            # Fall back to first available date in the year
            in_year = p[p.index >= year_start]
            if in_year.empty or in_year.iloc[0] == 0:
                return None
            r = float((last - in_year.iloc[0]) / in_year.iloc[0])
            return r if np.isfinite(r) else None
        prior = candidates.iloc[-1]
        if prior == 0:
            return None
        r = float((last - prior) / prior)
        return r if np.isfinite(r) else None

    return {
        "1M": _ret(21),
        "3M": _ret(63),
        "6M": _ret(126),
        "YTD": _ytd(),
        "1Y": _ret(252),
    }
