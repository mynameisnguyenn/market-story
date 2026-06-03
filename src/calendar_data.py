"""Upcoming-earnings calendar via yfinance — best-effort, degrades gracefully.

yfinance's earnings API shape shifts between versions; we read Ticker.calendar's
'Earnings Date' (a list of dates in 0.2.x) and tolerate anything else. Any failure
for a symbol is skipped rather than raised, so the dashboard never crashes on it.
"""
from __future__ import annotations

from datetime import date, datetime

import yfinance as yf

from . import config


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
        if isinstance(d, datetime):
            d = d.date()
        if isinstance(d, date) and d >= today:
            upcoming.append(d)
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
