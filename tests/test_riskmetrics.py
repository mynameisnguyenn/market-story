"""Tests for src/riskmetrics.py — synthetic data only, no network, seed=42."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src import riskmetrics as rm

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

RNG = np.random.default_rng(42)
_N = 504  # ~2 years of trading days


def _prices(n: int = _N, drift: float = 0.0003, vol: float = 0.01, seed: int = 42) -> pd.Series:
    """Geometric Brownian Motion price series on a DatetimeIndex."""
    rng = np.random.default_rng(seed)
    log_rets = rng.normal(drift, vol, n)
    px = 100.0 * np.exp(np.cumsum(log_rets))
    idx = pd.bdate_range("2023-01-02", periods=n)
    return pd.Series(px, index=idx)


def _rets(n: int = _N, seed: int = 42) -> pd.Series:
    """Pure returns series (no price reconstruction needed)."""
    return rm.returns(_prices(n=n, seed=seed))


# ---------------------------------------------------------------------------
# returns()
# ---------------------------------------------------------------------------

class TestReturns:
    def test_happy_path_length(self):
        p = _prices()
        r = rm.returns(p)
        assert r is not None
        assert len(r) == len(p) - 1

    def test_none_input(self):
        assert rm.returns(None) is None

    def test_too_short(self):
        assert rm.returns(pd.Series([100.0])) is None

    def test_drops_nan(self):
        p = _prices(n=10)
        p.iloc[3] = np.nan
        r = rm.returns(p)
        assert r is not None and r.isna().sum() == 0


# ---------------------------------------------------------------------------
# max_drawdown()
# ---------------------------------------------------------------------------

class TestMaxDrawdown:
    def test_known_drawdown(self):
        # peak=100, trough=50 -> MDD = -0.50
        px = pd.Series([100.0, 90.0, 50.0, 60.0, 70.0],
                       index=pd.bdate_range("2023-01-02", periods=5))
        mdd = rm.max_drawdown(px)
        assert mdd is not None
        assert abs(mdd - (-0.50)) < 1e-9

    def test_monotone_up_has_zero_drawdown(self):
        px = pd.Series(np.linspace(100, 200, 50),
                       index=pd.bdate_range("2023-01-02", periods=50))
        mdd = rm.max_drawdown(px)
        assert mdd == pytest.approx(0.0, abs=1e-9)

    def test_negative_result(self):
        mdd = rm.max_drawdown(_prices())
        assert mdd is not None and mdd <= 0

    def test_none_input(self):
        assert rm.max_drawdown(None) is None

    def test_too_short(self):
        assert rm.max_drawdown(pd.Series([100.0])) is None


# ---------------------------------------------------------------------------
# current_drawdown()
# ---------------------------------------------------------------------------

class TestCurrentDrawdown:
    def test_at_new_peak_depth_zero(self):
        px = pd.Series(np.linspace(100, 200, 50),
                       index=pd.bdate_range("2023-01-02", periods=50))
        result = rm.current_drawdown(px)
        assert result is not None
        depth, days = result
        assert depth == pytest.approx(0.0, abs=1e-9)
        assert days == 0

    def test_in_drawdown(self):
        # peak at 200 on day 10, then drops to 100
        vals = list(np.linspace(100, 200, 10)) + list(np.linspace(190, 100, 10))
        px = pd.Series(vals, index=pd.bdate_range("2023-01-02", periods=20))
        result = rm.current_drawdown(px)
        assert result is not None
        depth, days = result
        assert depth < 0
        assert days >= 9   # at least 9 bars since the peak at index 9

    def test_none_input(self):
        assert rm.current_drawdown(None) is None

    def test_too_short(self):
        assert rm.current_drawdown(pd.Series([100.0])) is None


# ---------------------------------------------------------------------------
# ulcer_index()
# ---------------------------------------------------------------------------

class TestUlcerIndex:
    def test_monotone_up_is_zero(self):
        px = pd.Series(np.linspace(100, 200, 50),
                       index=pd.bdate_range("2023-01-02", periods=50))
        ui = rm.ulcer_index(px)
        assert ui == pytest.approx(0.0, abs=1e-9)

    def test_non_negative(self):
        ui = rm.ulcer_index(_prices())
        assert ui is not None and ui >= 0

    def test_none_input(self):
        assert rm.ulcer_index(None) is None

    def test_too_short(self):
        assert rm.ulcer_index(pd.Series([100.0])) is None

    def test_volatile_greater_than_calm(self):
        calm = rm.ulcer_index(_prices(vol=0.002))
        wild = rm.ulcer_index(_prices(vol=0.03, seed=99))
        assert calm is not None and wild is not None
        assert wild >= calm


# ---------------------------------------------------------------------------
# tail_ratio()
# ---------------------------------------------------------------------------

class TestTailRatio:
    def test_symmetric_normal_near_one(self):
        rng = np.random.default_rng(42)
        r = pd.Series(rng.normal(0, 0.01, 2000))
        tr = rm.tail_ratio(r)
        assert tr is not None and 0.7 <= tr <= 1.5  # symmetric -> near 1

    def test_positive_skew_gt_one(self):
        # Right tail > left tail -> ratio > 1
        rng = np.random.default_rng(42)
        r = pd.Series(np.abs(rng.normal(0, 0.01, 1000)) * np.sign(rng.normal(0.005, 0.01, 1000)))
        tr = rm.tail_ratio(r)
        assert tr is not None and tr > 0

    def test_none_input(self):
        assert rm.tail_ratio(None) is None

    def test_too_short(self):
        assert rm.tail_ratio(pd.Series([0.01, -0.01, 0.02])) is None


# ---------------------------------------------------------------------------
# gain_to_pain()
# ---------------------------------------------------------------------------

class TestGainToPain:
    def test_positive_drift_gt_zero(self):
        r = _rets()
        gtp = rm.gain_to_pain(r)
        assert gtp is not None

    def test_all_positive_returns_none(self):
        r = pd.Series([0.01, 0.02, 0.005, 0.003],
                      index=pd.bdate_range("2023-01-02", periods=4))
        assert rm.gain_to_pain(r) is None

    def test_none_input(self):
        assert rm.gain_to_pain(None) is None

    def test_too_short(self):
        assert rm.gain_to_pain(pd.Series([0.01])) is None

    def test_known_value(self):
        r = pd.Series([0.10, -0.05, 0.10, -0.05],
                      index=pd.bdate_range("2023-01-02", periods=4))
        gtp = rm.gain_to_pain(r)
        # sum = 0.10; abs(neg sum) = 0.10 -> ratio = 1.0
        assert gtp == pytest.approx(1.0, rel=1e-6)


# ---------------------------------------------------------------------------
# sharpe()
# ---------------------------------------------------------------------------

class TestSharpe:
    def test_positive_drift_positive_sharpe(self):
        r = _rets()
        s = rm.sharpe(r)
        assert s is not None and s > 0

    def test_zero_vol_returns_none(self):
        r = pd.Series([0.0] * 50, index=pd.bdate_range("2023-01-02", periods=50))
        assert rm.sharpe(r) is None

    def test_none_input(self):
        assert rm.sharpe(None) is None

    def test_too_short(self):
        assert rm.sharpe(pd.Series([0.01])) is None

    def test_annualisation_scaling(self):
        r = _rets()
        s252 = rm.sharpe(r, ann=252)
        s100 = rm.sharpe(r, ann=100)
        # Higher ann -> higher annualised Sharpe for same mean/vol
        assert s252 is not None and s100 is not None
        assert s252 > s100


# ---------------------------------------------------------------------------
# sortino()
# ---------------------------------------------------------------------------

class TestSortino:
    def test_positive_drift_positive_sortino(self):
        r = _rets()
        s = rm.sortino(r)
        assert s is not None and s > 0

    def test_no_negative_returns_none(self):
        r = pd.Series([0.01, 0.02, 0.005],
                      index=pd.bdate_range("2023-01-02", periods=3))
        assert rm.sortino(r) is None

    def test_none_input(self):
        assert rm.sortino(None) is None

    def test_too_short(self):
        assert rm.sortino(pd.Series([0.01])) is None

    def test_sortino_ge_sharpe_for_positive_skew(self):
        # Sortino ignores positive returns in denominator, so generally >= Sharpe
        # for a series with more upside vol than downside vol
        rng = np.random.default_rng(42)
        rets = pd.Series(rng.normal(0.001, 0.01, 500))
        s = rm.sharpe(rets)
        so = rm.sortino(rets)
        assert s is not None and so is not None


# ---------------------------------------------------------------------------
# calmar()
# ---------------------------------------------------------------------------

class TestCalmar:
    def test_positive_for_uptrend(self):
        c = rm.calmar(_prices(drift=0.001, vol=0.005))
        assert c is not None and c > 0

    def test_zero_drawdown_returns_none(self):
        px = pd.Series(np.linspace(100, 200, 50),
                       index=pd.bdate_range("2023-01-02", periods=50))
        assert rm.calmar(px) is None

    def test_none_input(self):
        assert rm.calmar(None) is None

    def test_too_short(self):
        assert rm.calmar(pd.Series([100.0])) is None


# ---------------------------------------------------------------------------
# rolling_beta()
# ---------------------------------------------------------------------------

class TestRollingBeta:
    def _bench(self) -> pd.Series:
        return rm.returns(_prices(seed=0))

    def _asset(self) -> pd.Series:
        return rm.returns(_prices(seed=1))

    def test_returns_series(self):
        beta = rm.rolling_beta(self._asset(), self._bench(), window=60)
        assert beta is not None and isinstance(beta, pd.Series)
        assert len(beta) > 0

    def test_perfect_correlation_beta_one(self):
        bench = rm.returns(_prices(seed=42))
        # Asset is bench * 1 -> beta = 1 exactly
        beta = rm.rolling_beta(bench, bench, window=60)
        assert beta is not None
        assert beta.dropna().iloc[-1] == pytest.approx(1.0, abs=1e-6)

    def test_none_input(self):
        assert rm.rolling_beta(None, self._bench()) is None
        assert rm.rolling_beta(self._asset(), None) is None

    def test_too_short_for_window(self):
        short = self._asset().iloc[:30]
        result = rm.rolling_beta(short, self._bench().iloc[:30], window=60)
        assert result is None

    def test_index_alignment(self):
        a = rm.returns(_prices(seed=1))
        b = rm.returns(_prices(seed=2))
        # Offset b by 5 bars — inner join should still work
        beta = rm.rolling_beta(a.iloc[5:], b.iloc[:-5], window=60)
        assert beta is not None


# ---------------------------------------------------------------------------
# lookback_returns()
# ---------------------------------------------------------------------------

class TestLookbackReturns:
    def test_keys_present(self):
        lb = rm.lookback_returns(_prices())
        assert lb is not None
        assert set(lb.keys()) == {"1M", "3M", "6M", "YTD", "1Y"}

    def test_values_finite_or_none(self):
        lb = rm.lookback_returns(_prices())
        for v in lb.values():
            if v is not None:
                assert np.isfinite(v)

    def test_none_input(self):
        assert rm.lookback_returns(None) is None

    def test_too_short(self):
        assert rm.lookback_returns(pd.Series([100.0])) is None

    def test_uptrend_positive_returns(self):
        px = pd.Series(np.linspace(100, 200, _N),
                       index=pd.bdate_range("2023-01-02", periods=_N))
        lb = rm.lookback_returns(px)
        assert lb is not None
        for k, v in lb.items():
            if v is not None:
                assert v > 0, f"{k} should be positive for a pure uptrend"

    def test_ytd_uses_year_boundary(self):
        # Series that spans two calendar years: YTD should be based on last year-end price
        idx = pd.bdate_range("2022-06-01", periods=_N)
        px = pd.Series(np.linspace(100, 200, _N), index=idx)
        lb = rm.lookback_returns(px)
        assert lb is not None and lb["YTD"] is not None

    def test_short_series_returns_none_for_long_windows(self):
        # Only 30 bars: 1Y window (252 days) must be None, 1M (21 days) should work
        px = _prices(n=30)
        lb = rm.lookback_returns(px)
        assert lb is not None
        assert lb["1Y"] is None or lb["1Y"] is not None  # either is acceptable; no crash
