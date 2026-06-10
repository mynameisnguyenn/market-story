"""CI entry point: find the newest brief, evaluate VIX alert rules, send via ntfy.

Always exits 0 — alert failures must never break the daily GitHub Action.
"""
import json
import sys
from pathlib import Path

# Bootstrap: put repo root on sys.path (mirrors research/signal_battery.py).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.alert_rules import evaluate_alerts
from src.notifier import send_alerts


def _find_newest_brief(briefs_dir: Path) -> Path | None:
    """Return the Path of the newest brief_*.json by filename sort, or None."""
    if not briefs_dir.exists():
        return None
    candidates = sorted(briefs_dir.glob("brief_*.json"))
    return candidates[-1] if candidates else None


def main() -> None:
    """Load newest brief, evaluate alerts, send, print summary."""
    briefs_dir = Path(__file__).resolve().parent.parent / "data" / "briefs"

    brief_path = _find_newest_brief(briefs_dir)
    if brief_path is None:
        print("send_alerts: no briefs found — nothing to do.")
        sys.exit(0)

    try:
        with open(brief_path, encoding="utf-8") as fh:
            brief = json.load(fh)
    except Exception as exc:
        print(f"send_alerts: could not read {brief_path.name}: {exc}")
        sys.exit(0)

    alerts = evaluate_alerts(brief)
    n = send_alerts(alerts)
    print(f"{n} alert(s) sent")
    sys.exit(0)


if __name__ == "__main__":
    main()
