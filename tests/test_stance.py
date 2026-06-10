"""Stance ledger: parse -> log (omitted-visible) -> settle (next session) -> stats.

Pins the four traps the design grill caught: backfill_from_narratives() rewriting the file
must NOT drop stance rows; grade_pending() must NOT clobber pending stances to 'unresolved';
stats() must NOT count stance rows in the watch hit-rate; probability 0.0 must survive
(no falsy `or` chaining).
"""
import pandas as pd

from src import config, ledger, scorecard


# --- parse_stance -------------------------------------------------------------

def test_parse_stance_valid():
    text = 'x\n```stance\n{"direction": -1, "notes": "duration unwind"}\n```\ny'
    assert scorecard.parse_stance(text) == {"direction": -1, "notes": "duration unwind"}


def test_parse_stance_language_tag_and_flat():
    assert scorecard.parse_stance('```stance json\n{"direction": 0}\n```')["direction"] == 0


def test_parse_stance_invalid():
    assert scorecard.parse_stance("no block here") is None
    assert scorecard.parse_stance('```stance\n{"direction": 2}\n```') is None      # bad value
    assert scorecard.parse_stance('```stance\n{"direction": "1"}\n```') is None    # string, not int
    assert scorecard.parse_stance('```stance\n[1]\n```') is None                   # not a dict
    assert scorecard.parse_stance("") is None


# --- fixtures -----------------------------------------------------------------

def _setup(monkeypatch, tmp_path, narratives: dict[str, str]):
    ndir = tmp_path / "narratives"
    ndir.mkdir()
    for date, body in narratives.items():
        (ndir / f"narrative_{date}.md").write_text(body, encoding="utf-8")
    monkeypatch.setattr(config, "NARRATIVES_DIR", ndir)
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "ledger.jsonl")


_STANCE = '```stance\n{"direction": %d, "notes": "n"}\n```\n'


def _timeline():
    idx = pd.to_datetime(["2026-06-10", "2026-06-11", "2026-06-12"])
    return pd.DataFrame({"spx_chg": [0.5, -1.2, 0.8]}, index=idx)


# --- log + omitted-visible + idempotent ----------------------------------------

def test_log_stances_omitted_is_visible_and_prestart_exempt(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, {
        "2026-06-05": "# old, pre-stance era\n",            # before STANCE_START -> exempt
        "2026-06-10": "# has one\n" + _STANCE % -1,
        "2026-06-11": "# forgot the block\n",               # >= START, missing -> omitted
    })
    assert ledger.log_stances_from_narratives() == 2
    rows = [r for r in ledger.load() if r.get("kind") == "stance"]
    by_date = {r["logged"]: r for r in rows}
    assert set(by_date) == {"2026-06-10", "2026-06-11"}
    assert by_date["2026-06-10"]["direction"] == -1
    assert by_date["2026-06-11"]["status"] == "omitted"
    assert ledger.log_stances_from_narratives() == 0        # idempotent


# --- settle -------------------------------------------------------------------

def test_settle_uses_next_session_and_signs_pnl(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, {"2026-06-10": _STANCE % -1, "2026-06-12": _STANCE % 1})
    ledger.log_stances_from_narratives()
    from src import timeline
    monkeypatch.setattr(timeline, "load_df", _timeline)
    assert ledger.settle_stances() == 1                     # 06-12 has no next session yet
    by_date = {r["logged"]: r for r in ledger.load() if r.get("kind") == "stance"}
    assert by_date["2026-06-10"]["status"] == "settled"
    assert by_date["2026-06-10"]["spx_chg_next"] == -1.2    # the 06-11 print
    assert by_date["2026-06-10"]["pnl_pct"] == 1.2          # short into a down day -> win
    assert by_date["2026-06-12"]["status"] == "pending"


