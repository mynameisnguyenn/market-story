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
  claims, unemployment, industrial production — each with a **1-year percentile + z-score**.
- **Energy inventories (EIA)** — weekly crude / gasoline / distillate / SPR stocks +
  natural-gas storage, with the week-over-week **draw/build**.
- **Positioning (CFTC)** — leveraged-fund (spec) **net positioning** + weekly change for
  S&P / Nasdaq / VIX / Treasury futures, against asset-manager (real-money) net.
- **Labor & inflation (BLS)** — CPI, core CPI, payrolls, unemployment, earnings, participation.
- **Filings (SEC EDGAR)** — recent material filings for your watchlist names.
- **News** — 12 RSS feeds, de-duplicated and noise-filtered, newest first.

## The read — analytics that turn data into signal

The dashboard doesn't just tabulate; it interprets:

- **Statistical context** — every macro anchor (and cross-asset market: VIX, yields, credit,
  FX, oil/copper/gold) shows its **1-year percentile + z-score** — is HY OAS *historically*
  tight, is the curve at its flattest of the year?
- **Vol risk premium** — VIX vs 20-day realized volatility (a wide premium = complacency).
- **Hedge regime** — rolling **stock-bond return correlation** (positive = your Treasury hedge
  is broken), with a sign-flip flag.
- **"Today's read"** — a synthesized one-line **thesis** classifying the tape (e.g. *duration
  unwind vs credit de-risking*, *geopolitical premium vs reflation*) plus the evidence it rules out.
- **Thesis scorecard** — each narrative emits a machine-readable `watch` block; the next session
  **grades it** (hit / watching) — a running track record of the calls.
- **Metrics timeline** — `data/timeline.jsonl`, an append-only daily record (committed) that
  builds long-horizon context as it accrues.

## Methodology

1. **Market data** via `yfinance` — one batched daily-history pull; per-symbol snapshots
   compute 1-day, 1-week, and YTD change with zero-division/NaN guards.
2. **Macro** via FRED — the **keyed API** when `FRED_API_KEY` is set (reliable under the
   concurrent burst), else the keyless `fredgraph.csv` endpoint; retried, with a 1-year
   percentile + z-score per series. BLS/EIA/CFTC are separate best-effort fetchers.
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
src/market_data.py  yfinance (+ stooq fallback) + snapshot math
src/macro_data.py   FRED (keyed-first, keyless fallback) + 1y percentile/z
src/bls_data.py     BLS labor & inflation prints
src/eia_data.py     EIA weekly energy inventories
src/cftc_data.py    CFTC speculative positioning (COT)
src/edgar_data.py   SEC EDGAR watchlist filings
src/analytics.py    cross-asset extremes, vol premium, stock-bond corr
src/signals.py      signal lines + the "today's read" thesis (derive_lead)
src/regime.py       risk-on/off regime panel
src/scorecard.py    grade a narrative's watch block vs the next brief
src/timeline.py     append-only daily metrics timeline (committed)
src/history.py      local SQLite day-over-day snapshots
src/news.py         RSS aggregation, de-dupe, noise filter
src/brief.py        assemble + persist brief (json + md)
src/formatting.py   pct/bps/color helpers
.claude/commands/narrate.md   the /narrate project command
data/briefs/        brief_*.json / .md     (committed by the daily Action)
data/narratives/    narrative_*.md         (committed logbook; written by Claude)
data/timeline.jsonl append-only daily metrics record (committed)
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

127 tests, synthetic data only (no network): snapshot math (known-answer), movers/breadth,
FRED/BLS/EIA/CFTC snapshotting, the analytics (1y percentiles, vol premium, stock-bond
correlation), the "today's read" classifier, the thesis scorecard + metrics timeline, news
cleaning/de-dupe, an offline render-smoke of every tab, and a regression suite carried over
from two whole-codebase adversarial bug audits.

## Daily workflow

1. `python run.py` (or just hit **Refresh data** in the dashboard).
2. `python -m streamlit run app.py`.
3. In `claude`: *"narrate today's brief"* — get the story + risk lens, then ask anything
   ("why did the curve steepen?", "what's the read on energy?"). Re-run any day.

## Recently added

- **More credible sources** — direct **BLS**, **EIA** energy inventories, **CFTC** positioning,
  and **SEC EDGAR** filings (all keyless or free-key, best-effort, never crash the dashboard).
- **An analytics layer** — 1-year percentiles/z-scores, cross-asset extremes, the vol risk
  premium, and a stock-bond correlation (hedge) regime.
- **A synthesized "today's read"** thesis + a **thesis scorecard** that grades each call against
  the next session, and a committed **metrics timeline** for long-horizon context.
- **Reliability** — keyed-first FRED with retry (no more dropped series); editable watchlist;
  earnings + filings calendar; a public splash page; a daily GitHub Action that commits the
  brief + timeline.

## Ideas to extend

The data and analytics layers are deliberately complete — the value now is *using* it daily
(read the narrative, argue with the thesis, watch the scorecard). If anything:

- True multi-year percentiles + trend charts once `timeline.jsonl` accumulates a few months.
- A forward economic-calendar feed (CPI / NFP / FOMC dates) alongside earnings.
