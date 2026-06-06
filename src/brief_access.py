"""Tiny shared accessors for navigating a brief dict.

One definition of "find the row for this symbol / series id" so composite, signals,
and the dashboard don't each re-implement the same three lookups. Pure, leaf module
(imports nothing from the package) — safe to import from anywhere.
"""
from __future__ import annotations


def market_row(brief: dict, symbol: str) -> dict | None:
    """First market row (across every section) whose 'symbol' matches, or None."""
    for rows in (brief.get("markets") or {}).values():
        for row in rows:
            if row.get("symbol") == symbol:
                return row
    return None


def macro_row(brief: dict, series_id: str) -> dict | None:
    """First macro (FRED) row whose 'id' matches `series_id`, or None."""
    for row in brief.get("macro") or []:
        if row.get("id") == series_id:
            return row
    return None


def bls_row(brief: dict, series_id: str) -> dict | None:
    """First BLS row whose 'id' matches `series_id`, or None."""
    for row in brief.get("bls") or []:
        if row.get("id") == series_id:
            return row
    return None
