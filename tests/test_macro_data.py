"""Tests for FRED series snapshotting (synthetic series, no network)."""

import pandas as pd

from src import macro_data


def test_snapshot_latest_prev_change():
    series = pd.Series([4.10, 4.18, 4.25], index=pd.to_datetime(["2026-05-29", "2026-05-30", "2026-06-02"]))
    snap = macro_data._snapshot("DGS10", "10Y Treasury Yield", series)
    assert snap["latest"] == 4.25
    assert snap["prev"] == 4.18
    assert round(snap["change"], 2) == 0.07
    assert snap["date"] == "2026-06-02"


def test_snapshot_empty_series():
    snap = macro_data._snapshot("X", "X", None)
    assert snap["latest"] is None
    assert snap["change"] is None
    assert snap["date"] is None


def test_snapshot_single_observation():
    series = pd.Series([100.0], index=pd.to_datetime(["2026-06-01"]))
    snap = macro_data._snapshot("PAYEMS", "Payrolls", series)
    assert snap["latest"] == 100.0
    assert snap["prev"] is None
    assert snap["change"] is None
