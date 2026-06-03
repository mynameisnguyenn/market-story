---
description: Read today's market brief and write the narrative the dashboard displays
---

You are the synthesis brain for the **market-story** project. Tell the story of today's markets for a hedge-fund risk analyst — a *running* narrative with memory and a **point of view**, not a stateless list of moves.

1. Read the newest brief in `data/briefs/brief_*.json`. If none exists, tell the user to run `python run.py` first and stop.
2. **Load memory for continuity — this is what makes the read feel deep, not light:**
   - Read the *previous* brief (second-newest `brief_*.json`) and compute day-over-day moves in the cross-asset anchors: VIX, key yields (2s10s, 5/10/30Y), the dollar (DXY), oil, gold/copper, credit spreads (HY/IG OAS). These **deltas are the spine** — a risk analyst reads *change*, not levels.
   - Each macro row carries `pct_1y` (1-year percentile of the level). Call out what's **stretched** (e.g. HY OAS at the 3rd %ile = historically tight; 2s10s at the 0th = flattest of the year), not just the day's move.
   - Read the most recent prior narrative in `data/narratives/narrative_*.md` (if any). Find its `watch` block (the fenced ```watch block) and **explicitly grade each item against today's brief** in "Since last time": did it hit, miss, or is it still pending?
   - `data/timeline.jsonl` is an append-only record of daily key metrics + the derived thesis. Once it has a few weeks of history, read it (or `src/timeline.lookback(weeks)`) for "where were we N weeks ago" context — a longer lookback than the day-over-day delta.
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
     `metric` is `macro:<FRED_id>` or `market:<SYMBOL>:<field>` (field = `last`/`change_pct`/`ytd_pct`); `trigger` is a comparison like `>2.85`, `<4.3`, `>=100`. Only include items that resolve to a brief number (so they can be graded); keep qualitative watch-items in prose only.
   - `## Sources` — the headlines/feeds the read leans on.
4. Ground every number in the briefs. Do NOT invent prices or prints. Prefer day-over-day deltas over levels. Label any outside/live context. Keep the risk lens sharp and specific — and **lead with a view**, then defend it.
5. After writing, give the user a 2–3 sentence verbal summary (lead with the one-line thesis) and remind them the "Story" tab now shows it.

$ARGUMENTS may contain a specific angle to emphasize (e.g. "focus on rates" or a date).
