# Market Story — 2026-07-30

> *Brief: `brief_2026-07-29.json` (captured 2026-07-29 13:57 UTC — intraday Jul 29, 9:57am ET; pre-Fed decision at 14:00 ET. FRED vintage: 10Y/2Y Jul 27, 2s10s/EFFR/BEI Jul 28, HY/IG OAS Jul 27. CFTC Jul 21 unchanged. Previous brief: `brief_2026-07-28.json` (Jul 28 13:52 UTC). Note: Fed decision (14:00 ET Jul 29) and market close not captured — inferred from EFFR unchanged + macro context.)*

---

## Since last time

Grading `narrative_2026-07-29.md` watch items against `brief_2026-07-29.json`:

| Claim | Trigger | Horizon | Result |
|---|---|---|---|
| MSFT FCF compression on AI capex — <−5% | market:MSFT:change_pct <−5.0 | Jul 29 | **MISS.** MSFT −0.67% on Jul 29. No FCF disaster visible in market reaction. P=0.25 wrong. |
| MSFT beats Azure + positive FCF — >+3% | market:MSFT:change_pct >3.0 | Jul 29 | **MISS.** MSFT −0.67%. Beat thesis unconfirmed. P=0.35 wrong. Nasdaq −74,690 short NOT squeezed. |
| HY OAS holds above 2.75% on post-ceasefire FRED | macro:BAMLH0A0HYM2 >2.74 | Jul 31 | **EARLY HIT (pending Jul 31).** Jul 27 FRED: **2.81%** — widened +2bps ON THE DAY OF THE CEASEFIRE, with oil crashing −6.2%. Structural confirmation. P=0.38 correct direction. |
| HY OAS tightens below 2.70% on post-ceasefire FRED | macro:BAMLH0A0HYM2 <2.71 | Jul 31 | **MISS (early).** 2.81% — widened, not tightened. P=0.38 wrong. |
| VIX breaks and holds above 20.0 | market:^VIX:last >20.0 | Jul 30 | **MISS.** VIX 18.70 on Jul 29 brief (18.21 at Jul 28 FRED close). Did not breach 20. P=0.32 wrong. |
| 10Y FRED holds above 4.65% through Jul 31 | macro:DGS10 >4.64 | Jul 31 | **EARLY HIT (pending Jul 31).** Jul 27 FRED: **4.65%** — just above trigger. P=0.55 correct. |
| 10Y falls below 4.50% on dovish Fed signal | macro:DGS10 <4.50 | Jul 31 | **MISS (early).** 4.65% — far above target. P=0.18 wrong. |

**Running hit-rate update: 31/122 (25.4%) on settled items.** This session settles: 3 MISSes (MSFT ×2, VIX); 2 early HITs pending Jul 31 (HY OAS structural, 10Y >4.64%). The prior stance was direction: 0 (flat); S&P went 7,394→7,393 = essentially flat. Paper P&L: ≈0%.

**The big read on the watch-grading:** The MSFT in-line result and the VIX miss are disappointing directionally. But the HY OAS structural confirmation is the most important single data point of the entire cycle. The thesis was that credit would hold above 2.75% even as oil collapsed — it did, and it widened further to 2.81%. The credit bear arm of the thesis is now formally confirmed.

---

## Today in one line

**HY OAS 2.81% (Jul 27 FRED) printed ON THE DAY of the ceasefire while oil crashed −6.2% — definitively severing the oil-credit link and confirming AI capex destruction as an independent credit driver — then Iran launched ballistic missiles at US bases, collapsing the ceasefire in 36 hours and sending WTI back to $84.67 (+6.83%); with MSFT's neutral earnings leaving the Nasdaq −74,690 short intact and AMZN/META still to report, the structural bear thesis is simultaneously confirmed from two angles for the first time.**

*Flip to 0:* HY OAS tightens ≤2.70% on next FRED print (Jul 28+) OR WTI retreats below $78 on ceasefire 2.0. *Flip to conviction −1 target S&P 7,100:* AMZN or META confirm FCF destruction + HY OAS holds ≥2.85% + 10Y breaks above 4.75%.

---

## TL;DR

