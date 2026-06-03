# Market Story — 2026-06-03

## Since last time

This is the first read leaning on the full analytics stack — cross-asset percentiles, positioning, the vol premium, and a hedge-correlation check. Grading the prior watch items against today's tape:

- **HY OAS > 2.85 → de-risking?** — *Held.* OAS sits at **2.71% (3rd percentile of the year)**. Credit didn't widen, so the "unwind, not stress" call stands.
- **10Y break > 4.5%?** — *Watching.* 10Y at **4.49% (91st %ile)**, pressing the level but not through it. Duration pain is live but not yet a break.
- **WTI holds $95?** — *Triggered.* Crude **$95.80**, bid intact — and now backed by a hard EIA draw.

## Today in one line

**Duration unwind, not credit stress** — a −0.74% S&P with HY OAS *flat at the 3rd percentile* and yields *up* is a rates-driven de-rating of long-duration tech, not a solvency scare. **It flips to genuine de-risking only if HY OAS breaks ~2.85%** — until then, this is a positioning/duration event, and the hedges that matter are energy and cash, not Treasuries.

## TL;DR

- **The streak broke, led by the longest-duration names** — S&P −0.74%, Nasdaq −0.89%, all majors red; CRM −5.1%, NVDA −3.6%, MSFT −3.2% (Meta +4.2% the lone bid). Consequence: the de-rating is *rates math*, so it persists while 10Y holds the 91st %ile.
- **Your bond hedge isn't working** — stock-bond return correlation is **+0.76 (30d)**: Treasuries fell *with* equities. Consequence: on a duration-led day only energy/defensives cushion; don't lean on TLT.
- **Everything is priced for calm into the catalysts** — vol premium **+6.2** (VIX 16 vs 9.9 realized), credit at the 3rd %ile, specs net-short into it. Consequence: asymmetric — a soft payroll squeezes shorts up; an Iran headline gaps vol the short-vol crowd has to chase.

## What moved & why

**Equities — a rates-driven de-rating, not a growth scare.** 6 of 11 sectors red; the damage concentrated in AI-capex spenders and long-multiple platforms (CRM −5.09%, NVDA −3.62%, MSFT −3.17%, AMZN −2.53%), with **Energy +1.29%** the only real bid and Health/Staples the defensive tells. Broadcom's after-hours guide-down sharpened the semicap-fatigue read. **Meta +4.24%** bucked it — but one green mega-cap isn't leadership. Globally: Hang Seng +2.52% firm, Europe uniformly soft.

**The cross-asset extremes frame the regime.** This is late-cycle, priced-for-perfection: **Copper 98th %ile (+1.9σ)** and **10Y 96th (+1.7σ)** near 1-year highs, **credit ETFs rich (HYG 95th)**, while **VIX sits in the 25th**. The macro panel says the same in spread terms — **2s10s at the 0th percentile (flattest of the year)**, **HY *and* IG OAS at the 3rd**. When growth-cyclical (copper) and the long bond are both stretched and credit is this tight, there's little cushion if the catalyst turns.

**Rates — the cause, demoted to one line.** Yields rose across the curve (10Y +4bp to 4.49%, 5Y +4bp); that *is* the equity story, not a side note. Dollar firmer (DXY +0.30%, 87th %ile), yen pinned at 160.

## Macro & data

- **Energy (EIA):** commercial crude **drew ~8.0M bbl** and the **SPR drew ~8.0M** — the strategic buffer thinning as supply risk rises; gasoline/distillate built, so the tightness is crude-specific (Iran), not demand. This is the supply side under WTI's 86th-percentile level.
- **Rates/credit percentiles** (above): the single most useful macro read today — what's *stretched*, not just what moved.
- **BLS (April):** CPI +3.81% YoY, Core +2.75%; unemployment 4.3% (+0.1pp YoY). Sticky enough to keep the Fed boxed; markets await **Friday payrolls**.

## Risk lens

**Positioning — fast money was already defensive.** CFTC shows **leveraged funds net short the S&P (−458k, adding 56k shorts on the week)** and net short Treasuries, while **asset managers are heavily long (+1.0M)**. So Solomon's "greed" is real-money + retail length; the specs are hedged/short. Two-sided: it's squeeze fuel on a soft payroll, and confirmation that fast money de-risked before the first catalyst. **VIX specs are also net short** — short-vol crowded into live headline risk.

**Hedge efficacy — broken.** Stock-bond return correlation **+0.76 (30d, up from +0.48)**: Treasuries are not a hedge in this regime because rates are the *driver*. A real risk-off day won't be cushioned by duration — only by the energy/defensive sleeves that worked today.

**Vol — cheap-looking, for a reason.** VIX 16.1 vs **9.9 realized = a +6.2 premium**. Hedges *look* expensive vs. how calm the tape has been, but that calm is exactly the setup that snaps on a gap — and the short-vol positioning amplifies it.

**Tail risks:** (1) **Iran / Hormuz → $100+ oil** with the SPR already drawing — an oil spike into 4.3% unemployment and 3.8% CPI the Fed can't cut against. (2) **Short-vol unwind** into a headline gap. (3) **Spec-short squeeze** the other way on a benign payroll — −458k of S&P shorts is fuel. (4) **Credit is the line** — HY OAS through ~2.85% converts a tidy unwind into de-risking.

## What to watch

- **Friday payrolls** — soft + cooling Iran = squeeze (specs cover); hot + higher yields = more duration pain.
- **10Y 4.49% (91st %ile)** — a decisive break above 4.5% keeps pressure on tech; back under 4.4% relieves it.
- **HY OAS 2.71% (3rd %ile)** — the de-risking trigger; >2.85% changes the character.
- **Stock-bond corr +0.76** — watch for it to fall back below zero (hedge repairs) or stay positive (duration regime persists).
- **Copper −2.5% but 98th %ile** — does the cyclical leader keep cracking (growth worry spreading) or hold its stretched level?

```watch
[
  {"claim": "HY OAS widening flips unwind to de-risking", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.85", "horizon": "next session"},
  {"claim": "10Y decisive break keeps pressure on tech", "metric": "macro:DGS10", "trigger": ">4.5", "horizon": "next session"},
  {"claim": "Oil bid intact — WTI holds $95", "metric": "market:CL=F:last", "trigger": ">95", "horizon": "next session"},
  {"claim": "2s10s re-steepens off the 0th percentile", "metric": "macro:T10Y2Y", "trigger": ">0.55", "horizon": "next week"}
]
```

## Sources

- *Stock Market Today, June 3: Markets End Winning Streak on Middle East Escalation Fears* (Nasdaq)
- *Gold under pressure from higher rate expectations, while investors await U.S. payrolls report* (Seeking Alpha)
- *Broadcom plunges even as Q2 results, guidance top forecasts* (Seeking Alpha / Investing.com)
- *SpaceX targeting record IPO haul of up to $86 billion* (MarketWatch)
- Analytics: macro 1y percentiles, cross-asset extremes, CFTC positioning, vol risk premium, stock-bond correlation (all in `brief_2026-06-03.json`)
