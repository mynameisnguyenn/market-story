"""FOMC event-study engine: post-decision return windows over the timeline.

Computes compounded S&P 500 returns after each scheduled FOMC decision date, with
bootstrap confidence intervals on the median. Emergency/unscheduled meetings are
deliberately excluded — only the final day of each scheduled 8-per-year meeting is
included, because surprise-meeting contamination would confound the drift signal.
"""
from __future__ import annotations

import math
import random
from typing import Sequence

import pandas as pd

from src.timeline_returns import compound_pct

# ---------------------------------------------------------------------------
# FOMC scheduled decision dates 1998-2025 (final day of each scheduled meeting).
#
# EXCLUSIONS (deliberate):
#   - 1999-10-15  emergency inter-meeting cut (Y2K/LTCM aftermath)
#   - 2001-01-03  emergency cut after Nasdaq crash
#   - 2001-09-17  emergency cut post-9/11 (markets reopened)
#   - 2007-08-17  emergency discount-rate cut
#   - 2008-01-22  emergency inter-meeting cut
#   - 2008-10-08  emergency inter-meeting coordinated cut
#   - 2010-05-09  emergency conference call (European debt crisis)
#   - 2020-03-03  emergency cut (COVID-19 onset)
#   - 2020-03-15  emergency cut (COVID-19, weekend before markets reopened)
#
# PROVENANCE: VERIFIED 2026-06-10 against federalreserve.gov. 2021-2025 checked date-for-date
# vs fomccalendars.htm (40/40 exact); 1998/2001/2008/2015/2020 + all of 1999-2019 checked vs the
# per-year fomchistorical<year>.htm pages (Fed-page fetch corroborated against model knowledge,
# year by year). One correction applied from that pass: 2020-03-18 removed (the scheduled March
# meeting was CANCELLED for the 03-15 emergency cut). Net 223 scheduled decision days, 1998-2025.
# Anchor-checks: 2008-12-16 (ZIRP), 2022-06-15 (75bp hike), 2019-07-31
#   (first cut of 2019 easing cycle), 2015-12-16 (liftoff from ZLB).
# ---------------------------------------------------------------------------

