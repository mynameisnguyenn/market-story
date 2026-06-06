"""Tests for src/statistical.py — distribution + trend/mean-reversion flags.

All data is synthetic (np.random.seed(42)); no network calls.
"""
import math

import numpy as np
import pandas as pd
import pytest

from src import statistical


RNG = np.random.default_rng(42)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _normal_rets(n: int = 500) -> pd.Series:
    """Gaussian returns — should be close to normal."""
    rng = np.random.RandomState(42)
    return pd.Series(rng.normal(0, 0.01, n))


def _fat_rets(n: int = 500) -> pd.Series:
    """Student-t (df=3) returns — heavy tails, non-normal."""
    rng = np.random.RandomState(42)
    return pd.Series(rng.standard_t(df=3, size=n) * 0.01)


def _trending_rets(n: int = 200) -> pd.Series:
    """Positively autocorrelated returns — momentum / trending series."""
    rng = np.random.RandomState(42)
    noise = rng.normal(0, 0.005, n)
    # AR(1) with phi=0.6 -> strong positive autocorrelation
    arr = np.zeros(n)
    arr[0] = noise[0]
    for i in range(1, n):
        arr[i] = 0.6 * arr[i - 1] + noise[i]
    return pd.Series(arr)


def _mean_rev_rets(n: int = 200) -> pd.Series:
    """Negatively autocorrelated returns — mean-reverting series."""
    rng = np.random.RandomState(42)
    noise = rng.normal(0, 0.005, n)
    arr = np.zeros(n)
    arr[0] = noise[0]
    for i in range(1, n):
        arr[i] = -0.6 * arr[i - 1] + noise[i]
    return pd.Series(arr)


# ---------------------------------------------------------------------------
# jarque_bera
# ---------------------------------------------------------------------------

class TestJarqueBera:
    def test_normal_data_fails_to_reject(self):
        stat, is_normal = statistical.jarque_bera(_normal_rets())
        assert stat is not None
        assert is_normal is True   # Gaussian => fail to reject normality

    def test_fat_tails_reject_normality(self):
        stat, is_normal = statistical.jarque_bera(_fat_rets())
        assert stat is not None
        assert is_normal is False  # heavy tails => reject normality

    def test_empty_series_returns_none(self):
        result = statistical.jarque_bera(pd.Series([], dtype=float))
        assert result == (None, None)

    def test_short_series_returns_none(self):
        result = statistical.jarque_bera(pd.Series([0.01, -0.01, 0.02]))
        assert result == (None, None)

    def test_nan_values_are_dropped(self):
        rets = _normal_rets(300)
        rets_with_nan = rets.copy()
        rets_with_nan.iloc[::10] = np.nan
        stat, is_normal = statistical.jarque_bera(rets_with_nan)
        assert stat is not None
        assert isinstance(is_normal, bool)

    def test_stat_is_non_negative(self):
        stat, _ = statistical.jarque_bera(_normal_rets())
        assert stat >= 0.0

    def test_constant_series_returns_none(self):
        result = statistical.jarque_bera(pd.Series([0.01] * 50))
        assert result == (None, None)


# ---------------------------------------------------------------------------
# variance_ratio
# ---------------------------------------------------------------------------

class TestVarianceRatio:
    def test_trending_series_vr_greater_than_one(self):
        vr = statistical.variance_ratio(_trending_rets(), k=5)
        assert vr is not None
        assert vr > 1.0, f"Expected VR>1 for trending series, got {vr}"

    def test_mean_reverting_series_vr_less_than_one(self):
        vr = statistical.variance_ratio(_mean_rev_rets(), k=5)
        assert vr is not None
        assert vr < 1.0, f"Expected VR<1 for mean-reverting series, got {vr}"

    def test_random_walk_vr_near_one(self):
        rng = np.random.RandomState(0)
        # iid => VR should be close to 1 (within +/-0.3 for 1000 obs)
        iid = pd.Series(rng.normal(0, 0.01, 1000))
        vr = statistical.variance_ratio(iid, k=5)
        assert vr is not None
        assert 0.7 < vr < 1.3, f"Expected VR~1 for iid series, got {vr}"

    def test_empty_series_returns_none(self):
        assert statistical.variance_ratio(pd.Series([], dtype=float)) is None

    def test_too_short_returns_none(self):
        assert statistical.variance_ratio(pd.Series([0.01, 0.02]), k=5) is None

    def test_nan_values_dropped(self):
        rets = _trending_rets()
        rets.iloc[5] = np.nan
        rets.iloc[20] = np.nan
        vr = statistical.variance_ratio(rets, k=5)
        assert vr is not None

    def test_zero_variance_returns_none(self):
        assert statistical.variance_ratio(pd.Series([0.0] * 50), k=5) is None

    def test_custom_k(self):
        vr2 = statistical.variance_ratio(_trending_rets(), k=2)
        vr10 = statistical.variance_ratio(_trending_rets(), k=10)
        # Both should be >1 for a trending series; values differ with k
        assert vr2 is not None and vr10 is not None
        assert vr2 > 1.0 and vr10 > 1.0


# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------

class TestSummary:
    def test_trending_regime(self):
        result = statistical.summary(_trending_rets(300))
        assert result is not None
        assert result["regime"] == "trending"
        assert "jb" in result
        assert "vr" in result
        assert "normal" in result

    def test_mean_reverting_regime(self):
        result = statistical.summary(_mean_rev_rets(300))
        assert result is not None
        assert result["regime"] == "mean-reverting"

    def test_normal_gaussian_data(self):
        result = statistical.summary(_normal_rets(500))
        assert result is not None
        assert result["normal"] is True

    def test_fat_tails_not_normal(self):
        result = statistical.summary(_fat_rets(500))
        assert result is not None
        assert result["normal"] is False

    def test_empty_series_returns_none(self):
        assert statistical.summary(pd.Series([], dtype=float)) is None

    def test_short_series_returns_none(self):
        assert statistical.summary(pd.Series([0.01, -0.01, 0.02])) is None

    def test_return_dict_keys(self):
        result = statistical.summary(_normal_rets())
        assert result is not None
        assert set(result.keys()) == {"normal", "jb", "vr", "regime"}

    def test_regime_is_valid_string(self):
        result = statistical.summary(_normal_rets())
        assert result is not None
        assert result["regime"] in {"trending", "mean-reverting", "random"}

    def test_jb_is_float_or_none(self):
        result = statistical.summary(_normal_rets())
        assert result is not None
        assert result["jb"] is None or isinstance(result["jb"], float)

    def test_vr_is_float_or_none(self):
        result = statistical.summary(_normal_rets())
        assert result is not None
        assert result["vr"] is None or isinstance(result["vr"], float)

    def test_nan_series_handled(self):
        rets = pd.Series([np.nan] * 50)
        assert statistical.summary(rets) is None

    def test_series_with_some_nan(self):
        rets = _normal_rets(200)
        rets.iloc[::5] = np.nan
        result = statistical.summary(rets)
        # After dropping NaN there are still enough obs
        assert result is not None
        assert result["regime"] in {"trending", "mean-reverting", "random"}
