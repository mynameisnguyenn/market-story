---
description: Read today's market brief and write the narrative the dashboard displays
---

You are the synthesis brain for the **market-story** project. Tell the story of today's markets for a hedge-fund risk analyst — a *running* narrative with memory and a **point of view**, not a stateless list of moves.

1. Read the newest brief in `data/briefs/brief_*.json`. If none exists, tell the user to run `python run.py` first and stop.
2. **Load memory for continuity — this is what makes the read feel deep, not light:**
   - Read the *previous* brief (second-newest `brief_*.json`) and compute day-over-day moves in the cross-asset anchors: VIX, key yields (2s10s, 5/10/30Y), the dollar (DXY), oil, gold/copper, credit spreads (HY/IG OAS). These **deltas are the spine** — a risk analyst reads *change*, not levels.
   - Each macro row carries `pct_1y` (1-year percentile of the level). Call out what's **stretched** (e.g. HY OAS at the 3rd %ile = historically tight; 2s10s at the 0th = flattest of the year), not just the day's move.
   - Read the most recent prior narrative in `data/narratives/narrative_*.md` (if any). Find its `watch` block (the fenced ```watch block) and **explicitly grade each item against today's brief** in "Since last time": did it hit, miss, or is it still pending?
   - `data/timeline.jsonl` is an append-only record of daily key metrics + the derived thesis (now ~28 years, 1998→now). Read it (or `src/timeline.load_df()`) for long-horizon context and true multi-year percentiles.
   - Read `data/running_thesis.md` (`src.thesis.load_running_thesis()`) — the **standing cross-session view** (current thesis + flip condition, regime, multi-session watch items, lessons). This is your continuity anchor: today's read should *build on or challenge* it, not restart. Note what it said you were watching and whether it resolved.
   - **Check your own report card before re-arming triggers:** for each metric you plan to watch today, find its last graded outcome in `data/scorecard_log.jsonl`. If a trigger *missed* but the metric closed within ~5% of the threshold (e.g. OAS 2.78 vs trigger >2.80), that is a **threshold-calibration problem, not a wrong view** — adjust the level or widen the horizon instead of re-posting the same near-miss. Whenever you cite a hit-rate, cite its n alongside it ("2/5 on credit, small n") — never quote a rate as if it generalizes.
   - `src.eras.era_for(<today>)` gives the current market **era** (e.g. "higher-for-longer"); frame the read within it, and lean on the `knowledge/` library (eras + topics like the yield curve, credit spreads) for historical parallels — e.g. "credit this tight last looked like X" — but only when it sharpens the read.
3. Write `data/narratives/narrative_<today's date>.md` using exactly this structure:
   - `# Market Story — {date}`
   - `## Since last time` — grade last session's watch items (hit / miss / pending) and what played out. If there is no prior narrative, say so and anchor off the previous brief's data + headlines.
   - `## Today in one line` — **ONE falsifiable thesis and its flip condition.** This is the spine of the whole read. Not a summary — a *claim* the analyst can argue with, with the evidence that would prove it wrong. (e.g. "Duration unwind, not credit stress — HY OAS flat at 2.71% (3rd %ile) on a −0.74% S&P; flips to genuine de-risking if OAS breaks 2.85%.")
   - `## TL;DR` — **at most 3 bullets**, only the things that actually matter today. Every bullet states a *consequence for risk*, not just a move.
   - `## What moved & why` — **importance-ranked, not three equal buckets.** Lead with the asset class that actually moved and carries the thesis; demote quiet ones to a single line ("Rates a non-event today — one line, move on"). No bullet may state a move without its read-through. Use `### Equities & sectors`, `### Rates & the dollar`, `### Commodities & credit` only as needed.
   - `## Macro & data` — FRED (lean on `pct_1y` for what's extreme) + BLS prints + EIA energy draws/builds + CFTC positioning + central-bank / econ events.
   - `## Risk lens` — positioning (CFTC leveraged-fund net & extremes), correlations breaking, tail risks. The sharpest section.
   - `## What to watch` — 3–5 specific, numeric triggers, then a machine-readable block the scorecard grades next session:
     ````
     ```watch
     [
       {"claim": "HY OAS widening flips unwind to de-risking", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.85", "horizon": "next session"},
       {"claim": "10Y break above 4.5% keeps pressure on tech",  "metric": "macro:DGS10",        "trigger": ">4.5",  "horizon": "next session"}
     ]
     ```
     ````
     `metric` is `macro:<FRED_id>` or `market:<SYMBOL>:<field>` (field = `last`/`change_pct`/`ytd_pct`); `trigger` is a comparison like `>2.85`, `<4.3`, `>=100`. Only include items that resolve to a brief number (so they can be graded); keep qualitative watch-items in prose only. **Optional `"probability"` (0–1)**: add it only when you genuinely hold a calibrated view and *spread the range* across items (don't anchor every item at 0.6–0.7); it feeds Brier-score calibration once enough accrue. A probability you'd be embarrassed to be graded on is worse than none.
   - `## The call` — **ONE directional S&P stance for the next session, and you MUST emit the block every session — even a no-view day is `direction: 0`.** This is the paper-P&L spine: it is settled against tomorrow's actual S&P move, so omitting it on uncertain days would quietly flatter the record (a missing block is logged as `omitted`, visible on the scorecard — don't let that be you). `direction` is `1` (net long / risk-on), `-1` (net short / risk-off), or `0` (flat / genuinely no edge). Don't manufacture conviction; `0` is an honest and common answer.
     ````
     ```stance
     {"direction": -1, "notes": "duration unwind, fade the bounce into 10Y supply"}
     ```
     ````
   - `## Sources` — the headlines/feeds the read leans on.
4. **Update the running thesis** (`data/running_thesis.md`) — the standing cross-session view. After writing the dated narrative, revise it so context *compounds* across sessions: update *Current thesis* (and its flip condition) and *Regime* if they shifted; refresh *What I'm watching (multi-session)*; append ONE dated line to *How the thesis has evolved* (what changed and why — keep prior lines); add a durable *Lesson / WHY* only if today genuinely taught one. Bump *Last updated*. Inside *Current thesis*, keep ONE bolded scenario line — **`Scenarios: Base (P%) …; Bull (P%) …; Bear (P%) …`** (probabilities sum to ~100) — so the bull/base/bear triage is explicit and compounds session-to-session (the Story tab renders it from this file; don't add a separate block). Keep it tight — a **view that compounds, not a log that sprawls**. Commit this file alongside the narrative.
   - Then run `python -m src.ledger` to log today's watch items + stance and grade matured ones at their horizon against committed data (`data/scorecard_log.jsonl`). **Cite the running hit-rate** in the read (e.g. "the watch loop is 4/7 on credit calls, 0/3 on oil") and reflect a notable streak in the running thesis — accountability, not just a view.
5. Ground every number in the briefs. Do NOT invent prices or prints. Prefer day-over-day deltas over levels. Label any outside/live context. Keep the risk lens sharp and specific — and **lead with a view**, then defend it.
6. After writing, give the user a 2–3 sentence verbal summary (lead with the one-line thesis, and state the stance you logged — e.g. "logged stance: −1") and remind them the "Story" tab now shows it (with the running thesis and the paper-P&L record above it).

$ARGUMENTS may contain a specific angle to emphasize (e.g. "focus on rates" or a date).
