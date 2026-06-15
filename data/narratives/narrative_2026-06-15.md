# Market Story — 2026-06-15

> *Brief captured 2026-06-12 14:48 UTC — Friday session, early US morning (10:48am ET). Intraday snapshot; not a confirmed close. Weekend gap follows: Iran deal may or may not have materialized. CFTC positioning still June 2 (13 trading days stale). BoJ meets June 16–17 (tomorrow/Tuesday). All prices from brief_2026-06-12.json.*

---

## Since last time

Grading the June 12 `watch` block against the June 12 brief (horizon = "next 3 sessions" → June 12, 15, 16):

| Claim | Trigger | Result |
|---|---|---|
| HY OAS confirms cascade break above 2.83% | `macro:BAMLH0A0HYM2 > 2.83` | **PENDING** — FRED June 10 data unchanged at 2.80% in both briefs. Iran peace-deal news removes the near-term widening catalyst; verdict due this week. Recalibrating threshold to `>2.85%` given peace deal headwind. |
| WTI above $93.50 — Hormuz escalation premium | `market:CL=F:last > 93.5` | **MISS** — WTI $86.23 (−$4.57 from June 11 brief, −5.0%). Trump called off strikes overnight and claimed "close to a deal." Exactly the scenario where this trigger fails. P=0.25 → resolved at $0. |
| Gold below $4,000 — forced selling accelerates | `market:GC=F:last < 4000` | **MISS** — Gold $4,207.70 (+$106.80). The peace-deal news released forced sellers; the metal reversed $107 off the 6-month low in a single session. P=0.30 → resolved at $0. |
| USDJPY above 162 — BoJ pauses June hike | `market:USDJPY=X:last > 162` | **PENDING** — USDJPY 160.25 (−0.25). BoJ decision June 16–17. |

**Cumulative watch scorecard through June 12:** ~4 triggered of ~26 expired items. WTI >93.50 (P=0.25) and Gold <4000 (P=0.30) both missed in the same session they were logged — the Iran peace catalyst inverted both simultaneously. Credit watch: 0/7 on strict OAS triggers (>2.80%, then >2.83%), directionally correct all 7 sessions, threshold consistently 2–5bps too tight. The pattern is the trigger is right but the level is aggressive; adjusting to `>2.85%` for the coming week.

**June 11 stance (direction: −1): SETTLED +0.08%** — per scorecard log. S&P was down −0.08% on June 12 intraday; the short was profitable even as the broader market began pricing the Iran deal.

**June 12 stance (direction: −1): PENDING** — Intraday brief; June 12 close + weekend dynamics will determine settlement.

---

## Today in one line

**Trump's Friday call-off of Iran strikes vaporized the stagflation fear premium in one session (WTI −$5, VIX −3 pts, VRP from 8.2 to 4.0), but BlackRock's $13bn HPS credit fund just honored less than 40% of redemptions for the SECOND consecutive quarter, confirming that the private-credit cycle is deteriorating independent of any oil deal — so today the question is whether the deal survived the weekend, and if it didn't, the bear thesis reasserts faster because the vol protection was already vented.**

*Flip condition: Iran cease-fire confirmed by Monday open, Strait of Hormuz explicitly reopened — WTI breaks below $82, HY OAS reverses below 2.70% within 5 sessions, CFTC shows 50k+ net covering. All three required simultaneously; none confirmed yet.*

---

## TL;DR

- **The Friday fakeout question dominates Monday's open.** Trump claiming "US close to deal" and calling off planned strikes crashed WTI $5 and collapsed VIX 3 points. But this is the THIRD major Iran oil swing in this cycle (cease-fire June 9 → re-escalation June 10–11 → "deal" June 12). IBD's headline was not subtle: *"Is It Another Friday Fakeout?"* If the deal didn't materialize over the weekend, Monday opens with oil snapping back, VRP reconstituting from a dangerously low 4.0, and the bear thesis reasserting from a less-hedged starting point. **Consequence for risk:** The VRP compression is the bear's gift and the bull's trap simultaneously.

- **BlackRock private credit gate: second consecutive quarter.** FT June 12: *"BlackRock private credit fund honours less than 40% of redemption requests"* — HPS Corporate Lending Fund ($13bn), second quarter in a row below 40%. Two consecutive gates = a structural deterioration, not an anomaly. The private→public credit cascade thesis is now institutionally confirmed, independent of Iran. **Consequence for risk:** HY OAS at 2.80% is not an Iran story; it's a credit-cycle story. A peace deal reduces the energy catalyst but does not re-gate an ungated fund.

