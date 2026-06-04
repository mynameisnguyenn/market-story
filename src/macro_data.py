"""Fetch macro series from FRED.

With FRED_API_KEY set, the keyed fredapi endpoint is the primary path: it allows
120 req/min and doesn't throttle under the concurrent burst that makes the keyless
fredgraph CSV CDN randomly drop series. Without a key, the keyless CSV is the only
path (and fredapi an unused dependency).
"""

from __future__ import annotations

import io
import os
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

from . import config, series_archive

ARCHIVE_PATH = config.DATA_DIR / "history" / "macro.jsonl"   # committed full FRED history


def fetch_macro(series: list[tuple[str, str]] = config.FRED_SERIES) -> list[dict]:
    """Return latest snapshot for each (series_id, name) in `series`."""
    key = _load_env_key()
    fred = _make_fred(key) if key else None

    def _fetch_one(item: tuple[str, str]) -> dict:
        series_id, name = item
        return _snapshot(series_id, name, _fetch_with_retry(fred, series_id))

    # Moderate concurrency: fast, but not a burst big enough to trip FRED's limit
    # (which was randomly dropping a couple of series each run).
    with ThreadPoolExecutor(max_workers=min(6, len(series) or 1)) as pool:
        return list(pool.map(_fetch_one, series))


def _fetch_with_retry(fred, series_id: str, attempts: int = 3) -> pd.Series | None:
    """Keyed API first (reliable under load), keyless CSV fallback; both retried
    on a transient empty/throttled response before giving up. An empty result
    (not just None) counts as a miss and triggers the retry."""
    observations = None
    for attempt in range(attempts):
        observations = _fetch_via_fredapi(fred, series_id) if fred is not None else None
        if observations is None or len(observations) == 0:
            observations = _fetch_csv(series_id)
        if observations is not None and len(observations) > 0:
            return observations
        if attempt + 1 < attempts:
            time.sleep(0.5 * (attempt + 1))
    return observations


# Series that trend (indices that mostly rise): a 1y percentile is ~always ~100
# and not a rich/cheap signal, so we skip statistical context for them.
_TREND_SERIES = {"CPIAUCSL", "PCEPILFE", "PAYEMS", "INDPRO"}


def _stat_context(observations: pd.Series, window: int = 252):
    """Percentile rank (0-100) and z-score of the latest value within a trailing
    window — turns a level into 'is this extreme vs its own recent history'."""
    if observations is None or len(observations) < 30:
        return None, None
    tail = observations.iloc[-window:].astype(float)
    latest = float(tail.iloc[-1])
    pct = round(float((tail < latest).mean()) * 100.0, 1)
    std = float(tail.std())
    z = round((latest - float(tail.mean())) / std, 2) if std > 0 else None
    return pct, z


def _snapshot(series_id: str, name: str, observations: pd.Series | None) -> dict:
    """Latest value, prior value, change, and statistical context for one series."""
    if observations is None or len(observations) == 0:
        return {"id": series_id, "name": name, "latest": None, "date": None,
                "prev": None, "change": None, "pct_1y": None, "z_1y": None}
    latest = float(observations.iloc[-1])
    prev = float(observations.iloc[-2]) if len(observations) >= 2 else None
    pct_1y, z_1y = (None, None) if series_id in _TREND_SERIES else _stat_context(observations)
    return {
        "id": series_id,
        "name": name,
        "latest": latest,
        "date": str(observations.index[-1].date()),
        "prev": prev,
        "change": (latest - prev) if prev is not None else None,
        "pct_1y": pct_1y,
        "z_1y": z_1y,
    }


def _fetch_csv(series_id: str, timeout: int = config.FRED_TIMEOUT) -> pd.Series | None:
    """Keyless fredgraph CSV pull. Missing values arrive as '.' and are dropped.

    NB: FRED's CDN resets/throttles browser User-Agents on this endpoint, so we
    deliberately send the default requests UA (no override).
    """
    url = config.FRED_CSV_URL.format(series_id=series_id)
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        frame = pd.read_csv(io.StringIO(resp.text))
    except Exception:
        return None
    if frame.shape[1] < 2:
        return None
    date_col, value_col = frame.columns[0], frame.columns[-1]
    values = pd.to_numeric(frame[value_col], errors="coerce")
    series = pd.Series(values.values, index=pd.to_datetime(frame[date_col], errors="coerce"))
    return series[series.index.notna()].dropna()   # drop unparseable-date (NaT) rows too


def _fetch_via_fredapi(fred, series_id: str) -> pd.Series | None:
    try:
        return fred.get_series(series_id).dropna()
    except Exception:
        return None


def _make_fred(key: str):
    try:
        from fredapi import Fred
        return Fred(api_key=key)
    except Exception:
        return None


# --- committed history archive (data/history/macro.jsonl) -------------------

def _series_rows(series_id: str, observations: pd.Series | None) -> list[dict]:
    """A FRED series -> long-format archive rows [{date 'YYYY-MM-DD', series, value}]."""
    if observations is None or len(observations) == 0:
        return []
    out = []
    for ts, value in observations.items():
        try:
            fv = float(value)
        except (TypeError, ValueError):
            continue
        if fv != fv:                                  # NaN
            continue
        out.append({"date": str(pd.Timestamp(ts).date()), "series": series_id, "value": fv})
    return out


def _rebuild_fred_archive(series: list[tuple[str, str]]) -> int:
    """Fetch each series' FULL history (the fetchers already return it) and merge into the
    archive. Idempotent by (series, date) — so daily and one-time runs converge. Best-effort."""
    key = _load_env_key()
    fred = _make_fred(key) if key else None

    def _rows(item: tuple[str, str]) -> list[dict]:
        series_id, _name = item
        return _series_rows(series_id, _fetch_with_retry(fred, series_id))

    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=min(6, len(series) or 1)) as pool:
        for chunk in pool.map(_rows, series):
            rows.extend(chunk)
    return series_archive.merge(ARCHIVE_PATH, rows)


def backfill_fred_archive(series: list[tuple[str, str]] = config.FRED_SERIES) -> int:
    """One-time: pull each FRED series' full history into the archive (yields to 1962,
    Fed Funds to 1954, CPI to 1947, credit spreads to 1996)."""
    return _rebuild_fred_archive(series)


def update_fred_archive(series: list[tuple[str, str]] = config.FRED_SERIES) -> int:
    """Daily (Action): refresh the archive. FRED returns the whole series, so this is a
    full-refresh merge (mid-file inserts keep the daily git diff small)."""
    return _rebuild_fred_archive(series)


def load_fred_history(series_id: str | None = None) -> list[dict]:
    """Archived FRED history — all rows, or just one series_id (oldest-first)."""
    if series_id is None:
        return series_archive.load(ARCHIVE_PATH)
    return series_archive.history_for(ARCHIVE_PATH, series_id)


def _load_env_key() -> str | None:
    """FRED_API_KEY from the environment, or a gitignored .env file."""
    key = os.environ.get("FRED_API_KEY")
    if key:
        return key
    env_path = config.PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            name, sep, value = line.strip().partition("=")
            if sep and name.strip() == "FRED_API_KEY":   # exact name, not a prefix match
                return value.strip() or None
    return None


if __name__ == "__main__":
    n = backfill_fred_archive()
    print(f"macro archive: {n} observations in {ARCHIVE_PATH}")
