"""Tests for src/signal_ic.py — synthetic data only, no network, seed=42."""
import numpy as np
import pandas as pd
import pytest

from src import signal_ic


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

RNG = np.random.default_rng(42)
DATES = pd.date_range("2023-01-02", periods=252, freq="B")


def _prices(n: int = 252, drift: float = 0.0001, vol: float = 0.01) -> pd.Series:
    """Synthetic GBM price series on a business-day index."""
    rng = np.random.default_rng(42)
    log_rets = rng.normal(drift, vol, size=n)
    prices = 100.0 * np.exp(np.cumsum(log_rets))
    return pd.Series(prices, index=DATES[:n])


def _signal_correlated(prices: pd.Series, horizon: int = 1, noise: float = 0.5) -> pd.Series:
    """Signal that is positively correlated with horizon-day forward returns."""
    fwd = signal_ic.forward_returns(prices, horizon).dropna()
    rng = np.random.default_rng(42)
    noisy = fwd + rng.normal(0, noise * fwd.std(), size=len(fwd))
    return noisy


# ---------------------------------------------------------------------------
# forward_returns
# ---------------------------------------------------------------------------

class TestForwardReturns:
    def test_horizon_1_basic(self):
        prices = _prices()
        fwd = signal_ic.forward_returns(prices, 1)
        # Last `horizon` values should be NaN (shifted out)
        assert fwd.iloc[-1] is np.nan or np.isnan(fwd.iloc[-1])
        # Values in the middle should be non-NaN
        assert not np.isnan(fwd.iloc[0])

    def test_horizon_alignment(self):
        """forward_returns(t) == prices[t+h]/prices[t] - 1."""
        prices = _prices(50)
        h = 5
        fwd = signal_ic.forward_returns(prices, h)
        idx = 10
        expected = prices.iloc[idx + h] / prices.iloc[idx] - 1.0
        assert abs(fwd.iloc[idx] - expected) < 1e-10

    def test_empty_series_returns_empty(self):
        result = signal_ic.forward_returns(pd.Series(dtype=float), 1)
        assert len(result) == 0

    def test_too_short_returns_empty(self):
        prices = pd.Series([100.0, 101.0], index=DATES[:2])
        result = signal_ic.forward_returns(prices, 5)
        assert len(result) == 0

    def test_none_input_returns_empty(self):
        result = signal_ic.forward_returns(None, 1)
        assert len(result) == 0

    def test_series_with_nan_handled(self):
        prices = _prices(50).copy()
        prices.iloc[10] = np.nan
        fwd = signal_ic.forward_returns(prices, 1)
        assert isinstance(fwd, pd.Series)


# ---------------------------------------------------------------------------
# information_coefficient
# ---------------------------------------------------------------------------

class TestInformationCoefficient:
    def test_positive_ic_for_correlated_signal(self):
        prices = _prices()
        sig = _signal_correlated(prices, horizon=1, noise=0.3)
        ic = signal_ic.information_coefficient(sig, prices, 1)
        assert ic is not None
        assert ic > 0.1  # should be clearly positive given low noise

    def test_ic_bounded(self):
        prices = _prices()
        sig = _signal_correlated(prices, horizon=1, noise=0.5)
        ic = signal_ic.information_coefficient(sig, prices, 1)
        assert ic is not None
        assert -1.0 <= ic <= 1.0

    def test_random_signal_ic_near_zero(self):
        """A pure noise signal should have IC near zero on average."""
        prices = _prices()
        rng = np.random.default_rng(42)
        noise_sig = pd.Series(rng.normal(0, 1, len(prices)), index=prices.index)
        ic = signal_ic.information_coefficient(noise_sig, prices, 1)
        assert ic is not None
        assert abs(ic) < 0.25  # should be statistically small

    def test_none_signal_returns_none(self):
        prices = _prices()
        assert signal_ic.information_coefficient(None, prices, 1) is None

    def test_none_prices_returns_none(self):
        sig = pd.Series([1.0, 2.0, 3.0], index=DATES[:3])
        assert signal_ic.information_coefficient(sig, None, 1) is None

    def test_too_short_returns_none(self):
        prices = pd.Series([100.0, 101.0, 102.0], index=DATES[:3])
        sig = pd.Series([1.0, 2.0, 3.0], index=DATES[:3])
        assert signal_ic.information_coefficient(sig, prices, 5) is None

    def test_empty_series_returns_none(self):
        empty = pd.Series(dtype=float)
        assert signal_ic.information_coefficient(empty, empty, 1) is None

    def test_perfect_rank_signal_ic_is_one(self):
        """If the signal is the exact forward return, IC should be ~1.0."""
        prices = _prices(100)
        fwd = signal_ic.forward_returns(prices, 1).dropna()
        ic = signal_ic.information_coefficient(fwd, prices, 1)
        assert ic is not None
        assert ic > 0.95


