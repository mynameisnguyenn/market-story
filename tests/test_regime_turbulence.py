"""Tests for src/regime_turbulence.py — synthetic data only, no network."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.regime_turbulence import (
    turbulence,
    stress_percentile,
    from_closes,
    _MIN_OBS,
)


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _make_returns(n: int = 300, k: int = 4, seed: int = 42) -> pd.DataFrame:
    """k-asset synthetic daily returns DataFrame with a business-day DatetimeIndex."""
    rng = np.random.RandomState(seed)
    data = rng.randn(n, k) * 0.01
    idx = pd.date_range("2023-01-02", periods=n, freq="B")
    return pd.DataFrame(data, index=idx, columns=[f"asset_{i}" for i in range(k)])


def _make_shock(returns_df: pd.DataFrame, magnitude: float = 10.0) -> pd.DataFrame:
    """Return a copy with a large shock injected on the last row."""
    df = returns_df.copy()
    df.iloc[-1] = df.iloc[-1] * magnitude
    return df


# ---------------------------------------------------------------------------
# turbulence()
# ---------------------------------------------------------------------------

class TestTurbulence:
    def test_happy_path_returns_series_same_length(self):
        df = _make_returns()
        result = turbulence(df, lookback=60)
        assert isinstance(result, pd.Series)
        assert len(result) == len(df)

    def test_index_preserved(self):
        df = _make_returns()
        result = turbulence(df, lookback=60)
        assert result.index.equals(df.index)

    def test_nan_before_min_observations(self):
        df = _make_returns(n=200)
        result = turbulence(df, lookback=60)
        # The first _MIN_OBS rows (at minimum) must be NaN — window too short.
        assert result.iloc[:_MIN_OBS].isna().all()

    def test_non_negative_after_warmup(self):
        df = _make_returns(n=200)
        result = turbulence(df, lookback=60)
        valid = result.dropna()
        assert len(valid) > 0
        assert (valid >= 0).all()

    def test_shock_produces_higher_turbulence(self):
        df = _make_returns(n=200, seed=42)
        normal_t = turbulence(df, lookback=60)
        shocked_df = _make_shock(df, magnitude=15.0)
        shocked_t = turbulence(shocked_df, lookback=60)
        last_normal = normal_t.dropna().iloc[-1]
        last_shocked = shocked_t.dropna().iloc[-1]
        assert last_shocked > last_normal

    def test_empty_dataframe_returns_empty_series(self):
        result = turbulence(pd.DataFrame(), lookback=60)
        assert isinstance(result, pd.Series)
        assert result.empty

    def test_none_input_returns_empty_series(self):
        result = turbulence(None, lookback=60)
        assert isinstance(result, pd.Series)
        assert result.empty

    def test_single_row_is_nan(self):
        df = _make_returns(n=1)
        result = turbulence(df, lookback=60)
        assert len(result) == 1
        assert result.isna().all()

    def test_short_series_below_min_obs_all_nan(self):
        df = _make_returns(n=_MIN_OBS - 1)
        result = turbulence(df, lookback=60)
        assert result.isna().all()

    def test_single_asset_column_does_not_raise(self):
        """Degenerate single-column case should not raise."""
        rng = np.random.RandomState(7)
        df = pd.DataFrame(
            {"a": rng.randn(100) * 0.01},
            index=pd.date_range("2024-01-01", periods=100, freq="B"),
        )
        result = turbulence(df, lookback=50)
        assert isinstance(result, pd.Series)

    def test_all_nan_column_dropped_gracefully(self):
        df = _make_returns(n=150, k=3)
        df["nan_col"] = np.nan
        result = turbulence(df, lookback=60)
        assert isinstance(result, pd.Series)
        assert len(result) == len(df)

    def test_name_is_turbulence(self):
        df = _make_returns(n=150)
        result = turbulence(df, lookback=60)
        assert result.name == "turbulence"


# ---------------------------------------------------------------------------
# stress_percentile()
# ---------------------------------------------------------------------------

class TestStressPercentile:
    def test_output_in_0_1(self):
        df = _make_returns(n=300)
        turb = turbulence(df, lookback=60)
        sp = stress_percentile(turb, window=120)
        valid = sp.dropna()
        assert len(valid) > 0
        assert (valid >= 0.0).all() and (valid <= 1.0).all()

    def test_shocked_row_near_top_of_distribution(self):
        df = _make_returns(n=300, seed=42)
        shocked_df = _make_shock(df, magnitude=20.0)
        turb = turbulence(shocked_df, lookback=60)
        sp = stress_percentile(turb, window=120)
        last_sp = sp.dropna().iloc[-1]
        assert last_sp > 0.80, f"Expected high stress percentile, got {last_sp}"

    def test_empty_series_returns_empty(self):
        result = stress_percentile(pd.Series(dtype=float))
        assert result.empty

    def test_none_returns_empty(self):
        result = stress_percentile(None)
        assert result.empty

    def test_name_is_stress_pct(self):
        df = _make_returns(n=150)
        turb = turbulence(df, lookback=60)
        sp = stress_percentile(turb)
        assert sp.name == "stress_pct"

    def test_short_series_produces_nan(self):
        tiny = pd.Series([1.0], index=pd.date_range("2024-01-01", periods=1))
        result = stress_percentile(tiny, window=60)
        assert result.isna().all()

    def test_monotone_turb_yields_high_stress_at_end(self):
        """A monotonically rising turbulence series should yield high stress near end."""
        n = 200
        idx = pd.date_range("2023-01-02", periods=n, freq="B")
        turb = pd.Series(np.linspace(0.1, 10.0, n), index=idx, name="turbulence")
        sp = stress_percentile(turb, window=100)
        valid = sp.dropna()
        assert valid.iloc[-1] > 0.9

    def test_constant_series_stress_is_nan_or_zero(self):
        """Constant turbulence has no variation — percentile is 0 (nothing below it)."""
        n = 100
        idx = pd.date_range("2024-01-01", periods=n, freq="B")
        turb = pd.Series(np.ones(n) * 2.5, index=idx, name="turbulence")
        sp = stress_percentile(turb, window=60)
        valid = sp.dropna()
        if len(valid) > 0:
            assert (valid == 0.0).all()


# ---------------------------------------------------------------------------
# from_closes()
# ---------------------------------------------------------------------------

class TestFromCloses:
    def _make_closes(self, n: int = 300, seed: int = 42) -> dict:
        rng = np.random.RandomState(seed)
        idx = pd.date_range("2023-01-02", periods=n, freq="B")
        return {
            "^GSPC": pd.Series(100 * np.cumprod(1 + rng.randn(n) * 0.01), index=idx),
            "^VIX": pd.Series(15 + rng.randn(n) * 2, index=idx),
            "DX-Y.NYB": pd.Series(100 + rng.randn(n) * 0.5, index=idx),
        }

    def test_happy_path_returns_dict(self):
        closes = self._make_closes()
        result = from_closes(closes, lookback=60, pct_window=120)
        assert isinstance(result, dict)
        assert "turbulence" in result
        assert "stress_pct" in result

    def test_scalars_are_floats_or_none(self):
        closes = self._make_closes()
        result = from_closes(closes, lookback=60, pct_window=120)
        assert result is not None
        t_val = result["turbulence"]
        sp_val = result["stress_pct"]
        assert t_val is None or isinstance(t_val, float)
        assert sp_val is None or isinstance(sp_val, float)

    def test_series_keys_are_present(self):
        closes = self._make_closes()
        result = from_closes(closes, lookback=60, pct_window=120)
        assert result is not None
        assert isinstance(result["turb_series"], pd.Series)
        assert isinstance(result["stress_series"], pd.Series)

    def test_empty_closes_returns_none(self):
        assert from_closes({}) is None

    def test_none_closes_returns_none(self):
        assert from_closes(None) is None

    def test_too_short_closes_returns_none_or_none_scalars(self):
        rng = np.random.RandomState(0)
        idx = pd.date_range("2024-01-01", periods=5, freq="B")
        closes = {"^GSPC": pd.Series(100 + rng.randn(5), index=idx)}
        result = from_closes(closes, lookback=60)
        if result is not None:
            assert result["turbulence"] is None
            assert result["stress_pct"] is None

    def test_series_with_leading_nan_handled(self):
        rng = np.random.RandomState(3)
        n = 200
        idx = pd.date_range("2023-06-01", periods=n, freq="B")
        prices = pd.Series(100 + rng.randn(n).cumsum(), index=idx)
        prices.iloc[:10] = np.nan
        result = from_closes({"asset": prices}, lookback=60)
        # Should not raise regardless of result.
        assert result is None or isinstance(result, dict)

    def test_turbulence_scalar_is_non_negative(self):
        closes = self._make_closes(n=300)
        result = from_closes(closes, lookback=60, pct_window=120)
        if result is not None and result["turbulence"] is not None:
            assert result["turbulence"] >= 0.0

    def test_stress_pct_between_0_and_1(self):
        closes = self._make_closes(n=300)
        result = from_closes(closes, lookback=60, pct_window=120)
        if result is not None and result["stress_pct"] is not None:
            assert 0.0 <= result["stress_pct"] <= 1.0
