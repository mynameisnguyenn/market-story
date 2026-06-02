"""Assemble the daily brief and persist it as JSON + Markdown.

The JSON is the contract Claude reads to write the narrative; the Markdown is a
human-readable facts sheet so the brief is useful even without synthesis.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone

from . import config, formatting, macro_data, market_data, news


def build_brief(history=None, sections=None, macro=None, news_items=None, fetch: bool = True) -> dict:
    """Build the brief dict. With fetch=True, pull everything fresh."""
    if fetch:
        history = market_data.download_history(config.all_symbols())
        sections = market_data.build_market_sections(history)
        macro = macro_data.fetch_macro()
        news_items = news.fetch_news()
    sections = sections or {}
    return {
        "date": str(date.today()),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session_label": _session_label(),
        "markets": sections,
        "macro": macro or [],
        "movers": _movers(sections),
        "news": news_items or [],
        "stats": _stats(sections),
    }


def _session_label() -> str:
    return datetime.now(timezone.utc).strftime("as of %Y-%m-%d %H:%M UTC")


def _movers(sections: dict, n: int = 5) -> dict:
    """Top/bottom equity & index movers by 1-day percent change (ex-VIX)."""
    pool = []
    for key in ("us_equities", "sectors", "global_indices", "watchlist"):
        for row in sections.get(key, []):
            if row["symbol"] == "^VIX" or row.get("change_pct") is None:
                continue
            pool.append({"name": row["name"], "symbol": row["symbol"],
                         "change_pct": row["change_pct"], "group": key})
    ascending = sorted(pool, key=lambda x: x["change_pct"])
    return {"leaders": ascending[::-1][:n], "laggards": ascending[:n]}


def _stats(sections: dict) -> dict:
    """VIX level and sector breadth."""
    vix = next((r["last"] for r in sections.get("us_equities", []) if r["symbol"] == "^VIX"), None)
    sectors = [r for r in sections.get("sectors", []) if r.get("change_pct") is not None]
    advancers = sum(1 for r in sectors if r["change_pct"] > 0)
    decliners = sum(1 for r in sectors if r["change_pct"] < 0)
    return {"vix": vix, "sector_advancers": advancers,
            "sector_decliners": decliners, "sector_count": len(sectors)}


# --- Persistence -------------------------------------------------------------

def save_brief(brief: dict) -> tuple:
    """Write brief_<date>.json and brief_<date>.md; return their paths."""
    config.BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = config.BRIEFS_DIR / f"brief_{brief['date']}.json"
    json_path.write_text(json.dumps(brief, indent=2, default=str), encoding="utf-8")
    md_path = config.BRIEFS_DIR / f"brief_{brief['date']}.md"
    md_path.write_text(render_markdown(brief), encoding="utf-8")
    return json_path, md_path


def latest_brief_path():
    files = sorted(config.BRIEFS_DIR.glob("brief_*.json"))
    return files[-1] if files else None


def load_latest_brief() -> dict | None:
    path = latest_brief_path()
    return json.loads(path.read_text(encoding="utf-8")) if path else None


def latest_narrative_path():
    files = sorted(config.NARRATIVES_DIR.glob("narrative_*.md"))
    return files[-1] if files else None


def render_markdown(brief: dict) -> str:
    """Render a facts-only Markdown brief from the brief dict."""
    stats = brief.get("stats", {})
    lines = [
        f"# Market Brief — {brief['date']}",
        "",
        f"_{brief['session_label']}_",
        "",
        f"**VIX:** {formatting.fmt_num(stats.get('vix'))}  |  "
        f"**Sectors up/down:** {stats.get('sector_advancers', 0)}/{stats.get('sector_decliners', 0)}",
        "",
        "## Movers",
        "**Leaders:** " + _movers_line(brief["movers"]["leaders"]),
        "**Laggards:** " + _movers_line(brief["movers"]["laggards"]),
        "",
    ]
    for key, group in config.MARKET_GROUPS.items():
        lines += _market_table(group, brief["markets"].get(key, []))
    lines += _macro_table(brief.get("macro", []))
    lines += _headline_list(brief.get("news", []))
    return "\n".join(lines)


def _movers_line(movers: list[dict]) -> str:
    return ", ".join(f"{m['name']} {formatting.fmt_pct(m['change_pct'])}" for m in movers) or "n/a"


def _market_table(group: dict, rows: list[dict]) -> list[str]:
    is_yield = group["kind"] == "yield"
    head = "| Instrument | Last | 1D | 1W | YTD |"
    out = [f"## {group['label']}", head, "|---|---:|---:|---:|---:|"]
    for r in rows:
        one_day = formatting.fmt_bps(r.get("level_change")) if is_yield else formatting.fmt_pct(r.get("change_pct"))
        out.append(
            f"| {r['name']} | {formatting.fmt_num(r.get('last'))} | {one_day} | "
            f"{formatting.fmt_pct(r.get('change_1w_pct'))} | {formatting.fmt_pct(r.get('ytd_pct'))} |"
        )
    out.append("")
    return out


def _macro_table(macro: list[dict]) -> list[str]:
    out = ["## Macro (FRED)", "| Series | Latest | Δ | As of |", "|---|---:|---:|---|"]
    for m in macro:
        out.append(
            f"| {m['name']} | {formatting.fmt_num(m.get('latest'))} | "
            f"{formatting.fmt_num(m.get('change'))} | {m.get('date') or 'n/a'} |"
        )
    out.append("")
    return out


def _headline_list(news_items: list[dict], limit: int = 25) -> list[str]:
    out = ["## Top Headlines"]
    for item in news_items[:limit]:
        out.append(f"- **{item['title']}** — {item.get('source', '')}")
    out.append("")
    return out
