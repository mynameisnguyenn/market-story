"""Global & Macro tab — read-first: the risk view (regime, stress & danger, drawdown,
vol premium, extremes, correlations), then market tables, then the macro data archives."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src import (bls_data, composite, config, eia_data, pmi_proxy, regime, regime_turbulence,
                 riskmetrics, statistical)
from src.dashboard.charts import (color_changes, bls_styler, correlation_fig, energy_styler,
                                  extremes_styler, level_fig, macro_styler, positioning_styler,
                                  yield_curve_fig)
from src.dashboard.data import get_bls_history, get_energy_history, get_fred_history
from src.dashboard.widgets import tone_span, render_line, render_table

# Curated cross-asset set for the correlation matrix (all in config.all_symbols()).
CORR_INSTRUMENTS = [
    ("^GSPC", "S&P"), ("^IXIC", "Nasdaq"), ("^RUT", "Russell"),
    ("^TNX", "10Y"), ("DX-Y.NYB", "Dollar"), ("GC=F", "Gold"),
    ("CL=F", "WTI"), ("HYG", "HY Credit"), ("^VIX", "VIX"),
]

_RISK_ASSETS = [("^GSPC", "S&P 500"), ("^IXIC", "Nasdaq"), ("GC=F", "Gold"),
                ("CL=F", "WTI"), ("HG=F", "Copper"), ("DX-Y.NYB", "Dollar")]


def regime_panel(brief: dict) -> None:
    """A quick risk-on/off read derived from the macro (FRED) series."""
    signals = regime.assess(brief.get("macro", []), vix=brief.get("stats", {}).get("vix"))
    if not signals:
        return
    st.subheader(f"Risk regime — {regime.overall(signals)}")
    tone_map = {"on": "up", "off": "down", "neutral": "neutral"}
    cols = st.columns(len(signals))
    for col, s in zip(cols, signals):
        col.caption(s["label"])
        col.markdown(tone_span(s["reading"], tone_map.get(s["tone"], "neutral")), unsafe_allow_html=True)
    st.divider()


def _risk_drawdown_panel(closes: dict) -> None:
    """Per-asset risk over the embedded ~1y history (riskmetrics): drawdown, ulcer, sortino, tail."""
    rows = []
    for sym, name in _RISK_ASSETS:
        p = closes.get(sym)
        if p is None or len(pd.Series(p).dropna()) < 30:
            continue
        rets = riskmetrics.returns(p)
        lb = riskmetrics.lookback_returns(p) or {}
        md = riskmetrics.max_drawdown(p)
        cd = riskmetrics.current_drawdown(p)
        rows.append({
            "Asset": name,
            "1Y %": (lb.get("1Y") * 100) if lb.get("1Y") is not None else None,
            "Max DD %": (md * 100) if md is not None else None,
            "Cur DD %": (cd[0] * 100) if cd else None,
            "DD days": cd[1] if cd else None,
            "Ulcer": riskmetrics.ulcer_index(p),
            "Sortino": riskmetrics.sortino(rets),
            "Tail": riskmetrics.tail_ratio(rets),
            "Trend": (statistical.summary(rets) or {}).get("regime", "—"),
        })
    if not rows:
        return
    st.subheader("Risk & drawdown")
    st.caption("Per-asset over the embedded ~1y history — drawdown depth/duration, ulcer index, "
               "sortino, tail ratio. Source: riskmetrics (ffn/empyrical-style).")
    frame = pd.DataFrame(rows)
    st.dataframe(
        frame.style.format({"1Y %": "{:+.1f}", "Max DD %": "{:.1f}", "Cur DD %": "{:.1f}",
                            "Ulcer": "{:.1f}", "Sortino": "{:+.2f}", "Tail": "{:.2f}"}, na_rep="—")
        .map(color_changes, subset=["1Y %", "Sortino"]),
        use_container_width=True, hide_index=True)


def _stress_danger_panel(brief: dict, closes: dict) -> None:
    """Composite risk regime + Kritzman turbulence stress gauge (composite + regime_turbulence)."""
    dg = composite.evaluate(brief)
    ts = regime_turbulence.from_closes(closes)
    cols = st.columns(3)
    # Count of firing risk-off conditions (NOT a competing 'regime' label — that's regime_panel above).
    cols[0].metric("Risk-off signals", f"{dg['score']} firing", delta_color="off")
    if ts and ts.get("stress_pct") is not None:
        cols[1].metric("Market stress", f"{ts['stress_pct'] * 100:.0f}th %ile",
                       f"turbulence {ts['turbulence']:.1f}", delta_color="off")
    if dg.get("danger"):                                   # red delta = unmissable on a risk desk
        cols[2].metric("Danger flag", "⚠ DANGER", delta="risk-off", delta_color="inverse")
    else:
        cols[2].metric("Danger flag", "clear", delta="calm", delta_color="off")
    firing = [c["detail"] for c in dg.get("conditions", []) if c.get("on")]
    if firing:
        st.caption("Risk-off conditions firing: " + " · ".join(firing))
    st.caption("Market stress is **descriptive, not predictive**: it measures how unusual today's "
               "cross-asset moves are vs their own history — a thermometer, not a forecast. The 28-year "
               "backtest found turbulence has no edge on forward S&P returns (`research/signal-validation.md`).")
    st.divider()


def _archive_series(fred_rows: list[dict], sid: str):
    """A FRED series from the committed macro archive as a date-indexed pd.Series, or None."""
    obs = sorted((r["date"], r["value"]) for r in fred_rows if r.get("series") == sid)
    if len(obs) < 13:
        return None
    return pd.Series([v for _, v in obs], index=pd.to_datetime([d for d, _ in obs]))


def _growth_pulse_panel() -> None:
    """PMI-like real-activity diffusion proxy (pmi_proxy) from the committed FRED archive —
    industrial production + payrolls + (inverted) jobless claims, no new external feed."""
    rows = get_fred_history()
    if not rows:
        return
    comps = {}
    for sid, label in [("INDPRO", "Industrial production"), ("PAYEMS", "Payrolls"),
                       ("ICSA", "Initial claims")]:
        s = _archive_series(rows, sid)
        if s is not None:
            comps[label] = s
    latest, series = pmi_proxy.composite_index(comps, invert={"Initial claims"})
    if latest is None or series is None or len(series) < 6:
        return
    st.subheader("Growth pulse — real-activity diffusion (PMI proxy)")
    st.metric("Diffusion index", f"{latest:.1f}",
              f"{'expansion' if latest >= 50 else 'contraction'} ({latest - 50:+.1f} vs 50)",
              delta_color="normal" if latest >= 50 else "inverse")
    fig = level_fig(series)
    fig.add_hline(y=50, line=dict(color="#7beafb", width=1, dash="dot"), opacity=0.4)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", key="pmi_pulse")
    st.caption("Momentum of industrial production + payrolls + (inverted) initial claims, each "
               "normalized by its own 12-month volatility and mapped to a 0–100 diffusion scale: "
               ">50 = real activity accelerating, <50 = decelerating. A free-data ISM-PMI analog "
               "(ISM's own index is license-restricted off FRED), not the official print. Source: pmi_proxy.")
    st.divider()


def _energy_history_section() -> None:
    """Full weekly inventory history from the committed archive (petroleum back to 1982)."""
    hist = get_energy_history()
    if not hist:
        return
    names = {sid: name for _route, sid, name in eia_data.EIA_SERIES}
    with st.expander("📈 Inventory history — full weekly record (petroleum back to 1982)"):
        sid = st.selectbox("Series", list(names), format_func=lambda s: names.get(s, s),
                           key="energy_hist_sel")
        rows = [r for r in hist if r.get("series") == sid]
        if len(rows) < 5:
            st.caption("Not enough history for this series yet.")
            return
        idx = pd.to_datetime([r["date"] for r in rows])
        s = pd.Series([r["value"] for r in rows], index=idx).sort_index()
        units = rows[-1].get("units") or ""
        latest = float(s.iloc[-1])
        pct = round(float((s < latest).mean()) * 100)
        prior_yr = s[s.index <= s.index[-1] - pd.Timedelta(days=365)]
        line = (f"{names[sid]} · {len(s):,} weeks · {s.index[0].date()} → {s.index[-1].date()} · "
                f"latest {latest:,.0f} {units} · {pct}ᵗʰ %ile of the whole record")
        if len(prior_yr):
            line += f" · {latest - float(prior_yr.iloc[-1]):+,.0f} {units} YoY"
        st.caption(line)
        st.plotly_chart(level_fig(s), use_container_width=True, theme="streamlit", key=f"enh_{sid}")
        st.caption("Inventory *levels* (not the weekly draw/build). Faint red = crisis eras. "
                   "The SPR drawdown since 2022 and the gasoline/distillate seasonal saw-tooth are "
                   "visible here. Source: EIA, committed archive `data/history/energy.jsonl`.")


def _macro_history_section() -> None:
    """Deep history for any FRED or BLS series, straight from the committed archives —
    the same data the daily panels show, but back to inception (CPI/jobs to the 1940s,
    Treasury yields to the 1960s). The finance-history learning system reads from here too."""
    fred_rows, bls_rows = get_fred_history(), get_bls_history()
    fred_have = {r["series"] for r in fred_rows}
    bls_have = {r["series"] for r in bls_rows}
    options = {sid: f"{name}  ·  FRED {sid}" for sid, name in config.FRED_SERIES if sid in fred_have}
    options.update({sid: f"{name}  ·  BLS {sid}" for sid, name in bls_data.BLS_SERIES if sid in bls_have})
    if not options:
        return
    with st.expander("📈 Macro & labor history — full record (yields to the 1960s, CPI/jobs to the 1940s)"):
        sid = st.selectbox("Series", list(options), format_func=lambda s: options[s], key="macro_hist_sel")
        source = bls_rows if sid in bls_have else fred_rows
        rows = [r for r in source if r.get("series") == sid]
        if len(rows) < 5:
            st.caption("Not enough history for this series yet.")
            return
        s = pd.Series([r["value"] for r in rows],
                      index=pd.to_datetime([r["date"] for r in rows])).sort_index()
        latest = float(s.iloc[-1])
        pct = round(float((s < latest).mean()) * 100)
        st.caption(f"{options[sid]} · {len(s):,} obs · {s.index[0].date()} → {s.index[-1].date()} · "
                   f"latest {latest:,.2f} · {pct}ᵗʰ %ile of the whole record")
        st.plotly_chart(level_fig(s), use_container_width=True, theme="streamlit", key=f"mh_{sid}")
        st.caption("Faint red = crisis eras (dotcom · GFC · Euro debt · COVID · 2022 inflation shock). "
                   "Source: committed archives `data/history/macro.jsonl` + `labor.jsonl`.")


def macro_tab(brief: dict, closes: dict) -> None:
    # --- Risk view first: the read (regime, stress, drawdown, vol, extremes, correlations) ---
    regime_panel(brief)
    _stress_danger_panel(brief, closes)
    _risk_drawdown_panel(closes)
    vol = brief.get("vol")
    if vol:
        tag = "rich — protection expensive vs realized" if vol["premium"] > 3 \
            else "compressed — realized catching up to implied" if vol["premium"] < 0 else "normal"
        st.caption(f"Vol risk premium: VIX {vol['vix']} vs {vol['realized_20d']} realized (20d) "
                   f"= {vol['premium']:+.1f} pts ({tag}).")
    if brief.get("extremes"):
        st.subheader("Cross-asset extremes")
        st.caption("Where key markets sit in their ~1y range")
        st.dataframe(extremes_styler(brief["extremes"]), use_container_width=True, hide_index=True)
    corr = correlation_fig(closes, CORR_INSTRUMENTS)
    if corr is not None:
        st.plotly_chart(corr, use_container_width=True, theme="streamlit", key="corr_matrix")
        st.caption("Daily-return correlation, last 60 sessions. Watch for regime shifts "
                   "(e.g. stock–bond decoupling, or everything → +1 in a selloff).")
    st.divider()
    # --- Markets: the tables + the rates/FX charts ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Global Indices")
        render_table(brief["markets"].get("global_indices", []), "equity", "% changes")
        st.subheader("Rates (Treasury yields)")
        render_table(brief["markets"].get("rates", []), "yield", "Last in %, 1D in bps")
        st.subheader("FX")
        render_table(brief["markets"].get("fx", []), "fx", "% changes")
    with col2:
        st.subheader("Commodities")
        render_table(brief["markets"].get("commodities", []), "commodity", "% changes")
        st.subheader("Credit & Bonds")
        render_table(brief["markets"].get("credit", []), "credit", "% changes")
    curve = yield_curve_fig(brief["markets"].get("rates", []))
    if curve is not None:
        st.plotly_chart(curve, use_container_width=True, theme="streamlit", key="yield_curve")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("US 10Y Yield")
        render_line(closes, "^TNX", "US 10Y Yield", key="mac_tnx")
    with col4:
        st.subheader("US Dollar Index")
        render_line(closes, "DX-Y.NYB", "US Dollar Index", key="mac_dxy")
    st.divider()
    # --- Macro & data: growth pulse, FRED, BLS, energy, positioning (+ deep-history expanders) ---
    _growth_pulse_panel()
    st.subheader("Macro (FRED)")
    if brief.get("macro"):
        st.dataframe(macro_styler(brief["macro"]), use_container_width=True, hide_index=True)
    if brief.get("bls"):
        st.subheader("Labor & Inflation (BLS)")
        st.caption("Release-day prints, YoY %")
        st.dataframe(bls_styler(brief["bls"]), use_container_width=True, hide_index=True)
    _macro_history_section()
    if brief.get("energy"):
        st.subheader("Energy inventories (EIA, weekly)")
        st.caption("Δ is the week-over-week draw/build")
        st.dataframe(energy_styler(brief["energy"]), use_container_width=True, hide_index=True)
        st.caption("A crude **draw** (negative Δ) is typically bullish for oil, a build bearish; "
                   "natural gas swings between summer injections and winter withdrawals. Source: EIA.")
        _energy_history_section()
    if brief.get("positioning"):
        st.subheader("Speculative positioning (CFTC, weekly)")
        st.caption("Leveraged-fund net & weekly change")
        st.dataframe(positioning_styler(brief["positioning"]), use_container_width=True, hide_index=True)
        st.caption("Leveraged funds = hedge-fund/spec money; asset managers = real money. A large "
                   "spec net-short with real money long is a classic squeeze setup. Source: CFTC TFF.")
