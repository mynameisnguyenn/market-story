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


def test_assemble_rows_anchors_to_spx_calendar():
    idx = pd.date_range("2024-01-01", periods=5, freq="D")
    prices = pd.DataFrame({"spx": [100.0, 101.0, np.nan, 103.0, 104.0]}, index=idx)  # gap day
    rows = backfill.assemble_rows(prices, pd.DataFrame(), pd.Series(dtype=float))
    dates = [r["date"] for r in rows]
    assert "2024-01-03" not in dates and len(rows) == 4          # spx-less day dropped, no junk row
    r103 = next(r for r in rows if r["spx"] == 103.0)            # real 101->103 move measured across gap
    assert round(r103["spx_chg"], 2) == round((103 / 101 - 1) * 100, 2)


def test_assemble_rows_rejects_inf_and_stays_valid_json():
    import json
    idx = pd.date_range("2024-01-01", periods=3, freq="D")
    prices = pd.DataFrame({"spx": [0.0, 100.0, 101.0]}, index=idx)   # zero prior -> pct_change inf
    rows = backfill.assemble_rows(prices, pd.DataFrame(), pd.Series(dtype=float))
    json.dumps(rows, allow_nan=False)                            # must be RFC-valid (no Infinity/NaN)
    assert all(r["spx_chg"] != float("inf") for r in rows)


def test_assemble_rows_empty():
    assert backfill.assemble_rows(pd.DataFrame(), pd.DataFrame(), pd.Series(dtype=float)) == []
