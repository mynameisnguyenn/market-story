"""The synthesized 'read of the day' classifier (derive_lead) — synthetic briefs."""
from src import signals


def _brief(spx=None, hy_chg=None, hy_pct=None, y_chg=None, oil=None, copper=None, up=None, dn=None):
    mk = {"us_equities": [], "commodities": [], "rates": []}
    if spx is not None:
        mk["us_equities"].append({"symbol": "^GSPC", "name": "S&P", "change_pct": spx})
    if oil is not None:
        mk["commodities"].append({"symbol": "CL=F", "name": "WTI", "change_pct": oil})
    if copper is not None:
        mk["commodities"].append({"symbol": "HG=F", "name": "Copper", "change_pct": copper})
    if y_chg is not None:
        mk["rates"].append({"symbol": "^TNX", "name": "10Y", "level_change": y_chg})
    macro = []
    if hy_chg is not None or hy_pct is not None:
        macro.append({"id": "BAMLH0A0HYM2", "name": "HY OAS", "latest": 2.71,
                      "change": hy_chg, "pct_1y": hy_pct})
    return {"markets": mk, "macro": macro,
            "stats": {"sector_advancers": up, "sector_decliners": dn}}


def test_lead_unwind_not_stress():
    lead = signals.derive_lead(_brief(spx=-0.74, hy_chg=-0.01, hy_pct=3, y_chg=0.04))
    assert lead and lead["thesis"] == "unwind-not-stress"
    assert "duration-led" in lead["text"]


def test_lead_de_risking_when_credit_confirms():
    lead = signals.derive_lead(_brief(spx=-1.0, hy_chg=0.08))
    assert lead and lead["thesis"] == "de-risking"


def test_lead_geopolitical_premium_oil_up_copper_down():
    lead = signals.derive_lead(_brief(spx=-0.1, oil=2.6, copper=-2.5))
    assert lead and lead["thesis"] == "geopolitical-premium"


def test_lead_broad_risk_on():
    lead = signals.derive_lead(_brief(spx=0.8, up=9, dn=2))
    assert lead and lead["thesis"] == "risk-on"


def test_lead_default_on_quiet_day():
    """No dramatic theme -> a default 'resting regime' read, never None (the hero never blanks)."""
    lead = signals.derive_lead(_brief(spx=-0.2, hy_chg=0.0, oil=0.5, copper=0.2))
    assert lead is not None
    assert lead["tone"] == "neutral"
    assert lead["thesis"] in ("quiet", "resting-regime")
    assert lead["text"]


def test_lead_resting_regime_uses_analytics():
    """On a quiet day the default branch surfaces the brief's analytics (vol premium, extremes)."""
    brief = {"markets": {"us_equities": [{"symbol": "^GSPC", "name": "S&P", "change_pct": -0.2}]},
             "macro": [], "stats": {}, "vol": {"premium": 6.6}}
    lead = signals.derive_lead(brief)
    assert lead["thesis"] == "resting-regime" and "vol premium" in lead["text"]
