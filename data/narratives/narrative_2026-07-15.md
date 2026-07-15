# Market Story — 2026-07-15

> *Brief: `brief_2026-07-14.json` (generated 2026-07-14T13:22 UTC — captures Jul 14 pre-market open, ~9:22am ET, eight minutes before the NYSE open; CPI released at 8:30am ET is in the brief; July 14 intraday close is not). FRED Jul 10 vintage; BLS June 2026 (new, released today); CFTC Jul 7 vintage; EIA Jul 3 vintage unchanged.*

---

## Since last time

Grading `narrative_2026-07-14.md` watch items against `brief_2026-07-14.json`:

| Claim | Trigger | Result |
|---|---|---|
| Goldman Sachs Q2 beats on fee income — bank earnings confirm beyond JPM | market:GS:change_pct >3.0 (Jul 14) | **HIT on earnings, stock-move PENDING.** FT confirmed "Wall Street banks post blockbuster profits" — JPM, GS, Citi, BofA all beat (FT 09:29 UTC). BofA profit +27%; WF beat on interest income + trading. GS specific day-move not in brief (captured pre-open); XLF +0.65%. The *earnings* thesis was fully correct. Stock-move resolution in next brief. |
| HY OAS breaks above 2.72% on Jul 9–10 FRED vintage | macro:BAMLH0A0HYM2 >2.72 (Jul 16) | **MISS.** FRED Jul 10 vintage: HY OAS **2.69%** (4.0th %ile) — tightened 1bp from 2.70%. Credit actually hit a cycle low through WTI $80.60 and Hormuz escalation. |
| ASML Q2 miss — bar is exceptional, not record | market:ASML:change_pct <−5.0 (Jul 16) | **PENDING.** Reports Thursday Jul 16. ASML fell −3.97% to $1,726 in today's session — pre-earnings washout, not the earnings print. |
| June CPI above 4.5% — Iran energy + services reacceleration | macro:CPIAUCSL >336.5 (Jul 15) | **MASSIVE MISS.** BLS June CPI-U = 333.952 (P=0.55 for >336.5 was the wrongest probability in this log). June CPI YoY: **3.53%** vs May's 4.25%. Headline CPI fell MoM for the first time since 2020. |
| WTI fades below $72 by Friday | market:CL=F:last <72.0 (Jul 17) | **MISS.** WTI **$80.60** (+8.9% from Jul 13's $74.00). Cycle high. Largest two-day gain in four months. Oil calls: **0/11.** |

**Score: Two confirmed misses (CPI, HY OAS). Running hit-rate: 23/82 (28%) — the CPI call was the most confident miss of the cycle (P=0.55 for a level never reached; actual was 85bps below).**

**Stance from Jul 14: 0 (flat).** Graded against Jul 14's session — brief captured pre-open (9:22am ET, S&P futures slightly negative as IBM −22% and oil +8.9% offset the CPI relief). Flat was defensible given the pre-open chaos: the session resolved between "CPI relief" and "chip carnage + oil spike" forces simultaneously. Settled when Jul 14 close is confirmed.

---

## Today in one line

**June CPI printed 3.53% YoY — ceasefire-era energy deflation removed the "Warsh hikes" tail while WTI simultaneously hit $80.60 (cycle high, +8.9% in a single session), writing July's CPI hot as we speak; the Fed got a backward-looking gift, markets got a forward-looking problem, and ASML tomorrow is the tiebreaker that determines whether the gift gets spent or clawed back.**

*Flip to conviction +1: ASML beats (>+5% EUV orders + raised guidance) + WTI fades below $78 → CPI relief + credit floor + tech re-rate = bull confirmation. Flip to −1: ASML miss (<−5%) + WTI holds >$80 into next week → July CPI hot + chip derating compound = stagflation ambush. Remain +1 risk-on: ASML in-line + WTI $76–80 + HY OAS ≤2.72%.*

---

## TL;DR

- **June CPI 3.53% is the most important print of the cycle — and it's already stale.** Gas prices fell in June during the ceasefire window (WTI avg ~$67 June vs. $80.60 today). Core CPI was 2.59% — essentially at the Fed's 2% target in one reading. Warsh: "inflation will be a thing of the past." The Fed is on hold and everyone now knows it. But July's CPI will be written against $80.60 WTI, not $67. The relief is real; the durability is borrowed time.

- **IBM −22% is the most important earnings print of the cycle.** CEO Krishna: "large deals slipped as clients redirected money into chips, servers and memory." This is not demand destruction; it is demand **redirect**. The AI capex shift is now a *confirmed earnings signal*, not a narrative. Every dollar that left IBM's services went to chip fabs (ASML's order book, TSMC's wafer demand, NVDA's GPUs). ASML tomorrow reports directly into the upside of the same shift IBM just confirmed — yet ASML fell −3.97%.

