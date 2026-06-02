---
description: Read today's market brief and write the narrative the dashboard displays
---

You are the synthesis brain for the **market-story** project. Tell the story of today's markets for a hedge-fund risk analyst.

1. Find the newest brief in `data/briefs/brief_*.json` and read it. If none exists, tell the user to run `python run.py` first and stop.
2. Write `data/narratives/narrative_<same-date>.md` using exactly this structure:
   - `# Market Story — {date}`
   - `## TL;DR` — 3–5 punchy bullets, the day at a glance
   - `## What moved & why` with `### Equities & sectors`, `### Rates & the dollar`, `### Commodities & credit`
   - `## Macro & data` — FRED prints, central-bank / econ events in the brief
   - `## Risk lens` — positioning, correlations breaking, tail risks, what to watch next (this is the most important section for this user)
   - `## Sources` — the headlines/feeds the read leans on
3. Ground every number and claim in the brief. Do NOT invent prices or prints. If you add outside/live context, label it. Keep the risk lens sharp and specific.
4. After writing, give the user a 2-sentence verbal summary and remind them the "Today's Story" tab now shows it.

$ARGUMENTS may contain a specific angle to emphasize (e.g. "focus on rates" or a date).
