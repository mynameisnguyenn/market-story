"""Render smoke test: every tab must render with synthetic data and no exception.

This catches render-time bugs (duplicate element ids, None handling in panels)
that the pure-builder tests miss — the class that produced the two bugs the
screenshot loop had to catch by eye. Offline: no network, no real history DB.
"""


def _render_all_tabs():
    import pandas as pd
    import app

    def rows(syms):
        return [{"symbol": s, "name": s, "last": 100.0, "change_pct": 1.0,
                 "change_1w_pct": 2.0, "ytd_pct": 3.0, "level_change": 0.5} for s in syms]

    brief = {
        "date": "2026-06-02", "session_label": "test", "generated_at_utc": "2026-06-02T00:00:00",
        "markets": {
            "us_equities": rows(["^GSPC", "^IXIC", "^VIX"]),
            "sectors": rows(["XLK", "XLE"]),
            "watchlist": rows(["NVDA", "MSFT"]),
            "global_indices": rows(["^N225"]),
            "rates": rows(["^IRX", "^FVX", "^TNX", "^TYX"]),
            "fx": rows(["DX-Y.NYB"]),
            "commodities": rows(["GC=F"]) + [
                {"symbol": "CL=F", "name": "WTI", "last": 96.0, "change_pct": 2.5,
                 "change_1w_pct": 1.0, "ytd_pct": 1.0, "level_change": 0.0},
                {"symbol": "HG=F", "name": "Copper", "last": 6.5, "change_pct": -1.5,
                 "change_1w_pct": 0.0, "ytd_pct": 0.0, "level_change": 0.0},
            ],   # oil up / copper down -> exercises the derive_lead headline render
            "credit": rows(["HYG"]),
        },
        "macro": [
            {"id": "T10Y2Y", "name": "2s10s", "latest": 0.40, "change": 0.0,
             "pct_1y": 0.0, "z_1y": -2.1, "date": "2026-06-02"},
            {"id": "VIXCLS", "name": "VIX", "latest": 15.0, "change": 0.0,
             "pct_1y": 21.0, "z_1y": -0.7, "date": "2026-06-02"},
            {"id": "CPIAUCSL", "name": "CPI", "latest": 332.0, "change": 2.1,
             "pct_1y": None, "z_1y": None, "date": "2026-04-01"},   # trending -> blank %ile
        ],
        "bls": [{"id": "CUUR0000SA0", "name": "CPI-U", "latest": 333.0, "change": 0.3,
                 "yoy_pct": 3.8, "date": "2026-04"}],
        "energy": [{"id": "WCESTUS1", "name": "Crude (ex-SPR)", "latest": 433712.0,
                    "change": -7974.0, "units": "MBBL", "date": "2026-05-29"}],
        "positioning": [{"name": "S&P 500 (e-mini)", "lev_net": -457780.0, "lev_net_chg": -56226.0,
                         "asset_net": 1003607.0, "oi": 2093621.0, "date": "2026-05-26"}],
        "extremes": [{"symbol": "HG=F", "name": "Copper", "last": 6.48, "pct": 97.0, "z": 1.9, "n": 252},
                     {"symbol": "^VIX", "name": "VIX", "last": 16.0, "pct": 25.0, "z": -0.6, "n": 252}],
        "vol": {"vix": 16.0, "realized_20d": 10.0, "premium": 6.0},
        "movers": {"leaders": [{"name": "XLK", "change_pct": 2.0}],
                   "laggards": [{"name": "XLE", "change_pct": -1.0}]},
        "news": [{"title": "Test headline", "source": "Test", "link": "x",
                  "published": "2026-06-02T00:00:00", "summary": ""}],
        "stats": {"vix": 15.0, "sector_advancers": 1, "sector_decliners": 1, "sector_count": 2},
    }
    idx = pd.to_datetime(["2026-05-29", "2026-05-30", "2026-06-02"])
    closes = {s: pd.Series([100.0, 101.0, 102.0], index=idx) for s in ["^GSPC", "^TNX", "DX-Y.NYB"]}

    app.overview_tab(brief, closes)
    app.equities_tab(brief, closes)
    app.macro_tab(brief, closes)
    app.headlines_tab(brief)
    app.calendar_tab()
    app.narrative_tab(brief)


def test_all_tabs_render_without_error(monkeypatch, tmp_path):
    from src import config, history
    monkeypatch.setattr(history, "DB_PATH", tmp_path / "h.db")   # don't touch the real history DB
    # two narratives so the Story tab's watch-scorecard grades the prior's watch block
    ndir = tmp_path / "narratives"
    ndir.mkdir()
    (ndir / "narrative_2026-06-01.md").write_text(
        '# Prior\n```watch\n[{"claim":"VIX elevated","metric":"macro:VIXCLS",'
        '"trigger":">10","horizon":"next session"}]\n```\n', encoding="utf-8")
    (ndir / "narrative_2026-06-02.md").write_text("# Latest\nbody\n", encoding="utf-8")
    monkeypatch.setattr(config, "NARRATIVES_DIR", ndir)
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_function(_render_all_tabs).run()
    assert not at.exception, at.exception
