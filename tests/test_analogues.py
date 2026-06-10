"""Tests for src/analogues.py — VIX-episode analogue engine.

All data is synthetic; no network calls. np.random.seed(42) for reproducibility.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.analogues import episodes_summary, vix_episodes

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_df(n: int, seed: int = 42) -> pd.DataFrame:
    """Synthetic timeline DataFrame with ~n rows of realistic-ish VIX values."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2010-01-04", periods=n)
    vix = 15.0 + rng.normal(0, 3, size=n)
    vix = np.clip(vix, 9.0, 50.0)
    df = pd.DataFrame({"vix": vix}, index=dates)
    return df


def _inject_spike(df: pd.DataFrame, pos: int, level: float) -> pd.DataFrame:
    """Set a specific row's VIX to `level` to create an engineered spike."""
    df = df.copy()
    df.iloc[pos, df.columns.get_loc("vix")] = level
    return df


# ---------------------------------------------------------------------------
# Core fixture: ~300 rows with two engineered high-VIX spikes
# ---------------------------------------------------------------------------

@pytest.fixture
def df_with_spikes():
    """300-row df; today's vix is ~40 (high); two spikes at pos 50 and 200 (~40)."""
    np.random.seed(42)
    df = _make_df(300)
    # Spike at position 50 (far past) — vix ~40
    df = _inject_spike(df, 50, 40.0)
    # Spike at position 200 (further past) — vix ~41
    df = _inject_spike(df, 200, 41.0)
    # Set today's VIX (last row) to ~40 so the spikes are the nearest analogues
    df.iloc[-1, df.columns.get_loc("vix")] = 40.0
    return df


# ---------------------------------------------------------------------------
# 1. Nearest-percentile selection picks the engineered spike days
# ---------------------------------------------------------------------------

def test_nearest_percentile_selects_spikes(df_with_spikes):
    """The two engineered ~40-VIX days should rank as the top analogues."""
    episodes = vix_episodes(df_with_spikes, k=5, min_gap=5, exclude_recent=10)
    assert len(episodes) >= 2, "Expected at least 2 episodes"
    # The spike dates are known
    spike_date_50 = df_with_spikes.index[50].strftime("%Y-%m-%d")
    spike_date_200 = df_with_spikes.index[200].strftime("%Y-%m-%d")
    returned_dates = {e["date"] for e in episodes}
    assert spike_date_50 in returned_dates, f"Spike at pos 50 ({spike_date_50}) not found"
    assert spike_date_200 in returned_dates, f"Spike at pos 200 ({spike_date_200}) not found"


# ---------------------------------------------------------------------------
# 2. min_gap deduplication: two spikes 5 sessions apart -> only one selected
# ---------------------------------------------------------------------------

def test_min_gap_deduplicates_nearby_spikes():
    """Two spikes separated by only 4 sessions should produce at most one episode."""
    np.random.seed(42)
    df = _make_df(300)
    # Set today high
    df.iloc[-1, df.columns.get_loc("vix")] = 42.0
    # Two spikes 4 sessions apart (positions 100 and 104)
    df = _inject_spike(df, 100, 42.0)
    df = _inject_spike(df, 104, 42.0)

    episodes = vix_episodes(df, k=10, min_gap=21, exclude_recent=10)
    dates = [e["date"] for e in episodes]
    d100 = df.index[100].strftime("%Y-%m-%d")
    d104 = df.index[104].strftime("%Y-%m-%d")
    # At most one of the two adjacent spikes should appear
    both_present = (d100 in dates) and (d104 in dates)
    assert not both_present, "Both adjacent spikes selected — min_gap not enforced"


# ---------------------------------------------------------------------------
# 3. exclude_recent actually excludes the most recent N sessions
# ---------------------------------------------------------------------------

