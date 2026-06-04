"""EIA energy archive + snapshots — synthetic archive on a tmp path, no network."""
import json

from src import brief, eia_data


def _seed(tmp_path, monkeypatch, rows):
    p = tmp_path / "energy.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    monkeypatch.setattr(eia_data, "ARCHIVE_PATH", p)


def test_fetch_eia_from_archive_computes_weekly_draw(tmp_path, monkeypatch):
    _seed(tmp_path, monkeypatch, [
        {"date": "2026-05-15", "series": "WCESTUS1", "value": 445000.0, "units": "MBBL"},
        {"date": "2026-05-22", "series": "WCESTUS1", "value": 441686.0, "units": "MBBL"},
        {"date": "2026-05-29", "series": "WCESTUS1", "value": 433712.0, "units": "MBBL"},
    ])
    s = eia_data.fetch_eia([("petroleum/stoc/wstk", "WCESTUS1", "Crude")])[0]
    assert s["latest"] == 433712.0 and s["prev"] == 441686.0
    assert s["change"] == 433712.0 - 441686.0        # a draw (negative)
    assert s["change"] < 0
    assert s["date"] == "2026-05-29" and s["units"] == "MBBL"


def test_fetch_eia_single_obs_and_missing_series(tmp_path, monkeypatch):
    _seed(tmp_path, monkeypatch, [{"date": "2026-05-29", "series": "WCESTUS1", "value": 100.0, "units": "MBBL"}])
    by = {s["id"]: s for s in eia_data.fetch_eia([("p", "WCESTUS1", "Crude"), ("p", "MISSING", "Gone")])}
    assert by["WCESTUS1"]["latest"] == 100.0 and by["WCESTUS1"]["change"] is None
    assert by["MISSING"]["latest"] is None           # absent series -> blank snapshot, never crashes


def test_load_history_sorts_and_tolerates_bad_line(tmp_path, monkeypatch):
    p = tmp_path / "energy.jsonl"
    p.write_text('{"date":"2026-05-29","series":"X","value":1}\nGARBAGE\n'
                 '{"date":"2026-05-15","series":"X","value":2}\n', encoding="utf-8")
    monkeypatch.setattr(eia_data, "ARCHIVE_PATH", p)
    hist = eia_data.load_history()
    assert len(hist) == 2 and [r["date"] for r in hist] == ["2026-05-15", "2026-05-29"]   # sorted, garbage dropped


def test_fetch_eia_no_archive_no_key_degrades(tmp_path, monkeypatch):
    monkeypatch.setattr(eia_data, "ARCHIVE_PATH", tmp_path / "none.jsonl")
    monkeypatch.setattr(eia_data, "_load_key", lambda: None)
    assert eia_data.fetch_eia([("p", "WCESTUS1", "Crude")])[0]["latest"] is None   # no crash, blank snapshot


def test_build_brief_includes_energy():
    b = brief.build_brief(
        history={}, sections={}, macro=[], news_items=[], bls=[],
        energy=[{"id": "WCESTUS1", "name": "Crude oil (ex-SPR)", "latest": 433712,
                 "date": "2026-05-29", "prev": 441686, "change": -7974, "units": "MBBL"}],
        fetch=False,
    )
    assert "energy" in b and b["energy"][0]["name"] == "Crude oil (ex-SPR)"


def test_energy_table_markdown():
    rows = [{"name": "Crude oil (ex-SPR)", "latest": 433712, "change": -7974,
             "units": "MBBL", "date": "2026-05-29"}]
    text = "\n".join(brief._energy_table(rows))
    assert "Energy inventories (EIA" in text
    assert "draw" in text          # negative change → draw
    assert brief._energy_table([]) == []
