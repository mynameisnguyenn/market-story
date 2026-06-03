"""Regression tests for the bugs found in the whole-codebase audit (no network)."""
import numpy as np
import pandas as pd

from src import bls_data, brief, calendar_data, edgar_data, market_data, signals


def test_embed_history_survives_duplicate_and_misaligned_dates():
    # symbol A has a duplicate calendar day (collapsed intraday); B has a date A lacks.
    a = pd.DataFrame({"Close": [1.0, 2.0, 3.0]},
                     index=pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-02"]))
    b = pd.DataFrame({"Close": [10.0, 11.0]},
                     index=pd.to_datetime(["2026-01-01", "2026-01-03"]))
    out = brief._embed_history({"A": a, "B": b})   # must NOT raise (would blank the brief)
    assert "d" in out and "series" in out
    assert set(out["series"]) == {"A", "B"}


def test_movers_keeps_single_mover_on_degraded_day():
    sections = {"us_equities": [{"symbol": "AAA", "name": "AAA Inc", "change_pct": 1.5}]}
    m = brief._movers(sections)
    assert [r["symbol"] for r in m["leaders"]] == ["AAA"]
    assert m["laggards"] == []


def test_edgar_form_matches_family_not_exact():
    forms = ("8-K", "10-Q", "10-K", "6-K", "S-1", "424B")
    assert edgar_data._form_matches("10-K/A", forms)      # amendment kept
    assert edgar_data._form_matches("424B5", forms)       # prospectus kept
    assert edgar_data._form_matches("8-K", forms)
    assert not edgar_data._form_matches("10-KSB", forms)  # not over-matched by prefix
    assert not edgar_data._form_matches("4", forms)       # insider form excluded


def test_compute_snapshot_drops_nat_index_rows():
    idx = pd.to_datetime(["2025-12-31", "2026-01-02", "garbage"], errors="coerce")
    frame = pd.DataFrame({"Close": [100.0, 110.0, 999.0]}, index=idx)
    snap = market_data.compute_snapshot("X", "X", frame)   # NaT row must not corrupt YTD
    assert snap["last"] == 110.0
    assert round(snap["ytd_pct"], 1) == 10.0               # 110 vs prior-year-end 100


def test_bls_rate_series_yoy_is_percentage_points():
    data = [{"year": "2026", "period": "M06", "value": "4.0"}]
    data += [{"year": "2026", "period": f"M{m:02d}", "value": "3.9"} for m in (5, 4, 3, 2, 1)]
    data += [{"year": "2025", "period": f"M{m:02d}", "value": "3.7"} for m in (12, 11, 10, 9, 8, 7)]
    data += [{"year": "2025", "period": "M06", "value": "3.6"}]      # one year before
    snap = bls_data._snapshot("LNS14000000", "Unemployment rate", data)
    assert round(snap["yoy_pct"], 2) == 0.4    # +0.4 pp, NOT (4.0/3.6-1)*100 = +11.1%


def test_signals_mover_tone_follows_sign():
    b = {"markets": {}, "macro": [], "bls": [], "stats": {},
         "movers": {"leaders": [{"name": "AAA", "change_pct": -0.3}],   # best is still red
                    "laggards": [{"name": "BBB", "change_pct": -2.0}]}}
    out = signals.derive_signals(b)
    top = next(s for s in out if s["text"].startswith("Top mover"))
    assert top["tone"] == "down"               # was hardcoded "up"


def test_calendar_accepts_string_and_np_datetime(monkeypatch):
    class _Tk:
        calendar = {"Earnings Date": ["2099-07-15", np.datetime64("2099-08-01")]}
    monkeypatch.setattr(calendar_data.yf, "Ticker", lambda s: _Tk())
    got = calendar_data._next_earnings_date("AAA")
    assert got is not None and got.isoformat() == "2099-07-15"   # earliest, parsed from a string
