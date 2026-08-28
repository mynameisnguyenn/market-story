# Market Story — 2026-08-28

> *Brief: `brief_2026-08-27.json` (captured 2026-08-27 21:37 UTC — US close). Previous brief: `brief_2026-08-26.json` (premarket capture). Prior narrative: `narrative_2026-08-27.md`. FRED vintage: DGS10 4.66% (Aug 26), HY OAS 2.67% (Aug 26, 3.2nd %ile, THIRD consecutive). CFTC: Aug 18 vintage unchanged. EIA: Aug 21 vintage. Note: Warsh's Jackson Hole address is scheduled Friday Aug 28 — not captured in the Aug 27 brief. Two hawkish JH speeches (Hammack, Schmid) were captured.*

---

## Since last time

Grading `narrative_2026-08-27.md` watch items against `brief_2026-08-27.json`:

| # | Claim | Trigger | Result |
|---|---|---|---|
| 1 | Nvidia first print above $220 post-earnings fires Nasdaq −61k squeeze | `market:NVDA:last >220.0`, horizon 2026-08-27 | **HIT** — NVDA $228.0 (+8.74%). Best post-earnings session in 2 years (MarketWatch). The prior protocol (flip to +1 on NVDA >$220 AH) triggered. P=0.38 → actual far exceeded expectation. |
| 2 | WTI closes below $80 — Iran-Oman deal eliminates remaining risk premium | `market:CL=F:last <80.0`, horizon 2026-08-27 | **MISS** — WTI $83.54 (+1.59%). TACO pattern confirmed once more: the Oman mediation headlines evaporated within the session, WTI reversed all of Aug 26's decline and added more. Iran-Oman channel closed; Trump "Lake America" executive order (FT) signals continued geopolitical noise. |
| 3 | HY OAS third consecutive ≤2.69% — TGA arrest durable through Nvidia binary | `macro:BAMLH0A0HYM2 <=2.69`, horizon 2026-08-29 | **HIT** — HY OAS 2.67% (3.2nd %ile, FRED Aug 26 vintage). THIRD consecutive print below 2.70% gate. The TGA arrest thesis is confirmed durable. P=0.42. |
| 4 | 10Y market breaks below 4.55% on Warsh JH dovish acknowledgment | `market:^TNX:last <4.55`, horizon 2026-08-28 | **MISS** — market 10Y 4.672%. Warsh hasn't spoken yet (scheduled Aug 28). Two hawkish JH officials (Hammack: "time to act on raising rates"; Schmid: policy "not restrictive") set the tone. P=0.22 — skepticism warranted. |
| 5 | Gold through $4,750 — fiscal dominance QE path priced in | `market:GC=F:last >4750.0`, horizon 2026-08-29 | **MISS/PENDING** — Gold $4,655 (+1.23%). Rising but $95 from trigger. P=0.35. |

**Prior session VIX >18 (0/6 streak):** VIX 14.51 on NVDA earnings day — CONFIRMED MISS #7 on VIX timing. Recalibration to ≥20 continues.

**Running hit-rate: ~74/184 (40.2%)** — 2 new hits (NVDA, HY OAS), 3 new misses (WTI, 10Y, Gold). Credit calls improving (TGA thesis: 6/12). NVDA calls improving (1/1 post-protocol clarification). Gold directional: 5/8, still the most reliable sustained signal.

---

## Today in one line

**Nvidia beat-and-held above $220 exactly as the protocol predicted ($228, +8.74%), confirming the AI thesis for enterprise software too (CRM +22.58%), but 10-of-11 sectors were red simultaneously — the S&P gained 0.72% on the strength of two earnings prints while the rest of the market quietly de-risked ahead of Warsh at Jackson Hole today; the flip to a genuine broad bull requires Warsh to match PCE 3.3% with anything softer than Hammack's "time to act on raising rates."**

