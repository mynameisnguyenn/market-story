"""timeline_returns: forward-window helpers (settlement, event windows, VIX paths)."""
import pandas as pd
import pytest

from src import timeline_returns as tr


def _df():
    idx = pd.to_datetime(["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04", "2026-06-05"])
    return pd.DataFrame({"spx_chg": [0.5, -1.0, 2.0, None, 1.0],
                         "vix": [15.0, 18.0, 17.0, 16.0, 15.5]}, index=idx)


def test_next_session_chg_is_strictly_after():
    assert tr.next_session_chg(_df(), "2026-06-01") == -1.0


def test_next_session_chg_missing_print_is_none():
    assert tr.next_session_chg(_df(), "2026-06-03") is None   # next row's spx_chg is null


def test_next_session_chg_after_last_row_is_none():
    assert tr.next_session_chg(_df(), "2026-06-05") is None


def test_next_session_chg_weekend_date_settles_on_next_row():
    idx = pd.to_datetime(["2026-06-05", "2026-06-08"])        # Fri -> Mon
    df = pd.DataFrame({"spx_chg": [0.5, -0.7]}, index=idx)
    assert tr.next_session_chg(df, "2026-06-06") == -0.7      # Saturday stance settles Monday


def test_level_after_counts_sessions():
    assert tr.level_after(_df(), "2026-06-01", "vix", 2) == 17.0


def test_level_after_insufficient_history_is_none():
    assert tr.level_after(_df(), "2026-06-04", "vix", 5) is None


def test_compound_pct_compounds():
    assert tr.compound_pct(_df(), "2026-06-01", 2) == pytest.approx(0.98)   # -1% then +2%


def test_compound_pct_null_in_window_skips_event():
    assert tr.compound_pct(_df(), "2026-06-02", 3) is None    # window contains the null print


def test_degrades_on_garbage():
    assert tr.next_session_chg(pd.DataFrame(), "2026-06-01") is None
    assert tr.next_session_chg(None, "2026-06-01") is None
    assert tr.next_session_chg(_df(), "not-a-date") is None
    assert tr.level_after(_df(), "2026-06-01", "nope", 1) is None
    assert len(tr.rows_after(_df(), "2026-06-01", 0)) == 0
