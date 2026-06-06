"""Cross-asset statistical context from the embedded price history.

Extends the macro 1-year-percentile idea to the market instruments that get no FRED
stat-context: VIX, the 10Y, credit ETFs, the dollar, gold/oil/copper. `pct_z` here is the single
canonical percentile + z helper (macro_data._stat_context delegates to it) — percentile
of the latest level within a trailing window plus a z-score — run over the ~250 trading
days of closes already embedded in each brief.
Pure; degrades to [] / None rather than raising. Window is ~1y (label n).
"""
from __future__ import annotations

import math

# (symbol, label): risk anchors worth a "where is this vs its own range" read.
EXTREME_ANCHORS = [
    ("^VIX", "VIX"),
    ("^TNX", "10Y yield"),
    ("DX-Y.NYB", "Dollar (DXY)"),
    ("CL=F", "WTI crude"),
    ("HG=F", "Copper"),
    ("GC=F", "Gold"),
    ("HYG", "HY credit (HYG)"),
    ("TLT", "Long Treasuries (TLT)"),
]


def _clean(values) -> list:
    out = []
    for v in values:
        try:
            f = float(v)
        except (TypeError, ValueError):
            continue
        if not math.isnan(f):
            out.append(f)
    return out


def pct_z(values, window: int = 252, min_obs: int = 30):
    """Percentile (0-100) and z-score of the last value within a trailing window.

    The single source of truth for the "where does this level sit vs its own ~1y range"
    stat used across both the macro table (macro_data._stat_context) and the cross-asset
    extremes (compute_extremes). z uses the population std (ddof=0). Returns (None, None)
    when fewer than `min_obs` clean observations exist.
    """
    vals = _clean(values)
    if len(vals) < min_obs:
        return None, None
    tail = vals[-window:]
    latest = tail[-1]
    pct = round(sum(1 for v in tail if v < latest) / len(tail) * 100.0, 1)
    mean = sum(tail) / len(tail)
    std = math.sqrt(sum((v - mean) ** 2 for v in tail) / len(tail))
    z = round((latest - mean) / std, 2) if std > 0 else None
    return pct, z


def realized_vol(values, window: int = 20):
    """Annualized realized volatility (%) from the last `window` daily log returns."""
    vals = _clean(values)
    if len(vals) < window + 1:
        return None
    rets = [math.log(vals[i] / vals[i - 1]) for i in range(1, len(vals))
            if vals[i] > 0 and vals[i - 1] > 0]
    tail = rets[-window:]
    if len(tail) < window:
        return None
    mean = sum(tail) / len(tail)
    sd = math.sqrt(sum((r - mean) ** 2 for r in tail) / len(tail))
    return round(sd * math.sqrt(252) * 100.0, 1)


def compute_extremes(closes, window: int = 252) -> list[dict]:
    """{symbol,name,last,pct,z,n} for each anchor present in `closes`.

    `closes` is {symbol: pandas Series of closes} (e.g. from closes_from_brief).
    Only returns anchors with enough history; sorted by |z| (most stretched first).
    """
    out = []
    closes = closes or {}
    for sym, name in EXTREME_ANCHORS:
        series = closes.get(sym)
        if series is None:
            continue
        values = _clean(list(series))
        if len(values) < 30:
            continue
        pct, z = pct_z(values, window)
        if pct is None:
            continue
        out.append({"symbol": sym, "name": name, "last": values[-1],
                    "pct": pct, "z": z, "n": min(len(values), window)})
    out.sort(key=lambda r: abs(r["z"]) if r["z"] is not None else 0, reverse=True)
    return out


def stock_bond_corr(closes, window: int = 30) -> dict | None:
    """Rolling correlation of S&P vs long-Treasury daily returns — hedge efficacy.
    Negative = bonds cushion equities (the textbook hedge); positive = both fall
    together (the hedge is broken — a key risk-regime tell). Flags a recent sign flip."""
    closes = closes or {}
    spx, tlt = closes.get("^GSPC"), closes.get("TLT")
    if spx is None or tlt is None:
        return None
    import pandas as pd
    # Align by DATE: the inputs are Series carrying a DatetimeIndex, and upstream each
    # symbol is dropna'd independently (lengths/dates differ) — so an inner join on the
    # index is required. list()-ing them would align by row number and silently mismatch.
    rets = pd.concat([pd.Series(spx).pct_change(), pd.Series(tlt).pct_change()],
                     axis=1, join="inner").dropna()
    if len(rets) < window:
        return None
    cur = rets.iloc[-window:]
    corr = cur.iloc[:, 0].corr(cur.iloc[:, 1])
    if corr is None or (isinstance(corr, float) and math.isnan(corr)):
        return None
    corr = round(float(corr), 2)
    prior = None
    if len(rets) >= 2 * window:
        p = rets.iloc[-2 * window:-window]
        pv = p.iloc[:, 0].corr(p.iloc[:, 1])
        prior = round(float(pv), 2) if pv is not None and not math.isnan(pv) else None
    state = ("bonds hedging (normal)" if corr < -0.1
             else "stock-bond decoupled — hedge broken" if corr > 0.1 else "uncorrelated")
    flipped = prior is not None and (prior < 0) != (corr < 0)
    return {"corr": corr, "prior": prior, "state": state, "flipped": flipped, "window": window}


def compute_vol_premium(closes) -> dict | None:
    """VIX vs 20d realized vol of the S&P — the vol risk premium (implied minus
    realized). Positive & high = implied vol elevated vs realized, options/protection
    priced rich (the market is paying up for hedges), not complacency."""
    closes = closes or {}
    spx = closes.get("^GSPC")
    vix = closes.get("^VIX")
    if spx is None or vix is None:
        return None
    rv = realized_vol(list(spx), 20)
    vix_vals = _clean(list(vix))
    if rv is None or not vix_vals:
        return None
    vix_last = vix_vals[-1]
    return {"vix": round(vix_last, 1), "realized_20d": rv,
            "premium": round(vix_last - rv, 1)}
