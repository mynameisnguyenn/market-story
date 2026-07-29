# Market Story — 2026-07-29

> *Brief: `brief_2026-07-28.json` (captured 2026-07-28 13:52 UTC — intraday Jul 28. FRED vintage: 10Y/2Y Jul 24, 2s10s Jul 27, HY/IG OAS Jul 24. CFTC Jul 21 unchanged. Previous brief: `brief_2026-07-27.json` (Jul 27 14:20 UTC). Key forward events: MSFT earnings Jul 28 AH — after brief capture; Fed rate decision TODAY Jul 29 14:00 ET.)*

---

## Since last time

Grading `narrative_2026-07-28.md` watch items against `brief_2026-07-28.json`:

| Claim | Trigger | Result |
|---|---|---|
| HY OAS holds above 2.75% on Jul 28-29 FRED vintage — credit confirmation survives ceasefire | macro:BAMLH0A0HYM2 >2.74 (horizon Jul 30) | **PENDING (early data: tracking HIT).** Jul 24 FRED: **2.79%** (+2bps from 2.77%). This is the pre-ceasefire print — widening happened BEFORE oil collapsed. Post-ceasefire FRED (Jul 25+) hasn't landed yet; horizon Jul 30. P=0.30 correct direction so far. |
| HY OAS tightens back below 2.72% on Jul 28-29 FRED — signal borrowed from oil shock | macro:BAMLH0A0HYM2 <2.73 (horizon Jul 30) | **MISS (early data).** 2.79% — widened further. P=0.45 wrong. |
| MSFT reports Azure miss or FCF compression (<−5%) | market:MSFT:change_pct <-5.0 (horizon Jul 29) | **PENDING.** MSFT reports Jul 28 AH, after brief capture at 13:52 UTC. Result not available. P=0.22. |
| MSFT beats Azure + positive FCF (>+3%) | market:MSFT:change_pct >3.0 (horizon Jul 29) | **PENDING.** Same — result not available. P=0.38. |
| 10Y FRED falls below 4.55% on Jul 28-29 vintage | macro:DGS10 <4.55 (horizon Jul 31) | **MISS (early data).** Jul 24 FRED: 4.69% — fell only 2bps, far above 4.55%. P=0.20 wrong. |
| 10Y FRED holds above 4.65% despite ceasefire | macro:DGS10 >4.64 (horizon Jul 31) | **HIT (early data).** Jul 24 FRED: 4.69% > 4.64%. Yields held elevated despite oil collapse. P=0.55 correct. |
| USD/JPY breaks below 160 | market:USDJPY=X:last <160.0 (horizon Jul 31) | **MISS (tracking).** USD/JPY 163.837 (+0.14%). Yen barely moved even as Nikkei fell 3.95%. P=0.12 wrong. |

**Running hit-rate: 31/119 (26.1%).** Net this session: 1 early HIT (10Y >4.64%), 1 confirmed MISS (HY OAS tighten), 4 pending. The prior stance was 0 (flat); paper P&L zero.

---

## Today in one line

**HY OAS widened a further 2bps to 2.79% (Jul 24 FRED) before the ceasefire deflated oil — proving credit is pricing AI capex destruction, not oil inflation — yet 9/11 sectors rose, Apple hit $5 trillion, and Dow added 0.62% on the same tape where ASML fell 5%; the verdict is binary and landing today: MSFT AH and the Fed at 14:00 ET.**

*Flip to −1:* MSFT FCF compression confirmed AND/OR HY OAS holds above 2.77% on post-ceasefire FRED. *Flip to +1:* MSFT beats + Fed neutral/dovish + HY OAS tightens below 2.70%.

---

## TL;DR