*Flip to +1 (conviction):* Warsh at JH matches PCE 3.3% with any dovish acknowledgment (trend language, labor softness, "watchful" framing) → 10Y falls below 4.55%, duration squeeze begins, S&P 7,800+.  
*Flip to −1 (bear re-entry):* Warsh validates Hammack/Schmid hawkish framing (inflation "stubborn," policy "not restrictive," implies further hikes) → 10Y through 4.75% on WTI re-acceleration; VIX 14.51 at 11.1th %ile = extreme complacency unwind; S&P 7,450–7,550.

---

## TL;DR

- **The NVDA squeeze fired on cue, but breadth was the worst "up day" structure of the cycle: 1-of-11 sectors advancing.** S&P +0.72% was entirely carried by XLK +3.16%. The other 10 sectors averaged roughly −0.9%. The S&P is up; the market is not. When a single earnings print drives the index, the durability of the move depends entirely on the catalyst sustaining.

- **HY OAS 2.67% (3.2nd %ile) is the third consecutive print below 2.70% — the TGA thesis is formally confirmed.** Bessent's $950bn TGA operations have now held the credit floor through three FRED vintages, through the Nvidia binary, through WTI's reversal, and through two hawkish Jackson Hole speeches. Private credit lag clock is now Day 11–12 of the 20–40 day window; if HY OAS holds ≤2.69% through next week, the propagation window is effectively closed.

- **Warsh is the market today.** Two of his colleagues went hawkish at JH yesterday (Hammack: "now is the time to act" on raising rates; Schmid: inflation "stubborn and sticky," policy rate "not restrictive"). VIX at 14.51 (11.1th %ile) = maximum complacency. If Warsh even half-validates Hammack's framing, the move is asymmetric: VIX shorts (−19,093), duration shorts (Ultra T-Bond −861k), and a narrow-breadth S&P at all-time territory are all simultaneously vulnerable to covering.

---

## What moved & why

### Equities & sectors

**Session structure: post-NVDA-earnings open, two simultaneous enterprise-software beats, one of the narrowest "bull" sessions of the cycle.**

**XLK Technology +3.16% — the entire story.** Nvidia +8.74% to $228 is the pivot event: this is "best post-earnings-report session in 2 years" (MarketWatch) and directly falsifies the "5-of-5 beats-and-dips" structural pattern that dominated prior semiconductor earnings. NVDA opened above $220, held above $220 through the session, and closed at $228 — the squeeze trigger is confirmed. The Nasdaq closed sharply higher on the earnings catalyst (MarketWatch bulletin, 20:01 UTC). But NVDA alone doesn't explain XLK +3.16%; **CRM +22.58% to $252.05** is the second driver. Salesforce beat consensus by a wide margin and the enterprise software complex ripped: ServiceNow +10% (Seeking Alpha, 21:18 UTC), Synopsys +13% (21:08 UTC), Affirm +8% (21:10 UTC). The AI-to-enterprise-software transmission is working: NVDA confirms the infrastructure spend, CRM/NOW confirm the software monetization layer above it. This is the bull case's strongest internal confirmation of the cycle.

**10-of-11 sectors declined — a critical breadth warning.** XLP Consumer Staples −1.38%, XLV Health Care −1.13%, XLY Cons Discretionary −1.09%, XLC Comm Services −1.07%, XLI Industrials −0.85%. These declines aren't noise — they represent defensive and cyclical names de-risking ahead of Warsh. When 10 of 11 sectors sell while the index gains, the index gain is a mirage: NVDA and CRM are so large (via XLK's weight) that they overpower genuine risk-off positioning in the rest of the tape. The options market piece in MarketWatch (21:31 UTC) flagging "buy signals" for a surge is the sentiment framing — but the breadth data underneath it is the more honest signal.

