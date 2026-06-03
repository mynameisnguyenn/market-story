# market-story

A daily, re-runnable **global-markets intelligence** tool. It scrapes free market
data, macro series, and financial news every day, assembles a structured **brief**,
and turns it into a written **market story with a risk lens** — built to sharpen
market acumen and to be questioned and re-run.

Two layers, deliberately split:

- **Gather + display** — a Python pipeline + **Streamlit dashboard** (charts, sector
  map, rates/FX/commodities, live headline feed).
- **Synthesize** — *Claude Code is the brain*. The dashboard writes a structured brief;
  you ask Claude to narrate it and answer follow-ups. No API key, no LLM bill.

```
  Double-click "Market Story" on your Desktop   # one-click: opens the dashboard in your browser
  # — or from a terminal —
  python run.py                    # gather data -> data/briefs/brief_<date>.json + .md
  python -m streamlit run app.py   # open the dashboard
  claude  ->  "narrate today's brief"  (or /narrate)   # writes the story; Story tab shows it
```

Two pages (sidebar nav): **Daily Brief** (live markets) and **Learn the Markets** (researched
foundations — history timeline, players, the Fed, and money-flow Sankey diagrams). To host it
as a public website, see `DEPLOY.md`.

## What it covers

- **US equities & sectors** — S&P / Nasdaq / Dow / Russell / VIX, all 11 SPDR sectors.
- **Global macro** — Euro Stoxx, FTSE, DAX, CAC, Nikkei, Hang Seng, Shanghai; Treasury
  yields (with bps moves); DXY + major FX; WTI/Brent/gold/silver/copper/nat-gas; HY/IG
  credit and Treasury ETFs.
- **Macro prints (FRED)** — 18 risk-relevant series: the curve (2s10s, 10s3m), EFFR/SOFR,
  HY & IG credit spreads, breakevens, NFCI financial conditions, CPI/core-PCE, payrolls,
  claims, unemployment, industrial production.
- **News** — 12 RSS feeds, de-duplicated and noise-filtered, newest first.

## Methodology

1. **Market data** via `yfinance` — one batched daily-history pull; per-symbol snapshots
   compute 1-day, 1-week, and YTD change with zero-division/NaN guards.
2. **Macro** via FRED's keyless `fredgraph.csv` endpoint (no API key needed; set
   `FRED_API_KEY` in `.env` only if you want the `fredapi` fallback / metadata).
3. **News** via `feedparser` over a curated, **liveness-validated** feed list.
4. **Brief** assembled into `data/briefs/brief_<date>.json` (the contract Claude reads)
   plus a human-readable `.md` facts sheet.
5. **Narrative** written by Claude into `data/narratives/narrative_<date>.md`, rendered
   in the dashboard's **Story** tab.

### Source validation (why these feeds)

The feed list was validated against live sources. Excluded as **dead/frozen**: all WSJ
`feeds.a.dj.com` feeds (stale since Jan 2025), Reuters legacy RSS (DNS retired), and
MarketWatch `marketpulse` (frozen content behind a *misleadingly fresh* timestamp).
Included (live): CNBC Finance + Economy, MarketWatch top-stories/bulletins, FT, Yahoo
Finance, Investing.com markets, NYT Economy, Fed press, Nasdaq, BBC Business, Seeking Alpha.

Two real gotchas are handled in code:
- **FRED blocks browser User-Agents** on the CSV endpoint → we send the default UA.
- **News feeds block the default UA** → we send a browser UA. (Opposite requirements.)
- `^TNX`/`^FVX`/`^TYX`/`^IRX` are **yields in percent** (4.45 = 4.45%); 1-day moves are
  shown in **basis points**. `DX-Y.NYB` is the only DXY symbol Yahoo resolves. Shanghai
  (`000001.SS`) often carries a trailing-NaN bar, which we drop.

## Project structure

```
run.py              entry point: gather -> brief
app.py              streamlit dashboard (pure builders + st wrappers)
src/config.py       instruments, feeds, FRED series, paths
src/market_data.py  yfinance fetch + snapshot math
src/macro_data.py   FRED (keyless CSV, optional fredapi)
src/news.py         RSS aggregation, de-dupe, noise filter
src/brief.py        assemble + persist brief (json + md)
src/formatting.py   pct/bps/color helpers
.claude/commands/narrate.md   the /narrate project command
data/briefs/        brief_*.json / .md   (gitignored)
data/narratives/    narrative_*.md       (gitignored; written by Claude)
tests/              pytest, synthetic data only
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env       # optional: add FRED_API_KEY (not required)
```

Built/tested on **Python 3.14** (3.13+ fine). Note: if `streamlit` isn't on PATH, use
`python -m streamlit run app.py`.

## Testing

```bash
python -m pytest tests/ -v
```

53 tests, synthetic data only (no network): snapshot math (known-answer), movers/breadth,
FRED snapshotting, news cleaning/de-dupe, the dashboard's figure/table builders, the custom
watchlist store, earnings-calendar parsing, day-over-day snapshots, and the risk-regime read.

## Daily workflow

1. `python run.py` (or just hit **Refresh data** in the dashboard).
2. `python -m streamlit run app.py`.
3. In `claude`: *"narrate today's brief"* — get the story + risk lens, then ask anything
   ("why did the curve steepen?", "what's the read on energy?"). Re-run any day.

## Recently added

- **Editable watchlist** — add/remove tickers in the Equities tab, persisted to `data/watchlist.json`.
- **Earnings calendar** — a Calendar tab of upcoming earnings for your names + indices (yfinance).
- **Day-over-day deltas** — a "Since last session" panel backed by a local SQLite snapshot store.
- **Risk-regime read** and a **Treasury yield-curve** chart on the Macro tab; **keyword filter** on Headlines.
- **Scheduled pre-market run** — `.github/workflows/daily-brief.yml` builds the brief each weekday.

## Ideas to extend

- Cross-asset correlation matrix and rolling-beta views.
- Trend charts off the SQLite history once a few sessions have accumulated.
- An economic-calendar feed (CPI / NFP / FOMC dates) alongside earnings.
