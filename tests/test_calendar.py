"""Tests for earnings + econ-release calendars (network mocked, no calls)."""
from datetime import date, timedelta

from src import calendar_data, macro_data


def test_fetch_econ_releases_filters_window_and_sorts(monkeypatch):
    monkeypatch.setattr(macro_data, "_load_env_key", lambda: "key")
    soon = (date.today() + timedelta(days=2)).isoformat()
    far = (date.today() + timedelta(days=400)).isoformat()
    schedule = {50: soon, 10: far}     # jobs soon; CPI far; PCE/GDP -> None (skipped)
    monkeypatch.setattr(calendar_data, "_next_release_date",
                        lambda rid, key, today, **k: schedule.get(rid))
    rows = calendar_data.fetch_econ_releases(within_days=45)
    assert [r["name"] for r in rows] == ["Jobs report (payrolls)"]   # far CPI excluded
    assert rows[0]["days"] == 2


def test_fetch_econ_releases_no_key(monkeypatch):
    monkeypatch.setattr(macro_data, "_load_env_key", lambda: None)
    assert calendar_data.fetch_econ_releases() == []


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
