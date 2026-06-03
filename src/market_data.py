"""Fetch market data via yfinance and compute daily snapshots.

Yahoo quirks handled here (validated 2026-06): index symbols need a ^ prefix,
^TNX/^FVX/^TYX/^IRX are yields-in-percent, DX-Y.NYB is the only DXY that
resolves, futures (CL=F ...) are roll-spliced continuations, and 000001.SS
(Shanghai) often carries a trailing NaN bar that we drop.
"""

from __future__ import annotations

import io
import time

import pandas as pd
import requests
import yfinance as yf

from . import config

_DOWNLOAD_RETRIES = 3
_SINGLE_RETRIES = 1            # one attempt under throttle; the budget bounds the rest
_FALLBACK_BUDGET_S = 20        # cap total wall-clock on the per-symbol fallback

# Keyless Stooq EOD fallback for when Yahoo throttles. Indices need a hand map;
# plain US tickers map to "<ticker>.us". Futures/FX aren't reliably covered.
_STOOQ_INDEX = {"^GSPC": "^spx", "^IXIC": "^ndq", "^DJI": "^dji", "^RUT": "^rut", "^VIX": "^vix"}


def _stooq_symbol(sym: str):
    if sym in _STOOQ_INDEX:
        return _STOOQ_INDEX[sym]
    if sym.isalpha():                       # plain US ticker (NVDA, MSFT, XLK...)
        return sym.lower() + ".us"
    return None


def _download_stooq(sym: str):
    """Keyless Stooq EOD fallback; returns a Close DataFrame or None. Best-effort."""
    stooq = _stooq_symbol(sym)
    if not stooq:
        return None
    try:
        resp = requests.get(f"https://stooq.com/q/d/l/?s={stooq}&i=d", timeout=8)
        resp.raise_for_status()
        text = resp.text
        if not text or text[:1] == "<" or "Exceeded" in text:   # HTML page or hit-limit msg
            return None
        frame = pd.read_csv(io.StringIO(text))
        if "Close" not in frame.columns or "Date" not in frame.columns or frame.empty:
            return None
        frame.index = pd.to_datetime(frame["Date"], errors="coerce")
        frame = frame[frame.index.notna()].sort_index()   # drop unparseable dates; ensure order
        return frame[["Close"]].dropna()
    except Exception:
        return None


def download_history(symbols: list[str], period: str = config.HISTORY_PERIOD) -> dict[str, pd.DataFrame]:
    """Download daily history for many symbols; return {symbol: DataFrame}.

    Batches one yfinance call (with retry/backoff for transient 429s), then
    re-fetches any symbols missing from the batch individually so a single flaky
    ticker never blanks the dashboard.
    """
    if not symbols:
        return {}
    raw = _download_batch(symbols, period)
    out: dict[str, pd.DataFrame] = {}
    if raw is not None:
        for symbol in symbols:
            frame = _extract(raw, symbol, symbols)
            if frame is not None and not frame.empty:
                out[symbol] = frame
    # Per-symbol fallback, bounded by a wall-clock budget so a throttled feed
    # (e.g. Yahoo rate-limiting a cloud IP) degrades to partial data in seconds
    # instead of hanging for minutes grinding through every missing symbol.
    deadline = time.monotonic() + _FALLBACK_BUDGET_S
    for symbol in (s for s in symbols if s not in out):
        if time.monotonic() > deadline:
            break
        frame = _download_single(symbol, period)
        if frame is None or frame.empty:
            frame = _download_stooq(symbol)        # yfinance failed -> keyless Stooq
        if frame is not None and not frame.empty:
            out[symbol] = frame
    return out