**Notable divergence within watchlist:** NVDA +8.74%, MSFT +1.75%, TSM +2.30% — semis and cloud advancing. AMZN −1.54%, NFLX −1.99%, V −1.10%, MA −1.13%, GOOGL −0.39%, META −0.87% — platform and payment names quietly leaking. This is a continuation of the "AI infrastructure wins, everything else leaks" thesis. The Anthropic MatX deal collapse (Investing.com, 21:24 UTC — Anthropic planned then abandoned $7bn MatX purchase) is a footnote but signals that even within AI, M&A integration is messier than headlines suggest.

**Global: mixed without a consistent read.** DAX +0.31%, Nikkei +0.62%, Hang Seng +0.56% — Asia and Germany tracked the NVDA beat. CAC 40 −1.68%, Euro Stoxx −0.71%, FTSE −0.79% — Europe's negative session preceded the NVDA close and reflects the Hammack/Schmid hawkish tone at JH. The divergence within global is Warsh-expectation pricing, not a fundamental split.

### Rates & the dollar

**Cross-asset delta table (Aug 26 brief → Aug 27 brief):**

| Metric | Aug 26 Brief | Aug 27 Brief | Δ | 1Y Pct |
|---|---|---|---|---|
| **FRED DGS10** | 4.70% (Aug 24 vintage) | **4.66%** (Aug 26 vintage) | **−4bps** | 92.5th %ile |
| **FRED DGS2** | 4.24% (Aug 24 vintage) | **4.19%** (Aug 26 vintage) | **−5bps** | 87.7th %ile |
| **2s10s (T10Y2Y)** | 0.47% | **0.47%** (flat) | 0 | 21.4th %ile |
| **T10Y3M** | 0.78% | **0.83%** (+5bps) | **WIDER** | 94.0th %ile |
| **BEI** | 2.32% | **2.33%** (+1bp) | slight uptick | 56.3th %ile |
| **HY OAS** | 2.69% | **2.67%** (−2bps) | **3rd below gate** | **3.2nd %ile** |
| IG OAS | 0.81% | **0.80%** (−1bp) | tighter | 58.3th %ile |
| **VIXCLS** | 15.85 | **15.21** (−0.64) | −4.0% | 11.1th %ile |
| **Market 10Y** | 4.631% | **4.672%** | **+4bps** | ~91st %ile |
| **Market 30Y** | 5.166% | **5.191%** | **+2.5bps** | elevated |
| **Market 5Y** | 4.339% | **4.396%** | **+5.7bps** | elevated |
| **DXY** | 98.984 | **99.119** | **+0.14%** | ~50th %ile |
| **WTI** | $80.29 | **$83.54** | **+$3.25 (+4.1%)** | rebounding |
| **Gold** | ~$4,674 | **$4,655** | **−$19 (−0.4%)** | 75th %ile |
| **Copper** | ~$6.79 | **$6.69** | **−0.10 (−1.5%)** | elevated |

**Three reads from the delta table:**

1. **FRED yields fell (DGS10 −4bps, DGS2 −5bps), market yields rose (+4bps 10Y, +5.7bps 5Y).** This is the FRED vintage lag: the Aug 26 FRED data captured Monday/Tuesday's rate-relief on PCE 3.3%, while Thursday's market session (Aug 27) reversed some of that relief — consistent with Hammack and Schmid's hawkish JH framing spooking the long end slightly. The result: market 10Y at 4.672% is above FRED's 4.66% (Aug 26), meaning today the rate-relief from PCE hasn't stuck at the market level despite the credit-data confirmation. The FRED data is looking backward at the soft print; the market is looking forward at Warsh.

2. **BEI ticked up to 2.33% (+1bp) on an NVDA earnings day, while WTI reversed +4.1% to $83.54.** The BEI uptick is small but directionally significant: the market is pricing slightly MORE inflation expectations the morning after a massive tech earnings beat. This makes sense if WTI's reversal (Iran-Oman deal dead; TACO #16 confirmed) is flowing into breakevens. The "missing link" in the bull case — BEI falling toward 2.20%–2.25% — remains missing. BEI is moving the wrong direction for the duration squeeze narrative.