- **HY OAS 2.79% (Jul 24 FRED, +2bps) — widened PRE-ceasefire, on the GOOGL FCF miss, with oil still near $90.** This severs the oil-credit link: the market is pricing AI capex destruction as the independent credit driver. The next FRED print (Jul 25+, post-ceasefire) is the decisive test — if OAS holds above 2.75% with WTI at $80.89, it's structural.
- **XLK −3.22%, ASML −5.18%, TSMC −3.32%, Nasdaq −1.10% on a day 9/11 sectors advanced, Dow +0.62%, and Apple crossed $5 trillion.** Two markets, one index. Apple (AI monetization, no hyperscaler capex) at $5T vs ASML (AI manufacturing enabler, capex-dependent) at −5% is the market's clearest verdict on AI investment models.
- **Weekly scorecard: Nasdaq −4.56%, XLK −6.69%, Nikkei −5.84% vs Dow +0.60%, XLP +5.08%.** This is surgical derating of the AI infrastructure layer, not a broad selloff. The Fed and MSFT land today before the next brief is written.

---

## What moved & why

### Equities & sectors

**S&P 500 −0.25% to 7,394 (−$35), Nasdaq −1.10% to 24,659 (−273pts), Dow +0.62% to 52,536 (+325pts), Russell 2000 −0.22% to 2,942. VIX +1.93% to 19.03.** The Dow-Nasdaq spread (+0.62% vs −1.10%) is a single-session encapsulation of the regime.

**Sector dispersion:**

| Sector | Change | Read-through |
|---|---|---|
| XLP (Staples) | **+3.48%** | Defensive bid + oil → margins |
| XLV (Healthcare) | +2.61% | UNH beat; defensive rotation |
| XLB (Materials) | +1.85% | Lower input costs (oil) |
| XLC (Comm. Services) | +1.37% | NFLX +4.12%; non-AI media |
| XLU (Utilities) | +1.13% | Rate relief + defensive |
| XLRE (Real Estate) | +1.03% | Rate relief |
| XLY (Discretionary) | +0.84% | Lower oil = consumer purchasing power |
| XLF (Financials) | +0.40% | Stable credit; rate-net-income neutral |
| XLE (Energy) | +0.35% | WTI −2%, energy absorbs continued fall |
| XLI (Industrials) | −0.53% | Mixed |
| **XLK (Technology)** | **−3.22%** | AI chip derating, day 2 |

9/11 sectors advanced; the only meaningful red is XLK. The week's spread: XLK −6.69% vs XLP +5.08% — an 11.8 percentage-point weekly divergence. At Liberation Day magnitude, sustained over a second consecutive week.

**Movers — top leaders: NFLX +4.12%, CRM +3.51%.** NFLX is reversing its prior derating (was −6.35% in June, −1.96% in July); CRM is the second consecutive session as the top single-name leader. Enterprise software (CRM) and consumer streaming (NFLX) are separating cleanly from AI infrastructure. Both benefit from AI features without needing to build the infrastructure.

**Movers — top laggards: ASML −5.18%, TSMC −3.32%, NVDA −1.46%.** ASML has now shed ~12.7% in two sessions without a single earnings miss — this is positioning and sentiment, not fundamentals. The brief headline reads "chip stocks extend selloff on AI financing, China competition worries" (Investing.com 13:39 UTC). "AI financing" is the key phrase: the market is repricing the cost of capital for AI buildout, not just the demand for chips.

**Apple at $5 trillion** (Yahoo Finance 13:40 UTC Jul 28). The only prior company to reach this level was briefly Nvidia (during the AI capex frenzy peak). Apple's model: on-device AI, services revenue, no hyperscaler capex. GOOGL spent $190bn on AI and got FCF-negative. Apple benefits from the same AI wave without the bill. The $5T milestone on the same session ASML falls 5% is the market's clearest statement: the AI buildout model is broken; the AI monetization model is rewarded.

**Global: Nikkei −3.95% (−5.84% on week), Shanghai −1.16%.** The Nikkei decline is NOT yen-driven: USD/JPY +0.14% (yen weakening should SUPPORT Nikkei exports). The Nikkei is falling because Japan's semiconductor equipment complex (Advantest, Tokyo Electron, Shin-Etsu) mirrors ASML's derating. The Nikkei's −5.84% weekly loss is the largest since the BoJ hike disruption.

### Rates & the dollar

**Day-over-day deltas (Jul 28 brief vs Jul 27 brief):**