def _download_batch(symbols: list[str], period: str):
    """Batched download with backoff; returns a DataFrame or None."""
    for attempt in range(_DOWNLOAD_RETRIES):
        try:
            # No multi_level_index kwarg: it isn't accepted across all yfinance
            # versions (prod pins >=1.2.0, dev has 0.2.x). _extract collapses a
            # single-symbol MultiIndex defensively instead — version-agnostic.
            raw = yf.download(symbols, period=period, interval="1d", group_by="ticker",
                              auto_adjust=True, progress=False, threads=True)
            if raw is not None and not raw.empty:
                return raw
        except Exception:
            pass
        if attempt < _DOWNLOAD_RETRIES - 1:    # no sleep after the last attempt
            time.sleep(1.0 * (attempt + 1))
    return None


def _download_single(symbol: str, period: str):
    """Per-symbol fallback fetch with backoff; returns a DataFrame or None."""
    for attempt in range(_SINGLE_RETRIES):
        try:
            frame = yf.Ticker(symbol).history(period=period, interval="1d", auto_adjust=True)
            if frame is not None and not frame.empty and "Close" in frame.columns:
                return frame.dropna(subset=["Close"])
        except Exception:
            pass
        if attempt < _SINGLE_RETRIES - 1:      # no sleep after the last attempt
            time.sleep(1.0 * (attempt + 1))
    return None


def _extract(raw: pd.DataFrame, symbol: str, symbols: list[str]) -> pd.DataFrame | None:
    """Pull one symbol's frame out of a yf.download result, dropping NaN closes."""
    try:
        frame = raw.copy() if len(symbols) == 1 else raw[symbol].copy()
    except (KeyError, AttributeError):
        return None
    if isinstance(frame.columns, pd.MultiIndex):
        # a single-symbol download can come back as a (ticker, field) column index
        frame.columns = frame.columns.get_level_values(-1)
    if "Close" not in frame.columns:
        return None
    return frame.dropna(subset=["Close"])


def _pct(current, base) -> float | None:
    """Percent change with guards against zero/NaN bases."""
    if base in (None, 0) or pd.isna(base) or current is None or pd.isna(current):
        return None
    return (current / base - 1.0) * 100.0


def compute_snapshot(symbol: str, name: str, frame: pd.DataFrame) -> dict:
    """One symbol's snapshot: last level plus 1D/1W/YTD change and level delta."""
    close = frame["Close"].dropna()
    close = close[close.index.notna()]             # guard against NaT bars (e.g. stooq)
    if close.empty:
        return _empty_snapshot(symbol, name)
    last = float(close.iloc[-1])
    prev = float(close.iloc[-2]) if len(close) >= 2 else None
    week_ago = float(close.iloc[-6]) if len(close) >= 6 else None

    year = close.index[-1].year
    prior_year = close[close.index.year < year]
    this_year = close[close.index.year == year]
    if not prior_year.empty:
        ytd_base = float(prior_year.iloc[-1])          # last close of prior year
    elif not this_year.empty:
        ytd_base = float(this_year.iloc[0])
    else:
        ytd_base = None

    return {
        "symbol": symbol,
        "name": name,
        "last": last,
        "change_pct": _pct(last, prev),
        "change_1w_pct": _pct(last, week_ago),
        "ytd_pct": _pct(last, ytd_base),
        "level_change": (last - prev) if prev is not None else None,
    }


def _empty_snapshot(symbol: str, name: str) -> dict:
    return {
        "symbol": symbol,
        "name": name,
        "last": None,
        "change_pct": None,
        "change_1w_pct": None,
        "ytd_pct": None,
        "level_change": None,
    }


def build_market_sections(history: dict[str, pd.DataFrame]) -> dict[str, list[dict]]:
    """Assemble per-group snapshot lists keyed by group name (see config.MARKET_GROUPS)."""
    sections: dict[str, list[dict]] = {}
    for key in config.MARKET_GROUPS:
        rows = []
        for symbol, name in config.group_items(key):
            frame = history.get(symbol)
            rows.append(_empty_snapshot(symbol, name) if frame is None
                        else compute_snapshot(symbol, name, frame))
        sections[key] = rows
    return sections
