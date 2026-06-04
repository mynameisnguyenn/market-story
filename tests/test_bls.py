"""Tests for BLS snapshot parsing (requests mocked, no network)."""
from src import bls_data


def test_snapshot_change_and_yoy():
    # 13 monthly obs, newest-first: latest 110, prev 109, year-ago (idx 12) 100.
    data = [{"year": "2026", "period": "M06", "value": "110"},
            {"year": "2026", "period": "M05", "value": "109"}]
    data += [{"year": "2026", "period": f"M{m:02d}", "value": "105"} for m in (4, 3, 2, 1)]
    data += [{"year": "2025", "period": f"M{m:02d}", "value": "104"} for m in (12, 11, 10, 9, 8, 7)]
    data += [{"year": "2025", "period": "M06", "value": "100"}]   # idx 12 -> 1 year before
    snap = bls_data._snapshot("CUUR0000SA0", "CPI", data)
    assert snap["latest"] == 110.0 and snap["prev"] == 109.0
    assert snap["change"] == 1.0
    assert round(snap["yoy_pct"], 2) == 10.0
    assert snap["date"] == "2026-06"


def test_snapshot_ignores_annual_and_handles_empty():
    annual_only = [{"year": "2025", "period": "M13", "value": "300"}]   # M13 = annual avg
    snap = bls_data._snapshot("X", "X", annual_only)
    assert snap["latest"] is None and snap["yoy_pct"] is None
    assert bls_data._snapshot("X", "X", [])["latest"] is None


def test_fetch_bls_parses_payload(monkeypatch):
    payload = {"status": "REQUEST_SUCCEEDED", "Results": {"series": [
        {"seriesID": "LNS14000000", "data": [
            {"year": "2026", "period": "M05", "value": "4.3"},
            {"year": "2026", "period": "M04", "value": "4.2"}]}]}}

    class _Resp:
        def raise_for_status(self): pass
        def json(self): return payload

    monkeypatch.setattr(bls_data, "_load_key", lambda: None)
    monkeypatch.setattr(bls_data.requests, "post", lambda *a, **k: _Resp())
    rows = bls_data.fetch_bls([("LNS14000000", "Unemployment")])
    assert rows[0]["latest"] == 4.3 and round(rows[0]["change"], 2) == 0.1


def test_fetch_bls_best_effort_on_failure(monkeypatch):
    def _boom(*a, **k):
        raise RuntimeError("network down")
    monkeypatch.setattr(bls_data, "_load_key", lambda: None)
    monkeypatch.setattr(bls_data.requests, "post", _boom)
    rows = bls_data.fetch_bls([("CUUR0000SA0", "CPI")])
    assert rows[0]["latest"] is None        # degrades, does not raise


def test_obs_rows_drops_annual_and_bad_values():
    data = [{"year": "2026", "period": "M04", "value": "300.0"},
            {"year": "2026", "period": "M13", "value": "299"},      # annual avg -> dropped
            {"year": "2026", "period": "M03", "value": "n/a"}]      # unparseable -> dropped
    rows = bls_data._obs_rows("CUUR0000SA0", data)
    assert rows == [{"date": "2026-04", "series": "CUUR0000SA0", "value": 300.0}]


def test_backfill_bls_archive_chunks_and_merges(tmp_path, monkeypatch):
    monkeypatch.setattr(bls_data, "ARCHIVE_PATH", tmp_path / "labor.jsonl")
    monkeypatch.setattr(bls_data, "_load_key", lambda: None)
    calls = []

    def _fake_request(ids, key, start_year=None, end_year=None, timeout=15):
        calls.append((start_year, end_year))
        return {"status": "REQUEST_SUCCEEDED", "Results": {"series": [   # one obs at the chunk start
            {"seriesID": "CUUR0000SA0",
             "data": [{"year": str(start_year), "period": "M01", "value": "100"}]}]}}

    monkeypatch.setattr(bls_data, "_request", _fake_request)
    n = bls_data.backfill_bls_archive([("CUUR0000SA0", "CPI")], start_year=2000)
    assert all(hi - lo <= 9 for lo, hi in calls)                 # never exceeds the 10y keyless cap
    assert n == len(calls) and n >= 2                            # one row merged per chunk
    assert bls_data.load_bls_history("CUUR0000SA0")[0]["date"] == "2000-01"
