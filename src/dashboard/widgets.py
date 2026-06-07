"""Thin Streamlit render wrappers over the pure builders in `charts.py`.

These are the small st.* helpers shared across more than one panel. Panel-specific
rendering lives in the individual `panels.*` modules.
"""
from __future__ import annotations

import streamlit as st

from src import formatting
from src.dashboard.charts import line_fig, section_styler, sector_treemap_fig

# One semantic palette for every up/down/warn/neutral cue (charts, dots, badges) — sourced
# from formatting so tables and signals share the exact same green/red. Mirrors styles.css.
_TONE_HEX = {"up": formatting.GREEN, "down": formatting.RED, "warn": "#F5A623", "neutral": formatting.NEUTRAL}


def _tone_span(text: str, tone: str) -> str:
    """Inline HTML span colored by the shared semantic token (replaces Streamlit's :green[]/:red[],
    which use a different theme green/red and broke palette consistency)."""
    return f"<span style=\"color:{_TONE_HEX.get(tone, 'inherit')}\">{text}</span>"


def kpi_metric(col, row: dict | None, kind: str = "equity") -> None:
    if row is None or row.get("last") is None:
        col.metric(row["name"] if row else "n/a", "n/a")
        return
    if kind == "yield":
        delta = formatting.fmt_bps(row.get("level_change")) if row.get("level_change") is not None else None
        col.metric(row["name"], f"{row['last']:.2f}%", delta)
    else:
        change = row.get("change_pct")
        delta = formatting.fmt_pct(change) if change is not None else None
        color = "inverse" if row["symbol"] == "^VIX" else "normal"
        col.metric(row["name"], formatting.fmt_num(row["last"]), delta, delta_color=color)


def render_table(rows: list[dict], kind: str, caption: str) -> None:
    if not rows:
        st.caption("No data available.")
        return
    st.dataframe(section_styler(rows, kind), use_container_width=True, hide_index=True)
    st.caption(caption)


def render_treemap(rows: list[dict]) -> None:
    fig = sector_treemap_fig(rows)
    if fig is None:
        st.info("No sector data available.")
    else:
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def render_line(closes: dict, symbol: str, name: str, key: str | None = None) -> None:
    fig = line_fig(closes.get(symbol), name)
    if fig is None:
        st.info(f"No price history for {name}.")
    else:
        st.plotly_chart(fig, use_container_width=True, theme="streamlit", key=key)
