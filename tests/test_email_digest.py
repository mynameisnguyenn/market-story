"""Email digest rendering — synthetic brief, no network."""
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
        "macro": [], "bls": [], "stats": {"sector_advancers": 3, "sector_decliners": 8},
        "movers": {"leaders": [], "laggards": []},
    }


def test_render_email_has_structure_and_data(monkeypatch):
    monkeypatch.setattr(email_digest.brief_mod, "latest_narrative_path", lambda: None)
    html = email_digest.render_email(_brief())
    assert html.strip().startswith("<!DOCTYPE html>")
    assert "Market Story" in html and "Today's thesis" in html
    assert "S&amp;P 500" in html and "7,553.70" in html      # KPI rendered + HTML-escaped
    assert "+0.18%" in html and "-3.20%" in html             # up/down deltas present
    assert email_digest._TONE["up"] in html                  # at least one green delta colored


def test_render_email_degrades_on_empty_brief(monkeypatch):
    monkeypatch.setattr(email_digest.brief_mod, "latest_narrative_path", lambda: None)
    html = email_digest.render_email({"date": "2026-06-06", "markets": {}, "stats": {}})
    assert "Market Story" in html and "n/a" in html          # no crash; missing KPIs -> n/a


def test_watch_items_parses_fenced_block(monkeypatch, tmp_path):
    nb = tmp_path / "narrative_2026-06-06.md"
    nb.write_text("## Today in one line\nDuration unwind, not stress.\n\n"
                  "```watch\nAVGO gaps >10% -> cluster is a trend | AVGO < -10\n"
                  "WTI reclaims 95 = unwind | CL=F > 95\n```\n", encoding="utf-8")
    monkeypatch.setattr(email_digest.brief_mod, "latest_narrative_path", lambda: nb)
    assert email_digest._thesis({}) == "Duration unwind, not stress."
    items = email_digest._watch_items()
    assert len(items) == 2 and items[0] == ("AVGO gaps >10% -> cluster is a trend", "AVGO < -10")
