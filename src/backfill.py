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
    spx = prices["spx"].astype(float)
    log_ret = (spx / spx.shift(1)).apply(lambda x: math.log(x) if x and x > 0 else float("nan"))
    realized = log_ret.rolling(20).std() * math.sqrt(252) * 100.0     # annualized %, per day
    chg_pct = spx.pct_change(fill_method=None) * 100.0
    # as-of fill: each trading day gets the most recent prior value (daily FRED, weekly CFTC)
    fred = (fred.sort_index().reindex(prices.index, method="ffill")
            if fred is not None and not fred.empty else pd.DataFrame(index=prices.index))
    spec = (spec_net.sort_index().reindex(prices.index, method="ffill")
            if spec_net is not None and len(spec_net) else pd.Series(index=prices.index, dtype=float))

    rows = []
    for day in prices.index:
        def num(series, key):
            v = series.get(key) if hasattr(series, "get") else None
            return None if v is None or (isinstance(v, float) and math.isnan(v)) else round(float(v), 4)
        vix = num(prices.loc[day], "vix")
        rv = realized.get(day)
        rv = None if rv is None or (isinstance(rv, float) and math.isnan(rv)) else round(float(rv), 1)
        prem = round(vix - rv, 1) if (vix is not None and rv is not None) else None
        spec_v = spec.get(day)
        rows.append({
            "date": day.date().isoformat(),
            "spx": num(prices.loc[day], "spx"),
            "spx_chg": None if math.isnan(chg_pct.get(day, float("nan"))) else round(float(chg_pct[day]), 4),
            "vix": vix,
            "ust10": num(fred.loc[day], "ust10") if day in fred.index else None,
            "curve_2s10s": num(fred.loc[day], "curve_2s10s") if day in fred.index else None,
            "hy_oas": num(fred.loc[day], "hy_oas") if day in fred.index else None,
            "ig_oas": num(fred.loc[day], "ig_oas") if day in fred.index else None,
            "dxy": num(prices.loc[day], "dxy"),
            "wti": num(prices.loc[day], "wti"),
            "copper": num(prices.loc[day], "copper"),
            "gold": num(prices.loc[day], "gold"),
            "spx_spec_net": None if spec_v is None or (isinstance(spec_v, float) and math.isnan(spec_v)) else round(float(spec_v), 0),
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


def backfill(years: int = 3) -> int:
    """Fetch real history, assemble rows, and MERGE into the timeline without
    overwriting any existing (real, in-the-moment) row. Returns rows added."""
    prices = _fetch_prices(f"{max(years, 1)}y" if years <= 5 else "5y")
    if prices.empty:
        return 0
    cutoff = prices.index.max() - pd.Timedelta(days=365 * years + 5)
    prices = prices[prices.index >= cutoff]
    rows = assemble_rows(prices, _fetch_fred(), _fetch_spec_net())
    existing = timeline.load_timeline()
    have = {r.get("date") for r in existing}
    added = [r for r in rows if r.get("date") not in have]
    merged = existing + added
    merged.sort(key=lambda r: r.get("date", ""))
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(timeline.TIMELINE_PATH, "w", encoding="utf-8") as f:
        for r in merged:
            f.write(json.dumps(r) + "\n")
    return len(added)


if __name__ == "__main__":
    n = backfill(years=3)
    print(f"backfilled {n} historical rows into {timeline.TIMELINE_PATH}")
    print(f"timeline now has {len(timeline.load_timeline())} rows")
