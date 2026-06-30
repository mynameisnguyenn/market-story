# Market Story — 2026-06-30

> *Brief captured 2026-06-29 15:38 UTC (~11:38am ET). All prices from `brief_2026-06-29.json`. CFTC positioning June 23 vintage (the headline watch item from last session, now resolved). HY OAS and IG OAS: FRED June 26 vintage. Today is Q2-end — quarter-end rebalancing distorts closes; treat June 30 close signals with caution.*

---

## Since last time

Grading the June 29 `watch` block against `brief_2026-06-29.json`:

| Claim | Trigger | Result |
|---|---|---|
| CFTC June 23 S&P lev_net shows covering above −480k — first squeeze signal off cycle record | >−480,000 | **HIT** — S&P lev_net = **−373,468** (was −515,520 June 16; covered +142,052 contracts). Technically met, but the *mechanism* is more bearish than the headline: covering happened into a falling market (S&P fell from ~7,472 on June 23 to 7,360 on June 26 while +142k contracts were bought back) — **profit-taking**, not a forced squeeze. Simultaneously, Nasdaq shorts *added* −22,908 to −51,062 (bears rotated from broad S&P to targeted Nasdaq). P=0.45 — correct outcome, wrong mechanism. |
| HY OAS third consecutive print above 2.70% — credit regime widening confirmed | >2.70 | **HIT** — June 26 FRED: **2.83%** (+7bps from 2.76%; pct_1y 17.1→36.1). IG OAS +2bps to 0.77% (30.6th %ile from 12.7th). Three consecutive prints: 2.71% → 2.76% → 2.83%. P=0.60 — correct and understated; widening is *accelerating*, not merely persisting. |
| WTI closes above $72 — Iran vessel attack triggers renewed Hormuz enforcement | >72 | **MISS** — WTI $70.41 intraday (+1.70% but well below $72). NEW development: FT June 29 "US says it has agreed deal with Iran to halt strikes and resume talks" — a fresh ceasefire agreement reduces the near-term escalation thesis. P=0.30 — correct to hold low conviction. |
| Nasdaq underperforms S&P by more than 0.5% Monday — AI derating continues | ^IXIC <−0.5 | **MISS** — Nasdaq **+1.32%** vs S&P +0.73% intraday (Monday June 29). The bears added −22,908 Nasdaq shorts in the June 23 CFTC vintage; Monday's GOOGL Dow inclusion (+4.21%) and Amazon +4.13% squeezed that new position. Directionally wrong. P=0.55 — the bear rotation to Nasdaq was read correctly; the catalyst (GOOGL Dow inclusion) was not. |
| S&P 500 closes below 7,250 — credit + AI derating + fund outflows compound | <7,250 | **MISS** — S&P at 7,407 intraday. P=0.25 — correct to hold low conviction. |

Running hit-rate: **~19/57 (~33%)** — adding 2 HITs, 3 MISSes. Credit calls: 5/9 (56%) — the directional read on HY OAS has been consistently right even when thresholds miss. Oil calls: 0/5 (0%) — systematically wrong on the supply-disruption direction.

**June 29 stance (−1) settling:** Entry at S&P ~7,360 (June 26 close). Brief captures S&P at 7,407 intraday June 29 (+0.64%). If June 29 closed near 7,407, position running −0.64% (paper loss). Quarter-end distortion (June 30) inflates the noise; holding.

---

## Today in one line

**HY OAS 2.83% (June 26 FRED, third consecutive above 2.70%, 36th %ile — widening velocity +5bps then +7bps on sequential FRED prints) is the fastest credit repricing of this cycle; Monday's Nasdaq bounce (GOOGL Dow inclusion, Iran deal 2.0, Piper Sandler AI spending survey) is a tactical short squeeze on the bears' newly added Nasdaq position, not a structural clearing event — the flip requires HY OAS to reverse below 2.70% and IG OAS to hold below 0.78%, neither of which a Dow inclusion can deliver.**

