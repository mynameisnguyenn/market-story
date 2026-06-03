"""Fetch key labor & inflation prints directly from the BLS Public Data API.

BLS is the primary source for CPI and the jobs report that FRED merely
redistributes — pulling direct gets the release on release-day plus the
sub-indices. Keyless by default (v1 endpoint); set BLS_API_KEY in .env for the
higher v2 limits. Best-effort: any failure yields empty snapshots, never raises.
"""
from __future__ import annotations

import os
from datetime import date

import requests

from . import config

BLS_V1 = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
BLS_V2 = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
BLS_TIMEOUT = 15

# (series_id, display_name). Curated risk-analyst labor/inflation set.
BLS_SERIES = [
    ("CUUR0000SA0", "CPI-U, all items"),
    ("CUUR0000SA0L1E", "Core CPI (ex food & energy)"),
    ("CES0000000001", "Nonfarm payrolls (000s)"),
    ("LNS14000000", "Unemployment rate"),
    ("CES0500000003", "Avg hourly earnings"),
    ("LNS11300000", "Labor force participation"),
]


def fetch_bls(series: list[tuple[str, str]] = BLS_SERIES) -> list[dict]:
    """Latest snapshot for each BLS series (one batched POST). Best-effort."""
    key = _load_key()
    payload = _request([sid for sid, _ in series], key)
    by_id = _parse(payload) if payload else {}
    return [_snapshot(sid, name, by_id.get(sid, [])) for sid, name in series]


def _request(series_ids: list[str], key: str | None, timeout: int = BLS_TIMEOUT):
    """Single batched POST to BLS (v2 with key, else keyless v1). None on failure."""
    endpoint = BLS_V2 if key else BLS_V1
    year = date.today().year
    body = {"seriesid": series_ids, "startyear": str(year - 2), "endyear": str(year)}
    if key:
        body["registrationkey"] = key
    try:
        resp = requests.post(endpoint, json=body, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return None
    if not isinstance(data, dict) or data.get("status") != "REQUEST_SUCCEEDED":
        return None
    return data


def _parse(payload: dict) -> dict:
    """{series_id: [observations]} from a BLS payload."""
    out = {}
    for series in payload.get("Results", {}).get("series", []):
        out[series.get("seriesID")] = series.get("data", [])
    return out


def _to_float(value):
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _snapshot(series_id: str, name: str, data: list) -> dict:
    """Latest monthly value with month-over-month change and year-over-year %."""
    obs = [d for d in data
           if str(d.get("period", "")).startswith("M") and d.get("period") != "M13"]
    if not obs:
        return {"id": series_id, "name": name, "latest": None, "date": None,
                "prev": None, "change": None, "yoy_pct": None}
    obs.sort(key=lambda d: (d.get("year", ""), d.get("period", "")), reverse=True)
    latest = _to_float(obs[0].get("value"))
    prev = _to_float(obs[1].get("value")) if len(obs) >= 2 else None
    yoy = None
    if len(obs) >= 13:
        year_ago = _to_float(obs[12].get("value"))
        if latest is not None and year_ago:
            yoy = (latest / year_ago - 1.0) * 100.0
    return {
        "id": series_id,
        "name": name,
        "latest": latest,
        "date": f"{obs[0].get('year', '?')}-{obs[0].get('period', 'M00')[1:]}",
        "prev": prev,
        "change": (latest - prev) if (latest is not None and prev is not None) else None,
        "yoy_pct": yoy,
    }


def _load_key() -> str | None:
    """BLS_API_KEY from the environment or the gitignored .env (optional)."""
    key = os.environ.get("BLS_API_KEY")
    if key:
        return key
    env_path = config.PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            name, sep, value = line.strip().partition("=")
            if sep and name.strip() == "BLS_API_KEY":
                return value.strip() or None
    return None
