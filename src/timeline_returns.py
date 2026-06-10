"""Forward-window helpers over the committed timeline (data/timeline.jsonl).

Shared by the brain's paper-P&L settlement (next-session S&P change), the VIX-episode
analogues (where did fear go next), and the FOMC event study (post-event windows).
Pure functions over a timeline DataFrame (timeline.load_df()); no I/O. Every helper
returns None / empty rather than raising — callers degrade, never crash.
"""
from __future__ import annotations

import pandas as pd


def rows_after(df: pd.DataFrame, date, sessions: int) -> pd.DataFrame:
    """The first `sessions` timeline rows STRICTLY after `date` (empty if none/invalid)."""
    if df is None or len(df) == 0 or sessions <= 0:
        return pd.DataFrame()
    try:
        ts = pd.Timestamp(date)
    except Exception:
        return pd.DataFrame()
    return df[df.index > ts].iloc[:sessions]


def next_session_chg(df: pd.DataFrame, date, col: str = "spx_chg") -> float | None:
    """The next session's % change after `date` — the settlement print for a stance
    logged on `date`. None if that session hasn't happened or its value is missing."""
    rows = rows_after(df, date, 1)
    if len(rows) == 0 or col not in rows.columns:
        return None
    v = rows[col].iloc[0]
    return None if pd.isna(v) else float(v)


def level_after(df: pd.DataFrame, date, col: str, sessions: int) -> float | None:
    """`col`'s level exactly `sessions` rows after `date`. None until enough history."""
    rows = rows_after(df, date, sessions)
    if len(rows) < sessions or col not in rows.columns:
        return None
    v = rows[col].iloc[sessions - 1]
    return None if pd.isna(v) else float(v)


def compound_pct(df: pd.DataFrame, date, sessions: int, col: str = "spx_chg") -> float | None:
    """Compounded % return over the `sessions` rows after `date`. None unless EVERY
    session in the window is present and non-null — a partial window silently biases
    event averages, so callers skip the event instead."""
    rows = rows_after(df, date, sessions)
    if len(rows) < sessions or col not in rows.columns:
        return None
    vals = rows[col]
    if vals.isna().any():
        return None
    out = 1.0
    for v in vals:
        out *= 1.0 + float(v) / 100.0
    return (out - 1.0) * 100.0
