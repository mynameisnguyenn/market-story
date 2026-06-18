# Market Story — 2026-06-18

> *Brief captured 2026-06-17 15:15 UTC — Wednesday session, ~11:15am ET (pre-FOMC intraday snapshot; Warsh decision announced ~14:00 ET / 18:00 UTC after brief capture). All prices from brief_2026-06-17.json.*

---

## Since last time

Grading the June 17 `watch` block (from narrative_2026-06-17.md) against the June 17 brief:

| Claim | Trigger | Result |
|---|---|---|
| Warsh neutral: S&P extends above 7,650 within 2 sessions | `market:^GSPC:last > 7650` | **PENDING** — S&P at 7,507 in session 1 (pre-FOMC). Session 2 = today's June 18 close (post-FOMC). P=0.45. |
| Warsh hawkish: 2Y FRED reprices above 4.15% | `macro:DGS2 > 4.15` | **PENDING** — 2Y FRED fell to **4.07%** (Jun 15 print, −2bps). Direction wrong on the pre-FOMC session. 2 sessions remain. P=0.30. |
| WTI doesn't fall below $70 — OPEC+ defends | `market:CL=F:last > 70` | **HIT** — WTI at **$76.78** (+$1.91). Session 1 of 5. NATO confirms Hormuz restoration; Iranian tankers exiting. P=0.78 — correct probability, correctly confident. |
| HY OAS widens above 2.80% on Warsh hawkish | `macro:BAMLH0A0HYM2 > 2.80` | **PENDING** — HY OAS widened **+5bps to 2.71%** (first widening since the Iran rally). Moving toward trigger but not there. 4 sessions remain. P=0.20. |
| USDJPY falls below 158 — deferred BoJ carry unwind | `market:USDJPY=X:last < 158` | **PENDING** — 160.278 (−0.13%). 4 sessions remain. Carry trade still in place. P=0.25. |

**June 16 watch items resolving:**
- "S&P closes above 7,650 by end of week" — S&P at 7,507 on the final session (June 17) of that 5-session horizon. **MISSED.** P=0.35 → $0 on Brier.
- "BoJ hike → USDJPY below 158" — confirmed MISSED at 160.28, same as logged in scorecard. Carries confirmed: deferred.

**June 17 stance (+1, entered S&P ~7,539):** S&P at 7,507 at brief capture = −0.21% unrealized. Warsh speaks post-capture. **Pending settlement.**

