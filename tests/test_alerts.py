"""Tests for alert_rules.py and notifier.py — no network, synthetic data only."""
import sys
import types

import pytest

from src.alert_rules import evaluate_alerts, VIX_LEVEL_MIN, VIX_PCT_MIN, _HONESTY
from src import notifier


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _brief(level, pct):
    """Minimal brief with a single ^VIX extremes row."""
    return {"extremes": [{"symbol": "^VIX", "name": "VIX", "last": level, "pct": pct}]}


# ---------------------------------------------------------------------------
# alert_rules: boundary / gate tests
# ---------------------------------------------------------------------------

def test_fires_at_exact_minimum():
    alerts = evaluate_alerts(_brief(VIX_LEVEL_MIN, VIX_PCT_MIN))
    assert len(alerts) == 1
    assert alerts[0]["priority"] == "high"


def test_does_not_fire_level_just_below():
    alerts = evaluate_alerts(_brief(VIX_LEVEL_MIN - 0.1, VIX_PCT_MIN))
    assert alerts == []


def test_does_not_fire_pct_just_below():
    alerts = evaluate_alerts(_brief(VIX_LEVEL_MIN, VIX_PCT_MIN - 0.1))
    assert alerts == []


def test_fires_above_both_thresholds():
    alerts = evaluate_alerts(_brief(30.0, 95.0))
    assert len(alerts) == 1


def test_title_contains_level_and_pct():
    alerts = evaluate_alerts(_brief(27.3, 94.0))
    title = alerts[0]["title"]
    assert "27.3" in title
    assert "94" in title


def test_honesty_line_verbatim_in_body():
    alerts = evaluate_alerts(_brief(27.3, 94.0))
    assert _HONESTY in alerts[0]["body"]


def test_missing_extremes_key():
    assert evaluate_alerts({}) == []


def test_extremes_empty_list():
    assert evaluate_alerts({"extremes": []}) == []


def test_no_vix_row():
    brief = {"extremes": [{"symbol": "^GSPC", "last": 5500, "pct": 60}]}
    assert evaluate_alerts(brief) == []


def test_none_level_field():
    brief = {"extremes": [{"symbol": "^VIX", "last": None, "pct": 90.0}]}
    assert evaluate_alerts(brief) == []


def test_none_pct_field():
    brief = {"extremes": [{"symbol": "^VIX", "last": 28.0, "pct": None}]}
    assert evaluate_alerts(brief) == []


def test_both_none_fields():
    brief = {"extremes": [{"symbol": "^VIX", "last": None, "pct": None}]}
    assert evaluate_alerts(brief) == []


def test_non_dict_brief():
    assert evaluate_alerts(None) == []
    assert evaluate_alerts("not a dict") == []


def test_extremes_not_a_list():
    assert evaluate_alerts({"extremes": "bad"}) == []


# ---------------------------------------------------------------------------
# notifier: transport tests
# ---------------------------------------------------------------------------

def test_no_topic_returns_zero_no_exception(monkeypatch):
    monkeypatch.delenv("NTFY_TOPIC", raising=False)
    result = notifier.send_alerts([{"title": "T", "body": "B", "priority": "high"}])
    assert result == 0


def test_empty_topic_returns_zero(monkeypatch):
    monkeypatch.setenv("NTFY_TOPIC", "")
    result = notifier.send_alerts([{"title": "T", "body": "B", "priority": "high"}])
    assert result == 0


def test_with_topic_posts_correct_url_headers_body(monkeypatch):
    monkeypatch.setenv("NTFY_TOPIC", "test-topic-abc")
    calls = []

    def fake_post(url, data=None, headers=None, **kwargs):   # tolerate timeout= and friends
        calls.append({"url": url, "data": data, "headers": headers, "kwargs": kwargs})

    # The function does `import requests` inside; stub it via sys.modules.
    fake_requests = types.SimpleNamespace(post=fake_post)
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    alert = {"title": "VIX 28.0 — 90th percentile of 1y", "body": "VIX at 28.0. " + _HONESTY, "priority": "high"}
    count = notifier.send_alerts([alert])

    assert count == 1
    assert len(calls) == 1
    assert calls[0]["url"] == "https://ntfy.sh/test-topic-abc"
    assert calls[0]["headers"]["Title"] == alert["title"]
    assert calls[0]["headers"]["Priority"] == "high"
    assert calls[0]["headers"]["Tags"] == "chart_with_downwards_trend"
    assert calls[0]["data"] == alert["body"].encode("utf-8")
    assert calls[0]["kwargs"].get("timeout") is not None   # never let a hung POST stall the Action


def test_multiple_alerts_counted(monkeypatch):
    monkeypatch.setenv("NTFY_TOPIC", "test-topic-abc")
    fake_requests = types.SimpleNamespace(post=lambda *a, **kw: None)
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    alerts = [
        {"title": "A1", "body": "body1", "priority": "high"},
        {"title": "A2", "body": "body2", "priority": "high"},
    ]
    assert notifier.send_alerts(alerts) == 2


def test_post_raising_is_swallowed(monkeypatch):
    monkeypatch.setenv("NTFY_TOPIC", "test-topic-abc")

    def exploding_post(*args, **kwargs):
        raise RuntimeError("network is dead")

    fake_requests = types.SimpleNamespace(post=exploding_post)
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    result = notifier.send_alerts([{"title": "T", "body": "B", "priority": "high"}])
    assert result == 0   # failure swallowed, not raised


def test_no_topic_with_multiple_alerts_returns_zero(monkeypatch):
    monkeypatch.delenv("NTFY_TOPIC", raising=False)
    alerts = [{"title": "A", "body": "B", "priority": "high"}] * 5
    assert notifier.send_alerts(alerts) == 0