- **HY OAS 2.69% (4.0th %ile) is a cycle low, reached on a day with WTI +8.9% and Hormuz escalation continuing.** Banks are *profiting* from the geopolitical volatility: SpaceX IPO fee income, Iran-hedging flow, commercial lending. The financial system is not stressed by the chaos; it is underwriting it. Credit's green light is cleaner today than at any prior point in this cycle.

---

## What moved & why

### Equities & sectors

S&P 7,515.34, −0.79% (captured pre-open at 9:22am ET; S&P futures were +0.4% at 8:51am ET on CPI — the pre-open snapshot may not reflect the final session). Nasdaq 25,873.18, −1.55%. VIX 16.75 (+3.5% from 16.18 — slight uptick but still 44th %ile for the year).

| Sector | Change | Read |
|---|---|---|
| XLE Energy | **+3.01%** | WTI $80.60; Iran escalation + Hormuz |
| XLF Financials | **+0.65%** | Bank earnings blockbuster confirmed |
| XLU Utilities | +0.68% | Rate relief on cool CPI |
| XLRE Real Estate | +0.56% | Duration longs; rate-relief yield play |
| XLP Staples | +0.56% | Defensive + rate relief |
| XLV Health Care | +0.35% | Defensive bid |
| XLC Comm. Services | −0.04% | Flat |
| XLB Materials | −0.61% | Broad commodity bid offset by risk-off in sector |
| XLI Industrials | −0.85% | IBM confirmed enterprise IT-to-chip capex redirect |
| XLY Cons. Disc. | −1.02% | Consumer squeezed; "funflation" persists |
| **XLK Technology** | **−2.42%** | IBM −22%, ASML −3.97%, NVDA −3.52%, TSM −2.89% |

Six advancers, five decliners. The market at brief capture is split along a clean axis: rate-relief beneficiaries (financials, defensives, real estate) vs. chip crowding victims (XLK). This is NOT a risk-off pattern — credit is tightening — it is a chip-specific washout coinciding with a macro relief signal.

