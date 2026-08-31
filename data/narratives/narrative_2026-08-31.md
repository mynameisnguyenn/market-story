# Market Story — 2026-08-31

> *Brief: `brief_2026-08-28.json` (captured 2026-08-28 21:40 UTC — US close, Friday). Previous brief: `brief_2026-08-27.json`. Prior narrative: `narrative_2026-08-28.md`. FRED vintage: DGS10 4.67% (Aug 27), HY OAS 2.63% (Aug 27 — 0.0th %ile, FOURTH consecutive below gate). CFTC: Aug 25 vintage (first post-NVDA data, key upgrade). Stock-bond corr 0.43 (from 0.24). Warsh JH speech captured.*

---

## Since last time

Grading `narrative_2026-08-28.md` watch items against `brief_2026-08-28.json`:

| # | Claim | Trigger | Result |
|---|---|---|---|
| 1 | Warsh dovish: 10Y breaks below 4.55% during/after JH speech | `market:^TNX:last <4.55`, horizon 2026-08-28 | **MISS** — 10Y rose to 4.720% (+4.8bps from 4.672%). Warsh was explicitly hawkish: "still has work to do on inflation." The bond market took him at his word (MarketWatch). P=0.25 was correctly skeptical. |
| 2 | HY OAS fourth consecutive ≤2.69% — private credit lag window closing | `macro:BAMLH0A0HYM2 <=2.69`, horizon 2026-08-29 | **HIT** — HY OAS 2.63% (Aug 27 FRED vintage, −4bps). Fourth consecutive below gate. Now at **0.0th %ile — lowest print of the year**. TGA arrest is confirmed durable through a hawkish Warsh. P=0.55. |
| 3 | HY OAS widens ≥2.73% — lag propagating through TGA suppression | `macro:BAMLH0A0HYM2 >=2.73`, horizon 2026-08-29 | **MISS** — Opposite: compressed further to 2.63%. TGA suppression remains structural. |
| 4 | VIX spikes above 18 on hawkish Warsh — complacency unwind begins | `market:^VIX:last >18.0`, horizon 2026-08-28 | **MISS** — VIX 14.43 (−0.08 on the day). Warsh was hawkish; VIX did not care. Critically, CFTC Aug 25 vintage shows VIX shorts INCREASED from −19,093 to −30,143 in the week before the speech — maximum complacency was being actively added, not reduced. VIX timing recalibration: trigger now ≥20. Running: 0/8. |
| 5 | Gold through $4,750 — fiscal dominance bid accelerates post-Warsh | `market:GC=F:last >4750.0`, horizon 2026-09-04 | **CONFIRMED MISS** — Gold plunged to $4,504.10 (−$151, −3.2%). Warsh's real-rate shock overwhelmed the fiscal-debasement bid. The gold thesis (5/9 directional) absorbs its clearest fundamental miss. |

**Warsh confirmed the hawkish scenario exactly as the flip condition required; only VIX failed to respond. Running hit-rate: ~75/186 (40.3%). Credit: 7/13 (TGA thesis 4 for 4 most recent). Gold directional: 5/9. VIX timing: 0/8.**

---

## Today in one line

**Warsh at Jackson Hole delivered the hawkish verdict the prior narrative identified as the bear case — "still has work to do on inflation," September rate hike now a coin flip (CNBC) — 10Y rose to 4.72% (98.4th %ile), gold plunged $151, yet the VIX barely moved at 14.43 (2.8th %ile) because speculators were actively ADDING VIX shorts into the speech; the market is simultaneously pricing maximum complacency and a coin-flip rate hike, which is exactly the setup where a September hike would be maximally destructive.**

*Flip to 0 (neutral):* August NFP (Sep 4) prints +50–100k with neutral revisions, September FOMC language softens from "work to do" → hike probability falls below 40%, duration rally partially reverses Warsh selldown.  
*Flip to +1 (bull re-entry):* August NFP < 0k AND HY OAS holds ≤2.65% through Sep 4 → both rate hike and credit lag risks simultaneously closed; S&P 7,900 target.

---

## TL;DR

- **Warsh hawkish as the prior scenario named: "inflation concerning," September rate hike is a coin flip** (CNBC: "odds rose after Jackson Hole"). 10Y at 4.720% (+4.8bps on the session), 5Y +8.5bps to 4.481% — the 5Y is the epicenter of rate hike repricing (bear-flattening). 2s10s compressed 8bps to 0.39% (10.3th %ile, near flattest of the year). The bond market gave Warsh credibility that Yellen-era hawks rarely received.

