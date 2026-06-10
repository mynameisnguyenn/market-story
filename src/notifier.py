"""Thin ntfy.sh transport — POSTs alert dicts to a configured topic.

SECURITY NOTE: the NTFY_TOPIC value is never printed or logged here.
The topic name is the only authentication ntfy.sh has; leaking it
would allow anyone to send (or read, on paid plans) to that channel.
"""
from __future__ import annotations

import os


def send_alerts(alerts: list[dict]) -> int:
    """POST each alert to ntfy.sh/<topic>; return count of alerts sent.

    Reads NTFY_TOPIC from environment. If absent or empty, silently returns 0.
    Never raises — individual POST failures are swallowed and counted as unsent.
    """
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    if not topic:
        return 0

    import requests

    url = f"https://ntfy.sh/{topic}"
    sent = 0
    for alert in alerts:
        try:
            resp = requests.post(
                url,
                data=alert.get("body", "").encode("utf-8"),
                headers={
                    "Title": alert.get("title", ""),
                    "Priority": alert.get("priority", "default"),
                    "Tags": "chart_with_downwards_trend",
                },
                timeout=10,                      # a hung POST must not hang the daily Action
            )
            if getattr(resp, "ok", True):        # non-2xx counts as unsent; absent .ok = sent
                sent += 1
        except Exception:
            pass
    return sent