# ---------------------------------------------------------------------------
# ic_by_horizon
# ---------------------------------------------------------------------------

class TestIcByHorizon:
    def test_default_horizons_returned(self):
        prices = _prices()
        sig = _signal_correlated(prices, horizon=1)
        result = signal_ic.ic_by_horizon(sig, prices)
        assert set(result.keys()) == {1, 5, 21}

    def test_custom_horizons(self):
        prices = _prices()
        sig = _signal_correlated(prices, horizon=1)
        result = signal_ic.ic_by_horizon(sig, prices, horizons=[2, 10])
        assert set(result.keys()) == {2, 10}

    def test_all_values_bounded_or_none(self):
        prices = _prices()
        rng = np.random.default_rng(42)
        sig = pd.Series(rng.normal(0, 1, len(prices)), index=prices.index)
        result = signal_ic.ic_by_horizon(sig, prices)
        for v in result.values():
            if v is not None:
                assert -1.0 <= v <= 1.0

    def test_short_series_returns_nones(self):
        prices = pd.Series([100.0, 101.0], index=DATES[:2])
        sig = pd.Series([1.0, 2.0], index=DATES[:2])
        result = signal_ic.ic_by_horizon(sig, prices)
        assert all(v is None for v in result.values())

    def test_none_inputs_all_nones(self):
        result = signal_ic.ic_by_horizon(None, None)
        assert all(v is None for v in result.values())


# ---------------------------------------------------------------------------
# quantile_spread
# ---------------------------------------------------------------------------

class TestQuantileSpread:
    def test_spread_positive_for_correlated_signal(self):
        """A signal correlated with forward returns should give a positive spread."""
        prices = _prices()
        sig = _signal_correlated(prices, horizon=1, noise=0.2)
        spread = signal_ic.quantile_spread(sig, prices, horizon=1, q=5)
        assert spread is not None
        assert spread > 0.0

    def test_spread_is_float(self):
        prices = _prices()
        sig = _signal_correlated(prices, horizon=5, noise=0.5)
        spread = signal_ic.quantile_spread(sig, prices, horizon=5, q=5)
        if spread is not None:
            assert isinstance(spread, float)

    def test_none_signal_returns_none(self):
        prices = _prices()
        assert signal_ic.quantile_spread(None, prices, 1) is None

    def test_none_prices_returns_none(self):
        sig = pd.Series([1.0, 2.0, 3.0], index=DATES[:3])
        assert signal_ic.quantile_spread(sig, None, 1) is None

    def test_too_short_for_quantiles_returns_none(self):
        prices = pd.Series([100.0, 101.0, 102.0, 103.0], index=DATES[:4])
        sig = pd.Series([1.0, 2.0, 3.0, 4.0], index=DATES[:4])
        assert signal_ic.quantile_spread(sig, prices, horizon=1, q=5) is None

    def test_single_quantile_edge_case(self):
        prices = _prices(50)
        sig = _signal_correlated(prices, horizon=1)
        assert signal_ic.quantile_spread(sig, prices, horizon=1, q=1) is None

    def test_empty_returns_none(self):
        empty = pd.Series(dtype=float)
        assert signal_ic.quantile_spread(empty, empty, 1) is None

    def test_custom_q_accepted(self):
        prices = _prices()
        sig = _signal_correlated(prices, horizon=1, noise=0.3)
        spread = signal_ic.quantile_spread(sig, prices, horizon=1, q=3)
        assert spread is not None


# ---------------------------------------------------------------------------
# Internal: _rank_array
# ---------------------------------------------------------------------------

class TestRankArray:
    def test_basic_ranks(self):
        arr = np.array([3.0, 1.0, 2.0])
        ranks = signal_ic._rank_array(arr)
        # 1.0 -> rank 0, 2.0 -> rank 1, 3.0 -> rank 2
        assert ranks[1] == 0.0
        assert ranks[2] == 1.0
        assert ranks[0] == 2.0

    def test_tied_values_average_rank(self):
        arr = np.array([1.0, 1.0, 3.0])
        ranks = signal_ic._rank_array(arr)
        assert ranks[0] == 0.5
        assert ranks[1] == 0.5
        assert ranks[2] == 2.0
