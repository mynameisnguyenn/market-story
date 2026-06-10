# Market Story — 2026-06-10

> *Brief captured 2026-06-09 14:38 UTC — Tuesday session, mid-morning US time (10:38am ET). All prices are intraday snapshots, not closes. FRED macro series lag 1–2 days; CFTC positioning is as of June 2 (8 trading days stale). May CPI is due today (Wednesday, June 10) — this read precedes the print.*

---

## Since last time

Grading the June 9 `watch` block against Tuesday's brief data:

| Claim | Trigger | Result |
|---|---|---|
| HY OAS above 2.80% — cascade tell | `macro:BAMLH0A0HYM2 > 2.80` | **MISS (pending)** — OAS ticked DOWN 1bp to 2.75% (11.1th %ile), the first reversal after five consecutive sessions of drift. Directionally improved but 5bps from trigger. |
| S&P 500 closes below 7,350 | `market:^GSPC:last < 7350` | **MISS** — S&P at 7,426 (+0.28% intraday); Monday closed at ~7,406. Dead-cat reversal thesis invalidated at this reading. |
| 10Y above 4.60% | `macro:DGS10 > 4.60` | **MISS** — TNX at 4.538%, edged DOWN 0.6bps. Rates eased fractionally with the risk-on bid. |
| Gold above $4,450 — flip condition | `market:GC=F:last > 4450` | **MISS** — Gold at $4,345.50 (55.2nd %ile), down $9.90 from Monday. Still mid-distribution, neither recovering nor breaking. |

**Watch-loop running scorecard (cumulative, scorecard_log.jsonl):** 1 triggered out of 12 graded (8.3% hit rate). The single hit was 10Y > 4.5% on June 5 payrolls day. Oil downside calls (×3), copper breakdown (×2), USDJPY intervention (×1), HY OAS cascade (×3), and gold breakdown (×1) all missed. Directionally correct on HY OAS drift (+5bps from 2.71% to 2.76% over five sessions) but the level triggers remain untripped. The watch loop is useful for regime identification, not entry timing.

Multi-session watches:

- **May CPI** — due today (Wednesday June 10). The brief does not have it. This is the single most important data point of the week and probably the month. Everything below is pre-CPI context.
- **HY OAS 2.80% cascade trigger** — first 1bp reversal; still watching.
- **CFTC June 12 data** — Friday. Still the June 2 read (−500,732 spec short).
- **Private credit cascade clock: Day 7** — no new headlines in Tuesday's brief. Still inside the 21–42 day historical window (June 25 – July 16) for material public OAS widening.
- **SpaceX IPO supply** — Now generating index-inclusion speculation; two Nasdaq Markets articles on Tuesday about SpaceX joining the Nasdaq-100. The supply story is building.

---

## TL;DR

- **Oil crashed −4.07% to $87.58 — the Iran cease-fire premium is now fully unwound.** WTI is $4.24 below Monday's snapshot and well off the May high. If the energy component of May CPI reflected a similar easing ($88–90 vs. $95+), the headline print gets mechanical relief. This is the one piece of data that moves the hike-tail probability before today's CPI release.

- **Breadth turned genuine: 9 of 11 sectors up vs. Monday's 5/6, with small caps (Russell 2000 +1.38%) and REITs (+1.96%) leading.** Monday was a chip-specific catalyst trade (ASML +6.80%, Jensen Huang commentary). Tuesday is rotation into rate-sensitive/domestic cyclicals — a qualitatively different signal, though still mid-morning and unconfirmed at close.

- **HY OAS ticked −1bp to 2.75%** — the first interruption in a five-session drift from 2.71% to 2.76%. One basis point doesn't break the cascade narrative, but it is the first day the public credit market tracked the equity bounce rather than diverging from it. The Wells Fargo NII guidance raise (mid-teens Q2 markets growth) adds to the "credit is still functioning" picture.

- **BofA flagged 70% of bear market signals at red, and May CPI drops today.** The sell-side warning is the most pointed since the selloff began. The CPI print is the regime gate: above 3.8% = hike tail becomes baseline and Tuesday's constructive read is immediately invalidated; below 3.5% = cut narrative returns and the −500k spec short faces its worst scenario. Pending the data, everything else is noise.