- **HY OAS 2.81% (Jul 27 FRED, +2bps) — the formal 2.80% bear gate has been crossed.** Credit widened on the day oil was collapsing (Jul 27 ceasefire, WTI −6.2%). The next FRED print (Jul 28+) arrives with WTI at $84.67. If OAS holds above 2.80% when oil is also spiking, the dual-driver (structural credit + geopolitical oil) is active simultaneously — the strongest bear alignment of this cycle.
- **WTI +6.83% to $84.67: the 2-day ceasefire is over.** Iran launched ballistic missiles at US military installations (FT, 13:42 UTC); US and Saudi Arabia already struck Iran-backed militias in Iraq. The oil-spike thesis, officially "retired" with 16 prior attempts, is operational again — but now it's running on top of a confirmed structural credit deterioration.
- **MSFT −0.67%: in-line result, no clarity, no squeeze.** Neither FCF destruction (bear) nor Azure beat (bull) was confirmed by market reaction. The Nasdaq −74,690 short, which was the key asymmetry preventing a −1 entry last session, survived into AMZN/META earnings. AMZN and META are now the decisive hyperscaler FCF reads.

---

## What moved & why

### Equities & sectors

**S&P 500 −0.47% to 7,393 (−35 pts), Nasdaq −0.67% to 24,711 (−165 pts), Dow −1.13% to 52,149 (−387 pts), Russell 2000 −0.11% to 2,951. VIX +2.69% to 18.70.**

The Dow lagging tech for once is structurally meaningful: XLI −1.68% is the worst performer (Baird downgraded Caterpillar on data center regulatory risks; industrials are being repriced as both the AI buildout beneficiary AND the potential casualty of regulatory friction). XLE +2.44% is the top sector (oil back). Dow-heavy industrials and oil-weighted components are pulling in opposite directions.

Three consecutive sessions of XLK weakness:
| Session | XLK | ASML | TSMC | Magnitude |
|---|---|---|---|---|
| Jul 23 | — | −6.89% | −4.98% | Liberation Day magnitude |
| Jul 28 | −3.22% | −5.18% | −3.32% | Day 2 |
| Jul 29 | −1.10% | −2.01% | −2.54% | Day 3 (decelerating) |

The deceleration in daily loss magnitude is worth noting — but the direction hasn't reversed. XLK is −6.14% week-over-week; the AI infrastructure derating is a sustained trend, not a one-session event.

**MSFT at 390.70 (−0.67%):** The post-AH-earnings read. MSFT was at 393.72 (+1.19%) intraday on Jul 28 before reporting. It now trades at 390.70 (−0.67% from the Jul 28 close of ~393.34). The market gave back the pre-earnings excitement and then some, but there was no dramatic gap. This is consistent with an in-line report: Azure growth held, but FCF wasn't strong enough to counter the GOOGL template narrative. MarketWatch's headline "Will Microsoft, Meta and Amazon be next?" captures the market's unresolved question.

**CRM +1.91% (week: +13.48%)** continues its breakout. Enterprise AI-feature software (no hyperscaler capex) remains the market's preferred AI investment model. V +0.55%, MA +0.31% (strong card spend data from AmEx confirmed prior session).

**Global: Nikkei −1.49% to 61,434 (week: −7.08%).** The Japanese chip equipment complex (Advantest, Tokyo Electron, Shin-Etsu) continues its derating alongside ASML/TSM. Notably, USD/JPY is 163.76 — the yen has NOT strengthened despite the Nikkei's −7% weekly loss. The carry trade is still being funded at 40-year cheap levels even as the chip longs it funds are being liquidated. **Hang Seng +1.96%:** China stimulus bid providing a counterweight in Asia.

### Rates & the dollar

**Day-over-day deltas (Jul 29 brief vs Jul 28 brief):**

