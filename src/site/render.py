"""HTML render helpers shared by every section builder.

Plotly figures -> embeddable <div> (plotly.js loaded once in the page head); pandas
Stylers -> styled <table>; markdown -> HTML; small KPI/caption/section primitives.
Pure string-building, no I/O — unit-testable with synthetic figures/frames.
"""
from __future__ import annotations

import html as _html
import uuid

import plotly.io as pio

# All non-sparkline charts share one Plotly config; sparklines render static. The figure JSON
# is embedded inert (script type=application/json) and Plotly.newPlot runs lazily when a tab is
# first shown (see app.js) — so hidden tabs cost nothing until visited.

from src import formatting

# Dark Plotly layout so figures sit on the warm-black page instead of a white card.
_DARK = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cdc6bd", family="IBM Plex Mono, monospace", size=11),
    xaxis=dict(gridcolor="#241f1a", zerolinecolor="#241f1a"),
    yaxis=dict(gridcolor="#241f1a", zerolinecolor="#241f1a"),
    legend=dict(font=dict(color="#cdc6bd")),
    colorway=["#7beafb", "#f5a623", "#36C26F", "#FF5C6C"],
)
_PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True, "scrollZoom": False}


def _themed(fig):
    """Apply the dark page theme without clobbering colours a builder set deliberately."""
    fig.update_layout(
        paper_bgcolor=_DARK["paper_bgcolor"], plot_bgcolor=_DARK["plot_bgcolor"],
        font=_DARK["font"], legend=_DARK["legend"], autosize=True,
    )
    fig.update_xaxes(gridcolor="#241f1a", zerolinecolor="#241f1a")
    fig.update_yaxes(gridcolor="#241f1a", zerolinecolor="#241f1a")
    return fig


def fig_html(fig, *, minimal: bool = False) -> str:
    """A Plotly figure as a lazy-rendered chart: an empty <div> plus its figure JSON in an
    inert <script type="application/json">. app.js calls Plotly.newPlot the first time the
    chart's tab is shown. Returns '' for a None figure so builder output passes straight through."""
    if fig is None:
        return ""
    _themed(fig)
    fid = f"fig-{uuid.uuid4().hex[:10]}"
    spec = pio.to_json(fig, validate=False).replace("</", "<\\/")   # safe inside a <script> tag
    static = "1" if minimal else "0"
    cls = "chart spark-chart" if minimal else "chart"
    return (f'<div class="{cls}" id="{fid}" data-static="{static}"></div>'
            f'<script type="application/json" class="cdata" data-for="{fid}">{spec}</script>')


def styler_html(styler) -> str:
    """A pandas Styler as a wrapped HTML table (hidden index, our table classes).
    Returns '' on None/empty so a degraded section just omits the table."""
    if styler is None:
        return ""
    try:
        styler = styler.hide(axis="index")
    except Exception:
        pass
    try:
        return f'<div class="tbl">{styler.to_html()}</div>'
    except Exception:
        return ""


def md_html(text: str) -> str:
    """Render a markdown string (narratives, running thesis) to HTML."""
    if not text:
        return ""
    import markdown
    return ('<div class="md">'
            + markdown.markdown(text, extensions=["fenced_code", "tables", "sane_lists"])
            + "</div>")


def esc(value) -> str:
    return _html.escape("" if value is None else str(value))


def fmt(value, spec: str = ",.2f", dash: str = "—") -> str:
    """Format a number with `spec`, or a dash when missing/non-numeric."""
    if value is None:
        return dash
    try:
        return format(float(value), spec)
    except (TypeError, ValueError):
        return esc(value)


def tone_of(value) -> str:
    """'up' / 'down' / 'flat' for a signed change — drives the CSS colour class."""
    if value is None or value == 0 or formatting.is_missing(value):
        return "flat"
    return "up" if value > 0 else "down"


def kpi_card(label: str, value: str, delta: str | None = None, tone: str = "flat",
             spark: str = "") -> str:
    """A header KPI tile: label, big mono value, signed delta, optional sparkline div."""
    d = f'<div class="kpi-delta {tone}">{esc(delta)}</div>' if delta is not None else ""
    return (f'<div class="kpi"><div class="kpi-label">{esc(label)}</div>'
            f'<div class="kpi-value">{esc(value)}</div>{d}{spark}</div>')


def panel(title: str, body: str, *, sub: str = "") -> str:
    """A titled block (h2 + optional caption + body). Empty body -> empty string."""
    if not body:
        return ""
    cap = f'<p class="cap">{esc(sub)}</p>' if sub else ""
    return f'<section class="panel"><h2>{esc(title)}</h2>{cap}{body}</section>'


def caption(text: str) -> str:
    return f'<p class="cap">{esc(text)}</p>' if text else ""


def grid(cards: list[str], cols: int = 0) -> str:
    """A responsive grid of pre-rendered cards/divs. cols=0 -> auto-fit."""
    cells = "".join(cards)
    cls = f"grid grid-{cols}" if cols else "grid grid-auto"
    return f'<div class="{cls}">{cells}</div>'


def hero(label: str, text: str, *, color: str = "var(--accent)", foot: str = "") -> str:
    """The big serif 'today's read / thesis' card with a coloured left border."""
    f = f'<div class="hero-foot">{esc(foot)}</div>' if foot else ""
    return (f'<div class="hero" style="border-left-color:{color}">'
            f'<div class="hero-tag" style="color:{color}">● {esc(label)}</div>'
            f'<div class="hero-text">{esc(text)}</div>{f}</div>')


def tone_class(tone: str) -> str:
    """Map a derived-signal tone label onto our up/down/flat CSS class."""
    return {"up": "up", "down": "down", "positive": "up", "negative": "down",
            "risk-on": "up", "risk-off": "down", "bull": "up", "bear": "down"}.get(tone, "flat")


def details(summary_text: str, body: str, *, open_: bool = False) -> str:
    """A collapsible <details> (the static stand-in for st.expander). '' if no body."""
    if not body:
        return ""
    o = " open" if open_ else ""
    return f'<details{o}><summary>{esc(summary_text)}</summary>{body}</details>'
