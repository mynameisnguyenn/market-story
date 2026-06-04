"""Append-only daily metrics timeline (data/timeline.jsonl), committed so it grows
honestly across both local runs and the daily Action — the durable record behind
long-horizon context and the running thesis track record.

One compact JSON object per day: the cross-asset anchors, positioning, the derived
'read of the day', and the vol premium. Append-only, idempotent by date, best-effort
(a storage failure never crashes the brief). Its payoff compounds as data accrues —
true multi-year percentiles and a real track record of the daily calls, no fabrication.
"""
from __future__ import annotations

import json
import os

from . import config, signals

TIMELINE_PATH = config.DATA_DIR / "timeline.jsonl"


def atomic_write(rows: list[dict]) -> None:
    """Write the whole timeline atomically (temp file + os.replace) so a torn write
    can never destroy the committed history."""
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(r) + "\n" for r in rows)
    tmp = TIMELINE_PATH.with_suffix(".jsonl.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, TIMELINE_PATH)


def _row_for(brief: dict) -> dict:
    def mkt(sym, field="last"):
        for rows in brief.get("markets", {}).values():
            for r in rows:
                if r.get("symbol") == sym:
                    return r.get(field)
        return None

    def macro(sid):
        for m in brief.get("macro", []):
            if m.get("id") == sid:
                return m.get("latest")
        return None

    pos = {p.get("name"): p.get("lev_net") for p in brief.get("positioning", [])}
    lead = signals.derive_lead(brief) or {}
    return {
        "date": brief.get("date"),
        "spx": mkt("^GSPC"), "spx_chg": mkt("^GSPC", "change_pct"),
        "vix": mkt("^VIX"), "ust10": macro("DGS10"), "curve_2s10s": macro("T10Y2Y"),
        "hy_oas": macro("BAMLH0A0HYM2"), "ig_oas": macro("BAMLC0A0CM"),
        "dxy": mkt("DX-Y.NYB"), "wti": mkt("CL=F"), "copper": mkt("HG=F"), "gold": mkt("GC=F"),
        "spx_spec_net": pos.get("S&P 500 (e-mini)"),
        "vol_premium": (brief.get("vol") or {}).get("premium"),
        "thesis": lead.get("thesis"),
    }


def load_timeline() -> list[dict]:
    """All timeline rows, oldest first. Tolerates a single corrupt line (never
    discards the whole committed history over one torn/merge-mangled line). [] if none."""
    rows = []
    try:
        with open(TIMELINE_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception:
                    continue   # skip the bad line, keep the rest of the record
    except Exception:
        return []
    return sorted(rows, key=lambda r: r.get("date", ""))   # oldest-first regardless of append order


def append_today(brief: dict) -> None:
    """Append today's row (idempotent by date). The common new-day case is a single-line
    append so a multi-thousand-row timeline isn't rewritten daily; a same-day re-run does
    an atomic full rewrite to replace the existing row. Best-effort."""
    try:
        row = _row_for(brief)
        if not row.get("date"):
            return
        existing = load_timeline()
        if any(r.get("date") == row["date"] for r in existing):
            kept = [r for r in existing if r.get("date") != row["date"]] + [row]
            kept.sort(key=lambda r: r.get("date", ""))
            atomic_write(kept)
        else:
            config.DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(TIMELINE_PATH, "a", encoding="utf-8") as f:   # new day -> 1-line append
                f.write(json.dumps(row) + "\n")
    except Exception:
        pass


def load_df():
    """Timeline as a DataFrame indexed by date (for trend charts). Empty if none."""
    import pandas as pd
    rows = load_timeline()
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"]).set_index("date").sort_index()
    return df


def lookback(weeks: int) -> dict | None:
    """The timeline row ~`weeks` ago (≈5 trading rows/week), for a 'where were we then'
    read. None until enough history has accrued."""
    rows = load_timeline()
    target = len(rows) - 1 - max(1, weeks) * 5
    return rows[target] if 0 <= target < len(rows) - 1 else None
