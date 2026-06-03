"""Grade a prior narrative's machine-readable `watch` block against today's brief.

Each narrative emits a fenced ```watch block of {claim, metric, trigger, horizon}.
Next session this checks every numeric trigger against the current brief, so the read
becomes accountable — a quiet feedback loop to sharpen the call, not a spreadsheet.
Pure logic, no I/O; degrades to empty rather than raising.
"""
from __future__ import annotations

import json
import math
import re

# Allow an optional language tag/label on the fence line (```watch  or  ```watch json).
_WATCH_RE = re.compile(r"```watch[^\n]*\n(.+?)```", re.DOTALL)
_TRIGGER_RE = re.compile(r"^\s*(>=|<=|>|<|==)\s*(-?\d+(?:\.\d+)?)\s*$")


def parse_watch(text: str) -> list[dict]:
    """Extract watch items from a narrative's ```watch block. [] if none/invalid."""
    if not text:
        return []
    m = _WATCH_RE.search(text)
    if not m:
        return []
    try:
        items = json.loads(m.group(1).strip())
    except Exception:
        return []
    return [it for it in items if isinstance(it, dict)] if isinstance(items, list) else []


def resolve_metric(brief: dict, metric: str):
    """Current value of a metric ref: 'macro:<FRED_id>' or 'market:<symbol>:<field>'."""
    if not metric or ":" not in metric:
        return None
    kind, _, rest = metric.partition(":")
    if kind == "macro":
        for m in brief.get("macro", []):
            if m.get("id") == rest:
                return m.get("latest")
        return None
    if kind == "market":
        sym, _, field = rest.partition(":")
        field = field or "last"
        for rows in brief.get("markets", {}).values():
            for r in rows:
                if r.get("symbol") == sym:
                    return r.get(field)
    return None


def _evaluate(value, trigger: str):
    """True/False if the trigger holds for value; None if value/trigger unusable."""
    if value is None or not isinstance(trigger, str):
        return None
    m = _TRIGGER_RE.match(trigger)
    if not m:
        return None
    op, num = m.group(1), float(m.group(2))
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(v):                     # NaN/inf -> unresolved, not a false 'watching'
        return None
    return {">": v > num, "<": v < num, ">=": v >= num, "<=": v <= num, "==": v == num}[op]


def grade(items: list[dict], brief: dict) -> list[dict]:
    """Status per watch item: 'triggered' / 'watching' / 'unresolved'."""
    out = []
    for it in items:
        value = resolve_metric(brief, it.get("metric", ""))
        fired = _evaluate(value, it.get("trigger", ""))
        status = "unresolved" if fired is None else ("triggered" if fired else "watching")
        out.append({"claim": it.get("claim", ""), "metric": it.get("metric"),
                    "trigger": it.get("trigger"), "current": value, "status": status})
    return out


def summarize(graded: list[dict]) -> dict:
    resolved = [g for g in graded if g["status"] != "unresolved"]
    triggered = [g for g in graded if g["status"] == "triggered"]
    return {"total": len(graded), "resolved": len(resolved), "triggered": len(triggered)}


def score_prior(prev_narrative: str, brief: dict) -> dict:
    """Parse the prior narrative's watch block and grade it against today's brief."""
    graded = grade(parse_watch(prev_narrative), brief)
    return {"graded": graded, "summary": summarize(graded)}