def test_exclude_recent_removes_near_rows():
    """Any day in the last exclude_recent sessions must not appear as an analogue."""
    np.random.seed(42)
    df = _make_df(300)
    df.iloc[-1, df.columns.get_loc("vix")] = 42.0
    # Place a spike just inside the exclusion window (pos 260, exclude_recent=50 -> last 50 = 250..299)
    df = _inject_spike(df, 260, 42.0)

    episodes = vix_episodes(df, k=10, min_gap=5, exclude_recent=50)
    excluded_dates = {df.index[i].strftime("%Y-%m-%d") for i in range(250, 300)}
    returned_dates = {e["date"] for e in episodes}
    overlap = excluded_dates & returned_dates
    assert len(overlap) == 0, f"Excluded-window dates appeared: {overlap}"


# ---------------------------------------------------------------------------
# 4. Null-VIX rows are skipped; tiny / empty df returns []
# ---------------------------------------------------------------------------

def test_null_vix_rows_skipped():
    """Rows with NaN vix must not appear as analogues."""
    np.random.seed(42)
    df = _make_df(100)
    df.iloc[-1, df.columns.get_loc("vix")] = 40.0
    # NaN out a chunk of rows in the candidate zone
    df.iloc[10:40, df.columns.get_loc("vix")] = np.nan

    episodes = vix_episodes(df, k=5, min_gap=5, exclude_recent=5)
    nan_dates = {df.index[i].strftime("%Y-%m-%d") for i in range(10, 40)}
    returned_dates = {e["date"] for e in episodes}
    assert len(nan_dates & returned_dates) == 0, "NaN-vix rows appeared in episodes"


def test_empty_df_returns_empty():
    """Empty DataFrame -> []."""
    assert vix_episodes(pd.DataFrame()) == []


def test_tiny_df_returns_empty():
    """DataFrame with only 1 row (today) and no candidates -> []."""
    df = pd.DataFrame({"vix": [20.0]}, index=pd.bdate_range("2024-01-02", periods=1))
    result = vix_episodes(df, k=5, min_gap=5, exclude_recent=5)
    assert result == []


def test_today_vix_null_returns_empty():
    """If today's (last row's) VIX is NaN -> []."""
    np.random.seed(42)
    df = _make_df(100)
    df.iloc[-1, df.columns.get_loc("vix")] = np.nan
    assert vix_episodes(df, k=5, min_gap=5, exclude_recent=5) == []


def test_no_vix_column_returns_empty():
    """DataFrame without a 'vix' column -> []."""
    df = pd.DataFrame({"spx": [100, 101]}, index=pd.bdate_range("2024-01-02", periods=2))
    assert vix_episodes(df) == []


# ---------------------------------------------------------------------------
# 5. resolved flag: hand-built case
# ---------------------------------------------------------------------------

def test_resolved_flag_true_when_vix_falls():
    """resolved should be True when vix_21d < vix on the episode date."""
    np.random.seed(42)
    # Build a small df: spike at pos 10, then VIX declines after it
    dates = pd.bdate_range("2020-01-02", periods=120)
    vix = np.full(120, 15.0)
    vix[10] = 45.0          # big spike — the analogue
    vix[11:32] = 12.0       # VIX calms down after the spike (positions 11-31 are the 21 sessions after)
    vix[-1] = 44.0          # today's VIX is also high -> spike at 10 is the best analogue
    df = pd.DataFrame({"vix": vix}, index=dates)

    episodes = vix_episodes(df, k=3, min_gap=5, exclude_recent=5)
    spike_date = dates[10].strftime("%Y-%m-%d")
    ep = next((e for e in episodes if e["date"] == spike_date), None)
    assert ep is not None, f"Spike episode at {spike_date} not found in {[e['date'] for e in episodes]}"
    assert ep["resolved"] is True, f"Expected resolved=True, got {ep['resolved']}"
    assert ep["vix_21d"] is not None
    assert ep["vix_21d"] < ep["vix"]


def test_resolved_flag_false_when_vix_rises():
    """resolved should be False when vix_21d > vix on the episode date."""
    dates = pd.bdate_range("2020-01-02", periods=120)
    vix = np.full(120, 15.0)
    vix[10] = 30.0          # moderate spike — the analogue
    vix[11:32] = 45.0       # VIX escalates after (positions 11-31)
    vix[-1] = 30.0          # today matches the spike
    df = pd.DataFrame({"vix": vix}, index=dates)

    episodes = vix_episodes(df, k=3, min_gap=5, exclude_recent=5)
    spike_date = dates[10].strftime("%Y-%m-%d")
    ep = next((e for e in episodes if e["date"] == spike_date), None)
    assert ep is not None
    assert ep["resolved"] is False


