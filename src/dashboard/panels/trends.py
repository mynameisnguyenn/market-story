"""Trends tab — the committed cross-asset metrics timeline as charts, a time machine,
crisis-window replay, and signal Information Coefficient."""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from src import analogues, crisis, eras, riskmetrics, signal_ic
from src.dashboard.charts import color_changes, trend_fig
from src.dashboard.data import get_timeline_df

_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _fmt2(x) -> str:
    return f"{x:.2f}" if x is not None else "—"

TREND_METRICS = [
    ("ust10", "10Y Treasury yield (%)"),
    ("curve_2s10s", "2s10s curve (pp)"),
    ("hy_oas", "HY credit spread (%)"),
    ("vix", "VIX"),
    ("spx_spec_net", "S&P lev-fund net (contracts)"),
    ("vol_premium", "Vol risk premium (VIX − realized)"),
]


# Verdicts from the full 28-year block-bootstrap backtest (research/signal-validation.md): which of
# these signals actually have a robust forward-return edge, vs. which are descriptive context.
_SIGNAL_VERDICTS = {
    "vix": "✓ robust (buy-fear)",
    "curve_2s10s": "✗ no edge",
    "hy_oas": "⚠ short sample",
    "vol_premium": "✗ no edge",
}


def _crisis_signal_panel(df) -> None:
    """Crisis-window replay + signal Information Coefficient over the committed timeline."""
    if df is None or df.empty or "spx" not in df.columns:
        return
    spx = pd.to_numeric(df["spx"], errors="coerce").dropna()
    if len(spx) < 60:
        return
    spx_rets = spx.pct_change().dropna()
    st.divider()
    rep = [r for r in crisis.crisis_replay(spx_rets) if r.get("n_days")]
    if rep:
        st.subheader("Crisis replay — S&P through past stress windows")
        st.caption("How the S&P behaved in each episode, from the committed timeline. Source: crisis.")
        cr = pd.DataFrame([{
            "Episode": r["name"],
            "Return %": (r["return"] * 100) if r["return"] is not None else None,
            "Max DD %": (r["max_drawdown"] * 100) if r["max_drawdown"] is not None else None,
            "VaR95 %": (r["var95"] * 100) if r["var95"] is not None else None,
            "ES95 %": (r["es95"] * 100) if r["es95"] is not None else None,
        } for r in rep])
        st.dataframe(cr.style.format({"Return %": "{:+.1f}", "Max DD %": "{:.1f}",
                     "VaR95 %": "{:.2f}", "ES95 %": "{:.2f}"}, na_rep="—")
                     .map(color_changes, subset=["Return %"]),
                     use_container_width=True, hide_index=True)
    ic_rows = []
    hy_oas_short = False
    for label, col in [("VIX level", "vix"), ("2s10s curve", "curve_2s10s"),
                       ("HY OAS", "hy_oas"), ("Vol premium", "vol_premium")]:
        if col not in df.columns:
            continue
        sig = pd.to_numeric(df[col], errors="coerce")
        ic = signal_ic.ic_by_horizon(sig, spx)
        if any(v is not None for v in ic.values()):
            n = int(sig.notna().sum())
            if col == "hy_oas" and n < 252:                  # under ~1y of overlap — IC is noisy
                hy_oas_short = True
            ic_rows.append({"Signal": label, "IC 1d": ic.get(1), "IC 5d": ic.get(5),
                            "IC 21d": ic.get(21), "n": n,
                            "Edge (28y test)": _SIGNAL_VERDICTS.get(col, "—")})
    if ic_rows:
        st.subheader("Signal edge — Information Coefficient")
        st.caption("Live rank correlation of each signal with forward S&P returns. The **Edge** column "
                   "is the verdict from the full 28-year block-bootstrap backtest "
                   "(`research/signal-validation.md`): only **VIX level** shows a robust, regime-stable "
                   "edge (high fear → higher forward returns); the 2s10s curve and vol premium don't "
                   "predict; HY OAS rests on a ~3y sample. Read the live IC against that verdict, not on "
                   "its own. `n` = overlapping observations. Source: signal_ic.")
        st.dataframe(pd.DataFrame(ic_rows).style.format(
            {"IC 1d": "{:+.3f}", "IC 5d": "{:+.3f}", "IC 21d": "{:+.3f}", "n": "{:,d}"}, na_rep="—")
            .map(color_changes, subset=["IC 1d", "IC 5d", "IC 21d"]),
            use_container_width=True, hide_index=True)
        if hy_oas_short:
            st.caption("⚠ HY OAS history is FRED-license-limited to a ~3y trailing window, so its IC "
                       "rests on a smaller sample than the others — read it as indicative, not settled.")


