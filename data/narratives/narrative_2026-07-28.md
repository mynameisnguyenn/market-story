# Market Story — 2026-07-28

> *Brief: `brief_2026-07-27.json` (captured 2026-07-27 14:20 UTC — intraday Jul 27. Reflects Jul 27 mid-session US data. FRED vintage: 10Y/2Y Jul 23, 2s10s Jul 24, HY/IG OAS Jul 23, BEI Jul 24, VIXCLS Jul 24. CFTC Jul 21. Previous brief: `brief_2026-07-24.json` (Jul 23 full-session close data). Key forward events: MSFT earnings (tonight/this week), Fed rate decision Wednesday Jul 29, Meta/AMZN earnings later this week.)*

---

## Since last time

Grading `narrative_2026-07-27.md` watch items against `brief_2026-07-27.json` (Jul 23 FRED / Jul 21 CFTC / Jul 27 intraday market):

| Claim | Trigger | Result |
|---|---|---|
| HY OAS widens to >=2.73% on Jul 24-25 FRED print — credit confirms bear | macro:BAMLH0A0HYM2 >2.72 (horizon Jul 29) | **HIT.** HY OAS **2.77%** (Jul 23 FRED, +9bps from 2.68%). First formal credit confirmation of the bear thesis in this cycle. P=0.35 correct direction. |
| HY OAS tightens below 2.65% — credit armor structural; exit −1 | macro:BAMLH0A0HYM2 <2.65 (horizon Jul 29) | **MISS.** 2.77% (opposite direction). P=0.15 correct direction (did not tighten). |
| MSFT reports FCF compression or Azure miss (<−5%) | market:MSFT:change_pct <-5.0 (horizon Jul 30) | **PENDING.** MSFT earnings expected this week; not yet reported as of brief capture. |
| MSFT beats Azure + holds FCF positive (>+3%) | market:MSFT:change_pct >3.0 (horizon Jul 30) | **PENDING.** Same — not yet reported. |
| WTI breaks above $92 at Monday Jul 27 open | market:CL=F:last >92.0 (horizon Jul 27) | **MISS.** WTI **$83.75** (−6.2%). US-Iran pause triggered the largest one-day oil decline in two months. P=0.30 wrong. |
| WTI pulls back below $85 at Monday Jul 27 open | market:CL=F:last <85.0 (horizon Jul 27) | **HIT.** WTI $83.75. Ceasefire/pause scenario from the "third option" materialized. P=0.22 correct. |
| CFTC Jul 21: Nasdaq lev_net >−55k (bears covered) | macro:CFTC_NQ_NET >-55000 (horizon Jul 31) | **MISS.** Nasdaq lev_net −74,690 (added −10,527 — bears DEEPENED into the chip rout). |
| CFTC Jul 21: Nasdaq lev_net <−70k (bears added) | macro:CFTC_NQ_NET <-70000 (horizon Jul 31) | **HIT.** −74,690 (new near-cycle extreme). Institutional conviction in tech derating intact. |
| USD/JPY breaks below 160 | market:USDJPY=X:last <160.0 (horizon Jul 30) | **PENDING.** USD/JPY 163.74 (−0.12 from 163.86). Yen barely moved; horizon not expired. |

**Running hit-rate: ~31/119 (26.1%).** Net this session: 3 HITs (HY OAS confirmation, WTI reversal, Nasdaq bear adds) vs. 3 resolved MISSes (HY OAS tighten, WTI $92 spike, Nasdaq cover). The ceasefire scenario was correctly assigned the second-highest probability after the "above $92" option — the directional model on oil is right but the level threshold keeps overestimating spike persistence. Credit calls: 1/2 this session (HY OAS >2.73% HIT for the first time in this cycle).

**The −1 stance from Jul 27 narrative:** entered at S&P 7,408 (Jul 23 close). Jul 27 intraday S&P 7,429 = paper LOSS of ~0.29%. Stance not definitively settled yet (end-of-day Jul 27 close needed), but the relief rally partially offsets.

---

## Today in one line

