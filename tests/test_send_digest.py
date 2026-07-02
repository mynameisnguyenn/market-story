"""send_digest guards + always-exit-0 contract — SMTP mocked, no network."""
import json
import smtplib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import send_digest  # noqa: E402

from src import brief as brief_mod, ledger  # noqa: E402


def test_date_match_same_date_passes():
    ok, reason = send_digest._date_match(Path("brief_2026-07-02.json"),
                                         Path("narrative_2026-07-02.md"))
    assert ok and reason == ""


def test_date_match_mismatch_skips_with_reason():
    ok, reason = send_digest._date_match(Path("brief_2026-07-01.json"),
                                         Path("narrative_2026-07-02.md"))
    assert not ok and "2026-07-01" in reason and "2026-07-02" in reason


def test_date_match_missing_brief():
    ok, reason = send_digest._date_match(None, Path("narrative_2026-07-02.md"))
    assert not ok and "brief" in reason


def test_date_match_missing_narrative():
    ok, reason = send_digest._date_match(Path("brief_2026-07-02.json"), None)
    assert not ok and "narrative" in reason


def test_already_sent_three_states(tmp_path):
    marker = tmp_path / ".last_sent"
    assert not send_digest._already_sent("2026-07-02", marker)          # marker missing
    marker.write_text("2026-07-01\n", encoding="utf-8")
    assert not send_digest._already_sent("2026-07-02", marker)          # stale marker
    marker.write_text("2026-07-02\n", encoding="utf-8")
    assert send_digest._already_sent("2026-07-02", marker)              # already sent


class _SMTPSpy:
    calls = 0
    fail = False

    def __init__(self, *args, **kwargs):
        type(self).calls += 1

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def login(self, *args):
        pass

    def send_message(self, msg):
        if type(self).fail:
            raise RuntimeError("smtp down")
        type(self).last_subject = msg["Subject"]


def _setup(monkeypatch, tmp_path, brief_date="2026-07-02", narrative_date="2026-07-02"):
    bp = tmp_path / f"brief_{brief_date}.json"
    bp.write_text(json.dumps({"date": brief_date, "markets": {}, "stats": {}}), encoding="utf-8")
    nb = tmp_path / f"narrative_{narrative_date}.md"
    nb.write_text('## Today in one line\nTest thesis.\n```stance\n{"direction": 1, "notes": "t"}\n```\n',
                  encoding="utf-8")
    monkeypatch.setattr(brief_mod, "latest_brief_path", lambda: bp)
    monkeypatch.setattr(brief_mod, "latest_narrative_path", lambda: nb)
    monkeypatch.setattr(brief_mod, "prior_narrative_path", lambda: None)
    monkeypatch.setattr(ledger, "LEDGER_PATH", tmp_path / "ledger.jsonl")
    monkeypatch.setattr(send_digest, "MARKER_PATH", tmp_path / "emails" / ".last_sent")
    monkeypatch.setenv("GMAIL_USERNAME", "u@example.com")
    monkeypatch.setenv("GMAIL_APP_PASSWORD", "app-password")
    monkeypatch.setenv("MAIL_TO", "u@example.com")
    _SMTPSpy.calls, _SMTPSpy.fail = 0, False
    monkeypatch.setattr(smtplib, "SMTP_SSL", _SMTPSpy)


def _run_main():
    with pytest.raises(SystemExit) as exc_info:
        send_digest.main()
    assert exc_info.value.code == 0                          # the always-exit-0 contract


def test_main_sends_once_and_writes_marker(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path)
    _run_main()
    assert _SMTPSpy.calls == 1
    assert "2026-07-02" in _SMTPSpy.last_subject and "▲" in _SMTPSpy.last_subject
    assert send_digest.MARKER_PATH.read_text(encoding="utf-8").strip() == "2026-07-02"


def test_main_skips_on_date_mismatch(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, brief_date="2026-07-01")   # brief lags the narrative
    _run_main()
    assert _SMTPSpy.calls == 0


def test_main_skips_when_already_sent(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path)
    send_digest.MARKER_PATH.parent.mkdir(parents=True)
    send_digest.MARKER_PATH.write_text("2026-07-02\n", encoding="utf-8")
    _run_main()
    assert _SMTPSpy.calls == 0


def test_main_skips_without_secrets(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path)
    monkeypatch.delenv("GMAIL_APP_PASSWORD")
    _run_main()
    assert _SMTPSpy.calls == 0


def test_main_exits_zero_when_smtp_fails_and_marker_unwritten(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path)
    _SMTPSpy.fail = True
    _run_main()                                              # exception swallowed, exit 0
    assert not send_digest.MARKER_PATH.exists()              # failed send can retry next push
