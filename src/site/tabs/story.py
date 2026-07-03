"""Story tab — the running thesis, the prediction track record, and today's full narrative.

Mirrors src/dashboard/panels/narrative.py as static HTML, using the render helpers and
reading committed data only (no network, no Streamlit, no @st.cache_data wrappers).
"""
from __future__ import annotations

import pandas as pd

from src import brief as brief_mod
from src import calibration, ledger, thesis

from ..render import caption, details, esc, grid, kpi_card, md_html, panel, styler_html, tone_of


# ---------------------------------------------------------------------------
# Running thesis
# ---------------------------------------------------------------------------

def _running_thesis() -> str:
    """The committed standing cross-session view wrapped in a collapsible block."""
    try:
        rt = thesis.load_running_thesis()
    except Exception:
        rt = None
    if not rt:
        return ""
    body = md_html(rt)
    if not body:
        return ""
    blk = details(
        "\U0001f4cc Running thesis — the standing cross-session view",
        body,
        open_=False,
    )
    cap = caption(
        "The through-line, revised each session by /narrate. Today’s dated read is below."
    )
    return blk + cap


# ---------------------------------------------------------------------------
# Track record
# ---------------------------------------------------------------------------

def _watch_table(watch: list[dict]) -> str:
    """Every watch-block prediction as a styled HTML table inside a details expander."""
    if not watch:
        return ""
    try:
        df = pd.DataFrame([
            {
                "Logged": r.get("logged"),
                "Status": r.get("status"),
                "Metric": r.get("metric"),
                "Trigger": r.get("trigger"),
                "Resolved@": r.get("graded_value"),
                "Claim": r.get("claim"),
            }
            for r in watch
        ])
        st = df.style.set_table_attributes('class="records"')
        tbl = styler_html(st)
    except Exception:
        # Plain fallback table when styler fails.
        rows_html = "".join(
            f"<tr><td>{esc(r.get('logged'))}</td><td>{esc(r.get('status'))}</td>"
            f"<td>{esc(r.get('metric'))}</td><td>{esc(r.get('trigger'))}</td>"
            f"<td>{esc(r.get('graded_value'))}</td><td>{esc(r.get('claim'))}</td></tr>"
            for r in watch
        )
        tbl = (
            '<div class="tbl"><table><thead><tr>'
            "<th>Logged</th><th>Status</th><th>Metric</th>"
            "<th>Trigger</th><th>Resolved@</th><th>Claim</th>"
            f"</tr></thead><tbody>{rows_html}</tbody></table></div>"
        )
    body = tbl + caption(
        "Every watch-block prediction, graded at its horizon against committed data — "
        "the accountability the running thesis is built on."
    )
    return details(f"Every watch call graded ({len(watch)})", body)


def _calibration_panel(watch: list[dict]) -> str:
    """Brier calibration vs the base rate, gated on MIN_N graded probabilities. Fully
    self-contained — a failure here can never blank the hit-rate/stance sections."""
    try:
        graded = calibration.gradeable(watch)
        if len(graded) < calibration.MIN_N:
            return ""                              # not enough sample — render nothing, honestly
        bs = calibration.brier_score(watch)
        clim = calibration.climatology_brier(watch)
        bins = calibration.calibration_bins(watch, bins=5)
        if bs["score"] is None or clim["score"] is None or not bins:
            return ""                              # never trust a derived value to match its gate
        beats = bs["score"] < clim["score"]
        cards = [
            kpi_card("Brier score", f"{bs['score']:.3f}"),
            kpi_card("vs base rate", f"{clim['score']:.3f}",
                     delta="beats climatology" if beats else "worse than climatology",
                     tone=tone_of(clim["score"] - bs["score"])),
            kpi_card("Graded (n)", str(bs["n"])),
        ]
        rows = "".join(
            f"<tr><td>{b['bin_lo']:.0%}–{b['bin_hi']:.0%}</td><td>{b['n']}</td>"
            f"<td>{b['p_mean']:.0%}</td><td>{b['realized']:.0%}</td></tr>"
            for b in bins
        )
        tbl = ('<div class="tbl"><table><thead><tr><th>Bucket</th><th>n</th>'
               f"<th>Predicted</th><th>Realized</th></tr></thead><tbody>{rows}</tbody></table></div>")
        n_lo = min(b["n"] for b in bins)
        n_hi = max(b["n"] for b in bins)
        body = grid(cards, 3) + tbl + caption(
            f"Brier {bs['score']:.3f} vs {clim['score']:.3f} for always guessing the "
            f"{clim['base_rate']:.0%} base rate, n={bs['n']}. Sparse bins ({n_lo}–{n_hi} each) — "
            "read the table, not a trend."
        )
        return details("🎯 Calibration — are the stated confidences trustworthy?", body)
    except Exception:
        return ""


def _track_record() -> str:
    """Hit-rate KPIs + stance paper-P&L line + watch-call expander."""
    try:
        records = ledger.load()
        lstats = ledger.stats()
        ss = ledger.stance_stats(records)
    except Exception:
        return ""

    watch = [r for r in records if r.get("kind") != "stance"]
    if not watch and not ss["n_logged"]:
        return ""

    parts: list[str] = []

    if watch:
        hr = lstats.get("hit_rate")
        cards = [
            kpi_card("Hit rate", f"{hr * 100:.0f}%" if hr is not None else "—"),
            kpi_card("Resolved", str(lstats.get("graded", "—"))),
            kpi_card("Pending", str(lstats.get("pending", "—"))),
        ]
        parts.append(grid(cards, 3))

    if ss["n_logged"]:
        wr = f"{ss['win_rate'] * 100:.0f}%" if ss["win_rate"] is not None else "—"
        ap = f"{ss['avg_pnl_bps']:+.0f} bps" if ss["avg_pnl_bps"] is not None else "—"
        line = (
            f"<p><strong>Daily stance (paper):</strong> {esc(wr)} win rate on "
            f"{ss['n_directional']} directional calls · avg {esc(ap)}/session · "
            f"{ss['n_flat']} flat · {ss['n_omitted']} omitted</p>"
        )
        small = (
            " Small n — not yet meaningful; an equity curve unlocks at 63 settled sessions."
            if ss["n_directional"] < 63
            else ""
        )
        cap_text = (
            "Equal-weight next-session settlement of the narrative’s mandatory stance block; "
            f"flat and omitted days stay on the record.{small}"
        )
        parts.append(line + caption(cap_text))

    if watch:
        parts.append(_watch_table(watch))
    if watch:
        parts.append(_calibration_panel(watch))

    body = "".join(parts)
    return panel("Track record", body) if body else ""


# ---------------------------------------------------------------------------
# Latest narrative
# ---------------------------------------------------------------------------

def _narrative() -> str:
    """Today's full written narrative as rendered markdown."""
    try:
        path = brief_mod.latest_narrative_path()
    except Exception:
        return ""
    if not path or not path.exists():
        return caption(
            "No narrative yet. Run ‘python run.py’ then ask Claude to "
            "‘narrate today’s brief’ (or /narrate). The story will appear here."
        )
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return ""
    src_cap = caption(f"Source: {esc(path.name)}")
    return src_cap + md_html(text)


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------

def section(ctx) -> str:
    """Inner HTML for the Story tab: running thesis, track record, latest narrative."""
    parts = [
        _running_thesis(),
        _track_record(),
        _narrative(),
    ]
    return "".join(p for p in parts if p)