3. **2s10s flat at 0.47% (21.4th %ile) while T10Y3M widened to 0.83% (94.0th %ile).** The curve shape is unchanged even on a tech-rip day. The 10Y-3M spread at the 94th %ile means the longer-dated term premium is elevated while the front-end (held by Warsh's 3.63% EFFR) remains anchored. This is the structural backdrop for Warsh's speech: whether he signals any movement in the front end determines whether 2s10s steepens (bull) or the long end bears-steepens (stagflation tail).

**Dollar essentially unchanged at 99.12 (DXY)**, USD/JPY 159.36 (+0.09%). No meaningful FX reaction to NVDA earnings — the dollar is a Warsh spectator at this point, oscillating around 99.

### Commodities & credit

**WTI +1.59% to $83.54, Brent +0.82% to $88.56 — TACO pattern confirmed for the 16th time this cycle.** The Iran-Oman temporary Hormuz deal framework that drove WTI to $80.29 on Aug 26 collapsed within 24 hours. Trump's "Lake America" executive order (FT, 20:34 UTC) signaling deteriorating US-Canada relations is an unrelated headline but underscores the geopolitical noise backdrop. The formal watch gate ($80) is no longer in play — WTI is $3.54 above it. The August PCE (one-month lag from July's oil levels) was already the disinflation case; the September PCE will now reflect August's oil averaging closer to $83–85, which reduces the disinflation pipeline.

**Gold $4,655 (+1.23%), Silver $70.07 (+3.05%)** — the metals bid is intact. Gold's +1.23% on a tech-rip day, WTI-reversal day is the clearest expression of the dual-driver regime: gold is not tracking oil (geopolitical risk premium) but rather fiscal debasement (Bessent $950bn TGA). With WTI rising and gold rising simultaneously, the disinflation thesis takes a hit while the fiscal-dominance premium stays bid. Silver's +3.05% is the industrial-meets-monetary metals move; copper also +1.48%. The broad metals bid suggests real-asset demand is broadening.

**HYG −0.04%, LQD −0.05%, TLT −0.20%** — credit and duration quietly offered on the session. The FRED HY OAS printing 2.67% is the third consecutive gate confirmation, but the market HYG price was flat-to-negative even on a tech-rip S&P day. This is a subtle but important divergence: the TGA-suppressed FRED spread is one data point; the actual HYG market price action suggests marginal credit buyers are not aggressive. Duration (TLT −0.20%) is slightly offered ahead of Warsh — the risk is that Warsh validates the hawkish JH tone and TLT accelerates lower.

