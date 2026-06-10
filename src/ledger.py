"""Prediction ledger — the accountability TRACK RECORD the scorecard lacked.

`scorecard.py` grades the immediately-prior narrative against the next brief and throws the
result away. This accumulates EVERY watch-block prediction into a committed append-only log
(`data/scorecard_log.jsonl`), grades each **at its horizon** (a window, not just the next
session) against committed data — macro from `data/history/macro.jsonl`, single names via
yfinance — and computes a **running hit-rate** so the running thesis carries a real record,
not just a standing view.

Grading semantics: a threshold like `>2.85` is "did the metric satisfy it at any point inside
the horizon window?" (a hit). If the window has no data yet, the item stays `pending`; if the
metric can't be resolved at all, `unresolved`. Best-effort; never raises.
"""
from __future__ import annotations

import json
import os
import re

from . import config, macro_data, scorecard

LEDGER_PATH = config.DATA_DIR / "scorecard_log.jsonl"
STANCE_START = "2026-06-10"   # stance blocks exist only from this date — earlier narratives exempt


def horizon_sessions(horizon: str) -> int:
    """Trading sessions a horizon implies (so we know when an item has matured)."""
    h = (horizon or "").lower()
    m = re.search(r"(\d+)\s*session", h)
    if m:
        return max(int(m.group(1)), 1)
    if "week" in h:
        return 5
    if "month" in h:
        return 21
    return 1                                   # today / next session / Friday close / open


# --- persistence -------------------------------------------------------------

def load() -> list[dict]:
    rows = []
    try:
        with open(LEDGER_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except Exception:
                        continue
    except Exception:
        return []
    return rows


def _write(records: list[dict]) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(r) + "\n" for r in records)
    tmp = LEDGER_PATH.with_suffix(".jsonl.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, LEDGER_PATH)


def _key(rec: dict) -> tuple:
    return (rec.get("logged"), rec.get("metric"), rec.get("trigger"), rec.get("claim"))


# --- value windows (committed macro archive + yfinance for market symbols) ---

def _macro_window(series_id: str, start: str, sessions: int) -> list[float]:
    rows = sorted((r["date"], r["value"]) for r in macro_data.load_fred_history()
                  if r.get("series") == series_id)
    return [v for d, v in rows if d > start][:sessions + 2]


def _fetch_market(symbol: str, start: str, sessions: int):
    """yfinance daily frame for `symbol` after `start` (module-level so tests can monkeypatch)."""
    try:
        import pandas as pd
        import yfinance as yf
        df = yf.download(symbol, start=start, progress=False, auto_adjust=False)
        if df is None or len(df) == 0:
            return None
        close = df["Close"]
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]
        return close.dropna()
    except Exception:
        return None


def _market_window(symbol: str, field: str, start: str, sessions: int) -> list[float] | None:
    close = _fetch_market(symbol, start, sessions)
    if close is None or len(close) == 0:
        return None
    if field in ("change_pct", "pct"):
        series = close.pct_change().dropna() * 100.0
    else:
        series = close
    vals = [float(v) for d, v in zip(series.index, series.values) if str(d.date()) > start]
    return vals[:sessions + 2]


def _window_for(metric: str, trigger: str, start: str, sessions: int):
    """Return the list of values over the horizon window, or None if unresolvable."""
    if not metric or ":" not in metric:
        return None
    kind, _, rest = metric.partition(":")
    if kind == "macro":
        return _macro_window(rest, start, sessions)
    if kind == "market":
        sym, _, field = rest.partition(":")
        return _market_window(sym, field or "last", start, sessions)
    return None


def _grade(rec: dict) -> dict:
    """Resolve a record's status from its horizon window. Mutates + returns rec."""
    sessions = rec.get("horizon_sessions") or horizon_sessions(rec.get("horizon", ""))
    vals = _window_for(rec.get("metric", ""), rec.get("trigger", ""), rec.get("logged", ""), sessions)
    if vals is None:
        rec["status"] = "unresolved"
        return rec
    if not vals:
        rec["status"] = "pending"                       # horizon not elapsed yet
        return rec
    trig = rec.get("trigger", "")
    metric = rec.get("metric", "")
    # Level metrics (yields, prices) grade at the END of the horizon — a transient touch that
    # reverses is not a hit. Event metrics (a single-day % change / gap) grade any-point-in-window.
    if metric.endswith((":change_pct", ":pct")):
        for v in vals:
            if scorecard._evaluate(v, trig):
                rec["status"], rec["graded_value"] = "triggered", round(float(v), 4)
                return rec
        rec["status"], rec["graded_value"] = "missed", round(float(vals[-1]), 4)
        return rec
    last = vals[-1]
    rec["status"] = "triggered" if scorecard._evaluate(last, trig) else "missed"
    rec["graded_value"] = round(float(last), 4)
    return rec