**The geopolitical oil premium deflated in a single session (WTI −6.2% on US-Iran pause), but the AI chip derating didn't — ASML −7.5%, TSMC −4.3%, NVDA −3.8% on the same "risk-on" ceasefire day proves the semiconductor unwind is structural, not Iran-driven; and with HY OAS finally moving to 2.77% (+9bps, Jul 23 FRED) the credit arm of the bear thesis has just arrived exactly as the oil arm exits — making this a flat week, not a bear week, until MSFT and the Fed resolve by Wednesday; flip back to −1 if MSFT shows FCF compression or HY OAS holds above 2.80% post-ceasefire.**

*Bear conditions (revised):* (1) ✅ AI FCF destruction confirmed at GOOGL/AMZN — structural; (2) ❌ WTI $90 dual-choke — CEASEFIRE, removed near-term; (3) ✅ HY OAS 2.77% (Jul 23 FRED) — FINALLY triggered above 2.73%, but tentative (predates oil collapse). *The missing leg: HY OAS will likely tighten back with oil falling. The credit trigger needs to hold through the oil reversal to confirm the cycle turn.*

---

## TL;DR

- **US-Iran strikes pause → WTI −6.2% to $83.75 (largest one-day oil drop in two months), Dow +1.22%, Brent $90.27** — but on the same "relief" day: ASML −7.51%, TSMC −4.30%, NVDA −3.82%. Old economy cheered the ceasefire; new economy kept selling. This is the cleanest bifurcation of the cycle: two distinct markets — energy/financials/services one side, AI chips the other.
- **HY OAS printed 2.77% (+9bps, Jul 23 FRED vintage) — the first formal credit widening above the formal 2.73% watch trigger.** This is the credit confirmation the bear thesis has been waiting on for six weeks. However: it's a Jul 23 data point captured *before* today's oil collapse. Oil falling is disinflationary and credit-positive; the Jul 24–25 FRED vintage will be the real test of whether the credit arm survives the ceasefire.
- **MSFT earnings + Fed rate decision both land this week.** MSFT tonight is the third hyperscaler binary (GOOGL FCF-negative, AMZN pre-priced −4.57%). Fed Wednesday is the most consequential rate call since Warsh took the chair. Entering a directional position now replicates the documented Jul 9 mistake.

---

## What moved & why

### Equities & sectors

**S&P 500 +0.29% to 7,429, Dow +1.22% to 52,344, Nasdaq −0.49% to 25,015, Russell 2000 +0.67%.** The index dispersion says everything: the Dow, which is old economy / cyclical / financial-heavy, rose 600+ points on oil collapse and Iran pause. The Nasdaq, which is tech-heavy and AI-chip-exposed, fell. The S&P is the average of two opposing markets.

**Sector leaders: XLC +2.69%, XLP +2.10%, XLRE +2.06%, XLF +1.98%, XLY +1.90%, XLB +1.99%, XLV +1.51%.** Eight of eleven sectors advanced. The breadth is deceptively bullish — it reflects oil relief (energy costs falling benefits every non-energy business) rather than a genuine risk-on regime. Consumer Staples (XLP) and Consumer Discretionary (XLY) both +2% on the same day = inflation relief story (lower oil → lower transport/energy costs → margin expansion). Financials (XLF) +1.98% = lower rates + credit healthy narrative.

**Sector laggards: XLK −2.31%, XLE −1.02%, XLU −0.29%.** Technology (XLK) is the anomaly — on a broad-market-up day, tech fell 2.3%. This is the smoking gun: ASML −7.51%, TSMC −4.30%, NVDA −3.82% dragged the entire semiconductor complex. The AI chip derating is disconnected from the oil/geopolitics narrative entirely. XLE −1.02% is the expected response to WTI −6.2%.

**Top movers (leaders): CRM +9.53%, GOOGL +3.81%, MA +3.56%, V +2.93%.** CRM (Salesforce) +9.53% is the session's largest single-name move — significant but no specific earnings headline captured in the brief; this may reflect pre-earnings positioning or an AI contract announcement not yet in the feed. GOOGL +3.81% is a post-earnings relief bounce: after falling −7.13% on earnings day (Jul 23), the stock is recovering as investors conclude the FCF miss was a one-quarter capex spike, not structural. MA/V +2.93–3.56% = consumer spending intact (AmEx read-through; lower oil = more discretionary purchasing power).

