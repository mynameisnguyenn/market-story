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

from . import config, signals

TIMELINE_PATH = config.DATA_DIR / "timeline.jsonl"


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
    """All timeline rows, oldest first. [] if none/unreadable."""
    try:
        with open(TIMELINE_PATH, encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
    except Exception:
        return []


def append_today(brief: dict) -> None:
    """Append (or replace) today's row, keyed by date. Idempotent, best-effort."""
    try:
        row = _row_for(brief)
        if not row.get("date"):
            return
        rows = [r for r in load_timeline() if r.get("date") != row["date"]]
        rows.append(row)
        rows.sort(key=lambda r: r.get("date", ""))
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(TIMELINE_PATH, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
    except Exception:
        pass


def lookback(weeks: int) -> dict | None:
    """The timeline row ~`weeks` ago (≈5 trading rows/week), for a 'where were we then'
    read. None until enough history has accrued."""
    rows = load_timeline()
    target = len(rows) - 1 - max(1, weeks) * 5
    return rows[target] if 0 <= target < len(rows) - 1 else None