| Metric | Jul 28 | Jul 27 | Δ | 1Y Pct |
|---|---|---|---|---|
| 10Y mkt | 4.629% | 4.653% | **−2.4bps** | 97.6th %ile |
| 30Y mkt | 5.121% | 5.133% | **−1.2bps** | — |
| 5Y mkt | 4.384% | 4.410% | **−2.6bps** | — |
| 10Y FRED (Jul 24) | **4.69%** | 4.71% | **−2bps** | **99.2nd %ile** |
| 2Y FRED (Jul 24) | **4.33%** | 4.37% | **−4bps** | **99.2nd %ile** |
| 2s10s FRED (Jul 27) | **0.34%** | 0.36% | **−2bps** | **3.6th %ile** |
| **HY OAS (Jul 24)** | **2.79%** | 2.77% | **+2bps 🔴** | 31.7th %ile |
| IG OAS (Jul 24) | 0.80% | 0.79% | +1bp | 60.7th %ile |
| DXY | 101.518 | 101.448 | +0.07 | **99.2nd %ile** |

Yields fell marginally (−2-3bps across the curve) as oil continues falling and the ceasefire removes the oil-inflation tail. The 10Y at 4.629% (market) is still at the 97.6th 1-year percentile despite the slight relief. The FRED 10Y (4.69%, Jul 24 vintage) remains at the 99.2nd %ile — historically extreme in the data.

**2s10s re-flattened −2bps to 0.34% (3.6th %ile).** The brief steepening from the prior session (+2bps to 0.36% on Jul 24 FRED, noted as "ceasefire relief") has been fully reversed in one window. The 2s10s is back near the flattest levels of the cycle. The bond market is not buying the ceasefire as a regime-change event — it is pricing the structural stagflation narrative.

**HY OAS 2.79% (Jul 24 FRED, +2bps): The pre-ceasefire confirmation.** This is the most important new data point. On Jul 24, when oil was still near $90 and BEFORE the Jul 27 ceasefire, credit widened a further 2bps. The widening is not oil-driven — it is AI-capex-driven. GOOGL's Jul 23 FCF miss (−$190bn AI spend) is in the same FRED window as this widening. The credit market reacted to GOOGL before oil fell.

The post-ceasefire test (Jul 25+ FRED) is still outstanding. With oil now at $80.89, a tightening from 2.79% to below 2.72% would argue the widening was frontrunning a geopolitical shock that has now resolved. A hold above 2.75% argues credit has found a new floor driven by AI capex risk.

**The key counterintuitive observation:** 10Y yields FELL 2.4bps on a day XLK fell 3.22%. Normally, lower yields support tech (long-duration, DCF-sensitive). The fact that tech fell DESPITE rates easing confirms the derating is fundamental (AI FCF destruction), not macro (rate sensitivity). This is the clearest evidence of a structural derating.

### Commodities & credit

**WTI $80.89 (−2.08%), Brent $86.11 (−2.55%).** Oil continues the post-ceasefire slide: WTI has fallen from $90 (Jul 23) to $80.89 in 5 trading days — a $9.11 drop in one week. Weekly: −4.73%. The EIA commercial builds (crude +2,010 MBBL, gasoline +765 MBBL — BOTH building when WTI was at $90) confirm demand destruction was already underway before the ceasefire provided supply relief. The WTI YTD gain is still +40.87%.

**Gold $4,022.50 (−1.28%).** Gold approaching $4,000 — now at the 27.4th 1-year percentile, below the one-year median. Gold is falling despite: VIX at 19.03, HY OAS widening, and Nasdaq −4.56% weekly. The driver: falling oil removes the inflation-via-energy channel that supported gold as a stagflation hedge. If oil stays near $80, the inflation-scare premium in gold deflates further. The $4,000 level is a clean structural test.

**HYG +0.02%, LQD +0.11%, TLT +0.23%.** Credit ETFs barely moved despite the +2bps FRED widening in HY OAS — the FRED is a backward-looking data point (Jul 24) not yet reflected in real-time market prices. TLT +0.23% is consistent with yields falling −2bps.

---

## Macro & data

