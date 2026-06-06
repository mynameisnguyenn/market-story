"""Tests for src/composite.py — composite risk-on/off danger signal.

All data is synthetic; no network calls. np.random.seed(42) for reproducibility.
"""
import numpy as np
import pytest

from src import composite


# ---------------------------------------------------------------------------
# Shared brief factories
# ---------------------------------------------------------------------------

def _base_brief(
    t10y2y: float = 0.8,
    hy_change: float = -0.01,
    hy_pct: float = 30.0,
    hy_latest: float = 3.5,
    adv: int = 8,
    dec: int = 3,
    vol_premium: float = 1.0,
    vix_level: float = 14.0,
    sb_corr: float = -0.3,
    sb_flipped: bool = False,
) -> dict:
    """Build a fully-populated, fully-risk-on brief with overrideable kwargs."""
    return {
        "macro": [
            {"id": "T10Y2Y", "latest": t10y2y, "change": 0.02, "pct_1y": 40.0},
            {"id": "BAMLH0A0HYM2", "latest": hy_latest, "change": hy_change, "pct_1y": hy_pct},
        ],
        "stats": {"vix": vix_level, "sector_advancers": adv, "sector_decliners": dec},
        "vol": {"vix": vix_level, "realized_20d": vix_level - vol_premium, "premium": vol_premium},
        "stock_bond": {"corr": sb_corr, "prior": -0.4, "flipped": sb_flipped, "window": 30},
    }


def _risk_off_brief() -> dict:
    """All six conditions firing -> danger=True."""
    return _base_brief(
        t10y2y=-0.25,       # curve inverted
        hy_change=0.10,     # HY OAS widening
        hy_pct=90.0,        # >85th %ile
        adv=2, dec=9,       # negative breadth
        vol_premium=5.0,    # >3
        vix_level=28.0,     # >=25
        sb_corr=0.4,        # positive & flipped
        sb_flipped=True,
    )


# ---------------------------------------------------------------------------
# Return-shape contract
# ---------------------------------------------------------------------------

def test_evaluate_returns_required_keys():
    result = composite.evaluate(_base_brief())
    assert set(result.keys()) == {"danger", "conditions", "score", "regime"}


def test_conditions_have_required_fields():
    result = composite.evaluate(_base_brief())
    for c in result["conditions"]:
        assert "name" in c
        assert "on" in c
        assert "detail" in c
        assert isinstance(c["on"], bool)


def test_score_equals_on_conditions():
    result = composite.evaluate(_base_brief())
    assert result["score"] == sum(1 for c in result["conditions"] if c["on"])


def test_regime_labels_are_valid():
    for brief in (_base_brief(), _risk_off_brief(), {}):
        regime = composite.evaluate(brief)["regime"]
        assert regime in ("risk-on", "neutral", "risk-off")


# ---------------------------------------------------------------------------
# Happy-path: all conditions firing
# ---------------------------------------------------------------------------

def test_all_conditions_fire_in_risk_off_brief():
    result = composite.evaluate(_risk_off_brief())
    assert result["danger"] is True
    assert result["score"] >= 3
    assert result["regime"] == "risk-off"
    assert all(c["on"] for c in result["conditions"])


def test_risk_on_brief_gives_score_zero():
    result = composite.evaluate(_base_brief())
    assert result["score"] == 0
    assert result["danger"] is False
    assert result["regime"] == "risk-on"


# ---------------------------------------------------------------------------
# Individual condition unit tests
# ---------------------------------------------------------------------------

def test_yield_curve_inverted():
    on, detail = composite._cond_yield_curve({"macro": [{"id": "T10Y2Y", "latest": -0.5}]})
    assert on is True
    assert "inverted" in detail


def test_yield_curve_positive():
    on, detail = composite._cond_yield_curve({"macro": [{"id": "T10Y2Y", "latest": 1.2}]})
    assert on is False


def test_yield_curve_missing():
    on, detail = composite._cond_yield_curve({})
    assert on is None
    assert "not available" in detail


def test_hy_widening_on_change():
    brief = {"macro": [{"id": "BAMLH0A0HYM2", "latest": 4.0, "change": 0.05, "pct_1y": 40.0}]}
    on, detail = composite._cond_hy_widening(brief)
    assert on is True
    assert "widening" in detail


def test_hy_widening_on_percentile():
    brief = {"macro": [{"id": "BAMLH0A0HYM2", "latest": 6.0, "change": -0.01, "pct_1y": 90.0}]}
    on, detail = composite._cond_hy_widening(brief)
    assert on is True


def test_hy_stable():
    brief = {"macro": [{"id": "BAMLH0A0HYM2", "latest": 3.0, "change": -0.02, "pct_1y": 30.0}]}
    on, detail = composite._cond_hy_widening(brief)
    assert on is False
    assert "stable" in detail


def test_hy_missing():
    on, _ = composite._cond_hy_widening({})
    assert on is None


def test_sector_breadth_negative():
    brief = {"stats": {"sector_advancers": 2, "sector_decliners": 9}}
    on, detail = composite._cond_sector_breadth(brief)
    assert on is True
    assert "negative" in detail