FOMC_DECISION_DATES: tuple[str, ...] = (
    # 1998 — 8 scheduled meetings
    "1998-02-04",
    "1998-03-31",
    "1998-05-19",
    "1998-07-01",
    "1998-08-18",
    "1998-09-29",
    "1998-11-17",
    "1998-12-22",
    # 1999 — 8 scheduled meetings
    "1999-02-03",
    "1999-03-30",
    "1999-05-18",
    "1999-06-30",
    "1999-08-24",
    "1999-10-05",
    "1999-11-16",
    "1999-12-21",
    # 2000 — 8 scheduled meetings
    "2000-02-02",
    "2000-03-21",
    "2000-05-16",
    "2000-06-28",
    "2000-08-22",
    "2000-10-03",
    "2000-11-15",
    "2000-12-19",
    # 2001 — 8 scheduled meetings (emergency cuts excluded: 2001-01-03, 2001-09-17)
    "2001-01-31",
    "2001-03-20",
    "2001-05-15",
    "2001-06-27",
    "2001-08-21",
    "2001-10-02",
    "2001-11-06",
    "2001-12-11",
    # 2002 — 8 scheduled meetings
    "2002-01-30",
    "2002-03-19",
    "2002-05-07",
    "2002-06-26",
    "2002-08-13",
    "2002-09-24",
    "2002-11-06",
    "2002-12-10",
    # 2003 — 8 scheduled meetings
    "2003-01-29",
    "2003-03-18",
    "2003-05-06",
    "2003-06-25",
    "2003-08-12",
    "2003-09-16",
    "2003-10-28",
    "2003-12-09",
    # 2004 — 8 scheduled meetings
    "2004-01-28",
    "2004-03-16",
    "2004-05-04",
    "2004-06-30",
    "2004-08-10",
    "2004-09-21",
    "2004-11-10",
    "2004-12-14",
    # 2005 — 8 scheduled meetings
    "2005-02-02",
    "2005-03-22",
    "2005-05-03",
    "2005-06-30",
    "2005-08-09",
    "2005-09-20",
    "2005-11-01",
    "2005-12-13",
    # 2006 — 8 scheduled meetings
    "2006-01-31",
    "2006-03-28",
    "2006-05-10",
    "2006-06-29",
    "2006-08-08",
    "2006-09-20",
    "2006-10-25",
    "2006-12-12",
    # 2007 — 8 scheduled meetings (emergency discount-rate cut 2007-08-17 excluded)
    "2007-01-31",
    "2007-03-21",
    "2007-05-09",
    "2007-06-28",
    "2007-08-07",
    "2007-09-18",
    "2007-10-31",
    "2007-12-11",
    # 2008 — 8 scheduled meetings (emergency cuts 2008-01-22, 2008-10-08 excluded)
    "2008-01-30",
    "2008-03-18",
    "2008-04-30",
    "2008-06-25",
    "2008-08-05",
    "2008-09-16",
    "2008-10-29",
    "2008-12-16",  # ANCHOR: ZIRP (0-0.25% target) set here
    # 2009 — 8 scheduled meetings
    "2009-01-28",
    "2009-03-18",
    "2009-04-29",
    "2009-06-24",
    "2009-08-12",
    "2009-09-23",
    "2009-11-04",
    "2009-12-16",
    # 2010 — 8 scheduled meetings (emergency conference call 2010-05-09 excluded)
    "2010-01-27",
    "2010-03-16",
    "2010-04-28",
    "2010-06-23",
    "2010-08-10",
    "2010-09-21",
    "2010-11-03",
    "2010-12-14",
    # 2011 — 8 scheduled meetings
    "2011-01-26",
    "2011-03-15",
    "2011-04-27",
    "2011-06-22",
    "2011-08-09",
    "2011-09-21",
    "2011-11-02",
    "2011-12-13",
    # 2012 — 8 scheduled meetings
    "2012-01-25",
    "2012-03-13",
    "2012-04-25",
    "2012-06-20",
    "2012-08-01",
    "2012-09-13",
    "2012-10-24",
    "2012-12-12",
    # 2013 — 8 scheduled meetings
    "2013-01-30",
    "2013-03-20",
    "2013-05-01",
    "2013-06-19",
    "2013-07-31",
    "2013-09-18",
    "2013-10-30",
    "2013-12-18",
    # 2014 — 8 scheduled meetings
    "2014-01-29",
    "2014-03-19",
    "2014-04-30",
    "2014-06-18",
    "2014-07-30",
    "2014-09-17",
    "2014-10-29",
    "2014-12-17",
    # 2015 — 8 scheduled meetings
    "2015-01-28",
    "2015-03-18",
    "2015-04-29",
    "2015-06-17",
    "2015-07-29",
    "2015-09-17",
    "2015-10-28",
    "2015-12-16",  # ANCHOR: liftoff from ZLB (+25bp)
    # 2016 — 8 scheduled meetings
    "2016-01-27",
    "2016-03-16",
    "2016-04-27",
    "2016-06-15",
    "2016-07-27",
    "2016-09-21",
    "2016-11-02",
    "2016-12-14",
    # 2017 — 8 scheduled meetings
    "2017-02-01",
    "2017-03-15",
    "2017-05-03",
    "2017-06-14",
    "2017-07-26",
    "2017-09-20",
    "2017-11-01",
    "2017-12-13",
    # 2018 — 8 scheduled meetings
    "2018-01-31",
    "2018-03-21",
    "2018-05-02",
    "2018-06-13",
    "2018-08-01",
    "2018-09-26",
    "2018-11-08",
    "2018-12-19",
    # 2019 — 8 scheduled meetings
    "2019-01-30",
    "2019-03-20",
    "2019-05-01",
    "2019-06-19",
    "2019-07-31",  # ANCHOR: first cut of 2019 easing cycle
    "2019-09-18",
    "2019-10-30",
    "2019-12-11",
    # 2020 — 7 scheduled meetings. The March 17-18 meeting was CANCELLED (the Fed acted early
    # with the 2020-03-15 emergency cut to ZIRP), so there is no March decision day; the
    # 2020-03-03 and 2020-03-15 emergency cuts are excluded as unscheduled.
    "2020-01-29",
    "2020-04-29",
    "2020-06-10",
    "2020-07-29",
    "2020-09-16",
    "2020-11-05",
    "2020-12-16",
    # 2021 — 8 scheduled meetings
    "2021-01-27",
    "2021-03-17",
    "2021-04-28",
    "2021-06-16",
    "2021-07-28",
    "2021-09-22",
    "2021-11-03",
    "2021-12-15",
    # 2022 — 8 scheduled meetings
    "2022-01-26",
    "2022-03-16",
    "2022-05-04",
    "2022-06-15",  # ANCHOR: +75bp (first 75bp hike since 1994)
    "2022-07-27",
    "2022-09-21",
    "2022-11-02",
    "2022-12-14",
    # 2023 — 8 scheduled meetings
    "2023-02-01",
    "2023-03-22",
    "2023-05-03",
    "2023-06-14",
    "2023-07-26",
    "2023-09-20",
    "2023-11-01",
    "2023-12-13",
    # 2024 — 8 scheduled meetings
    "2024-01-31",
    "2024-03-20",
    "2024-05-01",
    "2024-06-12",
    "2024-07-31",
    "2024-09-18",
    "2024-11-07",
    "2024-12-18",
    # 2025 — 8 scheduled meetings
    "2025-01-29",
    "2025-03-19",
    "2025-05-07",
    "2025-06-18",
    "2025-07-30",
    "2025-09-17",
    "2025-10-29",
    "2025-12-10",
)


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

