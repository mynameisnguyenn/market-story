"""Email digest rendering — synthetic brief + narratives + ledger rows, no network."""
import json

from src import email_digest


def _brief():
    return {
        "date": "2026-06-06", "session_label": "PRE-US OPEN",
        "markets": {
            "us_equities": [{"symbol": "^GSPC", "name": "S&P 500", "last": 7553.7, "change_pct": 0.18},
                            {"symbol": "^VIX", "name": "VIX", "last": 16.1, "change_pct": -1.0}],
            "commodities": [{"symbol": "CL=F", "name": "WTI", "last": 92.4, "change_pct": -3.2},
                            {"symbol": "GC=F", "name": "Gold", "last": 4519.7, "change_pct": 1.24}],
        },
        "macro": [{"id": "DGS10", "name": "10Y Treasury", "latest": 4.46, "change": 0.03}],
        "bls": [], "stats": {"sector_advancers": 3, "sector_decliners": 8},
        "movers": {"leaders": [], "laggards": []},
        "extremes": [{"symbol": "DX-Y.NYB", "name": "Dollar (DXY)", "last": 101.3, "pct": 98.0},
                     {"symbol": "^TNX", "name": "10Y yield", "last": 4.46, "pct": 89.2},
                     {"symbol": "HG=F", "name": "Copper", "last": 6.5, "pct": 88.0},
                     {"symbol": "GC=F", "name": "Gold", "last": 4519.7, "pct": 87.5}],
    }


def _no_narratives(monkeypatch):
    monkeypatch.setattr(email_digest.brief_mod, "latest_narrative_path", lambda: None)
    monkeypatch.setattr(email_digest.brief_mod, "prior_narrative_path", lambda: None)


def _narrative(tmp_path, monkeypatch, date="2026-06-06", body="", prior_body=None):
    nb = tmp_path / f"narrative_{date}.md"
    nb.write_text(body, encoding="utf-8")
    monkeypatch.setattr(email_digest.brief_mod, "latest_narrative_path", lambda: nb)
    if prior_body is None:
        monkeypatch.setattr(email_digest.brief_mod, "prior_narrative_path", lambda: None)
    else:
        pb = tmp_path / "narrative_2026-06-05.md"
        pb.write_text(prior_body, encoding="utf-8")
        monkeypatch.setattr(email_digest.brief_mod, "prior_narrative_path", lambda: pb)
    return nb


def test_render_email_has_structure_and_data(monkeypatch):
    _no_narratives(monkeypatch)
    html = email_digest.render_email(_brief(), ledger_rows=[])
    assert html.strip().startswith("<!DOCTYPE html>")
    assert "Market Story" in html and "Today's thesis" in html
    assert "S&amp;P 500" in html and "7,553.70" in html      # KPI rendered + HTML-escaped
    assert "+0.18%" in html and "-3.20%" in html             # up/down deltas present
    assert email_digest._TONE["up"] in html                  # at least one green delta colored
    assert "+3 bps" in html                                  # the macro (10Y) KPI variant
    assert "supported-color-schemes" in html                 # Gmail dark-mode meta pair


def test_render_email_degrades_on_empty_brief(monkeypatch):
    _no_narratives(monkeypatch)
    html = email_digest.render_email({"date": "2026-06-06", "markets": {}, "stats": {}},
                                     ledger_rows=[])
    assert "Market Story" in html and "n/a" in html          # no crash; missing KPIs -> n/a
    assert "No stance logged today" in html                  # a gap never reads as a normal day
    assert "No prior watch items to grade yet." in html


def test_watch_items_parses_real_json_block(tmp_path, monkeypatch):
    """The real narrative format: a JSON array in the ```watch fence (scorecard.parse_watch)."""
    _narrative(tmp_path, monkeypatch, body=(
        "## Today in one line\nDuration unwind, not stress.\n\n"
        '```watch\n[\n'
        '  {"claim": "HY OAS widens", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.70",'
        ' "horizon": "2026-07-05", "probability": 0.65},\n'
        '  {"claim": "WTI reclaims 95", "metric": "market:CL=F:last", "trigger": ">95",'
        ' "horizon": "next week"}\n'
        ']\n```\n'))
    assert email_digest._thesis({}) == "Duration unwind, not stress."
    items = email_digest._watch_items()
    assert len(items) == 2 and items[0]["claim"] == "HY OAS widens"
    assert items[0]["probability"] == 0.65
    html = email_digest.render_email(_brief(), ledger_rows=[])
    assert "HY OAS widens" in html and "&gt;2.70" in html


