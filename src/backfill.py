"""Backfill the metrics timeline with REAL historical data (yfinance + FRED + CFTC).

Not fabricated — the actual daily prices, yields, spreads, and positioning that existed
each day. Gives `data/timeline.jsonl` multi-year depth so percentiles read against years
of history and trend charts have something to draw. Run occasionally:

    python -m src.backfill            # ~3 years, merged into data/timeline.jsonl

The assembly (`assemble_rows`) is pure and unit-tested; only the fetchers touch the network.
"""
from __future__ import annotations

import json
import math

import pandas as pd

from . import analytics, config, timeline

# price anchors (yfinance close) -> timeline field
_PRICE_FIELDS = {"^GSPC": "spx", "^VIX": "vix", "DX-Y.NYB": "dxy",
                 "CL=F": "wti", "HG=F": "copper", "GC=F": "gold"}
# FRED daily series -> timeline field
_FRED_FIELDS = {"DGS10": "ust10", "T10Y2Y": "curve_2s10s",
                "BAMLH0A0HYM2": "hy_oas", "BAMLC0A0CM": "ig_oas"}


def assemble_rows(prices: pd.DataFrame, fred: pd.DataFrame, spec_net: pd.Series) -> list[dict]:
    """Build timeline rows from aligned historical frames (pure; date-indexed inputs).

    prices: columns = timeline price fields (spx/vix/...); fred: columns = fred fields;
    spec_net: S&P leveraged-fund net (weekly, will be forward-filled to daily).
    """
    if prices is None or prices.empty or "spx" not in prices:
        return []
    prices = prices[prices["spx"].notna()]       # anchor to the S&P trading calendar
    if prices.empty:
        return []
    spx = prices["spx"].astype(float)
    log_ret = (spx / spx.shift(1)).apply(lambda x: math.log(x) if x and x > 0 else float("nan"))
    realized = log_ret.rolling(20).std(ddof=0) * math.sqrt(252) * 100.0   # population std (matches analytics)
    chg_pct = spx.pct_change(fill_method=None) * 100.0
    # as-of fill: each trading day gets the most recent prior value (daily FRED, weekly CFTC).
    # De-dup the SOURCE index first — a revised/re-filed report repeats a date, and reindex FROM a
    # duplicate-labeled index raises.
    if fred is not None and not fred.empty:
        fred = fred.sort_index()
        fred = fred[~fred.index.duplicated(keep="last")].reindex(prices.index, method="ffill")
    else:
        fred = pd.DataFrame(index=prices.index)
    if spec_net is not None and len(spec_net):
        spec_net = spec_net.sort_index()
        spec = spec_net[~spec_net.index.duplicated(keep="last")].reindex(prices.index, method="ffill")
    else:
        spec = pd.Series(index=prices.index, dtype=float)

    def fin(value, nd):
        """Round, but reject NaN/inf -> None (so the committed JSON stays finite/valid)."""
        try:
            fv = float(value)
        except (TypeError, ValueError):
            return None
        return round(fv, nd) if math.isfinite(fv) else None

    rows = []
    for day in prices.index:
        prow = prices.loc[day]
        frow = fred.loc[day] if day in fred.index else None
        vix = fin(prow.get("vix"), 4)
        rv = fin(realized.get(day), 1)
        prem = round(vix - rv, 1) if (vix is not None and rv is not None) else None
        rows.append({
            "date": day.date().isoformat(),
            "spx": fin(prow.get("spx"), 4),
            "spx_chg": fin(chg_pct.get(day), 4),
            "vix": vix,
            "ust10": fin(frow.get("ust10"), 4) if frow is not None else None,
            "curve_2s10s": fin(frow.get("curve_2s10s"), 4) if frow is not None else None,
            "hy_oas": fin(frow.get("hy_oas"), 4) if frow is not None else None,
            "ig_oas": fin(frow.get("ig_oas"), 4) if frow is not None else None,
            "dxy": fin(prow.get("dxy"), 4),
            "wti": fin(prow.get("wti"), 4),
            "copper": fin(prow.get("copper"), 4),
            "gold": fin(prow.get("gold"), 4),
            "spx_spec_net": fin(spec.get(day), 0),
            "vol_premium": prem,
            "thesis": None,          # historical rows carry no in-the-moment read (not hindsight-fabricated)
            "backfilled": True,
        })
    return rows


# --- fetchers (network) ------------------------------------------------------

