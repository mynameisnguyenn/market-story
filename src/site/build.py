"""Build orchestrator: committed daily data -> self-contained static site/.

Loads the latest brief + price closes straight from disk (no network — the same path the
dashboard's instant first-paint uses), builds each tab's HTML via src.site.tabs.<id>, renders
the page template, and writes site/index.html plus the copied static assets. Run via build_site.py.
"""
from __future__ import annotations

import importlib
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src import brief as brief_mod
from src import config, timeline

from . import sections

# A few loaders are @st.cache_data-wrapped; called outside a Streamlit runtime they warn
# harmlessly ("No runtime found"). Silence that logger so the build output stays clean.
logging.getLogger("streamlit.runtime.caching.cache_data_api").setLevel(logging.ERROR)

_PKG = Path(__file__).resolve().parent
_TEMPLATES = _PKG / "templates"
_STATIC = _PKG / "static"

# (id, label) — render order. The builder is src.site.tabs.<id>.section(ctx).
_TABS = [
    ("overview", "Overview"),
    ("story", "Story"),
    ("equities", "Equities & Sectors"),
    ("macro", "Global & Macro"),
    ("trends", "Trends"),
    ("headlines", "Headlines"),
    ("calendar", "Calendar"),
]


@dataclass
class SiteContext:
    brief: dict
    closes: dict
    tl: Any   # timeline DataFrame, or None


def _load() -> SiteContext:
    """Context from committed data only. Raises if no brief exists."""
    brief = brief_mod.load_latest_brief()
    if not brief or not brief.get("markets"):
        raise SystemExit("No brief found — run `python run.py` first.")
    closes = brief_mod.closes_from_brief(brief)
    try:
        tl = timeline.load_df()
    except Exception:
        tl = None
    return SiteContext(brief=brief, closes=closes, tl=tl)


def _build_tabs(ctx: SiteContext) -> list[dict]:
    out = []
    for tid, label in _TABS:
        try:
            mod = importlib.import_module(f"src.site.tabs.{tid}")
            html = mod.section(ctx)
        except ModuleNotFoundError:
            html = f'<p class="cap">“{label}” coming in the next build.</p>'
        except Exception as exc:                       # one bad tab must not kill the build
            html = f'<p class="cap">“{label}” failed to render: {type(exc).__name__}: {exc}.</p>'
        out.append({"id": tid, "label": label,
                    "html": html or f'<p class="cap">Nothing to show in “{label}” today.</p>'})
    return out


def build(out_dir: Path | None = None) -> Path:
    """Render the whole site to `out_dir` (default <project>/site). Returns the path."""
    out_dir = Path(out_dir) if out_dir else (config.PROJECT_ROOT / "site")
    ctx = _load()

    env = Environment(loader=FileSystemLoader(str(_TEMPLATES)),
                      autoescape=select_autoescape(["html"]))
    tmpl = env.get_template("index.html.j2")
    gen = str(ctx.brief.get("generated_at_utc", ""))
    page = tmpl.render(
        title="Market Story",
        session_label=ctx.brief.get("session_label", ""),
        generated=gen[11:19] + " UTC" if len(gen) >= 19 else gen,
        date=ctx.brief.get("date", ""),
        header=sections.header_html(ctx),
        tabs=_build_tabs(ctx),
    )

    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for item in _STATIC.iterdir():
        if item.is_file():
            shutil.copy2(item, assets / item.name)
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    return out_dir
