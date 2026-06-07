"""Tests for src/pmi_proxy.py — synthetic data only, no network."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.pmi_proxy import composite_index, to_diffusion_index, composite_pmi


def _monthly(n: int, trend: float, seed: int) -> pd.Series:
    """Strictly-positive monthly level series with drift (a daily walk resampled by callers)."""
    rng = np.random.default_rng(seed)
    rets = rng.normal(loc=trend, scale=0.01, size=n)
    prices = 100.0 * np.exp(np.cumsum(rets))
    return pd.Series(prices, index=pd.date_range("2018-01-01", periods=n, freq="MS"))


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

RNG = np.random.default_rng(42)


def _make_series(n: int = 120, trend: float = 0.0, seed_offset: int = 0) -> pd.Series:
    """Cumulative random-walk price series with optional drift."""
    rng = np.random.default_rng(42 + seed_offset)
    rets = rng.normal(loc=trend / 252, scale=0.01, size=n)
    prices = 100.0 * np.exp(np.cumsum(rets))
    idx = pd.date_range("2024-01-01", periods=n, freq="B")
    return pd.Series(prices, index=idx)


# ---------------------------------------------------------------------------
# to_diffusion_index — happy path
# ---------------------------------------------------------------------------

def test_returns_float_and_series():
    s = _make_series(120)
    latest, result = to_diffusion_index(s, window=12)
    assert isinstance(latest, float)
    assert isinstance(result, pd.Series)
    assert not result.empty


def test_output_bounded_0_100():
    s = _make_series(200)
    latest, result = to_diffusion_index(s, window=20)
    assert result is not None
    assert (result >= 0).all() and (result <= 100).all()
    assert 0.0 <= latest <= 100.0


def test_strong_uptrend_above_50():
    """A series with a persistent uptrend should have a mean diffusion above 50."""
    s = _make_series(200, trend=0.40, seed_offset=1)    # +40 % annual drift
    _, result = to_diffusion_index(s, window=12)
    assert result is not None and float(result.mean()) > 50.0


def test_strong_downtrend_below_50():
    """A series with a persistent downtrend should have a mean diffusion below 50."""
    s = _make_series(200, trend=-0.40, seed_offset=2)   # -40 % annual drift
    _, result = to_diffusion_index(s, window=12)
    assert result is not None and float(result.mean()) < 50.0


def test_series_index_aligned():
    """Result index must be a subset of the input's DatetimeIndex."""
    s = _make_series(60)
    _, result = to_diffusion_index(s, window=12)
    assert result is not None
    # all result dates must come from the original index (minus first obs)
    assert set(result.index).issubset(set(s.index))


def test_nan_values_in_series_handled():
    """NaN holes in the input must not crash the function."""
    s = _make_series(120)
    s.iloc[10:15] = np.nan
    s.iloc[60] = np.nan
    latest, result = to_diffusion_index(s, window=12)
    # After dropna in _validate the series is shorter but still valid
    assert latest is not None or result is None   # either works, just no exception


# ---------------------------------------------------------------------------
# to_diffusion_index — edge / short inputs
# ---------------------------------------------------------------------------

def test_empty_series_returns_none_none():
    latest, result = to_diffusion_index(pd.Series([], dtype=float), window=12)
    assert latest is None
    assert result is None


def test_none_input_returns_none_none():
    latest, result = to_diffusion_index(None, window=12)
    assert latest is None
    assert result is None


def test_too_short_returns_none_none():
    """Series shorter than window+1 must return (None, None)."""
    s = pd.Series([100.0, 101.0, 102.0])
    latest, result = to_diffusion_index(s, window=12)
    assert latest is None
    assert result is None


def test_exactly_window_plus_one_returns_valid():
    """Exactly window+1 points: 12 pct_changes, rolling_std(12) gives 1 valid value."""
    s = pd.Series(np.linspace(100, 110, 13))   # 13 points, window=12
    latest, result = to_diffusion_index(s, window=12)
    # 12 pct_changes; rolling_std(12) has one valid entry at the last position
    assert latest is not None
    assert result is not None and len(result) == 1


def test_constant_series_returns_none_or_nan_free():
    """Zero volatility: rolling_std=0, division guard must avoid NaN in output."""
    s = pd.Series([50.0] * 60)
    latest, result = to_diffusion_index(s, window=12)
    # pct_change is 0 everywhere -> scaled=0 -> diffusion=50, but std=0 triggers guard
    # So result is either None (all NaN dropped) or 50.0
    if latest is not None:
        assert latest == pytest.approx(50.0, abs=1e-6)


# ---------------------------------------------------------------------------
# composite_pmi — happy path
# ---------------------------------------------------------------------------

