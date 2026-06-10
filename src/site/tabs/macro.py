"""Global & Macro tab (static) — read-first: regime, stress & danger, risk & drawdown, the
growth/inflation pulse, the proxy-book stress table, then the market tables + rates/FX charts,
then the deep-history archive expanders. Faithful port of src.dashboard.panels.macro.

Contract: section(ctx) -> str. ctx.brief (dict), ctx.closes ({symbol: Series}), ctx.tl (timeline
DataFrame or None). No Streamlit, no network — every sub-panel degrades to '' rather than raise.
"""
from __future__ import annotations

import pandas as pd

from src import (bls_data, composite, config, eia_data, pmi_proxy, proxy_books, regime,
                 regime_turbulence, riskmetrics, statistical)
from src.dashboard import charts

from ..render import (caption, details, fig_html, grid, kpi_card, panel, styler_html)

# Curated cross-asset set for the correlation matrix (all in config.all_symbols()).
CORR_INSTRUMENTS = [
    ("^GSPC", "S&P"), ("^IXIC", "Nasdaq"), ("^RUT", "Russell"),
    ("^TNX", "10Y"), ("DX-Y.NYB", "Dollar"), ("GC=F", "Gold"),
    ("CL=F", "WTI"), ("HYG", "HY Credit"), ("^VIX", "VIX"),
]

_RISK_ASSETS = [("^GSPC", "S&P 500"), ("^IXIC", "Nasdaq"), ("GC=F", "Gold"),
                ("CL=F", "WTI"), ("HG=F", "Copper"), ("DX-Y.NYB", "Dollar")]


def _regime(ctx) -> str:
    """Risk regime read (FRED signals) + composite danger + Kritzman turbulence stress gauge."""
    brief, closes = ctx.brief, ctx.closes
    out = []
    signals = regime.assess(brief.get("macro", []), vix=(brief.get("stats") or {}).get("vix"))
    if signals:
        tone_map = {"on": "up", "off": "down", "neutral": "flat"}
        cards = [kpi_card(s["label"], s["reading"], tone=tone_map.get(s["tone"], "flat"))
                 for s in signals]
        out.append(panel(f"Risk regime — {regime.overall(signals)}", grid(cards)))
    out.append(_stress_danger(brief, closes))
    return "".join(p for p in out if p)


def _stress_danger(brief: dict, closes: dict) -> str:
    """Composite risk-off count + Kritzman turbulence stress gauge + the danger flag."""
    try:
        dg = composite.evaluate(brief)
    except Exception:
        return ""
    ts = regime_turbulence.from_closes(closes) or {}
    have_stress = ts.get("stress_pct") is not None
    cards = [kpi_card("Risk-off signals", f"{dg['score']} firing", tone="flat")]
    if have_stress:
        cards.append(kpi_card("Market stress", f"{ts['stress_pct'] * 100:.0f}th %ile",
                              f"turbulence {ts['turbulence']:.1f}", tone="flat"))
    if dg.get("danger"):
        cards.append(kpi_card("Danger flag", "DANGER", "risk-off", tone="down"))
    else:
        cards.append(kpi_card("Danger flag", "clear", "calm", tone="flat"))
    body = grid(cards)
    firing = [c["detail"] for c in dg.get("conditions", []) if c.get("on")]
    if firing:
        body += caption("Risk-off conditions firing: " + " · ".join(firing))
    body += caption("Market stress is descriptive, not predictive: it measures how unusual today's "
                    "cross-asset moves are vs their own history — a thermometer, not a forecast. The "
                    "28-year backtest found turbulence has no edge on forward S&P returns "
                    "(research/signal-validation.md).")
    return panel("Stress & danger", body)


def _risk(ctx) -> str:
    """Per-asset risk over the embedded ~1y history (riskmetrics): drawdown, ulcer, sortino, tail."""
    rows = []
    for sym, name in _RISK_ASSETS:
        p = ctx.closes.get(sym)
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
        return ""
    styler = (pd.DataFrame(rows).style
              .format({"1Y %": "{:+.1f}", "Max DD %": "{:.1f}", "Cur DD %": "{:.1f}",
                       "DD days": "{:.0f}", "Ulcer": "{:.1f}", "Sortino": "{:+.2f}",
                       "Tail": "{:.2f}"}, na_rep="—")
              .map(charts.color_changes, subset=["1Y %", "Sortino"]))
    sub = ("Per-asset over the embedded ~1y history — drawdown depth/duration, ulcer index, "
           "sortino, tail ratio. Source: riskmetrics (ffn/empyrical-style).")
    return panel("Risk & drawdown", styler_html(styler), sub=sub)