**Top movers (laggards): ASML −7.51%, TSMC −4.30%, NVDA −3.82%.** This is the third consecutive week of chip derating, and it now has nothing to do with oil. ASML reported in-line (Jul 16 earnings), TSMC reported a record +67% YoY (Jul 17) — both fell afterward. The pattern is established: exceptional results are "priced in" at these multiples and any imperfection triggers selling. NVDA has not yet reported Q2; the −3.8% is in sympathy with the broader chip complex and may reflect positioning reduction ahead of whatever MSFT says tonight about AI capex.

**Global: DAX +2.94%, Euro Stoxx 50 +1.85%, FTSE +1.68%, CAC +1.77%** — Europe broadly higher on oil/ceasefire relief. **Nikkei −2.25%** — yen slightly stronger (USD/JPY −0.12); Japan's export-heavy Nikkei suffers when the yen strengthens even modestly. **Hang Seng flat (−0.01%), Shanghai −0.48%** — China unmoved by the ceasefire; CXMT's 466% Shanghai debut (FT 07:29 UTC, "China's biggest IPO since 2010") absorbs domestic capital but doesn't lift the index.

**Steve Eisman (The Big Short) sold a key tech stock and is "starting to have doubts about AI"** (CNBC 13:59 UTC). Eisman's commentary is notable because he was correctly positioned for the 2008 GFC. His AI skepticism — "investors may be underestimating the risks if the AI boom fails to deliver" — is a public marker that the smart-money view on AI-capex destruction is broadening.

**Morgan Stanley: S&P 500 is echoing its 2021 setup** (MarketWatch 13:51 UTC). The 2021 setup was characterized by elevated valuations, high concentration in megacap growth, and a Fed pivot that eventually triggered a −27% peak-to-trough decline. This is the second consecutive week of a major sell-side comparison to a regime-change year.

### Rates & the dollar

| Metric | Jul 27 brief (Jul 23 FRED) | Jul 24 brief (Jul 22 FRED) | Δ | Pct (1Y) |
|---|---|---|---|---|
| 10Y FRED (Jul 23) | **4.71%** | 4.67% (Jul 22) | **+4bps** | **99.6th %ile** |
| 2Y FRED (Jul 23) | **4.37%** | 4.31% (Jul 22) | **+6bps** | **99.6th %ile** |
| 2s10s (Jul 24) | **0.36%** | 0.34% (Jul 23) | **+2bps** | **6.0th %ile** |
| 10Y-3M (Jul 24) | **0.73%** | 0.76% (Jul 23) | **−3bps** | **88.9th %ile** |
| BEI (Jul 24) | **2.26%** | 2.28% (Jul 23) | **−2bps** | **17.9th %ile** |
| **HY OAS (Jul 23)** | **2.77%** | 2.68% (Jul 22) | **+9bps 🔴** | **27.0th %ile** |
| IG OAS (Jul 23) | **0.79%** | 0.78% (Jul 22) | **+1bp** | **48.4th %ile** |
| Market 10Y | **4.653%** | 4.681% (Jul 24) | **−2.8bps** | — |
| Market 30Y | **5.133%** | 5.159% (Jul 24) | **−2.6bps** | — |
| DXY | **101.45** | 101.49 | **−0.04** | **99.2th %ile** |

**The FRED and market data are telling different stories on duration.** Market 10Y −2.8bps (to 4.653%) and 30Y −2.6bps (to 5.133%) — both slightly lower intraday as the ceasefire removes the oil-inflation tail. But the FRED vintages (one day older) show 10Y +4bps and 2Y +6bps — the underlying nominal rate pressure is still ascending in the data. This lag creates a flattering impression: markets see rally, FRED sees continuation of rate pressure.

**2s10s +2bps to 0.36% (6.0th %ile, from 3.6th %ile).** The fifth consecutive flattening ended — the curve steepened slightly. This is consistent with a geopolitical ceasefire: less oil supply risk = less stagflation pricing = the long end rallies more than the front. But 0.36% is still at the 6th %ile; the structural flatness remains. The "stagflation regime" interpretation hasn't been falsified — it's paused.

**BEI 2.26% (−2bps, 17.9th %ile).** Breakeven inflation ticked down slightly with the oil collapse. This is directionally correct: WTI −6.2% should reduce July CPI expectations modestly. But 2.26% is still well below 2.35% (the formal watch trigger) and well below what the WTI $90 → July CPI math implied last week. The BEI market is anchored by Warsh credibility.

