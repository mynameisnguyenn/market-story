"""Derive a simple risk-on/off regime read from the macro (FRED) series.

Pure logic, no I/O — each signal is labeled with a tone (on / off / neutral)
and the overall lean is just the balance of those tones.
"""
from __future__ import annotations


def _macro_value(macro: list[dict], series_id: str):
    for m in macro:
        if m.get("id") == series_id:
            return m.get("latest")
    return None


def assess(macro: list[dict], vix: float | None = None) -> list[dict]:
    """Return labeled risk signals: [{label, reading, tone}] (tone: on/off/neutral)."""
    signals: list[dict] = []

    curve = _macro_value(macro, "T10Y2Y")
    if curve is not None:
        if curve < 0:
            signals.append({"label": "2s10s curve", "reading": f"{curve:+.2f} · inverted", "tone": "off"})
        elif curve < 0.5:
            signals.append({"label": "2s10s curve", "reading": f"{curve:+.2f} · flat", "tone": "neutral"})
        else:
            signals.append({"label": "2s10s curve", "reading": f"{curve:+.2f} · positive", "tone": "on"})

    hy = _macro_value(macro, "BAMLH0A0HYM2")
    if hy is not None:
        if hy < 3.0:
            signals.append({"label": "HY credit spread", "reading": f"{hy:.2f}% · tight", "tone": "on"})
        elif hy < 5.0:
            signals.append({"label": "HY credit spread", "reading": f"{hy:.2f}% · normal", "tone": "neutral"})
        else:
            signals.append({"label": "HY credit spread", "reading": f"{hy:.2f}% · wide", "tone": "off"})

    vol = vix if vix is not None else _macro_value(macro, "VIXCLS")
    if vol is not None:
        if vol < 15:
            signals.append({"label": "VIX", "reading": f"{vol:.1f} · calm", "tone": "on"})
        elif vol < 25:
            signals.append({"label": "VIX", "reading": f"{vol:.1f} · normal", "tone": "neutral"})
        else:
            signals.append({"label": "VIX", "reading": f"{vol:.1f} · elevated", "tone": "off"})

    nfci = _macro_value(macro, "NFCI")
    if nfci is not None:
        if nfci < 0:
            signals.append({"label": "Financial conditions", "reading": f"{nfci:+.2f} · loose", "tone": "on"})
        else:
            signals.append({"label": "Financial conditions", "reading": f"{nfci:+.2f} · tight", "tone": "off"})

    return signals


def overall(signals: list[dict]) -> str:
    """One-line lean from the balance of on/off signals."""
    on = sum(1 for s in signals if s["tone"] == "on")
    off = sum(1 for s in signals if s["tone"] == "off")
    if on > off:
        return "Risk-on lean"
    if off > on:
        return "Risk-off lean"
    return "Mixed / neutral"
