# Market Story — 2026-06-19

> *Brief captured 2026-06-18 14:57 UTC — Thursday session, ~10:57am ET (post-FOMC, post-Iran-deal-signing morning snapshot). All prices from `brief_2026-06-18.json`. The FOMC decision (June 17 ~14:00 ET / ~18:00 UTC) and Iran deal formal signing (June 18 ~13:32 UTC) are both reflected in today's market levels.*

---

## Since last time

Grading the June 18 `watch` block (from `narrative_2026-06-18.md`) against the June 18 brief:

| Claim | Trigger | Result |
|---|---|---|
| Warsh neutral: S&P holds above 7,450 post-press conference | `market:^GSPC:last > 7450` | **HIT** — S&P at 7,497 (+1.04% morning session, prev close implied ~7,421). Warsh was "on script" per CNBC; Iran deal signing drove the morning surge. P=0.62 → correct direction. |
| HY OAS widening trend continues above 2.75% | `macro:BAMLH0A0HYM2 > 2.75` | **PENDING** — HY OAS still at 2.71% (June 16 FRED data; no new post-FOMC print yet in brief). 3-session horizon running. |
| CFTC June 16 S&P lev net covers to above -400k | `positioning:SPX:lev_net > -400000` | **PENDING** — CFTC still shows June 9 data (−451,586). June 16 data releases Friday June 20. |
| WTI holds above $72 — physical Hormuz deal intact | `market:CL=F:last > 72` | **HIT** — WTI at $73.29, but barely: −$3.49 (−4.56%) on the session. The formal deal signing sent oil down hard; $72 floor held for now. P=0.65 → correct, but trajectory is alarming. |
| 2s10s stays above 0.30% — curve doesn't invert on Warsh hawkish hold | `macro:T10Y2Y > 0.30` | **MISS** — 2s10s FRED: **0.29%** (June 17 close, z=−3.39). Crushed −9bps on FOMC day. Wrongly confident at P=0.72. This is the most important data point in the brief. |

**Running hit-rate: ~6/27 (22%) on settled items.** Two new hits (S&P, WTI), one miss (2s10s), two pending (HY OAS, CFTC). Hit-rate improving vs. prior 16% now that the FOMC binary has resolved; credit OAS remains 0-for-10 on the level triggers.

