"""Headlines tab — aggregated RSS feed rendered as clean HTML cards.

Contract: section(ctx) -> str  (inner HTML, no network, degrades on empty data).
"""
from __future__ import annotations

from src import config

from ..render import caption, esc, panel


def _fmt_published(published: str) -> str:
    """Trim ISO timestamp to 'YYYY-MM-DD HH:MM', swapping T for a space."""
    if not published:
        return ""
    return published[:16].replace("T", " ")


def _headline_card(item: dict) -> str:
    """One news item as an HTML card: linked title, source, published, summary."""
    title = item.get("title") or ""
    link = item.get("link") or ""
    source = item.get("source") or ""
    published = _fmt_published(item.get("published") or "")
    summary = item.get("summary") or ""

    if link:
        head_html = f'<a href="{esc(link)}" target="_blank" rel="noopener">{esc(title)}</a>'
    else:
        head_html = esc(title)

    meta_parts = []
    if source:
        meta_parts.append(esc(source))
    if published:
        meta_parts.append(esc(published))
    meta_html = f'<p class="cap">{" · ".join(meta_parts)}</p>' if meta_parts else ""

    summary_html = (f'<p class="news-summary">{esc(summary)}</p>'
                    if summary else "")

    return (f'<div class="news-card">'
            f'<p class="news-title"><strong>{head_html}</strong></p>'
            f'{meta_html}'
            f'{summary_html}'
            f'</div>')


def section(ctx) -> str:
    """Headlines tab: news list from brief['news'] as linked cards."""
    try:
        items = ctx.brief.get("news") or []
        if not items:
            return caption("No headlines in today's brief.")

        feed_count = len(getattr(config, "FEEDS", []))
        sub = f"{len(items)} headlines across {feed_count} feeds" if feed_count else f"{len(items)} headlines"

        cards_html = "".join(_headline_card(it) for it in items if it.get("title"))
        if not cards_html:
            return caption("No headlines to display.")

        body = f'<div class="news-list">{cards_html}</div>'
        return panel("Headlines", body, sub=sub)
    except Exception:
        return caption("Headlines unavailable.")