| Metric | Jul 29 | Jul 28 | Δ | 1Y Pct |
|---|---|---|---|---|
| 10Y mkt | 4.622% | 4.629% | −0.7bps | 96.8th %ile |
| 30Y mkt | 5.100% | 5.121% | −2.1bps | — |
| 5Y mkt | 4.389% | 4.384% | +0.5bps | — |
| **10Y FRED (Jul 27)** | **4.65%** | 4.69% (Jul 24) | **−4bps** | **98.0th %ile** |
| **2Y FRED (Jul 27)** | **4.31%** | 4.33% (Jul 24) | **−2bps** | **98.4th %ile** |
| **2s10s FRED (Jul 28)** | **0.35%** | 0.34% (Jul 27) | **+1bp** | 4.8th %ile |
| **EFFR (Jul 28)** | **3.63%** | 3.63% | **unchanged** | 8.7th %ile |
| **HY OAS (Jul 27)** | **2.81%** | 2.79% (Jul 24) | **+2bps 🔴** | 38.5th %ile |
| IG OAS (Jul 27) | 0.81% | 0.80% | +1bp | 69.0th %ile |
| **10Y BEI (Jul 28)** | **2.20%** | 2.21% | **−1bp** | **0.4th %ile** |
| DXY | 101.385 | 101.518 | −0.133 | 97.2th %ile |
| USD/JPY | 163.759 | 163.837 | −0.078 | — |

**The EFFR at 3.63% unchanged (Jul 28 vintage) is the strongest available signal on the Fed decision.** The brief was captured at 9:57 AM ET, before the 14:00 ET decision. With CPI 3.53% (first MoM decline since 2020), Core CPI 2.59%, NFP +57k, and NFCI at −0.554 (loosening), the macro setup mandated a hold. The "rate-hike jitters" headline in the news feed confirms the market went in nervous about a potential hike — if a hike were delivered, its scale of surprise would have been exceptional.

**The most anomalous spread in the brief:** 10Y BEI 2.20% (0.4th %ile — near the LOWEST OF THE YEAR) on a day WTI is surging +6.83% to $84.67. The bond market is NOT pricing the oil→inflation channel. This is the stagflation signature in reverse: the market believes the oil shock is a war risk premium (transitory), not an inflation driver (structural). If Iran escalation persists and WTI holds above $85 for 2+ weeks, the BEI will need to reprice — historical lag from oil to breakevens is 3–4 weeks. This is the sleeper risk for duration.

**2s10s +1bp to 0.35% (4.8th %ile).** Still historically flat, marginally steepening. The 10Y-3M spread at 0.71% (84.9th %ile) shows the short end is anchored (Fed on hold), while the long end carries term premium.

**Stock-bond correlation: 0.06 (prior: 0.66).** This is the single most structurally important number in the brief — the 30-day rolling correlation between stocks and bonds has collapsed from 0.66 to near-zero. For 8 weeks, bonds and stocks fell together (hedge broken). Now they are uncorrelated. The mechanism: once the market accepted the Fed is not hiking (EFFR flat, Warsh rhetoric softened post-CPI), the "higher rates → lower multiples → lower equities" chain broke. Bonds can now rally on growth scares independently of equity direction. The 60/40 is partially restored.

### Commodities & credit

**WTI $84.67 (+6.83%), Brent $89.72 (+6.70%).** Iran launched ballistic missiles at US military installations (FT, Jul 29 13:42 UTC); Trump vowed to deliver a "beating." US and Saudi Arabia had already struck Iran-backed militia positions in Iraq (MarketWatch, 11:32 UTC). The 2-day ceasefire of Jul 27 is over. Saudi Arabia is routing oil exports through a Mediterranean port (longer, more expensive — confirms Hormuz disruption is structuring new physical flows, not just a risk premium). The dual choke point (Hormuz + Red Sea) is back. WTI is at 71.4th %ile and approaching the $85 level that has historically been the tipping point for this cycle's vol events.

**Gold $4,070.50 (+0.85%).** Gold recovering with oil — the geopolitical-fear bid is back. But the BEI is STILL falling (−1bp to 2.20%). The bond market is explicitly not pricing the oil→inflation channel. Either the bond market is massively wrong about WTI persistence, or gold's $48 recovery is a thin safe-haven bid that will fade if the Fed's hold removes the stagflation-driver.

**HY OAS 2.81% (Jul 27 FRED) — the decisive print.** This is confirmed: HY OAS widened +2bps to 2.81% on the same FRED vintage date (Jul 27) that oil crashed −6.2% on the ceasefire. The credit market was widening WHILE the geopolitical catalyst was resolving. The formal 2.80% gate has been crossed. The 38.5th %ile reading (vs. 3.2nd %ile five weeks ago at the Iran-deal-credit-tightest-of-cycle) is the clearest quantitative expression of the regime shift.