- **Gold −3.2% to $4,504, Silver −3.4% to $67.09 — real rate shock overwhelms fiscal debasement bid.** BEI fell 2bps to 2.31% while nominal yields rose: real rates spiked, and gold got hit. The gold-as-fiscal-dominance trade was wrong on the day; the gold-as-real-rate-sensitive trade was right. $4,504 is still 61.5th %ile but the $4,750 target is off the table while hike probability is 50/50.

- **HY OAS 2.63% — FOURTH consecutive below gate, 0.0th %ile (lowest of the year).** The TGA suppression is structural through a hawkish JH. Private credit lag clock: Day 14–15 of the 20–40-day window. The next FRED vintage (Sep 1–2) is the critical test of whether TGA arrest closes the window clean.

- **CFTC Aug 25 vintage confirms the squeeze AND the complacency trap: Nasdaq covered 20,539 contracts (−61,771 → −41,232, NVDA squeeze printed); VIX shorts ADDED −11,050 (→ −30,143); Ultra T-Bond shorts barely moved at −848,988.** Three positions simultaneously wrong-sided for a September rate hike: long complacency (VIX short), short duration (T-Bond short that needs the hike to deepen), and still-short Nasdaq going into AI earnings season.

- **Stock-bond correlation 0.43 (from 0.24) — hedge formally broken.** When stocks and bonds sell together, 60/40 and risk-parity strategies face systematic deleveraging. September FOMC is the event that either restores or deepens the correlation breakdown.

---

## What moved & why

### Equities & sectors

**S&P 500 −0.25% to 7,711.76 | Nasdaq −0.52% | Dow −0.02% | Russell 2000 −1.39%.** The session structure is a textbook Fed-tightening rotation: rate-sensitive sectors sold, financials/cyclicals bid, AI leadership partially reversed.

**Weekly framing (more important than the day):** S&P +0.49% w/w, Nasdaq +0.85% w/w — Thursday's NVDA/CRM earnings sprint (+0.72%) more than offset Friday's Warsh selldown. The weekly win is real but narrow; the composition (5 advancing sectors vs. 6 declining on Friday) is not a bull market structure.

**Sector breakdown (Aug 28 close):**
- XLC Comm Services **+1.42%** — META +1.21%, GOOGL +1.74%; the communications complex held up on the Microsoft AI software narrative continuation (MSFT longest winning streak of the year, MarketWatch)
- XLY Cons Discretionary **+1.15%** — AMZN **+3.97%** is the standout; consumer spending thesis holds despite rate concerns
- XLP Cons Staples **+0.43%** — mild defensive bid
- XLF Financials **+0.38%** — rate hike cycle = bank NIM expansion; financials correctly bid on Warsh hawkish
- XLK Technology **−1.55%** — NVDA **−4.57%** to $217.55 (from $228 Thursday); TSM −2.29%; ASML −2.24%; semiconductor complex gives back Thursday's yield-shock-sensitive gains
- XLI Industrials **−0.93%**; XLU Utilities **−1.04%** (most rate-sensitive, expected sell on +8.5bps 5Y)
- XLV Health Care **−0.24%**; XLRE Real Estate **−0.40%**

**NVDA −4.57% to $217.55:** The earnings-driven squeeze ($228, +8.74% Thursday) partially reverses on yield shock. NVDA is still +1.3% w/w — the earnings catalyst was real. Data center revenue $89bn = 92.5% of total revenue in the July quarter; SpaceX AI chip spend emerging as a future upside driver (MarketWatch). The medium-term bull thesis is intact; the near-term rate environment is the headwind.

**PayPal −13%:** Stripe and Advent abandoned their ~$50B takeover (Nasdaq Markets). PayPal's standalone execution story is now the only thesis — the acqui-premium evaporated in a single session. This is a fintech sector signal: at current rates, mega-cap fintech M&A math doesn't pencil.

**Global indices:** Europe rallied (Euro Stoxx +0.95%, DAX +0.77%, CAC +0.98%, FTSE +0.29%) — carryover from Thursday's tech rally and no immediate ECB rate hike pressure. Asia mixed: Nikkei −0.20%, Hang Seng −0.34%, Shanghai +1.13% (China domestic stimulus narrative separate from Fed dynamics).