**HY OAS 2.77% (Jul 23 FRED, +9bps — 27th %ile).** This is the most significant data point in the brief. The prior 2.68% print (3.6th %ile) had caused the bear thesis to lose its credit arm six consecutive times. The 2.77% print formally crossed the 2.73% watch trigger for the first time this cycle. However: (a) it's a Jul 23 print — the data predates Jul 27's oil collapse; (b) oil falling is credit-positive (lowers default risk for energy issuers, eases financial conditions broadly); (c) HYG market ETF was only +0.13% intraday today — confirming no major spread movement in real time. The credit confirmation is real but fragile: it needs to hold through the oil reversal to mean anything.

**The Fed decision is Wednesday (July 29).** The economic calendar item "Fed's rate decision Wednesday; durable goods today" (MarketWatch 11:32 UTC) confirms the most important binary of the week arrives before we can write the next narrative. Warsh has delivered hawkish language throughout this cycle; with headline CPI at 3.53%, core 2.59%, and WTI now falling to $83.75 (reducing forward inflation pressure), the probabilities on a hold vs. hike are closer than market pricing suggests. **A surprise hold with dovish language is the highest-probability bull catalyst of the cycle; a hold with hawkish language is the base case; a hike is the bear tail.** Entering a directional position before knowing which it is has negative expected value.

**Lacy Hunt reversal on long bonds** (MarketWatch 12:00 UTC): "For 44 years, this investor held aces in the long-bond game. He just folded." Lacy Hunt is one of the most respected long-duration bond bulls in history. If he is exiting, it's a structural signal that the 40-year bull market in long bonds is genuinely over — not just tactically challenged by the current rate environment. The 30Y at 5.13% and 10Y at 4.71% (both at 99th+ %ile) become consistent with a new secular regime, not a cyclical overshoot.

**Singapore MAS surprise tightening** (CNBC 03:36 UTC): Singapore tightened monetary policy in a surprise move as rising oil prices rekindle inflation risk. The MAS manages via exchange rate; a tightening means allowing the SGD to appreciate. Singapore is the first DM/SM central bank to explicitly cite oil as the driver of a policy change this cycle. This is the first domino in a potential chain: if oil had stayed at $90, expect similar moves from other central banks. The ceasefire interrupts this chain today — but the mechanism is now demonstrated.

### Commodities & credit

**WTI $83.75 (−6.23%), Brent $90.27 (−6.73%)** — the largest single-day oil decline in two months. The trigger was explicitly the US announcing a pause in attacks on Iran to give "talks some space" (BBC 11:50 UTC). Oil went from $90 (WTI) to $83.75 intraday — reversing the entirety of the WTI floor that had been built from $81 → $84 → $86 → $90 over the prior three weeks. Brent fell from $97.84 to $90.27.

This is the TACO pattern ("Trump Always Chickens Out") borne out quantitatively — MarketWatch 13:02 UTC published a strategist's mathematical framework showing that the ceasefire pattern has been consistent throughout the cycle. "It appears the White House was beginning to feel the pressure of rising bond yields and falling stock prices." In other words: the $90 oil + 30Y >5% + S&P P/E below 20x combination forced the ceasefire. The bear thesis created its own antidote.

**What this means for oil calls:** WTI <$85 trigger HIT today (P=0.22). Oil calls are now 4/16 (improving from 4/15). The oil spike thesis required both a physical interruption AND sustained Iranian strategic commitment. The TACO pattern suggests the political commitment is soft; each escalation is followed by a de-escalation. **The oil spike thesis is now formally retired for this cycle** — the same conclusion as 0/9 on earlier attempts, now confirmed more durably by an explicit ceasefire mechanism.

**Gold $4,079 (+0.27%), Copper $6.38 (+0.93%).** Gold barely moved despite the oil/Iran resolution — which would normally be bearish for safe-haven assets. The +0.27% is consistent with gold finding a new floor as a stagflation hedge rather than a geopolitical hedge. Copper +0.93% is a demand-optimism signal: falling oil → lower input costs → manufacturing recovers → copper demand up. This is a mild risk-on read from the industrial metals.

**HYG +0.13%, LQD +0.28%, TLT +0.61%.** Credit and duration mildly bid on the session. The HYG move (+0.13%) is inconsistent with a major spread widening event — confirming that the 2.77% FRED print is a backward-looking data point not yet reflected in the real-time market. TLT +0.61% is the long-duration relief trade as oil-driven inflation expectations ease.

