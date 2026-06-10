"""Tests for src/proxy_books.py — synthetic data only, no network, seed=42.

THE sign test is the anchor of this suite: a falling-yield window MUST produce
a POSITIVE bond proxy return.  This is the exact bug the grill caught (pct_change
on a YIELD level column flips sign compared to the correct -duration * diff formula).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src import proxy_books as pb


# ---------------------------------------------------------------------------
# Synthetic DataFrame builders
# ---------------------------------------------------------------------------


def _make_df(
    periods: int = 500,
    start: str = "2006-01-01",
    seed: int = 42,
) -> pd.DataFrame:
    """Synthetic timeline DataFrame with spx, spx_chg, ust10 columns."""
    np.random.seed(seed)
    idx = pd.bdate_range(start=start, periods=periods)
    spx_chg = pd.Series(np.random.normal(0.0, 1.0, periods), index=idx)
    spx = 1000.0 * (1.0 + spx_chg / 100.0).cumprod()
    # yield: start ~4%, small daily moves
    ust10_chg = pd.Series(np.random.normal(0.0, 0.03, periods), index=idx)
    ust10 = 4.0 + ust10_chg.cumsum()
    return pd.DataFrame({"spx": spx, "spx_chg": spx_chg, "ust10": ust10}, index=idx)


def _crash_df(periods: int = 200, seed: int = 42) -> pd.DataFrame:
    """Synthetic crash: strong negative spx_chg, mild yield rally (falling yields)."""
    np.random.seed(seed)
    idx = pd.bdate_range(start="2008-09-01", periods=periods)
    # Equity crash: large negative returns
    spx_chg = pd.Series(np.random.normal(-0.5, 1.5, periods), index=idx)
    spx = 1000.0 * (1.0 + spx_chg / 100.0).cumprod()
    # Flight-to-safety: yields fall ~0.02pp per day on average
    ust10_chg = pd.Series(np.random.normal(-0.02, 0.01, periods), index=idx)
    ust10 = 4.5 + ust10_chg.cumsum()
    return pd.DataFrame({"spx": spx, "spx_chg": spx_chg, "ust10": ust10}, index=idx)


def _falling_yield_df(n: int = 20) -> pd.DataFrame:
    """Deterministic: yields fall by 0.10pp each day — bond return must be positive."""
    idx = pd.bdate_range(start="2020-01-01", periods=n)
    ust10 = pd.Series(5.0 - 0.10 * np.arange(n), index=idx, dtype=float)
    spx_chg = pd.Series(np.zeros(n), index=idx)
    return pd.DataFrame({"ust10": ust10, "spx_chg": spx_chg}, index=idx)


def _rising_yield_df(n: int = 20) -> pd.DataFrame:
    """Deterministic: yields rise by 0.10pp each day — bond return must be negative."""
    idx = pd.bdate_range(start="2020-01-01", periods=n)
    ust10 = pd.Series(3.0 + 0.10 * np.arange(n), index=idx, dtype=float)
    spx_chg = pd.Series(np.zeros(n), index=idx)
    return pd.DataFrame({"ust10": ust10, "spx_chg": spx_chg}, index=idx)


# ---------------------------------------------------------------------------
# THE SIGN TEST — pins the exact bug the grill caught
# ---------------------------------------------------------------------------


class TestBondProxyReturnsSign:
    """THE sign test: bond price moves opposite to yield."""

    def test_falling_yield_gives_positive_bond_return(self):
        """Yield falls -> bond prices rise -> positive return.

        The original bug used pct_change() on a yield level, which gives
        a dimensionless ratio with wrong sign semantics.  The fix is
        -BOND_DURATION * diff(), so a falling yield (negative diff) -> positive return.
        """
        df = _falling_yield_df()
        rets = pb.bond_proxy_returns(df)
        rets_clean = rets.dropna()
        assert len(rets_clean) > 0, "No non-NaN bond returns computed"
        assert (rets_clean > 0).all(), (
            f"All bond returns should be positive when yields fall; got {rets_clean.values}"
        )

    def test_rising_yield_gives_negative_bond_return(self):
        """Yield rises -> bond prices fall -> negative return."""
        df = _rising_yield_df()
        rets = pb.bond_proxy_returns(df)
        rets_clean = rets.dropna()
        assert len(rets_clean) > 0
        assert (rets_clean < 0).all(), (
            f"All bond returns should be negative when yields rise; got {rets_clean.values}"
        )

    def test_magnitude_is_duration_times_yield_change(self):
        """A +0.10pp yield move -> exactly -0.8% bond return."""
        idx = pd.bdate_range("2020-01-01", periods=2)
        # day 0: 4.00, day 1: 4.10 -> diff = +0.10 -> return = -8.0 * 0.10 = -0.80
        df = pd.DataFrame({"ust10": [4.00, 4.10], "spx_chg": [0.0, 0.0]}, index=idx)
        rets = pb.bond_proxy_returns(df)
        assert rets.iloc[1] == pytest.approx(-0.80, abs=1e-9)

    def test_first_row_is_nan_because_diff_needs_prior(self):
        """diff() on the first row is NaN — that's correct and expected."""
        df = _falling_yield_df(n=5)
        rets = pb.bond_proxy_returns(df)
        assert pd.isna(rets.iloc[0])

    def test_bond_duration_constant_is_8(self):
        assert pb.BOND_DURATION == 8.0


