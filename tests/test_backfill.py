"""Backfill assembly — pure, synthetic frames, no network."""
import numpy as np
import pandas as pd

from src import backfill


def test_assemble_rows_builds_real_metric_rows():
    idx = pd.date_range("2024-01-01", periods=30, freq="D")
    prices = pd.DataFrame({
        "spx": np.linspace(4000, 4300, 30), "vix": np.linspace(20, 14, 30),
        "dxy": np.linspace(100, 103, 30), "wti": np.linspace(70, 80, 30),
        "copper": np.linspace(3.5, 4.0, 30), "gold": np.linspace(2000, 2100, 30),
    }, index=idx)
    fred = pd.DataFrame({
        "ust10": np.linspace(4.0, 4.3, 30), "curve_2s10s": np.linspace(-0.5, 0.1, 30),
        "hy_oas": np.linspace(4.0, 3.5, 30), "ig_oas": np.linspace(1.2, 1.0, 30),
    }, index=idx)
    spec = pd.Series([-100000.0, -120000.0], index=pd.to_datetime(["2024-01-03", "2024-01-17"]))
    rows = backfill.assemble_rows(prices, fred, spec)
    assert len(rows) == 30
    r = rows[-1]
    assert r["date"] == "2024-01-30"
    assert r["spx"] == 4300.0 and r["ust10"] is not None and r["hy_oas"] is not None
    assert r["spx_spec_net"] == -120000.0      # as-of fill from the latest weekly value
    assert r["backfilled"] is True and r["thesis"] is None
    assert any(x["vol_premium"] is not None for x in rows)   # computed once 20 returns exist
    assert rows[0]["spx_spec_net"] is None     # before the first weekly report -> no positioning


def test_assemble_rows_empty():
    assert backfill.assemble_rows(pd.DataFrame(), pd.DataFrame(), pd.Series(dtype=float)) == []