def _proxy_books(ctx) -> str:
    """Illustrative proxy-book stress — diversified vs pure equities across past crises."""
    try:
        rows = [r for r in proxy_books.stress_books(ctx.tl) if r.get("n_days")]
    except Exception:
        return ""
    if not rows:
        return ""
    frame = pd.DataFrame([
        {"Book": r.get("book"), "Window": r.get("window"), "Days": r.get("n_days"),
         "Return": f"{r['return_pct']:+.1f}%" if r.get("return_pct") is not None else "—",
         "Max DD": f"{r['max_drawdown_pct']:.1f}%" if r.get("max_drawdown_pct") is not None else "—"}
        for r in rows])
    body = styler_html(frame.style)
    body += caption("Illustrative approximation: the bond leg is −8 × Δ(10Y yield) — an explicit "
                    "duration constant, not a bond index; no credit leg (HY OAS history starts 2023, "
                    "zero coverage of these windows). Answers the one question the Crisis replay "
                    "doesn't: what did a diversified book do in each episode. Not investment analysis.")
    return details("🧪 Proxy-book stress — diversified vs pure equities (illustrative)", body)


def _archive_series(fred_rows: list[dict], sid: str):
    """A FRED series from the committed macro archive as a date-indexed pd.Series, or None."""
    obs = sorted((r["date"], r["value"]) for r in fred_rows if r.get("series") == sid)
    if len(obs) < 13:
        return None
    return pd.Series([v for _, v in obs], index=pd.to_datetime([d for d, _ in obs]))


def _growth(ctx) -> str:
    """Growth + inflation momentum diffusions (pmi_proxy) from the committed FRED archive."""
    try:
        rows = macro_data_load_fred()
    except Exception:
        return ""
    if not rows:
        return ""
    comps = {}
    for sid, label in [("INDPRO", "Industrial production"), ("PAYEMS", "Payrolls"),
                       ("ICSA", "Initial claims")]:
        s = _archive_series(rows, sid)
        if s is not None:
            comps[label] = s
    latest, series = pmi_proxy.composite_index(comps, invert={"Initial claims"})
    if latest is None or series is None or len(series) < 6:
        return ""
    cards = [_growth_card("Growth", latest, series, accel_word=("expansion", "contraction"))]
    cpi = _archive_series(rows, "CPIAUCSL")
    inf_latest, inf_series = (pmi_proxy.composite_index({"CPI": cpi})
                              if cpi is not None else (None, None))
    if inf_latest is not None and inf_series is not None:
        cards.append(_growth_card("Inflation", inf_latest, inf_series,
                                  accel_word=("accelerating", "decelerating")))
    fig = charts.level_fig(series)
    fig.add_hline(y=50, line=dict(color="#7beafb", width=1, dash="dot"), opacity=0.4)
    body = grid(cards) + fig_html(fig)
    body += caption("Growth = momentum of industrial production + payrolls + (inverted) initial "
                    "claims; inflation = CPI momentum — each normalized by its own 12-month "
                    "volatility onto a 0–100 diffusion scale (>50 = accelerating). Chart shows the "
                    "growth composite. Momentum readings, not forecasts, and the two metrics "
                    "reference different data months (release lags differ). A free-data ISM-PMI "
                    "analog, not the official print. Source: pmi_proxy.")
    return panel("Growth & inflation pulse — momentum diffusions (PMI proxy)", body)


def _growth_card(label: str, latest: float, series, *, accel_word: tuple[str, str]) -> str:
    """One pulse KPI: 'Growth (through Apr 2026)' with a >50/<50 acceleration delta."""
    up, down = accel_word
    word = up if latest >= 50 else down
    title = f"{label} (through {series.index[-1]:%b %Y})"
    delta = f"{word} ({latest - 50:+.1f} vs 50)"
    return kpi_card(title, f"{latest:.1f}", delta, tone=("up" if latest >= 50 else "down"))


