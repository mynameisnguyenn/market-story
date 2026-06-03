"""Tests for the dashboard's pure figure/table builders (no Streamlit runtime)."""

import pandas as pd

import app


def _equity_rows():
    return [
        {"symbol": "XLK", "name": "Tech", "last": 198.2, "change_pct": 1.25,
         "change_1w_pct": 7.06, "ytd_pct": 37.85, "level_change": 2.4},
        {"symbol": "XLF", "name": "Financials", "last": None, "change_pct": None,
         "change_1w_pct": None, "ytd_pct": None, "level_change": None},
    ]


def _yield_rows():
    return [
        {"symbol": "^TNX", "name": "10Y Yield", "last": 4.45, "change_pct": -0.4,
         "change_1w_pct": -0.85, "ytd_pct": 7.0, "level_change": -0.02},
    ]


def test_section_records_yield_converts_to_bps():
    frame = app.section_records(_yield_rows(), "yield")
    assert frame.loc[0, "1D"] == -2.0          # -0.02 pp -> -2 bps


def test_section_records_equity_uses_change_pct():
    frame = app.section_records(_equity_rows(), "equity")
    assert frame.loc[0, "1D"] == 1.25
    assert pd.isna(frame.loc[1, "1D"])          # missing row stays NaN


def test_section_styler_renders_with_missing_values():
    html = app.section_styler(_equity_rows(), "equity").to_html()
    assert "Tech" in html and "n/a" in html     # NaN formatted as n/a, no crash


def test_section_styler_handles_empty_rows():
    html = app.section_styler([], "equity").to_html()  # empty group must not crash
    assert isinstance(html, str)


def test_macro_styler_handles_none_change():
    macro = [{"name": "10Y", "latest": 4.45, "change": 0.02, "date": "2026-06-01"},
             {"name": "CPI", "latest": None, "change": None, "date": None}]
    html = app.macro_styler(macro).to_html()
    assert "10Y" in html and "CPI" in html


def test_sector_treemap_fig_shows_change_value():
    fig = app.sector_treemap_fig(_equity_rows())
    assert fig is not None and len(fig.data) == 1
    trace = fig.data[0]
    # the +1.25% change must be displayed, not Plotly's mapped rgb() string
    assert any("+1.25%" in str(lbl) for lbl in trace.labels)
    assert "color" not in (trace.texttemplate or "")
    assert app.sector_treemap_fig([]) is None


def test_line_fig_builds_and_handles_empty():
    series = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(["2026-05-29", "2026-05-30", "2026-06-02"]))
    assert app.line_fig(series, "S&P 500") is not None
    assert app.line_fig(None, "S&P 500") is None
    assert app.line_fig(pd.Series([], dtype=float), "S&P 500") is None