# ---------------------------------------------------------------------------
# bond_proxy_returns — edge cases
# ---------------------------------------------------------------------------


class TestBondProxyReturnsEdgeCases:
    def test_missing_ust10_returns_empty(self):
        idx = pd.bdate_range("2020-01-01", periods=5)
        df = pd.DataFrame({"spx_chg": [0.1] * 5}, index=idx)
        rets = pb.bond_proxy_returns(df)
        assert isinstance(rets, pd.Series)
        assert rets.empty

    def test_none_input_returns_empty(self):
        rets = pb.bond_proxy_returns(None)
        assert isinstance(rets, pd.Series)
        assert rets.empty

    def test_nan_ust10_propagates_nan(self):
        idx = pd.bdate_range("2020-01-01", periods=4)
        df = pd.DataFrame(
            {"ust10": [4.0, float("nan"), 4.1, 4.2], "spx_chg": [0.0] * 4},
            index=idx,
        )
        rets = pb.bond_proxy_returns(df)
        assert pd.isna(rets.iloc[2])  # diff of NaN is NaN


# ---------------------------------------------------------------------------
# book_returns — weights apply correctly
# ---------------------------------------------------------------------------


class TestBookReturns:
    def test_100pct_spx_equals_spx_chg(self):
        """100% SPX book return == spx_chg (no NaN rows from bond leg)."""
        df = _make_df(periods=50)
        rets = pb.book_returns(df, {"spx": 1.0})
        assert not rets.empty
        # The first row of a bond leg would be NaN but we're not using bond here
        # so all spx_chg rows should be preserved
        pd.testing.assert_series_equal(
            rets.reset_index(drop=True),
            df["spx_chg"].reset_index(drop=True),
            check_names=False,
        )

    def test_hand_computed_weighted_return(self):
        """70/30 book: verify exact weighted sum on a hand-constructed case."""
        idx = pd.bdate_range("2020-01-02", periods=3)
        # day 0: spx_chg=2.0, ust10 needs prior day -> bond NaN -> row dropped
        # day 1: spx_chg=1.0, ust10: 4.0->3.9 -> yield_chg=-0.10 -> bond=+0.80
        #         weighted: 0.70*1.0 + 0.30*0.80 = 0.70+0.24 = 0.94
        # day 2: spx_chg=-1.0, ust10: 3.9->4.1 -> yield_chg=+0.20 -> bond=-1.60
        #         weighted: 0.70*(-1.0) + 0.30*(-1.60) = -0.70-0.48 = -1.18
        df = pd.DataFrame(
            {
                "spx_chg": [2.0, 1.0, -1.0],
                "ust10": [4.0, 3.9, 4.1],
            },
            index=idx,
        )
        rets = pb.book_returns(df, {"spx": 0.70, "bond": 0.30})
        # day 0 dropped (bond NaN), so 2 rows remain
        assert len(rets) == 2
        assert rets.iloc[0] == pytest.approx(0.94, abs=1e-9)
        assert rets.iloc[1] == pytest.approx(-1.18, abs=1e-9)

    def test_null_legs_drop_rows(self):
        """Rows where ANY needed leg is NaN must be excluded from output."""
        idx = pd.bdate_range("2020-01-01", periods=5)
        spx_chg = pd.Series([1.0, float("nan"), 1.0, 1.0, 1.0], index=idx)
        ust10 = pd.Series([4.0, 4.0, 4.0, 4.0, 4.0], index=idx)
        df = pd.DataFrame({"spx_chg": spx_chg, "ust10": ust10}, index=idx)
        rets = pb.book_returns(df, {"spx": 0.70, "bond": 0.30})
        # First bond return is NaN (diff), row with NaN spx_chg also dropped
        assert rets.isna().sum() == 0
        assert len(rets) < 5

    def test_empty_df_returns_empty_series(self):
        rets = pb.book_returns(pd.DataFrame(), {"spx": 1.0})
        assert isinstance(rets, pd.Series)
        assert rets.empty

    def test_none_df_returns_empty_series(self):
        rets = pb.book_returns(None, {"spx": 1.0})
        assert isinstance(rets, pd.Series)
        assert rets.empty

    def test_empty_weights_returns_empty_series(self):
        df = _make_df(periods=20)
        rets = pb.book_returns(df, {})
        assert isinstance(rets, pd.Series)
        assert rets.empty

    def test_missing_spx_chg_column_returns_empty(self):
        idx = pd.bdate_range("2020-01-01", periods=5)
        df = pd.DataFrame({"ust10": [4.0] * 5}, index=idx)
        rets = pb.book_returns(df, {"spx": 1.0})
        assert isinstance(rets, pd.Series)
        assert rets.empty