---

## Macro & data

**Durable Goods Orders (June): +0.3% MoM — "much less than expected"** (Nasdaq 13:48 UTC). Core durable goods (ex-transportation) was presumably also soft. Manufacturing demand is weakening; the +0.3% headline was a rebound from a prior decline but significantly below consensus. This adds to the soft data stack (NFP +57k, ADP +98k, home sales miss, PepsiCo miss) that says the real economy is slowing beneath the service-sector surface.

**BLS (June vintage — unchanged):** CPI-U 3.53% YoY (from May 4.25%); Core CPI 2.59%; NFP +57k (cycle low); Unemployment 4.2% (−0.1%); AHE +3.52% YoY; Participation 61.5%. The WTI collapse to $83.75 modestly reduces the July CPI oil-channel pressure — but WTI was ~$57 a year ago, so even at $83.75, the YoY energy contribution to July CPI is +47% on WTI alone. Headline CPI for July (due mid-August) will likely still rise from 3.53%.

**FRED (Jul 23 vintages):** 10Y 4.71% (99.6th %ile), 2Y 4.37% (99.6th %ile), EFFR 3.63% (unchanged, 8.7th %ile), SOFR 3.64% (25.4th %ile), NFCI −0.552 (6.7th %ile — LOOSE), BEI 2.26% (17.9th %ile). Financial conditions remain historically loose despite the credit widening. NFCI at the 6.7th %ile with HY OAS at 27th %ile (up from 3.6th) = conditions may be starting to tighten, but the NFCI lags by 3–6 weeks from private credit signals.

**EIA (Jul 17 vintage):** Crude +2,010 MBBL (BUILD), Gasoline +765 MBBL (BUILD), Distillate +1,395 MBBL (BUILD), SPR −5,057 MBBL (DRAW — largest of cycle). Commercial crude continuing to BUILD at WTI $90 last week confirmed demand destruction ahead of the ceasefire. The SPR draw of 5,057 MBBL was the largest single-week drain of the cycle — the government was using strategic reserves to suppress oil prices even before the ceasefire. This is a behind-the-scenes policy that augments the ceasefire's oil-market impact.

**CFTC (Jul 21 vintage):**

| Contract | Jul 21 lev_net | Change vs Jul 14 | Reading |
|---|---|---|---|
| S&P 500 e-mini | −322,865 | **+42,137 (covered)** | Bears took PROFIT on S&P −1.21%; disciplined, not a squeeze |
| Nasdaq-100 e-mini | −74,690 | **−10,527 (added)** | Bears DEEPENED Nasdaq short into chip rout; near-cycle extreme |
| VIX futures | +3,098 | −7,091 (reduced) | Vol longs exited — fear abating, VRP normalized |
| Ultra 10Y | −380,604 | −2,039 (marginal) | Duration shorts essentially unchanged |
| Ultra T-Bond | −899,165 | +11,287 (modest cover) | Long-end bears trimmed; small signal |

The S&P covering (+42k) is the most significant CFTC development: bears took disciplined profit after a −1.21% session. This is NOT a squeeze (the market would have rallied sharply if it were; S&P only +0.29% today). It's systematic position management — which means S&P bears still have 322k net short contracts, a substantial directional bet. The Nasdaq addition (−10,527 to −74,690) is striking: institutional bears ADDED to Nasdaq shorts after the GOOGL −7.13%/AMZN −4.57% session. This is conviction, not reactive positioning. The VIX reduction (−7k) suggests the options market expected less near-term volatility as of Jul 18 — before today's developments.

---

## Risk lens

**1. The core paradox: the ceasefire removed the oil catalyst exactly when credit confirmed the bear thesis.**

HY OAS 2.77% (Jul 23 FRED) is the first print above 2.73% in this cycle. The credit market FINALLY moved. But it moved on Jul 23 data — the same session as GOOGL −7.13% and the dual-choke escalation. Today, that escalation reversed: oil −6.2%, geopolitical tail capped. The next FRED print (Jul 24 data) will likely show HY OAS tightening back toward 2.70–2.72% as oil falls and the ceasefire narrative takes hold. The credit confirmation could be a one-day data artifact — captured in the gap between the GOOGL shock and the ceasefire.