def _tearsheet_panel(df) -> None:
    """quantstats-style tearsheet for the S&P over the full committed timeline: risk-adjusted
    headline metrics + a year × month return table, all from riskmetrics (no new data)."""
    if df is None or df.empty or "spx" not in df.columns:
        return
    spx = pd.to_numeric(df["spx"], errors="coerce").dropna()
    if len(spx) < 252:
        return
    rets = riskmetrics.returns(spx)
    if rets is None:
        return
    with st.expander("📊 Tearsheet — S&P 500 (full committed timeline)"):
        yrs = len(spx) / 252.0
        cagr = ((spx.iloc[-1] / spx.iloc[0]) ** (1 / yrs) - 1) * 100 if yrs > 0 else None
        vol = float(rets.std(ddof=1)) * (252 ** 0.5) * 100
        mdd = riskmetrics.max_drawdown(spx)
        cols = st.columns(6)
        cols[0].metric("CAGR", f"{cagr:.1f}%" if cagr is not None else "—")
        cols[1].metric("Vol (ann.)", f"{vol:.1f}%")
        cols[2].metric("Sharpe", _fmt2(riskmetrics.sharpe(rets)))
        cols[3].metric("Sortino", _fmt2(riskmetrics.sortino(rets)))
        cols[4].metric("Calmar", _fmt2(riskmetrics.calmar(spx)))
        cols[5].metric("Max DD", f"{mdd * 100:.1f}%" if mdd is not None else "—")
        st.caption(f"{spx.index[0].date()} → {spx.index[-1].date()} · {len(spx):,} sessions · "
                   "risk-free = 0. Source: riskmetrics over the committed timeline.")
        m = spx.groupby(spx.index.to_period("M")).last()
        mret = m.pct_change().dropna() * 100.0
        by: dict[int, dict[int, float]] = {}
        for p, v in mret.items():
            by.setdefault(p.year, {})[p.month] = float(v)
        rows = []
        for y in sorted(by):
            row = {"Year": y}
            for mi, mname in enumerate(_MONTHS, 1):
                row[mname] = by[y].get(mi)
            vals = list(by[y].values())
            row["FY %"] = (np.prod([1 + x / 100 for x in vals]) - 1) * 100 if vals else None
            rows.append(row)
        frame = pd.DataFrame(rows).set_index("Year")
        st.dataframe(
            frame.style.format({c: "{:+.1f}" for c in _MONTHS + ["FY %"]}, na_rep="·")
            .map(color_changes, subset=_MONTHS + ["FY %"]),
            use_container_width=True)
        st.caption("Monthly total returns (%), green/red by sign; **FY %** compounds the year. "
                   "The most recent month and year are partial (month-/year-to-date). "
                   "Built from the committed timeline's S&P series.")