# ---------------------------------------------------------------------------
# stress_books — drawdown comparison
# ---------------------------------------------------------------------------


class TestStressBooks:
    def test_returns_list_of_dicts(self):
        df = _make_df(periods=5000, start="2006-01-01")
        out = pb.stress_books(df)
        assert isinstance(out, list)
        assert len(out) > 0
        for row in out:
            assert isinstance(row, dict)

    def test_expected_keys_present(self):
        df = _make_df(periods=5000, start="2006-01-01")
        out = pb.stress_books(df)
        required = {"book", "window", "start", "end", "n_days", "return_pct", "max_drawdown_pct"}
        for row in out:
            assert required == set(row.keys()), f"Missing keys in {row}"

    def test_all_books_present(self):
        df = _make_df(periods=5000, start="2006-01-01")
        out = pb.stress_books(df)
        found_books = {row["book"] for row in out}
        assert found_books == set(pb.BOOKS.keys())

    def test_all_windows_present(self):
        df = _make_df(periods=5000, start="2006-01-01")
        out = pb.stress_books(df)
        from src.crisis import DEFAULT_WINDOWS
        expected_windows = {name for _, _, name in DEFAULT_WINDOWS}
        found_windows = {row["window"] for row in out}
        assert found_windows == expected_windows

    def test_7030_shallower_drawdown_than_100spx_in_crash(self):
        """70/30 book should have a shallower max drawdown than 100% SPX in a crash.

        In a crash with a flight-to-safety yield rally, bonds partially offset
        equity losses.  The 70/30 drawdown must be less deep (less negative)
        than the pure equity book.
        """
        df = _crash_df(periods=150, seed=42)
        # Use a custom window matching the crash df's date range
        from src.crisis import DEFAULT_WINDOWS
        # Run stress_books with the crash df — default windows include GFC 2008-09
        # which aligns with our crash df (starts 2008-09-01)
        out = pb.stress_books(df)
        # Find GFC window for both books
        gfc_rows = {
            row["book"]: row
            for row in out
            if row["window"] == "GFC 2008-09"
        }
        if len(gfc_rows) < 2:
            pytest.skip("GFC window not populated with crash data")

        spx_dd = gfc_rows["100% S&P 500"]["max_drawdown_pct"]
        balanced_dd = gfc_rows["70/30 S&P / 10Y proxy"]["max_drawdown_pct"]

        if spx_dd is None or balanced_dd is None:
            pytest.skip("Drawdown could not be computed for this window/data")

        # Both are negative (or zero); 70/30 should be less negative (closer to 0)
        assert balanced_dd > spx_dd, (
            f"70/30 drawdown ({balanced_dd:.2f}%) should be shallower than "
            f"100% SPX ({spx_dd:.2f}%) during a crash with flight-to-safety"
        )

    def test_no_hy_oas_in_output(self):
        """hy_oas must not appear anywhere in stress_books output (grill-verified: zero coverage)."""
        df = _make_df(periods=5000, start="2006-01-01")
        out = pb.stress_books(df)
        for row in out:
            for k in row:
                assert "hy_oas" not in k.lower(), f"hy_oas found in key '{k}'"

    def test_empty_df_degrades_to_empty_stat_rows(self):
        """Empty DataFrame input -> all stat fields are None, never raises."""
        out = pb.stress_books(pd.DataFrame())
        assert isinstance(out, list)
        assert len(out) > 0
        for row in out:
            assert row["n_days"] == 0
            assert row["return_pct"] is None
            assert row["max_drawdown_pct"] is None

    def test_none_df_degrades_gracefully(self):
        """None input -> same graceful degradation as empty DataFrame."""
        out = pb.stress_books(None)
        assert isinstance(out, list)
        for row in out:
            assert row["return_pct"] is None

    def test_n_days_is_nonnegative_int(self):
        df = _make_df(periods=5000, start="2006-01-01")
        out = pb.stress_books(df)
        for row in out:
            assert isinstance(row["n_days"], int)
            assert row["n_days"] >= 0

    def test_return_pct_is_float_or_none(self):
        df = _make_df(periods=5000, start="2006-01-01")
        out = pb.stress_books(df)
        for row in out:
            if row["return_pct"] is not None:
                assert isinstance(row["return_pct"], float)

    def test_max_drawdown_is_nonpositive_or_none(self):
        """Max drawdown is always <= 0 (loss or zero, never a gain)."""
        df = _make_df(periods=5000, start="2006-01-01")
        out = pb.stress_books(df)
        for row in out:
            if row["max_drawdown_pct"] is not None:
                assert row["max_drawdown_pct"] <= 0.0, (
                    f"Drawdown should be <= 0; got {row['max_drawdown_pct']} for {row}"
                )


# ---------------------------------------------------------------------------
# BOOKS constant
# ---------------------------------------------------------------------------


class TestBooksConstant:
    def test_books_has_expected_entries(self):
        assert "100% S&P 500" in pb.BOOKS
        assert "70/30 S&P / 10Y proxy" in pb.BOOKS

    def test_100pct_spx_weights_sum_to_one(self):
        w = pb.BOOKS["100% S&P 500"]
        assert sum(w.values()) == pytest.approx(1.0, abs=1e-9)

    def test_7030_weights_sum_to_one(self):
        w = pb.BOOKS["70/30 S&P / 10Y proxy"]
        assert sum(w.values()) == pytest.approx(1.0, abs=1e-9)

    def test_7030_has_spx_and_bond_legs(self):
        w = pb.BOOKS["70/30 S&P / 10Y proxy"]
        assert "spx" in w and "bond" in w
        assert w["spx"] == pytest.approx(0.70, abs=1e-9)
        assert w["bond"] == pytest.approx(0.30, abs=1e-9)