def test_stance_badge_directions(tmp_path, monkeypatch):
    _narrative(tmp_path, monkeypatch, body='```stance\n{"direction": -1, "notes": "fade it"}\n```\n')
    st = email_digest._stance_today()
    assert "Short" in st["label"] and st["color"] == email_digest._TONE["down"]
    assert st["notes"] == "fade it"
    _narrative(tmp_path, monkeypatch, body='```stance\n{"direction": 0, "notes": ""}\n```\n')
    assert "Flat" in email_digest._stance_today()["label"]


def test_stance_badge_no_block_and_no_narrative(tmp_path, monkeypatch):
    _narrative(tmp_path, monkeypatch, body="## Today in one line\nNo call today.\n")
    assert email_digest._stance_today()["label"] == "No stance logged today"
    _no_narratives(monkeypatch)
    assert email_digest._stance_today()["label"] == "No stance logged today"


def test_last_settled_stance_branches():
    settled = {"kind": "stance", "logged": "2026-06-04", "status": "settled",
               "direction": 1, "pnl_pct": 0.55}
    today = {"kind": "stance", "logged": "2026-06-05", "status": "pending", "direction": -1}
    out = email_digest._last_settled_stance([settled, today])
    assert "+0.55%" in out["text"] and out["color"] == email_digest._TONE["up"]

    flat = {"kind": "stance", "logged": "2026-06-04", "status": "settled",
            "direction": 0, "pnl_pct": None}
    assert "flat, no P&amp;L" in email_digest._last_settled_stance([flat, today])["text"]

    pending = {"kind": "stance", "logged": "2026-06-04", "status": "pending", "direction": 1}
    assert "settling" in email_digest._last_settled_stance([pending, today])["text"]

    omitted = {"kind": "stance", "logged": "2026-06-04", "status": "omitted", "direction": None}
    assert "no stance logged" in email_digest._last_settled_stance([omitted, today])["text"]

    assert email_digest._last_settled_stance([])["text"] == ""       # empty ledger
    assert email_digest._last_settled_stance([today])["text"] == ""  # only today's row


def test_track_record_gates_on_min_n():
    few = [{"status": "triggered"}] * 3 + [{"status": "missed"}] * 2
    assert "Building sample — 5/30" in email_digest._track_record(few)
    many = [{"status": "triggered"}] * 12 + [{"status": "missed"}] * 24
    assert "hit-rate 33%" in email_digest._track_record(many)
    assert "36 graded" in email_digest._track_record(many)


def test_extremes_capped_at_three_and_empty(monkeypatch):
    _no_narratives(monkeypatch)
    rows = email_digest._extremes_rows(_brief())
    assert len(rows) == 3 and rows[0]["name"] == "Dollar (DXY)"
    assert email_digest._extremes_rows({"markets": {}}) == []
    html = email_digest.render_email({"date": "2026-06-06", "markets": {}, "stats": {}},
                                     ledger_rows=[])
    assert "Stretched" not in html                           # section omitted entirely when empty


def test_regrade_summary_grades_prior_watch(tmp_path, monkeypatch):
    prior = ('```watch\n[{"claim": "S&P holds 7500", "metric": "market:^GSPC:last",'
             ' "trigger": ">7500", "horizon": "next session"}]\n```\n')
    _narrative(tmp_path, monkeypatch, body="## Today in one line\nx\n", prior_body=prior)
    graded = email_digest._regrade_summary(_brief())
    assert len(graded) == 1 and graded[0]["status"] == "triggered"
    html = email_digest.render_email(_brief(), ledger_rows=[])
    assert "HIT" in html and "Mechanical re-grade" in html


def test_regrade_summary_empty_when_no_prior_narrative(monkeypatch):
    _no_narratives(monkeypatch)
    assert email_digest._regrade_summary(_brief()) == []
