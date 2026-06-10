"""VIX-episode analogue engine — finds historical VIX regimes closest to today's.

NO forward S&P return computation — the story is where VIX went, not where equities went.
Pure functions over a timeline DataFrame (timeline.load_df()). Degrades gracefully on
missing data; public functions never raise.
"""
from __future__ import annotations

import pandas as pd

from src.eras import era_for
from src.timeline_returns import level_after

# Sentinels
_EMPTY: list[dict] = []


def _safe_percentile_rank(series: pd.Series, value: float) -> float | None:
    """Percentile rank of `value` in `series` (0-100). None if series is empty."""
    valid = series.dropna()
    if len(valid) == 0:
        return None
    n = len(valid)
    rank = (valid < value).sum() + 0.5 * (valid == value).sum()
    return float(rank / n * 100)


def vix_episodes(
    df: pd.DataFrame,
    k: int = 10,
    min_gap: int = 21,
    exclude_recent: int = 63,
) -> list[dict]:
    """Top-k historical VIX analogues to today's VIX percentile level.

    Returns list of dicts with keys: date, era, vix, vix_pct, vix_5d, vix_21d, resolved.
    Returns [] when the input is degenerate or today's VIX is missing.
    """
    try:
        return _vix_episodes_inner(df, k, min_gap, exclude_recent)
    except Exception:
        return _EMPTY


def _build_candidates(df: pd.DataFrame, vix_col: pd.Series, today_pct: float,
                      exclude_recent: int) -> list[tuple]:
    """Sorted (dist, date, vix, pct) tuples for all non-null candidate rows.

    Vectorized: a per-row _safe_percentile_rank would be O(n^2) over ~7k sessions —
    the exact complexity trap the design grill flagged. searchsorted on the sorted
    full history reproduces the midpoint rank ((< count) + 0.5 * (== count)) exactly."""
    import numpy as np
    cutoff_pos = len(df) - exclude_recent
    if cutoff_pos <= 0:
        return []
    cand = pd.to_numeric(df["vix"].iloc[:cutoff_pos], errors="coerce").dropna()
    if cand.empty:
        return []
    full = np.sort(vix_col.values.astype(float))
    vals = cand.values.astype(float)
    lo = np.searchsorted(full, vals, side="left")
    hi = np.searchsorted(full, vals, side="right")
    pcts = (lo + 0.5 * (hi - lo)) / len(full) * 100.0
    candidates = [(abs(p - today_pct), d, float(v), float(p))
                  for d, v, p in zip(cand.index, vals, pcts)]
    candidates.sort(key=lambda t: t[0])
    return candidates


def _episode_dict(df: pd.DataFrame, date, vix_val: float, vix_pct_val: float) -> dict:
    """Build a single episode record from a selected (date, vix, pct) triple."""
    date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)[:10]
    vix_5d = level_after(df, date, "vix", 5)
    vix_21d = level_after(df, date, "vix", 21)
    resolved = bool(vix_21d < vix_val) if vix_21d is not None else None
    return {
        "date": date_str,
        "era": era_for(date_str),
        "vix": vix_val,
        "vix_pct": vix_pct_val,
        "vix_5d": vix_5d,
        "vix_21d": vix_21d,
        "resolved": resolved,
    }


def _vix_episodes_inner(
    df: pd.DataFrame,
    k: int,
    min_gap: int,
    exclude_recent: int,
) -> list[dict]:
    """Inner implementation; caller wraps with try/except."""
    if df is None or len(df) == 0 or "vix" not in df.columns:
        return _EMPTY
    vix_col = df["vix"].dropna()
    if len(vix_col) == 0:
        return _EMPTY
    today_vix = df["vix"].iloc[-1]
    if pd.isna(today_vix):
        return _EMPTY
    today_pct = _safe_percentile_rank(vix_col, float(today_vix))
    if today_pct is None:
        return _EMPTY

    candidates = _build_candidates(df, vix_col, today_pct, exclude_recent)
    if not candidates:
        return _EMPTY

    # Greedy dedup: select up to k episodes that are >= min_gap sessions apart.
    selected: list[dict] = []
    selected_positions: list[int] = []
    for _dist, date, vix_val, vix_pct_val in candidates:
        if len(selected) >= k:
            break
        try:
            pos = df.index.get_loc(date)
        except KeyError:
            continue
        if any(abs(pos - sp) < min_gap for sp in selected_positions):
            continue
        selected.append(_episode_dict(df, date, vix_val, vix_pct_val))
        selected_positions.append(pos)
    return selected


def today_vix_pct(df: pd.DataFrame) -> float | None:
    """Full-history percentile (0-100) of the latest VIX value, or None when unavailable.
    Lets the panel caption tell the truth about whether today is actually a high-fear regime."""
    try:
        if df is None or len(df) == 0 or "vix" not in df.columns:
            return None
        col = df["vix"].dropna()
        last = df["vix"].iloc[-1]
        if len(col) == 0 or pd.isna(last):
            return None
        return _safe_percentile_rank(col, float(last))
    except Exception:
        return None


def episodes_summary(episodes: list[dict]) -> dict:
    """One-line panel read: how often did fear resolve lower within 21 sessions.

    Returns {n, resolved_lower, unresolved}.
    resolved_lower: count where resolved == True.
    unresolved: count where resolved is None (vix_21d missing / window not yet elapsed).
    """
    if not episodes:
        return {"n": 0, "resolved_lower": 0, "unresolved": 0}
    n = len(episodes)
    resolved_lower = sum(1 for e in episodes if e.get("resolved") is True)
    unresolved = sum(1 for e in episodes if e.get("resolved") is None)
    return {"n": n, "resolved_lower": resolved_lower, "unresolved": unresolved}