def _tables(ctx) -> str:
    """The market tables (indices/rates/FX/commodities/credit), vol premium, extremes,
    correlation matrix, yield curve, and the 10Y/DXY level charts."""
    brief, closes = ctx.brief, ctx.closes
    markets = brief.get("markets") or {}
    out = []
    out.append(_vol_premium(brief))
    if brief.get("extremes"):
        body = styler_html(charts.extremes_styler(brief["extremes"]))
        out.append(panel("Cross-asset extremes", body, sub="Where key markets sit in their ~1y range"))
    corr = charts.correlation_fig(closes, CORR_INSTRUMENTS)
    if corr is not None:
        body = fig_html(corr) + caption(
            "Daily-return correlation, last 60 sessions. Watch for regime shifts "
            "(e.g. stock–bond decoupling, or everything → +1 in a selloff).")
        out.append(panel("Cross-asset correlations", body))
    out.append(_market_tables(markets))
    out.append(panel("US Treasury yield curve",
                     fig_html(charts.yield_curve_fig(markets.get("rates", [])))))
    out.append(panel("US 10Y Yield", fig_html(charts.line_fig(closes.get("^TNX"), "US 10Y Yield"))))
    out.append(panel("US Dollar Index",
                     fig_html(charts.line_fig(closes.get("DX-Y.NYB"), "US Dollar Index"))))
    return "".join(p for p in out if p)


def _vol_premium(brief: dict) -> str:
    """The vol risk premium caption — VIX vs realized (20d)."""
    vol = brief.get("vol") or {}
    prem = vol.get("premium")
    if prem is None:
        return ""
    tag = "rich — protection expensive vs realized" if prem > 3 \
        else "compressed — realized catching up to implied" if prem < 0 else "normal"
    return caption(f"Vol risk premium: VIX {vol.get('vix')} vs {vol.get('realized_20d')} realized "
                   f"(20d) = {prem:+.1f} pts ({tag}).")


def _market_tables(markets: dict) -> str:
    """The five market group tables, each a section_styler -> styled HTML table."""
    groups = [("Global Indices", "global_indices", "equity", "% changes"),
              ("Rates (Treasury yields)", "rates", "yield", "Last in %, 1D in bps"),
              ("FX", "fx", "fx", "% changes"),
              ("Commodities", "commodities", "commodity", "% changes"),
              ("Credit & Bonds", "credit", "credit", "% changes")]
    out = []
    for title, key, kind, sub in groups:
        rows = markets.get(key, [])
        if not rows:
            continue
        out.append(panel(title, styler_html(charts.section_styler(rows, kind)), sub=sub))
    return "".join(out)


def _tables_macro_data(ctx) -> str:
    """FRED, BLS, energy, and positioning snapshot tables with their honesty captions."""
    brief = ctx.brief
    out = []
    if brief.get("macro"):
        out.append(panel("Macro (FRED)", styler_html(charts.macro_styler(brief["macro"]))))
    if brief.get("bls"):
        out.append(panel("Labor & Inflation (BLS)", styler_html(charts.bls_styler(brief["bls"])),
                         sub="Release-day prints, YoY %"))
    out.append(_macro_history())
    if brief.get("energy"):
        body = styler_html(charts.energy_styler(brief["energy"]))
        body += caption("A crude draw (negative Δ) is typically bullish for oil, a build bearish; "
                        "natural gas swings between summer injections and winter withdrawals. "
                        "Source: EIA.")
        body += _energy_history()
        out.append(panel("Energy inventories (EIA, weekly)", body,
                         sub="Δ is the week-over-week draw/build"))
    if brief.get("positioning"):
        body = styler_html(charts.positioning_styler(brief["positioning"]))
        body += caption("Leveraged funds = hedge-fund/spec money; asset managers = real money. A "
                        "large spec net-short with real money long is a classic squeeze setup. "
                        "Source: CFTC TFF.")
        out.append(panel("Speculative positioning (CFTC, weekly)", body,
                         sub="Leveraged-fund net & weekly change"))
    return "".join(p for p in out if p)