### Rates & the dollar

**Cross-asset delta table (Aug 27 brief → Aug 28 brief):**

| Metric | Aug 27 | Aug 28 | Δ | 1Y Pct |
|---|---|---|---|---|
| **FRED DGS10** | 4.66% | **4.67%** | +1bp | 92.5th %ile |
| **FRED DGS2** | 4.19% | **4.20%** | +1bp | 90.5th %ile |
| **2s10s (T10Y2Y)** | 0.47% | **0.39%** | **−8bps** | **10.3th %ile** |
| T10Y3M | 0.83% | **0.83%** | flat | 93.7th %ile |
| **BEI** | 2.33% | **2.31%** | −2bps | 49.6th %ile |
| **HY OAS** | 2.67% | **2.63%** | **−4bps** | **0.0th %ile** |
| IG OAS | 0.80% | **0.79%** | −1bp | 46.0th %ile |
| **Market 10Y** | 4.672% | **4.720%** | **+4.8bps** | **98.4th %ile** |
| **Market 5Y** | 4.396% | **4.481%** | **+8.5bps** | elevated |
| Market 30Y | 5.191% | **5.206%** | +1.5bps | elevated |
| **DXY** | 99.12 | **99.68** | **+0.56%** | 74.2th %ile |
| **Gold** | $4,655 | **$4,504** | **−$151 (−3.2%)** | 61.5th %ile |
| WTI | $83.54 | **$83.44** | −$0.10 | 66.7th %ile |
| Copper | $6.69 | **$6.64** | −$0.05 | 98.0th %ile |

**Three reads from the delta table:**

1. **Bear-flattening: the 5Y absorbed the most pain (+8.5bps) while the 30Y barely moved (+1.5bps).** 2s10s fell from 0.47% to 0.39% (10.3th %ile — near the flattest of the year). This is the market saying: "we price one hike (front-end up), but we also price a slowdown after it (back-end contained)." The 5Y is the epicenter of September FOMC repricing. If the hike materializes and data softens, the 5Y corrects hardest.

2. **BEI fell 2bps to 2.31% while nominal yields rose — real rates spiked.** This is why gold fell. Gold's correlation with real rates is near-instantaneous: higher real yields = lower gold. With BEI at 49.6th %ile and real rates at historic highs, the "gold as fiscal dominance" thesis requires TGA suppression to be persistent enough to offset the real rate headwind. That is a harder case to make at 4.72% nominal with BEI at 2.31%.

3. **Dollar +0.56% to 99.68 (DXY) — the most dollar-positive session in weeks.** EUR/USD −0.58%, GBP/USD −0.44%, USD/JPY +0.49% to 160.04. The rate differential widened: US rates rising (hike probable) while ECB/BOE are not hiking. USD/JPY at 160 is the policy stress level for the BOJ — above 160 and sustained, expect BOJ intervention language to re-emerge.

### Commodities & credit

**Gold −3.2% to $4,504.10 — the largest single-session drop of the cycle.** The fiscal-dominance thesis (Bessent $950bn TGA) is in tension with the real-rate shock. Gold remains +4.1% YTD, but the weekly chart is −2.6%. The thesis' flip condition: if September NFP disappoints and hike probability falls, real rates moderate and gold recovers toward $4,600. If the hike is priced in fully, the next support is ~$4,400 (prior technical range).

**Silver −3.4% to $67.09; Nat Gas −0.89%; WTI −0.11% to $83.44; Brent −1.57% to $88.29.** Metals broadly sold on real rate shock. WTI essentially flat — the geopolitical bid (Iran/TACO pattern, Pentagon-Venezuela talks, Bloomberg) is offsetting the dollar-strengthening headwind.

**Corn and wheat jumped to highest prices in more than three years (CNBC, 20:00 UTC).** This is the most underappreciated risk in the brief: food commodity inflation at 3-year highs adds a new channel to the PCE path. The drivers differ (corn vs. wheat), but the aggregate signal — broad commodity reflation beyond energy — is exactly what Warsh was citing in his "still has work to do" framing. August PCE (reported ~Oct 31) will reflect August energy ($82-84 average) and August food prices. The disinflation-via-commodities channel is closing.

**HYG −0.16%, LQD −0.36%, TLT −0.30%, AGG −0.35%** — credit and duration sold together on Warsh, validating the stock-bond correlation breakdown. FRED HY OAS at 2.63% (0.0th %ile) is structurally suppressed by TGA operations; the market-price HYG is drifting lower regardless.

