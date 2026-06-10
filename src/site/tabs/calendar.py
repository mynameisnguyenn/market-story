"""Calendar tab — next FOMC countdown and post-FOMC S&P drift event study.

Live-fetch panels (econ releases, earnings, 13F, SEC filings) are available in the
interactive dev app but are skipped here so the static build stays offline-safe.
"""
from __future__ import annotations

import pandas as pd

from src import calendar_data, event_study

from ..render import caption, details, esc, fmt, panel


def _fomc_panel(ctx) -> str:  # noqa: ARG001
    """Countdown to the next scheduled FOMC rate decision."""
    try:
        nf = calendar_data.next_fomc()
    except Exception:
        return ""
    if not nf:
        return panel(
            "Next FOMC decision",
            caption("Next FOMC date unavailable — update `FOMC_DECISIONS` in "
                    "`src/calendar_data.py` with the Fed's latest published calendar."),
        )
    d = nf["days"]
    when = "today" if d == 0 else "tomorrow" if d == 1 else f"in {d} days"
    body = (
        f'<div class="kpi">'
        f'<div class="kpi-label">Next decision</div>'
        f'<div class="kpi-value">{esc(nf["date"])}</div>'
        f'<div class="kpi-delta flat">{esc(when)}</div>'
        f'</div>'
        + caption(
            "Statement ~2:00pm ET; quarterly meetings add the Summary of Economic "
            "Projections + a press conference. Schedule from federalreserve.gov, "
            "verified 2026-06. Source: Federal Reserve."
        )
    )
    return panel("Next FOMC decision", body)


def _drift_table(rows: list[dict]) -> str:
    """Render the drift rows as a plain HTML table."""
    def cell(v: str, cls: str = "") -> str:
        c = f' class="{cls}"' if cls else ""
        return f"<td{c}>{esc(v)}</td>"

    header = (
        "<thead><tr>"
        + "".join(f"<th>{h}</th>" for h in
                  ["Horizon", "n", "Median", "95% CI", "% positive", "Skipped"])
        + "</tr></thead>"
    )
    body_rows = []
    for r in rows:
        median_str = f"{r['median']:+.2f}%" if r.get("median") is not None else "—"
        ci_str = (
            f"[{r['ci_lo']:+.2f}%, {r['ci_hi']:+.2f}%]"
            if r.get("ci_lo") is not None and r.get("ci_hi") is not None
            else "—"
        )
        frac_str = f"{r['frac_pos'] * 100:.0f}%" if r.get("frac_pos") is not None else "—"
        body_rows.append(
            "<tr>"
            + cell(f"T+{r['horizon']}")
            + cell(str(r.get("n", "—")))
            + cell(median_str)
            + cell(ci_str)
            + cell(frac_str)
            + cell(str(r.get("n_skipped", 0)))
            + "</tr>"
        )
    return f'<div class="tbl"><table>{header}<tbody>{"".join(body_rows)}</tbody></table></div>'


def _drift_panel(ctx) -> str:
    """28 years of post-FOMC S&P drift — the honest event study."""
    try:
        rows = event_study.fomc_drift(ctx.tl)
    except Exception:
        return ""
    if not rows:
        return ""

    all_ci_include_zero = all(r.get("includes_zero") is not False for r in rows)
    max_n = max(r.get("n", 0) for r in rows)

    inner_parts = []
    if all_ci_include_zero:
        inner_parts.append(
            f'<div class="info-box">'
            f"Across ~{max_n} scheduled decisions, S&amp;P returns after FOMC days are "
            "statistically indistinguishable from zero at every horizon tested "
            "(bootstrap CIs on the median all include zero). There is no detectable "
            "post-FOMC drift in this sample — that is the finding."
            f"</div>"
        )
    inner_parts.append(_drift_table(rows))
    inner_parts.append(caption(
        "Scheduled decisions only, 1998–2025 (unscheduled/emergency meetings excluded — "
        "their dates are themselves the news). T+1/2/5 windows never overlap across "
        "meetings ~6 weeks apart, so iid bootstrap CIs are valid here, unlike rolling-"
        "signal stats. Descriptive history, not a forecast. Source: event_study."
    ))

    expander = details(
        "Post-FOMC drift — S&P after every scheduled decision since 1998",
        "".join(inner_parts),
    )
    return expander if expander else ""


def _live_fetch_notice() -> str:
    """Short caption for panels that require network at render time."""
    return panel(
        "Live-fetch panels",
        caption(
            "Economic releases, upcoming earnings, 13F holdings, and SEC filings require "
            "live network calls and are available in the interactive dev app "
            "(streamlit run app.py). They are intentionally omitted from the static build "
            "to keep it offline-safe."
        ),
    )


def section(ctx) -> str:
    """Calendar tab: FOMC countdown, post-FOMC drift study, live-fetch notice."""
    parts = [
        _fomc_panel(ctx),
        _drift_panel(ctx),
        _live_fetch_notice(),
    ]
    return "".join(p for p in parts if p)