**FRED key new prints (Jul 24 vintages):**
- 10Y: 4.69% (−2bps; **99.2nd %ile, z=2.51**) — still near the year's high
- 2Y: 4.33% (−4bps; **99.2nd %ile, z=2.47**) — same regime
- 2s10s: 0.34% (Jul 27; −2bps; **3.6th %ile, z=−1.94**) — re-flattened back toward cycle lows
- HY OAS: **2.79%** (+2bps; 31.7th %ile) — continued widening
- IG OAS: 0.80% (+1bp; 60.7th %ile) — IG following HY
- Broad USD: 120.71 (75.4th %ile)

**White House: "Inflation much more likely to be transitory" — CEA Chair Stephen Miran (Seeking Alpha, 13:47 UTC Jul 28).** This is a senior White House statement directly addressing today's Fed decision. Miran's "transitory" framing aligns with the CPI 3.53% print (fell MoM for first time since 2020). The CEA Chair making this statement days before the Fed decision is political pressure in plain sight: the White House is signaling it does not want a hike. This narrows the Fed's optionality toward neutral/dovish hold.

**BLS (Jun vintage, unchanged):** CPI-U 3.53% YoY; Core CPI 2.59%; NFP +57k (cycle low); Unemployment 4.2%; AHE +3.52% YoY; Participation 61.5% (−0.3%).

**EIA (Jul 17 vintage):** Crude +2,010 MBBL (BUILD), Gasoline +765 MBBL (BUILD), Distillate +1,395 MBBL (BUILD), SPR −5,057 MBBL (DRAW — largest of cycle), Nat gas +32 BCF. The SPR drain of 5,057 MBBL reveals the government was suppressing oil prices via strategic reserve releases even before the ceasefire — the ceasefire adds supply-side relief on top of a policy intervention that was already working.

**CFTC (Jul 21, unchanged):**

| Contract | lev_net | Change | Reading |
|---|---|---|---|
| S&P 500 e-mini | −322,865 | +42,137 | Bears profit-took; still substantially short |
| Nasdaq-100 | **−74,690** | **−10,527** | Bears ADDED — near-cycle extreme |
| VIX futures | +3,098 | −7,091 | Vol longs reduced (before VIX rose to 19) |
| Ultra 10Y | −380,604 | −2,039 | Duration shorts unchanged |
| Ultra T-Bond | −899,165 | +11,287 | Long-end bears trimmed modestly |

The Nasdaq short at −74,690 is the dominant positioning fact: if MSFT beats tonight, this position is the fuel for a short squeeze. The bears added 10,527 contracts INTO the chip selloff — this is conviction, not reactive positioning. A MSFT beat at this loading would be the largest squeeze event of the cycle.

---

## Risk lens

**1. HY OAS 2.79% pre-ceasefire: the credit arm is now self-reinforcing.**

The sequence: HY OAS 2.68% (Jul 22 FRED, before GOOGL) → 2.77% (Jul 23, same session as GOOGL −7.13%) → **2.79% (Jul 24, the session after GOOGL)** — and oil was still at ~$90 on Jul 24. Credit widened BECAUSE of GOOGL FCF destruction, not because of oil. The ceasefire (Jul 27) removed WTI from $90 to $80; if the next FRED print shows OAS tightening, the oil-credit link was real. If OAS holds above 2.75%, the AI capex risk premium is the driver.

This distinction matters enormously: oil-driven credit widening fades with the oil spike. AI-capex-driven credit widening is structural (because the AI capex cycle is a multi-year commitment, not a single shock).

**2. Apple $5T vs ASML −5%: the market is pricing AI efficiency, not AI spending.**

Apple (no hyperscaler capex, on-device AI integration, services monetization) reached $5 trillion on a day the index S&P fell −0.25%. ASML (the leading enabler of AI fab buildout) fell 5% for the second consecutive session. The two stocks are pricing opposite theories of AI value:
- **Apple model:** AI features bolt onto existing margin structure; no capital commitment at risk
- **ASML/GOOGL model:** AI requires massive upfront capex that destroys near-term FCF; payoff uncertain and multi-year

