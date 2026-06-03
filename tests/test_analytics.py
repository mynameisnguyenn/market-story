"""Statistical-context analytics for macro series (no network)."""
import numpy as np
import pandas as pd

from src import macro_data


def test_stat_context_percentile_and_zscore():
    idx = pd.date_range("2025-01-01", periods=300, freq="D")
    s = pd.Series(np.arange(300, dtype=float), index=idx)   # latest is the max of the window
    pct, z = macro_data._stat_context(s)
    assert pct >= 99            # latest sits at the top of its trailing year
    assert z is not None and z > 1.5


def test_stat_context_low_value_is_low_percentile():
    idx = pd.date_range("2025-01-01", periods=300, freq="D")
    s = pd.Series(np.concatenate([np.arange(299, dtype=float), [0.0]]), index=idx)  # latest = min
    pct, z = macro_data._stat_context(s)
    assert pct == 0.0
    assert z < -1.5


def test_stat_context_needs_enough_history():
    assert macro_data._stat_context(pd.Series([1.0, 2.0, 3.0])) == (None, None)
    assert macro_data._stat_context(None) == (None, None)


def test_snapshot_skips_context_for_trending_series():
    idx = pd.date_range("2025-01-01", periods=300, freq="D")
    s = pd.Series(np.arange(300, dtype=float), index=idx)
    assert macro_data._snapshot("CPIAUCSL", "CPI", s)["pct_1y"] is None      # trending -> skipped
    level = macro_data._snapshot("DGS10", "10Y", s)
    assert level["pct_1y"] is not None and level["z_1y"] is not None         # mean-reverting -> computed
