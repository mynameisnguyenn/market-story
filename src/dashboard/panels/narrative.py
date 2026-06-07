"""Story tab — the running thesis, the prediction track record, last session's watch
scorecard, and today's full written narrative."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src import brief as brief_mod
from src import scorecard
from src.dashboard.data import get_ledger, get_running_thesis


def _watch_scorecard(brief: dict) -> None:
    """Grade the prior narrative's `watch` block against today's brief — the feedback
    loop that makes the read accountable. Quiet (an expander); skips if no prior."""
    prior = brief_mod.prior_narrative_path()
    if not prior or not prior.exists():
        return
    result = scorecard.score_prior(prior.read_text(encoding="utf-8"), brief)
    graded = result["graded"]
    if not graded:
        return
    s = result["summary"]
    icon = {"triggered": "🟠", "watching": "⚪", "unresolved": "·"}
    with st.expander(f"📋 Last session's watch — {s['triggered']}/{s['resolved']} triggered  ({prior.name})"):
        for g in graded:
            v = g.get("current")
            cur = (f"{v:g}" if isinstance(v, (int, float)) and not isinstance(v, bool)
                   else "n/a" if v is None else str(v))
            st.markdown(f"{icon.get(g['status'], '·')} **{g['status']}** — {g['claim']}  "
                        f"`{g.get('metric')} {g.get('trigger')}` (now {cur})")


def narrative_tab(brief: dict) -> None:
    rt = get_running_thesis()
    if rt:
        with st.expander("📌 Running thesis — the standing cross-session view", expanded=False):
            st.markdown(rt)
        st.caption("The through-line, revised each session by `/narrate`. Today's dated read is below.")
    records, lstats = get_ledger()
    if records:
        hr = lstats["hit_rate"]
        st.subheader("Track record")
        cols = st.columns(3)
        cols[0].metric("Hit rate", f"{hr * 100:.0f}%" if hr is not None else "—")
        cols[1].metric("Resolved", lstats["graded"])
        cols[2].metric("Pending", lstats["pending"])
        with st.expander(f"Every watch call graded ({lstats['total']})"):
            st.dataframe(pd.DataFrame([
                {"Logged": r["logged"], "Status": r["status"], "Metric": r["metric"],
                 "Trigger": r["trigger"], "Resolved@": r.get("graded_value"), "Claim": r["claim"]}
                for r in records]), use_container_width=True, hide_index=True)
        st.caption("Every watch-block prediction, graded at its horizon against committed data — "
                   "the accountability the running thesis is built on.")
        st.divider()
    path = brief_mod.latest_narrative_path()
    if path and path.exists():
        st.caption(f"Source: {path.name}")
        _watch_scorecard(brief)
        st.markdown(path.read_text(encoding="utf-8"))
    else:
        st.info(
            "No narrative yet. Open a terminal in this folder, run `claude`, and ask "
            "**“narrate today's brief”** (or `/narrate`). The story will appear here."
        )
        with st.expander("Show the raw facts brief"):
            st.markdown(brief_mod.render_markdown(brief))
