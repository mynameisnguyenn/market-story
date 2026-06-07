"""Upcoming-earnings calendar via yfinance — best-effort, degrades gracefully.

yfinance's earnings API shape shifts between versions; we read Ticker.calendar's
'Earnings Date' (a list of dates in 0.2.x) and tolerate anything else. Any failure
for a symbol is skipped rather than raised, so the dashboard never crashes on it.
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import date, datetime

import pandas as pd
import yfinance as yf

from . import config, macro_data

# Key economic releases by FRED release_id — the data a risk analyst trades around.
ECON_RELEASES = [(50, "Jobs report (payrolls)"), (10, "CPI"),
                 (21, "PCE / personal income"), (53, "GDP")]
_RELEASE_DATES_URL = "https://api.stlouisfed.org/fred/release/dates"

# FOMC rate-decision days (the second/last day of each meeting, when the statement is released),
# from the Fed's published calendar (federalreserve.gov/monetarypolicy/fomccalendars.htm).
# Static, no runtime feed — verified 2026-06; refresh annually when the Fed posts the next year.
FOMC_DECISIONS = [
    "2026-01-28", "2026-03-18", "2026-04-29", "2026-06-17", "2026-07-29",
    "2026-09-16", "2026-10-28", "2026-12-09",
    "2027-01-27", "2027-03-17", "2027-04-28", "2027-06-09", "2027-07-28",
    "2027-09-15", "2027-10-27", "2027-12-08",
]


def next_fomc(today: date | None = None) -> dict | None:
    """The next FOMC rate-decision day on/after `today`: {date, days}. None once the schedule
    runs out (a nudge to refresh FOMC_DECISIONS)."""
    today = today or date.today()
    for d in FOMC_DECISIONS:
        dd = date.fromisoformat(d)
        if dd >= today:
            return {"date": d, "days": (dd - today).days}
    return None


def _next_earnings_date(symbol: str) -> date | None:
    """Earliest upcoming earnings date for a symbol, or None."""
    try:
        cal = yf.Ticker(symbol).calendar
    except Exception:
        return None
    if isinstance(cal, dict):
        raw = cal.get("Earnings Date")
    else:                                   # older yfinance returned a DataFrame
        try:
            raw = list(cal.loc["Earnings Date"])
        except Exception:
            raw = None
    if raw is None:
        return None
    if not isinstance(raw, (list, tuple)):
        raw = [raw]
    today = date.today()
    upcoming = []
    for d in raw:
        ts = pd.to_datetime(d, errors="coerce")   # date/datetime/Timestamp/np.datetime64/ISO str
        if pd.notna(ts) and ts.date() >= today:
            upcoming.append(ts.date())
    return min(upcoming) if upcoming else None


def fetch_earnings(symbols: list[str], within_days: int = 60) -> list[dict]:
    """Upcoming earnings within `within_days`, earliest first. Best-effort."""
    today = date.today()
    rows = []
    for symbol in symbols:
        next_date = _next_earnings_date(symbol)
        if next_date is None:
            continue
        days = (next_date - today).days
        if 0 <= days <= within_days:
            rows.append({
                "symbol": symbol,
                "name": config.display_name(symbol),
                "date": next_date.isoformat(),
                "days": days,
            })
    rows.sort(key=lambda r: r["date"])
    return rows


def _next_release_date(release_id: int, key: str, today: str, timeout: int = 12) -> str | None:
    """First scheduled date on/after `today` for a FRED release. None on any failure."""
    url = _RELEASE_DATES_URL + "?" + urllib.parse.urlencode({
        "release_id": release_id, "api_key": key, "file_type": "json",
        "realtime_start": today, "include_release_dates_with_no_data": "true",
        "sort_order": "asc", "limit": 1})
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            payload = json.loads(resp.read())
        dates = payload.get("release_dates", [])
        return dates[0].get("date") if dates else None
    except Exception:
        return None


def fetch_econ_releases(within_days: int = 45) -> list[dict]:
    """Upcoming key US economic releases (the FRED publication schedule). Best-effort;
    [] without a FRED key. Each: {name, date, days}."""
    key = macro_data._load_env_key()
    if not key:
        return []
    today = date.today()
    rows = []
    for release_id, name in ECON_RELEASES:
        d = _next_release_date(release_id, key, today.isoformat())
        if not d:
            continue
        try:
            days = (date.fromisoformat(d) - today).days
        except ValueError:
            continue
        if 0 <= days <= within_days:
            rows.append({"name": name, "date": d, "days": days})
    rows.sort(key=lambda r: r["date"])
    return rows
