"""Trends tab — the committed cross-asset metrics timeline as charts, a static time
machine, crisis-window replay, signal Information Coefficient, VIX-episode analogues,
and a quantstats-style tearsheet. Mirrors src/dashboard/panels/trends.py (no Streamlit)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from src import analogues, crisis, eras, riskmetrics, signal_ic
from src.dashboard import charts

from ..render import caption, details, esc, panel, fig_html, md_html, styler_html

_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

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

# Static lookbacks for the time machine (interactive slider isn't available on a static page).
_LOOKBACK_WEEKS = [4, 13, 26, 52]


def _fmt2(x) -> str:
    return f"{x:.2f}" if x is not None else "—"


def _trend_charts(df) -> str:
    """Per-metric trend charts (charts.trend_fig) in a 2-col grid; each titled with the
    metric label + today's percentile over the whole window."""
    cards = []
    for col, title in TREND_METRICS:
        if col not in df.columns:
            continue
        series = df[col].dropna()
        if len(series) < 5:                        # skip a thinly-populated metric (no n=1 charts)
            continue
        latest = float(series.iloc[-1])
        pct = round(float((series < latest).mean()) * 100)
        fig = fig_html(charts.trend_fig(series))
        if not fig:
            continue
        head = (f'<div class="cap">{esc(title)} — {latest:,.2f} · '
                f'{pct}th %ile of {len(series)} sessions</div>')
        cards.append(f'<div>{head}{fig}</div>')
    if not cards:
        return ""
    sub = ("each anchor's path, with today's percentile over the whole window. Faint red = "
           "crisis eras (dotcom · GFC · Euro debt · COVID · the 2022 inflation shock).")
    return panel("Cross-asset anchors", f'<div class="grid grid-2">{"".join(cards)}</div>', sub=sub)


def _time_machine(df) -> str:
    """Static 'where were we ~N weeks ago' table for a few fixed lookbacks (4/13/26/52 wk):
    the era each falls in + every metric's level AS OF that date vs its own history to then."""
    rows = []
    for weeks in _LOOKBACK_WEEKS:
        pos = len(df) - 1 - weeks * 5             # ≈5 trading rows/week
        if pos < 0:
            continue
        as_of = df.index[pos]
        upto = df.iloc[: pos + 1]
        era = eras.era_for(as_of.date().isoformat())
        row = {"As of": as_of.date().isoformat(), "Era": (era or {}).get("name", "—")}
        for col, label in TREND_METRICS:
            if col not in upto.columns:
                continue
            series = upto[col].dropna()
            if len(series) < 5:
                continue
            val = float(series.iloc[-1])
            pct = round(float((series < val).mean()) * 100)
            row[label] = f"{val:,.2f} ({pct}%)"
        rows.append(row)
    if not rows:
        return ""
    table = pd.DataFrame(rows)
    body = styler_html(table.style)
    sub = ("Where markets stood ~4/13/26/52 weeks back, and which era it was; each cell is the "
           "level then with its percentile (history to that date). Static lookbacks stand in for "
           "the dashboard's interactive date picker.")
    return panel("🕰 Time machine", body, sub=sub)


def _crisis_replay(df, spx_rets) -> str:
    """Crisis-window replay — how the S&P behaved in each past stress window."""
    rep = [r for r in crisis.crisis_replay(spx_rets) if r.get("n_days")]
    if not rep:
        return ""
    cr = pd.DataFrame([{
        "Episode": r["name"],
        "Return %": (r["return"] * 100) if r["return"] is not None else None,
        "Max DD %": (r["max_drawdown"] * 100) if r["max_drawdown"] is not None else None,
        "VaR95 %": (r["var95"] * 100) if r["var95"] is not None else None,
        "ES95 %": (r["es95"] * 100) if r["es95"] is not None else None,
    } for r in rep])
    body = styler_html(
        cr.style.format({"Return %": "{:+.1f}", "Max DD %": "{:.1f}",
                         "VaR95 %": "{:.2f}", "ES95 %": "{:.2f}"}, na_rep="—")
        .map(charts.color_changes, subset=["Return %"]))
    sub = "How the S&P behaved in each episode, from the committed timeline. Source: crisis."
    return panel("Crisis replay — S&P through past stress windows", body, sub=sub)


def _signal_ic(df, spx) -> str:
    """Signal edge — live Information Coefficient with the 28y backtest verdict column."""
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
    if not ic_rows:
        return ""
    body = styler_html(pd.DataFrame(ic_rows).style.format(
        {"IC 1d": "{:+.3f}", "IC 5d": "{:+.3f}", "IC 21d": "{:+.3f}", "n": "{:,d}"}, na_rep="—")
        .map(charts.color_changes, subset=["IC 1d", "IC 5d", "IC 21d"]))
    sub = ("Live rank correlation of each signal with forward S&P returns. The Edge column is the "
           "verdict from the full 28-year block-bootstrap backtest (research/signal-validation.md): "
           "only VIX level shows a robust, regime-stable edge (high fear → higher forward returns); "
           "the 2s10s curve and vol premium don't predict; HY OAS rests on a ~3y sample. Read the "
           "live IC against that verdict, not on its own. n = overlapping observations. Source: "
           "signal_ic.")
    out = panel("Signal edge — Information Coefficient", body, sub=sub)
    if hy_oas_short:
        out += caption("⚠ HY OAS history is FRED-license-limited to a ~3y trailing window, so its IC "
                       "rests on a smaller sample than the others — read it as indicative, not settled.")
    return out