def _analogue_panel(df) -> None:
    """VIX-episode analogues: the historical days whose VIX percentile most resembles today's,
    and where fear went next. Anchored on the ONE validated signal (VIX level); deliberately
    shows NO forward S&P returns — k≈10 overlapping windows dressed as a return distribution
    would imply precision that isn't there (see research/signal-validation.md)."""
    try:
        eps = analogues.vix_episodes(df)
    except Exception:
        return
    if not eps:
        return
    s = analogues.episodes_summary(eps)
    today_pct = analogues.today_vix_pct(df)
    with st.expander("🌀 Days like today — VIX-percentile analogues"):
        known = s["n"] - s["unresolved"]
        if known > 0:
            st.markdown(f"**Fear resolved lower within 21 sessions in {s['resolved_lower']} "
                        f"of {known} comparable episodes.**")
        st.dataframe(pd.DataFrame([
            {"Date": e.get("date"), "Era": (e.get("era") or {}).get("name", "—"),
             "VIX": _fmt2(e.get("vix")), "%ile": _fmt2(e.get("vix_pct")),
             "VIX +5d": _fmt2(e.get("vix_5d")), "VIX +21d": _fmt2(e.get("vix_21d")),
             "Resolved lower": {True: "✓", False: "✗"}.get(e.get("resolved"), "…")}
            for e in eps]), use_container_width=True, hide_index=True)
        # The "buy fear" edge only applies in a HIGH-VIX regime. These analogues match today's
        # percentile, so when today is calm the matched days are calm too — cite the edge only then.
        if today_pct is not None and today_pct >= 70:
            edge = (" The 28y study's one validated read applies here: with VIX elevated, fear has "
                    "historically preceded higher forward returns (gross of costs).")
        else:
            edge = (" Today's VIX sits mid/low in its history, so these are calmer-regime analogues; "
                    "the validated buy-fear edge applies only when VIX is elevated — here this is "
                    "context, not a signal.")
        st.caption("Matched on full-history VIX percentile, episode-deduped (≥21 sessions apart), "
                   "most-recent quarter excluded. Descriptive memory of where fear went next — "
                   "**not a return forecast**." + edge)


def _time_machine(df) -> None:
    """Pick a historical date -> the era it falls in + each metric's level and percentile
    AS OF that date (vs its own history up to then)."""
    st.divider()
    st.subheader("🕰 Time machine")
    st.caption("Pick a date to see where markets stood, and which era it was")
    dmin, dmax = df.index[0].date(), df.index[-1].date()
    picked = st.date_input("As of", value=dmax, min_value=dmin, max_value=dmax, key="timemachine")
    upto = df[df.index <= pd.Timestamp(picked)]
    if upto.empty:
        st.caption("No data on or before that date.")
        return
    as_of = upto.index[-1]
    era = eras.era_for(as_of.date().isoformat())
    if era:
        st.markdown(f"**{as_of.date()} — {era['name']}**  ·  _{era['regime']}_. {era['blurb']}  \n"
                    f"Fed: {era['fed']}")
    snap = []
    for col, label in TREND_METRICS:
        if col not in upto.columns:
            continue
        series = upto[col].dropna()
        if len(series) < 5:
            continue
        val = float(series.iloc[-1])
        pct = round(float((series < val).mean()) * 100)
        snap.append({"Metric": label, "As-of value": round(val, 2),
                     "%ile (history to date)": pct})
    if snap:
        st.dataframe(pd.DataFrame(snap), use_container_width=True, hide_index=True)


def trends_tab() -> None:
    """Where the cross-asset anchors have been — the committed metrics timeline as charts."""
    df = get_timeline_df()
    if df.empty or len(df) < 5 or not isinstance(df.index, pd.DatetimeIndex):
        st.info("The metrics timeline is still accumulating — trend charts appear once a few "
                "sessions exist. Seed ~3 years of real history with `python -m src.backfill`.")
        return
    st.caption(f"{len(df)} sessions · {df.index[0].date()} → {df.index[-1].date()} — each anchor's "
               "path, with today's percentile over the whole window. Faint red = crisis eras "
               "(dotcom · GFC · Euro debt · COVID · the 2022 inflation shock).")
    cols = st.columns(2)
    for i, (col, title) in enumerate(TREND_METRICS):
        if col not in df.columns:
            continue
        series = df[col].dropna()
        if len(series) < 5:                        # skip a thinly-populated metric (no n=1 charts)
            continue
        with cols[i % 2]:
            latest = float(series.iloc[-1])
            pct = round(float((series < latest).mean()) * 100)
            st.markdown(f"**{title}** — {latest:,.2f}  ·  {pct}th %ile of {len(series)} sessions")
            st.plotly_chart(trend_fig(series), use_container_width=True,
                            theme="streamlit", key=f"trend_{col}")
    _time_machine(df)
    _crisis_signal_panel(df)
    _analogue_panel(df)
    _tearsheet_panel(df)