---

## Macro & data

**FRED (Aug 27–28 vintage — most recent):**
- DGS10: **4.67% (92.5th %ile)** — FRED catching up to the market 4.72%; the gap between FRED vintage and market-implied yield is closing
- DGS2: **4.20% (90.5th %ile)** — front end edging higher on hike repricing; 3.63% EFFR vs. 4.20% DGS2 = 57bps premium = one full hike priced in
- T10Y2Y (2s10s): **0.39% (10.3th %ile)** — dropped 8bps on Warsh day; bear-flattening; near flattest of the year
- T10YIE (BEI): **2.31% (49.6th %ile)** — fell 2bps; real rates spiked; disinflation in breakevens partially despite corn/wheat surge (lag effect)
- **HY OAS: 2.63% (0.0th %ile)** — FOURTH consecutive below gate; record tight for the year; the TGA structural suppression is confirmed through a hawkish JH
- IG OAS: **0.79%** — tighter; investment-grade not showing distress despite rate hike pricing
- NFCI: **−0.566 (1.6th %ile)** — historically loose; structural divergence from rate hike pricing persists
- VIXCLS: **14.51 (3.2nd %ile, Aug 27 vintage)** — the FRED data lags one day; market VIX at 14.43 on Aug 28

**BLS:**
- July vintage unchanged: NFP −23k, Unemployment 4.1%, AHE +3.15% YoY, CPI-U YoY 3.36%, Core CPI 2.48%
- **Annual benchmark revision (Aug 28):** BLS confirmed fewer jobs than initially reported in 2025–26 — downward adjustment of 0.1% of total workforce (NYT). Within normal bands; not a labor crisis signal. But the directional signal (softer) gives Warsh slightly less justification for aggressive tightening if combined with a soft August NFP.
- **Initial claims (Aug 22 vintage, from prior brief): 203k (7.5th %ile, −4k)** — claims at their tightest in over a year; labor market not signaling distress despite NFP turning negative.

**Warsh JH speech (Aug 28) — the macro event:**
- FT: "Hawkish Warsh hints Fed will raise rates if inflation does not fall soon" — "Wall Street cranks up bets on September increase"
- CNBC: "September Fed decision is now a coin flip as rate hike odds increase post Warsh"  
- CNBC: Warsh "advocates for 'quieter' central bank" — fewer speeches; September FOMC is the next communication point
- BBC: "Fed has 'work to do' if price rises don't ease for Americans"
- MarketWatch: "Kevin Warsh gets what every Fed chair hopes for: a bond market that trusts his word"
- FT: "Warsh settles some nerves at Jackson Hole" — "leaves open questions over Fed 'reaction function'" (the nuanced read: hawkish framing, but the trigger for a hike is not yet publicly calibrated)
- MarketWatch: "Fed chief Kevin Warsh said something Friday that won't sit well with Trump" — the Trump-Fed dynamic re-enters

**JPMorgan private bank:** "Bond market may be pricing AI productivity gains as yields rise." This is the optimistic counter-read: 4.72% 10Y reflects higher long-run growth expectations (AI productivity), not inflation fear. If this interpretation is correct, real yields can be higher and equities can still clear — the bull case for stocks at all-time territory.

