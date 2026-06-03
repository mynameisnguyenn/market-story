"""Tests for the derived 'today's signal' read (pure logic, no network)."""
from src import signals


def _brief():
    return {
        "markets": {
            "us_equities": [{"symbol": "^VIX", "name": "VIX", "last": 22.0, "change_pct": 6.0}],
            "commodities": [{"symbol": "CL=F", "name": "WTI Crude", "last": 96.0, "change_pct": 3.1}],
        },
        "macro": [
            {"id": "T10Y2Y", "latest": -0.15},
            {"id": "BAMLH0A0HYM2", "latest": 2.72},
        ],
        "bls": [{"id": "CUUR0000SA0L1E", "yoy_pct": 2.75}],
        "movers": {"leaders": [{"name": "ASML", "change_pct": 4.72}],
                   "laggards": [{"name": "Salesforce", "change_pct": -4.18}]},
        "stats": {"sector_advancers": 7, "sector_decliners": 4},
    }


def test_signals_cover_key_dimensions():
    sigs = signals.derive_signals(_brief(), limit=10)   # all dimensions, uncapped
    blob = " | ".join(s["text"] for s in sigs)
    assert "VIX jumped +6.0%" in blob              # big VIX move flagged with direction
    assert "ASML" in blob and "Salesforce" in blob  # top mover + biggest drag
    assert "2s10s curve -0.15 — inverted" in blob    # curve state
    assert "HY credit spread 2.72% — tight" in blob  # credit calm
    assert "WTI crude +3.1%" in blob                 # oil move
    assert "Core CPI +2.8% YoY" in blob              # sticky inflation
    assert all(s["tone"] in ("up", "down", "warn", "neutral") for s in sigs)


def test_signals_empty_brief_is_safe():
    assert signals.derive_signals({}) == []


def test_signals_respects_limit():
    assert len(signals.derive_signals(_brief(), limit=3)) == 3