def _fetch_prices(period: str = "5y") -> pd.DataFrame:
    import yfinance as yf
    cols = {}
    for sym, field in _PRICE_FIELDS.items():
        try:
            df = yf.download(sym, period=period, interval="1d", progress=False, auto_adjust=False)
            close = df["Close"]
            if hasattr(close, "columns"):
                close = close.iloc[:, 0]
            idx = pd.DatetimeIndex(close.index)
            if idx.tz is not None:
                idx = idx.tz_localize(None)
            cols[field] = pd.Series(close.values, index=idx.normalize())
        except Exception:
            continue
    return pd.DataFrame(cols).sort_index() if cols else pd.DataFrame()


def _fetch_fred(start: str = "2019-01-01") -> pd.DataFrame:
    from . import macro_data
    try:
        from fredapi import Fred
        fred = Fred(api_key=macro_data._load_env_key())
    except Exception:
        fred = None
    cols = {}
    for sid, field in _FRED_FIELDS.items():
        try:
            s = fred.get_series(sid, observation_start=start).dropna() if fred else macro_data._fetch_csv(sid)
            if s is not None and len(s):
                idx = pd.DatetimeIndex(s.index)
                cols[field] = pd.Series(s.values, index=idx.normalize())
        except Exception:
            continue
    return pd.DataFrame(cols).sort_index() if cols else pd.DataFrame()


def _fetch_spec_net(limit: int = 320) -> pd.Series:
    import urllib.parse
    import urllib.request
    url = ("https://publicreporting.cftc.gov/resource/gpe5-46if.json?"
           "$where=" + urllib.parse.quote("contract_market_name='E-MINI S&P 500'")
           + "&$select=" + urllib.parse.quote("report_date_as_yyyy_mm_dd,lev_money_positions_long,lev_money_positions_short")
           + "&$order=" + urllib.parse.quote("report_date_as_yyyy_mm_dd ASC")
           + f"&$limit={limit}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "market-story backfill"})
        rows = json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception:
        return pd.Series(dtype=float)
    dates, vals = [], []
    for r in rows:
        try:
            net = float(r["lev_money_positions_long"]) - float(r["lev_money_positions_short"])
            dates.append(pd.Timestamp(r["report_date_as_yyyy_mm_dd"]).normalize())
            vals.append(net)
        except Exception:
            continue
    return pd.Series(vals, index=pd.DatetimeIndex(dates)).sort_index()


def _merge_rows(fresh: list[dict], existing: list[dict]) -> list[dict]:
    """Fresh backfilled (derived) rows win by date — so a re-run REFRESHES stale derived data —
    EXCEPT a real, in-the-moment row (written live by the daily Action, no `backfilled` flag) is
    always preserved over a backfilled one for the same date. Oldest-first."""
    by_date = {r["date"]: r for r in fresh if r.get("date")}
    for r in existing:
        if not r.get("backfilled") and r.get("date"):
            by_date[r["date"]] = r                # a live row beats a derived one
    return sorted(by_date.values(), key=lambda r: r.get("date", ""))


def backfill(start: str = "1998-01-01") -> int:
    """Fetch all available real history back to `start`, assemble rows, and merge them in:
    refresh the derived (backfilled) rows, preserve the live daily rows. Each series goes back
    only as far as it genuinely exists (S&P/yields decades, spreads/positioning less). Atomic
    write — never leaves the committed history torn. Returns the row count after merge (0 if no change)."""
    try:
        start_ts = pd.Timestamp(start)
        if pd.isna(start_ts):
            return 0
    except Exception:
        return 0
    prices = _fetch_prices("max")
    if prices.empty:
        return 0
    prices = prices[prices.index >= start_ts]
    if prices.empty:
        return 0
    rows = assemble_rows(prices, _fetch_fred(start="1990-01-01"), _fetch_spec_net(limit=1300))
    if not rows:
        return 0
    existing = timeline.load_timeline()
    out = _merge_rows(rows, existing)
    if out == existing:
        return 0                                  # nothing changed -> don't rewrite the committed file
    try:
        timeline.atomic_write(out)                # temp file + os.replace
    except Exception:
        return 0                                  # leave the existing committed history untouched
    return len(out)


if __name__ == "__main__":
    import sys
    start = sys.argv[1] if len(sys.argv) > 1 else "1998-01-01"
    n = backfill(start=start)
    print(f"backfill from {start}: {'no change' if n == 0 else f'rebuilt -> {n} rows'} "
          f"in {timeline.TIMELINE_PATH}")
    print(f"timeline now has {len(timeline.load_timeline())} rows")
