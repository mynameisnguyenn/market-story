# Credit spreads (HY / IG OAS) — the early-warning system

A **credit spread** is the extra yield a corporate bond pays over a Treasury of the same maturity —
compensation for default risk. The standard gauges are **option-adjusted spreads (OAS)**:
- **HY OAS** (`hy_oas`): high-yield ("junk") spread — the risk-on/off thermometer.
- **IG OAS** (`ig_oas`): investment-grade spread — higher-quality, less jumpy.

## Why a risk analyst watches credit before equities
Equities can drift higher on momentum and narrative; **credit markets price survival**. When funding
gets harder and default risk rises, spreads widen *first* — often while stocks are still complacent.
So **credit is the line**: an equity selloff with *calm* credit is a positioning/duration unwind; an
equity selloff with *widening* credit is genuine de-risking. (This is the exact distinction the daily
"today's read" classifier makes.)

## The historical record
- **Tight (≈ 3% HY):** "priced for perfection" — no stress, but little cushion. *Today is here (3rd
  percentile).*
- **Normal (≈ 4–5%):** ordinary risk pricing.
- **Wide (> 6–8%):** stress. In the **GFC, HY OAS blew out toward ~20%** (Nov–Dec 2008) — the
  clearest crisis gauge of all. COVID (Mar 2020) spiked HY toward ~10–11% before the Fed's
  unprecedented move to **buy corporate bonds** crushed it back.

## The rule the daily brief lives by
> Watch HY OAS daily. A tight, flat spread flipping wider (e.g. through ~2.85% from the 3rd percentile)
> is what turns "tidy unwind" into "real de-risking." Credit confirms or denies the equity story.

## Read it in the data
`hy_oas` / `ig_oas` (our timeline's spread series starts 2023; the GFC/COVID blowouts predate it but
are the canonical lessons). See: [gfc], [covid], [higher-for-longer].
