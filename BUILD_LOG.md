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

**Tests:** 436 pytest, ~9s. `tests/test_render_smoke.py` renders every tab hermetically.

**Dev/iteration loop (how Claude "sees" the product):** run `app.py` **locally** (`localhost:8501`) and
screenshot it with a headless browser (Playwright) — no Streamlit login involved. This is independent of the
hosted app, whose privacy only blocks *anonymous verification of the deployed instance*. Make the hosted app
**public** to let Claude also screenshot/verify the live deployed version after a push.

---

## In progress / pending
- **Analytics library surfaced (9/9 — COMPLETE):** `riskmetrics` ✅ (Macro: Risk & drawdown + a Trend col
  from `statistical`), `regime_turbulence` + `composite` ✅ (Macro: Stress & danger), `rotation` ✅ (Equities:
  RRG), `breadth` ✅ (Equities: internals), `crisis` + `signal_ic` ✅ (Trends: crisis replay + Signal IC),
  `pmi_proxy` ✅ (Macro: Growth pulse — diffusion of INDPRO + payrolls + inverted claims, no new feed).
- **Tier-3 external data:** `FOMC countdown` ✅ (Calendar, static Fed schedule). **Deliberately NOT built —
  no reliable free source + against CLAUDE.md scope discipline:** CME FedWatch rate-cut probabilities (needs
  Fed-funds-futures strip / CME data), options/GEX (needs full chains; "no options" rule), econ-calendar
  consensus/surprise (no free consensus feed). Revisit only if a clean data source appears.
- **Tier-4 UX:** quantstats-style S&P tearsheet ✅ (Trends). Further tearsheet polish optional.
- **Make the hosted app public** (user action, Streamlit Cloud Sharing) — still the one open user action.

---

## Log (newest first)