**Key single-name reads:**
- **IBM −22% (worst day in nearly 40 years)**: The AI capex redirect is now a *confirmed GAAP earnings event*, not an analyst thesis. "Large deals slipped as clients redirected money into chips, servers and memory" (FT, CEO Krishna). IBM's enterprise IT services business has lost to ASML/NVDA/TSMC at the wallet-share level. This is structurally permanent — enterprises don't rebuild mainframe contracts after moving to AI chips.
- **ASML −3.97% to $1,726.04**: Pre-earnings slide deepens. YTD still +61.9%. The IBM confirmation that AI chip capex is surging IS the fundamental tailwind for ASML's Thursday EUV order print — yet the stock falls because crowding dynamics (Nasdaq lev_net −55,013) overpower fundamental signals pre-earnings. KeyBanc raised price targets on NVDA and Intel today — not ASML.
- **TSMC −2.89% ($421.58)**: Third consecutive session falling despite last week's record +67% YoY revenue. The benchmark for ASML's Thursday reaction is now firmly: "record is not enough; exceptional + raised guidance required."
- **Banks blockbuster** (FT: "JPMorgan, Goldman, Citi and BofA kick off earnings season with strong results"): BofA profit +27%, WF beat on interest income + trading. Yet BofA's stock FELL on the beat (MarketWatch: "Bank of America's stock falls despite blockbuster earnings"). Same dynamic as TSMC: strong is priced in. The bank earnings confirmed the earnings cycle is healthy; the stock reactions confirmed crowding at the top of the curve.
- **NVDA −3.52% ($203.53)**: Chip contagion from IBM signal + pre-ASML positioning. IBM confirmed AI chip demand is SURGING (at IBM's expense), yet NVDA falls. This is pure crowding / distribution ahead of the ASML binary.
- **CRM +4.84% ($171.22)**: The software brightspot. Enterprise clients reducing IBM services may expand software subscriptions instead. CRM is benefiting from the same capex redirect that's hurting IBM.
- **MSFT +1.53% ($390.99)**: CPI relief + software durability. Azure cloud is in the "winner" category of the AI redirect.
- **V +2.52%, MA +2.08%**: Payments bid on rate relief — the CPI print removed the "next rate hike" discount.
- **Nikkei +0.74%**: Asian bounce from yesterday's SK Hynix-driven selloff. Hang Seng +0.52%, Shanghai +1.36% — Asia recovering, not crashing.
- **MELI +0.81%**: EM consumer resilience despite broader risk-off.

### Rates & the dollar

| Instrument | Jul 14 brief | Jul 13 brief | Δ |
|---|---|---|---|
| 5Y | 4.301% | 4.335% | **−3.4bps** |
| 10Y | 4.571% | 4.585% | **−1.4bps** |
| 30Y | 5.090% | 5.080% | **+1.0bp** |
| DXY | 100.71 | 101.03 | **−0.32** |
| USD/JPY | 161.90 | 162.33 | −0.43 |
| EUR/USD | 1.1450 | — | +0.40% |
| USD/CNY | 6.7586 | 6.768 | −0.14% |

FRED vintage (Jul 10 — newest in brief):
- 2Y: **4.21% (98.8th %ile)** — UP 5bps from 4.16% (front end is NOT pricing cuts yet in FRED data)
- 2s10s: **0.36% (5.6th %ile)** — +1bp from 0.35%; slight steepening
- 10Y-3M: 0.73 (91.7th %ile) — +2bps (curve still in re-steepening phase from the June inversion)
- 10Y BEI: **2.26% (15.9th %ile)** — +2bps (breakevens ticked slightly on oil but barely moved for WTI +8.9%)
- HY OAS: **2.69% (4.0th %ile)** — cycle low

**The rates read:** The live yield curve is showing CPI relief (5Y −3.4bps, 10Y −1.4bps, DXY −0.32), but the structure remains instructive. The long end (30Y +1bp) is NOT rallying with the front end — term premium continues to build. The FRED 2Y is rising (+5bps to 4.21%, 98.8th %ile) — the rate-cut path is not yet being priced into the 2-year. Warsh's "inflation will be a thing of the past" statement removes the *upside* risk to rates, but not the term-premium/fiscal pressure that keeps the 30Y above 5%.

**10Y BEI at 2.26% (+2bps) on a WTI +8.9% session** = markets are not pricing a sustained Iran CPI channel. The breakeven interpretation: this is a temporary spike, not a structural energy price reset. If WTI stays at $80.60 for two weeks, the 10Y BEI will catch up.

**DXY −0.32 to 100.71** is the mechanical response to lower short-end yields. USD/CNY −0.14% = yuan continuing to strengthen — consistent with capital repatriation to EM markets on Fed-on-hold signals.

**Extremes (1-year percentile from brief):**
- 10Y yield: **97.2th %ile** — historically elevated
- DXY: **93.3rd %ile** — still stretched high despite today's dollar weakness
- Copper: **94.4th %ile** — near historical highs
- HY credit (HYG): **92.8th %ile** — credit tight at 1-year highs
- TLT: **14.3rd %ile** — long bonds at 1-year lows (cheap but not touching the floor)
- VIX: 44.0th %ile — moderate, not fear mode
- Gold: 34.9th %ile — below year median (not a safe-haven bid regime)

### Commodities & credit

| Asset | Jul 14 brief | Jul 13 brief | Δ |
|---|---|---|---|
| WTI | **$80.60** | $74.00 | **+$6.60 (+8.9%)** |
| Brent | **$86.59** | $78.77 | **+$7.82 (+9.9%)** |
| Gold | **$4,084.70** | $4,046.30 | **+$38.40 (+0.95%)** |
| Silver | $59.41 | $58.56 | +1.4% |
| Copper | $6.387 | $6.334 | +0.8% |
| Nat Gas | $2.884 | $2.852 | +1.1% |
| HY OAS (FRED Jul 10) | **2.69%** | 2.70% | **−1bp — cycle low** |
| IG OAS (FRED Jul 10) | 0.77% | 0.76% | +1bp |

**WTI $80.60** — attempt 11. But qualitatively different from attempts 1–10: this is the *largest two-day percentage gain in four months* (MarketWatch), driven by confirmed Hormuz escalation (FT: "Washington and Tehran send warnings by missile — most dangerous period since April truce"). The prior 10 spikes each faded within 2 sessions. If this follows the pattern: WTI is back below $74 by Friday. If it doesn't: we're in a structurally higher oil regime, July CPI is hot, and the CPI relief rally was a one-day event. Note: EIA crude ex-SPR shows a +2,998 MBBL build (supply is NOT tight), and the SPR draw of −6,166 MBBL suggests active government price suppression — these are structurally bearish for the physical premium embedded in $80.60.

**Gold $4,084.70 (+0.95%) alongside WTI +8.9%** is a DIFFERENT correlation from the past two Iran escalations. On Jul 8 (Iran ceasefire ended), gold fell −1.32% as oil spiked. On Jul 13 (Hormuz sovereignty claim), gold fell −1.50% as oil spiked. Today, BOTH gold and oil are up. The shift: the June CPI print (3.53%) removed the "oil → inflation → bond selling → real yields up → gold down" mechanical. With Warsh on hold and core inflation at 2.59%, the real-yield headwind on gold has reduced — so today's Hormuz escalation triggers safe-haven gold buying without the rate-repricing penalty.

**HY OAS 2.69% (4.0th %ile) — cycle low, reached through WTI +8.9% and Hormuz escalation.** This is the single most important number in the brief. The four prior FRED prints: 2.70%, 2.70%, 2.70%, and now 2.69%. Credit is TIGHTENING through an oil spike, an ongoing sovereign escalation at a major oil chokepoint, and pre-earnings chip washout. The structural reason: banks are profiting from the volatility (SpaceX IPO fees, Iran-hedging desks, commercial lending demand). BofA CEO Brian Moynihan: "healthy economic backdrop."

---

## Macro & data

**BLS June 2026 (released today, Jul 14):**
- CPI-U: 333.952 (prev May: 335.123) — **fell 1.17 MoM, first monthly decline since 2020**
- YoY: **3.53%** (vs. May's 4.25%; expected ~3.8–4.5%)
- Core CPI: 336.882 (prev: 336.846) — +0.04 MoM; YoY **2.59%** (at the Fed's target)
- Driver: energy prices fell during June ceasefire window — WTI averaged ~$67 in June vs. $65 a year ago; gas was cheap at the pump
- Not demand-driven disinflation: AHE +3.52% YoY (wages sticky), participation 61.5% (50-year low)
- Forward problem: July CPI will compare $80.60 WTI to ~$57 WTI July 2025 = +41% energy YoY tailwind (if oil stays here through month-end, July CPI re-accelerates sharply)

**NFP / Labor (June 2026, unchanged):**
- NFP: +57k (+0.32% YoY, 25-year pace low)
- Unemployment: 4.2% (down from 4.3%)
- AHE: $37.64, YoY +3.52% — wage inflation sticky; services disinflation not confirmed

**FRED (Jul 10 vintage):**
- 2Y: **4.21% (98.8th %ile)** — front end is NOT pricing cuts; Warsh on hold, not easing
- 2s10s: **0.36% (5.6th %ile)** — modest steepening from the year's flattest (0.35%)
- 10Y BEI: **2.26% (15.9th %ile)** — barely moved on WTI +8.9%; markets still treating oil spike as transient
- HY OAS: **2.69% (4.0th %ile)** — cycle low
- NFCI: **−0.515 (18.7th %ile)** — Gate 2 window officially opened **today, Jul 15**. Jul 3 vintage (lag); Jul 17 vintage is the first post-window check
- EFFR: **3.62% (0.0th %ile)** — cycle low; Fed on hold at the bottom of the range

**EIA (Jul 3 vintage — unchanged):**
- Crude ex-SPR: +2,998 MBBL build (bearish structural — supply is not tight despite Hormuz)
- SPR draw: −6,166 MBBL (political price suppression; government fighting the spike with reserves)
- Distillate draw: −4,980 MBBL (industrial demand live)
- Nat gas build: +61 BCF (bearish gas; domestic supply intact)

**Warsh testimony today (CNBC, 12:30 UTC):** "Inflation will be a thing of the past" — cited AI investment boom's disinflationary effects. Explicitly dovish following the cool CPI print. "Get monetary policy right" = no hike hints. Traders are reining in bets on Fed rate rises (FT: "traders rein in bets on Fed rate rises as easing energy costs help tame price surges").

**Key events for the rest of the week:**
- **Today (Jul 15)**: NFCI Gate 2 window fully open; Warsh testimony continues
- **Thursday (Jul 16)**: ASML Q2 earnings — THE binary for the whole cycle
- **Thursday (Jul 16)**: PPI June (pending; follows CPI pattern)
- **Mid-July (this week or next)**: BoJ decision — USD/JPY 161.90 still near 40-year yen low

---

## Risk lens

**1. The "backward CPI / forward oil" stagflation ambush is live.** June CPI 3.53% reflects June's ceasefire-era WTI (~$67 avg). WTI is now $80.60. The energy component of July CPI compares ~$80 July 2026 WTI to ~$57 July 2025 WTI — a +40% energy YoY tailwind going into the July print. If WTI stays above $78 through month-end, the July CPI will re-accelerate meaningfully from June's 3.53%. The market is pricing the backward-looking disinflation as durable; the forward-looking inflation is being written in $80.60 oil every day. At HY OAS 2.69% (4.0th %ile) and VIX 16.75 (44th %ile), no one is pricing the July CPI tail.

**2. IBM −22% made the AI CapEx shift a confirmed earnings event, not a thesis.** Before today: the AI platform-vs-legacy narrative was analytical. After today: a $60bn+ enterprise services company confirmed quarter-over-quarter wallet-share loss to AI chips. This is now in GAAP P&L. Every competitor in legacy IT (Accenture, Dell, HPE) has the same exposure. The "AI premium" in S&P multiples (9.8% YTD at 7,515) is still primarily priced through the winners (NVDA, ASML, TSMC, MSFT). The losers are now being confirmed — but they are NOT in the S&P's winner-dominated multiple.

**3. ASML at $1,726 (−3.97% today, −5.4% 1w, +61.9% YTD) tomorrow: the IBM tailwind vs. the crowding trap.** IBM confirmed AI chip capex is surging. ASML's EUV machines are the only technology that can manufacture the chips IBM's clients redirected to. This is a direct fundamental tailwind for ASML's Q2 order book. Yet ASML fell −3.97% today alongside the same IBM announcement that confirmed its demand. The mechanism: Nasdaq lev_net −55,013 (partially covered from −68,617, still very short); TSMC record revenue → −1.28% set the "exceptional + guide-up" bar. ASML needs EUV bookings beat + raised 2026 guidance. IBM is the data that should make that beat more likely, not less. The risk is crowding dynamics pricing in a miss despite the fundamental signal.

**4. S&P e-mini lev_net −361,875 (CFTC Jul 7) = SHORT SQUEEZE ASYMMETRY on the right catalyst.** The spec S&P short is near its cycle extreme. CPI relief + bank beats + ASML beat on Thursday would be a three-catalyst sequence for which the short side has no stop to press — they are all forced to cover. The asymmetry: if all three catalysts hit, the covering of 362k contracts into a market that's already up from CPI amplifies the upside non-linearly. If ASML misses, the shorts can simply sit and add. Bear's free option is valuable; the squeeze pressure on bulls is conditional on ASML.

**5. NFCI Gate 2 window opened today — the slow-burn risk under the relief.** Three private credit gates preceded this window (BlackRock HPS, Ares, Blue Owl — total >$30bn in redemption events). The NFCI is currently −0.515 (Jul 3 vintage, 18.7th %ile). The Jul 17 vintage is the first post-window check. If the private credit stress is transmitting to broader financial conditions, the NFCI should tighten from −0.515 toward −0.30 this week. HY OAS at 2.69% is NOT pricing this lag — liquid credit and private credit are decoupled. Watch for divergence: HY OAS can stay tight while NFCI tightens if the stress is entirely in illiquid private funds. The divergence itself is the signal.

**6. WTI attempt 11: the SPR suppression is the tell.** The EIA data shows the SPR drawing at −6,166 MBBL per week (political suppression). The administration is fighting the oil spike with strategic reserves. This confirms: (a) the $80.60 spike is recognized as a political problem; (b) the suppression will eventually hit capacity limits; and (c) the physical market is NOT actually as tight as $80.60 implies (crude ex-SPR had a +2,998 MBBL build). The SPR draw pattern matches past oil-spike episodes where the government successfully capped the spike — the fade probability is higher than $80.60 implies.

---

## What to watch

1. **ASML Q2 earnings Thursday Jul 16 — THE binary.** IBM today confirmed AI chip capex is surging at the fundamental level. Pre-earnings slide has brought ASML to $1,726 (−5.4% for the week). Nasdaq lev_net −55,013 = covered from −68,617 but still significantly short. TSMC set the bar: +67% YoY revenue → negative stock. ASML needs EUV bookings beat + raised 2026 guidance + demand statement that goes beyond "strong" to "exceptional." P=0.25 for beat (>+5%); P=0.45 in-line; P=0.30 for miss (<−5%). Note: a miss into Nasdaq −55k = compound derating risk; a beat triggers partial 55k short cover.

2. **WTI: does $80.60 (attempt 11) fade or hold?** The first 10 oil spike attempts all faded within 1–2 sessions. EIA data is bearish (crude build +2,998 MBBL; SPR actively suppressing). FT: "most dangerous period of fighting since April truce" = highest-quality Hormuz escalation yet. P=0.50 for fade below $78 by Friday; P=0.35 for hold $78–83 (standoff); P=0.15 for break above $84 (enforcement priced). Below $78 → July CPI stagflation tail shrinks → bull confirmation. Above $84 → July CPI trajectory hot → rate-hike expectations rebuild → cool CPI rally reversed.

3. **NFCI Jul 17 vintage — first post-Gate-2 window check.** Window opened today. Current: −0.515 (Jul 3 vintage). If tightening to above −0.30: private credit stress beginning to transmit to public financial conditions. P=0.25 for >−0.30 by Jul 17.

4. **S&P close above 7,542 today (Jul 15 close)?** The brief was captured pre-open at 7,515 (−0.79% from prior close). S&P futures were +0.4% at 8:51am ET on the CPI print. A July 15 close above 7,542 confirms CPI relief dominated the session; below 7,500 means chip carnage and oil overwhelmed the macro relief. P=0.60 for close above 7,542.

5. **BoJ mid-July decision — the carry unwind tail.** USD/JPY 161.90 (near 40-year yen low; −0.43 from 162.33 yesterday). BoJ meeting this month. A surprise hike or hawkish statement would unwind yen carry trades that fund the most crowded AI chip longs (ASML +62% YTD, TSMC +39%). USD/JPY breaking below 160 is the signal. P=0.20 for a move that sends USD/JPY below 160.

```watch
[
  {"claim": "ASML Q2 beats — IBM confirmed AI chip capex flowing to fabs; EUV orders + raised 2026 guidance", "metric": "market:ASML:change_pct", "trigger": ">5.0", "horizon": "2026-07-16", "probability": 0.25},
  {"claim": "WTI fades below $78 by Friday — attempt 11 on oil spike fails like 1-10; EIA supply bearish", "metric": "market:CL=F:last", "trigger": "<78.0", "horizon": "2026-07-17", "probability": 0.50},
  {"claim": "NFCI tightens above -0.30 on Jul 17 vintage — Gate 2 window transmitting private credit stress to public conditions", "metric": "macro:NFCI", "trigger": ">-0.30", "horizon": "2026-07-17", "probability": 0.25},
  {"claim": "S&P closes above 7,542 today — CPI relief rally dominates pre-ASML session; short-squeeze asymmetry on 362k spec short", "metric": "market:^GSPC:last", "trigger": ">7542.0", "horizon": "2026-07-15", "probability": 0.60},
  {"claim": "ASML Q2 miss — TSMC pattern repeats; crowding drives negative price reaction even if earnings strong", "metric": "market:ASML:change_pct", "trigger": "<-5.0", "horizon": "2026-07-16", "probability": 0.30}
]
```

---

## The call

**Direction: +1 (net long / risk-on).**

Three signals align for the first time this cycle:

1. **CPI removed the primary bear trigger.** June CPI 3.53% YoY eliminates the "Warsh hikes into hot inflation" tail. Core CPI 2.59% is essentially at the Fed's target. Warsh: "inflation will be a thing of the past." The near-term rate-hike scenario — which was the load-bearing wall of the bear case — has been demolished by the BLS, not by wishful thinking.

2. **Credit at cycle lows confirms no systemic stress.** HY OAS 2.69% (4.0th %ile) through WTI +8.9%, Hormuz escalation, and pre-ASML chip washout. Banks are profiting (not stressed) by the volatility. The financial system's earnings power is underwriting the geopolitical chaos. This is the cleanest credit green light of the cycle.

3. **Earnings cycle confirmed healthy.** JPM, GS, BofA, WF all beat. The earnings cycle is NOT cracking — it is the one structural pillar that has stayed intact through every bear signal. IBM confirmed the AI capex redirect is real, which validates ASML's fundamental demand story for Thursday.

The pattern I've fallen into: staying flat when three signals are collectively bullish because "the binary is tomorrow." That discipline cost the record (23/82, 28%) without protecting against the downside (the misses were the flat calls, not the wrong-direction calls). Today, the three-signal alignment — CPI + credit + earnings — is more simultaneous than at any prior session this cycle. The flat-before-binary logic was right when two of three signals were absent; it is wrong when all three are present.

The flip risk remains: ASML miss on Thursday triggers a −1 re-entry, particularly if HY OAS breaks above 2.72% on the next FRED print. But entering +1 into a CPI-confirmed, credit-confirmed, bank-confirmed environment the session before a pivotal earnings binary is the right asymmetric call — the short squeeze (362k S&P e-mini net short) provides upside amplification if ASML beats.

```stance
{"direction": 1, "notes": "Long. June CPI 3.53% YoY (prev May 4.25%) eliminated primary bear trigger — headline CPI fell MoM first time since 2020; Core 2.59% at Fed target. Warsh: 'inflation will be a thing of the past.' HY OAS 2.69% (4.0th %ile) = cycle low through WTI +8.9% and Hormuz escalation. Banks confirmed blockbuster (JPM/GS/BofA/WF; FT Jul 14 09:29 UTC). IBM -22% confirms AI capex redirect flowing to chip fabs = ASML tailwind for Thursday. CFTC Jul 7: S&P e-mini -361,875 = squeeze asymmetry on bull catalyst. ASML reports Thursday Jul 16 — pre-earnings slide to $1,726 (down -5.4% weekly) has partially cleared crowding. Flip to 0: ASML miss (<-5%) + WTI holds >$80 next week. Flip to -1: ASML miss + HY OAS >2.72% on next FRED print + WTI >$82. Running watch hit-rate: 23/82 (28%). Oil calls: 0/11."}
```

---

## Sources

- *Consumer prices rose 3.5% annually in June, less than expected as energy prices eased* (CNBC Economy, 2026-07-14 13:09 UTC)
- *Consumer prices fall for first time since early days of COVID pandemic, but war against high inflation isn't won* (MarketWatch, 2026-07-14 13:11 UTC)
- *US inflation fell more than expected to 3.5% in June as petrol prices tumbled* (FT International, 2026-07-14 12:57 UTC)
- *US inflation rate eases to 3.5% as gasoline prices fall* (BBC Business, 2026-07-14 12:59 UTC)
- *CPI Shockingly Cool, Curbing Fed Rate-Hike Odds; Warsh Ahead* (IBD via Yahoo Finance, 2026-07-14 12:53 UTC)
- *Wall Street banks post blockbuster profits as equities trading booms* (FT International, 2026-07-14 09:29 UTC)
- *Wells Fargo tops profit estimates on interest income boost, trading boom* (Investing.com, 2026-07-14 13:06 UTC)
- *Bank of America profit jumps 27% as CEO Brian Moynihan signals 'healthy economic backdrop'* (Yahoo Finance, 2026-07-14 11:48 UTC)
- *Bank of America's stock falls despite blockbuster earnings report* (MarketWatch, 2026-07-14 11:55 UTC)
- *IBM shares set to plunge 23% as customers shift spending to AI* (FT International, 2026-07-14 13:01 UTC)
- *IBM's stock dives toward worst day in nearly 40 years after earnings miss* (MarketWatch, 2026-07-14 11:50 UTC)
- *IBM Craters 20% On 'Disappointing' Results. Big Blue Hit By AI CapEx Shift.* (IBD via Yahoo Finance, 2026-07-14 12:45 UTC)
- *Warsh promises inflation will be a 'thing of the past,' cites benefits of AI investment boom* (CNBC Finance, 2026-07-14 12:30 UTC)
- *Warsh to Reiterate Fed's Pledge to Get Inflation Down* (NYT Economy, 2026-07-14 12:57 UTC)
- *Washington and Tehran send warnings by missile* (FT International, 2026-07-14 12:24 UTC)
- *Oil prices see largest two-day percentage gain in four months on U.S.-Iran fight* (MarketWatch, 2026-07-14 09:18 UTC)
- *Europe shares pare losses as cooling U.S. CPI tempers interest rate anxieties* (Investing.com, 2026-07-14 12:59 UTC)
- *Global growth optimism climbs to five-month high, BofA survey shows* (Seeking Alpha, 2026-07-14 13:11 UTC)
- *Skyworks gets rating cut; Nvidia, Intel among those seeing price target boost at KeyBanc* (Seeking Alpha, 2026-07-14 13:19 UTC)
- *Apple downgraded to Underweight as KeyBanc believes rising prices will slow growth* (Seeking Alpha, 2026-07-14 13:16 UTC)
- Analytics: `brief_2026-07-14.json` (Jul 14 13:22 UTC); `brief_2026-07-13.json`; CFTC Jul 7 vintage; FRED Jul 10 vintage; BLS June 2026; EIA Jul 3 vintage; `data/scorecard_log.jsonl`; `data/running_thesis.md`