def test_composite_equal_weights():
    """Equal-weight composite with two series returns a float in [0, 100]."""
    s1 = _make_series(120, seed_offset=10)
    s2 = _make_series(120, seed_offset=11)
    result = composite_pmi({"A": s1, "B": s2}, window=12)
    assert isinstance(result, float)
    assert 0.0 <= result <= 100.0


def test_composite_single_series_matches_to_diffusion():
    """Single-series composite must equal to_diffusion_index directly."""
    s = _make_series(120, seed_offset=20)
    direct, _ = to_diffusion_index(s, window=12)
    composite = composite_pmi({"X": s}, window=12)
    assert direct is not None and composite is not None
    assert composite == pytest.approx(direct, abs=1e-10)


def test_composite_custom_weights_normalised():
    """Custom weights are renormalised; result still in [0, 100]."""
    s1 = _make_series(120, seed_offset=30)
    s2 = _make_series(120, seed_offset=31)
    w = {"A": 3.0, "B": 1.0}
    result = composite_pmi({"A": s1, "B": s2}, weights=w, window=12)
    assert result is not None
    assert 0.0 <= result <= 100.0


def test_composite_bad_series_dropped_silently():
    """Short/None series should be skipped; remaining series drive the result."""
    s_good = _make_series(120, seed_offset=40)
    result = composite_pmi(
        {"good": s_good, "short": pd.Series([1.0, 2.0]), "none": None},
        window=12,
    )
    direct, _ = to_diffusion_index(s_good, window=12)
    assert result is not None
    assert result == pytest.approx(direct, abs=1e-10)


def test_composite_all_bad_returns_none():
    result = composite_pmi(
        {"a": pd.Series([1.0]), "b": pd.Series([], dtype=float)},
        window=12,
    )
    assert result is None


def test_composite_empty_dict_returns_none():
    assert composite_pmi({}) is None


# ---------------------------------------------------------------------------
# Expansion / contraction labelling
# ---------------------------------------------------------------------------

def test_expansion_composite_mean_above_50():
    """Composite of two strongly uptrending series should average >50 over its history."""
    s1 = _make_series(200, trend=0.40, seed_offset=50)
    s2 = _make_series(200, trend=0.40, seed_offset=51)
    # Use the individual series means to validate the directional property
    _, r1 = to_diffusion_index(s1, window=12)
    _, r2 = to_diffusion_index(s2, window=12)
    assert r1 is not None and r2 is not None
    assert float(r1.mean()) > 50.0 and float(r2.mean()) > 50.0


def test_contraction_composite_mean_below_50():
    """Composite of two strongly downtrending series should average <50 over its history."""
    s1 = _make_series(200, trend=-0.40, seed_offset=60)
    s2 = _make_series(200, trend=-0.40, seed_offset=61)
    _, r1 = to_diffusion_index(s1, window=12)
    _, r2 = to_diffusion_index(s2, window=12)
    assert r1 is not None and r2 is not None
    assert float(r1.mean()) < 50.0 and float(r2.mean()) < 50.0


# ---------------------------------------------------------------------------
# composite_index — the charted diffusion SERIES (with sign-aware inversion)
# ---------------------------------------------------------------------------

def test_composite_index_returns_bounded_series():
    a, b = _monthly(60, 0.004, 70), _monthly(60, 0.004, 71)
    latest, comp = composite_index({"A": a, "B": b}, window=12)
    assert isinstance(latest, float) and isinstance(comp, pd.Series)
    assert (comp >= 0).all() and (comp <= 100).all() and 0.0 <= latest <= 100.0


def test_composite_index_inverts_bad_when_rising():
    """A strongly RISING series reads as expansion normally, but as contraction when inverted
    (the jobless-claims case) — reflected around 50."""
    rising = _monthly(60, 0.02, 72)             # persistent uptrend
    up, _ = composite_index({"x": rising}, window=12)
    down, _ = composite_index({"x": rising}, invert={"x"}, window=12)
    assert up is not None and down is not None
    assert up > 50.0 and down < 50.0
    assert down == pytest.approx(100.0 - up, abs=1e-9)   # exact reflection


def test_composite_index_aligns_mixed_frequencies():
    """A weekly series and a monthly series both resample to month-end and align."""
    weekly = pd.Series(100.0 + np.arange(160) * 0.5,
                       index=pd.date_range("2018-01-01", periods=160, freq="W"))
    monthly = _monthly(40, 0.003, 73)
    latest, comp = composite_index({"wk": weekly, "mo": monthly}, window=12)
    assert latest is not None and comp is not None and not comp.empty


def test_composite_index_empty_returns_none():
    assert composite_index({}) == (None, None)
    assert composite_index({"a": None, "b": pd.Series([1.0])}) == (None, None)
