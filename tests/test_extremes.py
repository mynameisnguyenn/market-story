"""Cross-asset extremes + vol-risk-premium analytics (no network)."""
import numpy as np
import pandas as pd

from src import analytics


def test_pct_z_high_and_low():
    pct, z = analytics._pct_z(list(range(300)))
    assert pct >= 99 and z > 1.5
    pct_lo, z_lo = analytics._pct_z(list(range(299, -1, -1)))   # latest is the min
    assert pct_lo == 0.0 and z_lo < -1.5


def test_realized_vol_basics():
    flat = analytics.realized_vol([100.0] * 60, 20)
    assert flat == 0.0
    assert analytics.realized_vol([1.0, 2.0, 3.0], 20) is None   # not enough history


def test_compute_extremes_filters_and_sorts():
    idx = pd.date_range("2025-01-01", periods=300, freq="D")
    closes = {
        "^VIX": pd.Series(np.linspace(10, 40, 300), index=idx),    # rising -> high pct, +z
        "TLT": pd.Series(np.linspace(95, 80, 300), index=idx),     # falling -> low pct, -z
        "ZZZ": pd.Series([1.0, 2.0], index=idx[:2]),               # not an anchor
    }
    ext = analytics.compute_extremes(closes)
    syms = [e["symbol"] for e in ext]
    assert "^VIX" in syms and "TLT" in syms and "ZZZ" not in syms
    zs = [abs(e["z"]) for e in ext if e["z"] is not None]
    assert zs == sorted(zs, reverse=True)                          # most stretched first
    assert all(e["n"] <= 252 for e in ext)


def test_compute_vol_premium():
    idx = pd.date_range("2025-01-01", periods=300, freq="D")
    closes = {
        "^GSPC": pd.Series(np.linspace(5000, 5500, 300), index=idx),   # gentle drift -> low realized
        "^VIX": pd.Series(np.full(300, 16.0), index=idx),
    }
    vp = analytics.compute_vol_premium(closes)
    assert vp is not None and vp["vix"] == 16.0
    assert vp["premium"] == round(16.0 - vp["realized_20d"], 1)


def test_analytics_degrade_empty():
    assert analytics.compute_extremes({}) == []
    assert analytics.compute_extremes(None) == []
    assert analytics.compute_vol_premium({}) is None
