"""Overview tab — the landing read: thesis hero, derived signal strip, day-over-day
deltas, leaders/laggards, and the headline S&P chart."""
from __future__ import annotations

import html

import streamlit as st

from src import brief as brief_mod
from src import eras, formatting, history, signals
from src.dashboard.widgets import TONE_HEX, tone_span, render_line


def signals_strip(brief: dict) -> None:
    """Lead the Overview with the day's derived read — data turned into signal."""
    lead = signals.derive_lead(brief)
    sigs = signals.derive_signals(brief)
    if not lead and not sigs:
        return
    if lead:
        color = TONE_HEX.get(lead["tone"], "#7beafb")
        st.markdown(
            f"""<div style="background:var(--surface);border:1px solid var(--border);border-left:4px solid {color};
            border-radius:10px;padding:16px 20px;margin:2px 0 12px;">
            <div style="font-family:'Space Grotesk',sans-serif;font-size:.66rem;text-transform:uppercase;
            letter-spacing:.13em;color:{color};margin-bottom:6px;">● Today's read</div>
            <div style="font-family:'Instrument Serif',Georgia,serif;font-size:1.5rem;line-height:1.3;
            color:var(--text);">{html.escape(lead['text'])}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    if sigs:
        st.subheader("⚡ Today's signal")
        cols = st.columns(2)
        for i, s in enumerate(sigs):
            cols[i % 2].markdown(tone_span("●", s["tone"]) + "  " + html.escape(s["text"]),
                                 unsafe_allow_html=True)
    era = eras.era_for(brief.get("date", ""))
    if era:
        st.caption(f"📅 We're in the **{era['name']}** era ({era['regime']}). "
                   f"Fed: {era['fed']}. See the **Trends** tab's time machine, or run `/finance` to dig in.")
    st.divider()


def deltas_panel(brief: dict) -> None:
    """Headline level changes since the prior saved session (day-over-day)."""
    key_syms = ["^GSPC", "^IXIC", "^TNX", "DX-Y.NYB", "GC=F", "^VIX"]
    result = history.deltas(brief, key_syms)
    if result is None:
        st.caption("📈 Day-over-day deltas appear here once you've run this on a prior day "
                   "— snapshots are saved automatically on every refresh.")
        return
    prior_date, rows = result
    if not rows:
        return
    st.subheader(f"Since last session ({prior_date})")
    cols = st.columns(len(rows))
    for col, r in zip(cols, rows):
        if r["symbol"] == "^TNX":
            delta = formatting.fmt_bps(r["change"]) if r["change"] is not None else None
            col.metric(r["name"], f"{r['last']:.2f}%", delta)
        else:
            delta = formatting.fmt_pct(r["change_pct"]) if r["change_pct"] is not None else None
            color = "inverse" if r["symbol"] == "^VIX" else "normal"
            col.metric(r["name"], formatting.fmt_num(r["last"]), delta, delta_color=color)
    st.divider()


def _narrative_thesis(path) -> str | None:
    """The written read's one-line thesis: first content line under '## Today in one line'
    (or a 'thesis' header). None if not found — so the hero degrades to the derived lead."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None
    for i, ln in enumerate(lines):
        low = ln.strip().lower()
        if low.startswith("##") and ("one line" in low or "thesis" in low):
            for body in lines[i + 1:]:
                t = body.strip()
                if t and not t.startswith("#"):
                    return t.lstrip("*->•_ ").strip()
            break
    return None


def _thesis_hero(brief: dict) -> None:
    """Lead the Overview with the written narrative's thesis (the product is the read, not the
    data). Silent if there's no narrative — signals_strip's derived lead then carries the top."""
    path = brief_mod.latest_narrative_path()
    if not path or not path.exists():
        return
    thesis = _narrative_thesis(path)
    if not thesis:
        return
    ndate = path.stem.replace("narrative_", "")
    stale = f" · from {ndate}, older than today's brief" if ndate < str(brief.get("date", "")) else ""
    st.markdown(
        f"""<div style="background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--accent);
        border-radius:10px;padding:16px 20px;margin:2px 0 12px;">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:.66rem;text-transform:uppercase;
        letter-spacing:.13em;color:var(--accent);margin-bottom:6px;">● Today's thesis{stale}</div>
        <div style="font-family:'Instrument Serif',Georgia,serif;font-size:1.6rem;line-height:1.3;
        color:var(--text);">{html.escape(thesis)}</div>
        <div style="font-size:.78rem;color:var(--text-dim);margin-top:9px;">Full read in the <b>Story</b> tab →</div>
        </div>""",
        unsafe_allow_html=True,
    )


def overview_tab(brief: dict, closes: dict) -> None:
    _thesis_hero(brief)
    signals_strip(brief)
    deltas_panel(brief)
    movers = brief["movers"]
    left, right = st.columns(2)
    with left:
        st.subheader("Leaders")
        for m in movers["leaders"]:
            st.markdown(f"**{m['name']}**  " + tone_span(formatting.fmt_pct(m["change_pct"]),
                        "up" if (m.get("change_pct") or 0) >= 0 else "down"), unsafe_allow_html=True)
    with right:
        st.subheader("Laggards")
        for m in movers["laggards"]:
            st.markdown(f"**{m['name']}**  " + tone_span(formatting.fmt_pct(m["change_pct"]),
                        "up" if (m.get("change_pct") or 0) >= 0 else "down"), unsafe_allow_html=True)
    st.divider()
    st.subheader("S&P 500")
    render_line(closes, "^GSPC", "S&P 500", key="ov_sp500")
