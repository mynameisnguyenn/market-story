"""Tests for display formatting helpers."""

import math

from src import formatting


def test_fmt_pct_signed():
    assert formatting.fmt_pct(0.42) == "+0.42%"
    assert formatting.fmt_pct(-1.5) == "-1.50%"


def test_fmt_pct_missing_returns_na():
    assert formatting.fmt_pct(None) == "n/a"
    assert formatting.fmt_pct(float("nan")) == "n/a"


def test_fmt_bps_converts_percentage_points():
    assert formatting.fmt_bps(0.05) == "+5 bps"     # 0.05pp = 5bps
    assert formatting.fmt_bps(-0.12) == "-12 bps"


def test_arrow_directions():
    assert formatting.arrow(1.0) == "▲"
    assert formatting.arrow(-1.0) == "▼"
    assert formatting.arrow(0) == "→"
    assert formatting.arrow(None) == "→"


def test_color_for_up_down_neutral():
    assert formatting.color_for(1.0) == formatting.GREEN
    assert formatting.color_for(-1.0) == formatting.RED
    assert formatting.color_for(0) == formatting.NEUTRAL
    assert formatting.color_for(None) == formatting.NEUTRAL


def test_is_missing():
    assert formatting.is_missing(None)
    assert formatting.is_missing(math.nan)
    assert not formatting.is_missing(0.0)