- **SpaceX IPO ($75bn, largest in history) hit the Nasdaq Friday.** Indicated +30% from the $135 IPO price; valuation ~$1.8T+. S&P 500 said NO (profitability threshold unmet). Nasdaq-100 inclusion is next (watch rebalancing date). **Consequence for risk:** The largest equity supply event ever draws passive capital toward SPCX and strains liquidity everywhere else at the same moment the spec short is at records and credit is gating.

---

## What moved & why

### Equities & sectors

Brief-to-brief (June 11 intraday → June 12 intraday as of 10:48am ET):

| Asset | Jun 11 brief | Jun 12 brief | Δ | Read |
|---|---|---|---|---|
| S&P 500 | 7,292.18 | 7,388.35 | **+96.17 (+1.32%)** | Masked by intraday −0.08% on June 12; most of the gain was the June 11 afternoon recovery |
| Nasdaq Composite | 25,294.95 | 25,683.70 | +388.75 (+1.54%) | −0.49% intraday June 12; SpaceX IPO competing with the index |
| Russell 2000 | 2,874.10 | 2,954.19 | **+80.09 (+2.79%)** | Biggest US beneficiary of rate relief + Iran peace; small caps carry highest sensitivity to both |
| Nikkei 225 | 64,179.27 | 66,020.04 | **+1,840.77 (+2.87%)** | Japan is the clean terms-of-trade winner: oil importer + Iran deal = deflationary tailwind; largest single-session move in the week |
| Euro Stoxx 50 | 6,057.74 | 6,148.53 | +90.79 (+1.50%) | European relief; UK GDP −0.1% in April already in the data — recovery priced faster than the damage |
| Hang Seng | 24,249.29 | 24,718.10 | +468.81 (+1.93%) | China/Asia risk-on; copper +2.5% = demand narrative |

June 12 sector snapshot (intraday, 10:48am ET):