def test_sector_breadth_positive():
    brief = {"stats": {"sector_advancers": 9, "sector_decliners": 2}}
    on, detail = composite._cond_sector_breadth(brief)
    assert on is False
    assert "positive" in detail


def test_sector_breadth_missing():
    on, _ = composite._cond_sector_breadth({})
    assert on is None


def test_vol_premium_elevated():
    brief = {"vol": {"vix": 18.0, "realized_20d": 10.0, "premium": 8.0}}
    on, detail = composite._cond_vol_premium(brief)
    assert on is True
    assert "elevated" in detail


def test_vol_premium_normal():
    brief = {"vol": {"vix": 14.0, "realized_20d": 12.0, "premium": 2.0}}
    on, detail = composite._cond_vol_premium(brief)
    assert on is False
    assert "normal" in detail


def test_vol_premium_missing():
    on, _ = composite._cond_vol_premium({})
    assert on is None


def test_stock_bond_corr_flipped():
    brief = {"stock_bond": {"corr": 0.35, "prior": -0.2, "flipped": True, "window": 30}}
    on, detail = composite._cond_stock_bond_corr(brief)
    assert on is True
    assert "flipped" in detail


def test_stock_bond_corr_intact():
    brief = {"stock_bond": {"corr": -0.3, "prior": -0.4, "flipped": False, "window": 30}}
    on, detail = composite._cond_stock_bond_corr(brief)
    assert on is False
    assert "intact" in detail


def test_stock_bond_corr_missing():
    on, _ = composite._cond_stock_bond_corr({})
    assert on is None


def test_vix_elevated():
    brief = {"stats": {"vix": 30.0}, "vol": {"vix": 30.0}}
    on, detail = composite._cond_vix_level(brief)
    assert on is True
    assert "fear" in detail


def test_vix_calm():
    brief = {"stats": {"vix": 12.0}}
    on, detail = composite._cond_vix_level(brief)
    assert on is False
    assert "calm" in detail


def test_vix_missing():
    on, _ = composite._cond_vix_level({})
    assert on is None


# ---------------------------------------------------------------------------
# Edge / degenerate cases
# ---------------------------------------------------------------------------

def test_empty_brief_is_safe():
    result = composite.evaluate({})
    assert result["danger"] is False
    assert result["score"] == 0
    assert result["regime"] == "risk-on"
    assert isinstance(result["conditions"], list)
    assert len(result["conditions"]) == len(composite._CONDITIONS)


def test_none_brief_is_safe():
    result = composite.evaluate(None)
    assert result["score"] == 0


def test_partial_brief_skips_missing_conditions():
    """Partially populated brief: only curve data present."""
    brief = {"macro": [{"id": "T10Y2Y", "latest": -0.3}]}
    result = composite.evaluate(brief)
    # Only curve condition can fire; rest silently absent
    on_names = [c["name"] for c in result["conditions"] if c["on"]]
    assert any("curve" in n.lower() or "2s10s" in n.lower() for n in on_names)
    assert result["score"] == 1
    assert result["danger"] is False   # 1 < threshold of 3


def test_custom_threshold_lower():
    """With threshold=1, a single firing condition triggers danger."""
    brief = {"macro": [{"id": "T10Y2Y", "latest": -0.5}]}
    result = composite.evaluate(brief, threshold=1)
    assert result["danger"] is True
    assert result["regime"] == "risk-off"


def test_custom_threshold_higher():
    """With threshold=7 (impossible with 6 conditions), danger never fires."""
    result = composite.evaluate(_risk_off_brief(), threshold=7)
    assert result["danger"] is False


def test_nan_values_are_handled():
    """NaN in macro latest must not raise."""
    brief = {
        "macro": [{"id": "T10Y2Y", "latest": float("nan")}],
        "stats": {"vix": float("nan"), "sector_advancers": float("nan"), "sector_decliners": float("nan")},
        "vol": {"vix": float("nan"), "realized_20d": float("nan"), "premium": float("nan")},
        "stock_bond": {"corr": float("nan"), "flipped": None},
    }
    result = composite.evaluate(brief)
    assert isinstance(result["score"], int)


def test_score_3_yields_neutral_or_risk_off():
    """Exactly threshold=3 conditions -> danger True, regime risk-off."""
    np.random.seed(42)
    brief = _base_brief(
        t10y2y=-0.10,       # curve inverted -> on
        hy_change=0.05,     # HY widening -> on
        adv=3, dec=8,       # negative breadth -> on
        vol_premium=1.0,    # normal
        vix_level=18.0,     # normal
        sb_corr=-0.2, sb_flipped=False,
    )
    result = composite.evaluate(brief)
    assert result["score"] == 3
    assert result["danger"] is True
    assert result["regime"] == "risk-off"


def test_conditions_list_length_matches_registered():
    """evaluate always returns one entry per registered condition."""
    result = composite.evaluate({})
    assert len(result["conditions"]) == len(composite._CONDITIONS)