### 2026-06-10 — The accountability slate: 9 ambitious features design-grilled, 8 shipped descoped, 1 cut
User asked for all nine ambitious features WITH a continuous adversarial grill on each. Ran a 28-agent
design-grill workflow first (per-feature designer + efficacy critic + engineering critic + Opus synthesis):
**zero features survived as designed** — 8 shipped in grill-descoped form, 1 cut. The grill caught 4 bugs
pre-build: a `pct_change()`-on-a-yield sign error (would have shown GFC bonds −43%), a turbulence alert that
would silently no-op forever (`stress_pct` never reaches the brief JSON), a meaningless conviction-weighted
Sharpe, and a forward-return "distribution" with ~1–2 effective dof. What shipped:
- **Stance ledger (paper P&L of the daily call):** mandatory ```stance block (`{"direction": -1|0|1, "notes"}`)
  in every narrative ≥ 2026-06-10; a MISSING block logs as `omitted` (selection-bias guard). `scorecard.parse_stance`,
  `ledger.log_stances_from_narratives/settle_stances/stance_stats` (kind="stance" rows in scorecard_log.jsonl,
  settled with the NEXT session's `spx_chg` from the committed timeline). Story tab shows win-rate/flat/omitted;
  equity curve deliberately deferred to 63 settled sessions. 4 grill-trap guards each pinned in `test_stance.py`
  (backfill rewrite preserves stances; grade_pending skips them; watch stats exclude them; probability 0.0 survives).
- **Calibration (infra only, zero UI):** optional `probability` on watch items → stored in `confidence`;
  `src/calibration.py` (Brier, bins, MIN_N=30). Panel deliberately deferred ~90 days until real probabilities exist.
- **VIX-episode analogues** (`src/analogues.py`, Trends expander): nearest full-history VIX-percentile days,
  episode-deduped (≥21 sessions), era labels, where fear went next (+5/+21 sessions). NO forward S&P returns —
  the grill's hard line. Vectorized (a per-row rank would have been O(n²) over 7k sessions).
- **FOMC event study** (`src/event_study.py`, Calendar expander): 224 scheduled decision dates 1998–2025
  (emergency meetings excluded), T+1/2/5 compounded drift, median + iid-bootstrap CIs (defensible: ~6-week
  spacing → windows never overlap). If all CIs straddle zero the panel LEADS with "no detectable drift" —
  the honest null is the deliverable. ⚠ Date provenance: 3 agreeing model-knowledge passes; NOT yet verified
  against live federalreserve.gov (fetch was down at build time) — see TODO in the file before citing n.
- **Growth & inflation pulse** (Macro): quadrant feature descoped to a second diffusion metric (CPI momentum)
  beside the growth pulse, each stamped with its own data-through month. No quadrant labels (51/49 flips on
  an INDPRO revision), no per-quadrant asset stats (stagflation n ≈ one episode).
- **Proxy-book stress** (`src/proxy_books.py`, Macro expander): 100% SPX vs 70/30 through the crisis windows;
  bond leg = −8 × Δy (explicit duration constant; the sign test is pinned in tests). No HY OAS leg (zero
  coverage of all three windows). Labeled illustrative.
- **Phone alerts** (`src/alert_rules.py` + `src/notifier.py` + `scripts/send_alerts.py` + Action step):
  VIX-only dual gate (level ≥ 25 AND 1y-pct ≥ 80), ntfy.sh transport (NTFY_TOPIC secret; topic never logged;
  timeout=10), always-exit-0. Turbulence rule cut (data lie). Setup in SETUP.md. No dashboard panel.
- **Scenarios → one bolded line** in running_thesis.md (narrate.md spec); third machine-readable format killed.
- **Brain-memory CUT** to a narrate.md nudge: near-miss triggers are threshold-calibration problems — fix the
  level, not the view; always cite n. (Per-series hit-rate table = regime anecdote at n≤5.)
- Shared infra: `src/timeline_returns.py` (rows_after/next_session_chg/level_after/compound_pct). Story-tab
  latent crash fixed (watch table KeyError on stance rows). Render smoke now uses a 320-session 2020 synthetic
  timeline so the new panels exercise instead of no-opping; + a stance row in the ledger fixture.
- VERIFICATION (all complete): **600 tests pass** (452 → +148). All 4 changed tabs screenshot-verified live,
  expanders opened, zero exceptions (FOMC-drift honest-null box fires; proxy-books shows both books across
  crises; analogues leak no forward S&P returns). **FOMC dates Fed-verified 2026-06-10** against
  federalreserve.gov (2021-25 exact; 1998-2019 swept) — found + fixed one real error: `2020-03-18` was a
  CANCELLED meeting (now 223 dates). An 18-agent adversarial review raised 14 issues, 10 verified real, all
  fixed: backfill was wiping watch `asof_value` every run (data loss); analogue caption claimed the buy-fear
  edge regardless of today's VIX regime; FOMC honest-null gate misread an n=0 horizon; alert Action step
  lacked `continue-on-error`; flat-stance P&L encoded as 0.0 vs None; + 5 lower-sev edges. 4 regression tests
  pin the worst (asof preservation, flat-pnl, bootstrap n_boot=0 guard, the 2020 date). Built initially during
  a `claude-fable-5` model-setting outage that blocked the classifier; verified in full once switched back to
  Opus 4.8 (the same pytest command that failed ~12× then ran clean — the proof the name was unloadable).

### 2026-06-07 — Deep review (5-dimension workflow) — fixed 1 crash + a degradation/correctness cluster
After the `line_fig` overlay bug (which the 449-test suite rendered but didn't catch), ran a 5-dimension
deep-review workflow (render hazards · None/NaN degradation · numeric correctness · integration/contracts ·
diff scan), each candidate adversarially verified: 30 candidates → 12 confirmed, 4 plausible, 14 refuted.
Fixed the real ones:
- **HIGH — Overview crash on a partial brief** (`overview.py`): `brief["movers"]` was a bare subscript; the
  nonce=0 fast-load serves whatever JSON is on disk with no schema check, so an old/partial brief (missing
  `movers`) `KeyError`-crashed the whole tab. Now `brief.get("movers") or {}` + `.get("leaders"/"laggards")`.
  Same hardening applied to the page header (`app.py` `session_label`/`generated_at_utc`/`stats`) and the
  Macro vol-premium caption (`vol["premium"]` → guarded). A new render-smoke test renders the Overview from
  a partial brief (incl. a None-`change_pct` mover) and asserts it degrades, not crashes; +2 pure
  `derive_signals` tests for the None-mover guard (`signals.py`).
- **MED — "1Y" range button was `step="all"`** (`charts.py`): mislabeled — showed all data, not one year.
  Now an actual 1-year backward step.
- **LOW correctness/display**: PMI growth-pulse x-axis labeled month-START (`pmi_proxy.composite_index`
  `to_timestamp(how="end")`); Risk & drawdown `DD days` was outside the Styler format (rendered `"None"` →
  now `—`); Stress & danger used a fixed 3 columns leaving a gap when turbulence is absent (now sizes to
  what's available); tearsheet caption flags the latest month/year as partial (MTD/YTD); FOMC panel nudges
  to refresh the schedule once it's exhausted (post-2027); BLS YoY now allows a 0.0 year-ago for rate series
  (was skipped by a truthiness check) while still guarding division for ratio series.
- Deliberately NOT changed: `pmi_proxy._rolling_std` ddof=0 (kept — consistent with the percentile/z ddof=0
  unification, documented, ~negligible effect). 14 refuted candidates needed no action.
- 452 tests pass; Macro/Overview verified live (no stException).

### 2026-06-07 — Signal-validation backtest + close-the-loop honesty pass
Asked the honest question after surfacing 9 analytics modules: **does any of it actually predict
forward S&P returns?**
- **`src/backtest.py`** (+8 tests) — the certified engine: strictly-future returns (no lookahead),
  moving-block-bootstrap CIs (overlapping forward windows make naive t-stats lie), level-vs-change,
  sub-period stability. Tests pin the guards (perfect predictor → significant; pure noise → not).
- **`research/signal-validation.md`** + **`research/signal_battery.py`** — the study: every dashboard
  signal over the 28-yr committed timeline, independently reproduced + adversarially refuted by a
  4-agent workflow (all four confirmed). **Verdict: only VIX *level* has a robust, regime-stable,
  economically-meaningful edge** (buy-fear; positive in all 6 regimes; survives dropping GFC+COVID).
  The 10Y-yield relationship is real but regime-conditional (sign *flipped* +0.32 in the 2022 inflation
  shock). Gold/HY/IG "edges" are artifacts (non-stationary trend / 3-yr backfilled single regime —
  change-form null). The 2s10s curve, dollar, positioning, vol premium, and the **Kritzman turbulence +
  "Market stress" gauge are non-predictive (descriptive, not alpha)**. 16/48 level tests significant vs
  ~2.4 by chance — only VIX survives the deeper tests.
- **Close-the-loop honesty pass** — made the dashboard tell that truth: the Signal-IC panel (Trends) now
  carries an **"Edge (28y test)"** column (VIX ✓ robust / 2s10s ✗ / HY OAS ⚠ short-sample / vol-premium ✗)
  and includes VIX level; the Stress & danger panel (Macro) now states the turbulence gauge is
  **descriptive, not predictive** ("a thermometer, not a forecast"). Both link `research/signal-validation.md`.
- Did NOT backfill historical narratives/predictions — that would be hindsight fabrication (the exact
  lookahead the backtest eliminates) and would poison the ledger. The numerical/era context already spans
  every day to 1998 (timeline + eras + Time Machine); the *written* record stays a genuine forward log.
- 449 tests pass; both UI changes verified live via the screenshot loop.

### 2026-06-06 — Finished the feature slate (analytics 9/9, FOMC, tearsheet) + flagged cleanup
Knocked out the remaining backlog:
- **`pmi_proxy` surfaced** (`43213e3`) — the 9th and last analytics module. Added `composite_index`
  (`fa8b1bc`): a sign-aware, frequency-aligned diffusion SERIES (not just the scalar `composite_pmi`).
  Macro tab "Growth pulse" = momentum of INDPRO + payrolls + (inverted) initial claims, each normalized
  by its own 12-mo vol → 0-100 (>50 accelerating). Built from the committed FRED archive — **no new feed**.
  A free-data ISM analog (ISM's own PMI is license-restricted off FRED). The analytics library is now 9/9.
- **FOMC countdown** (`286608d`) — Calendar tab leads with the next FOMC rate-decision day. Static schedule
  (`calendar_data.FOMC_DECISIONS`, from the Fed's published calendar, verified 2026-06; refresh annually),
  so no fragile runtime feed. `next_fomc(today)` + test.
- **quantstats-style S&P tearsheet** (`43213e3`) — Trends tab: CAGR / vol / Sharpe / Sortino / Calmar /
  max-DD + a year×month return matrix (green/red, FY% compounding), from the committed timeline + riskmetrics.
- **Cleanup** (`43213e3`) — promoted the 3 cross-module dashboard helpers the adversarial review flagged
  (`color_changes`, `tone_span`, `TONE_HEX`) to public names.
- **Verified the daily-narrate remote routine is healthy** — `trig_01Acbc…`, cron `45 12 * * 1-5`, enabled,
  last fired 2026-06-05 12:45 UTC, next Mon 2026-06-08. (No code; status check via the routines API.)
- 441 tests pass; PMI/tearsheet/FOMC all verified live via the screenshot loop (none are exercised with real
  data by the hermetic render-smoke — their synthetic fixtures lack INDPRO/PAYEMS/ICSA and `spx`).

**Deliberately NOT built (with reasons):** CME FedWatch probabilities, options/GEX, econ-calendar
consensus/surprise — each needs a paid/scraped/proprietary source and runs against the scope-discipline rule;
shipping fragile scrapers would erode the daily read. Documented in the pending section for if a source appears.

### 2026-06-06 — The two deferred items, done (+ a bonus bug the live screenshot caught)
After the feature work above shipped to `main`, did both previously-deferred items as isolated commits:
- **Brief-accessor dedup** (`5912b5e`): `src/brief_access.py` (`market_row` / `macro_row` / `bls_row`) —
  `composite`, `signals`, and the dashboard's `row_for` all reference the one definition now.
- **Split `app.py` 1140 → 107 lines** into a `src/dashboard/` package: `charts.py` (pure builders,
  no Streamlit, unit-tested) → `widgets.py` (st render wrappers) + `data.py` (cached loaders +
  plumbing) → `panels/*.py` (one module per tab) → `app.py` (wiring + re-exports of the `app.X`
  surface tests use). Every file now under the 500-line convention (largest `charts.py` = 249). The
  two cross-tab figure builders became `charts.trend_fig` / `charts.level_fig` (public). Clean DAG,
  no import cycles, cached loaders are shared objects so `app.get_*.clear()` still works.
- **Bonus fix** (`04ededa`): the live screenshot caught the vol-premium inversion ALSO living in
  `signals.derive_lead` (`signals.py:147`) — it drives the Overview's "Today's read" banner, the most
  visible line on the landing page. "(hedges look cheap)" → "(protection rich)" for prem>3. Bug-fix
  #3 had only covered app/composite/analytics; the hermetic tests can't see banner copy, the screenshot did.
- **Verified**: 436 tests pass; live Playwright screenshots of all tabs render with no exception; and a
  3-dimension adversarial-review workflow (reference-completeness · behavior-drift vs the pre-split
  monolith in git · import/cache safety) found no high/medium issues — only stale doc pointers in
  `DESIGN.md` / `style_lab.py` (fixed) and convention nits. **Dev/iteration loop note:** the live
  screenshot pass remains essential — it catches UI-copy bugs (this one) that hermetic render-smoke can't.

### 2026-06-06 — Deep-review bug fixes + Wave 1 (polish) + Wave 2 (structure)
Acted on the deep review (code/usability/UI). **3 accountability-integrity bug fixes** (`8864e21`)
— they each made the dashboard *look* more trustworthy than it was:
- **Sortino** (`src/riskmetrics.py`): downside deviation divided squared shortfalls by the count
  of down-days only; per Estrada/empyrical it's `sqrt(mean(min(r,0)^2))` over ALL returns — the
  old form understated Sortino ~40%.
- **Ledger horizon grading** (`src/ledger.py`): level metrics (yields/prices) were "triggered" if
  the trigger was hit at ANY point in the window, inflating the hit-rate. Level metrics now grade at
  the END of the horizon; only event metrics (`:change_pct`/`:pct`) keep any-point semantics. +2
  regression tests pin the distinction.
- **Vol-premium label** (`app.py`, `composite.py`, `analytics.py`): a high VIX-minus-realized premium
  was captioned "complacency / cheap-looking hedges" — self-contradictory and inverted. Elevated
  implied-vs-realized = protection priced RICH (paying up for hedges), the opposite of complacency.

**Wave 1 polish** (`5169195`): composite DANGER flag now renders a red "risk-off" delta (was the same
neutral grey as every metric — unacceptable on a risk desk); colored the signed columns that were
monochrome (Sortino on Risk & drawdown, Return % on Crisis replay, IC 1d/5d/21d on Signal edge); the
Signal IC table shows `n` per signal + a caveat when HY OAS is short-sampled (FRED license-limited to
~3y); cached `timeline.load_df()` behind `get_timeline_df()` (the Trends tab was re-parsing ~7k rows
every rerun) and render-smoke clears it.

**Wave 2 structure** (`02e6979`): **unified the percentile/z math** — `analytics._pct_z` (population
std, ddof=0) and `macro_data._stat_context` (sample std, ddof=1) silently disagreed; `analytics.pct_z`
is now the single source of truth and `_stat_context` delegates (percentile unchanged, z now
consistent). **Regrouped the Global & Macro tab read-first**: risk view (regime → stress & danger →
risk & drawdown → vol premium → extremes → correlations) leads, then market tables + rates/FX charts,
then macro data — the risk-lens panels used to be split top-and-bottom. **Trimmed the duplicate "US
Sectors" flat table** on Equities (already shown as treemap + RRG + breadth). Verified via the local
Playwright screenshot loop.

**Deferred at the time (both DONE the same day — see the next entry):** the `_macro_row` dedup and
the `app.py` split. Originally held back as over-engineering / refactor-risk; the user said "go ahead"
so both were done as their own isolated, separately-verified commits after the feature work shipped.

### 2026-06-06 — Analytics surfacing batch 3 (library 8/9 surfaced)
`statistical` → a "Trend" column (trending / mean-reverting / random) on the Macro Risk & drawdown table.
`crisis` + `signal_ic` → Trends tab: a "Crisis replay" table (S&P through GFC/COVID/2022 from the 28y
timeline: return, max DD, VaR95, ES95) and a "Signal edge — Information Coefficient" table (2s10s / HY OAS /
vol-premium vs forward S&P returns). `pmi_proxy` deferred — needs ISM-proxy FRED series we don't fetch yet.

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
