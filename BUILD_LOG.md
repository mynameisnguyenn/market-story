# BUILD_LOG — market-story

The project's running memory: **what exists, why, and where** — so a fresh Claude session (or
future-you) can recover state without trusting anyone's recollection. Append a dated entry per
substantial build (newest first). Source of truth for "did we build X?" Pairs with `CLAUDE.md`
(how it works), `DESIGN.md` (the look), and `git log` (the exact diffs).

---

## Current state (the map)

**What it is:** a daily global-markets Streamlit dashboard for a hedge-fund risk analyst, narrated
by Claude (Python gathers → brief JSON → Claude writes a thesis-first narrative → versioned logbook).

**Where it runs**
- **Local:** double-click `Launch Market Story.bat` (or the Desktop "Market Story" shortcut) → `localhost:8501`.
  Interpreter `~/anaconda3/python.exe`; git at `~/anaconda3/Library/bin/git.exe` (neither is on PATH).
- **Hosted:** `https://market-story-9kpggwcnhbucneaakauxjz.streamlit.app/` (Streamlit Community Cloud, repo
  `github.com/mynameisnguyenn/market-story`, branch `main`, auto-redeploys on push). **Currently PRIVATE**
  (login-gated) — set Sharing → Public for no-login phone access. Install as a PWA / Add to Home Screen.
- **Daily Action** (`.github/workflows/daily-brief.yml`, 12:00 UTC weekdays): runs `run.py`, commits the
  brief + timeline + history archives + running thesis + ledger; a weekday remote routine narrates ~12:45 UTC.

**Keys:** `.env` (gitignored) has FRED, EIA, SEC_USER_AGENT (BLS empty → keyless v1). Same go in Streamlit
**Secrets** for the hosted app; bridged via `app._load_cloud_secrets`. Keys never render in the UI.

**Design skill:** `market-story-design` (Claude Design export) installed at `~/.claude/skills/` AND committed
at `.claude/skills/market-story-design/` (canonical). Tokens match `styles.css`.

**Committed data (the "memory"):** `data/timeline.jsonl` (cross-asset metrics 1998→), `data/history/{energy,
labor,macro}.jsonl` (deep history), `data/running_thesis.md` (standing view), `data/scorecard_log.jsonl`
(prediction ledger), `data/narratives/*.md`. Briefs are gitignored but force-committed by the Action.

**Tests:** ~434 pytest, ~2 min. `tests/test_render_smoke.py` renders every tab hermetically.

**Dev/iteration loop (how Claude "sees" the product):** run `app.py` **locally** (`localhost:8501`) and
screenshot it with a headless browser (Playwright) — no Streamlit login involved. This is independent of the
hosted app, whose privacy only blocks *anonymous verification of the deployed instance*. Make the hosted app
**public** to let Claude also screenshot/verify the live deployed version after a push.

---

## In progress / pending
- **Surface the analytics library** (built + tested in `src/`): `riskmetrics` ✅ (Macro: Risk & drawdown),
  `regime_turbulence` + `composite` ✅ (Macro: Stress & danger panel), `rotation` ✅ (Equities: RRG chart),
  `breadth` ✅ (Equities: internals) — **still to surface:** `signal_ic`, `crisis`, `pmi_proxy`, `statistical`.
- **Tier-3 external data** (need new sources + reliability caveats, not pure): options/GEX, CME FedWatch +
  FOMC countdown, econ-calendar consensus/surprise.
- **Tier-4 UX:** quantstats-style tearsheet polish.
- **Make the hosted app public** (user action, Streamlit Cloud Sharing).

---

## Log (newest first)

### 2026-06-06 — Analytics surfacing batch 2
Wired 4 of the library modules into the dashboard: **regime_turbulence + composite** → a "Stress & danger"
panel on the Macro tab (Risk-off signals count + Kritzman turbulence stress %ile + danger flag + firing
conditions; the composite was reframed to NOT print a competing regime label next to `regime_panel`).
**rotation** → a "Sector rotation (RRG)" quadrant scatter on the Equities tab (long=120/short=20 to fit the
~1y embedded history). **breadth** → a "Sector breadth & internals" panel (advance/decline, % above 50d MA,
new highs/lows, McClellan). All degrade to nothing when history is short (render-smoke stays green).

