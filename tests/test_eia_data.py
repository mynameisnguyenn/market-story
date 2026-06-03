"""EIA energy-inventory snapshots — synthetic rows only, no network (per CLAUDE.md)."""
from src import brief, eia_data


def test_snapshot_computes_weekly_draw():
    rows = [
        {"period": "2026-05-29", "value": "433712", "units": "MBBL"},
        {"period": "2026-05-22", "value": "441686", "units": "MBBL"},
        {"period": "2026-05-15", "value": "445000", "units": "MBBL"},
    ]
    snap = eia_data._snapshot("WCESTUS1", "Crude oil (ex-SPR)", rows)
    assert snap["latest"] == 433712
    assert snap["prev"] == 441686
    assert snap["change"] == 433712 - 441686   # a draw (negative)
    assert snap["change"] < 0
    assert snap["date"] == "2026-05-29"
    assert snap["units"] == "MBBL"


def test_snapshot_orders_unsorted_rows_newest_first():
    rows = [
        {"period": "2026-05-15", "value": "445000"},
        {"period": "2026-05-29", "value": "433712"},
        {"period": "2026-05-22", "value": "441686"},
    ]
    snap = eia_data._snapshot("X", "x", rows)
    assert snap["date"] == "2026-05-29"
    assert snap["latest"] == 433712
    assert snap["prev"] == 441686


def test_snapshot_handles_single_row():
    snap = eia_data._snapshot("X", "x", [{"period": "2026-05-29", "value": "100"}])
    assert snap["latest"] == 100
    assert snap["prev"] is None
    assert snap["change"] is None


def test_snapshot_handles_empty_and_bad_values():
    assert eia_data._snapshot("X", "x", [])["latest"] is None
    bad = eia_data._snapshot("X", "x", [{"period": "2026-05-29", "value": "n/a"}])
    assert bad["latest"] is None
    assert bad["change"] is None


def test_fetch_eia_returns_empty_without_key(monkeypatch):
    monkeypatch.setattr(eia_data, "_load_key", lambda: None)
    assert eia_data.fetch_eia() == []


def test_build_brief_includes_energy():
    b = brief.build_brief(
        history={}, sections={}, macro=[], news_items=[], bls=[],
        energy=[{"id": "WCESTUS1", "name": "Crude oil (ex-SPR)", "latest": 433712,
                 "date": "2026-05-29", "prev": 441686, "change": -7974, "units": "MBBL"}],
        fetch=False,
    )
    assert "energy" in b
    assert b["energy"][0]["name"] == "Crude oil (ex-SPR)"


def test_energy_table_markdown():
    rows = [{"name": "Crude oil (ex-SPR)", "latest": 433712, "change": -7974,
             "units": "MBBL", "date": "2026-05-29"}]
    text = "\n".join(brief._energy_table(rows))
    assert "Energy inventories (EIA" in text
    assert "draw" in text          # negative change → draw
    assert brief._energy_table([]) == []
