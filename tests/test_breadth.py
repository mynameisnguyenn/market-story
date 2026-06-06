"""Tests for src/breadth.py — pure breadth/internals functions.

All data is synthetic (np.random.seed(42)).  No network calls.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.breadth import advance_decline, mcclellan, new_highs_lows, pct_above_ma

# ---------------------------------------------------------------------------
# shared fixtures
# ---------------------------------------------------------------------------

RNG = np.random.default_rng(42)


def _price_series(n: int = 300, start: float = 100.0, drift: float = 0.0003,
                  vol: float = 0.01, name: str = "A") -> pd.Series:
    """Geometric random walk with a DatetimeIndex."""
    idx = pd.date_range("2024-01-02", periods=n, freq="B")
    rets = RNG.normal(drift, vol, n)
    prices = start * np.exp(np.cumsum(rets))
    return pd.Series(prices, index=idx, name=name)


def _closes(n_symbols: int = 10, n_bars: int = 300) -> dict:
    return {f"SYM{i}": _price_series(n_bars, name=f"SYM{i}") for i in range(n_symbols)}


# ---------------------------------------------------------------------------
# advance_decline
# ---------------------------------------------------------------------------

class TestAdvanceDecline:
    def test_happy_path_counts_sum(self):
        closes = _closes(10, 100)
        result = advance_decline(closes)
        assert result is not None
        assert result["advancers"] + result["decliners"] <= 10
        assert result["net"] == result["advancers"] - result["decliners"]

    def test_all_up_day(self):
        idx = pd.date_range("2024-01-02", periods=5, freq="B")
        closes = {
            "A": pd.Series([100, 101, 102, 103, 104], index=idx, dtype=float),
            "B": pd.Series([50, 51, 52, 53, 54], index=idx, dtype=float),
        }
        result = advance_decline(closes)
        assert result["advancers"] == 2
        assert result["decliners"] == 0
        assert result["net"] == 2

    def test_all_down_day(self):
        idx = pd.date_range("2024-01-02", periods=3, freq="B")
        closes = {
            "A": pd.Series([100, 99, 98], index=idx, dtype=float),
        }
        result = advance_decline(closes)
        assert result["decliners"] == 1
        assert result["advancers"] == 0
        assert result["net"] == -1

    def test_empty_dict_returns_none(self):
        assert advance_decline({}) is None

    def test_single_bar_series_skipped(self):
        idx = pd.date_range("2024-01-02", periods=1, freq="B")
        closes = {"A": pd.Series([100.0], index=idx)}
        # Only 1 bar per series — not enough to compute a return; expect None.
        assert advance_decline(closes) is None

    def test_nan_series_skipped(self):
        idx = pd.date_range("2024-01-02", periods=5, freq="B")
        closes = {
            "A": pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan], index=idx),
            "B": pd.Series([100, 101, 102, 103, 104], index=idx, dtype=float),
        }
        result = advance_decline(closes)
        assert result is not None
        assert result["advancers"] == 1


# ---------------------------------------------------------------------------
# pct_above_ma
# ---------------------------------------------------------------------------

class TestPctAboveMa:
    def test_happy_path_in_range(self):
        closes = _closes(20, 300)
        result = pct_above_ma(closes, window=50)
        assert result is not None
        assert 0.0 <= result <= 100.0

    def test_all_above(self):
        """Perfectly trending series — all names above 50-day MA."""
        idx = pd.date_range("2024-01-02", periods=100, freq="B")
        # Strictly rising price so last close > any MA.
        closes = {
            "A": pd.Series(np.arange(1, 101, dtype=float), index=idx),
            "B": pd.Series(np.arange(2, 102, dtype=float), index=idx),
        }
        assert pct_above_ma(closes, window=50) == 100.0

    def test_all_below(self):
        """Strictly falling series — all names below 50-day MA."""
        idx = pd.date_range("2024-01-02", periods=100, freq="B")
        closes = {
            "A": pd.Series(np.arange(100, 0, -1, dtype=float), index=idx),
        }
        assert pct_above_ma(closes, window=50) == 0.0

    def test_empty_returns_none(self):
        assert pct_above_ma({}) is None

    def test_short_series_skipped(self):
        """Series shorter than window must be skipped; if all are short, return None."""
        idx = pd.date_range("2024-01-02", periods=10, freq="B")
        closes = {"A": pd.Series(np.ones(10), index=idx)}
        assert pct_above_ma(closes, window=50) is None

    def test_mixed_lengths(self):
        """Only long-enough series are counted."""
        idx_short = pd.date_range("2024-01-02", periods=10, freq="B")
        idx_long = pd.date_range("2024-01-02", periods=100, freq="B")
        closes = {
            "short": pd.Series(np.ones(10), index=idx_short),
            "long": pd.Series(np.arange(1, 101, dtype=float), index=idx_long),
        }
        result = pct_above_ma(closes, window=50)
        assert result == 100.0  # only the long rising series counts


# ---------------------------------------------------------------------------
# new_highs_lows
# ---------------------------------------------------------------------------

class TestNewHighsLows:
    def test_happy_path_structure(self):
        closes = _closes(10, 300)
        result = new_highs_lows(closes, window=252)
        assert result is not None
        assert "new_highs" in result and "new_lows" in result
        assert result["new_highs"] + result["new_lows"] <= 10

    def test_all_at_highs(self):
        """Strictly rising prices — every name at an N-day high."""
        idx = pd.date_range("2024-01-02", periods=260, freq="B")
        closes = {
            "A": pd.Series(np.arange(1, 261, dtype=float), index=idx),
            "B": pd.Series(np.arange(2, 262, dtype=float), index=idx),
        }
        result = new_highs_lows(closes, window=252)
        assert result["new_highs"] == 2
        assert result["new_lows"] == 0

    def test_all_at_lows(self):
        """Strictly falling prices — every name at an N-day low."""
        idx = pd.date_range("2024-01-02", periods=260, freq="B")
        closes = {
            "A": pd.Series(np.arange(260, 0, -1, dtype=float), index=idx),
        }
        result = new_highs_lows(closes, window=252)
        assert result["new_lows"] == 1
        assert result["new_highs"] == 0

    def test_empty_returns_none(self):
        assert new_highs_lows({}) is None

    def test_single_bar_returns_none(self):
        idx = pd.date_range("2024-01-02", periods=1, freq="B")
        closes = {"A": pd.Series([100.0], index=idx)}
        assert new_highs_lows(closes, window=252) is None

    def test_short_series_uses_available_window(self):
        """Series shorter than window still counts — uses available history."""
        idx = pd.date_range("2024-01-02", periods=10, freq="B")
        closes = {"A": pd.Series(np.arange(1, 11, dtype=float), index=idx)}
        result = new_highs_lows(closes, window=252)
        assert result is not None
        assert result["new_highs"] == 1


# ---------------------------------------------------------------------------
# mcclellan
# ---------------------------------------------------------------------------

class TestMcclellan:
    def test_happy_path_returns_float(self):
        closes = _closes(20, 200)
        result = mcclellan(closes, fast=19, slow=39)
        assert result is not None
        assert isinstance(result, float)

    def test_bullish_tape_positive_oscillator(self):
        """When all issues advance every day the net is always +N; oscillator is positive."""
        n = 100
        idx = pd.date_range("2024-01-02", periods=n, freq="B")
        closes = {
            f"S{i}": pd.Series(np.arange(1, n + 1, dtype=float) + i, index=idx)
            for i in range(5)
        }
        result = mcclellan(closes, fast=19, slow=39)
        assert result is not None
        assert result > 0

    def test_bearish_tape_negative_oscillator(self):
        """When all issues decline every day the oscillator is negative."""
        n = 100
        idx = pd.date_range("2024-01-02", periods=n, freq="B")
        closes = {
            f"S{i}": pd.Series(np.arange(n, 0, -1, dtype=float) + i, index=idx)
            for i in range(5)
        }
        result = mcclellan(closes, fast=19, slow=39)
        assert result is not None
        assert result < 0

    def test_empty_returns_none(self):
        assert mcclellan({}) is None

    def test_too_short_returns_none(self):
        """Fewer bars than the slow span -> not enough history."""
        idx = pd.date_range("2024-01-02", periods=10, freq="B")
        closes = {
            "A": pd.Series(np.arange(1, 11, dtype=float), index=idx),
        }
        assert mcclellan(closes, fast=19, slow=39) is None

    def test_invalid_span_returns_none(self):
        closes = _closes(5, 100)
        assert mcclellan(closes, fast=39, slow=19) is None  # fast >= slow

    def test_nan_series_handled(self):
        """NaN-only series are dropped; valid ones still produce a result."""
        idx = pd.date_range("2024-01-02", periods=100, freq="B")
        closes = {
            "nan": pd.Series([np.nan] * 100, index=idx),
            "good": pd.Series(np.arange(1, 101, dtype=float), index=idx),
        }
        # Only 1 clean series — not enough for a meaningful oscillator but should
        # not raise; it returns None (net series length = 99 < slow=39? no, 99 >= 39).
        result = mcclellan(closes, fast=19, slow=39)
        # 1 series always rising: net == 1 every bar -> EMA(1,19) - EMA(1,39) ~= 0.
        assert result is not None
        assert abs(result) < 1.0