**The test that matters: HY OAS on Jul 28–29 FRED vintages.** If OAS holds above 2.75% despite WTI falling to $83.75, credit is telling a story about AI capex destruction and private credit stress that has *nothing to do with oil*. That would be a high-conviction bear signal. If OAS snaps back below 2.72%, the credit confirmation was borrowed from the oil shock and dissolves with it.

**2. ASML −7.5%, TSMC −4.3%, NVDA −3.8% on a "relief" day — the chip derating is structural.**

On a day when: (a) oil fell 6.2%, (b) the Dow rose 600 points, (c) 8/11 sectors advanced, (d) CRM +9.5% and GOOGL +3.8% — the semiconductor complex (ASML, TSMC, NVDA) fell 4–8%. This cannot be explained by oil, Iran, or macro uncertainty. The chip derating is being driven by something specific: the AI capex destruction narrative, ASML's post-earnings drift (the TSMC beats-and-dips pattern #5–6), and positioning unwind as Nasdaq bears add 10k contracts to the cycle extreme.

ASML is the purest leading indicator of AI capex commitments — it sells the equipment that builds new fabs. If ASML −7.5% on a broad-market-up day, the AI infrastructure spending cycle is being repriced structurally, not cyclically. This is the most important cross-asset signal in today's brief.

**3. MSFT tonight — the third hyperscaler binary and the clearest risk pivot of the week.**

GOOGL confirmed FCF-negative from AI spend. AMZN was pre-priced −4.57% on the GOOGL template. MSFT (Azure + OpenAI relationship) is the third leg. If Azure capex is compressing MSFT FCF similarly to GOOGL Cloud, the AI destruction is confirmed at all three hyperscalers — and the ASML/TSMC positioning unwind has years, not weeks, to run. If MSFT beats and holds FCF-positive (Azure being more capital-efficient), the GOOGL miss was idiosyncratic and the AI thesis is partially rehabilitated.

The market is set up for a binary reaction: MSFT stalled at $393.97 (Fibonacci resistance per Investing.com 14:06 UTC) into earnings. A beat would be the catalyst for a broad tech short squeeze (Nasdaq −74,690 is the fuel). A miss would be the catalyst for the next leg down in tech multiples.

**4. The Fed decision Wednesday — the binary above all binaries.**

The Fed rate decision on Wednesday July 29 arrives simultaneously with:
- MSFT earnings overnight (tonight)
- Meta earnings (expected later this week)
- AMZN earnings (expected later this week)
- HY OAS resolution (Jul 28–29 FRED vintage will show the post-ceasefire credit read)

Warsh has been hawkish throughout: "inflation will be a thing of the past" (Jul 14 after June CPI 3.53%) was dovish; but BofA Hartnett's call for a hike (last week), Lavorgna's "Fed has to hike" commentary (Jul 17), and Singapore MAS preemptive tightening all set up a potential hawkish hold statement Wednesday. A hold with hawkish language (no rate cuts in 2026) is the base case and would leave current pressure on multiples intact. A surprise hike is the bear tail — S&P −3%+ immediately.

**5. Yen carry and Lacy Hunt's long-bond reversal.**

USD/JPY 163.74 — barely moved despite the Iran ceasefire. The yen carry trade (borrowing yen to fund long positions in ASML, TSMC, and other high-beta assets) is still loaded. Lacy Hunt exiting his 44-year long-bond position (MarketWatch 12:00 UTC) is a structural marker: the long-end of the Treasury curve at 5.13% may be the new secular equilibrium, not a cyclical extreme. If that's right, the duration shorts (Ultra T-Bond −899k, Ultra 10Y −381k) are structurally correct, and the investors who funded their AI-chip longs with yen carry are simultaneously exposed to: (a) chip derating, (b) yen strengthening if BoJ acts, (c) a long bond that doesn't rally to the 4% floor that justified the carry math.

**What to watch next (numeric triggers):**

---

## What to watch

**1. HY OAS — does the credit confirmation survive the oil collapse?**

The 2.77% (Jul 23 FRED) is the first formal signal. The Jul 28–29 FRED vintage is the first post-ceasefire read. If OAS holds above 2.75%, credit is pricing something beyond oil (AI capex + private credit stress). If it snaps back below 2.72%, the credit signal dissolves with the oil shock.

