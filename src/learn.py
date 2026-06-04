"""Learn-the-Markets page: educational content + money-flow visualizations.

Content and viz data live as files under learn/ (generated via deep research).
Figure builders are pure (unit-tested); render() lays out the Streamlit page and
degrades gracefully when a content file is missing.
"""

from __future__ import annotations

import json

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from . import config, eras

LEARN_DIR = config.PROJECT_ROOT / "learn"
NODE_COLOR = "#4C9AFF"
LINK_COLOR = "rgba(76,154,255,0.35)"

CATEGORY_COLORS = {
    "Founding": "#4C9AFF",
    "Crash": "#EF5350",
    "Reform": "#26A69A",
    "Innovation": "#AB47BC",
    "Boom": "#FFA726",
}


# --- Loaders -----------------------------------------------------------------

def load_text(filename: str) -> str:
    path = LEARN_DIR / filename
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_json(filename: str):
    path = LEARN_DIR / filename
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


# --- Pure figure builders ----------------------------------------------------

def sankey_figure(flow: dict | None, height: int = 480):
    """Plotly Sankey from {title, nodes:[label], links:[{source,target,value,label}]}."""
    if not flow or not flow.get("nodes") or not flow.get("links"):
        return None
    nodes = flow["nodes"]
    index = {label: i for i, label in enumerate(nodes)}
    src, tgt, val, lab = [], [], [], []
    for link in flow["links"]:
        s, t = link.get("source"), link.get("target")
        if s not in index or t not in index:
            continue
        src.append(index[s])
        tgt.append(index[t])
        val.append(link.get("value") or 1)
        lab.append(link.get("label", ""))
    if not src:
        return None
    fig = go.Figure(go.Sankey(
        node=dict(label=nodes, pad=18, thickness=18, color=NODE_COLOR,
                  line=dict(color="rgba(255,255,255,0.2)", width=0.5)),
        link=dict(source=src, target=tgt, value=val, label=lab, color=LINK_COLOR),
    ))
    fig.update_layout(height=height, margin=dict(t=36, l=10, r=10, b=10),
                      title=flow.get("title", ""), font=dict(size=12))
    return fig


def timeline_figure(events: list[dict] | None, height: int = 420):
    """Scatter timeline of historical events, colored by category."""
    if not events:
        return None
    events = sorted(events, key=lambda e: e.get("year", 0))
    fig = go.Figure()
    for category, color in CATEGORY_COLORS.items():
        pts = [e for e in events if e.get("category") == category]
        if pts:
            _add_timeline_trace(fig, pts, category, color)
    other = [e for e in events if e.get("category") not in CATEGORY_COLORS]
    if other:
        _add_timeline_trace(fig, other, "Other", "#9AA0A6")
    fig.update_layout(
        height=height, margin=dict(t=20, l=10, r=10, b=10),
        yaxis=dict(visible=False, range=[0.8, 1.2]),
        xaxis=dict(title="Year"), legend=dict(orientation="h"),
    )
    return fig


def _add_timeline_trace(fig, points, name, color):
    fig.add_trace(go.Scatter(
        x=[e["year"] for e in points], y=[1] * len(points), mode="markers",
        marker=dict(size=14, color=color), name=name,
        text=[f"{e['year']} — {e['title']}<br>{e.get('blurb', '')}" for e in points],
        hovertemplate="%{text}<extra></extra>",
    ))


# --- Streamlit render --------------------------------------------------------

def render() -> None:
    st.title("📚 Learn the Markets")
    st.caption("Foundations for a risk analyst — researched and fact-checked.")
    intro = load_text("00_intro.md")
    if intro:
        st.markdown(intro)
    tabs = st.tabs(["What is a market", "History", "Eras", "Players", "The Fed", "How money moves"])
    with tabs[0]:
        _section("01_what_is_a_market.md")
    with tabs[1]:
        _history()
    with tabs[2]:
        _eras()
    with tabs[3]:
        _players()
    with tabs[4]:
        _the_fed()
    with tabs[5]:
        _money_flows()


def _eras() -> None:
    st.markdown("### Market eras  ·  1998 → today")
    st.caption("The regimes behind the daily brief — open one to read the full history. These same "
               "eras shade the **Trends** tab, and the `/finance` tutor teaches them against the data.")
    kdir = config.PROJECT_ROOT / "knowledge" / "eras"
    for e in eras.ERAS:
        end = (e["end"] or "now")[:4]
        with st.expander(f"{e['start'][:4]}–{end}  ·  {e['name']}  —  {e['regime']}"):
            st.markdown(f"_{e['blurb']}_  \n**Fed:** {e['fed']}")
            path = kdir / f"{e['key']}.md"
            if path.exists():
                body = path.read_text(encoding="utf-8")
                if body.startswith("---"):                 # strip YAML frontmatter for display
                    body = body.split("---", 2)[-1]
                st.markdown(body)


def _section(filename: str) -> None:
    text = load_text(filename)
    st.markdown(text) if text else st.info("This section hasn't been generated yet.")


def _history() -> None:
    events = load_json("timeline.json")
    fig = timeline_figure(events)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    _section("02_history.md")
    if events:
        with st.expander("Full timeline (chronological)"):
            for e in sorted(events, key=lambda x: x.get("year", 0)):
                st.markdown(f"**{e['year']} — {e['title']}** · {e.get('blurb', '')}")


def _players() -> None:
    _section("03_players.md")
    players = load_json("players.json")
    if players:
        frame = pd.DataFrame([
            {"Group": p.get("group"), "Role": p.get("role"),
             "Examples": p.get("examples", ""), "Scale / AUM": p.get("scale", "")}
            for p in players
        ])
        st.dataframe(frame, use_container_width=True, hide_index=True)
    flows = load_json("flows.json") or {}
    fig = sankey_figure(flows.get("equity_order"))
    if fig is not None:
        st.subheader("How an order flows to settlement")
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def _the_fed() -> None:
    _section("04_the_fed.md")
    flows = load_json("flows.json") or {}
    fig = sankey_figure(flows.get("fed_transmission"))
    if fig is not None:
        st.subheader("Monetary-policy transmission")
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def _money_flows() -> None:
    flows = load_json("flows.json") or {}
    fig = sankey_figure(flows.get("money_flow"))
    if fig is not None:
        st.subheader("How money flows through the system")
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    _section("05_money_flows.md")