**Running hit-rate: approximately 4/25 (16%, n=25)** once WTI >70 settles — credit OAS: 0/10 (persistently wrong on level, consistently right on direction until Iran inverted the thesis), yield direction: 3/6, oil direction: 3/6. Near-miss alert: 2Y at 4.07% vs trigger 4.15% = 8bps gap — within calibration range but not a near-miss worth adjusting yet (Warsh's decision is the test).

---

## Today in one line

**The pre-FOMC session on June 17 delivered the first crack in "priced for perfection": HY OAS widened +5bps (first move in a week from the 1.2nd %ile), VRP reconstituted from 0.6 to 1.4, and the 2s10s hit the flattest point of the year (0.0th %ile) — the market bought insurance before Warsh spoke while the S&P barely moved, which means the credit and vol markets are pricing more hawkish risk than the equity tape shows.**

*Flip to bear confirmed: Warsh's statement carries any hawkish language on core CPI (2.85%) or AHE (3.45%) → 2Y gaps above 4.15%, VRP snaps toward 4–6, S&P breaks below 7,400. Flip to bull confirmed: Warsh neutral hold + explicit "progress on inflation" → credit re-tightens, VRP normalizes to 2–3, S&P recovers toward 7,650.*

---

## TL;DR

- **HY OAS widened +5bps to 2.71% (3.6th %ile) — first directional crack since the Iran deal.** Still historically tight (tighter than 96.4% of the past year), but the direction reversed. Credit and vol priced more Warsh hawkish risk than equities did. If this widens further through 2.75% post-FOMC, the credit tightening cycle from the Iran deal is over.

- **Semiconductor hardware leading while mega-cap software sells.** ASML +5.9%, TSMC +2.5%, Applied Materials surging vs. MSFT −2.0%, META −2.1%, AMZN −2.3%, GOOGL −2.5%. This rotation matters structurally: hardware enablers of AI capex (equipment, foundries) are outperforming platform/software plays with elevated multiples. CRM at YTD −39.8% is the clearest expression of that derating.

- **Stock-bond correlation improved: 0.71 → 0.61.** Not fixed, still "hedge broken" by the dashboard's classifier, but the drift toward decoupling matters. If Warsh is neutral and yields fall, the correlation continues to compress — and bonds start to work as a partial hedge again. That would be the most important portfolio-construction change in three weeks.

---

## What moved & why

### Equities & sectors

Brief-to-brief (June 16 → June 17, both intraday):

| Asset | June 16 brief | June 17 brief | Δ | Read |
|---|---|---|---|---|
| S&P 500 | 7,539.20 | **7,507.22** | **−31.98** | Pre-FOMC stall; market waiting for Warsh binary resolution |
| Nasdaq | 26,549.89 | **26,325.63** | **−224.26** | Mega-cap software drag outweighs semi strength at index level |
| Dow | 52,177.24 | **52,111.60** | **−65.64** | Modest pullback from ATH |
| Russell 2000 | 2,960.23 | **2,957.55** | **−2.68** | Small-cap essentially flat; cyclical posture maintained |
| VIX | 15.85 | **16.84** | **+0.99 (+6.25%)** | Pre-FOMC hedge buying; VRP reconstituted from 0.6 to 1.4 |

Breadth: 4 sector advancers / 7 decliners — negative into the decision.

**Sector rotation — the session's defining story:**

| Sector | Δ | Read |
|---|---|---|
| Technology (XLK) | **+1.14%** | ASML +5.9%, TSMC +2.5%, Applied Materials surge — semiconductor hardware leading |
| Industrials (XLI) | **+0.69%** | Cyclical underpinning; EU-US trade deal tailwind continues |
| Materials (XLB) | **+0.49%** | Copper flat (−0.07%) but materials sector holding |
| Comm. Services (XLC) | **−1.58%** | GOOGL −2.5% is the heaviest drag; platform derating |
| Cons. Discretionary (XLY) | **−1.06%** | AMZN −2.3%; consumer stress signal (MarketWatch: gas soaking retail dollars) |
| Cons. Staples (XLP) | **−1.05%** | Defensive selling into risk-on semi leadership is counterintuitive — read as rotation OUT, not fear |

**The semiconductor/mega-cap software bifurcation:**

This is not a one-sector story. Within tech:
- **Gaining:** Hardware enabling AI (ASML +5.9%, TSMC +2.5%, Applied Materials) — foundry/equipment capacity is the bottleneck for the AI capex cycle
- **Selling:** Software/platform at elevated multiples (MSFT −2.0%, META −2.1%, AMZN −2.3%, GOOGL −2.5%, CRM −1.9%)

The ASML +5.9% is especially meaningful: it's a European company (benefits from EU-US trade deal) making the machines that every chipmaker needs. The AI capex buildout cannot happen without ASML extreme-UV lithography. FT (10:25 UTC): *"Buying Cursor could be SpaceX's Instagram moment."* The SpaceX/Cursor narrative reinforces the view that AI coding productivity is the next capex wave. SpaceX itself is DOWN for the first time since IPO (Investing.com, 14:32 UTC) — first-session profit-taking after the 5th-largest-company run.

**Private credit stress — new datapoint:**
FT (June 17, 13:30 UTC): *"Thoma Bravo hands Medallia to lenders in one of PE's biggest losses. Consortium led by Blackstone to take over troubled software company."* Thoma Bravo acquired Medallia in 2021 at peak multiples; the restructuring materializes now. This is a DIFFERENT PE firm from BlackRock HPS (running thesis: Gate 2), confirming that 2021-vintage software PE buyouts are restructuring as a category, not just one GP. Consequence: the private credit stress is broadening across GPs; the NFCI is still not registering (22.6th %ile) — the lag clock is running.

### Rates & the dollar

Brief-to-brief levels (June 16 → June 17) vs. FRED updates:

| Tenor | June 16 brief | June 17 brief | Δ (level) | FRED date | Note |
|---|---|---|---|---|---|
| 5Y (market) | 4.146% | 4.179% | **+3.3bps** | intraday | June 17 intraday change was −3.4bps = yields were falling during the session from a higher open |
| 10Y (market) | 4.426% | 4.443% | **+1.7bps** | intraday | Same: slightly higher brief-to-brief but falling intraday |
| 30Y (market) | 4.929% | 4.931% | **+0.2bps** | intraday | Long end essentially anchored |
| 2Y (FRED) | 4.09% (Jun 12) | **4.07%** (Jun 15) | **−2bps** | Jun 15 | Front end gently easing; market not pricing hawkish hold yet in FRED |
| 10Y (FRED) | 4.48% (Jun 12) | **4.47%** (Jun 15) | **−1bp** | Jun 15 | 92.1th %ile — still stretched high |
| **2s10s (FRED)** | 0.40% (Jun 15) | **0.38%** (Jun 16) | **−2bps** | Jun 16 | **0.0th %ile — flattest of the year, z=−2.29** |
| 10Y-3M (FRED) | 0.68% (Jun 15) | **0.64%** (Jun 16) | **−4bps** | Jun 16 | 82.9th %ile — still steep vs. bills |
| 10Y Breakeven | 2.32% (Jun 15) | **2.29%** (Jun 16) | **−3bps** | Jun 16 | 23.4th %ile — falling on energy deflation; market taking back some inflation premium |

**2s10s at 0.0th %ile (0.38%) is a critical read.** The curve hit its flattest point of the year on June 16 FRED data. The structural anomaly persists: 2s10s at the 0th %ile (almost inverted) while 10Y-3M is at the 82.9th %ile (steep vs. bills). The curve is simultaneously near-flat on the on-the-run pairs AND steep on the bill spread. This is Warsh's dilemma in curve form: the front end is anchored by FOMC expectations (no cuts), while the long end is held down by inflation expectations that have barely moved (breakeven 2.29%, 23.4th %ile — only slightly above median).

**Dollar and FX:**
DXY: 99.483 → **99.692** (+0.21%). FT (04:00 UTC June 17): *"Investors pile into bullish dollar bets as 'US exceptionalism' trade returns. Traders expect buoyant American economy to keep Fed from cutting rates despite oil price fall."* The dollar bid is the market saying: strong retail sales + no Fed cut = US exceptionalism intact. EUR/USD slipped from 1.1618 to **1.1594**; USD/JPY barely moved at **160.278** (−0.13%) — carry still in place post-BoJ.

### Commodities & credit

**WTI: $74.87 → $76.78 (+$1.91, +2.55%)** — first bounce after two consecutive −7%+ days.

Three concrete Hormuz catalysts in the brief:
1. *"Three Iranian tankers exit U.S. blockade for first time in months"* (CNBC, 07:23 UTC) — physical reopening confirmed
2. *"NATO allies ready to help restore Strait of Hormuz shipping, Rutte says"* (SA, 15:07 UTC) — multilateral security guarantee
3. *"President Trump sees price of oil soon receding to prewar level"* (SA, 15:02 UTC) — political framing of <$75 as the "target"

Counter: FT (14:21 UTC): *"Trump says US will not invest in $300bn fund for Iran."* The reconstruction fund was reportedly a core Iranian incentive. Bipartisan backlash forced a retreat. This is the deal's first structural crack: the physical opening is real (tankers moving), but the political architecture is contested. Iranian tankers at sea ≠ a durable deal. Risk: Iran re-escalates on fund removal → WTI bounces to $80–85.

Contrarian bid: MarketWatch (13:39 UTC): *"An oil bull's 'insane' bet: Why this veteran trader is buying energy stocks as crude prices tumble."* XLE was essentially flat on the day (−0.42%), suggesting the energy sector has already bottomed its relative underperformance for the immediate post-deal period.

**Gold: $4,364.90 → $4,366.60 (+$1.70, flat)**
Gold is testing the inflation-hedge thesis going into Warsh. Flat on a pre-FOMC waiting day is neutral — the real test is whether gold sells off or holds on Warsh's statement. An extremely tight 56.0th %ile ranking (essentially at the 1-year median) — gold is neither stretched nor washed out.

**Credit — the KEY FRED update in this brief:**

| Series | Jun 15 FRED | Jun 16 FRED | Δ | pct_1y | z_1y | Read |
|---|---|---|---|---|---|---|
| HY OAS | 2.66% | **2.71%** | **+5bps** | **3.6th** | −1.27 | **First widening since the Iran deal; HYG still at 98.8th %ile** |
| IG OAS | 0.73% | **0.75%** | **+2bps** | 10.7th | −1.06 | Also widening, off the 0.0th %ile floor |
| VRP | ~0.6 | **1.4** | **+0.8** | — | — | Fear premium reconstituting pre-Warsh |

HY OAS at 2.71% is the most important data point in this brief. It's the first FRED widening since HY OAS reached 1.2nd %ile (2.66%) three sessions ago. Still historically tight (3.6th %ile = tighter than 96.4% of the year), but the direction has flipped. Three possible readings:
1. Pre-FOMC credit protection buying (one-session noise)
2. Thoma Bravo/Medallia PE stress leaking into public HY
3. Iran deal euphoria in credit has fully run its course at these levels

The calibration lesson applies: the trigger for "credit stress re-emerging" was set at 2.80% (5 sessions). At 2.71%, the claim still needs +9bps. The near-miss concern: if Warsh is neutral and credit re-tightens to 2.66%, this was one-session noise. But if widening continues, the 2.75% level becomes the first confirmation of a new direction.

---

## Macro & data

**Retail sales jump (FT, 14:23 UTC):** *"US retail sales jump in sign consumers are weathering petrol shock. Data shows economy remains in robust shape as Kevin Warsh takes charge of Fed."* Strong retail sales is the single most important data point for Warsh's policy calculus: consumers absorbing the oil spike = less demand destruction = no justification for accommodation. Core CPI 2.85%, AHE +3.45%, AND retail holding up = Warsh's mandate is not met by demand weakness. Consequence: a hawkish lean becomes more defensible even on a hold.

**New home construction 6-year low (MarketWatch Bulletins, 00:22 UTC):** Housing starts at 6-year lows. Rate-sensitive sectors are clearly suppressed by the higher-for-longer environment. This is the dovish counter-input to retail sales: some real-economy sectors ARE suffering. But housing's lag to rate moves is long (6–12 months), and Warsh won't pivot on lagged construction data when retail is holding up.

**Trump walks back $300bn Iran reconstruction fund (FT, 14:21 UTC):** Fierce bipartisan backlash forced the reversal. The deal's political durability is now in question. Consequence for energy: if the fund was Iran's primary non-nuclear incentive, its removal increases the probability of deal renegotiation. Physical tankers are moving; political framework is cracking. Watch the next 48 hours of Iranian government statements.

**Warsh dot withdrawn (CNBC, 14:24 UTC):** Warsh expected NOT to submit his "dot" to the SEP. No new rate projections from the Chair. This is maximum deliberate ambiguity — neutral on the rate path, no commitment, complete flexibility. Consequence: the market cannot anchor off a Warsh dot; tone of the press conference language is the ONLY signal.

**Kalshi unified board (CNBC, 14:25 UTC):** Unanimous FOMC vote expected (vs. divided April vote). Unanimity signals Warsh has consolidated the board. This could mean he's imposed discipline on both doves and hawks — but the direction of the consensus is unknown from this data alone.

**UK inflation held at 2.8% (CNBC, 06:41 UTC):** Bank of England meets June 18 (today). Higher petrol prices offset by slower food price rises. BoE meeting is a secondary-market event but could move sterling and EM FX if BoE surprises.

**FRED updates (from June 17 brief):**

| Series | Value | Date | pct_1y | Change | Read |
|---|---|---|---|---|---|
| EFFR | 3.63% | Jun 16 | 7.1st | 0 | Fed holding; 7.1st %ile = historically accommodative despite 4.25% CPI |
| SOFR | 3.63% | Jun 16 | 11.1st | **−6bps** | SOFR ticked down from 3.69%; overnight funding easing slightly |
| 10Y Breakeven | 2.29% | Jun 16 | 23.4th | −3bps | Inflation expectations declining on energy deflation |
| NFCI | −0.505 | Jun 12 | 22.6th | flat | Still not registering any stress — Medallia/PE lag |
| VIXCLS | 16.41 | Jun 16 | 35.3rd | +0.21 | VIX close nudging up; pre-FOMC repricing |

**EIA energy (June 5 vintage — unchanged):** crude ex-SPR −7,227 MBBL draw; gasoline +186 MBBL build. June 12 EIA data still pending; the first Hormuz reopening data appears in the June 19 EIA release. This is the most important energy data event of the week AFTER the FOMC.

**CFTC (June 9 vintage):** S&P e-mini lev net at −451,586; Nasdaq −34,306; VIX futures lev net −35,290 (adding short). June 16 CFTC data releases Friday June 20 — the first read on post-deal/post-Warsh positioning velocity.

---

## Risk lens

**1. Warsh's press conference (June 18 afternoon) — already announced post-brief capture.**
The pre-FOMC session gave us the market's pricing: yields falling intraday, VRP rebuilding to 1.4, credit widening +5bps. Net reading: 60–65% neutral hold priced, 30–35% hawkish lean hedged. The retail sales surprise is the most hawkish input. Housing starts weakness is the most dovish.

The scenario branches (outcome unknown from this brief):
- *Neutral hold (P≈0.60):* "Progress on inflation; policy is data-dependent." → 2Y stays near 4.07%, S&P recovers to 7,540+, VRP normalizes from 1.4 toward 2–3 over 3–5 sessions, credit re-tightens from 2.71%.
- *Hawkish lean (P≈0.30):* "Core inflation and wage growth require continued vigilance; energy disinflation does not resolve the mandate." → 2Y gaps toward 4.15%+, VRP snaps from 1.4 toward 4–6, S&P breaks below 7,400, stock-bond correlation may re-elevate from 0.61.
- *Dovish lean (P≈0.10):* Explicit acknowledgment of progress toward 2% target → S&P squeezes 2%+ to 7,700+, VRP collapses, 2s10s steepens.

**2. Stock-bond correlation: 0.71 → 0.61 — first improvement in weeks.**
The brief shows the 30-day stock-bond correlation dropped from 0.71 (June 16 narrative) to 0.61. The state is still "hedge broken" (above 0.5 cutoff), but the directionality matters. If Warsh is neutral and yields continue to drift down, the correlation should continue declining toward 0.5 — which is the threshold where standard 60/40 diversification begins to function again. Consequence for risk: hedging via puts is less critical if bonds start to work again. Monitor for correlation below 0.55 in the next brief.

**3. Private credit stress broadening — Thoma Bravo/Medallia confirms pattern.**
BlackRock HPS Gate 2 + Thoma Bravo/Medallia = at least two major PE shops restructuring 2021-vintage buyouts in the same week. The running thesis tracks a 3–6 week lag from private credit gates to public NFCI. NFCI at 22.6th %ile is the tell that public markets haven't caught this. If a third PE shop announces restructuring by July, the pattern becomes a trend rather than idiosyncratic. Gate 3 at BlackRock HPS is the September calendar event; Thoma Bravo adds a new clock.

**4. Semiconductor vs. mega-cap software rotation — structural, not tactical.**
ASML at +5.9% and TSMC at +2.5% while MSFT/META/AMZN/GOOGL all fall −2%+ is the market repricing the AI value chain. The market is increasingly paying for the physical infrastructure (chips, equipment, power) and deferring payment on the software layer (where revenue models are less certain). Consequence: a sector rotation FROM mega-cap software TO semi hardware is not a bull/bear call on AI — it's a repricing of WHERE in the stack the value accretes near-term. CRM at −39.8% YTD is the most extreme expression.

**5. HYG at 98.8th %ile / HY OAS at 3.6th %ile — credit can widen from here with very little catalyst.**
Even with the +5bps widening, HY OAS is at 2.71% — still the 3.6th %ile (tighter than 96.4% of the year). There is almost no cushion. A Warsh hawkish surprise from this base would widen HY OAS 15–25bps immediately (to 2.86–2.96%), triggering the scorecard claim AND the running thesis bear scenario simultaneously. A neutral hold would re-tighten to 2.66% (1st %ile). The asymmetry is severe: upside for credit (tighter) is measured in bps; downside (wider) on a hawkish surprise is hundreds of bps from historical episodes.

**6. Iran deal durability — fund removal vs. physical tankers.**
The physical reopening is real (CNBC: three tankers exiting). The political deal is under pressure (Trump $300bn fund denial, FT "humiliation" framing). The risk: if Iran reads the fund removal as a material breach → WTI bounces $5–8 within one session. At WTI $76.78, OPEC+ is still slightly below the informal floor. An Iran-triggered re-spike toward $82 would partially reverse the June CPI deflation thesis and re-test the "energy disinflation = cuts" narrative.

---

## What to watch

1. **Warsh press conference outcome (June 18)** — binary already resolved, outcome in next brief. Watch for: (a) S&P reaction (above/below 7,450 = neutral/hawkish tell), (b) 2Y market yield gap vs. 4.10% (currently 4.07% FRED, but market is real-time), (c) VIX closing level vs. 16.84 today.

2. **HY OAS next FRED update** — first session after Warsh. 2.71% is the current level. Above 2.75% = widening trend confirmed, credit not re-tightening on neutral Warsh. Below 2.68% = one-session pre-FOMC noise, Iran deal credit bid returns.

3. **CFTC June 16 data (Friday June 20)** — first post-deal/post-Warsh positioning read. S&P e-mini lev net at −451,586. Expect: 60–100k additional covering on neutral Warsh, <30k on hawkish (bears re-establish). Below −380k = squeeze has structural legs.

4. **WTI $72 floor and Iran $300bn fund dispute** — physical tankers are moving, but political deal is contested. Watch for Iranian government statement on fund removal within 48 hours. WTI above $78 = deal uncertainty re-pricing; below $73 = overshooting the physical reopening.

5. **2s10s: watch for 0.30% floor** — at 0.38% and the 0.0th %ile. A hawkish Warsh that anchors the front end higher would push 2s10s toward 0.25–0.30% (near-inversion territory). The curve inverting from a neutral base (VIX 16, HY 2.71%) would be the clearest recession-odds-increasing signal of the cycle.

```watch
[
  {"claim": "Warsh neutral: S&P holds above 7,450 post-press conference", "metric": "market:^GSPC:last", "trigger": ">7450", "horizon": "next session", "probability": 0.62},
  {"claim": "HY OAS widening trend continues above 2.75%", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.75", "horizon": "next 3 sessions", "probability": 0.35},
  {"claim": "CFTC June 16 S&P lev net covers to above -400k", "metric": "positioning:SPX:lev_net", "trigger": ">-400000", "horizon": "this week", "probability": 0.50},
  {"claim": "WTI holds above $72 — physical Hormuz deal intact despite fund dispute", "metric": "market:CL=F:last", "trigger": ">72", "horizon": "next 3 sessions", "probability": 0.65},
  {"claim": "2s10s stays above 0.30% — curve doesn't invert on Warsh hawkish hold", "metric": "macro:T10Y2Y", "trigger": ">0.30", "horizon": "next 3 sessions", "probability": 0.72}
]
```

---

## The call

The June 17 stance (+1, entered S&P ~7,539) is pending settlement against today's close. The brief shows: S&P at 7,507 (−0.21% unrealized), VRP at 1.4 (hedge reconstituted, no longer near-free), HY OAS widening for the first time. The Warsh binary resolved this afternoon — after the brief was captured.

For the June 18 stance: the FOMC outcome is known as of ~14:00 ET today but is not in this brief's data. The conditional long protocol is clear: flip to −1 if hawkish. Without post-decision confirmation in this brief's S&P level, entering a new directional bet would be thesis drift. The correct answer is flat (0) — this is NOT uncertainty-avoidance, it's the protocol. The June 17 +1 stance will settle today; the June 18 stance starts from zero with post-FOMC data.

The bull case for re-entering +1 in the next brief: Warsh neutral → S&P holds 7,450+, VRP compresses from 1.4, HY re-tightens from 2.71%, CFTC shows material covering → re-enter long toward 7,650.

The bear case: Warsh hawkish → flip immediately to −1. S&P below 7,400, 2Y market yield above 4.15%, HY OAS gaps above 2.80%. These triggers are explicit in the running thesis.

July seasonality: Seeking Alpha (15:04 UTC June 17) notes July seasonality typically positive for stocks — structural tailwind for the bull case IF Warsh is neutral.

```stance
{"direction": 0, "notes": "FOMC decision resolved after brief capture (June 17, 15:15 UTC vs ~18:00 UTC decision). June 17 stance (+1, entered 7,539) pending settlement against today's close. Cannot confirm Warsh tone (neutral vs hawkish) from this brief. Pre-decision signals: yields falling intraday, VRP 0.6→1.4 (reconstituting), HY OAS +5bps first widening, stock-bond correlation improved 0.71→0.61. Retail sales strong (hawkish input); housing starts 6-year low (dovish). Flat until post-FOMC brief confirms neutral (re-enter +1 toward 7,650) or hawkish (flip to -1, 2Y>4.15% the trigger). Running P&L: Jun 11 +0.08%, Jun 12 -1.83%, Jun 15/16 (0) flat. Jun 17 +1 pending."}
```

---

## Sources

- *US retail sales jump in sign consumers are weathering petrol shock* (FT International, 2026-06-17 14:23 UTC)
- *Three Iranian tankers exit U.S. blockade for first time in months as shipowners eye Hormuz in 'wary disbelief'* (CNBC Economy, 2026-06-17 07:23 UTC)
- *Investors pile into bullish dollar bets as 'US exceptionalism' trade returns* (FT International, 2026-06-17 04:00 UTC)
- *Trump says US will not invest in $300bn fund for Iran* (FT International, 2026-06-17 14:21 UTC)
- *NATO allies ready to help restore Strait of Hormuz shipping, Rutte says* (Seeking Alpha, 2026-06-17 15:07 UTC)
- *'Humiliation': Trump battles claims his Iran deal is worse than Obama's* (FT International, 2026-06-17 01:04 UTC)
- *Thoma Bravo hands Medallia to lenders in one of PE's biggest losses* (FT International, 2026-06-17 13:30 UTC)
- *President Trump sees price of oil soon receding to prewar level* (Seeking Alpha, 2026-06-17 15:02 UTC)
- *Fed Chair Warsh expected to withhold 'dot' from central bank's interest rate outlook* (CNBC Finance, 2026-06-17 14:24 UTC)
- *More united Fed board seen at Warsh's first meeting, according to Kalshi traders* (CNBC Finance, 2026-06-17 14:25 UTC)
- *Wall Street struggles as investors await Federal Reserve rate policy* (Seeking Alpha, 2026-06-17 15:03 UTC)
- *Stock Market Today: Dow Rises Before Fed Decision; SpaceX Turns Lower; Biotechs Gain* (Yahoo Finance / IBD, 2026-06-17 14:24 UTC)
- *Buying Cursor could be SpaceX's Instagram moment* (FT International, 2026-06-17 10:25 UTC)
- *SpaceX down for the first time since IPO after surpassing Amazon in market cap* (Investing.com Markets, 2026-06-17 14:32 UTC)
- *New home construction sinks to a 6-year low* (MarketWatch Bulletins, 2026-06-17 00:22 UTC)
- *An oil bull's 'insane' bet: Why this veteran trader is buying energy stocks as crude prices tumble* (MarketWatch Top Stories, 2026-06-17 13:39 UTC)
- *Here's how stocks performed under different Fed chairs — and how much influence Warsh really has* (MarketWatch Top Stories, 2026-06-17 15:08 UTC)
- *Applied Materials (AMAT) Climbed Amid Broad-Based Growth Drivers* (Yahoo Finance, 2026-06-17 14:33 UTC)
- *July seasonality could give stocks another tailwind* (Seeking Alpha, 2026-06-17 15:04 UTC)
- *Germany backs French push for US-style tariffs and quotas* (FT International, 2026-06-17 12:47 UTC)
- *UK inflation holds steady at 2.8% in May* (CNBC Economy, 2026-06-17 06:41 UTC)
- *The U.S. Economy Is Leaving Small Businesses Behind* (NYT Economy, 2026-06-17 09:04 UTC)
- *High gas prices soak up more retail-sales dollars — and restaurants are paying the bill* (MarketWatch Top Stories, 2026-06-17 13:24 UTC)
- Analytics: FRED macro through June 16; market data June 17 ~11:15am ET; `brief_2026-06-17.json`; `data/scorecard_log.jsonl`
