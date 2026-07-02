"""CI entry point: render the daily digest and email it via Gmail SMTP.

Always exits 0 — a digest failure must never break the pipeline. Sends only when the
newest brief and newest narrative carry the SAME date: GitHub's cron queue lands the
daily brief 1.5-4.5h AFTER the ~12:45 UTC narrative (see BUILD_LOG 2026-07-02), so the
narrative push date-mismatches and skips, and the later brief push completes the pair.
send-digest.yml therefore triggers on pushes to BOTH data/narratives/** and
data/briefs/**; the committed data/emails/.last_sent marker prevents a double send.
"""
import json
import os
import re
import sys
from pathlib import Path

# Bootstrap: put repo root on sys.path (mirrors scripts/send_alerts.py).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

MARKER_PATH = Path(__file__).resolve().parent.parent / "data" / "emails" / ".last_sent"
_ARROW = {1: "▲", -1: "▼", 0: "→"}


def _file_date(path: Path | None) -> str | None:
    """YYYY-MM-DD from a brief_/narrative_ filename, or None."""
    if path is None:
        return None
    m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    return m.group(1) if m else None


def _date_match(brief_path: Path | None, narrative_path: Path | None) -> tuple[bool, str]:
    """Both files exist and carry the same date — the guard against emailing today's
    thesis over yesterday's numbers (the commit-order inversion)."""
    bd, nd = _file_date(brief_path), _file_date(narrative_path)
    if not bd:
        return False, "no brief on disk"
    if not nd:
        return False, "no narrative on disk"
    if bd != nd:
        return False, f"brief={bd} narrative={nd} — pipeline mid-commit, waiting for the pair"
    return True, ""


def _already_sent(narrative_date: str, marker_path: Path | None = None) -> bool:
    marker = marker_path if marker_path is not None else MARKER_PATH
    try:
        return marker.read_text(encoding="utf-8").strip() == narrative_date
    except Exception:
        return False


def main() -> None:
    from src import brief as brief_mod, email_digest, ledger, scorecard

    brief_path = brief_mod.latest_brief_path()
    narrative_path = brief_mod.latest_narrative_path()
    ok, reason = _date_match(brief_path, narrative_path)
    if not ok:
        print(f"send_digest: {reason} — skipping.")
        sys.exit(0)
    digest_date = _file_date(narrative_path)
    if _already_sent(digest_date):
        print(f"send_digest: {digest_date} already sent — skipping.")
        sys.exit(0)
    user = os.environ.get("GMAIL_USERNAME")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    mail_to = os.environ.get("MAIL_TO")
    if not (user and password and mail_to):
        print("send_digest: GMAIL_USERNAME/GMAIL_APP_PASSWORD/MAIL_TO not set — skipping.")
        sys.exit(0)

    try:
        import smtplib
        from email.message import EmailMessage

        brief = json.loads(brief_path.read_text(encoding="utf-8"))
        html = email_digest.render_email(brief, ledger_rows=ledger.load())
        stance = scorecard.parse_stance(narrative_path.read_text(encoding="utf-8"))
        arrow = _ARROW.get(stance["direction"], "•") if stance else "•"
        clause = email_digest._thesis(brief)[:60]

        msg = EmailMessage()
        msg["Subject"] = f"Market Story — {digest_date} — {arrow} {clause}"
        msg["From"] = user
        msg["To"] = mail_to
        msg.set_content("Open in an HTML mail client to read the daily brief.")
        msg.add_alternative(html, subtype="html")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
        MARKER_PATH.parent.mkdir(parents=True, exist_ok=True)
        MARKER_PATH.write_text(digest_date + "\n", encoding="utf-8")
        print(f"send_digest: sent {digest_date} digest to {mail_to}.")
    except Exception as exc:
        print(f"send_digest: send failed: {exc}")
    sys.exit(0)


if __name__ == "__main__":
    main()
