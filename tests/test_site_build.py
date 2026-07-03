"""Static-site build smoke: the whole site renders with no tab erroring.

Offline (no network). The committed-brief tests skip on a fresh clone before `python run.py`;
the synthetic-context tests below NEVER skip, so a broken tab can't hide behind repo state.
"""
import pytest


def _has_brief() -> bool:
    from src import brief as brief_mod
    b = brief_mod.load_latest_brief()
    return bool(b and b.get("markets"))


@pytest.mark.skipif(not _has_brief(), reason="no committed brief — run `python run.py` first")
def test_site_builds_without_tab_errors(tmp_path):
    from src.site.build import build

    out = build(tmp_path)
    index = out / "index.html"
    assert index.exists(), "build did not write index.html"
    html = index.read_text(encoding="utf-8")

    # masthead + every tab section present
    assert "Global Markets Brief" in html
    for tab_id in ("overview", "story", "equities", "macro", "trends", "headlines", "calendar"):
        assert f'id="{tab_id}"' in html, f"missing tab section: {tab_id}"

    # no tab raised, and no tab is an unported placeholder
    assert "failed to render" not in html, "a tab raised during build"
    assert "coming in the next build" not in html, "a tab module is missing"

    # charts embedded as lazy figure JSON (rendered by app.js on tab show) + assets copied
    assert 'class="chart"' in html or "spark-chart" in html
    assert 'class="cdata"' in html, "figure JSON not embedded"
    assert (out / "assets" / "style.css").exists()
    assert (out / "assets" / "app.js").exists()


@pytest.mark.skipif(not _has_brief(), reason="no committed brief")
def test_every_tab_section_returns_html():
    """Each tab module's section(ctx) returns non-trivial HTML (degrades, never raises)."""
    import importlib

    from src import brief as brief_mod, timeline
    from src.site.build import SiteContext

    b = brief_mod.load_latest_brief()
    ctx = SiteContext(brief=b, closes=brief_mod.closes_from_brief(b), tl=timeline.load_df())
    for tab_id in ("overview", "story", "equities", "macro", "trends", "headlines", "calendar"):
        mod = importlib.import_module(f"src.site.tabs.{tab_id}")
        html = mod.section(ctx)
        assert isinstance(html, str), f"{tab_id}.section did not return a string"


# --- synthetic-context coverage (ports test_render_smoke's never-skips posture) --------------

def _synthetic_brief() -> dict:
    return {
        "date": "2026-06-06", "session_label": "US close", "generated_at_utc": "2026-06-06T21:00:00",
        "markets": {
            "us_equities": [{"symbol": "^GSPC", "name": "S&P 500", "last": 7500.0, "change_pct": 0.4,
                             "change_1w_pct": 1.2, "ytd_pct": 8.0, "level_change": None}],
            "rates": [{"symbol": "^TNX", "name": "10Y Yield", "last": 4.4, "change_pct": -0.3,
                       "change_1w_pct": -0.9, "ytd_pct": 6.0, "level_change": -0.015}],
            "sectors": [], "global_indices": [], "fx": [], "commodities": [], "credit": [],
        },
        "macro": [{"id": "DGS10", "name": "10Y Treasury", "latest": 4.4, "date": "2026-06-05",
                   "prev": 4.42, "change": -0.02, "pct_1y": 55.0, "z_1y": 0.2}],
        "bls": [], "energy": [], "positioning": [], "extremes": [],
        "vol": {"vix": 15.0, "realized_20d": 12.0, "premium": 3.0},
        "movers": {"leaders": [], "laggards": []},
        "news": [{"title": "Fed holds", "source": "T", "published": "", "link": "", "summary": ""}],
        "stats": {"vix": 15.0, "advancers": 1, "decliners": 0},
    }


def _synthetic_ctx(brief: dict):
    from src import brief as brief_mod
    from src.site.build import SiteContext
    return SiteContext(brief=brief, closes=brief_mod.closes_from_brief(brief), tl=None)


def test_every_tab_renders_from_synthetic_context():
    """No committed data needed — each tab degrades (never raises) on a minimal brief."""
    import importlib

    ctx = _synthetic_ctx(_synthetic_brief())
    for tab_id in ("overview", "story", "equities", "macro", "trends", "headlines", "calendar"):
        mod = importlib.import_module(f"src.site.tabs.{tab_id}")
        html = mod.section(ctx)
        assert isinstance(html, str), f"{tab_id}.section did not return a string"


def test_overview_degrades_on_partial_brief():
    """The nonce=0 fast-load can serve an old/partial brief — a missing 'movers' key (and a
    None-change mover) must degrade, not KeyError-crash the landing tab."""
    import importlib

    brief = _synthetic_brief()
    del brief["movers"]
    html = importlib.import_module("src.site.tabs.overview").section(_synthetic_ctx(brief))
    assert isinstance(html, str) and html

    brief = _synthetic_brief()
    brief["movers"] = {"leaders": [{"name": "X", "change_pct": None}], "laggards": []}
    html = importlib.import_module("src.site.tabs.overview").section(_synthetic_ctx(brief))
    assert isinstance(html, str) and html


def test_build_fails_loudly_on_missing_tab_module(monkeypatch):
    """A ModuleNotFoundError is a broken dependency, not a 'coming soon' tab — the build must
    raise so CI can never deploy a silently gutted site."""
    import importlib

    from src.site import build as build_mod

    real_import = importlib.import_module

    def _broken(name, *a, **k):
        if name == "src.site.tabs.overview":
            raise ModuleNotFoundError("No module named 'streamlit'")
        return real_import(name, *a, **k)

    monkeypatch.setattr(build_mod.importlib, "import_module", _broken)
    with pytest.raises(ModuleNotFoundError):
        build_mod._build_tabs(_synthetic_ctx(_synthetic_brief()))
