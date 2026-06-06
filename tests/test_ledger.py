"""Prediction ledger — synthetic macro archive + mocked market fetch, no network."""
import json

import pandas as pd

from src import ledger, macro_data


def _seed_macro(tmp_path, monkeypatch, rows):
    p = tmp_path / "macro.jsonl"
    p.write_text("\n".join(json.dumps({"series": s, "date": d, "value": v}) for s, d, v in rows),
                 encoding="utf-8")
    monkeypatch.setattr(macro_data, "ARCHIVE_PATH", p)


def test_horizon_sessions():
    assert ledger.horizon_sessions("next session") == 1
    assert ledger.horizon_sessions("next 2 sessions") == 2
    assert ledger.horizon_sessions("next week") == 5
    assert ledger.horizon_sessions("over the next month") == 21


def test_macro_threshold_hit_and_miss(tmp_path, monkeypatch):
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "log.jsonl")
    _seed_macro(tmp_path, monkeypatch, [
        ("DGS10", "2026-06-04", 4.52), ("DGS10", "2026-06-05", 4.48),     # exceeded 4.5 in-window
        ("T10Y2Y", "2026-06-04", 0.42), ("T10Y2Y", "2026-06-05", 0.41),   # never exceeded 0.55
    ])
    ledger.log_predictions("2026-06-03", [
        {"claim": "10Y breaks 4.5", "metric": "macro:DGS10", "trigger": ">4.5", "horizon": "next week"},
        {"claim": "curve steepens", "metric": "macro:T10Y2Y", "trigger": ">0.55", "horizon": "next week"},
    ])
    s = ledger.grade_pending()
    by = {r["metric"]: r["status"] for r in ledger.load()}
    assert by["macro:DGS10"] == "triggered"
    assert by["macro:T10Y2Y"] == "missed"
    assert s["hit_rate"] == 0.5


def test_single_name_resolves_via_market_fetch(tmp_path, monkeypatch):
    """The whole point of the fix: a single-name call the old scorecard returned None for."""
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "log.jsonl")
    _seed_macro(tmp_path, monkeypatch, [])
    idx = pd.to_datetime(["2026-06-03", "2026-06-04"])
    monkeypatch.setattr(ledger, "_fetch_market",     # AVGO 250 -> 212.5 = -15% on 06-04
                        lambda sym, start, sess: pd.Series([250.0, 212.5], index=idx))
    ledger.log_predictions("2026-06-03", [
        {"claim": "AVGO gap", "metric": "market:AVGO:change_pct", "trigger": "<-10", "horizon": "next session"}])
    ledger.grade_pending()
    r = ledger.load()[0]
    assert r["status"] == "triggered" and r["graded_value"] <= -10


def test_pending_when_window_not_elapsed(tmp_path, monkeypatch):
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "log.jsonl")
    _seed_macro(tmp_path, monkeypatch, [("DGS10", "2026-06-01", 4.4)])   # only data BEFORE the call
    ledger.log_predictions("2026-06-03", [
        {"claim": "x", "metric": "macro:DGS10", "trigger": ">4.5", "horizon": "next session"}])
    ledger.grade_pending()
    assert ledger.load()[0]["status"] == "pending"


def test_log_predictions_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "log.jsonl")
    item = [{"claim": "x", "metric": "macro:DGS10", "trigger": ">4.5", "horizon": "next session"}]
    ledger.log_predictions("2026-06-03", item)
    ledger.log_predictions("2026-06-03", item)          # same key -> no duplicate
    assert len(ledger.load()) == 1
