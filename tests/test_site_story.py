"""Story-tab calibration panel — synthetic ledger via a tmp LEDGER_PATH, no network."""
import json

from src import calibration, ledger
from src.site.tabs import story


def _setup(monkeypatch, tmp_path, rows):
    """Write synthetic ledger rows through the real persistence path (mirrors test_stance)."""
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "ledger.jsonl")
    ledger._write(rows)


def _graded_rows(n, prob_a=0.3, prob_b=0.6):
    """n gradeable watch rows across two probability buckets, ~half triggered."""
    rows = []
    for i in range(n):
        rows.append({"logged": f"2026-06-{(i % 28) + 1:02d}", "claim": f"c{i}",
                     "metric": "macro:DGS10", "trigger": ">4", "horizon": "next session",
                     "status": "triggered" if i % 2 == 0 else "missed",
                     "probability": prob_a if i % 3 else prob_b})
    return rows


def test_calibration_panel_absent_below_min_n(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, _graded_rows(calibration.MIN_N - 6))
    html = story._track_record()
    assert "Hit rate" in html                     # track record still renders
    assert "Calibration" not in html              # panel gated off below MIN_N


def test_calibration_panel_present_above_min_n(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, _graded_rows(calibration.MIN_N + 6))
    html = story._track_record()
    assert "Calibration" in html and "<table>" in html
    assert "Brier" in html and "base rate" in html


def test_calibration_panel_failure_does_not_blank_track_record(monkeypatch, tmp_path):
    """A bug in the calibration path degrades to nothing — hit-rate/stance keep rendering."""
    _setup(monkeypatch, tmp_path, _graded_rows(calibration.MIN_N + 6))

    def _boom(records):
        raise RuntimeError("calibration bug")

    monkeypatch.setattr(calibration, "gradeable", _boom)
    html = story._track_record()
    assert "Hit rate" in html and "Calibration" not in html
