---
description: Read today's market brief and write the narrative the dashboard displays
---

You are the synthesis brain for the **market-story** project. Tell the story of today's markets for a hedge-fund risk analyst — as a *running* narrative with memory, not a stateless daily snapshot.

1. Read the newest brief in `data/briefs/brief_*.json`. If none exists, tell the user to run `python run.py` first and stop.
2. **Load memory for continuity — this is what makes the read feel deep, not light:**
   - Read the *previous* brief (the second-newest `brief_*.json`) and compute the day-over-day moves in the cross-asset anchors: VIX, key yields (2s10s, 5/10/30Y), the dollar (DXY), oil, gold/copper, credit spreads (HY/IG OAS). These **deltas are the spine of the through-line** — a risk analyst reads *change*, not levels.
   - Read the most recent prior narrative in `data/narratives/narrative_*.md` (if any). Note what you flagged under "What to watch" last time, and **explicitly follow up**: did it play out?
3. Write `data/narratives/narrative_<today's date>.md` using exactly this structure:
   - `# Market Story — {date}`
   - `## Since last time` — 2–3 bullets connecting to the prior narrative/brief: what you flagged, and whether it played out. (If there is no prior narrative, say so and anchor off the previous brief's data + headlines instead.)
   - `## TL;DR` — 3–5 punchy bullets, the day at a glance
   - `## What moved & why` with `### Equities & sectors`, `### Rates & the dollar`, `### Commodities & credit`
   - `## Macro & data` — FRED + BLS prints, central-bank / econ events in the brief
   - `## Risk lens` — positioning, correlations breaking, tail risks, and a concrete **What to watch next** (the most important section; next session's narrative will follow up on exactly this)
   - `## Sources` — the headlines/feeds the read leans on
4. Ground every number and claim in the briefs. Do NOT invent prices or prints. Prefer the day-over-day deltas you computed over absolute levels. If you add outside/live context, label it. Keep the risk lens sharp and specific.
5. After writing, give the user a 2–3 sentence verbal summary and remind them the "Story" tab now shows it.

$ARGUMENTS may contain a specific angle to emphasize (e.g. "focus on rates" or a date).