The market is voting emphatically for the Apple model. This is consistent with the IBM −22% signal (Jul 14: "clients redirected money FROM IBM TO chips" = the spending is happening, but the returns aren't flowing to legacy software), Salesforce +3.51% (enterprise AI-feature bolt-on), and NFLX +4.12% (AI recommendation engine without capex risk).

**3. VRP 9.7 — options market most scared of the cycle.**

VIX 19.0 vs realized 20d vol 9.3 = VRP 9.7. The prior session was VRP 8.4; the Jul 23 cycle high was 10.0. VRP at 9.7 means options buyers are paying nearly double realized risk in premium. The VIX headline (19.03) is near the 73.4th %ile — not in panic territory — but the premium above realized vol is extreme. The two immediate binaries (MSFT + Fed) are priced into VIX but the market doesn't know which direction they resolve. After they land, VRP should compress sharply in whichever direction.

**4. Nikkei −3.95% without yen strength — the chip derating is global.**

USD/JPY +0.14% (yen WEAKER, should support Nikkei via export advantage). Yet Nikkei −3.95%. This is the Japanese semiconductor equipment and materials complex: Advantest (test equipment), Tokyo Electron (fab equipment), Shin-Etsu (silicon wafers) — all exposed to the same AI buildout derating that ASML is experiencing. The global chip equipment supply chain is being repriced simultaneously. The Nikkei's −5.84% weekly decline traces directly to this layer.

The yen carry trade remains coiled at USD/JPY 163.84. The carry is funded; the chip longs it funded are being liquidated. So far the two moves are uncorrelated — chips fall, yen doesn't move. If MSFT misses and triggers a sharp equity decline, the carry unwind could ADD to the selling (3-5 USD/JPY handles, simultaneous with chip selling).

**5. The Fed decision — the day's binary.**

Going into the decision (results not in this brief):
- CPI 3.53% (MoM decline for first time since 2020) — removes "must hike" case
- Core CPI 2.59% — well-controlled
- WTI $80.89 (−10.4% from peak) — forward inflation pressure easing
- NFP +57k — labor softening
- CEA Miran "transitory" — White House aligned with dovish hold
- BUT: DXY 99.2nd %ile, 10Y 99.2nd %ile — financial conditions still historically tight

The macro setup favors a hold. The question is the language. Warsh has been hawkish throughout; "following the script" (neutral hold) is the base case. The tail that matters for bears: a hold with hawkish language ("no rate cuts expected, monitoring inflation") keeps the multiple compression intact. The tail that matters for bulls: a dovish hold ("labor weakness merits attention") triggers the Nasdaq −74,690 squeeze.

---

## What to watch

**1. MSFT reaction today — the decisive AI capex read.**

MSFT reports Jul 28 AH. Azure revenue growth and FCF trajectory vs GOOGL's −$190bn AI spend pattern.

```watch
[
  {"claim": "MSFT shows FCF compression on AI capex — 3 of 3 hyperscalers confirm structural AI P&L destruction; chip derating accelerates; -1 entry triggered", "metric": "market:MSFT:change_pct", "trigger": "<-5.0", "horizon": "2026-07-29", "probability": 0.25},
  {"claim": "MSFT beats Azure + positive FCF — GOOGL miss idiosyncratic; Nasdaq -74,690 short squeeze; re-evaluate +1", "metric": "market:MSFT:change_pct", "trigger": ">3.0", "horizon": "2026-07-29", "probability": 0.35}
]
```

**2. HY OAS post-ceasefire test — structural vs oil-driven.**

The next FRED vintage (Jul 25+) arrives post-ceasefire. Does credit hold above 2.75% with oil at $80.89?

```watch
[
  {"claim": "HY OAS holds above 2.75% on post-ceasefire FRED — AI capex is the independent credit driver; bear thesis structurally confirmed", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.74", "horizon": "2026-07-31", "probability": 0.38},
  {"claim": "HY OAS tightens below 2.70% on post-ceasefire FRED — oil-collapse reverses the widening; credit arm dissolves again", "metric": "macro:BAMLH0A0HYM2", "trigger": "<2.71", "horizon": "2026-07-31", "probability": 0.38}
]
```

**3. VIX — does fear break the 20 threshold?**

VIX at 19.03 (73.4th %ile), approaching 20. Above 20 with HY OAS >2.75% = bear signals aligning.

```watch
[
  {"claim": "VIX breaks and holds above 20.0 — vol regime change; options market pricing a tail not captured in realized vol", "metric": "market:^VIX:last", "trigger": ">20.0", "horizon": "2026-07-30", "probability": 0.32}
]
```

**4. 10Y post-Fed.**

The term structure's verdict on Warsh's language.

```watch
[
  {"claim": "10Y FRED holds above 4.65% through Jul 31 — term premium / fiscal dominant; Fed language hawkish or neutral; no multiple relief", "metric": "macro:DGS10", "trigger": ">4.64", "horizon": "2026-07-31", "probability": 0.55},
  {"claim": "10Y falls below 4.50% on dovish Fed signal — multiple relief begins; chip selloff overdone thesis gains traction", "metric": "macro:DGS10", "trigger": "<4.50", "horizon": "2026-07-31", "probability": 0.18}
]
```

---

## The call

**Direction: 0 (flat) — maintaining. Both resolving binaries (MSFT + Fed) land today; entering −1 before either replicates the documented Jul 9 mistake.**

The bear evidence has strengthened materially:
- HY OAS 2.79% (pre-ceasefire widening = structural signal)
- XLK −3.22%, ASML −5.18% day 2
- Nasdaq −4.56% weekly
- VRP 9.7 (near-cycle high)
- Nikkei −5.84% weekly

But the Nasdaq short at −74,690 is the key asymmetry. A MSFT beat tonight triggers a squeeze that would destroy a fresh −1 position instantaneously. The Jul 9 parallel is exact: entered −1 before a hyperscaler earnings event, got squeezed by the relief bid.

**Conditional entry map (for real-time action today/tonight):**
- **Enter −1** if MSFT FCF compression confirmed (change_pct <−5%) OR Fed hawkish hold + HY OAS holds above 2.77% on next FRED print
- **Enter +1** if MSFT beats (>+3%) + Fed neutral/dovish + HY OAS tightens below 2.70%
- **Remain 0** if MSFT in-line, Fed neutral, credit ambiguous

The credit story is the most compelling it has been all cycle. The right move is to wait 12 hours for the information, then act with conviction rather than anticipate.

```stance
{"direction": 0, "notes": "Maintaining flat. HY OAS 2.79% (Jul 24 FRED, +2bps) = credit widened PRE-ceasefire on GOOGL FCF miss — AI capex is the driver, not oil. XLK -3.22%, ASML -5.18% day 2 structural. VRP 9.7 near-cycle high. BUT Nasdaq -74,690 short + MSFT earnings tonight = documented Jul 9 squeeze risk prevents -1 entry pre-binary. Fed resolves today. Conditional entries: -1 on MSFT FCF miss OR Fed hawkish + OAS >2.77%; +1 on MSFT beat + Fed dovish/neutral + OAS <2.70%. Running hit-rate: 31/119 (26.1%). Oil calls retired."}
```

---

## Sources

- *Apple tops $5 trillion market cap, only second company to hit the milestone* (Yahoo Finance, 2026-07-28T13:40 UTC)
- *U.S. chip stocks extend selloff on AI financing, China competition worries* (Investing.com, 2026-07-28T13:39 UTC)
- *Current inflation is 'much more likely to be transitory' – Stephen Miran* (Seeking Alpha, 2026-07-28T13:47 UTC)
- *Nasdaq opens lower as AI worries mount ahead of pivotal earnings* (Investing.com, 2026-07-28T13:36 UTC)
- *US backs Madagascar rare earths project in push to loosen China's supply chain grip* (Investing.com, 2026-07-28T13:42 UTC)
- *Moonshot wants more Nvidia Blackwell GPUs for its next AI model: report* (Seeking Alpha, 2026-07-28T13:46 UTC)
- *What's next for UnitedHealth after its major Q2 earnings beat?* (Seeking Alpha, 2026-07-28T13:47 UTC)
- Analytics: `brief_2026-07-28.json` (Jul 28 13:52 UTC intraday); `brief_2026-07-27.json` (Jul 27 14:20 UTC); CFTC Jul 21 vintage; FRED Jul 24 / Jul 27 vintages; `data/running_thesis.md`