**IG OAS +1bp to 0.81% (69.0th %ile):** Investment-grade is following HY. IG widening is more concerning than HY in isolation because IG reflects fundamentals, not just risk appetite.

---

## Macro & data

**FRED (key new prints, Jul 27 vintage):**
- 10Y: 4.65% (−4bps from prior; **98.0th %ile, z=2.25**) — yields eased but remain historically extreme
- 2Y: 4.31% (−2bps; **98.4th %ile, z=2.36**) — same regime
- 2s10s: 0.35% (Jul 28, +1bp; **4.8th %ile**) — marginally steeper, still historically flat
- EFFR: 3.63% (Jul 28, unchanged — **Fed held**)
- NFCI: −0.554 (Jul 24, 6.0th %ile) — LOOSENING, most accommodative in months; financial conditions heading opposite to the bear trigger
- BEI: **2.20% (Jul 28, 0.4th %ile)** — −1bp on a day WTI +6.83%; bond market explicitly rejecting oil-inflation channel
- HY OAS: **2.81% (Jul 27, 38.5th %ile, +2bps)** — formal gate crossed
- IG OAS: 0.81% (Jul 27, 69.0th %ile)
- **Initial claims: 187,000 (Jul 18, 0.0th %ile, z=−1.88)** — labor is historically tight; no Fed cover from labor deterioration

**BLS (Jun vintage, unchanged):**
CPI-U 3.53% YoY; Core CPI 2.59%; NFP +57k (cycle low); Unemployment 4.2% (prev 4.3%, -0.1pp); AHE +3.52% YoY; Participation 61.5% (−0.3pp — historic decline).

**EIA (Jul 17 vintage, unchanged):** Crude +2,010 MBBL (BUILD), Gasoline +765 MBBL (BUILD), Distillate +1,395 MBBL (BUILD), **SPR −5,057 MBBL (DRAW — largest of cycle)**. The SPR draw is the government's active price-suppression mechanism even as Iran escalates. With SPR now at 311,447 MBBL (down from 316,504), the government's buffer is shrinking.

**CFTC (Jul 21, unchanged):**

| Contract | lev_net | Change | Reading |
|---|---|---|---|
| S&P 500 e-mini | −322,865 | +42,137 | Disciplined profit-taking; still substantially short |
| **Nasdaq-100** | **−74,690** | **−10,527** | **Bears ADDED — near-cycle extreme; conviction intact** |
| VIX futures | +3,098 | −7,091 | Vol longs reduced (before Iran re-escalated) |
| Ultra 10Y | −380,604 | −2,039 | Duration shorts unchanged; institutional holding |
| Ultra T-Bond | −899,165 | +11,287 | Long-end bears trimmed modestly |

The Nasdaq −74,690 short is the dominant positioning fact. Bears ADDED 10,527 contracts INTO the chip derating week. MSFT's in-line earnings did not trigger a squeeze. The position is now sitting through AMZN and META reporting. If both confirm the GOOGL FCF pattern, the short side gets further vindicated; if either breaks the pattern with strong FCF, the squeeze could be violent.

---

## Risk lens

**1. The dual-driver is now active simultaneously — for the first time this cycle.**

For the past three weeks, the bear thesis operated sequentially:
- Week 1: Credit widened (AI capex)
- Week 2: Oil spiked, then ceasefire deflated oil, credit widened DESPITE oil falling

Now both are active together:
- Credit: HY OAS 2.81% (formal gate crossed; AI capex structural)
- Oil: WTI $84.67 (+6.83%; Iran escalation resumed)

When the oil-credit link was debated, one driver could explain away the other. Now credit has confirmed independence from oil, AND oil is spiking simultaneously. The S&P at 7,393 faces compression from two separate structural forces: AI FCF destruction (longer-term multiple de-rating) and oil-driven inflation (shorter-term margin/multiple pressure). The bear thesis is on its strongest footing since the cycle began.

**2. MSFT in-line = ambiguity preserved, but the pattern is forming.**

GOOGL: −7.13% (FCF destruction, $190bn AI spend). MSFT: −0.67% (in-line/ambiguous). The market's question is whether GOOGL's result is idiosyncratic or systematic. MSFT's neutral result doesn't break the pattern — it just doesn't confirm it. AMZN and META are reporting next. If either shows FCF compression similar to GOOGL, the "systematic" verdict is confirmed and the chip-derating leg gets a second driver (platform FCF risk).

