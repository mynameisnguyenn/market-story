"""Weekly energy inventories from the EIA Open Data API (v2), with a committed history archive.

The supply side behind the oil/natgas prices the dashboard charts: the EIA Weekly Petroleum
Status Report (crude / gasoline / distillate / SPR stocks) and the Weekly Natural Gas Storage
Report. The number traders trade is the *weekly change* — a crude **draw** is bullish, a **build**
bearish.

Storage model: the full weekly history (back to 1982 for petroleum) lives in a committed archive
`data/history/energy.jsonl`. The daily Action refreshes it (it has the key); the dashboard reads
the archive for the panel and the history chart — so the panel never blanks even without a live
key, and the data spans the whole history. The live API is the source for the archive only.

Free key: EIA_API_KEY in .env (register at eia.gov/opendata). Best-effort throughout — never raises.
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor

import requests

from . import config

EIA_BASE = "https://api.eia.gov/v2"
EIA_TIMEOUT = 25
EIA_UA = "market-story (https://github.com/mynameisnguyenn/market-story)"
ARCHIVE_PATH = config.DATA_DIR / "history" / "energy.jsonl"

# (route, series_id, display_name). Petroleum stocks (thousand barrels) + L48 natgas storage (Bcf).
EIA_SERIES = [
    ("petroleum/stoc/wstk", "WCESTUS1", "Crude oil (ex-SPR)"),
    ("petroleum/stoc/wstk", "WGTSTUS1", "Gasoline"),
    ("petroleum/stoc/wstk", "WDISTUS1", "Distillate"),
    ("petroleum/stoc/wstk", "WCSSTUS1", "Crude in SPR"),
    ("natural-gas/stor/wkly", "NW2_EPG0_SWO_R48_BCF", "Nat gas storage (L48)"),
]


def _to_float(value):
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


# --- the live API (used to build/refresh the archive) -----------------------

def _fetch_obs(route: str, series_id: str, key: str, length: int, direction: str) -> list:
    """Weekly observations for one series. [] on any failure."""
    params = [("api_key", key), ("frequency", "weekly"), ("data[0]", "value"),
              ("facets[series][]", series_id), ("sort[0][column]", "period"),
              ("sort[0][direction]", direction), ("length", str(length))]
    try:
        resp = requests.get(f"{EIA_BASE}/{route}/data/", params=params,
                            headers={"User-Agent": EIA_UA}, timeout=EIA_TIMEOUT)
        resp.raise_for_status()
        return resp.json().get("response", {}).get("data", []) or []
    except Exception:
        return []


# --- the committed archive (data/history/energy.jsonl) ----------------------

def _atomic_write(rows: list[dict]) -> None:
    ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(r) + "\n" for r in rows)
    tmp = ARCHIVE_PATH.with_suffix(".jsonl.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:   # force LF (no platform churn)
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, ARCHIVE_PATH)


def load_history() -> list[dict]:
    """All archived weekly observations [{date, series, value, units}], oldest-first. Tolerant."""
    rows = []
    try:
        with open(ARCHIVE_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return []
    return sorted(rows, key=lambda r: (r.get("series", ""), r.get("date", "")))


def _rebuild_archive(series, key, recent_only: bool) -> int:
    """Fetch obs per series and MERGE into the archive (idempotent by series+date). Best-effort."""
    if not key:
        return 0
    existing = {(r.get("series"), r.get("date")): r for r in load_history()}
    length, direction = (16, "desc") if recent_only else (5000, "asc")
    with ThreadPoolExecutor(max_workers=min(8, len(series) or 1)) as pool:
        futures = {pool.submit(_fetch_obs, route, sid, key, length, direction): sid
                   for route, sid, _name in series}
        for fut, sid in futures.items():
            try:
                obs = fut.result()
            except Exception:
                obs = []
            for o in obs:
                v, period = _to_float(o.get("value")), o.get("period")
                if v is None or not period:
                    continue
                existing[(sid, period)] = {"date": period, "series": sid,
                                           "value": v, "units": o.get("units")}
    rows = sorted(existing.values(), key=lambda r: (r["series"], r["date"]))
    try:
        _atomic_write(rows)
    except Exception:
        return 0
    return len(rows)


def backfill_archive(series=EIA_SERIES) -> int:
    """One-time: pull the full weekly history into the archive."""
    return _rebuild_archive(series, _load_key(), recent_only=False)


def update_archive(series=EIA_SERIES) -> int:
    """Daily (Action): merge the latest few weeks into the archive."""
    return _rebuild_archive(series, _load_key(), recent_only=True)


# --- what the dashboard reads -----------------------------------------------

def fetch_eia(series: list[tuple[str, str, str]] = EIA_SERIES) -> list[dict]:
    """Latest snapshot (+ week-over-week change) per series, FROM THE ARCHIVE (so it never
    blanks without a live key). Falls back to a live pull only if the archive is empty."""
    snaps = _snapshots_from_archive(series)
    if any(s["latest"] is not None for s in snaps):
        return snaps
    key = _load_key()                              # archive empty -> try live once
    if not key:
        return snaps
    update_archive(series)
    return _snapshots_from_archive(series)


def _snapshots_from_archive(series) -> list[dict]:
    by_series: dict[str, list] = {}
    for r in load_history():
        by_series.setdefault(r.get("series"), []).append(r)
    out = []
    for _route, sid, name in series:
        rows = by_series.get(sid, [])               # already oldest-first from load_history
        if not rows:
            out.append({"id": sid, "name": name, "latest": None, "date": None,
                        "prev": None, "change": None, "units": None})
            continue
        latest, prev = rows[-1]["value"], (rows[-2]["value"] if len(rows) >= 2 else None)
        out.append({"id": sid, "name": name, "latest": latest, "date": rows[-1]["date"],
                    "prev": prev, "change": (latest - prev) if prev is not None else None,
                    "units": rows[-1].get("units")})
    return out


def _load_key() -> str | None:
    """EIA_API_KEY from the environment or the gitignored .env."""
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


if __name__ == "__main__":
    n = backfill_archive()
    print(f"energy archive: {n} weekly observations in {ARCHIVE_PATH}")
