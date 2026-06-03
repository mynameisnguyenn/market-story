"""Persist daily brief snapshots to SQLite so the dashboard can show
'what changed since your last session'. Local-only (data/history.db, gitignored).
Every helper is best-effort — a storage failure must never crash the dashboard.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import date

from . import config

DB_PATH = config.DATA_DIR / "history.db"


def _connect() -> sqlite3.Connection:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS snapshots (date TEXT PRIMARY KEY, payload TEXT NOT NULL)")
    return conn


def _snapshot_payload(brief: dict) -> dict:
    """Compact {symbol: last} map across all market groups, plus key stats."""
    levels = {}
    for rows in brief.get("markets", {}).values():
        for r in rows:
            if r.get("last") is not None:
                levels[r["symbol"]] = r["last"]
    return {"levels": levels, "stats": brief.get("stats", {})}


def save_today(brief: dict) -> None:
    """Upsert the snapshot keyed by the brief's date. Best-effort."""
    try:
        payload = json.dumps(_snapshot_payload(brief))
        with _connect() as conn:
            conn.execute(
                "INSERT INTO snapshots(date, payload) VALUES(?, ?) "
                "ON CONFLICT(date) DO UPDATE SET payload=excluded.payload",
                (brief.get("date", str(date.today())), payload),
            )
    except Exception:
        pass


def previous_snapshot(before: str) -> tuple[str, dict] | None:
    """Most recent snapshot strictly before `before` date, or None."""
    try:
        with _connect() as conn:
            row = conn.execute(
                "SELECT date, payload FROM snapshots WHERE date < ? ORDER BY date DESC LIMIT 1",
                (before,),
            ).fetchone()
        return (row[0], json.loads(row[1])) if row else None
    except Exception:
        return None


def deltas(brief: dict, symbols: list[str]) -> tuple[str, list[dict]] | None:
    """Level + % change per symbol vs the most recent prior snapshot.

    Returns (prior_date, rows) or None when there's no earlier snapshot yet.
    """
    prior = previous_snapshot(brief.get("date", str(date.today())))
    if prior is None:
        return None
    prior_date, prior_payload = prior
    prior_levels = prior_payload.get("levels", {})
    today_levels = _snapshot_payload(brief)["levels"]
    rows = []
    for sym in symbols:
        now, was = today_levels.get(sym), prior_levels.get(sym)
        if now is None or was is None:
            continue
        rows.append({
            "symbol": sym,
            "name": config.display_name(sym),
            "last": now,
            "change": now - was,
            "change_pct": (now / was - 1.0) * 100.0 if was else None,
        })
    return prior_date, rows