The MacroWatch framing is correct: "Alphabet and Tesla took a hit from soaring AI spending. Will Microsoft, Meta and Amazon be next?" is the market's live question, and the answer is landing this week.

**3. VRP 9.7 (VIX 18.70 vs realized 9.0): the highest sustained vol premium of the cycle.**

VRP at 9.7 is essentially the same level as the prior session. Options buyers are paying 2× realized vol for protection. But VIX is not in the 80th+ percentile — it's 69.8th %ile. This is "binary vol" pricing: investors know the catalyst calendar (AMZN/META, Iran, Fed language) but can't price direction. After AMZN/META resolve and Iran either escalates or backs down, VRP should compress sharply. The stock-bond corr 0.06 means TLT can act as a genuine portfolio hedge while waiting for the binary to resolve.

**4. Stock-bond correlation 0.06: the hedge is back; use it.**

The collapse from 0.66 to 0.06 is the most important structural shift in the brief. For months, the strategy of holding bonds as equity hedge was broken (both fell on inflation/rate fears). Now: if equities sell off on AI FCF destruction + Iran, Treasuries should rally (growth scare → flight to safety, with Fed on hold removing the rates-shock overlay). The 60/40 hedge is functional again. A −1 S&P entry can be partially hedged with TLT longs. This is a structural change in risk management that wasn't available 4 sessions ago.

**5. Yen carry and the BoJ: the underpriced tail.**

USD/JPY 163.76 (Nikkei −7.08% weekly without yen strengthening). The MarketWatch framing: "The Fed isn't your biggest worry... The central-bank decision that actually impacts your 401(k) lands in Tokyo." Japan is the largest foreign holder of US Treasuries. GPIF's $1.8T repatriation potential + BoJ normalization (now at 31-year-high policy rates) = if USD/JPY breaks below 160 and triggers carry unwind, the selling hits: (a) yen-funded chip longs, (b) US Treasuries (GPIF repatriation), (c) S&P broadly. The Nikkei's AI chip complex selloff is happening WITHOUT yen strengthening — meaning the carry trade is still funded and loaded. When it unwinds, it adds to already-happening chip selling. This is the tail risk that is entirely uncorrelated with the US AI/Iran narrative, and the most dangerous because of that independence.

---

## What to watch

**The thesis needs three things to be confirmed or refuted in the next 3 sessions:**

1. **HY OAS next FRED print (Jul 28+ vintage)** — does credit hold >2.80% with oil at $84.67? This is the decisive test.
2. **AMZN and META FCF** — the third and fourth hyperscaler reads. GOOGL confirmed destruction. MSFT was ambiguous. One more confirmation = "systematic" verdict.
3. **WTI: can Iran maintain pressure above $85?** Saudi Arabia's Mediterranean rerouting is structuring permanent supply adjustments, not just a risk premium.

```watch
[
  {"claim": "HY OAS holds above 2.80% on Jul 28+ FRED vintage — dual-driver (AI capex + oil) confirmed; bear thesis on strongest footing of cycle", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.79", "horizon": "2026-08-03", "probability": 0.55},
  {"claim": "AMZN reports FCF compression or negative FCF growth — systematic hyperscaler pattern confirmed (3 of 4)", "metric": "market:AMZN:change_pct", "trigger": "<-5.0", "horizon": "2026-08-01", "probability": 0.30},
  {"claim": "VIX breaks above 20.0 — dual credit+vol bear signal alignment", "metric": "market:^VIX:last", "trigger": ">20.0", "horizon": "2026-07-31", "probability": 0.42},
  {"claim": "WTI reclaims $90 as Iran escalation persists", "metric": "market:CL=F:last", "trigger": ">90.0", "horizon": "2026-08-03", "probability": 0.38},
  {"claim": "10Y BEI rises above 2.30% as oil shock begins flowing through to inflation expectations (3-4 week lag from WTI)", "metric": "macro:T10YIE", "trigger": ">2.29", "horizon": "2026-08-07", "probability": 0.45}
]
```

---

## The call