def _series_from_archive(rows: list[dict], sid: str):
    """Date-indexed Series for one archive series id (oldest-first), or None if too short."""
    obs = [(r["date"], r["value"]) for r in rows if r.get("series") == sid and r.get("value") is not None]
    if len(obs) < 5:
        return None
    s = pd.Series([v for _, v in obs], index=pd.to_datetime([d for d, _ in obs])).sort_index()
    return s


def _archive_chart(s, label: str, *, units: str = "", value_spec: str = ",.2f") -> str:
    """A level_fig + percentile caption for one archived series, stacked inside a <details>."""
    latest = float(s.iloc[-1])
    pct = round(float((s < latest).mean()) * 100)
    line = (f"{label} · {len(s):,} obs · {s.index[0].date()} → {s.index[-1].date()} · "
            f"latest {format(latest, value_spec)} {units} · {pct}ᵗʰ %ile of the whole record")
    return caption(line.strip()) + fig_html(charts.level_fig(s))


def _macro_history() -> str:
    """Deep FRED/BLS history — the 2-3 headline series stacked (the live picker is dev-only)."""
    try:
        fred_rows, bls_rows = macro_data_load_fred(), bls_data.load_bls_history()
    except Exception:
        return ""
    fred_names = dict(config.FRED_SERIES)
    body = ""
    for sid in ("DGS10", "CPIAUCSL", "UNRATE"):
        s = _series_from_archive(fred_rows, sid)
        if s is not None:
            body += _archive_chart(s, f"{fred_names.get(sid, sid)}  ·  FRED {sid}")
    if not body and bls_rows:
        for sid, name in bls_data.BLS_SERIES[:2]:
            s = _series_from_archive(bls_rows, sid)
            if s is not None:
                body += _archive_chart(s, f"{name}  ·  BLS {sid}")
    if not body:
        return ""
    body += caption("Faint red = crisis eras (dotcom · GFC · Euro debt · COVID · 2022 inflation "
                    "shock). Source: committed archives data/history/macro.jsonl + labor.jsonl. The "
                    "full interactive series picker (yields to the 1960s, CPI/jobs to the 1940s) "
                    "lives in the dev app.")
    return details("📈 Macro & labor history — headline series (full picker in the dev app)", body)


def _energy_history() -> str:
    """Full weekly inventory history — the headline crude series (live picker is dev-only)."""
    try:
        hist = eia_data.load_history()
    except Exception:
        return ""
    if not hist:
        return ""
    names = {sid: name for _route, sid, name in eia_data.EIA_SERIES}
    body = ""
    for sid in ("WCESTUS1", "NW2_EPG0_SWO_R48_BCF"):
        s = _series_from_archive(hist, sid)
        if s is None:
            continue
        units = next((r.get("units") or "" for r in reversed(hist) if r.get("series") == sid), "")
        body += _archive_chart(s, names.get(sid, sid), units=units, value_spec=",.0f")
    if not body:
        return ""
    body += caption("Inventory levels (not the weekly draw/build). Faint red = crisis eras. The SPR "
                    "drawdown since 2022 and the gasoline/distillate seasonal saw-tooth are visible "
                    "here. Source: EIA, committed archive data/history/energy.jsonl. The full "
                    "per-series picker lives in the dev app.")
    return details("📈 Inventory history — full weekly record (petroleum back to 1982)", body)


def macro_data_load_fred() -> list[dict]:
    """The committed FRED history archive (data/history/macro.jsonl). Local import keeps the
    module load cheap and avoids a hard dependency at import time."""
    from src import macro_data
    return macro_data.load_fred_history()


def _archives(ctx) -> str:
    """Macro-data snapshot tables (FRED/BLS/energy/positioning) + the deep-history expanders."""
    return _tables_macro_data(ctx)


def section(ctx) -> str:
    """Assemble the Global & Macro tab — risk view first, then markets, then the data archives."""
    parts = [
        _regime(ctx),
        _risk(ctx),
        _proxy_books(ctx),
        _tables(ctx),
        _growth(ctx),
        _archives(ctx),
    ]
    return "".join(p for p in parts if p)
