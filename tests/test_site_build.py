"""Static-site build smoke: the whole site renders from committed data with no tab erroring.

Offline (no network) — same posture as test_render_smoke. Reads the committed brief; if none
exists (a fresh clone before `python run.py`), the test skips rather than fails.
"""
import os

import pytest

os.environ.setdefault("STREAMLIT_LOGGER_LEVEL", "error")


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
