"""Aggregate, clean, and de-duplicate financial news from RSS feeds.

Feeds are fetched with a browser User-Agent (several publishers block the
default one). Filing/technical-alert noise is dropped per config.
"""

from __future__ import annotations

import calendar
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import feedparser
import requests

from . import config

_TAG_RE = re.compile(r"<[^>]+>")


def fetch_news(
    feeds: list[tuple[str, str]] = config.FEEDS,
    per_feed: int = config.NEWS_PER_FEED,
    max_total: int = config.NEWS_MAX_TOTAL,
) -> list[dict]:
    """Return recent, de-duplicated headlines sorted newest-first."""
    items: list[dict] = []
    seen: set[str] = set()
    # Fetch feeds concurrently (network-bound); de-dupe/normalize stays
    # sequential and in feed order so the dedup priority is unchanged.
    with ThreadPoolExecutor(max_workers=min(12, len(feeds) or 1)) as pool:
        parsed_feeds = list(pool.map(lambda f: (f[0], _fetch_feed(f[1])), feeds))
    for source, parsed in parsed_feeds:
        if parsed is None:
            continue
        for entry in parsed.entries[:per_feed]:
            item = _normalize(entry, source, seen)
            if item is not None:
                items.append(item)
    items.sort(key=lambda x: x["_ts"], reverse=True)
    for item in items:
        item.pop("_ts", None)
    return items[:max_total]


def _fetch_feed(url: str, timeout: int = config.NEWS_TIMEOUT):
    """Fetch + parse one feed; return None on any failure."""
    try:
        resp = requests.get(url, headers={"User-Agent": config.BROWSER_UA}, timeout=timeout)
        resp.raise_for_status()
        return feedparser.parse(resp.content)
    except Exception:
        return None


def _normalize(entry, source: str, seen: set[str]) -> dict | None:
    """Turn a feed entry into a clean item, or None if noise/duplicate."""
    if _is_noise(entry):
        return None
    title = (entry.get("title") or "").strip()
    if not title:
        return None
    key = title.lower()
    if key in seen:
        return None
    seen.add(key)
    published = _entry_time(entry)
    return {
        "title": title,
        "source": source,
        "link": entry.get("link", ""),
        "summary": _clean(entry.get("summary", "")),
        "published": published.isoformat() if published else None,
        "_ts": published.timestamp() if published else 0.0,
    }


def _is_noise(entry) -> bool:
    """Drop SEC filing items and algorithmic technical-alert spam."""
    link = entry.get("link") or ""
    author = (entry.get("author") or "").lower()
    if any(sub in link for sub in config.NEWS_SKIP_LINK_SUBSTRINGS):
        return True
    return any(skip.lower() in author for skip in config.NEWS_SKIP_AUTHORS)


def _entry_time(entry) -> datetime | None:
    """UTC datetime from the entry's published/updated struct, if present.

    feedparser normalizes *_parsed to a UTC struct_time, so we use
    calendar.timegm (interprets the struct as UTC), not time.mktime (local time).
    """
    for attr in ("published_parsed", "updated_parsed"):
        parsed = entry.get(attr)
        if parsed:
            return datetime.fromtimestamp(calendar.timegm(parsed), tz=timezone.utc)
    return None


def _clean(text: str, limit: int = 280) -> str:
    """Strip HTML tags and clamp summary length."""
    return _TAG_RE.sub("", text or "").strip()[:limit]
