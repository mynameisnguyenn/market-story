"""CFTC speculative-positioning snapshots — synthetic rows, no network."""
from src import brief, cftc_data


def test_snapshot_computes_lev_net_and_change():
    row = {
        "lev_money_positions_long": "149287", "lev_money_positions_short": "607067",
        "change_in_lev_money_long": "-14809", "change_in_lev_money_short": "41417",
        "asset_mgr_positions_long": "1204894", "asset_mgr_positions_short": "201287",
        "open_interest_all": "2093621", "report_date_as_yyyy_mm_dd": "2026-05-26T00:00:00.000",
    }
    snap = cftc_data._snapshot("S&P 500 (e-mini)", row)
    assert snap["lev_net"] == 149287 - 607067            # net short
    assert snap["lev_net"] < 0
    assert snap["lev_net_chg"] == -14809 - 41417
    assert snap["asset_net"] == 1204894 - 201287
    assert snap["date"] == "2026-05-26"                  # ISO timestamp trimmed to the date


def test_snapshot_handles_missing_row_and_fields():
    empty = cftc_data._snapshot("X", None)
    assert empty["lev_net"] is None and empty["date"] is None
    partial = cftc_data._snapshot("X", {"lev_money_positions_long": "100"})   # short leg missing
    assert partial["lev_net"] is None                    # net needs both legs


def test_build_brief_includes_positioning():
    b = brief.build_brief(
        history={}, sections={}, macro=[], news_items=[], bls=[], energy=[],
        positioning=[{"name": "S&P 500 (e-mini)", "lev_net": -1, "lev_net_chg": -2,
                      "asset_net": 3, "oi": 9, "date": "2026-05-26"}],
        fetch=False,
    )
    assert b["positioning"][0]["name"] == "S&P 500 (e-mini)"


def test_positioning_table_markdown():
    rows = [{"name": "S&P 500 (e-mini)", "lev_net": -457780, "lev_net_chg": -56226,
             "asset_net": 1003607, "oi": 2093621, "date": "2026-05-26"}]
    text = "\n".join(brief._positioning_table(rows))
    assert "Speculative positioning (CFTC" in text
    assert "net short" in text
    assert brief._positioning_table([]) == []
