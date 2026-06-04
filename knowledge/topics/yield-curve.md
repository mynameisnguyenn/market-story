# The yield curve (and why inversion matters)

The **yield curve** plots Treasury yields by maturity. The single most-watched slope is the
**2s10s** — the 10-year yield minus the 2-year (`curve_2s10s` in the timeline).

## What the slope means
- **Positively sloped (normal):** long rates > short rates. The market expects growth/inflation;
  banks earn a spread (borrow short, lend long). Healthy expansion.
- **Flat:** the cycle is maturing; the Fed has hiked the front end toward the long end.
- **Inverted (2s10s < 0):** short rates > long rates. The market expects the Fed to *cut* in the
  future — i.e. it's pricing a slowdown/recession that will force easing. The front end is pinned
  high by current Fed policy while the long end falls on those growth fears.

## Why it's a recession signal
A 2s10s (or 10y-3m) inversion has **preceded every US recession since the 1960s**, typically by
**~6–18 months** — one of the most reliable lead indicators in macro. The *causal* story: tight
policy (high short rates) eventually slows the economy; the bond market front-runs the resulting cuts.

## The crucial caveats (the daily-brief discipline)
- **It's a signal, not a clock.** The lag is long and variable. The 2019 inversion was "right" only
  via COVID; the deep **2022–24 inversion** has *not* (yet) produced a recession — the "higher-for-
  longer / soft landing" puzzle.
- **The inversion ending (re-steepening) is often the more dangerous moment** — the curve typically
  "bull-steepens" as the Fed cuts *into* a downturn.

## Read it in the data
`curve_2s10s` in the timeline (1998→now): inverted ahead of 2001 (dotcom), 2007 (GFC), briefly 2019,
and deeply 2022→. On the **Trends** tab it sits near its 0th percentile today — the flattest/most-
inverted of the modern record. See: [gfc], [housing-boom], [inflation], [higher-for-longer].
