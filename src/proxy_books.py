"""Proxy-book stress engine — synthetic portfolio construction over the timeline.

Builds simple proxy portfolios (e.g. 100% S&P, 70/30 equity/bond) and replays
them through named crisis windows, reporting return and max-drawdown stats per book.
Pure; no network, no I/O.
"""
from __future__ import annotations

import pandas as pd

from src import crisis as _crisis
from src import riskmetrics as _rm

# illustrative approximation — bond price return ~= -duration x yield change
BOND_DURATION = 8.0

BOOKS: dict[str, dict[str, float]] = {
    "100% S&P 500": {"spx": 1.0},
    "70/30 S&P / 10Y proxy": {"spx": 0.70, "bond": 0.30},
}


# ---------------------------------------------------------------------------
# Leg builders
# ---------------------------------------------------------------------------


def bond_proxy_returns(df: pd.DataFrame) -> pd.Series:
    """Bond price proxy returns (%) from 10Y yield level column 'ust10'.

    A +0.10pp rise in yield -> -0.8% return.  NaN where ust10 is missing.
    """
    if df is None or "ust10" not in df.columns:
        return pd.Series(dtype=float)
    yield_chg = df["ust10"].diff()
    return -BOND_DURATION * yield_chg


# ---------------------------------------------------------------------------
# Portfolio return builder
# ---------------------------------------------------------------------------


def book_returns(df: pd.DataFrame, weights: dict[str, float]) -> pd.Series:
    """Weighted daily % return series for a proxy book.

    weights keys: 'spx' -> df['spx_chg'], 'bond' -> bond_proxy_returns(df).
    Rows where ANY needed leg is null are dropped.  Returns empty Series on
    empty input or when degraded.
    """
    if df is None or df.empty or not weights:
        return pd.Series(dtype=float)

    legs: dict[str, pd.Series] = {}
    if "spx" in weights:
        if "spx_chg" not in df.columns:
            return pd.Series(dtype=float)
        legs["spx"] = df["spx_chg"]
    if "bond" in weights:
        legs["bond"] = bond_proxy_returns(df)

    if not legs:
        return pd.Series(dtype=float)

    combined = pd.concat(legs, axis=1)
    combined = combined.dropna(how="any")
    if combined.empty:
        return pd.Series(dtype=float)

    result = pd.Series(0.0, index=combined.index)
    for leg, w in weights.items():
        if leg in combined.columns:
            result = result + w * combined[leg]
    return result


# ---------------------------------------------------------------------------
# Stress engine
# ---------------------------------------------------------------------------


def stress_books(df: pd.DataFrame) -> list[dict]:
    """Stress each book through all DEFAULT_WINDOWS from crisis.py.

    Returns a list of dicts, one per (book, window) pair, each containing:
        {book, window, start, end, n_days, return_pct, max_drawdown_pct}
    Any field that cannot be computed is None.  Degrades gracefully on empty
    or None input — returns list of dicts with None stats (never raises).
    """
    results: list[dict] = []

    if df is None or df.empty:
        for book_name in BOOKS:
            for start, end, window_name in _crisis.DEFAULT_WINDOWS:
                results.append({
                    "book": book_name,
                    "window": window_name,
                    "start": start,
                    "end": end,
                    "n_days": 0,
                    "return_pct": None,
                    "max_drawdown_pct": None,
                })
        return results

    for book_name, weights in BOOKS.items():
        rets = book_returns(df, weights)

        # crisis_replay expects fractional returns; book_returns gives % returns
        # convert % -> fractional for crisis_replay, then convert back
        if rets.empty:
            frac_rets = rets
        else:
            frac_rets = rets / 100.0

        replay_rows = _crisis.crisis_replay(frac_rets)

        for row in replay_rows:
            window_name = row["name"]
            start = row["start"]
            end = row["end"]
            n = row["n_days"]

            # Convert fractional total return -> pct
            raw_return = row["return"]
            return_pct = round(raw_return * 100.0, 4) if raw_return is not None else None

            # max_drawdown from riskmetrics needs a price/level series
            # build cumulative level from the window's % returns
            max_dd_pct = _window_max_drawdown_pct(frac_rets, start, end)

            results.append({
                "book": book_name,
                "window": window_name,
                "start": start,
                "end": end,
                "n_days": n,
                "return_pct": return_pct,
                "max_drawdown_pct": max_dd_pct,
            })

    return results


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------


def _window_max_drawdown_pct(
    frac_rets: pd.Series,
    start: str,
    end: str,
) -> float | None:
    """Max drawdown (%) for frac_rets sliced to [start, end].

    Builds a cumulative price level from (1+r).cumprod() then calls
    riskmetrics.max_drawdown.  Returns None when window is empty or too short.
    """
    if frac_rets is None or frac_rets.empty:
        return None
    try:
        window_rets = frac_rets.dropna().loc[start:end]
    except Exception:
        return None
    if len(window_rets) < 2:
        return None
    cum_level = (1.0 + window_rets).cumprod()
    mdd = _rm.max_drawdown(cum_level)
    if mdd is None:
        return None
    return round(mdd * 100.0, 4)