### 2026-06-06 — Analytics module library + first surfacing
- **9 pure analytics modules + tests** drafted in parallel **on Sonnet**, integrated with formula review
  (`c27a4a8`): `riskmetrics`, `regime_turbulence` (Kritzman turbulence = smooth stress signal), `rotation`
  (RRG: RS-Ratio/RS-Momentum quadrants), `composite` (multi-condition danger flag), `pmi_proxy` (FRED
  diffusion index), `crisis` (window replay), `statistical` (Jarque-Bera + variance-ratio), `signal_ic`
  (alphalens-style IC), `breadth`. Added `scipy` dep. Fixed 3 draft bugs on the way in.
- **riskmetrics surfaced** as a Risk & drawdown panel on the Macro tab (`c2c5fff`).
- Set the **workflow model policy** (Sonnet for bounded/parallel agents, Opus for synthesis, Haiku trivial)
  — saved to auto-memory.

### 2026-06-06 — Accountability loop
- **Prediction ledger** (`7d6de22`): `src/ledger.py` + `data/scorecard_log.jsonl`. Accumulates every watch-block
  prediction, grades each AT ITS HORIZON (window) against committed data (macro archive + yfinance for single
  names — fixes the old scorecard that couldn't grade AVGO-type calls or multi-session horizons), running
  hit-rate on the Story tab. Backtest showed the prior scorecard kept no track record; this is the fix.
- **Running thesis** (`5aee69c`): `data/running_thesis.md` + `src/thesis.py`. The standing cross-session view
  (current thesis + flip condition, regime, multi-session watch, lessons) — the "string of context"; `/narrate`
  reads it at the start and revises it after. Shown on the Story tab.

### 2026-06-06 — Distribution surfaces
- **Email digest** (`e128a84`): `src/email_digest.py` renders the brief+narrative to email-safe HTML.
- **Design skill version-controlled** (`1a074fb`, `e87bd3d`): the `market-story-design` skill into the repo
  (fixed a gitignore inline-comment bug that dropped its PNG assets).

### 2026-06-04 — Ellis-dark redesign + multi-device
- **Ellis-dark theme** (`ec8c27c`, `50a48e4`): extracted CSS → `styles.css` (token-driven) + `style_lab.py`
  sandbox + `DESIGN.md`; warm near-black + electric-cyan, Instrument Serif headline over IBM Plex Mono;
  one green/one red unified; mobile `@media` + sidebar auto-collapse; surfaced the narrative read (Story → tab 2,
  thesis hero on Overview, never-blank `derive_lead`); `**bold**` section labels → real subheaders. Borrowed
  from ellis.com (Next.js/Tailwind/Vercel).
- **Multi-device** (`364495d`): fixed the broken laptop launcher (`python` was the MS Store stub → full
  Anaconda path), Desktop shortcut, PWA polish (page_icon, minimal toolbar), DEPLOY.md install steps.

### 2026-06-04 — Deep history archives + smart money
- **Committed full-history archives**: EIA energy to 1982 (`c3c22d6`, fixed the blank panel — reads from disk,
  no live key), BLS labor to 1947 + full FRED (`254107d`). Generic helper `src/series_archive.py`.
- **13F smart-money tracker** (`72b5cc6`, `2994ed3`): prominent managers' holdings + QoQ flow (EDGAR 13F-HR,
  CUSIP-keyed, thousands-vs-dollars normalized) on the Calendar tab.
- **Fixes**: stale 2024-25 S&P positioning (`e0c51df`); era framing on Overview (`e855629`); LF/line-ending +
  backfill + era_for review fixes (`2171963`).
