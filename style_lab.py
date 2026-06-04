"""Design sandbox — iterate on styles.css against every component on ONE screen.

    python -m streamlit run style_lab.py

Edit styles.css (or live-edit in the browser via F12 -> Elements -> Styles), save, and
this reloads (runOnSave=true). Bank the looks you like into styles.css — the real app
loads the exact same file, so what you tune here is what ships. No live data, no network.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ACCENT = "#7beafb"   # keep in sync with styles.css --accent / app.LINE_COLOR


def _css() -> str:
    try:
        return (Path(__file__).parent / "styles.css").read_text(encoding="utf-8")
    except Exception:
        return ""


st.set_page_config(page_title="Style Lab", page_icon="🎨", layout="wide")
st.markdown(f"<style>{_css()}</style>", unsafe_allow_html=True)

st.sidebar.title("Style Lab")
st.sidebar.caption("Edit **styles.css** → save → this reloads. Or F12 live-edit, then bank the winners. "
                   "Retune the whole system from the `:root` tokens at the top of styles.css.")

st.title("Market Story")
st.markdown("_The headline above is the serif display face (Instrument Serif). "
            "Below: every component on one screen for fast tuning._")

# "Today's read" hero card — mirrors signals_strip() in app.py
st.markdown(
    f"""<div style="background:var(--surface);border:1px solid var(--border);border-left:4px solid {ACCENT};
    border-radius:10px;padding:16px 20px;margin:2px 0 14px;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:.66rem;text-transform:uppercase;
    letter-spacing:.13em;color:{ACCENT};margin-bottom:6px;">● Today's read</div>
    <div style="font-family:'Instrument Serif',Georgia,serif;font-size:1.5rem;line-height:1.3;color:var(--text);">
    Risk is rich and hedges look cheap — VIX at 16 sits below 20-day realized vol, and HY credit
    spreads are at their 3rd percentile of the year.</div>
    </div>""", unsafe_allow_html=True)

st.subheader("Metrics — mono numerals, cyan accent bar, hover")
cols = st.columns(4)
for col, (label, val, delta) in zip(cols, [
        ("S&P 500", "5,944", "+0.42%"), ("VIX", "16.1", "-3.1%"),
        ("10Y Treasury", "4.21%", "+2 bps"), ("WTI crude", "$78.40", "-1.2%")]):
    col.metric(label, val, delta)

st.subheader("Table — tabular figures")
df = pd.DataFrame({
    "Instrument": ["S&P 500", "Nasdaq 100", "Gold", "Copper", "HY OAS (bps)"],
    "Last": [5944.1, 21380.5, 2412.0, 4.81, 312.0],
    "1D %": [0.42, 0.61, -0.30, 1.10, -2.00],
    "YTD %": [11.2, 14.8, 9.1, -3.4, None],
})
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("Tabs, charts, controls")
t1, t2, t3 = st.tabs(["Overview", "Macro", "Trends"])
with t1:
    fig = go.Figure(go.Scatter(y=[1, 1.2, 1.1, 1.4, 1.35, 1.6, 1.55, 1.8, 1.72, 1.95],
                               mode="lines", line=dict(color=ACCENT, width=1.6),
                               fill="tozeroy", fillcolor="rgba(123,234,251,0.07)"))
    fig.update_layout(height=240, margin=dict(l=8, r=8, t=8, b=8),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#241f1a", zeroline=False))
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    st.markdown("Inline tone: :green[+0.42%] · :red[-2.00%] · :orange[watch] · "
                f"<a href='#' style='color:{ACCENT}'>a cyan link</a>", unsafe_allow_html=True)
with t2:
    st.markdown("### A section header (h3)")
    st.write("Body text in the warm off-white. Subheads use Space Grotesk with tight tracking.")
with t3:
    st.button("A primary button")
    st.slider("A slider (uses the accent)", 0, 100, 60)
    st.selectbox("A selectbox", ["Crude oil", "Gasoline", "Distillate"])

with st.expander("An expander — click to open"):
    st.write("Expander body content sits on the secondary surface.")
st.caption("A caption — warm dim text. Tweak the :root tokens in styles.css to retune everything at once.")
