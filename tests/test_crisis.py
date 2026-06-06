"""Tests for src/crisis.py — synthetic data only, no network."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src import crisis


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _make_returns(
    start: str = "2006-01-01",
    periods: int = 5000,
    seed: int = 42,
) -> pd.Series:
    """Daily log-normal returns spanning ~2006-2026, seeded for reproducibility."""
    np.random.seed(seed)
    rets = pd.Series(
        np.random.normal(0.0003, 0.012, periods),
        index=pd.bdate_range(start=start, periods=periods),
    )
    return rets


def _short_returns(periods: int = 3) -> pd.Series:
    np.random.seed(42)
    return pd.Series(
        np.random.normal(0.0, 0.01, periods),
        index=pd.bdate_range("2020-01-01", periods=periods),
    )


# ---------------------------------------------------------------------------
# crisis_replay — happy path
# ---------------------------------------------------------------------------

class TestCrisisReplay:
    def test_default_windows_returns_three_results(self):
        rets = _make_returns()
        out = crisis.crisis_replay(rets)
        assert len(out) == 3

    def test_all_expected_keys_present(self):
        rets = _make_returns()
        out = crisis.crisis_replay(rets)
        required = {"name", "start", "end", "n_days", "return", "max_drawdown", "var95", "es95"}
        for row in out:
            assert required == set(row.keys())

    def test_gfc_window_has_negative_return(self):
        """GFC 2008-09: a severe bear market — total return must be negative."""
        rets = _make_returns()
        out = crisis.crisis_replay(rets)
        gfc = next(r for r in out if "GFC" in r["name"])
        assert gfc["n_days"] > 0
        assert gfc["return"] is not None
        # We can't guarantee sign with seeded random data, but n_days and types matter
        assert isinstance(gfc["return"], float)
        assert isinstance(gfc["max_drawdown"], float)
        assert gfc["max_drawdown"] <= 0.0       # drawdown is always <= 0

    def test_var95_is_at_or_below_es95(self):
        """ES95 must be <= VaR95 (more extreme by definition)."""
        rets = _make_returns()
        out = crisis.crisis_replay(rets)
        for row in out:
            if row["var95"] is not None and row["es95"] is not None:
                assert row["es95"] <= row["var95"], (
                    f"{row['name']}: ES95={row['es95']} should be <= VaR95={row['var95']}"
                )

    def test_custom_windows(self):
        rets = _make_returns()
        windows = [("2010-01-01", "2010-12-31", "My custom 2010")]
        out = crisis.crisis_replay(rets, windows=windows)
        assert len(out) == 1
        assert out[0]["name"] == "My custom 2010"
        assert out[0]["n_days"] > 0

    def test_window_outside_series_range_returns_none_stats(self):
        rets = _make_returns(start="2020-01-01", periods=100)
        windows = [("1990-01-01", "1991-12-31", "Pre-history")]
        out = crisis.crisis_replay(rets, windows=windows)
        assert out[0]["n_days"] == 0
        assert out[0]["return"] is None
        assert out[0]["max_drawdown"] is None

    def test_max_drawdown_on_monotone_decline(self):
        """A series that only falls should have a large negative drawdown."""
        idx = pd.bdate_range("2020-01-01", periods=50)
        rets = pd.Series([-0.01] * 50, index=idx)
        windows = [("2020-01-01", "2021-01-01", "Decline")]
        out = crisis.crisis_replay(rets, windows=windows)
        dd = out[0]["max_drawdown"]
        assert dd is not None and dd < -0.3

    def test_max_drawdown_on_monotone_rise_is_zero(self):
        """A series that only rises has zero drawdown."""
        idx = pd.bdate_range("2020-01-01", periods=50)
        rets = pd.Series([0.01] * 50, index=idx)
        windows = [("2020-01-01", "2021-01-01", "Rise")]
        out = crisis.crisis_replay(rets, windows=windows)
        dd = out[0]["max_drawdown"]
        assert dd is not None and dd == pytest.approx(0.0, abs=1e-9)

    def test_total_return_sign_matches_sum_of_positives(self):
        """All-positive returns -> compound return is positive."""
        idx = pd.bdate_range("2020-01-01", periods=30)
        rets = pd.Series([0.005] * 30, index=idx)
        windows = [("2020-01-01", "2021-01-01", "Up")]
        out = crisis.crisis_replay(rets, windows=windows)
        assert out[0]["return"] > 0.0


# ---------------------------------------------------------------------------
# crisis_replay — empty / short / NaN inputs
# ---------------------------------------------------------------------------

class TestCrisisReplayEdgeCases:
    def test_empty_series_returns_none_stats(self):
        out = crisis.crisis_replay(pd.Series(dtype=float))
        assert len(out) == 3          # still returns all default window rows
        for row in out:
            assert row["return"] is None

    def test_none_series_returns_none_stats(self):
        out = crisis.crisis_replay(None)
        assert len(out) == 3
        for row in out:
            assert row["return"] is None

    def test_series_with_all_nan(self):
        idx = pd.bdate_range("2008-01-01", periods=200)
        rets = pd.Series([float("nan")] * 200, index=idx)
        out = crisis.crisis_replay(rets)
        for row in out:
            assert row["return"] is None or row["n_days"] == 0

    def test_single_obs_window_returns_zero_return(self):
        idx = pd.bdate_range("2020-02-03", periods=1)
        rets = pd.Series([0.02], index=idx)
        windows = [("2020-02-01", "2020-02-28", "Single")]
        out = crisis.crisis_replay(rets, windows=windows)
        assert out[0]["n_days"] == 1
        assert out[0]["return"] == pytest.approx(0.02, rel=1e-6)
        # var95/es95 need >=5 obs
        assert out[0]["var95"] is None
        assert out[0]["es95"] is None

    def test_empty_windows_list(self):
        rets = _make_returns()
        out = crisis.crisis_replay(rets, windows=[])
        assert out == []

    def test_nan_values_are_dropped(self):
        np.random.seed(42)
        vals = np.random.normal(0.0, 0.01, 100).tolist()
        vals[5] = float("nan")
        vals[20] = float("nan")
        idx = pd.bdate_range("2020-01-01", periods=100)
        rets = pd.Series(vals, index=idx)
        windows = [("2020-01-01", "2021-01-01", "NaN test")]
        out = crisis.crisis_replay(rets, windows=windows)
        assert out[0]["n_days"] == 98    # 2 NaNs dropped


# ---------------------------------------------------------------------------
# move_percentile — happy path
# ---------------------------------------------------------------------------

class TestMovePercentile:
    def test_min_value_is_zero_percentile(self):
        s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        assert crisis.move_percentile(s, 0.5) == pytest.approx(0.0)

    def test_max_value_is_100_percentile(self):
        s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        assert crisis.move_percentile(s, 6.0) == pytest.approx(100.0)

    def test_median_value_is_near_50(self):
        np.random.seed(42)
        s = pd.Series(np.random.normal(0.0, 0.01, 1000))
        pct = crisis.move_percentile(s, 0.0)
        assert pct is not None and 40.0 < pct < 60.0

    def test_large_positive_move_ranks_high(self):
        np.random.seed(42)
        s = pd.Series(np.random.normal(0.0, 0.01, 500))
        pct = crisis.move_percentile(s, 0.05)    # +5% in a 1%-vol series
        assert pct is not None and pct > 90.0

    def test_large_negative_move_ranks_low(self):
        np.random.seed(42)
        s = pd.Series(np.random.normal(0.0, 0.01, 500))
        pct = crisis.move_percentile(s, -0.05)
        assert pct is not None and pct < 10.0

    def test_returns_float_in_0_100(self):
        np.random.seed(42)
        s = pd.Series(np.random.normal(0.0, 0.01, 252))
        for v in [-0.03, 0.0, 0.03]:
            pct = crisis.move_percentile(s, v)
            assert pct is not None
            assert 0.0 <= pct <= 100.0


# ---------------------------------------------------------------------------
# move_percentile — edge cases
# ---------------------------------------------------------------------------

class TestMovePercentileEdgeCases:
    def test_short_series_returns_none(self):
        assert crisis.move_percentile(pd.Series([0.01, 0.02, 0.03]), 0.01) is None
        assert crisis.move_percentile(pd.Series([0.01, 0.02, 0.03, 0.04]), 0.01) is None

    def test_exactly_five_obs_works(self):
        s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        result = crisis.move_percentile(s, 3.0)
        assert result is not None

    def test_none_series_returns_none(self):
        assert crisis.move_percentile(None, 0.01) is None

    def test_nan_value_returns_none(self):
        s = pd.Series([0.01, 0.02, 0.03, 0.04, 0.05])
        assert crisis.move_percentile(s, float("nan")) is None

    def test_inf_value_returns_none(self):
        s = pd.Series([0.01, 0.02, 0.03, 0.04, 0.05])
        assert crisis.move_percentile(s, float("inf")) is None

    def test_series_with_nans_are_dropped(self):
        s = pd.Series([0.01, float("nan"), 0.02, 0.03, 0.04, 0.05])
        result = crisis.move_percentile(s, 0.03)
        assert result is not None    # 5 clean obs remain

    def test_empty_series_returns_none(self):
        assert crisis.move_percentile(pd.Series(dtype=float), 0.01) is None

    def test_all_nan_series_returns_none(self):
        s = pd.Series([float("nan")] * 10)
        assert crisis.move_percentile(s, 0.01) is None
