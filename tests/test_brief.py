"""Tests for brief assembly: movers, breadth, and markdown rendering."""

from src import brief


def _sections():
    return {
        "us_equities": [
            {"symbol": "^GSPC", "name": "S&P 500", "change_pct": 1.0, "last": 5000.0,
             "change_1w_pct": 2.0, "ytd_pct": 8.0, "level_change": 50.0},
            {"symbol": "^VIX", "name": "VIX", "change_pct": -5.0, "last": 14.0,
             "change_1w_pct": None, "ytd_pct": None, "level_change": -0.7},
        ],
        "sectors": [
            {"symbol": "XLK", "name": "Technology", "change_pct": 2.0, "last": 1.0,
             "change_1w_pct": 1.0, "ytd_pct": 5.0, "level_change": 0.02},
            {"symbol": "XLE", "name": "Energy", "change_pct": -1.5, "last": 1.0,
             "change_1w_pct": -1.0, "ytd_pct": -3.0, "level_change": -0.01},
        ],
        "global_indices": [
            {"symbol": "^N225", "name": "Nikkei", "change_pct": 0.5, "last": 1.0,
             "change_1w_pct": 0.2, "ytd_pct": 1.0, "level_change": 0.0},
        ],
    }


def test_movers_rank_and_exclude_vix():
    movers = brief._movers(_sections())
    assert movers["leaders"][0]["name"] == "Technology"   # +2.0 is best
    assert movers["laggards"][0]["name"] == "Energy"      # -1.5 is worst
    names = [m["name"] for m in movers["leaders"]]
    assert "VIX" not in names                              # VIX excluded from movers


def test_stats_breadth_and_vix():
    stats = brief._stats(_sections())
    assert stats["vix"] == 14.0
    assert stats["sector_advancers"] == 1
    assert stats["sector_decliners"] == 1
    assert stats["sector_count"] == 2


def test_render_markdown_smoke():
    payload = brief.build_brief(sections=_sections(), macro=[], news_items=[], fetch=False)
    text = brief.render_markdown(payload)
    assert text.startswith("# Market Brief")
    assert "Technology" in text
    assert "## Movers" in text


def test_history_embed_and_reconstruct_roundtrip():
    import pandas as pd
    idx = pd.to_datetime(["2026-05-29", "2026-06-01", "2026-06-02"])
    hist = {"^GSPC": pd.DataFrame({"Close": [100.0, 101.5, 102.25]}, index=idx)}
    b = brief.build_brief(history=hist, sections={}, macro=[], news_items=[], fetch=False)
    assert b["history"]["series"]["^GSPC"] == [100.0, 101.5, 102.25]   # embedded (shared-axis)
    closes = brief.closes_from_brief(b)
    assert len(closes["^GSPC"]) == 3 and float(closes["^GSPC"].iloc[-1]) == 102.25  # rebuilt


def test_movers_no_overlap_when_pool_small():
    sections = {"us_equities": [
        {"symbol": "A", "name": "A", "change_pct": -2.0, "last": 1.0},
        {"symbol": "B", "name": "B", "change_pct": 0.5, "last": 1.0},
        {"symbol": "C", "name": "C", "change_pct": 3.0, "last": 1.0},
    ]}
    movers = brief._movers(sections)
    lead = {m["symbol"] for m in movers["leaders"]}
    lag = {m["symbol"] for m in movers["laggards"]}
    assert lead.isdisjoint(lag)             # no instrument in both lists
    assert "C" in lead and "A" in lag       # best is a leader, worst a laggard
