"""The running thesis — market-story's standing, cross-session market view.

Distinct from the dated daily narratives (which are snapshots): this single committed file is
the THROUGH-LINE — the current standing thesis + flip condition, the regime, multi-session
watch items, how the view has evolved, and durable lessons. The `/narrate` loop reads it at
the start (continuity) and revises it after each session, so context compounds across sessions
(the "agent notes file" pattern). Pure I/O here — the synthesis/maintenance is Claude's job.
"""
from __future__ import annotations

from . import config

RUNNING_THESIS_PATH = config.DATA_DIR / "running_thesis.md"


def load_running_thesis() -> str | None:
    """The full running-thesis markdown, or None if absent/empty."""
    try:
        text = RUNNING_THESIS_PATH.read_text(encoding="utf-8").strip()
    except Exception:
        return None
    return text or None


def narrative_thesis(path) -> str | None:
    """The written read's one-line thesis: first content line under '## Today in one line'
    (or a 'thesis' header). None if not found — callers degrade to their derived lead."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None
    for i, ln in enumerate(lines):
        low = ln.strip().lower()
        if low.startswith("##") and ("one line" in low or "thesis" in low):
            for body in lines[i + 1:]:
                t = body.strip()
                if t and not t.startswith("#"):
                    return t.lstrip("*->•_ ").strip()
            break
    return None


def section(name: str) -> str | None:
    """The body of a '## <name>' section (case-insensitive), or None if not found/empty."""
    text = load_running_thesis()
    if not text:
        return None
    out, capturing = [], False
    for ln in text.splitlines():
        if ln.strip().startswith("## "):
            if capturing:                       # next header ends the section
                break
            capturing = ln.strip()[3:].strip().lower() == name.strip().lower()
            continue
        if capturing:
            out.append(ln)
    body = "\n".join(out).strip()
    return body or None


def current_thesis() -> str | None:
    """Just the 'Current thesis' section — the compact standing view."""
    return section("Current thesis")
