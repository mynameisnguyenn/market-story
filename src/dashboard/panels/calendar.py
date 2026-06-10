"""Calendar tab — upcoming economic releases, smart-money 13F holdings, watchlist
earnings dates, and recent SEC filings."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src import calendar_data, config, event_study, thirteenf
from src.dashboard.data import get_13f, get_earnings, get_econ, get_filings, get_timeline_df


def _earnings_section() -> None:
    """Upcoming earnings for the watchlist + indices (button-triggered, cached)."""
    st.subheader("Upcoming earnings — watchlist + US indices")
    symbols = tuple(dict.fromkeys(s for s, _ in config.get_watchlist() + config.US_EQUITIES))
    if st.button("Load / refresh earnings dates", key="load_earnings"):
        st.session_state["earnings_rows"] = get_earnings(symbols)
    rows = st.session_state.get("earnings_rows")
    if rows is None:
        st.caption("Click to pull next earnings dates via yfinance (cached 1h). "
                   "Kept off the main load so the dashboard stays fast.")
    elif not rows:
        st.info("No upcoming earnings in the next 60 days, or the source is throttling — try again shortly.")
    else:
        frame = pd.DataFrame([
            {"Date": r["date"], "In (days)": r["days"], "Ticker": r["symbol"], "Company": r["name"]}
            for r in rows
        ])
        st.dataframe(frame, use_container_width=True, hide_index=True)
        st.caption(f"{len(rows)} names · earliest first · via yfinance")


def _filings_section() -> None:
    """Recent SEC EDGAR filings for the watchlist (button-triggered, cached)."""
    st.subheader("Recent SEC filings — watchlist")
    wl = tuple(s for s, _ in config.get_watchlist())
    if st.button("Load / refresh SEC filings", key="load_filings"):
        st.session_state["filings_rows"] = get_filings(wl)
    rows = st.session_state.get("filings_rows")
    if rows is None:
        st.caption("Click to pull recent 8-K / 10-Q / 10-K filings for your watchlist "
                   "via SEC EDGAR (keyless, cached 6h).")
    elif not rows:
        st.info("No recent filings found, or SEC is rate-limiting — try again shortly.")
    else:
        frame = pd.DataFrame([
            {"Date": r["date"], "Ticker": r["symbol"], "Form": r["form"],
             "Description": r["desc"], "Filing": r["link"]}
            for r in rows
        ])
        st.dataframe(
            frame, use_container_width=True, hide_index=True,
            column_config={"Filing": st.column_config.LinkColumn("Filing", display_text="open")},
        )
        st.caption(f"{len(rows)} filings · newest first · via SEC EDGAR")


def _fomc_section() -> None:
    """Countdown to the next FOMC rate decision — the single biggest scheduled macro risk event."""
    nf = calendar_data.next_fomc()
    if not nf:                                   # schedule ran out — nudge to refresh the dates
        st.caption("Next FOMC date unavailable — update `FOMC_DECISIONS` in `src/calendar_data.py` "
                   "with the Fed's latest published calendar.")
        return
    d = nf["days"]
    when = "today" if d == 0 else "tomorrow" if d == 1 else f"in {d} days"
    st.subheader("Next FOMC decision")
    st.metric(nf["date"], when, delta="rate decision + statement", delta_color="off")
    st.caption("Statement ~2:00pm ET; quarterly meetings add the Summary of Economic Projections + a "
               "press conference. Schedule from federalreserve.gov, verified 2026-06. Source: Federal Reserve.")


def _fomc_drift_section() -> None:
    """28 years of post-FOMC S&P drift — the honest event study. If the bootstrap CIs all
    straddle zero (the statistically expected result), the panel says exactly that, leading:
    'no detectable drift' delivered confidently IS the finding, not a failure to find one."""
    try:
        rows = event_study.fomc_drift(get_timeline_df())
    except Exception:
        return
    if not rows:
        return
    with st.expander("📐 Post-FOMC drift — S&P after every scheduled decision since 1998"):
        if all(r.get("includes_zero") is not False for r in rows):   # None (n=0 horizon) is neutral
            st.info(f"Across ~{max(r.get('n', 0) for r in rows)} scheduled decisions, S&P returns "
                    "after FOMC days are statistically indistinguishable from zero at every horizon "
                    "tested (bootstrap CIs on the median all include zero). There is no detectable "
                    "post-FOMC drift in this sample — that is the finding.")
        st.dataframe(pd.DataFrame([
            {"Horizon": f"T+{r['horizon']}", "n": r.get("n"),
             "Median": f"{r['median']:+.2f}%" if r.get("median") is not None else "—",
             "95% CI": (f"[{r['ci_lo']:+.2f}%, {r['ci_hi']:+.2f}%]"
                        if r.get("ci_lo") is not None and r.get("ci_hi") is not None else "—"),
             "% positive": f"{r['frac_pos'] * 100:.0f}%" if r.get("frac_pos") is not None else "—",
             "Skipped": r.get("n_skipped", 0)}
            for r in rows]), use_container_width=True, hide_index=True)
        st.caption("Scheduled decisions only, 1998–2025 (unscheduled/emergency meetings excluded — "
                   "their dates are themselves the news). T+1/2/5 windows never overlap across "
                   "meetings ~6 weeks apart, so iid bootstrap CIs are valid here, unlike rolling-"
                   "signal stats. Descriptive history, **not a forecast**. Source: event_study.")
    st.divider()


def _econ_section() -> None:
    rows = get_econ()
    if not rows:
        return
    st.subheader("Economic releases")
    st.caption("The data the market trades around")
    frame = pd.DataFrame([
        {"Release": r["name"], "Date": r["date"],
         "In": ("tomorrow ⚠️" if r["days"] == 1 else "today ⚠️" if r["days"] == 0 else f"{r['days']} days")}
        for r in rows
    ])
    st.dataframe(frame, use_container_width=True, hide_index=True)


def _13f_section() -> None:
    st.subheader("Smart money (13F)")
    st.caption("What prominent managers hold, and last quarter's flow")
    st.caption("Quarterly SEC 13F-HR filings: **long US equities only**, ~45-day lag — positioning, not real-time.")
    names = [n for n, _ in thirteenf.FUNDS]
    choice = st.selectbox("Manager", names, key="f13_fund", label_visibility="collapsed")
    data = get_13f(choice, dict(thirteenf.FUNDS)[choice])
    if not data:
        st.caption("No 13F available for that manager right now.")
        return
    st.caption(f"As of {data['date']} · {data['positions']} positions · ${data['total_value'] / 1e9:,.1f}B reported")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("_Top holdings_")
        st.dataframe(pd.DataFrame([
            {"Holding": h["issuer"], "$B": round(h["value"] / 1e9, 2), "%": round(h["pct"], 1)}
            for h in data["top"]]), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("_Last quarter's moves (vs prior 13F)_")
        st.dataframe(pd.DataFrame([
            {"Move": c["action"], "Holding": c["issuer"], "Δ $B": round(c["delta"] / 1e9, 2)}
            for c in data["changes"]]), use_container_width=True, hide_index=True)


def calendar_tab() -> None:
    _fomc_section()
    _fomc_drift_section()
    _econ_section()
    st.divider()
    _13f_section()
    st.divider()
    _earnings_section()
    st.divider()
    _filings_section()
