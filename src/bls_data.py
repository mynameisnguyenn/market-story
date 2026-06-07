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

from . import config, series_archive

BLS_V1 = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
BLS_V2 = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
BLS_TIMEOUT = 15
ARCHIVE_PATH = config.DATA_DIR / "history" / "labor.jsonl"   # committed full monthly history

# (series_id, display_name). Curated risk-analyst labor/inflation set.
BLS_SERIES = [
    ("CUUR0000SA0", "CPI-U, all items"),
    ("CUUR0000SA0L1E", "Core CPI (ex food & energy)"),
    ("CES0000000001", "Nonfarm payrolls (000s)"),
    ("LNS14000000", "Unemployment rate"),
    ("CES0500000003", "Avg hourly earnings"),
    ("LNS11300000", "Labor force participation"),
]

# Series that are themselves percentages: their "YoY" is a percentage-POINT change,
# not a percent-of-a-percent (unemployment 3.6->4.0 is +0.4 pp, not +11%).
RATE_SERIES = {"LNS14000000", "LNS11300000"}


def fetch_bls(series: list[tuple[str, str]] = BLS_SERIES) -> list[dict]:
    """Latest snapshot for each BLS series (one batched POST). Best-effort."""
    key = _load_key()
    payload = _request([sid for sid, _ in series], key)
    by_id = _parse(payload) if payload else {}
    return [_snapshot(sid, name, by_id.get(sid, [])) for sid, name in series]


def _request(series_ids: list[str], key: str | None, start_year: int | None = None,
             end_year: int | None = None, timeout: int = BLS_TIMEOUT):
    """Single batched POST to BLS (v2 with key, else keyless v1). None on failure.
    Defaults to the trailing ~3 years (snapshot path); pass a range to backfill."""
    endpoint = BLS_V2 if key else BLS_V1
    end_year = end_year or date.today().year
    start_year = start_year or (end_year - 2)
    body = {"seriesid": series_ids, "startyear": str(start_year), "endyear": str(end_year)}
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
        if latest is not None and year_ago is not None:
            if series_id in RATE_SERIES:                 # rate diff: a 0.0 year-ago is valid
                yoy = latest - year_ago
            elif year_ago != 0:                          # ratio: still guard division by zero
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


# --- committed history archive (data/history/labor.jsonl) -------------------

def _obs_rows(series_id: str, data: list) -> list[dict]:
    """BLS observations -> long-format archive rows [{date 'YYYY-MM', series, value}]."""
    out = []
    for d in data:
        period = str(d.get("period", ""))
        if not period.startswith("M") or period == "M13":      # drop annual-average rows
            continue
        v = _to_float(d.get("value"))
        if v is None:
            continue
        out.append({"date": f"{d.get('year', '?')}-{period[1:]}", "series": series_id, "value": v})
    return out


def backfill_bls_archive(series: list[tuple[str, str]] = BLS_SERIES, start_year: int = 1947) -> int:
    """One-time: pull each series' full monthly history into the archive, in 10-year chunks
    (the keyless BLS cap — a wider span is silently halved, leaving gaps). CPI and
    unemployment go back to the 1940s. ~8 requests, well under the 25/day keyless limit."""
    key = _load_key()
    rows: list[dict] = []
    end = date.today().year
    lo = start_year
    while lo <= end:
        hi = min(lo + 9, end)                                   # 10-year inclusive span (keyless cap)
        payload = _request([sid for sid, _ in series], key, start_year=lo, end_year=hi)
        by_id = _parse(payload) if payload else {}
        for sid, _name in series:
            rows.extend(_obs_rows(sid, by_id.get(sid, [])))
        lo = hi + 1
    return series_archive.merge(ARCHIVE_PATH, rows)


def update_bls_archive(series: list[tuple[str, str]] = BLS_SERIES) -> int:
    """Daily (Action): merge the trailing few years into the archive. Idempotent."""
    key = _load_key()
    payload = _request([sid for sid, _ in series], key)
    by_id = _parse(payload) if payload else {}
    rows = [r for sid, _name in series for r in _obs_rows(sid, by_id.get(sid, []))]
    return series_archive.merge(ARCHIVE_PATH, rows) if rows else len(series_archive.load(ARCHIVE_PATH))


def load_bls_history(series_id: str | None = None) -> list[dict]:
    """Archived monthly history — all rows, or just one series_id (oldest-first)."""
    if series_id is None:
        return series_archive.load(ARCHIVE_PATH)
    return series_archive.history_for(ARCHIVE_PATH, series_id)


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


if __name__ == "__main__":
    n = backfill_bls_archive()
    print(f"labor archive: {n} monthly observations in {ARCHIVE_PATH}")
