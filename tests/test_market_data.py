"""Tests for snapshot math (known-answer, synthetic data)."""

import pandas as pd
import pytest

from src import market_data


def _frame():
    dates = pd.to_datetime([
        "2025-12-31", "2026-01-02", "2026-01-05", "2026-01-06",
        "2026-01-07", "2026-01-08", "2026-01-09",
    ])
    return pd.DataFrame({"Close": [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 110.0]}, index=dates)


def test_compute_snapshot_known_answers():
    snap = market_data.compute_snapshot("^GSPC", "S&P 500", _frame())
    assert snap["last"] == 110.0
    assert snap["change_pct"] == pytest.approx((110 / 105 - 1) * 100)   # vs prev close
    assert snap["change_1w_pct"] == pytest.approx((110 / 101 - 1) * 100)  # vs iloc[-6]
    assert snap["ytd_pct"] == pytest.approx(10.0)                       # vs prior-year close 100
    assert snap["level_change"] == pytest.approx(5.0)


def test_compute_snapshot_empty_frame():
    snap = market_data.compute_snapshot("X", "X", pd.DataFrame({"Close": []}))
    assert snap["last"] is None
    assert snap["change_pct"] is None


def test_pct_guards_zero_and_nan():
    assert market_data._pct(100, 0) is None
    assert market_data._pct(100, None) is None
    assert market_data._pct(None, 100) is None
    assert market_data._pct(110, 100) == pytest.approx(10.0)


def test_build_sections_handles_missing_symbol():
    sections = market_data.build_market_sections({})  # nothing downloaded
    assert set(sections) == set(market_data.config.MARKET_GROUPS)
    assert all(row["last"] is None for row in sections["us_equities"])


def test_watchlist_group_wired_in():
    from src import config
    assert "watchlist" in config.MARKET_GROUPS
    assert "NVDA" in config.all_symbols()


def test_download_history_caps_fallback_under_throttle(monkeypatch):
    # Batch fully fails (throttle); fallback must stop at the budget, not grind all.
    monkeypatch.setattr(market_data, "_download_batch", lambda s, p: None)
    calls = []
    monkeypatch.setattr(market_data, "_download_single",
                        lambda sym, p: calls.append(sym) or None)
    clock = {"t": 0.0}

    def fake_monotonic():           # advance 10s per call -> trips the 20s budget fast
        clock["t"] += 10.0
        return clock["t"]
    monkeypatch.setattr(market_data.time, "monotonic", fake_monotonic)
    out = market_data.download_history(["A", "B", "C", "D", "E", "F", "G", "H"])
    assert out == {}                 # nothing came back (all throttled)
    assert len(calls) < 8            # stopped early — did NOT try every symbol


def test_extract_handles_single_symbol_multiindex():
    dates = pd.to_datetime(["2026-06-01", "2026-06-02"])
    cols = pd.MultiIndex.from_tuples([("^GSPC", "Open"), ("^GSPC", "Close")])
    raw = pd.DataFrame([[100.0, 101.0], [102.0, 103.0]], index=dates, columns=cols)
    frame = market_data._extract(raw, "^GSPC", ["^GSPC"])
    assert frame is not None and "Close" in frame.columns
    assert frame["Close"].iloc[-1] == 103.0
