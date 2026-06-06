"""Tests for src/rotation.py — synthetic data only, no network."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src import rotation


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

RNG = np.random.default_rng(42)
N = 300  # enough history for long=252


def _series(n: int = N, drift: float = 0.0, seed_offset: int = 0) -> pd.Series:
    """Random-walk price series with optional drift, DatetimeIndex."""
    rng = np.random.default_rng(42 + seed_offset)
    log_rets = rng.normal(drift / 252, 0.01, size=n)
    prices = 100.0 * np.exp(np.cumsum(log_rets))
    idx = pd.date_range("2023-01-01", periods=n, freq="B")
    return pd.Series(prices, index=idx)


BENCH = _series(N, drift=0.05, seed_offset=99)


# ---------------------------------------------------------------------------
# rs_ratio
# ---------------------------------------------------------------------------

class TestRsRatio:
    def test_returns_float_for_good_input(self):
        p = _series(N, drift=0.10, seed_offset=1)
        result = rotation.rs_ratio(p, BENCH)
        assert isinstance(result, float)

    def test_none_on_too_short(self):
        short = _series(10)
        assert rotation.rs_ratio(short, BENCH) is None

    def test_none_on_empty(self):
        assert rotation.rs_ratio(pd.Series(dtype=float), BENCH) is None

    def test_none_on_zero_benchmark(self):
        zero_bench = pd.Series(np.zeros(N),
                               index=pd.date_range("2023-01-01", periods=N, freq="B"))
        assert rotation.rs_ratio(_series(N), zero_bench) is None

    def test_nan_tolerance(self):
        p = _series(N, seed_offset=2).copy()
        p.iloc[10:20] = np.nan  # inject NaN band
        result = rotation.rs_ratio(p, BENCH)
        # after dropna alignment, might be None if too short, but should not raise
        assert result is None or isinstance(result, float)

    def test_rising_relative_strength_positive(self):
        """Relative strength trending UP within the window -> positive z-score.
        (A constant multiple of the benchmark sits at its mean -> z~0, so RS-ratio
        measures the *trend* of relative strength, not the level.)"""
        rising = pd.Series(BENCH.values * np.linspace(1.0, 2.0, N), index=BENCH.index)
        result = rotation.rs_ratio(rising, BENCH)
        assert result is not None and result > 0

    def test_falling_relative_strength_negative(self):
        falling = pd.Series(BENCH.values * np.linspace(2.0, 1.0, N), index=BENCH.index)
        result = rotation.rs_ratio(falling, BENCH)
        assert result is not None and result < 0


# ---------------------------------------------------------------------------
# rs_momentum
# ---------------------------------------------------------------------------

class TestRsMomentum:
    def test_returns_float_for_good_input(self):
        p = _series(N, drift=0.12, seed_offset=3)
        result = rotation.rs_momentum(p, BENCH)
        assert isinstance(result, float)

    def test_none_on_too_short(self):
        short = _series(50)
        assert rotation.rs_momentum(short, BENCH) is None

    def test_none_on_empty(self):
        assert rotation.rs_momentum(pd.Series(dtype=float), BENCH) is None

    def test_none_on_zero_benchmark(self):
        zero_bench = pd.Series(np.zeros(N),
                               index=pd.date_range("2023-01-01", periods=N, freq="B"))
        assert rotation.rs_momentum(_series(N), zero_bench) is None

    def test_accelerating_outperformer_positive_momentum(self):
        """A series with accelerating relative strength should have positive momentum."""
        # Build a benchmark that is flat and a price that ramps hard in the final 252 bars
        idx = pd.date_range("2020-01-01", periods=N, freq="B")
        flat_bench = pd.Series(np.ones(N) * 100.0, index=idx)
        # price doubles over the full window — strong long-term relative strength
        prices = pd.Series(np.linspace(50.0, 200.0, N), index=idx)
        result = rotation.rs_momentum(prices, flat_bench)
        assert result is not None and result > 0

    def test_decelerating_produces_negative_momentum(self):
        """A series that underperforms over the long window but recovered short-term."""
        idx = pd.date_range("2020-01-01", periods=N, freq="B")
        flat_bench = pd.Series(np.ones(N) * 100.0, index=idx)
        # price declines over the long term -> negative long momentum
        prices = pd.Series(np.linspace(200.0, 50.0, N), index=idx)
        result = rotation.rs_momentum(prices, flat_bench)
        assert result is not None and result < 0


# ---------------------------------------------------------------------------
# quadrant
# ---------------------------------------------------------------------------

class TestQuadrant:
    @pytest.mark.parametrize("ratio,mom,expected", [
        (1.0,  0.5,  "Leading"),
        (0.0,  0.0,  "Leading"),   # boundary: non-negative treated as Leading / Improving per sign
        (1.0, -0.5,  "Weakening"),
        (-1.0, -0.5, "Lagging"),
        (-1.0,  0.5, "Improving"),
    ])
    def test_quadrant_labels(self, ratio, mom, expected):
        assert rotation.quadrant(ratio, mom) == expected

    def test_all_quadrants_covered(self):
        labels = {rotation.quadrant(r, m) for r, m in [(1, 1), (1, -1), (-1, -1), (-1, 1)]}
        assert labels == {"Leading", "Weakening", "Lagging", "Improving"}


# ---------------------------------------------------------------------------
# rrg (integration)
# ---------------------------------------------------------------------------

class TestRrg:
    def _symbols(self):
        return {
            "SPY": _series(N, drift=0.10, seed_offset=10),
            "GLD": _series(N, drift=0.03, seed_offset=11),
            "TLT": _series(N, drift=-0.05, seed_offset=12),
        }

    def test_returns_dataframe_with_expected_columns(self):
        df = rotation.rrg(self._symbols(), BENCH)
        assert list(df.columns) == ["symbol", "rs_ratio", "rs_momentum", "quadrant"]

    def test_all_symbols_present(self):
        df = rotation.rrg(self._symbols(), BENCH)
        assert set(df["symbol"]) == {"SPY", "GLD", "TLT"}

    def test_quadrant_values_valid(self):
        df = rotation.rrg(self._symbols(), BENCH)
        valid = {"Leading", "Weakening", "Lagging", "Improving"}
        assert df["quadrant"].isin(valid).all()

    def test_empty_dict_returns_empty_dataframe(self):
        df = rotation.rrg({}, BENCH)
        assert df.empty
        assert list(df.columns) == ["symbol", "rs_ratio", "rs_momentum", "quadrant"]

    def test_short_series_excluded_gracefully(self):
        symbols = {
            "LONG": _series(N, seed_offset=20),
            "SHORT": _series(10, seed_offset=21),   # too short -> excluded
        }
        df = rotation.rrg(symbols, BENCH)
        assert "LONG" in df["symbol"].values
        assert "SHORT" not in df["symbol"].values

    def test_all_nan_series_excluded_gracefully(self):
        symbols = {
            "GOOD": _series(N, seed_offset=30),
            "BAD": pd.Series([np.nan] * N,
                             index=pd.date_range("2023-01-01", periods=N, freq="B")),
        }
        df = rotation.rrg(symbols, BENCH)
        assert "GOOD" in df["symbol"].values
        assert "BAD" not in df["symbol"].values

    def test_dtypes_are_numeric(self):
        df = rotation.rrg(self._symbols(), BENCH)
        assert df["rs_ratio"].dtype == float
        assert df["rs_momentum"].dtype == float

    def test_single_symbol(self):
        df = rotation.rrg({"SPY": _series(N, seed_offset=40)}, BENCH)
        assert len(df) == 1
        assert df.iloc[0]["symbol"] == "SPY"
