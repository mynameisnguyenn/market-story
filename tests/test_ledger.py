"""Prediction ledger — synthetic macro archive + mocked market fetch, no network."""
import json

import pandas as pd

from src import config, ledger, macro_data


def _seed_macro(tmp_path, monkeypatch, rows):
    p = tmp_path / "macro.jsonl"
    p.write_text("\n".join(json.dumps({"series": s, "date": d, "value": v}) for s, d, v in rows),
                 encoding="utf-8")
    monkeypatch.setattr(macro_data, "ARCHIVE_PATH", p)


def _isolate_briefs(tmp_path, monkeypatch):
    """Point BRIEFS_DIR at a dir that is never created — no test may read the real repo briefs."""
    monkeypatch.setattr(config, "BRIEFS_DIR", tmp_path / "briefs")


def test_horizon_sessions():
    assert ledger.horizon_sessions("next session") == 1
    assert ledger.horizon_sessions("next 2 sessions") == 2
    assert ledger.horizon_sessions("next week") == 5
    assert ledger.horizon_sessions("over the next month") == 21


def test_horizon_sessions_iso_date():
    # Wed 07-01 -> Wed 07-08 spans 5 business days (07-04 is a Saturday, no holiday dependency)
    assert ledger.horizon_sessions("2026-07-08", "2026-07-01") == 5


def test_horizon_sessions_iso_date_in_past_clamps_to_one():
    assert ledger.horizon_sessions("2026-06-01", "2026-07-01") == 1


def test_horizon_sessions_malformed_iso_falls_through():
    assert ledger.horizon_sessions("2026-13-40", "2026-07-01") == 1


def test_macro_threshold_hit_and_miss(tmp_path, monkeypatch):
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "log.jsonl")
    _isolate_briefs(tmp_path, monkeypatch)
    _seed_macro(tmp_path, monkeypatch, [
        ("DGS10", "2026-06-04", 4.48), ("DGS10", "2026-06-05", 4.52),     # ends the window above 4.5
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


def test_level_metric_transient_touch_reverses_is_miss(tmp_path, monkeypatch):
    """A level metric (yield) that pierces the trigger mid-window but closes back inside is a
    MISS — level claims grade at the end of the horizon, not any-point-in-window."""
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "log.jsonl")
    _isolate_briefs(tmp_path, monkeypatch)
    _seed_macro(tmp_path, monkeypatch, [
        ("DGS10", "2026-06-04", 4.55), ("DGS10", "2026-06-05", 4.40),   # touched >4.5 then reversed
    ])
    ledger.log_predictions("2026-06-03", [
        {"claim": "10Y holds above 4.5", "metric": "macro:DGS10", "trigger": ">4.5", "horizon": "next week"}])
    ledger.grade_pending()
    r = ledger.load()[0]
    assert r["status"] == "missed" and r["graded_value"] == 4.40


def test_event_metric_grades_any_point_in_window(tmp_path, monkeypatch):
    """An event metric (a single-day % change) grades any-point-in-window — a one-day gap that
    later reverses still counts as triggered."""
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "log.jsonl")
    _isolate_briefs(tmp_path, monkeypatch)
    _seed_macro(tmp_path, monkeypatch, [])
    idx = pd.to_datetime(["2026-06-04", "2026-06-05"])
    monkeypatch.setattr(ledger, "_market_window",
                        lambda sym, field, start, sess: [-12.0, 1.0])   # gap day, then bounce
    ledger.log_predictions("2026-06-03", [
        {"claim": "AVGO gaps down", "metric": "market:AVGO:change_pct", "trigger": "<-10", "horizon": "next week"}])
    ledger.grade_pending()
    r = ledger.load()[0]
    assert r["status"] == "triggered" and r["graded_value"] == -12.0


def test_single_name_resolves_via_market_fetch(tmp_path, monkeypatch):
    """The whole point of the fix: a single-name call the old scorecard returned None for."""
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "log.jsonl")
    _isolate_briefs(tmp_path, monkeypatch)
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
    _isolate_briefs(tmp_path, monkeypatch)
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


def _write_brief(briefs_dir, date, symbol, last, change_pct):
    briefs_dir.mkdir(parents=True, exist_ok=True)
    (briefs_dir / f"brief_{date}.json").write_text(json.dumps(
        {"date": date, "markets": {"us_equities": [
            {"symbol": symbol, "last": last, "change_pct": change_pct}]}}), encoding="utf-8")


def test_market_window_prefers_committed_brief(tmp_path, monkeypatch):
    """Committed brief data grades market: items with zero network — the CI-reliability fix."""
    _isolate_briefs(tmp_path, monkeypatch)
    _write_brief(tmp_path / "briefs", "2026-06-04", "NVDA", 120.0, 3.2)
    _write_brief(tmp_path / "briefs", "2026-06-05", "NVDA", 118.7, -1.1)
    monkeypatch.setattr(ledger, "_fetch_market",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("network path must not fire")))
    assert ledger._market_window("NVDA", "change_pct", "2026-06-03", 2) == [3.2, -1.1]


def test_market_window_falls_back_to_yfinance_when_symbol_absent(tmp_path, monkeypatch):
    """A symbol the briefs never carry (single name) still resolves via the yfinance fallback."""
    _isolate_briefs(tmp_path, monkeypatch)
    _write_brief(tmp_path / "briefs", "2026-06-04", "NVDA", 120.0, 3.2)
    idx = pd.to_datetime(["2026-06-04", "2026-06-05"])
    monkeypatch.setattr(ledger, "_fetch_market",
                        lambda sym, start, sess: pd.Series([250.0, 212.5], index=idx))
    vals = ledger._market_window("AVGO", "change_pct", "2026-06-03", 2)
    assert vals and vals[0] <= -10                      # -15% derived from the mocked series