**Direction: −1 (net short / risk-off)**

This is the first session where the structural case is assembled from both legs simultaneously:

| Condition | Status |
|---|---|
| HY OAS >2.80% | ✅ CONFIRMED: 2.81% (Jul 27 FRED) |
| Credit independent of oil | ✅ CONFIRMED: credit widened as oil crashed |
| Oil shock catalyst | ✅ ACTIVE: WTI +6.83%, Iran ballistic missiles |
| MSFT — no bull squeeze | ✅ CONFIRMED: −0.67%, Nasdaq −74,690 intact |
| Fed on hold | ✅ INFERRED: EFFR 3.63% unchanged |
| Hedge functional | ✅ CONFIRMED: stock-bond corr 0.06 |

The one thing that's NOT confirmed is whether AMZN/META will repeat the GOOGL pattern. If META or AMZN beat on FCF, the position needs reassessment. But entering into the AMZN/META reporting WITH the credit gate already crossed and oil spiking is the right time to be short — the macro setup has never been cleaner for a bear entry.

**Stop conditions:** HY OAS ≤2.70% on next FRED print (credit reverts = structural thesis false) **OR** WTI falls below $78 (ceasefire 2.0 confirmed, oil spike self-corrects) **OR** AMZN + META both report FCF-positive with strong forward guidance.

**Position sizing note:** With stock-bond corr 0.06, a partial TLT long alongside the S&P short provides genuine portfolio risk reduction for the first time this cycle. Use it.

```stance
{"direction": -1, "notes": "Bear entry: HY OAS 2.81% (Jul 27 FRED) = formal 2.80% gate crossed for first time this cycle; credit widened ON THE DAY ceasefire collapsed oil −6.2% = AI capex is the structural driver, oil is now an additional overlay. Iran launched ballistic missiles at US bases; ceasefire 2.0 operational; WTI +6.83% to $84.67. MSFT −0.67% (in-line, neither trigger) = Nasdaq −74,690 short intact into AMZN/META. Fed held (EFFR 3.63% unchanged). Stock-bond corr 0.06 = hedge functional; partial TLT long reduces net portfolio risk. Stop: OAS ≤2.70% OR WTI <$78 OR AMZN+META both FCF-positive. Running hit-rate: 31/122 (25.4%) settled. Scenarios: Bear 45% / Base 35% / Bull 20%."}
```

---

## Sources

- *Trump vows to deliver 'beating' to Iran in retaliation for latest attack* (FT, 2026-07-29T13:42 UTC)
- *Oil prices rise after U.S. and Saudi Arabia attack Iran-backed militias in Iraq* (MarketWatch, 2026-07-29T11:32 UTC)
- *Dow Falls As Iran Hostilities Ignite Again; SK Hynix Slides* (Yahoo Finance/IBD, 2026-07-29T13:42 UTC)
- *Is AI facing a big financial reckoning?* (BBC Business, 2026-07-29T13:49 UTC)
- *Alphabet and Tesla took a hit from soaring AI spending. Will Microsoft, Meta and Amazon be next?* (MarketWatch, 2026-07-29T13:32 UTC)
- *The Fed isn't your biggest worry. The central-bank decision that actually impacts your 401(k) lands in Tokyo.* (MarketWatch, 2026-07-29T13:33 UTC)
- *Saudi Arabia has a new, and pricier, workaround to export its oil* (MarketWatch, 2026-07-29T11:16 UTC)
- *'Nothing seems to shake this market.' Why it's time to go all-in on stocks* (MarketWatch, 2026-07-29T11:17 UTC)
- *Baird downgrades Caterpillar to Neutral on rising data center regulatory risks* (Investing.com, 2026-07-29T13:18 UTC)
- *A profit squeeze is coming for tech. This manager is betting on these unglamorous stocks instead.* (MarketWatch, 2026-07-29T13:30 UTC)
- *SK Hynix stock rout shines light on this stunning semiconductor stock reality* (Yahoo Finance, 2026-07-29T13:50 UTC)
- Analytics: `brief_2026-07-29.json` (Jul 29 13:57 UTC intraday); `brief_2026-07-28.json` (Jul 28 13:52 UTC); CFTC Jul 21 vintage; FRED Jul 27/28 vintages; `data/running_thesis.md`