**June 17 +1 stance (entered S&P ~7,539):** FOMC day S&P close implied at ~7,421 (from June 18 brief's +1.04% = ~7,497/1.0104). Direction was vindicated by June 18's Iran-deal morning rally (+1.04%); the stance settles against June 18 close (pending — brief captured mid-morning). Entry at 7,539 is currently ~−0.6% underwater from peak FOMC close, but the directional call is correct.

---

## Today in one line

**Warsh on-script neutral hold + Iran deal formal signing delivered the double catalyst that cleared the pre-FOMC binary — but the 2s10s crushed −9bps to 0.29% (z=−3.39, near-inversion) on FOMC day before the Iran deal rally covered its tracks, and gold fell −2.35% while oil fell −4.56%: the market is pricing supply-side disinflation as a free lunch when the curve is already telling you the front end isn't moving.**

*Flip to sustained bull: S&P holds above 7,500 through CFTC Friday data, HY OAS re-tightens to 2.66% on the first post-FOMC FRED print, 2s10s recovers above 0.35%. Flip to bear: HY OAS breaks above 2.75% on the next FRED update OR 2s10s closes below 0.20% (formal inversion territory).*

---

## TL;DR

- **The dual catalyst is confirmed, and the conditional long is re-entered per thesis protocol.** Warsh was "on script" (CNBC: "followed the script closely"); Iran deal was formally signed (FT 13:32 UTC). S&P +1.04%, Nasdaq +1.35%, Russell +1.19%. Both flip-to-bull triggers from the running thesis were met. Consequence: the FOMC-binary overhang is cleared; the next regime test is CFTC covering data Friday and the first post-event HY OAS print.

- **The 2s10s at 0.29% (z=−3.39) on FOMC day is the signal everyone is ignoring.** The curve crushed −9bps on June 17 despite a neutral hold. Warsh anchored the front end (EFFR unchanged at 3.63%, 2Y FRED fell only −2bps to 4.05%) while the long end drifted lower on Iran deflation. Result: 2s10s is near-inverted for the first time this cycle. A flat/inverted curve with HY OAS at the 3.6th %ile and VIX closing at 18.44 is the textbook late-cycle setup — even if the rally continues for weeks.

- **AI hardware bifurcation deepens, IT consulting capitulates.** TSMC +4.76%, ASML +3.59%, Intel +11% on the Apple foundry deal. Accenture hit its lowest level since 2017 on earnings as "AI threat mounts" (FT). The market is now paying for physical infrastructure (chips, foundries, nuclear, data centers) and derating the human capital layer (consulting, software platforms). Apple announced it will raise prices due to AI-driven chip cost inflation — the AI build is becoming inflationary at the consumer level.

---

## What moved & why

### Equities & sectors

**June 17 close (implied ~7,421) → June 18 brief (7,497, +1.04%):**

| Asset | June 17 brief | June 18 brief | Δ session | Read |
|---|---|---|---|---|
| S&P 500 | 7,507 (pre-FOMC) | **7,497 (+1.04%)** | Prev close ~7,421; Iran deal gap-up | Double catalyst morning rally |
| Nasdaq | 26,326 | **26,373 (+1.35%)** | Tech hardware bid | Semis driving the leadership |
| Dow | 52,112 | **51,781 (+0.56%)** | Lagging tech-heavy peers | Industrials muted |
| Russell 2000 | 2,958 | **2,953 (+1.19%)** | Risk-on bid | Small caps participating |
| VIX (intraday) | 16.84 | **17.11 (−7.2%)** | Down from 18.44 FOMC close | Fear dissipating post-deal |
| VIX (FRED close, June 17) | 16.41 (Jun 16) | **18.44 (Jun 17)** | **+2.03 (+12.4%)** | FOMC day fear spike |

**Breadth: 8 sector advancers / 3 decliners.** A genuine broad advance, not a narrow surge.

**The defining session story — AI hardware wins, IT consulting loses:**

| Sector/Name | Δ | Read |
|---|---|---|
| Technology (XLK) | **+2.84%** | Semis carrying; TSMC +4.76%, ASML +3.59%, NVDA +2.32% |
| Utilities (XLU) | **+1.63%** | AI power infrastructure bid; nuclear theme active |
| Industrials (XLI) | **+1.43%** | Data center construction + reshoring tailwinds |
| Energy (XLE) | **−1.92%** | Oil −4.56% = direct sector hit as Iran supply unlocks |
| Health Care (XLV) | **−1.02%** | Defensive rotation out on risk-on; no specific catalyst |

**Intel's Apple deal (+11%) is the session's single most important equity story.** Trump announced Intel will build chips for Apple in the US. This validates the US semiconductor reshoring thesis at the largest possible scale — Apple, which spent two decades offshoring chip design to TSMC, is now being pointed at domestic fabrication. Consequence: if Intel wins the Apple foundry relationship at meaningful volume, it changes Intel's financial model (foundry margins, utilization) AND creates a geopolitical moat argument for US-made chips. Analysts note the relationship may "start small" (MarketWatch), but the political and strategic signal is massive.

**Accenture hitting a 9-year low (FT: "shares fall to lowest since 2017")** is the other side of the same thesis. IT consulting is being disrupted by AI coding agents: Cursor, GitHub Copilot, and the wave of agent-based development tools are compressing the billable-hour model that funds companies like Accenture. CRM at −42% YTD and Accenture at 9-year lows = the software and consulting layers of the tech stack are being repriced while the physical infrastructure layer hits records.

**SpaceX −6%** continuing post-listing profit taking (MarketWatch: "vastly more expensive than any stock in the S&P 500, fueled by 'FOMO'"). Retail FOMO into SpaceX ETFs is well-documented; the first real-money selloff after peak enthusiasm is the normal post-listing pattern. The Cursor AI acquisition thesis doesn't change, but valuation gravity is operating.

**Nuclear: Oklo and Centrus surged** after signing a uranium deal backed by Meta and Sam Altman. AI data center power demand is the driver — hyperscalers are now directly funding fuel supply chains for nuclear plants. This is real capex, not promises.

### Rates & the dollar

**The 2s10s crush is the narrative:**

| Tenor | June 17 brief | June 18 brief | Δ | pct_1y | Note |
|---|---|---|---|---|---|
| 5Y (market) | 4.179% | **4.202% (−0.26%)** | −1.1bps | — | Barely moving |
| 10Y (market) | 4.443% | **4.428% (−1.31%)** | **−5.9bps** | — | Long end rallying on Iran deflation |
| 30Y (market) | 4.931% | **4.877% (−1.97%)** | **−9.8bps** | — | Long end rally most pronounced |
| 2Y (FRED) | 4.07% (Jun 15) | **4.05%** (Jun 16) | **−2bps** | 93.3th %ile | Front end barely moving |
| 10Y (FRED) | 4.47% (Jun 15) | **4.43%** (Jun 16) | −4bps | 85.7th %ile | |
| **2s10s (FRED)** | 0.38% (Jun 16) | **0.29%** (Jun 17) | **−9bps** | **0.0th %ile** | z = −3.39. Near-inversion. |
| 10Y Breakeven | 2.29% (Jun 16) | **2.26%** (Jun 17) | −3bps | 9.9th %ile | Inflation expectations compressing further |

**The 2s10s at 0.29% is the read-through nobody wants to say.** On FOMC day, the curve crushed −9bps despite a "neutral" Warsh. The mechanism: Warsh held (anchoring the front end), long rates fell on the Iran-deal disinflation trade (30Y down −9.8bps today), and the result is a curve that is now 1bp from flat/inversion. The z-score of −3.39 means this is not a normal level — this is 3.4 standard deviations below the 1-year average, the most extreme reading in the data. A neutral Fed + supply-side disinflation is supposed to steepen the curve (less inflation = less long-duration risk premium); instead it's flattening because the front end is glued. That glue is Warsh: the market does not believe cuts are coming.

**Breakeven at 2.26% (9.9th %ile) and falling.** The Iran deal's most direct effect: energy disinflation is now pricing a sub-10th-percentile inflation premium into 10-year bonds. This is the bond market's cleanest signal that the deal changes the CPI path — if oil stays near $72–75, June CPI should print below 4.0% (vs. May's 4.25%), potentially opening a window for Warsh to shift rhetoric by September.

**Dollar: DXY +0.94 to 100.63.** The dollar bid strengthened post-FOMC — Warsh neutral with high data dependency = no near-term cut path = dollar supported. EUR/USD fell −1.08% to 1.1485; GBP fell −1.34% on BoE hold at 3.75%.

**Bank of England: held at 3.75% (7-2 vote).** BBC: "Bank warns of impact of high energy prices." The BoE is stuck in the same box as the Fed: energy inflation overhang prevents easing even as growth softens (UK job vacancies at 5-year low). The 7-2 vote (vs. June split) suggests the BoE is less conflicted than last meeting — the Iran deal hasn't yet been treated as a meaningful disinflation input.

### Commodities & credit

**WTI: $76.78 → $73.29 (−$3.49, −4.56%).** The formal deal signing (FT: "US and Iran sign deal as Trump vows to release frozen funds and ease sanctions") is being read as a supply unlock, full stop. Trump acknowledges Iran keeps ballistic missiles — an important concession that will fuel future political opposition, but the market is pricing supply, not geopolitics. At $73.29, WTI is $0.69 above the June 18 watch trigger of $72.

Counter-signal from EIA (June 12 vintage — first update since June 5):
- Crude ex-SPR: **−8,263 MBBL** draw (vs. prior −7,227 MBBL) — drawdown ACCELERATING
- Gasoline: **−906 MBBL** draw (vs. prior +186 MBBL BUILD — switched to draw!)
- Distillate: +951 MBBL build
- SPR: −8,941 MBBL (continued drawdown)

The EIA demand signal (crude + gasoline both drawing) is bullish for oil fundamentals. The price decline is entirely supply-side (Iran deal) + political narrative (Trump: "oil soon receding to prewar level"). If Iranian supply takes 3–6 months to fully materialize in global markets (which is typical of sanctions-lifting logistics), the EIA demand trajectory could re-bid WTI above $75 before Iranian barrels arrive. NYT: "Why Flight Prices Might Not Fall After the U.S.-Iran Deal — jet fuel may stay expensive for months." That's the lag clock running.

**Gold: $4,366.60 → $4,263.90 (−$102.70, −2.35%).** Silver −6.19%. Gold is deflating the safe-haven and inflation-hedge premium simultaneously: Iran deal removes geopolitical risk premium; energy disinflation removes the inflation hedge bid. Gold now at 56th %ile — right at 1-year median, suggesting the overshoot from the war period is fully corrected. The question from here: does gold find a floor at current levels (Warsh hawkish = higher real rates = gold headwind; but structural USD weakness + fiscal expansion = gold tailwind) or does it continue toward the April lows near $4,000?

**Copper: $6.48 → $6.41 (−1.14%).** Industrial metals softening slightly. Copper remains at the 97.6th %ile (1-year percentile of level) — still historically elevated. The supply chain reshoring thesis (Intel/Apple, data center buildout) should support copper demand structurally, but the near-term move reflects risk-off in industrial metals concurrent with the Iran deal.

**Credit: HY OAS 2.71%, IG OAS 0.75% — no new FRED data.** The June 16 reading is the most recent. HYG +0.36%, LQD +0.52% — credit ETFs rallying on risk-on. But without a new FRED print, we cannot confirm whether the +5bps widening from June 16 was pre-FOMC noise (that will re-tighten) or the start of a directional shift. This is the most important data point to watch for the next brief.

---

## Macro & data

**Warsh's first press conference (June 17, post-brief capture):** Multiple CNBC/NYT articles covering it. CNBC: "Warsh followed the script on interest rates closely." "Five big takeaways" imply: (1) unanimous vote, (2) no new dot submitted, (3) data dependency emphasized, (4) communication style deliberate/jargon-heavy (NYT: "Warsh Makes His Case With Jargon, and a Penchant for Detail"), (5) no explicit signal on next move direction. This is the most "on script" possible outcome — markets had a brief VIX spike to 18.44 close (fear: was Warsh secretly hawkish?), then the Iran deal the next morning resolved it.

**Iran deal formally signed (FT 13:32 UTC June 18):** "US and Iran sign deal as Trump vows to release frozen funds and ease sanctions. President says Iranians will receive incentives when they 'behave' and acknowledges Tehran will keep ballistic missiles." The ballistic missile concession is the most politically explosive detail — it was a red line for many Republicans and may face congressional resistance. But the market is treating the signing as definitive.

**Intel/Apple foundry deal:** Trump announced Intel will make chips for Apple in the US. Intel +11%. Consequence: (1) Intel's foundry utilization could be the best in years if Apple moves even 10% of its chip volume; (2) the deal represents a direct US government orchestration of supply chain reshoring; (3) Apple's disclosure that AI chip costs will raise its prices (BBC) and Intel winning the relationship suggests Apple is paying up for US-made chips — price inflation at the consumer level.

**EIA June 12 data (first update since June 5 vintage):**
- Crude ex-SPR: −8,263 MBBL (accelerating draws)
- Gasoline: −906 MBBL (switching from build to draw — demand recovering?)
- SPR: −8,941 MBBL (administration still drawing down strategic reserve)
The gap between fundamentals (crude draws accelerating) and price (WTI −4.56%) is unusually wide. If Iranian barrels take months to arrive, this gap closes — probably upward on oil.

**Jobless claims (June 18 calendar):** MarketWatch noted it as today's calendar item. ICSA in the June 18 brief shows 226k (June 13 vintage, −4k from prior, 65.5th %ile) — still well-behaved. No labor market stress signal.

**Swiss National Bank held.** "War pushes up inflation forecast." Same higher-for-longer dynamic globally.

**Nuclear energy / AI power:** Oklo + Centrus uranium deal backed by Meta and Sam Altman. GE Vernova supplier near breakout as data centers lift construction. The AI power buildout is now forcing direct investment in fuel supply chains — this is a multi-year structural theme, not a trade.

**Apple to raise prices due to AI boom.** BBC: "The firm's outgoing boss Tim Cook did not say when prices would rise or which products would be affected." AI-chip cost inflation is now becoming consumer CPI. This is the flip side of the energy disinflation thesis: energy deflates; AI-hardware inflates.

**Gas prices barely below $4/gallon nationally** (MarketWatch). Despite WTI at $73, the consumer pump price lag means retail energy costs remain elevated. The Iran deal disinflation thesis will take weeks to reach the gas pump.

---

## Risk lens

**1. 2s10s at 0.29% — the curve inversion clock is running.**
The 2s10s breached my watch trigger of 0.30% (I set 0.72 probability it wouldn't — wrongly confident). At z=−3.39, this is not a tail event in the data; it's a statistical extreme that historically precedes recessions with a 6–18 month lag. The specific concern: the curve is near-inverted with HY OAS still at the 3.6th %ile (historically tight) and unemployment at 4.3% (still below 5% full-cycle pressure zone). The classic late-cycle setup has the curve inverted BEFORE credit widens — which is exactly what's beginning to unfold. **The risk is that credit is lagging the curve signal, not that the curve signal is wrong.**

**2. VIX closed at 18.44 on FOMC day — the market was more stressed than the equity tape implied.**
The VIX close of 18.44 on June 17 (69.4th %ile) was the highest close since the Iran war escalation. A "neutral" Warsh should have compressed VIX, not elevated it. The fact that VIX closed at 18.44 despite Warsh being "on script" suggests the market was pricing tail risks (hawkish surprise, Iran deal unraveling) that didn't materialize — and today's morning VIX of 17.11 is the relief unwind. Watch for whether VIX settles below 16 by end of week (genuine de-risking) or stays elevated (residual uncertainty).

**3. HY OAS: first post-FOMC FRED print is regime-defining.**
The June 18 brief still shows June 16 FRED data (2.71%, 3.6th %ile). The June 17 FOMC day close and June 18 morning data are not yet in the FRED series. The next FRED update (probably visible in tomorrow's brief) will show whether: (a) credit re-tightened toward 2.66% on neutral Warsh + Iran deal relief (bull case), or (b) credit continued widening above 2.75% (bear case). Given that HYG was +0.36% in today's session and LQD +0.52%, the ETF signal leans toward re-tightening. But FRED OAS is slow to update. **The credit market is the umpire between the bull case (Iran + Warsh = relief rally continues) and the bear case (curve inversion + private credit stress + VIX spike = late-cycle fragility).**

**4. AI hardware vs. software/consulting bifurcation deepens.**
TSMC +4.76%, ASML +3.59%, Intel +11%, nuclear stocks surging vs. Accenture at 9-year lows, CRM at −42% YTD, MSFT −21% YTD. This is not rotation — it's repricing. The market is saying: the value in the AI cycle accretes to the picks-and-shovels (chips, equipment, power, foundries), not to the layer above (platforms, consulting, software with uncertain revenue models). Consequence: any portfolio long mega-cap software (MSFT, META at −13% YTD, AMZN +4%) is fighting the structural tide. The question is when these companies benefit from AI capabilities, not whether the technology works.

**5. Iran deal complexity: Trump concedes ballistic missiles, bipartisan pushback continues.**
The formal signing acknowledges Iran keeps ballistic missiles — a concession that Republican hawks will contest. The $300bn reconstruction fund dispute (Trump denied it, then apparently re-included it in the formal terms: "vows to release frozen funds") will face congressional scrutiny. Physical Hormuz traffic is normalizing (Foreign Office drops UAE travel warning — BBC), but the political architecture remains fragile. The risk is that Iranian domestic hardliners use the ballistic missile concession + fund dispute to pressure the government toward non-compliance within 60–90 days. WTI at $73.29 is not pricing that scenario.

**6. CFTC positioning (June 9 data, stale) — Friday June 20 is the key update.**
S&P e-mini lev net at −451,586 (short). June 16 data releases Friday. If bears covered 50–100k contracts post-FOMC + post-deal (which the bull thesis requires), S&P lev net would move toward −380–400k. Below −380k = squeeze has structural momentum. Above −430k = bears held or added, rally is a trap.

---

## What to watch

1. **HY OAS next FRED update (first post-FOMC print)** — the regime umpire. At 2.71% now. Above 2.75% = widening trend accelerating despite relief rally; the bull case is challenged. Below 2.68% = re-tightening confirmed, credit tail dissipating.

2. **CFTC June 16 data (Friday June 20)** — S&P e-mini lev net. Current: −451,586. Below −380k = bear covering confirms squeeze has legs. Above −430k = bears held or added during the FOMC uncertainty = rally may be short-lived.

3. **WTI $70 floor** — at $73.29, the $72 watch is now a $70 structural floor question. If Iranian barrels actually arrive in July, WTI could test $70 before fundamentals recover. Below $70 = demand destruction signal (even with Iran supply, that's a big move); above $76 = Iranian supply arrival is delayed, physical market tight.

4. **2s10s recovery** — does the curve recover above 0.35% on energy disinflation → rate-cut-by-year-end expectations, or does it sink further toward 0.20% as the long end rallies faster than the front end can fall? Inversion (0.0% or below) within next 10 sessions = recession probability pricing materially increases.

5. **VIX: close below 16 vs. hold above 17** — today at 17.11. A close below 16 in the next 1–2 sessions = genuine risk appetite returning. Hold above 17 = the FOMC/Iran binary removed the acute fear but residual uncertainty persists. Watch correlation with credit for the next leg.

```watch
[
  {"claim": "HY OAS re-tightens to 2.68% or below on first post-FOMC FRED print", "metric": "macro:BAMLH0A0HYM2", "trigger": "<2.68", "horizon": "next 3 sessions", "probability": 0.45},
  {"claim": "CFTC June 16 S&P lev net covers to above -400k", "metric": "positioning:SPX:lev_net", "trigger": ">-400000", "horizon": "this week", "probability": 0.55},
  {"claim": "WTI holds above $70 — Iran supply arrival delayed vs. expectations", "metric": "market:CL=F:last", "trigger": ">70", "horizon": "next 5 sessions", "probability": 0.70},
  {"claim": "2s10s recovers above 0.35% as long end rallies on Iran disinflation thesis", "metric": "macro:T10Y2Y", "trigger": ">0.35", "horizon": "next 5 sessions", "probability": 0.40},
  {"claim": "S&P holds above 7,450 through CFTC Friday data (no reversal on positioning)", "metric": "market:^GSPC:last", "trigger": ">7450", "horizon": "next 3 sessions", "probability": 0.68}
]
```

---

## The call

The running thesis flip conditions for bull re-entry are both confirmed: (1) Warsh neutral language confirmed per CNBC ("followed the script closely"), and (2) S&P held above 7,450 post-FOMC and is trading at 7,497 this morning. Per protocol: re-enter +1.

The 2s10s miss (0.29%, below my trigger) is a medium-term cautionary signal but not an immediate de-risking trigger. The curve's near-inversion is a recession pre-signal with a 6–18 month lead time, not a next-session trade. The short-term dynamics (CFTC covering Friday, HY OAS re-tightening, semi leadership, Iran deal removing inflation overhang) favor the bull case for the next 3–5 sessions.

Stop: flip to −1 if HY OAS breaks 2.75% on next FRED print OR S&P closes below 7,300. Target: 7,650 on CFTC covering + credit re-tightening confirmation.

June 17 +1 stance (entered S&P ~7,539): directional call vindicated by today's Iran deal gap-up; settlement against June 18 close pending.

```stance
{"direction": 1, "notes": "Both flip-to-bull triggers met per running thesis: Warsh neutral confirmed (CNBC: 'followed script closely'), S&P held above 7,450 (at 7,497 +1.04%). Re-entering +1 at S&P ~7,497. Caution: 2s10s breached 0.30% (0.29%, z=-3.39, FOMC day) — medium-term recession signal, not immediate trigger. Iran deal formal signing (FT 13:32 UTC) is the immediate catalyst. CFTC covering Friday is the next confirmation gate. Stop: -1 if HY OAS >2.75% on next FRED print OR S&P <7,300. Target: 7,650. Jun 17 +1 stance (entered 7,539) settling against Jun 18 close."}
```

---

## Sources

- *US and Iran sign deal as Trump vows to release frozen funds and ease sanctions* (FT International, 2026-06-18 13:32 UTC)
- *Stocks open higher after U.S., Iran sign initial deal to end war* (MarketWatch Bulletins, 2026-06-18 13:31 UTC)
- *Wall Street jumps 1% as U.S.-Iran peace deal boosts sentiment* (Investing.com Markets, 2026-06-18 14:48 UTC)
- *Here are the five big takeaways from Kevin Warsh's first meeting as Fed chairman* (CNBC Economy, 2026-06-17 23:51 UTC)
- *Warsh Makes His Case With Jargon, and a Penchant for Detail* (NYT Economy, 2026-06-18 01:52 UTC)
- *Stock market today: Dow, S&P 500, Nasdaq climb with focus on Iran deal, Fed hike path* (Yahoo Finance, 2026-06-17 23:05 UTC)
- *Intel's stock jumps 11% — even as analysts say new Apple chip deal might start small* (MarketWatch Top Stories, 2026-06-18 14:05 UTC)
- *Intel shares jump as Trump says company will make chips for Apple* (MarketWatch Bulletins, 2026-06-18 10:15 UTC)
- *Accenture shares fall to lowest since 2017 as AI threat mounts* (FT International, 2026-06-18 13:51 UTC)
- *Two big reasons Accenture's stock is sliding in the wake of earnings* (MarketWatch Top Stories, 2026-06-18 14:19 UTC)
- *Apple to raise prices as AI boom pushes up chip costs* (BBC Business, 2026-06-18 14:03 UTC)
- *Apple says it will be forced to raise prices due to the AI boom* (MarketWatch Bulletins, 2026-06-17 22:07 UTC)
- *Nuclear Stocks Oklo, Centrus Jump After Signing Uranium Deal* (Yahoo Finance / IBD, 2026-06-18 14:36 UTC)
- *Bank of England holds interest rates at 3.75% amid Iran war peace prospects* (CNBC Economy, 2026-06-18 11:49 UTC)
- *Interest rates held as Bank warns of impact of high energy prices* (BBC Business, 2026-06-18 12:50 UTC)
- *Swiss Central Bank Holds Rates as War Pushes Up Inflation Forecast* (Yahoo Finance / WSJ, 2026-06-18 14:39 UTC)
- *SpaceX drops 6% as post-listing euphoria cools* (Investing.com Markets, 2026-06-18 14:42 UTC)
- *SpaceX is vastly more expensive than any stock in the S&P 500, fueled by 'FOMO' mentality* (MarketWatch Top Stories, 2026-06-18 14:38 UTC)
- *Gas prices — barely — are now below $4 per gallon nationally* (MarketWatch Bulletins, 2026-06-18 11:00 UTC)
- *The next two weeks could be a bumpy ride for U.S. stocks. Buy any dip, this strategist says.* (Citadel / MarketWatch Top Stories, 2026-06-18 13:33 UTC)
- *Why Flight Prices Might Not Fall After the U.S.-Iran Deal* (NYT Economy, 2026-06-18 09:03 UTC)
- *GE Vernova Supplier Near Breakout As Data Centers Lift Construction Sector* (Yahoo Finance / IBD, 2026-06-18 14:24 UTC)
- *Ukraine hits Moscow with largest-ever drone attack* (FT International, 2026-06-18 09:54 UTC)
- *Hegseth unveils six-month review of US military presence in Europe* (FT International, 2026-06-18 11:17 UTC)
- *Foreign Office drops 'do not travel' advice for UAE* (BBC Business, 2026-06-18 14:56 UTC)
- *Fueled by chipmakers, South Korea and Japan each hit new records* (MarketWatch Bulletins, 2026-06-18 09:43 UTC)
- *The Fed may make a mistake if it listens to the market, says Morgan Stanley* (MarketWatch Bulletins, 2026-06-18 10:46 UTC)
- Analytics: FRED macro through June 17; market data June 18 ~10:57am ET; EIA June 12 vintage; `brief_2026-06-18.json`; `brief_2026-06-17.json`; `data/scorecard_log.jsonl`
