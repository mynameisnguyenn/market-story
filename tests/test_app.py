"""Tests for the dashboard's pure figure/table builders (no Streamlit runtime)."""

import pandas as pd
import pytest

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


def test_filter_headlines():
    items = [
        {"title": "Fed holds rates", "source": "CNBC"},
        {"title": "Oil rallies", "source": "Reuters"},
        {"title": "NVDA earnings beat", "source": "Yahoo"},
    ]
    assert len(app.filter_headlines(items, "")) == 3                       # empty -> all
    assert [i["title"] for i in app.filter_headlines(items, "fed")] == ["Fed holds rates"]
    assert len(app.filter_headlines(items, "oil")) == 1
    assert app.filter_headlines(items, "cnbc") == [items[0]]               # matches source too
    assert app.filter_headlines(items, "zzz") == []


def test_yield_curve_fig_builds_and_needs_two_points():
    rates = [
        {"symbol": "^IRX", "name": "13W", "last": 4.20},
        {"symbol": "^TNX", "name": "10Y", "last": 4.45},
        {"symbol": "^TYX", "name": "30Y", "last": 4.70},
    ]
    fig = app.yield_curve_fig(rates)
    assert fig is not None and len(fig.data) == 1
    assert list(fig.data[0].x) == [0.25, 10.0, 30.0]          # sorted by maturity
    assert app.yield_curve_fig([{"symbol": "^TNX", "last": 4.45}]) is None  # one point
    assert app.yield_curve_fig([]) is None


def _corr_dates():
    return pd.to_datetime(["2026-05-20", "2026-05-21", "2026-05-22", "2026-05-26",
                           "2026-05-27", "2026-05-28", "2026-05-29", "2026-06-01"])


def test_compute_correlations_perfect_and_shape():
    idx = _corr_dates()
    a = pd.Series([100, 101, 103, 102, 104, 106, 105, 108], index=idx, dtype=float)
    closes = {"A": a, "B": a * 3.0}              # B is a scalar multiple -> identical returns
    corr = app.compute_correlations(closes, ["A", "B"], window=60)
    assert corr is not None and corr.shape == (2, 2)
    assert corr.loc["A", "A"] == pytest.approx(1.0)
    assert corr.loc["A", "B"] == pytest.approx(1.0)
    assert app.compute_correlations({"A": a}, ["A"], 60) is None   # need >= 2 series


def test_correlation_fig_builds_and_handles_thin():
    idx = _corr_dates()
    a = pd.Series([100, 101, 103, 102, 104, 106, 105, 108], index=idx, dtype=float)
    insts = [("A", "Alpha"), ("B", "Beta")]
    assert app.correlation_fig({"A": a, "B": a * 2.0}, insts) is not None
    assert app.correlation_fig({}, insts) is None                 # no data -> None


def test_sparkline_fig_builds_and_handles_short():
    s = pd.Series([100.0, 101.0, 99.0, 103.0],
                  index=pd.to_datetime(["2026-05-29", "2026-06-01", "2026-06-02", "2026-06-03"]))
    fig = app.sparkline_fig(s)
    assert fig is not None and len(fig.data) == 1
    assert app.sparkline_fig(pd.Series([1.0])) is None     # too short
    assert app.sparkline_fig(None) is None


def test_line_fig_builds_and_handles_empty():
    series = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(["2026-05-29", "2026-05-30", "2026-06-02"]))
    assert app.line_fig(series, "S&P 500") is not None
    assert app.line_fig(None, "S&P 500") is None
    assert app.line_fig(pd.Series([], dtype=float), "S&P 500") is None