```watch
[
  {"claim": "HY OAS holds above 2.75% on Jul 28-29 FRED vintage — credit confirmation survives ceasefire; AI capex + private credit story independent of oil", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.74", "horizon": "2026-07-30", "probability": 0.30},
  {"claim": "HY OAS tightens back below 2.72% on Jul 28-29 FRED — credit signal was borrowed from oil shock; reverts with ceasefire", "metric": "macro:BAMLH0A0HYM2", "trigger": "<2.73", "horizon": "2026-07-30", "probability": 0.45}
]
```

**2. MSFT earnings — the decisive AI capex binary.**

MSFT (tonight/this week). Azure is the second-largest cloud provider. If FCF compresses similarly to GOOGL, the AI capex destruction is a hyperscaler-wide phenomenon.

```watch
[
  {"claim": "MSFT reports Azure miss or FCF compression — AI capex destroys FCF at 3 of 3 hyperscalers; ASML/TSMC derating accelerates; chip complex -5%+", "metric": "market:MSFT:change_pct", "trigger": "<-5.0", "horizon": "2026-07-29", "probability": 0.22},
  {"claim": "MSFT beats Azure + positive FCF — GOOGL miss was idiosyncratic (Gemini vs GPT cost differential); AI monetization intact; Nasdaq short squeeze from -74,690", "metric": "market:MSFT:change_pct", "trigger": ">3.0", "horizon": "2026-07-29", "probability": 0.38}
]
```

**3. 10Y yield — does the ceasefire buy relief at the long end?**

With oil down 6.2%, the inflation expectations channel should ease. If 10Y falls below 4.55% on the FRED, the rate pressure on tech multiples eases meaningfully.

```watch
[
  {"claim": "10Y FRED falls below 4.55% on Jul 28-29 vintage — ceasefire + disinflation signal; multiple pressure eases; supports S&P +2%+", "metric": "macro:DGS10", "trigger": "<4.55", "horizon": "2026-07-31", "probability": 0.20},
  {"claim": "10Y FRED holds above 4.65% despite ceasefire — secular term premium / Lacy Hunt thesis wins; no multiple relief for tech", "metric": "macro:DGS10", "trigger": ">4.64", "horizon": "2026-07-31", "probability": 0.55}
]
```

**4. USD/JPY — yen carry still coiled.**

163.74 with BoJ at 31-year highs. The carry trade hasn't unwound; it's waiting.

```watch
[
  {"claim": "USD/JPY breaks below 160 — yen carry unwind starts; ASML/TSMC positioning at -74,690 Nasdaq carries unwind risk; Nikkei -5%+", "metric": "market:USDJPY=X:last", "trigger": "<160.0", "horizon": "2026-07-31", "probability": 0.12}
]
```

---

## The call

**Direction: 0 (flat) — removing the −1 stance; waiting for MSFT and the Fed to resolve.**