# --- logging + grading the live loop ----------------------------------------

def log_predictions(narrative_date: str, items: list[dict], asof: dict | None = None) -> int:
    """Append a narrative's watch items as open predictions (idempotent by key)."""
    existing = {_key(r): r for r in load()}
    for it in items:
        rec = {
            "logged": narrative_date,
            "claim": it.get("claim", ""),
            "metric": it.get("metric"),
            "trigger": it.get("trigger"),
            "horizon": it.get("horizon", ""),
            "horizon_sessions": horizon_sessions(it.get("horizon", "")),
            "asof_value": scorecard.resolve_metric(asof, it.get("metric", "")) if asof else None,
            # 0-1 for Brier scoring; 0.0 is a VALID probability, so no falsy `or` chaining here
            "confidence": it.get("probability") if it.get("probability") is not None else it.get("confidence"),
            "status": "pending",
        }
        existing.setdefault(_key(rec), rec)              # don't clobber an already-graded item
    rows = sorted(existing.values(), key=lambda r: (r.get("logged", ""), str(r.get("metric"))))
    _write(rows)
    return len(rows)


def grade_pending() -> dict:
    """Grade every pending/unresolved record against its window; persist; return stats()."""
    rows = load()
    for r in rows:
        if r.get("kind") == "stance":
            continue                               # stances settle via settle_stances(), not _grade
        if r.get("status") in (None, "pending", "unresolved"):
            _grade(r)
    _write(rows)
    return stats()


def stats() -> dict:
    """Running track record: counts + hit-rate, overall and per metric family."""
    rows = [r for r in load() if r.get("kind") != "stance"]   # stance ledger has its own stats
    from collections import Counter
    c = Counter(r.get("status") for r in rows)
    graded = c["triggered"] + c["missed"]
    by_metric = {}
    for r in rows:
        fam = (r.get("metric") or "?").split(":")[0]
        d = by_metric.setdefault(fam, {"triggered": 0, "missed": 0})
        if r.get("status") in d:
            d[r["status"]] += 1
    return {
        "total": len(rows), "triggered": c["triggered"], "missed": c["missed"],
        "pending": c["pending"], "unresolved": c["unresolved"],
        "graded": graded, "hit_rate": (c["triggered"] / graded) if graded else None,
        "by_metric": by_metric,
    }


def backfill_from_narratives() -> dict:
    """Rebuild the ledger from every committed narrative's watch block, grading each. Seeds the
    track record from history (this is the persisted version of the backtest)."""
    prior = load()                                               # rebuild rewrites the file, so first
    stances = [r for r in prior if r.get("kind") == "stance"]    # capture what the markdown can't carry:
    asof = {_key(r): r.get("asof_value") for r in prior          # the stance ledger + each watch item's
            if r.get("kind") != "stance"}                        # at-log-time snapshot (None in the .md)
    records: dict[tuple, dict] = {}
    for path in sorted(config.NARRATIVES_DIR.glob("narrative_*.md")):
        m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
        if not m:
            continue
        ndate = m.group(1)
        for it in scorecard.parse_watch(path.read_text(encoding="utf-8")):
            rec = {
                "logged": ndate, "claim": it.get("claim", ""), "metric": it.get("metric"),
                "trigger": it.get("trigger"), "horizon": it.get("horizon", ""),
                "horizon_sessions": horizon_sessions(it.get("horizon", "")),
                "asof_value": None, "status": "pending",
                "confidence": it.get("probability") if it.get("probability") is not None else it.get("confidence"),
            }
            rec["asof_value"] = asof.get(_key(rec))              # preserve the original snapshot
            records[_key(rec)] = _grade(rec)
    rows = list(records.values()) + stances
    _write(sorted(rows, key=lambda r: (r.get("logged", ""), str(r.get("metric")))))
    return stats()