*Bear confirmation: HY OAS 4th print above 2.80%; IG OAS through 0.80%; VIX catches credit above 22. Bull reversal requires: HY OAS below 2.70% on next FRED print, S&P above 7,450 post-July-1 open (filtering quarter-end), AND CFTC Nasdaq showing covering — all three together.*

---

## TL;DR

- **HY OAS 5th → 17th → 36th %ile in three FRED prints: this is acceleration, not widening.** 2.71% (Jun 23) → 2.76% (Jun 24) → 2.83% (Jun 26), with IG OAS following: 3.2nd → 12.7th → 30.6th %ile in the same window. The rate of change is the signal — at current velocity, HY OAS crosses the 50th %ile within two sessions.

- **CFTC June 23 data: bears repositioned, not capitulated.** S&P shorts covered +142k (profit-taking into last week's decline). But: Nasdaq shorts *added* −22,908 (new lev_net −51,062) and VIX longs increased −5,568. Sophisticated rotation from broad-index to Nasdaq-specific bear. Today's Nasdaq +1.32% is squeezing the new Nasdaq position; it's painful short-term but doesn't change the structural thesis.

- **New Iran deal (FT) is the main bull wildcard: removes the oil spike tail, but WTI is still up +1.70%.** The market is pricing the deal with skepticism (June 19 deal lasted 6 days before the June 25 vessel incident). If this deal holds, WTI below $68 is on the table. If it fractures, $72+ is immediate. Today is also Q2 quarter-end — treat close prices as rebalancing noise, not signal.

---

## What moved & why

### Equities & sectors

**Monday June 29: mega-cap tech squeeze vs. real-economy deterioration.** The GOOGL Dow inclusion drove mechanical index demand across tech; AMZN/META/ASML/TSM all followed. Meanwhile, everything growth-sensitive — materials, real estate, small caps — fell.

| Sector | Jun 29 Δ | Read |
|---|---|---|
| XLY (Cons. Discretionary) | **+2.15%** | Amazon +4.13%; single-stock, not a cyclical signal |
| XLC (Comm. Services) | **+1.70%** | GOOGL +4.21% on Dow inclusion — structural index demand |
| XLK (Technology) | **+1.29%** | Broad tech recovery; ASML +2.72%, TSM +2.91%, META +2.87% |
| XLF (Financials) | +0.43% | Steady |
| XLI (Industrials) | +0.44% | Mild; no direction |
| XLV (Health Care) | −0.21% | Giving back last week's defensive premium |
| XLP (Cons. Staples) | −0.54% | Defensive unwind as risk-on bid returns |
| XLU (Utilities) | −0.75% | 5Y yield +0.39% intraday pressuring rate-sensitives |
| XLRE (Real Estate) | **−1.35%** | Rate-sensitive; amplified on 5Y tick up |
| XLB (Materials) | **−2.52%** | Worst sector; commodity complex under pressure despite WTI bounce |

**Russell 2000 −1.04% while S&P +0.73%** — this divergence is the tell. A genuine risk-on recovery would lift small caps; the Monday bid is concentrated in Dow-component-sized names. Small caps are pricing soft growth; mega-caps are pricing GOOGL's index event. These are not the same thing.

**GOOGL +4.21% — Alphabet joins the Dow** (Yahoo Finance 15:20 UTC). Creates mandatory index-rebalancing demand from Dow-tracking funds and improves sentiment for AI mega-cap complex. Real demand pull, but it's a one-session event. Next session reverts to fundamentals: Chinese AI model competition (June 26 brief), GOOGL's AI-scientist defection (June 22 brief), search market share questions. The inclusion doesn't resolve any of those.

**The CFTC-NASDAQ squeeze in real time.** Bears added −22,908 contracts to Nasdaq-100 shorts in the week of June 23 (lev_net −28,154 → −51,062). Today GOOGL +4.21%, AMZN +4.13%, ASML +2.72%, TSM +2.91% — the *specific names* most likely to move Nasdaq are rallying hardest. The bear rotation to Nasdaq was directionally right on the thesis (AI derating); the timing was punished by an index-composition event. If this is short-covering forced by the GOOGL catalyst, the position rebuilds at slightly higher levels.

**Micron and Intel lower despite broad market gains** (Seeking Alpha 15:12 UTC). Chip sector split: mega-cap platform names (GOOGL, AMZN) recover; memory/foundry names (INTC, MU) lag. Consistent with the June 25 brief's read: Micron's beat validated existing utilization (current), while ASML's equipment orders reflect future capex commitments under pressure.

**Verizon −7%, AT&T 52-week low** (Investing.com 15:22 UTC): SpaceX satellite + cable convergence attacking traditional telco. Structural disruption, ongoing.

### Rates & the dollar

**Rates barely moved; the FRED credit data is the session.**

| Metric | Jun 26 brief | Jun 29 brief | Δ |
|---|---|---|---|
| 10Y (FRED) | 4.41% (Jun 24, 81.7th %ile) | **4.40%** (Jun 25, 79.8th %ile) | −1bp |
| 2Y (FRED) | 4.11% (Jun 24, 95.6th %ile) | **4.09%** (Jun 25, 94.4th %ile) | −2bps |
| 2s10s (FRED) | 0.31% (Jun 25, 1.6th %ile) | **0.31%** (Jun 26, 1.6th %ile) | flat |
| 10Y Breakeven | 2.21% (Jun 25, 0.4th %ile) | **2.20%** (Jun 26, 0.4th %ile) | −1bp |
| **HY OAS** | 2.76% (Jun 24, 17.1st %ile) | **2.83%** (Jun 26, 36.1st %ile) | **+7bps** |
| **IG OAS** | 0.75% (Jun 24, 12.7th %ile) | **0.77%** (Jun 26, 30.6th %ile) | **+2bps** |

The 10Y at 4.40% (79.8th %ile) and 2Y at 4.09% (94.4th %ile) are quiet — Warsh is holding, and the bond market is not pricing near-term cuts OR hikes aggressively. MarketWatch (15:34 UTC): "Wall Street is bracing for a wave of Fed rate hikes that may never come." The bond market agrees: 10Y is FALLING despite hawkish Warsh rhetoric. The 2s10s at 0.31% (1.6th %ile) is stuck. Near-flat curve + widening credit is the structural setup for recession pricing; the question is timing.

**10Y Breakeven 2.20% (0.4th %ile) — off the absolute floor but still historically extreme.** Maximum disinflation pricing. The bond market is telling you oil normalization (Iran deal 2.0) kills the inflation risk. If that's wrong (Iran deal fractures, WTI to $72+), the breakeven has significant repricing potential.

**DXY 101.14 (−0.21% intraday)** — dollar slightly weaker on the risk-on Monday bid. EUR/USD flat at 1.1423. USD/JPY +0.09% to 161.94 — carry trade quietly adding, which signals the BoJ-fear unwind of late June is not accelerating. The 5Y yield +0.39% intraday is pushing the belly of the curve mildly higher; not a regime shift.

### Commodities & credit

**WTI $70.41 (+1.70%) — rising despite a new Iran deal.** This is the paradox of the day. The FT announces a fresh ceasefire ("halt strikes and resume talks") and oil rallies. Most likely explanation: quarter-end rebalancing in commodity funds (June 30), not a fundamental signal. The June 19 peace deal sent WTI down −$5 instantly; the June 29 deal produced +1.70%. The market's diminishing discount of each Iran deal is itself a signal — deal fatigue means the next incident carries a larger risk premium.

**Brent +2.18% ($73.56)** — the WTI/Brent spread narrowing from ~$3.44 to ~$3.15. Consistent with global demand normalization rather than supply disruption.

**Gold $4,033.50 (−1.11%)** — continuing the trend lower, now at the 33.7th %ile. Gold's safe-haven function remains broken: credit is widening sharply (HY OAS 36th %ile, accelerating), and gold is falling. Either this risk-off isn't real (equity vol too low), or the safe-haven bid has been structurally replaced. The test: if VIX spikes above 22 on a catalyst, does gold bid? If not, the correlation has permanently shifted.

**HY OAS 2.83% / IG OAS 0.77% — see rates table.** The credit market is the session; everything else is context.

**EIA (June 19 vintage):** Crude draw −6,088 MBBL (modest bullish for demand), gasoline build +2,064 MBBL, distillate build +3,064 MBBL (product demand softening), SPR draw −9,060 MBBL (continuing even with WTI below $73). Nat gas +76 Bcf build (2,835 Bcf; normal injection season).

---

## Macro & data

**BLS (May 2026):**
- **CPI-U YoY: 4.25%** — headline inflation at 4.25% in May despite WTI averaging below $75. This reflects base effects and services inflation, not just energy. Even at current oil prices, the YoY won't clear 4.0% until late Q3 at the earliest.
- **Core CPI YoY: 2.85%** — the gap between headline (4.25%) and core (2.85%) means 140bps of current CPI is energy/food driven. WTI at $70 is helpful for headline but Warsh's preferred gauge (core PCE 3.4%) is the binding constraint.
- **Unemployment: 4.3%** (28.6th %ile; May, unchanged from April). Labor market softening but not deteriorating.
- **Avg hourly earnings: $37.53 (+3.45% YoY)** — real wages still deeply negative against 4.25% CPI; consumer purchasing power is being eroded despite nominal wage gains. A persistent drag on consumption.
- **Labor force participation: 61.8% (−0.6% YoY)** — declining participation means the unemployment rate understates labor market slack AND makes supply-side disinflation structurally harder.

**FRED (June 29 brief vintage):**
- EFFR 3.63% (June 26, 7.1st %ile) — Warsh holding; the rate is at the 7th %ile, meaning rates have been lower 93% of the year
- SOFR 3.62% (June 26, 8.3rd %ile, −2bps from 3.64%)
- NFCI −0.516 (June 19, 18.7th %ile) — financial conditions still loose; the lag model (6–8 weeks from June 19) targets late July–mid-August for NFCI tightening to confirm what HY OAS is already signaling
- VIX close (FRED): 18.41 (June 26, 67.5th %ile) — down from 18.89; equity vol is FALLING as credit widens. This is the divergence.

**Warsh skepticism building** (Seeking Alpha 15:19 UTC: "Warsh's Fed debut: Worse than a World Cup without Italy?"): Market confidence in Warsh's communication is fraying. MarketWatch (15:34 UTC): "Wall Street is bracing for a wave of Fed rate hikes that may never come." The bond market (10Y at 4.40%, falling) is explicitly betting Warsh's hawkishness is bluster. Supreme Court ruled Fed's Lisa Cook can stay (MarketWatch 15:12 UTC) — policy-continuity positive.

**Piper Sandler CIO survey: AI spending "beyond experimental"** (Investing.com 15:19 UTC): Directly contradicts Wedbush's "no ROI benchmarks" (June 26). One of these surveys is sampling a different population (large-cap CIOs with committed capex vs. SMB/mid-cap exploratory deployments), or the distribution is genuinely bimodal. Both can be true: the largest enterprises are past the experimental stage while the median enterprise still lacks benchmarks. The AI spending-certainty debate is not settled by two surveys in four days.

**Morgan Stanley: "America was built on fragile credit, speculation, not stability"** (Seeking Alpha 15:07 UTC): A major bank naming the structural vulnerability explicitly. This is the kind of sentiment that precedes actual de-risking at the institutional level — not a near-term trade signal but a multi-session positioning backdrop.

---

## Risk lens

**1. Credit acceleration is the one number that matters this week.** HY OAS moved from the 5.2nd %ile to the 17.1st %ile to the 36.1st %ile in three consecutive FRED prints. IG OAS: 3.2nd → 12.7th → 30.6th %ile in the same window. This is not a "spread widening back to normal" — this is an acceleration of the fastest pace in this cycle. At current velocity (+5bps, +7bps on sequential prints), HY OAS reaches the 50th %ile within one to two FRED sessions. The 50th %ile (~3.00%) is the historical median and a regime threshold that equity multiples have not priced.

**2. CFTC June 23 data: sophisticated repositioning, not capitulation.** The S&P covers (+142k) look like a squeeze signal at first glance. They're not:
- Covering occurred into a falling market (profit-taking, not forced)
- Simultaneously: Nasdaq shorts ADDED −22,908 (bears repositioned to the specific AI-derating thesis)
- VIX longs increased −5,568 (more hedging, not less risk)
- Ultra 10Y shorted −14,771 more (duration bears pressed)
The result: net S&P short fell from −515k to −373k (still the second-largest short in this series), while a NEW concentrated Nasdaq short opened at −51k. Today's Nasdaq bounce is squeezing the new position. If bears were capitulating, they would've covered VIX longs and reduced hedging — they added to both.

**3. The Iran deal paradox.** FT June 29: new deal announced. WTI up +1.70%. The market is paying less attention to each successive Iran deal announcement, which is itself a signal: deal fatigue means the risk premium embedded in the *next* incident is larger, not smaller. The June 19 deal wiped $5 off WTI within hours; the June 29 deal produced a bounce. The market has been burned twice by deal assumptions that proved temporary; it's no longer reflexively selling oil on headlines. This makes WTI harder to trade but keeps the tail risk alive.

**4. Complacency embedded in equity vol while credit accelerates.** VRP has compressed to 1.6 (VIX 18.3 vs. realized 16.7). When HY OAS is at the 36th %ile and accelerating, a VRP of 1.6 is historically low — it says equity markets are not pricing the credit signal at all. The setup for a vol shock: HY OAS prints above 3.00% → a catalyst forces equity vol to catch up → VIX spikes from 18 to 25+ in a compressed window. The trigger need not be credit-specific; any catalyst (Iran incident, large earnings miss, FOMC surprise) that forces correlation between credit and equity is enough.

**5. Quarter-end distortion: June 30 close is noise.** Quarter-end rebalancing creates artificial price pressure — asset managers adjusting equity/bond weights produce mechanical price moves unrelated to fundamentals. S&P above or below 7,450 at the June 30 close does not constitute a directional signal. Wait for the July 1 open to establish genuine direction post-rebalancing.

**What to watch next:**
- HY OAS 4th FRED print (likely Wed July 2): does the widening continue above 2.83% or reverse? The velocity of the current three-print sequence is what makes this the single most important data point of the week.
- CFTC July 7 data (June 30 vintage): did bears cover Nasdaq on Monday's squeeze or pressed? The −51k Nasdaq position is the active risk.
- Iran deal durability through July 1: the "halt strikes" language has a narrower scope than the June 19 deal's Hormuz restrictions — giving both parties more ambiguity. Watch AIS ship data and State Department statements through Tuesday.
- IG OAS approaching 0.80%: at 0.77% (30.6th %ile) and moving at +2bps per FRED print, the 0.80% level is 1–2 sessions away. Investment-grade above 0.80% triggers rebalancing flows in investment-grade credit ETFs (LQD has explicit IG OAS constraints in many pension mandates).

---

## What to watch

1. **HY OAS 4th consecutive print above 2.70% — acceleration unabated.** 2.71% → 2.76% → 2.83%; each print is +5–7bps. A 4th print above 2.80% confirms regime acceleration. A reversal below 2.75% would be the first pause in the widening trajectory. P=0.65 — IG OAS at 30.6th %ile suggests the move is broad, not HY-specific.

2. **IG OAS breaks above 0.80% — the next investment-grade threshold.** From 0.75% (12.7th %ile, June 24) to 0.77% (30.6th %ile, June 26) in one FRED print. At current velocity, 0.80% is 1–2 sessions away. Above 0.80%, IG credit repricing starts triggering pension-mandate technical flows. P=0.45 — the move is already fast; 0.80% would be the threshold that turns a credit widening into a credit-market event.

3. **Iran deal fractures within 72h — WTI spikes above $72.** June 19 deal lasted 6 days before the June 25 vessel incident. Watch for any vessel attack, boarding, or formal restriction announcement through July 1. P=0.25 — the deal language ("halt strikes") is narrower than June 19, giving both parties more room to operate within it; each successive deal buys slightly more time before fracture.

4. **S&P 500 holds above 7,450 on July 1 open — bounce confirmed, not quarter-end noise.** June 30 close is compromised by rebalancing flows; July 1 is the clean read. If S&P gaps above 7,450 at the open AND Nasdaq leads, one bear stop condition is approaching. P=0.35 — the Nasdaq squeeze is real but the credit backdrop hasn't changed.

5. **VIX closes above 22 — equity vol catches up to credit.** VRP at 1.6 with HY OAS at 36th %ile is the widest credit-vol divergence in this cycle. The reversion candidate: equity vol spikes to catch credit. P=0.30 for VIX above 22 within 3 sessions — requires a catalyst (Iran incident, bad jobs data, HY OAS shock print).

```watch
[
  {"claim": "HY OAS 4th consecutive print above 2.70% — credit acceleration unabated", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.70", "horizon": "next 3 sessions", "probability": 0.65},
  {"claim": "IG OAS breaks above 0.80% — investment-grade threshold breached", "metric": "macro:BAMLC0A0CM", "trigger": ">0.80", "horizon": "next 3 sessions", "probability": 0.45},
  {"claim": "S&P 500 holds above 7,450 on July 1 open — bounce confirmed, not quarter-end noise", "metric": "market:^GSPC:last", "trigger": ">7450", "horizon": "2026-07-01", "probability": 0.35},
  {"claim": "VIX closes above 22 — equity vol catches up to credit divergence", "metric": "market:^VIX:last", "trigger": ">22", "horizon": "next 3 sessions", "probability": 0.30},
  {"claim": "WTI holds above $72 — Iran deal fractures again within 72h", "metric": "market:CL=F:last", "trigger": ">72", "horizon": "2026-07-01", "probability": 0.25}
]
```

---

## The call

**Direction: −1 (maintaining bear).**

The primary stop condition — HY OAS below 2.70% — is further from being met than at any point in the last two weeks. HY OAS is at 2.83% (36.1st %ile) and accelerating. IG OAS is at 0.77% (30.6th %ile) and accelerating. No stop condition has been met. The Monday Nasdaq bounce is a tactical squeeze of the bears' newly added Nasdaq position (−51k lev_net, June 23 vintage); it's painful but not structurally falsifying.

The quarter-end distortion (June 30) makes today's close unreliable as a signal in either direction. Holding −1 through the close; reassess on July 1 open when the rebalancing noise clears.

**Why −1:**
- HY OAS 2.83% (June 26 FRED, 36.1st %ile) — third consecutive above 2.70%; velocity +5bps then +7bps on sequential prints; no sign of deceleration
- IG OAS 0.77% (30.6th %ile) — from 3.2nd %ile in one week; investment-grade repricing now active
- CFTC: S&P covered +142k (profit-taking), Nasdaq −22,908 additional shorts — repositioning, not capitulation; net S&P short still −373k (second-largest in series)
- VRP 1.6 vs. HY OAS 36th %ile = the widest credit-vol divergence of this cycle; embedded complacency in equity vol
- CPI 4.25% YoY (May 2026) — headline running hot; Warsh has no data to cut
- Russell 2000 −1.04%, Materials −2.52% Monday — growth-sensitive sectors absent from the bounce; it's an index-event rally, not a growth signal
- NFCI lag: 6–8 weeks from June 19 NFCI (−0.516) targets late July–August tightening; NFCI is the lagging confirmation of what HY OAS is leading

**Why not 0 (flat):**
- Zero stop conditions met; HY OAS is moving AWAY from the stop, not toward it
- Monday bounce is tactically painful but mechanically explicable (GOOGL Dow inclusion + quarter-end + Iran deal news)
- July 1 open (post-rebalancing) is the real test; not June 30 close

**Stop to 0:** HY OAS reverses below 2.70% on next FRED print AND S&P holds above 7,450 on the July 1 open (filtering quarter-end noise). Both conditions required simultaneously.
**Flip to +1:** HY OAS below 2.65%, CFTC Nasdaq covering above −30k, S&P above 7,500 — all three simultaneously unmet.

```stance
{"direction": -1, "notes": "Maintaining bear. HY OAS 2.83% (Jun 26 FRED, 36.1st %ile) — third consecutive above 2.70%; acceleration (+5bps, +7bps sequential). IG OAS 0.77% (30.6th %ile from 3.2nd in one week). CFTC June 23: S&P covered +142k (profit-taking into falling market, not a squeeze) but Nasdaq shorted -22,908 more (−51k lev_net). VRP 1.6 vs. HY OAS 36th %ile = widest credit-vol divergence of the cycle. Russell −1.04%, Materials −2.52% Monday — cyclical growth absent. CPI 4.25% YoY (May). NFCI lag targets late July. Q2 quarter-end distortion today — no directional trade on June 30 close. Stop to 0: HY OAS <2.70% AND S&P >7,450 post-July-1 open. Flip to +1: HY OAS <2.65%, CFTC Nasdaq >-30k, S&P >7,500 — all unmet."}
```

---

## Sources

- *US says it has agreed deal with Iran to halt strikes and resume talks* (FT International, 2026-06-29 15:23 UTC)
- *Alphabet debuts in Dow Jones Industrial Average as index tilts toward tech* (Yahoo Finance, 2026-06-29 15:20 UTC)
- *Piper Sandler CIO survey finds AI spending 'beyond experimental'* (Investing.com Markets, 2026-06-29 15:19 UTC)
- *Warsh's Fed debut: Worse than a World Cup without Italy?* (Seeking Alpha, 2026-06-29 15:19 UTC)
- *Wall Street is bracing for a wave of Fed rate hikes that may never come. These sectors stand to gain.* (MarketWatch Top Stories, 2026-06-29 15:34 UTC)
- *Micron, Intel lead chip stocks lower on Monday despite broader market gains* (Seeking Alpha, 2026-06-29 15:12 UTC)
- *Fed's Lisa Cook can stay on at central bank while challenging Trump's attempt to fire her, Supreme Court rules* (MarketWatch Top Stories, 2026-06-29 15:12 UTC)
- *Amazon Stock's Climb Leads Strong Day For Magnificent Seven* (Yahoo Finance, 2026-06-29 15:12 UTC)
- *Tech stocks halt slide, Google rises after joining the Dow* (Yahoo Finance, 2026-06-29 15:10 UTC)
- *Verizon falls 7%, AT&T hits 52-week low as SpaceX and cable rivals converge* (Investing.com Markets, 2026-06-29 15:22 UTC)
- *NBCUniversal to be split from Comcast in latest media shakeup* (Investing.com Markets, 2026-06-29 15:18 UTC)
- *America was built on fragile credit, speculation, not stability: Morgan Stanley* (Seeking Alpha, 2026-06-29 15:07 UTC)
- *Apple in the spotlight as Wall Street, Washington weigh in on possible China memory push* (Seeking Alpha, 2026-06-29 15:26 UTC)
- Analytics: FRED macro through June 25–26; CFTC June 23 vintage (the watch item, now resolved); BLS May 2026; EIA June 19 vintage; market data June 29 ~11:38am ET (Q2 end); `brief_2026-06-29.json`; `brief_2026-06-26.json`; `data/running_thesis.md`
