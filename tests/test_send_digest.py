"""send_digest guards + always-exit-0 contract — Resend API mocked, no network."""
import json
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


class _Resp:
    def __init__(self, status_code):
        self.status_code = status_code
        self.text = "" if status_code == 200 else '{"message": "invalid key"}'


class _PostSpy:
    calls = 0
    status = 200
    raise_exc = False
    last_payload = None

    @classmethod
    def post(cls, url, headers=None, json=None, timeout=None):
        cls.calls += 1
        cls.last_payload = json
        if cls.raise_exc:
            raise RuntimeError("network down")
        return _Resp(cls.status)


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
    monkeypatch.setenv("RESEND_API_KEY", "re_test_key")
    monkeypatch.setenv("MAIL_TO", "u@example.com")
    _PostSpy.calls, _PostSpy.status, _PostSpy.raise_exc = 0, 200, False
    monkeypatch.setattr(send_digest.requests, "post", _PostSpy.post)


def _run_main():
    with pytest.raises(SystemExit) as exc_info:
        send_digest.main()
    assert exc_info.value.code == 0                          # the always-exit-0 contract


def test_main_sends_once_and_writes_marker(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path)
    _run_main()
    assert _PostSpy.calls == 1
    subject = _PostSpy.last_payload["subject"]
    assert "2026-07-02" in subject and "▲" in subject
    assert _PostSpy.last_payload["to"] == ["u@example.com"]
    assert "<!DOCTYPE html>" in _PostSpy.last_payload["html"]
    assert send_digest.MARKER_PATH.read_text(encoding="utf-8").strip() == "2026-07-02"


def test_main_skips_on_date_mismatch(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, brief_date="2026-07-01")   # brief lags the narrative
    _run_main()
    assert _PostSpy.calls == 0


def test_main_skips_when_already_sent(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path)
    send_digest.MARKER_PATH.parent.mkdir(parents=True)
    send_digest.MARKER_PATH.write_text("2026-07-02\n", encoding="utf-8")
    _run_main()
    assert _PostSpy.calls == 0


def test_main_skips_without_secrets(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path)
    monkeypatch.delenv("RESEND_API_KEY")
    _run_main()
    assert _PostSpy.calls == 0


def test_main_exits_zero_on_api_error_and_marker_unwritten(monkeypatch, tmp_path):
    """A non-2xx Resend response leaves the marker unwritten so the next push retries."""
    _setup(monkeypatch, tmp_path)
    _PostSpy.status = 401
    _run_main()
    assert not send_digest.MARKER_PATH.exists()


def test_main_exits_zero_when_network_fails_and_marker_unwritten(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path)
    _PostSpy.raise_exc = True
    _run_main()                                              # exception swallowed, exit 0
    assert not send_digest.MARKER_PATH.exists()              # failed send can retry next push
