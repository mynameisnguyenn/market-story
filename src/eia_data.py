"""Fetch weekly energy inventories directly from the EIA Open Data API (v2).

The supply side behind the oil/natgas prices the dashboard already charts: the
EIA Weekly Petroleum Status Report (crude / gasoline / distillate ending stocks)
and the Weekly Natural Gas Storage Report. The number traders trade is the
*weekly change* — a crude **draw** (stocks fell) is typically bullish for oil, a
**build** bearish; natural gas swings between summer injections and winter
withdrawals.

Requires a free key (EIA_API_KEY in .env; register at eia.gov/opendata). Without
one the API 403s, so we degrade to an empty list and the energy panel simply
hides — never raises, never crashes the dashboard.
"""
from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor

import requests

from . import config

EIA_BASE = "https://api.eia.gov/v2"
EIA_TIMEOUT = 20
EIA_UA = "market-story (https://github.com/mynameisnguyenn/market-story)"

# (route, series_id, display_name). The EIA weekly headline set: petroleum
# ending stocks (thousand barrels) + Lower-48 natural gas working storage (Bcf).
EIA_SERIES = [
    ("petroleum/stoc/wstk", "WCESTUS1", "Crude oil (ex-SPR)"),
    ("petroleum/stoc/wstk", "WGTSTUS1", "Gasoline"),
    ("petroleum/stoc/wstk", "WDISTUS1", "Distillate"),
    ("petroleum/stoc/wstk", "WCSSTUS1", "Crude in SPR"),
    ("natural-gas/stor/wkly", "NW2_EPG0_SWO_R48_BCF", "Nat gas storage (L48)"),
]


def fetch_eia(series: list[tuple[str, str, str]] = EIA_SERIES) -> list[dict]:
    """Latest snapshot (+ week-over-week change) for each EIA series.

    Best-effort and concurrent; returns [] with no key so the panel hides.
    """
    key = _load_key()
    if not key:
        return []
    with ThreadPoolExecutor(max_workers=min(8, len(series) or 1)) as pool:
        futures = {
            pool.submit(_fetch_series, route, sid, key): (sid, name)
            for route, sid, name in series
        }
        rows_by_id = {}
        for future, (sid, name) in futures.items():
            try:
                rows_by_id[sid] = future.result()
            except Exception:
                rows_by_id[sid] = []
    return [_snapshot(sid, name, rows_by_id.get(sid, [])) for _route, sid, name in series]


def _fetch_series(route: str, series_id: str, key: str, timeout: int = EIA_TIMEOUT) -> list:
    """Latest weekly observations for one series (newest first). [] on any failure."""
    params = [
        ("api_key", key),
        ("frequency", "weekly"),
        ("data[0]", "value"),
        ("facets[series][]", series_id),
        ("sort[0][column]", "period"),
        ("sort[0][direction]", "desc"),
        ("length", "4"),
    ]
    try:
        resp = requests.get(f"{EIA_BASE}/{route}/data/", params=params,
                            headers={"User-Agent": EIA_UA}, timeout=timeout)
        resp.raise_for_status()
        payload = resp.json()
    except Exception:
        return []
    return payload.get("response", {}).get("data", []) or []


def _to_float(value):
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _snapshot(series_id: str, name: str, rows: list) -> dict:
    """Latest weekly stock level with the week-over-week change (the draw/build)."""
    rows = [r for r in rows if _to_float(r.get("value")) is not None]
    rows.sort(key=lambda r: str(r.get("period", "")), reverse=True)
    if not rows:
        return {"id": series_id, "name": name, "latest": None, "date": None,
                "prev": None, "change": None, "units": None}
    latest = _to_float(rows[0].get("value"))
    prev = _to_float(rows[1].get("value")) if len(rows) >= 2 else None
    return {
        "id": series_id,
        "name": name,
        "latest": latest,
        "date": rows[0].get("period"),
        "prev": prev,
        "change": (latest - prev) if (latest is not None and prev is not None) else None,
        "units": rows[0].get("units"),
    }


def _load_key() -> str | None:
    """EIA_API_KEY from the environment or the gitignored .env (required)."""
    key = os.environ.get("EIA_API_KEY")
    if key:
        return key
    env_path = config.PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            name, sep, value = line.strip().partition("=")
            if sep and name.strip() == "EIA_API_KEY":
                return value.strip() or None
    return None