def _crisis_signal_panel(df) -> str:
    """Crisis-window replay + signal Information Coefficient over the committed timeline."""
    if df is None or df.empty or "spx" not in df.columns:
        return ""
    spx = pd.to_numeric(df["spx"], errors="coerce").dropna()
    if len(spx) < 60:
        return ""
    spx_rets = spx.pct_change().dropna()
    return _crisis_replay(df, spx_rets) + _signal_ic(df, spx)


def _analogue_panel(df) -> str:
    """VIX-episode analogues: the historical days whose VIX percentile most resembles today's,
    and where fear went next. Anchored on the ONE validated signal (VIX level); deliberately
    shows NO forward S&P returns (see research/signal-validation.md)."""
    try:
        eps = analogues.vix_episodes(df)
    except Exception:
        return ""
    if not eps:
        return ""
    s = analogues.episodes_summary(eps)
    today_pct = analogues.today_vix_pct(df)
    parts = []
    known = s["n"] - s["unresolved"]
    if known > 0:
        parts.append(md_html(f"**Fear resolved lower within 21 sessions in {s['resolved_lower']} "
                             f"of {known} comparable episodes.**"))
    table = pd.DataFrame([
        {"Date": e.get("date"), "Era": (e.get("era") or {}).get("name", "—"),
         "VIX": _fmt2(e.get("vix")), "%ile": _fmt2(e.get("vix_pct")),
         "VIX +5d": _fmt2(e.get("vix_5d")), "VIX +21d": _fmt2(e.get("vix_21d")),
         "Resolved lower": {True: "✓", False: "✗"}.get(e.get("resolved"), "…")}
        for e in eps])
    parts.append(styler_html(table.style))
    # The "buy fear" edge only applies in a HIGH-VIX regime. These analogues match today's
    # percentile, so when today is calm the matched days are calm too — cite the edge only then.
    if today_pct is not None and today_pct >= 70:
        edge = (" The 28y study's one validated read applies here: with VIX elevated, fear has "
                "historically preceded higher forward returns (gross of costs).")
    else:
        edge = (" Today's VIX sits mid/low in its history, so these are calmer-regime analogues; "
                "the validated buy-fear edge applies only when VIX is elevated — here this is "
                "context, not a signal.")
    parts.append(caption("Matched on full-history VIX percentile, episode-deduped (≥21 sessions "
                         "apart), most-recent quarter excluded. Descriptive memory of where fear "
                         "went next — not a return forecast." + edge))
    body = "".join(p for p in parts if p)
    return details("🌀 Days like today — VIX-percentile analogues", body)


def _tearsheet_metrics(spx, rets) -> str:
    """Risk-adjusted headline KPIs row for the tearsheet."""
    yrs = len(spx) / 252.0
    cagr = ((spx.iloc[-1] / spx.iloc[0]) ** (1 / yrs) - 1) * 100 if yrs > 0 else None
    vol = float(rets.std(ddof=1)) * (252 ** 0.5) * 100
    mdd = riskmetrics.max_drawdown(spx)
    cells = [
        ("CAGR", f"{cagr:.1f}%" if cagr is not None else "—"),
        ("Vol (ann.)", f"{vol:.1f}%"),
        ("Sharpe", _fmt2(riskmetrics.sharpe(rets))),
        ("Sortino", _fmt2(riskmetrics.sortino(rets))),
        ("Calmar", _fmt2(riskmetrics.calmar(spx))),
        ("Max DD", f"{mdd * 100:.1f}%" if mdd is not None else "—"),
    ]
    return ('<table class="tear-kpi"><tr>'
            + "".join(f"<th>{esc(lab)}</th>" for lab, _ in cells) + "</tr><tr>"
            + "".join(f"<td>{esc(val)}</td>" for _, val in cells) + "</tr></table>")


def _tearsheet_table(spx) -> str:
    """Year × month return table (%), green/red by sign, with a compounded FY column."""
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
    return styler_html(
        frame.style.format({c: "{:+.1f}" for c in _MONTHS + ["FY %"]}, na_rep="·")
        .map(charts.color_changes, subset=_MONTHS + ["FY %"]))


def _tearsheet_panel(df) -> str:
    """quantstats-style tearsheet for the S&P over the full committed timeline (no new data)."""
    if df is None or df.empty or "spx" not in df.columns:
        return ""
    spx = pd.to_numeric(df["spx"], errors="coerce").dropna()
    if len(spx) < 252:
        return ""
    rets = riskmetrics.returns(spx)
    if rets is None:
        return ""
    body = _tearsheet_metrics(spx, rets)
    body += caption(f"{spx.index[0].date()} → {spx.index[-1].date()} · {len(spx):,} sessions · "
                    "risk-free = 0. Source: riskmetrics over the committed timeline.")
    body += _tearsheet_table(spx)
    body += caption("Monthly total returns (%), green/red by sign; FY % compounds the year. "
                    "The most recent month and year are partial (month-/year-to-date). "
                    "Built from the committed timeline's S&P series.")
    return details("📊 Tearsheet — S&P 500 (full committed timeline)", body)


def section(ctx) -> str:
    """Where the cross-asset anchors have been — the committed metrics timeline as charts."""
    df = ctx.tl
    if df is None or df.empty or len(df) < 5 or not isinstance(df.index, pd.DatetimeIndex):
        return caption("The metrics timeline is still accumulating — trend charts appear once a "
                       "few sessions exist. Seed ~3 years of real history with `python -m src.backfill`.")
    intro = caption(f"{len(df)} sessions · {df.index[0].date()} → {df.index[-1].date()} — each "
                    "anchor's path, with today's percentile over the whole window.")
    parts = [
        intro,
        _trend_charts(df),
        _time_machine(df),
        _crisis_signal_panel(df),
        _analogue_panel(df),
        _tearsheet_panel(df),
    ]
    return "".join(p for p in parts if p)
