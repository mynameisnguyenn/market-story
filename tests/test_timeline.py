"""Append-only metrics timeline (no network; tmp paths)."""
from src import config, timeline


def _patch(tmp_path, monkeypatch):
    monkeypatch.setattr(timeline, "TIMELINE_PATH", tmp_path / "tl.jsonl")
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)


def test_append_and_load_extracts_key_metrics(tmp_path, monkeypatch):
    _patch(tmp_path, monkeypatch)
    brief = {
        "date": "2026-06-03",
        "markets": {"us_equities": [{"symbol": "^GSPC", "last": 7553.0, "change_pct": -0.74},
                                     {"symbol": "^VIX", "last": 16.06}],
                    "commodities": [{"symbol": "CL=F", "last": 96.2}]},
        "macro": [{"id": "DGS10", "latest": 4.46}, {"id": "BAMLH0A0HYM2", "latest": 2.71}],
        "positioning": [{"name": "S&P 500 (e-mini)", "lev_net": -457780}],
        "vol": {"premium": 6.2}, "stats": {},
    }
    timeline.append_today(brief)
    rows = timeline.load_timeline()
    assert len(rows) == 1
    r = rows[0]
    assert r["spx"] == 7553.0 and r["vix"] == 16.06 and r["wti"] == 96.2
    assert r["ust10"] == 4.46 and r["hy_oas"] == 2.71
    assert r["spx_spec_net"] == -457780 and r["vol_premium"] == 6.2


def test_append_idempotent_by_date(tmp_path, monkeypatch):
    _patch(tmp_path, monkeypatch)
    timeline.append_today({"date": "2026-06-03", "markets": {}, "macro": [], "positioning": []})
    timeline.append_today({"date": "2026-06-03",
                           "markets": {"us_equities": [{"symbol": "^GSPC", "last": 99.0}]},
                           "macro": [], "positioning": []})
    rows = timeline.load_timeline()
    assert len(rows) == 1 and rows[0]["spx"] == 99.0    # same date -> replaced, not duplicated


def test_rows_sorted_by_date(tmp_path, monkeypatch):
    _patch(tmp_path, monkeypatch)
    for d in ["2026-06-03", "2026-06-01", "2026-06-02"]:
        timeline.append_today({"date": d, "markets": {}, "macro": [], "positioning": []})
    assert [r["date"] for r in timeline.load_timeline()] == ["2026-06-01", "2026-06-02", "2026-06-03"]


def test_load_empty_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(timeline, "TIMELINE_PATH", tmp_path / "none.jsonl")
    assert timeline.load_timeline() == []


def test_load_tolerates_one_corrupt_line(tmp_path, monkeypatch):
    path = tmp_path / "tl.jsonl"
    path.write_text('{"date": "2026-06-01", "spx": 1}\nGARBAGE NOT JSON\n'
                    '{"date": "2026-06-02", "spx": 2}\n', encoding="utf-8")
    monkeypatch.setattr(timeline, "TIMELINE_PATH", path)
    rows = timeline.load_timeline()
    assert [r["date"] for r in rows] == ["2026-06-01", "2026-06-02"]   # bad line skipped, rest kept
