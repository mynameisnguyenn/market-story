"""Generic committed history archive for time-series data sources.

A small, dependency-free helper that stores the full history of a data source as a
long-format JSONL file under `data/history/` — one row per observation,
`{date, series, value, ...}`. Sources (BLS, FRED, …) keep their own archive path and
call load/write/merge here, so the dashboard can read deep history straight from disk
without a live key, and each series spans its whole record.

LF-only writes + atomic replace (temp + os.replace + fsync) so the Windows dev box and
the Linux daily Action never churn line endings or leave a half-written file. Mirrors
the self-contained pattern in `eia_data.py` (the first archive); kept generic for reuse.
"""
from __future__ import annotations

import json
import os


def load(path) -> list[dict]:
    """All rows from the archive, sorted by (series, date). Tolerant of a bad line; [] if absent."""
    rows = []
    try:
        with open(path, encoding="utf-8") as f:
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


def write(path, rows: list[dict]) -> None:
    """Atomically (re)write the archive as LF-only JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(r) + "\n" for r in rows)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def merge(path, fresh: list[dict]) -> int:
    """Merge fresh rows into the archive, idempotent by (series, date); fresh wins.
    Skips rows missing series/date/value. Returns the total row count after merge."""
    existing = {(r.get("series"), r.get("date")): r for r in load(path)}
    for r in fresh:
        if r.get("series") and r.get("date") and r.get("value") is not None:
            existing[(r["series"], r["date"])] = r
    rows = sorted(existing.values(), key=lambda r: (r["series"], r["date"]))
    write(path, rows)
    return len(rows)


def history_for(path, series_id: str) -> list[dict]:
    """Just the rows for one series_id, oldest-first."""
    return [r for r in load(path) if r.get("series") == series_id]
