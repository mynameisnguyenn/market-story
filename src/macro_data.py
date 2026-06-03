"""Fetch macro series from FRED.

Primary path is the keyless fredgraph CSV endpoint (no API key, no dependency).
If FRED_API_KEY is set and a CSV pull fails, fall back to the fredapi library.
"""

from __future__ import annotations

import io
import os

import pandas as pd
import requests

from . import config


def fetch_macro(series: list[tuple[str, str]] = config.FRED_SERIES) -> list[dict]:
    """Return latest snapshot for each (series_id, name) in `series`."""
    key = _load_env_key()
    fred = _make_fred(key) if key else None
    rows = []
    for series_id, name in series:
        observations = _fetch_csv(series_id)
        if observations is None and fred is not None:
            observations = _fetch_via_fredapi(fred, series_id)
        rows.append(_snapshot(series_id, name, observations))
    return rows


def _snapshot(series_id: str, name: str, observations: pd.Series | None) -> dict:
    """Latest value, prior value, and change for one series."""
    if observations is None or len(observations) == 0:
        return {"id": series_id, "name": name, "latest": None, "date": None, "prev": None, "change": None}
    latest = float(observations.iloc[-1])
    prev = float(observations.iloc[-2]) if len(observations) >= 2 else None
    return {
        "id": series_id,
        "name": name,
        "latest": latest,
        "date": str(observations.index[-1].date()),
        "prev": prev,
        "change": (latest - prev) if prev is not None else None,
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