---

## What moved & why

### Equities & sectors

Tuesday's session (as of 10:38am ET) shows 9/11 sectors up — more breadth than the entire previous week. But the rotation pattern is the tell:

| Sector | Δ | Read |
|---|---|---|
| Real Estate (XLRE) | **+1.96%** | Rate-sensitive; responding to modest 10Y relief (−1.4bps). First meaningful XLRE gain since the selloff. |
| Cons. Discretionary (XLY) | **+1.54%** | Domestic consumer bid; partially driven by oil price relief (gasoline deflation) |
| Russell 2000 | **+1.38%** | Small caps, domestically focused, more rate-sensitive than large-cap; leading = mild rate-relief signal |
| Industrials (XLI) | **+1.07%** | Follows oil-relief (input cost) and small-cap cyclical bid |
| Financials (XLF) | **+1.04%** | Wells Fargo NII guidance; bank fundamentals still strong |
| Technology (XLK) | **−0.43%** | Chip-catalyst fade; no new AI hardware news today; platform/software names dragging |
| Energy (XLE) | **−1.93%** | Directly tracking WTI −4.07%; only meaningful sector laggard |

Within tech, the hardware/software split persists. ASML is the two-day leader at +3.45% (Terafab demand remains structural) and META +1.86%. But CRM −2.03%, NVDA −0.63%, MSFT −0.55% — platform software continues to reprice. CRM is now −30.9% YTD. Even NVDA, which drove Monday's Nasdaq bid, is slightly red on Tuesday. The chip bounce was a one-day catalyst trade; ASML's sustained outperformance reflects its monopoly on the physical throughput of AI chip production (EUV lithography), not a sector re-rating.

**Oracle Q4 preview** is front-of-mind in the headlines (AI infrastructure, cloud revenue growth). If Oracle beats after the close today, it could reignite the AI cloud narrative, but that does not change the rates or credit backdrop.

**Global:** Nikkei +2.17% — the two-day leader globally, extending Monday's Asia miss (Japan was closed during Monday's Iran-halt rally). FTSE −0.37% and Hang Seng −0.37% are the modest laggards.

### Rates & the dollar

Rates moved fractionally lower on Tuesday morning, but the long end is sticky:

| Tenor | Mon snapshot | Tue snapshot | Δ | 1Y %ile |
|---|---|---|---|---|
| 5Y | 4.278% | 4.264% | −1.4bps | — |
| 10Y | 4.544% | 4.538% | −0.6bps | **96.8th** |
| 30Y | 5.013% | **5.019%** | **+0.6bps** | — |
| 2s10s (FRED Jun 8) | 0.38% | **0.41%** | **+3bps** | **0.4th** |

The 30Y crossed 5.0% on Monday and is holding above it on Tuesday — the long end is not rallying with equities. The belly (5Y, 10Y) is easing modestly while the long end firms: this is mild bear steepening in the long end, slightly contradicting the risk-on tone. Historically, when both equities and 30Y yields rise simultaneously, it signals either growth optimism driving supply expectations (bearish for bonds) or supply concerns (also bearish for bonds). Neither is a clean risk-on.

The **2s10s steepening to 0.41% (+3bps from the Monday FRED read of 0.38%)** is the first meaningful curve steepening in four weeks. It's still at the 0.4th %ile — virtually the flattest of the year — but the direction has changed. If this continues through the CPI print, it would suggest the market is pricing in slightly more growth (reducing the inversion pressure), which is consistent with the broader breadth improvement.

**Dollar: DXY 99.786, −0.26%.** This is the second consecutive day of modest dollar softening: Monday −0.11%, Tuesday −0.26%. EURUSD +0.42%, GBP +0.50%. The dollar's decline is consistent with geopolitical risk premium normalizing (Iran cease-fire) and oil crashing. A softer dollar usually supports gold, but gold is slightly down on Tuesday — that divergence is a signal worth watching.

### Commodities & credit