**EIA (Aug 21 vintage):** Crude ex-SPR +95 MBBL (tiny build — flat); Gasoline −2,536 MBBL; Distillate −2,228 MBBL; SPR −3,700 MBBL (Bessent's release channel active). The product drawdowns are demand-constructive for WTI; SPR releases are the government's cap on any price spike.

**Canada:** GDP Q2 3.30% annualized — beat despite trade war. Canadian stocks −0.76% on trade war tension (Nasdaq). Pentagon in talks for Venezuelan oil fields (Bloomberg) — a new geopolitical channel for energy supply that could reduce OPEC leverage over time.

---

## Risk lens

**The positioning setup entering September is the most dangerous combination of the cycle:**

**1. VIX shorts at −30,143 (CFTC Aug 25) entering a coin-flip rate hike.** The prior narrative had VIX shorts at −19,093 (Aug 18 vintage) and warned of asymmetric vol risk. Speculators did not unwind — they ADDED −11,050 more VIX shorts in the week before Warsh. VIX at 14.43 (2.8th %ile) entering a 50% probability of the first rate hike under Warsh is historically anomalous. The last time VIX was at the ~3rd %ile entering a contested Fed decision was November 2021 — the unwind from that positioning error took VIX from 15 to 38 over three months. The mechanism: a September hike announcement fires the VIX shorts immediately; the covering amplifies the underlying move.

**2. Ultra T-Bond shorts at −848,988 — essentially unchanged, stuck.** Duration bears entered a hawkish Warsh with a near-maximum short and barely moved (covered only 12,369 contracts). This is a trapped position: the shorts need higher yields to profit, but at 10Y 4.72% (98.4th %ile) and 5Y 4.48%, the rates are already near the top of the 1-year range. A soft August NFP print on Sep 4 or a softer September FOMC would be a catastrophic covering squeeze for this position.

**3. Stock-bond correlation 0.43 (from 0.24) — the hedge is formally broken.** When stocks and bonds both fall (positive correlation), risk-parity strategies and 60/40 allocations face simultaneous drawdowns. Systematic deleveraging (vol-targeting, risk-parity) sells both legs to maintain portfolio vol targets. This becomes self-reinforcing: selling pushes correlation higher, which forces more selling. The correlation is now at a level that would trigger marginal deleveraging for strategies running below their vol budgets.

**4. HY OAS at 0.0th %ile while September rate hike is a coin flip — the most extreme contradiction in the brief.** Credit is at the tightest level of the year (2.63%) on the same day the Fed chair hints at a rate hike. One of these is wrong. The resolution: either Bessent's TGA operations continue to suppress the credit floor regardless of rate moves (and the coin-flip probability overstates actual hike likelihood), OR the hike materializes and eventually breaks the TGA suppression (the credit floor cracks with a lag). Private credit lag clock: **Day 14–15 of the 20–40-day window.** The remaining days (15–25 more) are the higher-risk half.

**5. Food commodity reflation is the least-discussed August risk.** Corn and wheat at 3-year highs (CNBC) were not in any prior watch list. Combined with WTI $83 average for August, the August PCE path (~Oct 31 report) is pointing toward 3.4%–3.5% — which would REVERSE the three-month deceleration trend (3.6% → 3.4% → 3.3%). If the August PCE reverses the trend, Warsh's "coin flip" becomes near-certain, and the December FOMC is also in play. This is the macro tail risk the market is not pricing.

**What to watch next (3–5 numeric triggers):**

1. **August Nonfarm Payrolls (Sep 4 — the most important near-term data point):** After July NFP −23k, another negative print would significantly soften September hike probability — Warsh needs positive job growth to justify the "inflation still high, economy still resilient" framing. A print below 0 → hike probability falls to ~25%, VIX covers, gold recovers $4,600. A print above +100k → hike probability rises to ~65%, 10Y through 4.75%, S&P 7,400 retest.

2. **HY OAS fifth consecutive print (next FRED vintage, Sep 1–2):** At 0.0th %ile (2.63%), the only direction that confirms the private credit lag window is closed is another print ≤2.63%. A widening to ≥2.75% after four consecutive below-gate prints would be the most significant single credit data point of the cycle — it would mean TGA suppression is losing to lag propagation.

3. **VIX close above 17 (next structural level):** VIX at 14.43 (2.8th %ile) entering September FOMC. A close above 17 begins the unwind from maximum complacency; above 20 triggers systematic deleveraging. The trigger is not a market event but a data event (September NFP or September FOMC itself, Sep 16–17). The VIX shorts at −30,143 are the accelerant.

4. **Gold $4,400 support or $4,600 recovery:** Post-Warsh gold at $4,504 is 61.5th %ile. If hike probability firms: $4,400 is the next technical support (prior June consolidation range). If August NFP disappoints and hike probability falls: recovery toward $4,600 and the fiscal-dominance thesis reengages. Gold remains the most reliable single-asset signal in this cycle (5/9 directional calls correct).

5. **2s10s (10Y–2Y) through 0.30% or steepening to 0.50%+:** Curve at 0.39% (10.3th %ile). If bear-flattening continues (hike confirmed), the curve compresses to inverted territory — 2s10s below 0.30% signals the market prices a policy error (hike into slowdown). If data softens and hike is priced out, 2s10s steepens toward 0.50%: the bull bull steepener begins, duration rally.

```watch
[
  {"claim": "HY OAS fifth consecutive below gate (≤2.63%) — private credit lag window closing clean", "metric": "macro:BAMLH0A0HYM2", "trigger": "<=2.63", "horizon": "2026-09-04", "probability": 0.60},
  {"claim": "HY OAS widens above 2.75% — TGA suppression breaks, lag propagating through", "metric": "macro:BAMLH0A0HYM2", "trigger": ">=2.75", "horizon": "2026-09-04", "probability": 0.10},
  {"claim": "August NFP above +100k — September hike now 65%+, S&P retest 7,400", "metric": "macro:PAYEMS:monthly_change", "trigger": ">100", "horizon": "2026-09-04", "probability": 0.38},
  {"claim": "VIX closes above 17 — complacency unwind begins, −30k VIX shorts covering", "metric": "market:^VIX:last", "trigger": ">17.0", "horizon": "2026-09-07", "probability": 0.28},
  {"claim": "Gold falls below $4,400 — real rate shock extends, hike probability firms", "metric": "market:GC=F:last", "trigger": "<4400.0", "horizon": "2026-09-07", "probability": 0.32}
]
```

---

## The call

**Direction: −1 (defensive/cautiously short)**

Warsh spoke. He said "work to do." The bond market believed him. September rate hike is a coin flip. The setup: 10Y at 4.72% (98.4th %ile), VIX at 14.43 (2.8th %ile), VIX shorts at −30,143 (increasing), stock-bond correlation 0.43 (hedge broken), corn/wheat at 3-year highs seeding the next PCE print, and gold's fiscal debasement thesis taking its first clean hit. The bear case that the prior narrative marked as "NOT priced" is now partially priced in rates (10Y up 4.8bps) but NOT priced in vol (VIX flat).

The asymmetry entering the week: the bull requires both August NFP to disappoint AND Warsh to soften (dual condition). The bear requires only one of: NFP upside, or corn/wheat PCE translation, or any September FOMC language that confirms "coin flip" is conservative. The probability weight favors staying defensive until September 4.

The prior flat (direction: 0) was correct to wait for Warsh. Warsh has resolved. Entering −1 at S&P 7,712 with the understanding that the flip conditions are specific and actionable.

Flip to 0: August NFP in +50–100k range (ambiguous for hike) AND September FOMC preview language softens from "work to do."  
Flip to +1: August NFP <0 AND HY OAS holds ≤2.65% through Sep 4 → dual-gate closure on rate hike and credit lag simultaneously.

Running hit-rate: **~75/186 (40.3%)**. Credit calls: 7/13 (TGA thesis: 4 consecutive hits). Gold directional: 5/9 (first clean thesis miss on Warsh day). VIX timing: 0/8 (recalibrating trigger to ≥20). Oil direction: retired (TACO pattern is structural noise, not a tradeable signal).

```stance
{"direction": -1, "notes": "Defensive. Warsh confirmed hawkish at JH Aug 28: 'still has work to do on inflation,' September hike coin flip (CNBC). 10Y 4.720% (98.4th %ile, +4.8bps). 5Y +8.5bps to 4.481% (bear-flattener). Gold −$151 to $4,504 = real rate shock confirmed. VIX 14.43 (2.8th %ile) = maximum complacency + −30,143 VIX shorts. Stock-bond corr 0.43 (hedge broken). CFTC Aug 25: Nasdaq covered 20k (squeeze printed) but VIX shorts added −11k (bad). S&P 7,712. HY OAS 2.63% (0.0th %ile, 4th consecutive). Private credit lag Day 14-15 of 20-40. Corn/wheat 3Y highs = August PCE risk. Flip to 0: NFP +50-100k + soft September FOMC. Flip to +1: NFP <0 AND HY OAS ≤2.65% Sep 4. Running: 75/186 (40.3%)."}
```

---

## Sources

- *Hawkish Warsh hints Fed will raise rates if inflation does not fall soon* (FT International, 2026-08-28T16:50:09 UTC) — "Wall Street cranks up bets on September increase in borrowing costs"
- *September Fed decision is now a coin flip as rate hike odds increase post Warsh* (CNBC Finance, 2026-08-28T15:22:10 UTC)
- *Fed Chairman Warsh expresses concern about inflation, advocates for 'quieter' central bank* (CNBC Economy, 2026-08-28T16:11:51 UTC)
- *Kevin Warsh gets what every Fed chair hopes for: a bond market that trusts his word* (MarketWatch Top Stories, 2026-08-28T20:10:00 UTC)
- *Warsh settles some nerves at Jackson Hole* (FT International, 2026-08-28T16:38:14 UTC)
- *Fed has 'work to do' if price rises don't ease for Americans, Warsh says* (BBC Business, 2026-08-28T15:15:26 UTC)
- *Fed chief Kevin Warsh said something Friday that won't sit well with Trump* (MarketWatch Bulletins, 2026-08-28T17:08:50 UTC)
- *Stocks end lower, seal weekly gains as Fed's Warsh fuels rate-hike expectations* (MarketWatch Bulletins, 2026-08-28T20:13:47 UTC)
- *Wall Street ends lower on hawkish Warsh at Jackson Hole, but rises for the week* (Investing.com Markets, 2026-08-28T20:15:23 UTC)
- *Gold plunges as Warsh's Jackson Hole inflation concerns spark rate hike bets* (Seeking Alpha, 2026-08-28T21:15:46 UTC)
- *Microsoft's stock seals its longest winning streak of the year as AI software fears fade* (MarketWatch Top Stories, 2026-08-28T21:34:00 UTC)
- *Nvidia's revenue forecast is so huge that Wall Street wonders if SpaceX is the reason* (MarketWatch Top Stories, 2026-08-28T20:58:00 UTC) — data center revenue $89bn = 92.5% of total Q revenue
- *Stock Market Today, Aug. 28: PayPal Falls 13% After Stripe and Advent Abandon $50B Takeover* (Nasdaq Markets, 2026-08-28T21:00:44 UTC)
- *Corn and wheat prices jump to highest prices in more than three years* (CNBC Finance, 2026-08-28T20:00:56 UTC)
- *Bond market may be pricing AI productivity gains as yields rise: JPMorgan Private Bank* (Investing.com Markets, 2026-08-28T20:12:29 UTC)
- *Smaller Revision Points to More Accurate Jobs Numbers* (NYT Economy, 2026-08-28T16:21:55 UTC) — 0.1% downward BLS revision
- *Fewer U.S. jobs were created in 2025–26 than previously reported* (MarketWatch Bulletins, 2026-08-28T15:33:50 UTC)
- *A stock-market reality check is coming this autumn, predicts Bank of America* (MarketWatch Bulletins, 2026-08-28T14:44:57 UTC)
- *US manufacturing is booming — but it's no thanks to Trump's tariffs* (FT International, 2026-08-28T17:00:04 UTC)
- *Canadian Stocks Slide Amid Persisting Trade War Concerns, GDP Data Release* (Nasdaq Markets, 2026-08-28T20:32:28 UTC) — Canada GDP 3.30% annualized Q2
- *Pentagon in talks for Venezuelan oil fields deal through middleman* (Investing.com/Bloomberg, 2026-08-28T20:37:48 UTC)
- *U.S. appeals court rules against prediction markets, sets up likely fight at Supreme Court* (CNBC Finance, 2026-08-28T21:34:33 UTC)
- Analytics: `brief_2026-08-28.json` (21:40 UTC close data — S&P 7,711.76 (−0.25%), Nasdaq 26,402 (−0.52%), VIX 14.43, XLK −1.55%, XLC +1.42%, XLY +1.15%, NVDA −4.57% to $217.55, AMZN +3.97%; FRED Aug 27: **DGS10 4.67% (92.5th %ile)**, DGS2 4.20%, **T10Y2Y 0.39% (10.3th %ile, −8bps)**, **HY OAS 2.63% (0.0th %ile — FOURTH consecutive)**, BEI 2.31% (49.6th %ile, −2bps); Market: 10Y 4.720% (98.4th %ile), 5Y 4.481% (+8.5bps), 30Y 5.206%; DXY 99.68 (+0.56%); Gold $4,504 (−$151, −3.2%); WTI $83.44; Brent $88.29; CFTC Aug 25: S&P −315,204 (−33,802), Nasdaq −41,232 (+20,539 covered), VIX −30,143 (−11,050 added), Ultra T-Bond −848,988 (+12,369 covered); stock-bond corr 0.43 (from 0.24, "hedge broken"); VIX vol premium 4.1 (VIX 14.4 vs. 20d realized 10.3%). Corn/wheat 3-year highs (CNBC). PayPal −13% on deal collapse.
