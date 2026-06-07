"""Headlines tab — the aggregated RSS feed with a case-insensitive filter."""
from __future__ import annotations

import streamlit as st

from src import config


def filter_headlines(items: list[dict], query: str) -> list[dict]:
    """Case-insensitive filter on title + source; empty query returns all."""
    q = query.strip().lower()
    if not q:
        return items
    return [it for it in items
            if q in it.get("title", "").lower() or q in it.get("source", "").lower()]


def headlines_tab(brief: dict) -> None:
    all_items = brief.get("news", [])
    query = st.text_input("Filter headlines", placeholder="e.g. Fed, oil, NVDA…", key="news_filter")
    items = filter_headlines(all_items, query)
    if query.strip():
        st.caption(f"{len(items)} of {len(all_items)} headlines matching “{query.strip()}”")
    else:
        st.caption(f"{len(items)} headlines across {len(config.FEEDS)} feeds")
    with st.container(height=560):
        for item in items:
            link = item.get("link")
            head = f"[{item['title']}]({link})" if link else item["title"]
            st.markdown(f"**{head}**")
            meta = item.get("source", "")
            if item.get("published"):
                meta += f" · {item['published'][:16].replace('T', ' ')}"
            st.caption(meta)