**WTI: $87.58, −$4.24 (−4.62% from Monday's mid-session snapshot).** This is the defining move of the week so far. The chart of the past five sessions: oil surged on Middle East tension, then crashed on the Iran-halt. The net result from last week's close is WTI −6.6% (1-week change per brief). The support question is now $85 — if the cease-fire holds and OPEC+ adds supply concerns, there is nothing technical between $87 and the $84–86 zone. The crude inventory draw of 7,974 MBBL (week of May 29) provides a floor, but inventory draws in refinery maintenance season (May-June) are seasonal, not demand-driven.

**The inflation read-through from oil is significant:** If WTI averages $88 in June vs. $92–95 in May, the energy component of June CPI gets a 30–50bps tailwind. But May CPI (due today) reflects May prices. With WTI averaging roughly $92–95 for most of May, energy likely added to the May headline. Tuesday's oil crash is a June story, not a May CPI story. Don't let the oil move confuse the CPI read.

**Gold: $4,345.50, −$9.90 (−0.23%).** The gold/dollar divergence is notable: DXY fell −0.26% while gold fell −0.23%. In a normal dollar-weakening regime, gold should rise (they're inversely correlated). The fact that gold is not responding to dollar softening suggests the safe-haven and dollar-hedge bids are absent — gold is inert, not just waiting. The range ($4,300–$4,450) remains intact.

**Copper: $6.433, +$0.057 (+0.89%, 96.8th %ile).** Copper maintained above $6.40 for the second session. The demand signal is ambiguous: copper at the 97th %ile in a week where oil crashed −6.6% and consumer financial stress is at July 2022 highs is a contradiction. Copper either leads growth (and the rest of the data is lagging) or it converges down (and the stress signals are leading).

**HY OAS (FRED, June 8): 2.75% (11.1th %ile), −1bp.** The first reversal in a five-session drift. Combined with Wells Fargo's NII guidance and XLF +1.04%, credit conditions are not deteriorating on Tuesday. The cascade narrative requires sustained directional drift — one basis point does not erase it. IG OAS +1bp to 0.75% (9.9th %ile) — near historically tight. There is still no IG spread buffer; the market is not pricing credit risk.

---

## Macro & data

**May CPI (due today, June 10):** April headline was 3.81% / core 2.75%. The brief has no May print — it is expected today. This is the only macro data that matters this week. Key scenarios:
- **Above 3.8% headline:** Ferguson/Warsh hike framing becomes consensus baseline. 10Y breaks above 4.60%, XLK faces a second compression wave, and the −500k spec short is vindicated. The June-July private credit cascade clock accelerates in significance.
- **3.5–3.8%:** Status quo — the current fragility-without-resolution regime holds; equity volatility stays elevated; the hike tail stays as a 15–25% probability.
- **Below 3.5%:** Cut narrative returns. The −500k spec short faces its most dangerous scenario (largest S&P short in history facing a macro reversal). XLRE, XLY, small caps extend their Tuesday leadership. This seems unlikely given April was 3.81% and May energy prices were elevated.

**US Trade Deficit April: $55.9B** (Nasdaq Markets, June 9) — roughly in line with estimates. A pre-tariff normalization. No major surprise; modestly positive for GDP. Trade data precedes the geopolitical flare-up and is not a real-time signal.

**Wells Fargo NII guidance (June 9):** Q2 markets revenue growth "mid-teens," 2026 NII guidance reaffirmed. Banks are not seeing the credit stress that the private credit narrative implies. Bank NII and markets revenue are the canary-in-the-coal-mine for institutional credit transmission — if banks stay healthy, the private credit cascade is slower to transmit. This is a moderately important counterpoint.

**BofA bear market signals (70% flashing red):** BofA's indicator framework — which typically combines valuation (P/E vs. earnings growth), credit spreads, sentiment, and breadth — is at 70% on the bear side. The bank's models have historically been better at state identification than timing. The current state: stretched equity valuations at the 97th %ile yield, 10Y at the 97th %ile, VIX premium elevated, CFTC spec short at record — all of which independently validate the "70% bear signals" framing.

**FRED (latest, as of brief):**
- DGS10: **4.55%** (97.2nd %ile, June 5) — virtually unchanged at cycle high
- DGS2: **4.17%** (99.6th %ile, June 5) — near the highest 2Y in the past year
- T10Y2Y: **0.41%** (0.4th %ile, June 8) — steepened 3bps but still historically flat
- T10Y3M: **0.76%** (94.0th %ile) — belly is not pricing cuts
- EFFR: **3.62%** (0th %ile) — unchanged, lowest in past year (already cut)
- HY OAS: **2.75%** (11.1th %ile) — tight but drifting; −1bp reversal
- IG OAS: **0.75%** (9.9th %ile) — near record tight for the year
- 10Y Breakeven: **2.35%** (52.8th %ile) — mid-distribution; bond market is NOT pricing a hike; this is the most important divergence from the sell-side hike narrative
- Initial Claims: 225k (62.3rd %ile, week of May 30) — softening from 212k; no break in labor

---

## Risk lens

**CFTC positioning (June 2 — stale by 8 trading days; fresh data Friday June 12):**

| Contract | Net | WoW Δ | Read |
|---|---|---|---|
| S&P e-mini | **−500,732** | **−42,952** | Record spec short, expanded 9.5% in one week. Two sessions of small S&P gains have not forced covering at this scale (~$263bn notional). |
| Nasdaq-100 | −53,650 | −1,971 | Aligned short; barely moved |
| VIX futures | −33,033 | **+16,303 covered** | Earlier covering as VIX spiked to 21.51; vol-short squeezed first |
| Ultra T-Bond | −909,397 | −38,384 | Bond bears still adding; duration short near extremes |
| Ultra 10Y | −285,323 | −45,597 | Same; rate short expanding even as yields flatlined |

The spec short at −500,732 has now survived: AVGO −15%, CRM −5%, VIX spike to 21.51, and two days of small S&P gains. The CFTC Friday update is the week's most important non-price data: did the broad-based Tuesday rally (9/11 sectors up, small caps +1.38%) prompt any covering? At +0.28% intraday, probably not — systematic shorts do not capitulate on one-session moves. The pain threshold likely requires several sessions of 0.5%+ gains or a clear macro reversal (i.e., a soft CPI print).

**Vol structure:** VIX 18.41 (68.3rd %ile), realized 20d = 12.9%, vol risk premium = 5.5%. The premium ticked UP from 4.9 Monday to 5.5 Tuesday — realized vol dropped (12.9% vs. 13.2%) while VIX is essentially flat. The market is still buying tail protection even as spot cools. This is a fragility regime signature: fear doesn't evaporate cleanly, it gets repriced into shorter tails while realized vol normalizes. The dispersion regime continues: ASML +3.45% and CRM −2.03% on the same day means single-name vol is structurally elevated even as index VIX appears contained.

**Correlation watch:**
- Dollar down, gold down simultaneously — the gold/dollar inverse correlation is broken. Safe-haven bid is absent regardless of which way the dollar moves.
- Oil −4.62% while copper +0.89% — commodity complex is not moving as a unit; oil is pricing geopolitical normalization while copper is pricing demand. These signals are pointing in opposite directions.
- Long Treasuries (TLT) +0.40% as equities rally — UNLIKE the prior three sessions where TLT sold as equities rose. A small restoration of the classic bonds/equities inverse relationship, or just noise at this magnitude.

**Private credit cascade: Day 7** (June 4 = Day 0). No new headlines in the Tuesday brief. Historical pattern: material public OAS widening arrives Day 21–42 (June 25 – July 16). Current HY OAS 2.75%, 5bps from the 2.80% cascade trigger. The one-basis-point improvement today interrupts the drift but doesn't change the clock — if anything, Day 7 quiet after the initial cascade acceleration is consistent with the pattern (public markets are slow to price what private markets have already shown).

**SpaceX Nasdaq-100 inclusion risk:** Two articles on June 9 (Nasdaq Markets) specifically discussing SpaceX joining the QQQ. If this materializes, passive QQQ vehicles (AUM ~$300bn) must buy SpaceX by selling existing holdings proportionally. At a $1.8T valuation, even a 2% QQQ weight would require $6bn of buying — funded by selling $6bn of existing names. The timing: arriving into a period of already-compressed tech multiples and the largest spec short in history. This is an equity supply shock, not a liquidity event.

**Oil and the May CPI interaction:** WTI −4% today matters for June CPI (the July print), not May (the one due today). May averaged roughly $89–95 WTI. A May headline of 3.6–3.9% is the most likely range. The oil crash is a post-CPI development and doesn't bail out today's print.

**What to watch next:**

1. **May CPI today (June 10)** — the override. Above 3.8% = hike tail baseline; the entire constructive Tuesday read is invalidated. Below 3.5% = cut narrative and a short-squeeze setup. Nothing else matters until the print.

2. **HY OAS: does Tuesday's −1bp reversal hold?** A second consecutive session below 2.76% starts eroding the cascade thesis. A move above 2.78%+ on CPI surprise would confirm the drift resumed.

3. **WTI holding or breaking $85** — if oil slides further post-CPI (supply concern + geopolitical normalization), $85 is the next structural support. Below $85 on sustained volume = demand-growth-scare signal, not just geopolitics.

4. **Oracle Q4 results (after Tuesday close)** — AI cloud/infrastructure revenue is the bellwether for the AI spending cycle at the enterprise layer (vs. semiconductor at the infrastructure layer). A beat on AI cloud growth could extend Tuesday's rotation; a miss accelerates the AI-infra skepticism story that AVGO started.

5. **CFTC data Friday June 12** — the positioning verdict on whether Tuesday's broad breadth forced any spec-short covering.

```watch
[
  {"claim": "HY OAS above 2.80% — private credit cascade reaching public markets", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.80", "horizon": "this week"},
  {"claim": "WTI crude below $85 — oil floor fails, demand concern not just geopolitics", "metric": "market:CL=F:last", "trigger": "<85", "horizon": "next 2 sessions"},
  {"claim": "S&P 500 closes above 7,500 — correction over, spec short squeezed", "metric": "market:^GSPC:last", "trigger": ">7500", "horizon": "next 3 sessions"},
  {"claim": "10Y yield above 4.65% — post-CPI hike tail fully priced into the long end", "metric": "macro:DGS10", "trigger": ">4.65", "horizon": "this week"}
]
```

---

## Sources

- *Oracle Q4 preview: AI infrastructure, cloud strength in focus* (Seeking Alpha, 2026-06-09)
- *Wells Fargo sees Q2 markets growth in mid-teens; reaffirms 2026 NII guidance* (Seeking Alpha, 2026-06-09)
- *U.S. Trade Deficit Narrows To $55.9 Billion In April, Roughly In Line With Estimates* (Nasdaq Markets, 2026-06-09)
- *BofA warns investors to take profits as 70% of the bank's bear market signals flash red* (Yahoo Finance, 2026-06-09)
- *SpaceX Could Join the Nasdaq-100 Very Soon. Should You Buy the Invesco QQQ Trust Today?* (Nasdaq Markets, 2026-06-09)
- *Forget SpaceX: These 3 Stocks Have Better Potential to Become 10-Baggers* (Nasdaq Markets, 2026-06-09)
- *Microsoft tests key support at $411 after bearish reversal: Live levels* (Investing.com, 2026-06-09)
- *CrowdStrike shares fall as 'Mythos moment' fails to cheer investors* (Investing.com, 2026-06-09)
- *Scott Bessent visibly rattled after getting fact-checked to his face for claiming 'groceries are going down'* (Yahoo Finance, 2026-06-09)
- *HSBC is out with new AI TAM forecasts to 2030* (Investing.com, 2026-06-09)
- *Dell, HPE seen well positioned for AI and enterprise demand despite stock gains* (Investing.com, 2026-06-09)
- *Factbox — Airlines resume some Middle East flights but disruption continues* (Yahoo Finance, 2026-06-09)
- Analytics: CFTC positioning (June 2 — stale), vol risk premium, 1-year percentiles, FRED macro series — `brief_2026-06-09.json`
