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


def test_series_rows_drops_nan():
    series = pd.Series([4.1, float("nan"), 4.3],
                       index=pd.to_datetime(["1962-01-02", "1962-01-03", "1962-01-04"]))
    rows = macro_data._series_rows("DGS10", series)
    assert rows == [{"date": "1962-01-02", "series": "DGS10", "value": 4.1},
                    {"date": "1962-01-04", "series": "DGS10", "value": 4.3}]
    assert macro_data._series_rows("DGS10", None) == []


def test_fred_archive_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(macro_data, "ARCHIVE_PATH", tmp_path / "macro.jsonl")
    monkeypatch.setattr(macro_data, "_load_env_key", lambda: None)
    full = pd.Series([4.1, 4.2, 4.3],
                     index=pd.to_datetime(["1962-01-02", "1962-01-03", "1962-01-04"]))
    monkeypatch.setattr(macro_data, "_fetch_with_retry", lambda fred, sid, attempts=3: full)
    n = macro_data.backfill_fred_archive([("DGS10", "10Y Treasury Yield")])
    assert n == 3
    hist = macro_data.load_fred_history("DGS10")
    assert len(hist) == 3 and hist[0]["date"] == "1962-01-02" and hist[-1]["value"] == 4.3
    macro_data.update_fred_archive([("DGS10", "10Y Treasury Yield")])   # idempotent re-merge
    assert len(macro_data.load_fred_history("DGS10")) == 3
