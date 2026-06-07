"""Tests for src/backtest.py — synthetic data only, no network. These certify the engine that
certifies the signals, so they check the honesty guarantees directly: no lookahead, a real
predictor reads as significant, and pure noise reads as NOT significant."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src import backtest


def _prices(n=800, seed=42):
    rng = np.random.default_rng(seed)
    rets = rng.normal(0.0003, 0.01, n)
    return pd.Series(100.0 * np.exp(np.cumsum(rets)),
                     index=pd.bdate_range("2010-01-01", periods=n))


def test_forward_returns_are_strictly_future_no_lookahead():
    p = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0],
                  index=pd.bdate_range("2020-01-01", periods=5))
    fr = backtest.forward_returns(p, 1)
    assert fr.iloc[0] == pytest.approx(0.01)          # return from t0 to t1, indexed at t0
    assert pd.isna(fr.iloc[-1])                        # last point cannot see the future
    fr2 = backtest.forward_returns(p, 2)
    assert pd.isna(fr2.iloc[-1]) and pd.isna(fr2.iloc[-2])   # last `horizon` points are NaN


def test_perfect_predictor_is_significant():
    p = _prices()
    fwd = backtest.forward_returns(p, 1)              # signal = the realised next-day return
    boot = backtest.block_bootstrap_ic(fwd, p, 1, seed=0)
    assert boot is not None
    assert boot["ic"] > 0.99 and boot["significant"] and boot["ci_lo"] > 0


def test_pure_noise_is_not_significant():
    """A signal independent of price must NOT clear the bootstrap CI — the key false-positive guard."""
    p = _prices()
    rng = np.random.default_rng(7)
    noise = pd.Series(rng.normal(size=len(p)), index=p.index)
    boot = backtest.block_bootstrap_ic(noise, p, 21, seed=0)
    assert boot is not None
    assert abs(boot["ic"]) < 0.1
    assert not boot["significant"]                    # CI straddles zero
    assert boot["ci_lo"] < 0 < boot["ci_hi"]


def test_block_bootstrap_deterministic_with_seed():
    p = _prices()
    sig = p.shift(1)                                   # a (lagged-price) signal with some structure
    a = backtest.block_bootstrap_ic(sig, p, 5, seed=123)
    b = backtest.block_bootstrap_ic(sig, p, 5, seed=123)
    assert a == b                                      # reproducible


def test_information_coefficient_and_too_short():
    p = _prices(60)
    r = backtest.information_coefficient(p.shift(1), p, 5)
    assert r is not None and isinstance(r[0], float) and r[1] > 0
    assert backtest.information_coefficient(pd.Series([1.0, 2.0]), p, 5) is None


def test_ic_subperiods_splits_by_signal_date():
    p = _prices()
    sig = p.shift(1)
    periods = [("first", "2010-01-01", "2011-12-31"), ("second", "2012-01-01", "2099-01-01")]
    sub = backtest.ic_subperiods(sig, p, 21, periods)
    assert set(sub) == {"first", "second"}
    assert sub["first"]["n"] > 0 and sub["second"]["n"] > 0


def test_evaluate_signal_structure():
    p = _prices()
    out = backtest.evaluate_signal(p.shift(1), p,
                                   periods=[("all", "2010-01-01", "2099-01-01")])
    assert set(out["horizons"]) == set(backtest.HORIZONS)
    assert "bootstrap" in out["horizons"][21] and "quantile_spread" in out["horizons"][21]
    assert "subperiods_21d" in out and "all" in out["subperiods_21d"]


def test_bootstrap_none_on_thin_data():
    p = _prices(20)
    assert backtest.block_bootstrap_ic(p.shift(1), p, 21) is None   # n < 30 after alignment