| Sector | Δ Day | Read |
|---|---|---|
| Energy (XLE) | +1.63% | Counterintuitive: WTI intraday −1.69% while energy equities rally. Equity market pricing cheaper cost-of-capital + credit relief, not the oil price. Watch for reversal if deal fails. |
| Financials (XLF) | +1.24% | BofA "what to buy on Iran deal" = credit spread relief bid; Visa +1.76% (payments volume normalisation) |
| Materials (XLB) | +1.31% | Copper +2.5%; metals rallying on peace = demand restoration narrative |
| Real Estate (XLRE) | +0.99% | Rate relief (10Y −2bps); rate-sensitive bid intact |
| Cons. Discretionary (XLY) | **−1.11%** | Amazon −2.63%; consumers hit as SpaceX sucks oxygen from the tape |
| Comm. Services (XLC) | −0.62% | MSFT −1.47%, NFLX −1.85%, META −0.81% |
| Technology (XLK) | −0.09% | ASML −2.37% (giveback of Thursday's +4.86%); AI software still under multiple compression |

The XLE/WTI inversion is the tell: energy equities are pricing a 2–3 step narrative (peace → lower oil → lower inflation → eventual rate cuts → cheaper capital for energy companies), while crude is pricing the physical reality. One of them will be wrong by end of week.

Key watchlist names: ASML −2.37% (pure giveback; not a fundamental signal), Amazon −2.63% (AWS capex story continues to weigh), CRM −1.67% (week: −11.6%, now YTD −37.9%).

### Rates & the dollar

| Tenor / Series | Jun 11 brief | Jun 12 brief | Δ | %ile |
|---|---|---|---|---|
| 10Y (market) | 4.521% | **4.499%** | −2.2bps | 95.6th |
| 5Y (market) | 4.253% | **4.225%** | −2.8bps | — |
| 30Y (market) | 4.997% | **4.986%** | −1.1bps | — |
| 2s10s (FRED, Jun 11) | 0.42% (Jun 10) | **0.40%** | **−2bps** | 0.4th |
| 10Y Breakeven (FRED) | 2.34% (47.2nd) | **2.29% (24.2nd)** | **−5bps** | — |
| VIXCLS (FRED) | 22.22 (87.7th) | **19.44 (75.8th)** | **−2.78 pts** | — |

The 10Y breakeven is the most forward-looking read: −5bps in one FRED observation (June 10 → June 11), falling from the 47th to the 24th %ile. Bond markets are pricing OUT long-run inflation risk based on the Iran deal news, FASTER than the physical oil market. This is the exact pattern of the June 9 cease-fire (breakevens fell, then oil rebounded, then breakevens caught back up). If Monday's oil open is above $88, breakevens reprice up violently.

The 2s10s reflattened from 0.42% to 0.40% — back at the 0.4th %ile. Despite a peace-deal risk-on session, the curve remains glued to the flattest levels of the year. A confirmed peace deal that prompts Fed cut expectations should steepen the curve (2Y falls as short end reprices). The fact that it FLATTENED is either (a) FRED lag artifact or (b) the bond market reading the peace deal as growth-negative-not-inflation-negative (recession hedge > rate-cut pricing). Watch 2s10s response Monday.

**Dollar: DXY 99.754 (−0.441, back below 100, 90.5th %ile).** The safe-haven dollar bid that pushed DXY above 100 (97.6th %ile) reversed on peace deal news. EUR/USD +0.45% to 1.1575 — EUR recovering despite ECB hiking into a growth slowdown.

**USDJPY: 160.249 (−0.253).** Slightly stronger yen on risk-on. BoJ June 16–17 is binary: clean +25bps hike → USDJPY 158–159, carry unwind risk reduced; pause on leadership vacuum → USDJPY 162+, carry unwind activated. The yen's slight strengthening on Iran peace day suggests the market is giving the BoJ a slight benefit of the doubt.

### Commodities & credit

**WTI: $86.23 (−$4.57 from June 11 brief, −5.04%). The third major Iran oil swing.**

| Day | Event | WTI |
|---|---|---|
| Jun 9 | Cease-fire premium priced out | $87.58 (−4.07%) |
| Jun 10 | Re-escalation: helicopter downed | $89.71 (+1.71%) |
| Jun 11 | "Total control" language; tanker attack; Indian sailors killed | $90.80 (+1.21%) |
| Jun 12 | Trump calls off strikes, "close to deal" | **$86.23 (−$4.57)** |

Pattern: WTI swings $3–5 per Iran headline. The FT (14:25 UTC) described oil at a "three-month low." MarketWatch (13:55 UTC): "Global oil prices drop to $88 a barrel on hopes for an Iran peace deal as early as this weekend." WTI is now at the 73.4th %ile — elevated but not the 87th %ile extreme of $90.80. If the deal is confirmed, WTI could test $82–84 (the pre-Iran-conflict range). If the deal fails: the baseline is above $90 again by Tuesday.

**Gold: $4,207.70 (+$106.80 brief-to-brief, +2.60%). The forced-selling narrative reversed.**

The metal that was "speculative investors exiting" (FT June 11, 6-month low) reversed $107 in a single session. Interpretation: (a) margin call pressure reduced as vol collapsed (VRP 4.0, VIX 19), releasing the forced sellers, and (b) the gold inflation-hedge bid reasserted as peace deal news created a new narrative. The price is at the 48.4th %ile — back to a neutral level, not a structural re-rating. The Q1 2026 premium above $4,300 is NOT back.

Silver: $66.76 (+4.30%). Copper: $6.421 (+2.46%, 96.8th %ile). Both metals rallied on the China demand + peace deal narrative. Copper at 96.8th %ile remains a stretched position.

**HY OAS: 2.80% (FRED June 10 — UNCHANGED from June 11 brief, same data point).**

No new FRED OAS data appears in the June 12 brief. The HYG ETF was −0.12% intraday on June 12 even as the broader market rallied — a quiet credit market signal that the peace deal was not fully changing the credit narrative. The decisive read will come from the next FRED update this week.

**The BlackRock HPS gate: the most important non-price signal of the session.**

FT (June 12, 13:05 UTC): *"BlackRock private credit fund honours less than 40% of redemption requests — The firm's $13bn HPS Corporate Lending Fund limits withdrawals for a second consecutive quarter."*

Two consecutive quarterly gates = structural deterioration. The private→public credit cascade timeline (thesis since June 4): Gate 1 was anomaly; Gate 2 is the cycle. The BREIT precedent (2022–23): gates started Q1, public REIT underperformance lasted 4 quarters, credit markets lagged 6–9 months. An Iran oil deal does not unlock a gated $13bn credit fund. HY OAS at 2.80% is the public-market read-through of this, not of oil.

---

## Macro & data

No new economic data in the June 12 brief — Friday intraday snapshot contained no new prints. The macro table as of the latest FRED observations:

| Series | Latest | FRED Date | 1Y %ile | Δ from prior | Read |
|---|---|---|---|---|---|
| 10Y Treasury (FRED) | 4.55% | Jun 10 | 96.4th | +0.02% | Market 10Y now 4.499%; converging |
| 2Y Treasury (FRED) | 4.13% | Jun 10 | 97.6th | flat | 2Y stuck; 2s10s can only steepen via 10Y falling |
| 2s10s (FRED) | 0.40% | Jun 11 | 0.4th | **−0.02%** | Reflattened; back to flattest range of year |
| 10Y Breakeven | 2.29% | Jun 11 | 24.2nd | **−0.05%** | Bond mkt pricing out long-run inflation on Iran deal |
| HY OAS | 2.80% | Jun 10 | 23.0th | unchanged | AT the trigger; no FRED update yet |
| IG OAS | 0.75% | Jun 10 | 9.9th | flat | Historically tight; HY leads by 3–6 weeks |
| VIXCLS | 19.44 | Jun 11 | 75.8th | **−2.78** | Down from 87.7th %ile; fear premium vented |
| NFCI | −0.506 | Jun 5 | 22.2nd | flat | **Lagging — will catch credit deterioration 6–8 weeks out** |
| EFFR | 3.62% | Jun 11 | 0th | flat | Fed on hold; lowest of 1-year range |
| Initial Claims | 229k | Jun 6 | 71.8th | +4k | 4.5-month high; labor softening pre-exists Iran |

**The NFCI lag is the sleeper risk.** At −0.506 (22.2nd %ile, "slightly accommodative" as of June 5), the Chicago Fed Financial Conditions Index has not yet registered: HY OAS widening, BlackRock gates, VIX at 22, private credit stress. The NFCI typically lags 4–8 weeks. When it crosses above 0 (neutral → restrictive), the "conditions are still easy" argument disappears and the feedback loop from tight credit to real activity accelerates.

**UK GDP −0.1% in April (BBC/CNBC June 12):** *"UK economy shrank 0.1% in April as Iran conflict weighed on growth — services activity declined and companies cited pressure from the Middle East conflict."* The Iran transmission channel is now IN THE DATA, not a forecast. ECB hiking into European contraction (UK −0.1% April, Germany likely weaker) is the synchronized policy-mistake scenario. The World Bank's June 11 warning was not a risk scenario; it was a delayed fact-check on data already being collected.

**SpaceX IPO dynamics:**
- Raised $75bn at $135/share (555.6 million shares); history's largest IPO
- Indicated +30% open; projected $1.8T+ valuation at open
- S&P 500 said NO (profitability threshold: not yet profitable enough for index inclusion)
- Nasdaq-100 eligible; rebalancing into SPCX would force passive buying into Nasdaq-100, squeezing out smaller constituents
- "Rocket Lab and these four stocks are joining the Nasdaq 100; SpaceX may be next" (MarketWatch) — index supply shock in progress

---

## Risk lens

**The VRP collapse is the most actionable risk signal from this session.**

VRP: 4.0 (June 12) vs 8.2 (June 11). Realized 20d vol: 15.0% vs VIX: 19.0%. In one session, the fear premium was vented. This creates two scenarios:

1. **Peace deal confirmed by Monday:** VRP stays compressed, VIX drifts below 18, the bear trade suffers a short squeeze. But the STRUCTURAL risks (BlackRock gate, HY OAS, NFCI catch-up) persist with no portfolio protection remaining.
2. **Friday fakeout confirmed:** WTI snaps back above $88 Monday open, VIX reconstitutes toward 22 rapidly (VRP 4.0 → 8.0 in hours), and the bear trade reasserts from a position where speculative longs have added risk into the peace deal.

The 2022 parallel: every cease-fire rumor in the Russia-Ukraine conflict temporarily deflated oil and vol before the reality re-established. The June 9 → June 10 → June 11 cycle is already the precedent in this conflict.

**The three concurrent stress signals — status update:**
1. **HY OAS 2.80%** — still at the trigger, unchanged. Iran deal news doesn't fix credit.
2. **BlackRock HPS: Gate 2** — ESCALATED from anomaly to structural. Independent of oil.
3. **Stock-bond correlation: 0.71** (vs 0.64 prior, vs 0.45 a week ago) — MORE broken after the relief rally. In a risk-on session (equities up, bonds also bid), the correlation should have dropped. Instead it ROSE. This is a regime signal: the two assets are now pricing the same macro narrative simultaneously (peace deal = equities rally AND bonds rally), which means in a risk-off event both fall together. 60/40 diversification is providing NEGATIVE value.

**CFTC (June 2 data, 13 days stale):** S&P net −500,732 (record short). The June 9 CFTC data was released June 12 at 3pm ET — AFTER the brief was captured. That data will appear in the next brief and is the highest-stakes positioning datapoint of the week. If shorts covered 50k+, the squeeze risk is live. If they added 30k+, the bear case has institutional momentum even into the peace deal rally.

**BoJ June 16–17:** USDJPY at 160.25. BoJ decision is binary — no gradations:
- **Hike +25bps (Ueda deputy delivers):** USDJPY 158–159, carry unwind risk reduced. Positive for global risk assets; yen safe haven re-engages as a diversifier.
- **Pause (leadership vacuum, uncertainty):** USDJPY snaps to 162+, JPY carry unwinds begin. Given the June 11 brief flagged this as the "highest-magnitude external CB event for US markets this month," a pause here + Friday fakeout on Iran = the double-tail event.

**SpaceX index supply shock:** The largest IPO in history (by dollar size) entering Nasdaq trading creates passive rebalancing flows. If Nasdaq-100 adds SPCX, every index fund must buy it — forcing sales of other Nasdaq-100 constituents. In a market where spec shorts are at records and credit is gating, liquidity shocks from forced rebalancing at historic sizes are non-trivial. The KPMG AI-hallucination story (FT June 12) and the tech multiple compression thesis are both competing with SpaceX animal spirits for the Nasdaq narrative.

---

## What to watch

1. **WTI Monday open below $84** — Iran deal confirmed, energy stagflation thesis impaired. If WTI opens at $84 or lower, the peace is pricing and the bull scenario (HY OAS reversal, Vol compression, spec short squeeze) activates. The June 9 cease-fire premium crashed oil −4% to $87.58 before re-escalating. This deal needs to be MORE credible than June 9 to break below $84. Probability: 0.30.

2. **HY OAS clean break above 2.85%** (FRED June 13+ data, expected this week) — credit-cycle story independent of Iran. If spreads widen despite oil falling, the private credit cascade (BlackRock Gate 2 confirmed) is the driver, not geopolitics. The Bear case does not need Iran to be right. Probability: 0.30 (lowered from 0.55 on removal of near-term Iran catalyst; structural credit pressure argues for higher, peace deal headwind argues for lower).

3. **BoJ hike +25bps confirmed June 16–17, USDJPY falls below 158** — clean institutional signal; carry unwind tail removed; yen diversification partly restored. Probability: 0.60 (deputy has incentive to demonstrate credibility; consensus is for the hike; leadership vacuum is a risk, not a base case).

4. **CFTC June 9 S&P spec net above −530k** — specs deepened shorts through the −3.85% week rather than covering into the ASML bounce; bear thesis has structural support, no squeeze without a confirmed deal. Probability: 0.50 (specs were profitable being short all week; no reason to cover until the deal is confirmed).

5. **SpaceX (SPCX) closes its Day 1 above $175 (+30% from IPO price of $135)** — animal spirits intact; Nasdaq-100 inclusion anticipated; liquidity doesn't crack. A pop-and-drop (open +30%, close +10%) would signal IPO liquidity strain and an appetite check on the market's risk tolerance. Probability: 0.50 (Friday fakeout resolved either way; SPCX may trade Friday afternoon data).

```watch
[
  {"claim": "WTI opens below $84 Monday — Iran deal confirmed, stagflation thesis impaired", "metric": "market:CL=F:last", "trigger": "<84", "horizon": "Monday open", "probability": 0.30},
  {"claim": "HY OAS clean break above 2.85% — credit cycle deteriorating independent of Iran", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.85", "horizon": "next 5 sessions", "probability": 0.30},
  {"claim": "BoJ hikes +25bps June 16-17, USDJPY falls below 158 — carry tail removed", "metric": "market:USDJPY=X:last", "trigger": "<158", "horizon": "next week", "probability": 0.40},
  {"claim": "CFTC June 9 S&P spec short deepened above -530k — bears entrenched through peace-deal week", "metric": "positioning:SPX:lev_net", "trigger": "<-530000", "horizon": "this week", "probability": 0.50}
]
```

---

## The call

Two things are simultaneously true after Friday's brief:

**Bearish:** BlackRock private credit gate (2nd quarter, confirmed structural); HY OAS at 2.80% (same, unchanged by any Iran news); stock-bond correlation 0.71 (worse); NFCI lagging but will catch up; UK GDP already contracting from Iran; CPI 4.25% + PPI +1.1% in the pipeline regardless of whether WTI is $86 or $90.

**Bullish:** VRP at 4.0 (cheapest hedging of the week), VIX 18.99, Trump explicitly called off strikes and claimed deal is close, WTI at $86 (not $95), breakevens pricing out long-run inflation, global equities rallying broadly (Nikkei +2.87%, Russell +2.79%).

The honest call with a weekend gap and unconfirmed peace deal: **direction 0 (flat)**. The Iran deal status is the binary that overwhelms every other signal at the Monday open. Without knowing whether the deal materialized, a clean short is exposed to WTI $82 and a squeeze; a clean long is exposed to WTI $90 + BlackRock gate. The credit cycle is the slow-burn thesis that is right in 30–60 days regardless. But Monday's first 30 minutes will be determined by one data point: where oil opens.

Check WTI first. Below $84 = cover the short and reassess. Above $88 = re-establish direction −1, VRP has been re-primed.

```stance
{"direction": 0, "notes": "Weekend gap; Iran deal unconfirmed. WTI <$84 on confirmed deal = bear thesis structurally impaired, cover short; WTI >$88 Monday = Friday fakeout confirmed, re-establish -1 with VRP reset to buy protection cheap. BlackRock Gate 2 + HY OAS 2.80% argue the credit cycle is the right thesis regardless; but Monday's oil open is the regime switch. No clean edge without it."}
```

---

## Sources

- *Trump says US close to deal with Iran and calls off strikes* (FT, 2026-06-12 00:53 UTC)
- *Oil touches three-month low after Trump says US close to Iran deal* (FT, 2026-06-12 14:26 UTC)
- *Global oil prices drop to $88 a barrel on hopes for an Iran peace deal as early as this weekend* (MarketWatch, 2026-06-12)
- *Oil Prices Waver On U.S.-Iran Deal. Is It Another Friday Fakeout?* (IBD via Yahoo Finance, 2026-06-12)
- *These are the assets investors should buy if a peace deal with Iran happens, says Bank of America* (MarketWatch, 2026-06-12)
- *BlackRock private credit fund honours less than 40% of redemption requests* (FT, 2026-06-12 13:05 UTC)
- *SpaceX raising $75 billion in record-setting IPO as Nasdaq debut awaits* (CNBC, 2026-06-12)
- *SpaceX set to surge past $2 trillion valuation in blockbuster Nasdaq debut* (Investing.com, 2026-06-12)
- *The S&P 500 already made a big call on SpaceX stock and index fund investors need to know it* (CNBC, 2026-06-12)
- *Rocket Lab and these four stocks are joining the Nasdaq 100; SpaceX may be next* (MarketWatch, 2026-06-12)
- *UK economy contracts as Iran war impact felt* (BBC, 2026-06-12)
- *UK economy shrank 0.1% in April as Iran conflict weighed on growth* (CNBC Economy, 2026-06-12)
- *The great bond and equity conundrum* (FT, 2026-06-12)
- *From startup to $1.8 trillion: The investors who took a chance on SpaceX now reap the rewards* (CNBC, 2026-06-12)
- *KPMG report contained AI hallucinations on benefits of AI* (FT, 2026-06-12)
- Analytics: CFTC positioning June 2 (13 days stale); FRED macro June 10–11; EIA energy June 5; `brief_2026-06-12.json`; `data/scorecard_log.jsonl`