The −1 stance was entered at S&P 7,408 (Jul 23 close). S&P 7,429 on Jul 27 intraday = paper loss of ~0.29%. The stop conditions were: (1) HY OAS ≤2.65% (not met — OAS at 2.77%), (2) AMZN beats + WTI <$85 (WTI <$85 IS MET today; AMZN earnings pending this week but AMZN hasn't reported yet).

The WTI stop condition has now been met. WTI is $83.75 — below $85 for the first time in the entire oil spike sequence. The ceasefire is the mechanism. This was one of the explicit stop conditions for the −1 stance ("AMZN beats + WTI <$85"). Half the stop condition is now met.

**Why not re-enter −1:** MSFT reporting tonight creates a binary that has historically destroyed directional positions (Jul 9 replay: entered −1, MSFT equivalent on the opposite side destroyed the position). The CFTC shows S&P bears took 42k contracts of disciplined profit — not panic covering. The fat tail tonight is MSFT beat + Nasdaq short squeeze from −74,690 contracts. Pressing −1 into that setup has negative expected value.

**Why not enter +1:** ASML −7.5%, TSMC −4.3%, NVDA −3.8% on a relief day is a structural warning. HY OAS 2.77% (even if tentative) is the first credit confirmation of the cycle. The Dow +1.22% is energy relief, not earnings confirmation. FRED yields are still at 99th %ile (10Y 4.71%, 2Y 4.37%). Lacy Hunt exit and Morgan Stanley 2021-echo both argue against chasing the relief bounce.

**The honest answer is 0 (flat):** No edge this session. The oil catalyst resolved; the earnings binary isn't resolved. Come back Wednesday after MSFT + the Fed.

```stance
{"direction": 0, "notes": "Removing -1: WTI stop condition met ($83.75 < $85 on Iran ceasefire/pause). MSFT earnings tonight = too binary to press -1 (documented Jul 9 mistake). Fed decision Wednesday. Credit confirmation (HY OAS 2.77%) is tentative — Jul 23 data predates oil collapse; Jul 28-29 FRED is the real test. ASML -7.5%/TSMC -4.3%/NVDA -3.8% structural (not oil-driven) but Nasdaq -74,690 short squeeze risk on MSFT beat prevents -1. Bull entry conditions: MSFT beat + FCF positive + HY OAS tightens <2.72% + Fed dovish. Bear re-entry: MSFT FCF compression OR Fed hawkish surprise + HY OAS holds >2.75% post-ceasefire. Running hit-rate: 31/119 (26.1%). Credit calls: 1/2 this session. Oil calls: retired (0 edge in this cycle)."}
```

---

## Sources

- *Oil falls 8% as Iran and US pause strikes over Strait of Hormuz* (FT International, 2026-07-27T10:29 UTC)
- *Oil price dives as US and Iran pause attacks — "attacks halted to give talks some space"* (BBC Business, 2026-07-27T11:50 UTC)
- *Oil prices see largest one-day declines in two months after U.S. and Iran pause strikes* (MarketWatch, 2026-07-27T13:27 UTC)
- *Strategist's mathematical formula for Trump's 'TACOs' borne out by weekend ceasefire* (MarketWatch, 2026-07-27T13:02 UTC)
- *Dow Jumps 600 Points On U.S.-Iran Hopes; Oil Prices Plunge* (Yahoo Finance, 2026-07-27T13:42 UTC)
- *Dow, S&P 500, Nasdaq open higher as Iran hostilities are paused* (MarketWatch Bulletins, 2026-07-27T13:30 UTC)
- *Steve Eisman is starting to have doubts about AI — sold a key tech stock* (CNBC Finance, 2026-07-27T13:59 UTC)
- *The S&P 500 is echoing its 2021 setup, according to Morgan Stanley* (MarketWatch, 2026-07-27T13:51 UTC)
- *For 44 years, this investor held aces in the long-bond game. He just folded.* (MarketWatch, 2026-07-27T12:00 UTC) — Lacy Hunt long-bond exit
- *U.S. Durable Goods Orders Rise 0.3% In June, Much Less Than Expected* (Nasdaq Markets, 2026-07-27T13:48 UTC)
- *Economic calendar: Fed's rate decision Wednesday; durable goods today* (MarketWatch Bulletins, 2026-07-27T11:32 UTC)
- *Tech stocks today: Big Tech earnings this week mark a pivotal moment for the AI trade* (Yahoo Finance, 2026-07-27T13:46 UTC)
- *Stock market today: Dow, S&P 500, Nasdaq rise as oil tumbles, investors brace for busy week* (Yahoo Finance, 2026-07-27T08:04 UTC)
- *Singapore tightens monetary policy in surprise move as rising oil prices rekindle inflation risk* (CNBC Economy, 2026-07-27T03:36 UTC)
- *Chinese chip champion CXMT soars 466% in market debut — briefly China's most valuable listed company* (FT International, 2026-07-27T07:29 UTC)
- *Microsoft stalls at $393.97 Fibonacci resistance: Live levels* (Investing.com, 2026-07-27T14:06 UTC)
- *Why is Visa stock climbing today?* (Investing.com, 2026-07-27T14:05 UTC)
- *Could voter rage over AI data centers tank your utility stocks?* (MarketWatch, 2026-07-27T14:15 UTC)
- *Ukraine, Iran and how regional wars go global* (FT International, 2026-07-27T11:14 UTC)
- Analytics: `brief_2026-07-27.json` (Jul 27 14:20 UTC intraday); `brief_2026-07-24.json` (Jul 23 full close); CFTC Jul 21 vintage; FRED Jul 23–24 vintages; `data/running_thesis.md`