**EIA (Aug 21 vintage):** Crude ex-SPR +95 MBBL (tiny build — essentially flat); Gasoline −2,536 MBBL (seasonal draw); Distillate −2,228 MBBL (draw); SPR −3,700 MBBL (continuing draw — Bessent's SPR release channel remains active). The inventory picture: crude essentially flat, products drawing, SPR releasing. WTI's reversal from $80 to $83 is geopolitical (not supply shock), and the SPR release is providing a mild cap — but Bessent would need much larger SPR releases to counter an Iran-driven spike.

---

## Macro & data

**FRED (Aug 26 vintage — most recent):**
- 10Y: **4.66% (92.5th %ile, −4bps from 4.70% Aug 24)** — pulled back on PCE 3.3% but now facing Warsh upward pressure in market rates
- 2Y: **4.19% (87.7th %ile, −5bps)** — the first meaningful front-end relief of the cycle; PCE 3.3% shifted short-end pricing marginally dovish; Warsh holds 3.63% EFFR, so this move is fragile
- 2s10s: **0.47% (21.4th %ile, flat)** — curve unchanged; no steepening despite tech rip; Warsh is the next catalyst
- T10Y3M: **0.83% (94.0th %ile, +2bps)** — the long-over-short spread remains historically wide; recession/slowdown premium in the long end
- BEI: **2.33% (56.3th %ile, +1bp)** — slight uptick; WTI reversal and gold strength are flowing into breakevens; the disinflation-via-energy channel is closing
- **HY OAS: 2.67% (3.2nd %ile, −2bps, THIRD CONSECUTIVE below gate)** — the TGA arrest thesis is confirmed. Day 11–12 of the 20–40-day private credit propagation window; if HY OAS prints below 2.69% in next week's FRED vintages, the propagation window is closed without contagion
- IG OAS: **0.80% (58.3th %ile, −1bp)** — tighter; investment-grade not showing stress
- NFCI: **−0.566 (1.6th %ile, Aug 21 vintage)** — historically loose public financial conditions; structural divergence from private credit lag (Day 11–12) persists
- VIXCLS: **15.21 (11.1th %ile)** — extreme complacency; VIX fell after NVDA resolved, but Warsh is today's live binary; VIX at 11.1th %ile entering a Fed chair speech with two hawkish colleagues who preceded him = asymmetric vol risk
- EFFR: **3.63% (unchanged)** — Warsh's rate; any signal of change here is the macro event of the year

**BLS (July vintage — unchanged):**
- CPI-U YoY: 3.364% | Core CPI: 2.478% | NFP: −23,000 (July) | Unemployment: 4.1% (down from 4.2%) | AHE YoY: 3.15% | LFP: 61.4%
- **Initial claims (Aug 22 vintage): 203,000 (7.5th %ile, −4,000 from 207k)** — labor market tightening marginally; claims below 210k = no distress signal yet despite NFP −23k

**Fed speakers at Jackson Hole (Aug 27 — captured in brief):**
- **Fed's Hammack (CNBC, 17:31 UTC): "now is the time to act" on raising interest rates** — the most hawkish JH statement of the cycle; Hammack is voting member; this is not a dissent, it is a public call for hikes while PCE is at 3.3% (130bps above target)
- **Kansas City Fed's Schmid (CNBC, 14:11 UTC): inflation "stubborn and sticky," policy rate "not restrictive"** — same message from a different angle; the JH pre-Warsh tone is: two officials believe current 3.63% EFFR is not restrictive enough
- **Warsh's speech is scheduled for Friday Aug 28 — not yet in the brief.** His framing: the history of Jackson Hole speeches suggests market-moving framework addresses (MarketWatch, 18:31/19:35 UTC). The CNBC preview (21:03 UTC) frames his as the key speech. After Hammack/Schmid, the market bar for "hawkish" is already set high; Warsh needs to either match or significantly soften relative to his colleagues.

**FT: "Don't draw the wrong conclusion from Treasury yields" (14:45 UTC)** — FT's framing is that investors are marking up expectations for long-run economic growth, not just inflation. This is the bull interpretation of elevated real yields: growth premium, not fear premium. Worth filing as a counterweight to the structural bearish read on 4.66% 10Y.

---

## Risk lens

**1. Warsh's JH address today is the single most important near-term catalyst — and he's walking into a hawkish trap set by his own colleagues.**

Hammack said "time to act" on rate hikes. Schmid said the rate "not restrictive." If Warsh agrees, the market has a hawkish surprise on top of a narrowly-supported S&P at all-time territory, with VIX at 14.51 (11.1th %ile). The mechanical setup: VIX shorts at −19,093, Ultra T-Bond shorts at −861,357, and a Nasdaq that just partially covered (from −89k to −62k) but still has significant residual short exposure. A hawkish Warsh is not just a rate catalyst — it fires covering that amplifies the bond selloff (shorts cover → rates rise → equity multiples compress → equity shorts forced to cover at worse levels). The asymmetry: a dovish Warsh is already partially priced (VIX complacency, credit at 3.2nd %ile). A hawkish Warsh is NOT priced, because nobody expected Hammack to say "time to act on raising rates" and still have the S&P near all-time highs.

**2. The breadth problem: 1/11 sectors advancing on a +0.72% day is not a bull market signal.**

The S&P is above 7,730 because NVDA (market cap ~$5.5tn) and CRM added hundreds of billions in one session. The equal-weighted S&P would have been significantly negative. The XLP −1.38%, XLV −1.13%, XLY −1.09% declines are consistent with risk-off positioning ahead of Warsh, not a general bull cycle. The "buy signal" from options markets (MarketWatch, 21:31 UTC) is a near-ATH momentum framing; the breadth data beneath it is a warning that the index-level rally is unsupported by broad participation. The S&P 500's YTD is +12.9%, but 9 of 11 sectors are lagging that return significantly — only XLK (+31.3% YTD) and XLE (+41.2% YTD) are leading.

**3. WTI TACO is now the permanent constraint on the disinflation argument.**

WTI has reversed every "deal" within 24–48 hours for 16 documented episodes. At $83.54, oil is $3.54 above the $80 formal gate and $5.54 above the $78 maximum gate. The September PCE (reported ~Oct 31) will reflect August oil at $82–85 average — materially higher than July's $80 range. Even if Warsh acknowledges PCE 3.3% as progress, the oil reversal means August PCE may not continue the disinflation trend. Warsh needs to weigh the trend (3 months of deceleration: 3.6% → 3.4% → 3.3%) against the level (still 130bps above target) in an environment where energy is re-accelerating.

**4. Private credit lag clock: Day 11–12 of 20–40 window — TGA thesis holding but not yet cleared.**

Three FRED HY OAS prints below 2.70% (2.69%, 2.69%, 2.67%) confirm the TGA arrest is durable through the first half of the propagation window. The BlackRock HPS / Blue Owl Aug 17 gates had a 20–40-day lag. We're at Day 11–12. The second half of the window (Days 13–20+) is the higher-risk period if the gates represent genuine portfolio stress rather than operational friction. The next FRED vintage (Aug 27 data, due Aug 28–29) is the critical test: if HY OAS prints at 2.67% or tighter again, the propagation window is closing without contagion. If the next print widens to ≥2.73%, the lag is printing through regardless of TGA suppression level.

**5. CFTC Aug 25 vintage due today (Friday Aug 29) — first post-Nvidia data, most important positioning read of the cycle.**

The Aug 27 brief still carries the Aug 18 CFTC data (Nasdaq −61,771, VIX −19,093, Ultra T-Bond −861,357). The Aug 25 CFTC vintage will reveal: (a) whether the Nasdaq short was force-covered after NVDA's AH beat (a dramatic cover to −30k or lower fires the squeeze narrative retroactively); (b) whether VIX shorts were added or reduced ahead of Warsh; (c) whether the Ultra T-Bond short deepened through PCE week or began covering. This data determines whether today's bull narrative has mechanical support or is running on thin short-covering.

**What to watch next (3–5 numeric triggers):**

1. **Warsh at Jackson Hole (Friday Aug 28 — live event):** dovish framing ("PCE trend encouraging," "watchful," "labor softening") → 10Y falls below 4.55%, VIX covers, flip to +1. Hawkish framing (validates Hammack/Schmid: inflation "stubborn," policy "not restrictive," hints at hike) → 10Y through 4.75%, VIX expansion, S&P 7,450–7,550 retest.

2. **HY OAS next FRED vintage (Aug 27–28 data, due Aug 28–29):** fourth consecutive ≤2.69% closes the private credit lag window. A print ≥2.73% after three consecutive below-gate prints would be the most significant single credit data point of the cycle — confirms lag is printing through.

3. **CFTC Aug 25 vintage (due today):** Nasdaq short covering from −61k → −35k or below = squeeze narrative confirmed post-NVDA. Bears adding back → structural short intact, Warsh risk is amplified. Ultra T-Bond short change from −861k → any covering = duration squeeze begins.

4. **S&P breadth Friday:** if Warsh is dovish, watch whether 10-of-11 sector pattern reverses to 8+/11. Breadth staying narrow (≤3 sectors advancing) on any S&P gain would be the clearest regime fragility signal.

5. **10Y yield response to Warsh:** break below 4.55% → duration squeeze underway, +1 protocol active. Hold above 4.70% on hawkish Warsh → 30Y pressure through 5.20%, term premium spike.

```watch
[
  {"claim": "Warsh dovish: 10Y breaks below 4.55% during/after JH speech", "metric": "market:^TNX:last", "trigger": "<4.55", "horizon": "2026-08-28", "probability": 0.25},
  {"claim": "HY OAS fourth consecutive ≤2.69% — private credit lag window closing", "metric": "macro:BAMLH0A0HYM2", "trigger": "<=2.69", "horizon": "2026-08-29", "probability": 0.55},
  {"claim": "HY OAS widens ≥2.73% — lag propagating through TGA suppression", "metric": "macro:BAMLH0A0HYM2", "trigger": ">=2.73", "horizon": "2026-08-29", "probability": 0.12},
  {"claim": "VIX spikes above 18 on hawkish Warsh — complacency unwind begins", "metric": "market:^VIX:last", "trigger": ">18.0", "horizon": "2026-08-28", "probability": 0.28},
  {"claim": "Gold through $4,750 — fiscal dominance bid accelerates post-Warsh", "metric": "market:GC=F:last", "trigger": ">4750.0", "horizon": "2026-09-04", "probability": 0.30}
]
```

---

## The call

**Direction: 0 (flat) — maintained, pending Warsh.**

The prior protocol was clear: flip to +1 on confirmation of NVDA >$220 AH. That confirmation is now in the brief ($228, +8.74%). But the protocol also required "any Warsh dovish acknowledgment at JH" — and Warsh has not yet spoken. Two of his colleagues (Hammack, Schmid) went explicitly hawkish. Entering +1 before Warsh speaks repeats the Jul 9 lesson — entering directional on a known binary morning has been the cycle's most systematic mistake.

The structural asymmetry today: the bull case (NVDA confirmed + Warsh soft) is partially priced (VIX at 11.1th %ile, HY OAS at 3.2nd %ile). The bear case (NVDA confirmed but Warsh hawkish) is NOT priced — the market is sitting at a narrow-breadth all-time-territory level with maximum complacency. Flat is the only honest answer until Warsh resolves.

If Warsh is dovish (within today's session): flip to +1 at next session open; the three-gate alignment (PCE ✓, HY OAS ✓ x3, NFP ✓) supports the S&P 7,800–7,900 target.  
If Warsh is hawkish (validates Hammack/Schmid): flip to −1; VIX at 14.51 unwinds toward 18–20; S&P 7,400–7,550 retest. The WTI reversal ($83.54) and hawkish JH tone would simultaneously close the disinflation + dovish-Fed gate combination — the bear thesis returns with the strongest multi-signal confirmation since early July.

Running hit-rate: **~74/184 (40.2%)**. Credit calls: 6/12 (improving, TGA thesis holding). Gold directional: 5/8 (most reliable sustained signal). VIX timing: 0/7 (recalibrating; trigger now ≥20). Oil direction: retired post-TACO pattern.

```stance
{"direction": 0, "notes": "Flat pending Warsh JH address (Aug 28). NVDA >$220 flip trigger confirmed ($228, +8.74%), but Warsh hawkish/dovish framing is the remaining macro gate. Two hawkish officials preceded him (Hammack: raise rates; Schmid: not restrictive). VIX 14.51 (11.1th %ile) = maximum complacency entering the speech. Flip protocol: +1 if Warsh soft-acknowledges PCE trend (S&P 7,800–7,900); -1 if Warsh validates Hammack framing (S&P 7,400–7,550). HY OAS: 2.67% x3 = TGA thesis confirmed. WTI TACO #16 confirmed ($83.54, gate missed). Running: 74/184 (40.2%). S&P 7,731 at close."}
```

---

## Sources

- *Nasdaq closes sharply higher as Nvidia earnings trigger tech-fueled stock rally* (MarketWatch Bulletins, 2026-08-27T20:01:52 UTC)
- *Nvidia is having its best post-earnings-report session in 2 years — follow live* (MarketWatch Bulletins, 2026-08-27T13:51:43 UTC)
- *Stocks making the biggest moves midday: Nvidia, Okta, Hormel, Veeva, HP, Celsius, Best Buy & more* (CNBC Finance, 2026-08-27T20:09:44 UTC)
- *ServiceNow gains 10% amid enterprise software rally* (Seeking Alpha, 2026-08-27T21:18:28 UTC)
- *Synopsys rises 13%, boosted by earnings* (Seeking Alpha, 2026-08-27T21:08:22 UTC)
- *Affirm posts trades higher after new co-president, Q4 earnings, healthy guidance* (Seeking Alpha, 2026-08-27T21:10:51 UTC)
- *Gap names new Old Navy CEO and lifts profit forecast, shares jump 14%* (Investing.com, 2026-08-27T21:18:29 UTC)
- *Fed Chairman Kevin Warsh delivers his key Jackson Hole speech Friday. Here's what to expect* (CNBC Finance, 2026-08-27T21:03:08 UTC)
- *How will stocks perform when the Fed chair speaks at Jackson Hole?* (MarketWatch, 2026-08-27T18:31:00 UTC / 19:35 UTC)
- *Fed's Hammack says 'now is the time to act' on raising interest rates* (CNBC Economy, 2026-08-27T17:31:09 UTC)
- *Kansas City Fed's Schmid says inflation 'stubborn' and 'sticky,' policy rate not restrictive* (CNBC Finance, 2026-08-27T14:11:29 UTC)
- *The S&P 500 is nearing a positive level — and the options market suggests a surge is likely* (MarketWatch, 2026-08-27T21:31:00 UTC)
- *Don't draw the wrong conclusion from Treasury yields* (FT International, 2026-08-27T14:45:47 UTC)
- *Bank of America doubles down on Nvidia stock* (Yahoo Finance, 2026-08-27T15:30:54 UTC)
- *Exclusive-Anthropic planned, then abandoned $7 billion purchase of MatX, sources say* (Investing.com, 2026-08-27T21:24:24 UTC)
- *Trump orders Lake Ontario to be renamed 'Lake America' in new slight to Canada* (FT International, 2026-08-27T20:34:30 UTC)
- *Marvell is boosting its forecasts, but that's not enough to lift its stock* (MarketWatch, 2026-08-27T21:12:00 UTC)
- *US bank regulators to narrow enforcement focus to financial risks* (FT International, 2026-08-27T19:50:02 UTC)
- *Citadel Securities hits record $7.3 billion revenue* (Investing.com, 2026-08-27T21:15:21 UTC)
- Analytics: `brief_2026-08-27.json` (21:37 UTC close data — S&P 7,731.0 (+0.72%), Nasdaq 26,541 (+1.57%), VIX 14.51 (−4.60%), XLK +3.16% (1/11 sectors advancing), NVDA +8.74% to $228.0, CRM +22.58% to $252.05; FRED Aug 26: **DGS10 4.66% (92.5th %ile)**, DGS2 4.19% (87.7th %ile), **HY OAS 2.67% (3.2nd %ile — THIRD consecutive below gate)**, IG OAS 0.80%, 2s10s 0.47% (21.4th %ile), T10Y3M 0.83% (94.0th %ile), BEI 2.33% (56.3th %ile, +1bp); Market: 10Y 4.672%, 30Y 5.191%, 5Y 4.396%; WTI $83.54 (+1.59%, TACO confirmed); Gold $4,655 (+1.23%); DXY 99.12; Initial claims 203k (7.5th %ile, −4k); CFTC Aug 18 unchanged: Nasdaq −61,771, Ultra T-Bond −861,357; Hammack: "raise rates"; Schmid: "not restrictive"; Warsh speech pending Aug 28.