def event_returns(
    df: pd.DataFrame,
    dates: Sequence[str],
    horizon: int,
) -> list[float]:
    """Compound S&P returns over `horizon` sessions after each date in `dates`.

    Events where compound_pct returns None (partial window or any null in window)
    are silently skipped — callers inspect n_skipped via fomc_drift if needed.
    """
    if df is None or len(df) == 0 or "spx_chg" not in df.columns or horizon <= 0:
        return []
    results = []
    for d in dates:
        val = compound_pct(df, d, horizon)
        if val is not None:
            results.append(val)
    return results


def bootstrap_ci(
    values: list[float],
    n_boot: int = 2000,
    seed: int = 0,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """IID bootstrap CI on the median of `values` at level (1-alpha).

    IID bootstrap is defensible here because scheduled FOMC meetings are ~6 weeks
    apart (roughly 30 trading sessions), so post-event return windows of T+1, T+2,
    or T+5 sessions never overlap across events. There is no autocorrelation in the
    event sample that would require a block bootstrap (contrast with the rolling-
    signal backtest in backtest.py, which uses overlapping windows and needs blocks).

    Returns (lo, hi). Returns (nan, nan) if values is empty or n_boot <= 0.
    """
    if not values or n_boot <= 0:
        return (math.nan, math.nan)
    n = len(values)
    rng = random.Random(seed)
    medians = []
    for _ in range(n_boot):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        sample.sort()
        mid = n // 2
        med = sample[mid] if n % 2 == 1 else (sample[mid - 1] + sample[mid]) / 2.0
        medians.append(med)
    medians.sort()
    lo_idx = int(alpha / 2.0 * n_boot)
    hi_idx = int((1.0 - alpha / 2.0) * n_boot) - 1
    lo_idx = max(0, min(lo_idx, n_boot - 1))
    hi_idx = max(0, min(hi_idx, n_boot - 1))
    return (medians[lo_idx], medians[hi_idx])


def fomc_drift(
    df: pd.DataFrame,
    horizons: tuple[int, ...] = (1, 2, 5),
) -> list[dict]:
    """Post-FOMC S&P drift table across horizons, using FOMC_DECISION_DATES.

    Returns a list of dicts, one per horizon::

        {horizon, n, n_skipped, median, frac_pos, ci_lo, ci_hi, includes_zero}

    Returns an empty list if df is empty or lacks spx_chg.
    """
    if df is None or len(df) == 0 or "spx_chg" not in df.columns:
        return []
    rows = []
    total_dates = len(FOMC_DECISION_DATES)
    for h in horizons:
        vals = event_returns(df, FOMC_DECISION_DATES, h)
        n = len(vals)
        n_skipped = total_dates - n
        if n == 0:
            rows.append({
                "horizon": h,
                "n": 0,
                "n_skipped": n_skipped,
                "median": None,
                "frac_pos": None,
                "ci_lo": None,
                "ci_hi": None,
                "includes_zero": None,
            })
            continue
        vals_sorted = sorted(vals)
        mid = n // 2
        median = vals_sorted[mid] if n % 2 == 1 else (vals_sorted[mid - 1] + vals_sorted[mid]) / 2.0
        frac_pos = sum(1 for v in vals if v > 0) / n
        ci_lo, ci_hi = bootstrap_ci(vals)
        includes_zero = (
            None if (math.isnan(ci_lo) or math.isnan(ci_hi))
            else (ci_lo <= 0.0 <= ci_hi)
        )
        rows.append({
            "horizon": h,
            "n": n,
            "n_skipped": n_skipped,
            "median": median,
            "frac_pos": frac_pos,
            "ci_lo": ci_lo,
            "ci_hi": ci_hi,
            "includes_zero": includes_zero,
        })
    return rows
