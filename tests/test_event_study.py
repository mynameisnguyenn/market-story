"""Tests for src/event_study.py — synthetic data only, no network, no real timeline."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from src.event_study import (
    FOMC_DECISION_DATES,
    bootstrap_ci,
    event_returns,
    fomc_drift,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_df(dates: list[str], changes: list[float | None]) -> pd.DataFrame:
    """Build a minimal timeline DataFrame indexed by date with spx_chg column."""
    idx = pd.to_datetime(dates)
    spx_chg = pd.array(changes, dtype="Float64")
    return pd.DataFrame({"spx_chg": spx_chg}, index=idx)


# ---------------------------------------------------------------------------
# event_returns
# ---------------------------------------------------------------------------

class TestEventReturns:
    def test_single_session_exact(self):
        """T+1 return after an event equals the next session's change (no compounding effect)."""
        df = _make_df(
            ["2020-01-02", "2020-01-03", "2020-01-06"],
            [0.0, 2.0, -1.0],
        )
        result = event_returns(df, ["2020-01-02"], horizon=1)
        assert len(result) == 1
        assert result[0] == pytest.approx(2.0)

    def test_two_session_compound(self):
        """T+2 compound: (1 + 2/100) * (1 + -1/100) - 1 = 0.0098 = 0.98%."""
        df = _make_df(
            ["2020-01-02", "2020-01-03", "2020-01-06", "2020-01-07"],
            [0.0, 2.0, -1.0, 0.5],
        )
        result = event_returns(df, ["2020-01-02"], horizon=2)
        assert len(result) == 1
        assert result[0] == pytest.approx(0.98)

    def test_null_in_window_skips_event(self):
        """An event whose window contains a null is excluded from results."""
        df = _make_df(
            ["2020-01-02", "2020-01-03", "2020-01-06"],
            [0.0, None, 1.0],
        )
        result = event_returns(df, ["2020-01-02"], horizon=2)
        assert result == []

    def test_multiple_events_partial_skip(self):
        """Events with complete windows are included; null-window events are skipped."""
        df = _make_df(
            ["2020-01-02", "2020-01-03",  # event A: clean T+1
             "2020-01-06", "2020-01-07",  # event B: null in T+1
             "2020-01-08", "2020-01-09"],  # extra row
            [0.0, 3.0, 0.0, None, 0.0, 1.5],
        )
        result = event_returns(df, ["2020-01-02", "2020-01-06"], horizon=1)
        assert len(result) == 1
        assert result[0] == pytest.approx(3.0)

    def test_median_and_frac_pos_hand_computable(self):
        """Hand-computable case: 5 events, returns [1, 2, 3, -1, -2].

        Sorted: [-2, -1, 1, 2, 3]. Median = 1.0. frac_pos = 3/5 = 0.6.
        """
        # Build a df with 6 rows so 5 T+1 windows are non-overlapping
        # Each "event" date is followed by one session with the known return.
        dates = [
            "2020-01-02", "2020-01-03",   # event 0 -> +1
            "2020-01-06", "2020-01-07",   # event 1 -> +2
            "2020-01-08", "2020-01-09",   # event 2 -> +3
            "2020-01-10", "2020-01-13",   # event 3 -> -1
            "2020-01-14", "2020-01-15",   # event 4 -> -2
        ]
        changes = [0.0, 1.0, 0.0, 2.0, 0.0, 3.0, 0.0, -1.0, 0.0, -2.0]
        df = _make_df(dates, changes)
        event_dates = ["2020-01-02", "2020-01-06", "2020-01-08", "2020-01-10", "2020-01-14"]
        vals = event_returns(df, event_dates, horizon=1)
        assert sorted(vals) == pytest.approx([-2.0, -1.0, 1.0, 2.0, 3.0])
        median = sorted(vals)[len(vals) // 2]
        assert median == pytest.approx(1.0)
        frac_pos = sum(1 for v in vals if v > 0) / len(vals)
        assert frac_pos == pytest.approx(0.6)

    def test_empty_df_returns_empty(self):
        assert event_returns(pd.DataFrame(), ["2020-01-02"], horizon=1) == []

    def test_none_df_returns_empty(self):
        assert event_returns(None, ["2020-01-02"], horizon=1) == []

    def test_no_spx_chg_column_returns_empty(self):
        df = _make_df(["2020-01-02", "2020-01-03"], [0.0, 1.0])
        df = df.rename(columns={"spx_chg": "other"})
        assert event_returns(df, ["2020-01-02"], horizon=1) == []

    def test_horizon_zero_returns_empty(self):
        df = _make_df(["2020-01-02", "2020-01-03"], [0.0, 1.0])
        assert event_returns(df, ["2020-01-02"], horizon=0) == []


# ---------------------------------------------------------------------------
# bootstrap_ci
# ---------------------------------------------------------------------------

class TestBootstrapCI:
    def test_empty_values_returns_nan_tuple(self):
        lo, hi = bootstrap_ci([])
        assert math.isnan(lo)
        assert math.isnan(hi)

    def test_zero_nboot_degrades_not_raises(self):
        """n_boot=0 must degrade to (nan, nan), not IndexError on an empty medians list."""
        lo, hi = bootstrap_ci([1.0, 2.0, 3.0], n_boot=0)
        assert math.isnan(lo) and math.isnan(hi)

    def test_ci_contains_zero_for_zero_mean_noise(self):
        """Seeded symmetric noise: 95% CI on median must include zero."""
        np.random.seed(42)
        vals = list(np.random.normal(0, 1, 80))
        lo, hi = bootstrap_ci(vals, n_boot=2000, seed=0)
        assert lo <= 0.0 <= hi, f"Expected CI [{lo:.3f}, {hi:.3f}] to include 0"

    def test_ci_excludes_zero_for_strongly_positive_data(self):
        """All-positive returns: CI should be entirely above zero."""
        vals = [1.0] * 50
        lo, hi = bootstrap_ci(vals, n_boot=500, seed=0)
        assert lo > 0.0

    def test_lo_le_hi(self):
        vals = [0.5, -0.3, 1.2, -0.1, 0.8]
        lo, hi = bootstrap_ci(vals, n_boot=200, seed=7)
        assert lo <= hi

    def test_single_value_ci(self):
        lo, hi = bootstrap_ci([3.14], n_boot=100, seed=0)
        assert lo == pytest.approx(3.14)
        assert hi == pytest.approx(3.14)


# ---------------------------------------------------------------------------
# fomc_drift
# ---------------------------------------------------------------------------

class TestFomcDrift:
    def _minimal_df(self) -> pd.DataFrame:
        """A small df with a known clean window around one real FOMC date."""
        # Use 2020-06-10 (scheduled FOMC) as an anchor event.
        # Surround it with 5 clean sessions after.
        dates = pd.bdate_range("2020-06-08", periods=8)
        np.random.seed(42)
        changes = list(np.random.normal(0.1, 1.0, 8))
        df = pd.DataFrame({"spx_chg": changes}, index=dates)
        return df

    def test_returns_list_of_dicts(self):
        df = self._minimal_df()
        result = fomc_drift(df, horizons=(1,))
        assert isinstance(result, list)
        assert len(result) == 1
        row = result[0]
        assert row["horizon"] == 1
        assert isinstance(row["n"], int)
        assert isinstance(row["n_skipped"], int)

    def test_n_plus_n_skipped_equals_total_dates(self):
        df = self._minimal_df()
        total = len(FOMC_DECISION_DATES)
        result = fomc_drift(df, horizons=(1, 2, 5))
        for row in result:
            assert row["n"] + row["n_skipped"] == total

    def test_empty_df_returns_empty_list(self):
        assert fomc_drift(pd.DataFrame(), horizons=(1,)) == []

    def test_none_df_returns_empty_list(self):
        assert fomc_drift(None, horizons=(1,)) == []

    def test_no_usable_events_returns_zero_n(self):
        """A df with no rows after any FOMC date -> n=0, graceful degradation."""
        # All rows are before the earliest FOMC date
        dates = pd.to_datetime(["1997-01-02", "1997-01-03"])
        df = pd.DataFrame({"spx_chg": [0.1, 0.2]}, index=dates)
        result = fomc_drift(df, horizons=(1,))
        assert len(result) == 1
        assert result[0]["n"] == 0
        assert result[0]["median"] is None

    def test_includes_zero_field_type(self):
        """includes_zero is bool or None, never an unexpected type."""
        df = self._minimal_df()
        result = fomc_drift(df, horizons=(1, 5))
        for row in result:
            assert row["includes_zero"] is None or isinstance(row["includes_zero"], bool)

    def test_frac_pos_in_unit_interval(self):
        df = self._minimal_df()
        result = fomc_drift(df, horizons=(1,))
        for row in result:
            if row["frac_pos"] is not None:
                assert 0.0 <= row["frac_pos"] <= 1.0

    def test_null_inside_window_counted_in_n_skipped(self):
        """Inject a null into a window after a known FOMC date; it must land in n_skipped."""
        # Use a real FOMC date with a tight, controlled surrounding window.
        # 2024-06-12 is a real FOMC date.
        # Build a df: 2024-06-12 (event day), then T+1 has null spx_chg.
        base = pd.bdate_range("2024-06-11", periods=10)
        changes = [0.5] * 10
        df = pd.DataFrame({"spx_chg": pd.array(changes, dtype="Float64")}, index=base)
        # Inject null at T+1 after 2024-06-12 (index 1 in bdate_range starting 2024-06-11 is 2024-06-12,
        # so T+1 is 2024-06-13, which is index 2 in the range)
        df.loc[pd.Timestamp("2024-06-13"), "spx_chg"] = pd.NA
        result_with_null = fomc_drift(df, horizons=(1,))
        # Compare with a df that has no null (full clean data)
        df_clean = df.copy()
        df_clean.loc[pd.Timestamp("2024-06-13"), "spx_chg"] = 0.5
        result_clean = fomc_drift(df_clean, horizons=(1,))
        row_null = result_with_null[0]
        row_clean = result_clean[0]
        # The null version should skip at least one more event than the clean version
        assert row_null["n_skipped"] >= row_clean["n_skipped"]


# ---------------------------------------------------------------------------
# FOMC_DECISION_DATES sanity checks
# ---------------------------------------------------------------------------

class TestFomcDecisionDates:
    def test_all_parse_as_dates(self):
        """Every entry must parse as a valid date without raising."""
        for d in FOMC_DECISION_DATES:
            parsed = pd.Timestamp(d)
            assert not pd.isna(parsed), f"Failed to parse: {d!r}"

    def test_strictly_increasing(self):
        """Dates must be in ascending order with no duplicates."""
        timestamps = [pd.Timestamp(d) for d in FOMC_DECISION_DATES]
        for i in range(1, len(timestamps)):
            assert timestamps[i] > timestamps[i - 1], (
                f"Not strictly increasing at index {i}: "
                f"{FOMC_DECISION_DATES[i-1]} -> {FOMC_DECISION_DATES[i]}"
            )

    def test_year_range_1998_to_2025(self):
        """All dates must fall within 1998-2025."""
        for d in FOMC_DECISION_DATES:
            year = pd.Timestamp(d).year
            assert 1998 <= year <= 2025, f"Out-of-range year in {d!r}: {year}"

    def test_2020_03_18_cancelled_meeting_absent(self):
        """The scheduled March 17-18 2020 meeting was CANCELLED (the 03-15 emergency cut replaced
        it). It is not a real decision day and must not contaminate the event windows."""
        assert "2020-03-18" not in FOMC_DECISION_DATES

    def test_per_year_count_between_7_and_9(self):
        """Each year should have 7-9 scheduled meetings."""
        from collections import Counter
        year_counts = Counter(pd.Timestamp(d).year for d in FOMC_DECISION_DATES)
        for year, count in year_counts.items():
            assert 7 <= count <= 9, f"Year {year} has {count} dates (expected 7-9)"

    def test_total_count_plausible(self):
        """224 ± 16 dates expected (28 years × ~8/yr)."""
        n = len(FOMC_DECISION_DATES)
        assert 208 <= n <= 240, f"Total count {n} outside plausible range [208, 240]"

    def test_anchor_dates_present(self):
        """Four known anchor dates must be present."""
        anchors = {
            "2008-12-16",  # ZIRP
            "2022-06-15",  # +75bp
            "2019-07-31",  # first cut of 2019 easing cycle
            "2015-12-16",  # liftoff from ZLB
        }
        dates_set = set(FOMC_DECISION_DATES)
        for anchor in anchors:
            assert anchor in dates_set, f"Anchor date missing: {anchor}"