# --- the stance ledger: paper P&L of the daily directional call ----------------
# One record per narrative date (kind="stance"). Settlement is the NEXT session's S&P
# print from the committed timeline — keyless, no lookahead, no backfilled predictions.

def log_stances_from_narratives() -> int:
    """Log one stance record per narrative dated >= STANCE_START (idempotent by date).
    A narrative WITHOUT a stance block logs as 'omitted' — visible, so skipping uncertain
    days can't quietly flatter the record (the selection-bias guard the grill demanded)."""
    rows = load()
    have = {r.get("logged") for r in rows if r.get("kind") == "stance"}
    added = 0
    for path in sorted(config.NARRATIVES_DIR.glob("narrative_*.md")):
        m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
        if not m or m.group(1) < STANCE_START or m.group(1) in have:
            continue
        st = scorecard.parse_stance(path.read_text(encoding="utf-8"))
        rec = {"kind": "stance", "logged": m.group(1), "status": "pending"}
        if st is None:
            rec.update({"direction": None, "status": "omitted"})
        else:
            rec.update({"direction": st["direction"], "notes": st["notes"]})
        rows.append(rec)
        added += 1
    if added:
        rows.sort(key=lambda r: (r.get("logged", ""), str(r.get("metric"))))
        _write(rows)
    return added


def settle_stances() -> int:
    """Mark pending stances to market with the next session's S&P % change (committed
    timeline). A stance logged on D settles with the first row strictly after D."""
    from . import timeline, timeline_returns
    rows = load()
    df = timeline.load_df()
    settled = 0
    for r in rows:
        if r.get("kind") != "stance" or r.get("status") != "pending":
            continue
        chg = timeline_returns.next_session_chg(df, r.get("logged", ""))
        if chg is None:
            continue                               # next session hasn't printed yet
        nxt = timeline_returns.rows_after(df, r.get("logged", ""), 1)   # record WHICH row settled it
        r["settlement_date"] = nxt.index[0].strftime("%Y-%m-%d") if len(nxt) else None
        r["spx_chg_next"] = round(chg, 4)
        # flat (direction 0) has no P&L: None, not 0.0 — so the ledger can't confuse a no-view
        # day with a directional call that happened to break even.
        r["pnl_pct"] = round(r["direction"] * chg, 4) if r.get("direction") not in (0, None) else None
        r["status"] = "settled"
        settled += 1
    if settled:
        _write(rows)
    return settled


def stance_stats(rows: list[dict] | None = None) -> dict:
    """The brain's directional record: win rate on non-flat settled calls + honesty counts
    (flat and omitted days stay visible — they are part of the record, not noise).
    Pass already-loaded rows to avoid a second disk read (the dashboard does)."""
    rows = [r for r in (rows if rows is not None else load()) if r.get("kind") == "stance"]
    settled = [r for r in rows if r.get("status") == "settled"]
    direc = [r for r in settled if r.get("direction") in (-1, 1)]
    pnls = [r["pnl_pct"] for r in direc if r.get("pnl_pct") is not None]
    wins = sum(1 for p in pnls if p > 0)
    return {
        "n_logged": len(rows), "n_settled": len(settled), "n_directional": len(direc),
        "n_flat": sum(1 for r in settled if r.get("direction") == 0),
        "n_omitted": sum(1 for r in rows if r.get("status") == "omitted"),
        "wins": wins, "win_rate": (wins / len(pnls)) if pnls else None,
        "avg_pnl_bps": (sum(pnls) / len(pnls) * 100.0) if pnls else None,
    }


if __name__ == "__main__":
    s = backfill_from_narratives()
    print(f"ledger: {s['total']} predictions | {s['triggered']} hit / {s['missed']} miss / "
          f"{s['pending']} pending / {s['unresolved']} unresolved | hit-rate {s['hit_rate']}")
    log_stances_from_narratives()
    settle_stances()
    ss = stance_stats()
    wr = "n/a" if ss["win_rate"] is None else f"{ss['win_rate'] * 100:.0f}%"
    print(f"stance: {ss['n_logged']} logged | {ss['n_directional']} directional settled | "
          f"win-rate {wr} | {ss['n_flat']} flat | {ss['n_omitted']} omitted")
