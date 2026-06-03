"""Assemble the daily brief and persist it as JSON + Markdown.

The JSON is the contract Claude reads to write the narrative; the Markdown is a
human-readable facts sheet so the brief is useful even without synthesis.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone

from . import analytics, bls_data, cftc_data, config, eia_data, formatting, macro_data, market_data, news
from . import history as history_db   # aliased so build_brief's `history` arg can't shadow it


def build_brief(history=None, sections=None, macro=None, news_items=None,
                bls=None, energy=None, positioning=None, fetch: bool = True) -> dict:
    """Build the brief dict. With fetch=True, pull everything fresh."""
    if fetch:
        history = market_data.download_history(config.all_symbols())
        sections = market_data.build_market_sections(history)
        macro = macro_data.fetch_macro()
        news_items = news.fetch_news()
        bls = bls_data.fetch_bls()
        energy = eia_data.fetch_eia()
        positioning = cftc_data.fetch_cftc()
    sections = sections or {}
    closes = _history_closes(history)
    return {
        "date": str(date.today()),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session_label": _session_label(),
        "markets": sections,
        "macro": macro or [],
        "bls": bls or [],
        "energy": energy or [],
        "positioning": positioning or [],
        "movers": _movers(sections),
        "news": news_items or [],
        "stats": _stats(sections),
        "history": _embed_history(history),   # compact price series for instant chart reload
        "extremes": analytics.compute_extremes(closes),   # cross-asset 1y percentile/z
        "vol": analytics.compute_vol_premium(closes),     # VIX vs realized (vol risk premium)
    }


def _history_closes(history) -> dict:
    """{symbol: Close Series} from the raw history frames, for the analytics layer."""
    if not history:
        return {}
    out = {}
    for sym, frame in history.items():
        try:
            out[sym] = frame["Close"].dropna()
        except Exception:
            continue
    return out


def _embed_history(history) -> dict:
    """Shared date axis + aligned per-symbol closes so the dashboard can rebuild
    charts from a saved brief without a fresh download (instant load). The shared
    axis avoids repeating ~250 dates per symbol."""
    if not history:
        return {}
    import pandas as pd
    series = {}
    for sym, frame in history.items():
        try:
            close = frame["Close"].dropna()
            if close.empty:
                continue
            # Normalize the index: some symbols come back tz-aware, others tz-naive
            # (prod yfinance), which can't be joined; collapse all to tz-naive dates.
            idx = pd.DatetimeIndex(close.index)
            if idx.tz is not None:
                idx = idx.tz_localize(None)
            s = pd.Series(close.values, index=idx.normalize())
            series[sym] = s[~s.index.duplicated(keep="last")]   # collapsed dates can duplicate
        except Exception:
            continue
    if not series:
        return {}
    try:
        frame = pd.DataFrame(series)   # aligns symbols onto the union of dates
    except Exception:
        return {}                      # one bad index must not blank the whole brief
    dates = [d.strftime("%Y-%m-%d") for d in frame.index]
    cols = {sym: [None if pd.isna(v) else round(float(v), 4) for v in frame[sym].values]
            for sym in frame.columns}
    return {"d": dates, "series": cols}


def closes_from_brief(brief: dict):
    """Reconstruct {symbol: Close Series} from a brief's embedded history."""
    import pandas as pd
    h = brief.get("history") or {}
    out = {}
    if "d" in h and "series" in h:                      # shared-axis format
        idx = pd.to_datetime(h["d"])
        for sym, vals in h["series"].items():
            try:
                out[sym] = pd.Series(vals, index=idx).dropna()
            except Exception:
                continue
    else:                                               # legacy per-symbol format
        for sym, hh in h.items():
            try:
                if isinstance(hh, dict) and "c" in hh:
                    out[sym] = pd.Series(hh["c"], index=pd.to_datetime(hh["d"]))
            except Exception:
                continue
    return out


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
    if len(ascending) <= 1:                        # degenerate feed day: show the one we have
        return {"leaders": ascending, "laggards": []}
    # take fewer when the pool is small so an instrument can't be both a
    # leader and a laggard (feeds fail constantly -> the pool can be < 2n).
    half = n if len(ascending) >= 2 * n else len(ascending) // 2
    return {"leaders": ascending[::-1][:half], "laggards": ascending[:half]}


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
    history_db.save_today(brief)
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


def prior_narrative_path():
    """The narrative before the latest — the one whose `watch` block we grade today."""
    files = sorted(config.NARRATIVES_DIR.glob("narrative_*.md"))
    return files[-2] if len(files) >= 2 else None


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
    lines += _bls_table(brief.get("bls", []))
    lines += _energy_table(brief.get("energy", []))
    lines += _positioning_table(brief.get("positioning", []))
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
    out = ["## Macro (FRED)", "| Series | Latest | Δ | 1y %ile | As of |", "|---|---:|---:|---:|---|"]
    for m in macro:
        pct = m.get("pct_1y")
        out.append(
            f"| {m['name']} | {formatting.fmt_num(m.get('latest'))} | "
            f"{formatting.fmt_num(m.get('change'))} | {'' if pct is None else f'{pct:.0f}'} | "
            f"{m.get('date') or 'n/a'} |"
        )
    out.append("")
    return out


def _bls_table(rows: list[dict]) -> list[str]:
    if not rows:
        return []
    out = ["## Labor & Inflation (BLS)", "| Series | Latest | MoM Δ | YoY % | As of |",
           "|---|---:|---:|---:|---|"]
    for m in rows:
        out.append(
            f"| {m['name']} | {formatting.fmt_num(m.get('latest'))} | "
            f"{formatting.fmt_num(m.get('change'))} | {formatting.fmt_pct(m.get('yoy_pct'))} | "
            f"{m.get('date') or 'n/a'} |"
        )
    out.append("")
    return out


def _energy_table(rows: list[dict]) -> list[str]:
    """EIA weekly inventories: a negative weekly change is a draw, positive a build."""
    if not rows:
        return []
    out = ["## Energy inventories (EIA, weekly)", "| Series | Latest | Δ wk | Draw/Build | Units | As of |",
           "|---|---:|---:|---|---|---|"]
    for m in rows:
        change = m.get("change")
        flow = "n/a" if change is None else ("draw" if change < 0 else "build" if change > 0 else "flat")
        out.append(
            f"| {m['name']} | {formatting.fmt_num(m.get('latest'))} | "
            f"{formatting.fmt_num(change)} | {flow} | {m.get('units') or ''} | "
            f"{m.get('date') or 'n/a'} |"
        )
    out.append("")
    return out


def _positioning_table(rows: list[dict]) -> list[str]:
    """CFTC leveraged-fund (spec) net positioning + the week-over-week change."""
    if not rows:
        return []
    out = ["## Speculative positioning (CFTC, weekly)",
           "| Contract | Lev-fund net | Side | Δ wk | Asset-mgr net | As of |",
           "|---|---:|---|---:|---:|---|"]
    for m in rows:
        net = m.get("lev_net")
        side = "n/a" if net is None else ("net long" if net > 0 else "net short" if net < 0 else "flat")
        out.append(
            f"| {m['name']} | {formatting.fmt_num(net)} | {side} | "
            f"{formatting.fmt_num(m.get('lev_net_chg'))} | {formatting.fmt_num(m.get('asset_net'))} | "
            f"{m.get('date') or 'n/a'} |"
        )
    out.append("")
    return out


def _headline_list(news_items: list[dict], limit: int = 25) -> list[str]:
    out = ["## Top Headlines"]
    for item in news_items[:limit]:
        out.append(f"- **{item['title']}** — {item.get('source', '')}")
    out.append("")
    return out
