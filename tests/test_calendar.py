"""Tests for earnings-calendar parsing (yfinance mocked, no network)."""
from datetime import date, timedelta

from src import calendar_data


class _FakeTicker:
    def __init__(self, cal):
        self._cal = cal

    @property
    def calendar(self):
        return self._cal


def _patch(monkeypatch, mapping):
    monkeypatch.setattr(calendar_data.yf, "Ticker", lambda s: _FakeTicker(mapping.get(s)))


def test_fetch_earnings_picks_next_future_date(monkeypatch):
    soon = date.today() + timedelta(days=10)
    _patch(monkeypatch, {"AAA": {"Earnings Date": [soon]}})
    rows = calendar_data.fetch_earnings(["AAA"])
    assert len(rows) == 1
    assert rows[0]["symbol"] == "AAA" and rows[0]["date"] == soon.isoformat()
    assert rows[0]["days"] == 10


def test_fetch_earnings_skips_past_and_far(monkeypatch):
    past = date.today() - timedelta(days=5)
    far = date.today() + timedelta(days=120)
    _patch(monkeypatch, {"PAST": {"Earnings Date": [past]}, "FAR": {"Earnings Date": [far]}})
    assert calendar_data.fetch_earnings(["PAST", "FAR"], within_days=60) == []


def test_fetch_earnings_sorted_and_skips_missing(monkeypatch):
    d_far = date.today() + timedelta(days=30)
    d_near = date.today() + timedelta(days=5)
    _patch(monkeypatch, {"A": {"Earnings Date": [d_far]}, "B": {"Earnings Date": [d_near]}, "C": None})
    rows = calendar_data.fetch_earnings(["A", "B", "C"])
    assert [r["symbol"] for r in rows] == ["B", "A"]
