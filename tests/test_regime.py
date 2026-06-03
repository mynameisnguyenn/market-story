"""Tests for the risk-regime read (pure logic, no network)."""
from src import regime


def test_assess_labels_signals_and_overall():
    macro = [
        {"id": "T10Y2Y", "latest": -0.20},       # inverted -> off
        {"id": "BAMLH0A0HYM2", "latest": 2.5},   # tight -> on
        {"id": "VIXCLS", "latest": 12.0},        # calm -> on
        {"id": "NFCI", "latest": -0.5},          # loose -> on
    ]
    sigs = regime.assess(macro)
    tones = {s["label"]: s["tone"] for s in sigs}
    assert tones["2s10s curve"] == "off"
    assert tones["HY credit spread"] == "on"
    assert tones["VIX"] == "on"
    assert tones["Financial conditions"] == "on"
    assert regime.overall(sigs) == "Risk-on lean"


def test_assess_handles_missing_series():
    assert regime.assess([]) == []
    sigs = regime.assess([{"id": "VIXCLS", "latest": 30.0}])
    assert len(sigs) == 1 and sigs[0]["tone"] == "off"   # elevated VIX


def test_live_vix_overrides_series():
    sigs = regime.assess([{"id": "VIXCLS", "latest": 30.0}], vix=12.0)
    assert sigs[0]["tone"] == "on"                        # live VIX wins


def test_overall_mixed():
    assert regime.overall([{"tone": "on"}, {"tone": "off"}]) == "Mixed / neutral"
