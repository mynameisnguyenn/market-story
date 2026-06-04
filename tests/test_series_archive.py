"""Generic history-archive helper — round-trip, idempotent merge, LF, tolerance."""
from src import series_archive


def test_write_load_round_trip_sorted(tmp_path):
    p = tmp_path / "x.jsonl"
    series_archive.write(p, [
        {"date": "2026-05-29", "series": "B", "value": 2.0},
        {"date": "2026-05-15", "series": "A", "value": 1.0},
        {"date": "2026-05-22", "series": "A", "value": 1.5},
    ])
    rows = series_archive.load(p)
    assert [(r["series"], r["date"]) for r in rows] == [
        ("A", "2026-05-15"), ("A", "2026-05-22"), ("B", "2026-05-29")]   # (series, date) order


def test_write_is_lf_only(tmp_path):
    p = tmp_path / "x.jsonl"
    series_archive.write(p, [{"date": "2026-05-29", "series": "A", "value": 1.0}])
    assert b"\r\n" not in p.read_bytes()


def test_merge_is_idempotent_and_fresh_wins(tmp_path):
    p = tmp_path / "x.jsonl"
    series_archive.merge(p, [{"date": "2026-05-15", "series": "A", "value": 1.0}])
    n = series_archive.merge(p, [
        {"date": "2026-05-15", "series": "A", "value": 9.9},     # same key -> overwrite
        {"date": "2026-05-22", "series": "A", "value": 2.0},     # new key  -> add
    ])
    assert n == 2
    by_date = {r["date"]: r["value"] for r in series_archive.load(p)}
    assert by_date == {"2026-05-15": 9.9, "2026-05-22": 2.0}


def test_merge_skips_incomplete_rows(tmp_path):
    p = tmp_path / "x.jsonl"
    n = series_archive.merge(p, [
        {"date": "2026-05-15", "series": "A", "value": 1.0},
        {"date": "2026-05-22", "series": "A"},                   # no value
        {"series": "A", "value": 3.0},                           # no date
        {"date": "2026-05-29", "value": 4.0},                    # no series
    ])
    assert n == 1


def test_load_tolerates_bad_line_and_missing_file(tmp_path):
    assert series_archive.load(tmp_path / "absent.jsonl") == []
    p = tmp_path / "x.jsonl"
    p.write_text('{"date":"2026-05-29","series":"A","value":1}\nNOT JSON\n', encoding="utf-8")
    assert len(series_archive.load(p)) == 1


def test_history_for_filters_one_series(tmp_path):
    p = tmp_path / "x.jsonl"
    series_archive.write(p, [
        {"date": "2026-05-15", "series": "A", "value": 1.0},
        {"date": "2026-05-15", "series": "B", "value": 2.0},
    ])
    a = series_archive.history_for(p, "A")
    assert len(a) == 1 and a[0]["series"] == "A"