def test_stance_stats(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, {"2026-06-10": _STANCE % -1, "2026-06-11": _STANCE % 0,
                                   "2026-06-12": "no block\n"})
    ledger.log_stances_from_narratives()
    from src import timeline
    monkeypatch.setattr(timeline, "load_df", _timeline)
    ledger.settle_stances()
    s = ledger.stance_stats()
    assert s["n_logged"] == 3 and s["n_omitted"] == 1
    assert s["n_directional"] == 1 and s["win_rate"] == 1.0
    assert s["avg_pnl_bps"] == 120.0                        # +1.2% on the one settled call
    assert s["n_flat"] == 1                                 # 06-11 flat settled vs 06-12 print


# --- the four grill traps -----------------------------------------------------

def test_backfill_rewrite_preserves_stance_rows(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, {"2026-06-10": _STANCE % 1 +
                                   '```watch\n[{"claim":"c","metric":"macro:DGS10","trigger":">4.5","horizon":"next session"}]\n```'})
    ledger.log_stances_from_narratives()
    monkeypatch.setattr(ledger, "_grade", lambda rec: rec)  # no network/archive in tests
    ledger.backfill_from_narratives()                       # full rewrite of the file
    rows = ledger.load()
    assert any(r.get("kind") == "stance" for r in rows), "rebuild dropped the stance ledger"
    assert any(r.get("metric") == "macro:DGS10" for r in rows)


def test_grade_pending_skips_stances(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, {"2026-06-10": _STANCE % 1})
    ledger.log_stances_from_narratives()
    ledger.grade_pending()                                  # must not touch the stance row
    row = next(r for r in ledger.load() if r.get("kind") == "stance")
    assert row["status"] == "pending", "grade_pending clobbered a stance to unresolved"


def test_watch_stats_exclude_stance_rows(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, {"2026-06-10": _STANCE % 1})
    ledger.log_stances_from_narratives()
    s = ledger.stats()
    assert s["total"] == 0                                  # stance rows are not watch records


def test_settle_flat_stance_pnl_none_with_provenance(monkeypatch, tmp_path):
    """A flat (direction 0) settled stance records pnl_pct=None (not 0.0, which would look like a
    break-even directional trade) and a settlement_date for audit provenance."""
    _setup(monkeypatch, tmp_path, {"2026-06-10": _STANCE % 0})
    ledger.log_stances_from_narratives()
    from src import timeline
    monkeypatch.setattr(timeline, "load_df", _timeline)
    ledger.settle_stances()
    row = next(r for r in ledger.load() if r.get("kind") == "stance")
    assert row["status"] == "settled"
    assert row["pnl_pct"] is None                       # flat -> no P&L, NOT 0.0
    assert row["spx_chg_next"] == -1.2
    assert row["settlement_date"] == "2026-06-11"       # which row settled it


def test_backfill_preserves_asof_value(monkeypatch, tmp_path):
    """The daily backfill rewrite must NOT wipe the at-log-time snapshot captured by
    log_predictions() (the markdown has no asof_value; a naive rebuild would null it forever)."""
    _setup(monkeypatch, tmp_path, {"2026-06-10":
        '```watch\n[{"claim":"c","metric":"macro:DGS10","trigger":">4.5","horizon":"next session"}]\n```'})
    ledger.log_predictions("2026-06-10", [{"claim": "c", "metric": "macro:DGS10",
                                           "trigger": ">4.5", "horizon": "next session"}],
                           asof={"macro": [{"id": "DGS10", "latest": 4.42}]})
    assert ledger.load()[0]["asof_value"] == 4.42
    monkeypatch.setattr(ledger, "_grade", lambda rec: rec)   # no archive/network in tests
    ledger.backfill_from_narratives()                        # full rewrite of the file
    rec = next(r for r in ledger.load() if r.get("metric") == "macro:DGS10")
    assert rec["asof_value"] == 4.42, "backfill wiped the at-log-time snapshot"


def test_probability_zero_survives(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, {})
    ledger.log_predictions("2026-06-10", [{"claim": "c", "metric": "macro:DGS10",
                                           "trigger": ">4.5", "horizon": "next session",
                                           "probability": 0.0}])
    rec = ledger.load()[0]
    assert rec["confidence"] == 0.0, "probability 0.0 was dropped by falsy chaining"
