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


def test_fetch_csv_drops_nat_index_rows(monkeypatch):
    import requests

    class _Resp:
        text = "DATE,DGS10\n2026-06-01,4.40\nbad-date,4.50\n"

        def raise_for_status(self):
            pass

    monkeypatch.setattr(requests, "get", lambda *a, **k: _Resp())
    series = macro_data._fetch_csv("DGS10")
    assert series is not None and series.index.notna().all()
    assert len(series) == 1 and series.iloc[-1] == 4.40


def test_load_env_key_requires_exact_name(tmp_path, monkeypatch):
    monkeypatch.delenv("FRED_API_KEY", raising=False)
    (tmp_path / ".env").write_text("FRED_API_KEY_OLD=expired\nFRED_API_KEY=real-key\n", encoding="utf-8")
    monkeypatch.setattr(macro_data.config, "PROJECT_ROOT", tmp_path)
    assert macro_data._load_env_key() == "real-key"   # not 'expired'