def test_resolved_none_when_vix21d_missing():
    """When vix_21d is unavailable (near end of history), resolved must be None."""
    np.random.seed(42)
    # Short df: spike near the end but with < 21 rows of history after it
    n = 30
    dates = pd.bdate_range("2024-01-02", periods=n)
    vix = np.full(n, 15.0)
    vix[5] = 40.0   # spike near position 5 — only ~24 rows of history exist
    vix[-1] = 40.0  # today's VIX matches spike
    df = pd.DataFrame({"vix": vix}, index=dates)

    # exclude_recent=5 so pos 5 (with 24 rows after = positions 6..29 = 24 sessions) IS included
    # But spike is at pos 5 with 24 sessions after it (>21), so vix_21d should be available.
    # To force None: put spike at a position that has < 21 rows after it.
    vix2 = np.full(n, 15.0)
    vix2[n - 8] = 40.0   # only 7 rows after (< 21), so vix_21d will be None
    vix2[-1] = 40.0
    df2 = pd.DataFrame({"vix": vix2}, index=dates)

    # exclude_recent=5: last 5 rows excluded, so n-8 is in the candidate zone (pos n-8 < n-5)
    episodes = vix_episodes(df2, k=3, min_gap=5, exclude_recent=5)
    spike_date = dates[n - 8].strftime("%Y-%m-%d")
    ep = next((e for e in episodes if e["date"] == spike_date), None)
    assert ep is not None, f"{spike_date} not in {[e['date'] for e in episodes]}"
    assert ep["vix_21d"] is None, f"Expected vix_21d=None, got {ep['vix_21d']}"
    assert ep["resolved"] is None


# ---------------------------------------------------------------------------
# 6. episodes_summary
# ---------------------------------------------------------------------------

def test_episodes_summary_counts():
    """episodes_summary counts resolved/unresolved correctly."""
    episodes = [
        {"resolved": True},
        {"resolved": True},
        {"resolved": False},
        {"resolved": None},
        {"resolved": None},
    ]
    s = episodes_summary(episodes)
    assert s["n"] == 5
    assert s["resolved_lower"] == 2
    assert s["unresolved"] == 2


def test_episodes_summary_empty():
    """episodes_summary on [] -> all zeros."""
    s = episodes_summary([])
    assert s == {"n": 0, "resolved_lower": 0, "unresolved": 0}


# ---------------------------------------------------------------------------
# 7. Episode dict shape
# ---------------------------------------------------------------------------

def test_episode_dict_shape(df_with_spikes):
    """Every episode dict must have the required keys."""
    required = {"date", "era", "vix", "vix_pct", "vix_5d", "vix_21d", "resolved"}
    episodes = vix_episodes(df_with_spikes, k=3, min_gap=5, exclude_recent=10)
    assert len(episodes) > 0
    for ep in episodes:
        missing = required - ep.keys()
        assert not missing, f"Missing keys: {missing}"
        # date must be a valid ISO string
        assert len(ep["date"]) == 10
        assert ep["date"][4] == "-"


# ---------------------------------------------------------------------------
# 8. k respected
# ---------------------------------------------------------------------------

def test_k_respected(df_with_spikes):
    """Result length must not exceed k."""
    for k in (1, 3, 5, 10):
        episodes = vix_episodes(df_with_spikes, k=k, min_gap=5, exclude_recent=10)
        assert len(episodes) <= k, f"Got {len(episodes)} episodes for k={k}"


# ---------------------------------------------------------------------------
# 9. vix_pct within [0, 100]
# ---------------------------------------------------------------------------

def test_vix_pct_range(df_with_spikes):
    """vix_pct must be in [0, 100] for all episodes."""
    episodes = vix_episodes(df_with_spikes, k=10, min_gap=5, exclude_recent=10)
    for ep in episodes:
        assert 0.0 <= ep["vix_pct"] <= 100.0, f"vix_pct out of range: {ep['vix_pct']}"
