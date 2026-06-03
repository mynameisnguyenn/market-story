# CLAUDE.md — market-story

Daily global-markets intelligence tool for a hedge-fund **risk analyst**. It scrapes
free market data + macro + news every day, assembles a structured **brief**, and turns
it into a written **market story** with a risk lens. Built to sharpen market acumen and
to be re-run and questioned daily.

## Architecture (read this before editing)

Two layers, deliberately split:

1. **Gather + display (Python / Streamlit)** — `run.py` and `app.py`. NO LLM here.
   - `run.py` fetches everything and writes a structured brief to
     `data/briefs/brief_YYYY-MM-DD.json` (+ a human-readable `brief_YYYY-MM-DD.md`).
   - `app.py` is the Streamlit dashboard: charts, sector heatmap, rates/FX/commodities,
     headline feed, and a "Today's Story" panel that renders the latest narrative file.

2. **Synthesize (Claude Code = the brain).** There is no API key. The narrative and all
   follow-up Q&A are produced by *me, Claude*, when the user runs `claude` in this folder.

### The brain loop (how I narrate — IMPORTANT)

When the user says "narrate today's brief", runs `/narrate`, or asks a market question:

1. Read the newest file in `data/briefs/` (e.g. `brief_2026-06-03.json`). If none exists,
   tell them to run `python run.py` first.
2. **Load memory (stateful narration — this is what stops the read feeling "light"):**
   read the *previous* brief (second-newest `brief_*.json`) and diff the cross-asset
   anchors (VIX, 2s10s/5/10/30Y yields, DXY, oil, gold/copper, HY/IG OAS); also read the
   most recent prior `data/narratives/narrative_*.md` and follow up on its "what to watch".
   Each macro row carries `pct_1y` (1-year percentile of the level) — use it to call out
   what's *stretched* (e.g. HY OAS at the 3rd %ile = historically tight; 2s10s at the 0th
   = flattest of the year), not just the day's move.
3. Write the story to `data/narratives/narrative_YYYY-MM-DD.md` (same date as the brief),
   using this structure:
   ```
   # Market Story — {date}
   ## Since last time   (grade last session's `watch` items: hit / miss / pending)
   ## Today in one line (ONE falsifiable thesis + its flip condition — the spine)
   ## TL;DR             (≤3 bullets; each states a consequence for risk, not just a move)
   ## What moved & why  (importance-ranked; demote quiet asset classes to a single line)
   ## Macro & data      (FRED + pct_1y extremes, BLS, EIA draws/builds, CFTC positioning, events)
   ## Risk lens         (positioning, correlations breaking, tail risks — the sharpest section)
   ## What to watch     (3–5 numeric triggers + a machine-readable ```watch block to grade)
   ## Sources           (headlines + feeds the read leans on)
   ```
   See `.claude/commands/narrate.md` for the full spec (thesis-first, the `watch` block format).
4. The dashboard auto-displays this file in the "Today's Story" tab — no extra step.
5. Ground every claim in the brief's numbers/headlines; prefer day-over-day deltas over
   levels. Don't invent prints. If you pull in outside knowledge or live web context, say
   so. Keep the **risk lens** sharp — this user is a risk analyst, not a retail trader.

For follow-up questions ("why did the curve steepen?", "what's the read on XLE?"),
answer from the brief first; only fetch more (WebSearch/yfinance) if the brief lacks it.

## Brief JSON shape (contract between the two layers)

```jsonc
{
  "date": "2026-06-02", "generated_at_utc": "...", "session_label": "US close",
  "markets": {
    "us_equities": [{ "symbol": "^GSPC", "name": "S&P 500", "last": 5xxx, "change_pct": 0.4, "change_1w_pct": ..., "ytd_pct": ... }],
    "global_indices": [...], "sectors": [...], "rates": [...], "fx": [...],
    "commodities": [...], "credit": [...]
  },
  "macro": [{ "id": "DGS10", "name": "10Y Treasury", "latest": 4.2, "date": "...", "prev": 4.18, "change": 0.02, "pct_1y": 91, "z_1y": 1.5 }],
  "bls":   [{ "id": "CUUR0000SA0", "name": "CPI-U, all items", "latest": ..., "date": "2026-04", "change": ..., "yoy_pct": ... }],
  "energy":[{ "id": "WCESTUS1", "name": "Crude oil (ex-SPR)", "latest": 433712, "date": "2026-05-29", "prev": 441686, "change": -7974, "units": "MBBL" }],
  "positioning":[{ "name": "S&P 500 (e-mini)", "lev_net": -457780, "lev_net_chg": -56226, "asset_net": 1003607, "oi": 2093621, "date": "2026-05-26" }],
  "movers": { "leaders": [...], "laggards": [...] },
  "news": [{ "title": "...", "source": "...", "published": "...", "link": "...", "summary": "..." }],
  "stats": { "vix": 14.2, "advancers": 7, "decliners": 4 }
}
```

## How to run

```bash
python run.py            # fetch data + news, write today's brief
streamlit run app.py     # open the dashboard
# then in claude: "narrate today's brief"  (or /narrate)
```

## Conventions (inherits global rules in ~/.claude/rules/)

- Python 3.13+, PEP 8, snake_case; constants UPPER_CASE (`TRADING_DAYS = 252`).
- pandas-first; functions < 60 lines, files < 500 lines; one-line docstrings.
- **Guard every division** (zero vol, empty series). Always handle NaN / missing data —
  feeds and tickers fail constantly; degrade gracefully, never crash the dashboard.
- No network calls in tests — synthetic data only, `np.random.seed(42)`.
- No hardcoded paths — use `pathlib.Path` rooted at the project dir (see `src/config.py`).
- Secrets via `.env` only; never commit keys (FRED + EIA keys live in `.env` and as GitHub
  repo secrets; bridged to Streamlit Cloud via `_load_cloud_secrets`).
- **Scope discipline:** the value is the daily *read*, not data breadth. The credible-source
  stack (FRED/BLS/EIA/CFTC/SEC/yfinance/RSS) is deliberately complete — don't add more
  instruments/feeds/options/intraday/crypto/backtester without a clear reason. Sharpen the
  narrative, the analytics, and the design instead.

## Layout

```
run.py            entry point: gather -> brief
app.py            streamlit dashboard
src/config.py     instruments, feeds, FRED series, paths
src/market_data.py  yfinance (+ stooq fallback)
src/macro_data.py   FRED (keyless CSV or fredapi)
src/news.py         RSS aggregation + dedupe
src/brief.py        assemble + save brief (json + md)
src/formatting.py   pct/color helpers
data/briefs/        brief_*.json / .md   (gitignored)
data/narratives/    narrative_*.md       (gitignored; written by Claude)
tests/              pytest, synthetic data
```
