# Signal validation — do the dashboard's signals actually predict?

**Run:** 2026-06-06 · committed timeline `data/timeline.jsonl` (7,150 sessions, 1998-01-02 → 2026-06-05)
· engine `src/backtest.py` (tested) · independently reproduced + adversarially refuted by a 4-agent workflow.

> **One-line verdict:** of everything the dashboard surfaces, **exactly one signal has a robust,
> regime-stable, economically-meaningful edge on forward S&P returns — the VIX *level* (buy-fear).**
> The 10Y-yield relationship is real but *regime-conditional* (it flipped sign in 2022). Everything
> else is either a statistical artifact or genuinely non-predictive — including the headline
> **"Market stress" turbulence gauge, which is descriptive, not predictive.** That's a fine role for a
> risk-awareness tool — but don't trade these ICs.

## How this can't fool itself (method)

The Information Coefficient (Spearman rank correlation of a signal with *forward* S&P returns) is easy
to fake yourself with. Guards used:

- **No lookahead** — forward returns are `pct_change(h).shift(-h)`; the last `h` points are NaN and can
  never leak into the fit. (`tests/test_backtest.py` pins this.)
- **Block-bootstrap CIs, not t-stats** — daily samples of an `h`-day forward return overlap ~`h`×, so a
  naive standard error (`1/√n`) overstates significance wildly. A moving-block bootstrap (block ≈ `h`)
  preserves that autocorrelation and widens the CI honestly. **"Significant" = the bootstrap 95% CI
  excludes zero.** (Certified: a perfect predictor reads significant; pure noise reads *not* significant.)
- **Level vs. change** — a "significant" IC on a *level* that vanishes in the *change* form is the classic
  spurious correlation of two trending series. Every signal is tested both ways.
- **Sub-period ICs** — an edge that lives in one regime (e.g. 2008) is not an edge. Six eras: pre-GFC,
  GFC, 2010s, COVID, 2022-23 inflation, 2024-26.
- **Independent adversarial reproduction** — four skeptic agents re-ran the numbers from scratch and were
  asked to *refute* each conclusion. All four confirmed.
- **Multiple testing** — 48 level tests were run; **16 cleared the bar, vs ~2.4 expected by chance.** So
  there is real structure — but most of the 16 fail the deeper tests below.

## Verdict by signal

| Signal | Verdict | 21d level IC (95% CI) | Why |
|---|---|---|---|
| **VIX (level)** | ✅ **Real edge** | **+0.13 [+0.04, +0.21]** | Positive in **all 6** regimes; survives dropping GFC+COVID (+0.12); quantile spread +1.4%/21d. |
| 10Y yield (level) | ⚠️ **Regime-conditional** | −0.10 [−0.19, −0.03] | Full-sample sig, but **sign flips**: −0.14/−0.35 pre-2022 → **+0.32** (2022-23), +0.11 (2024-26). Not stable. |
| Gold (level) | ❌ Spurious | +0.15 [+0.06, +0.23] | Non-stationary trend artifact — **change-form IC ≈ 0** (+0.002). |
| HY OAS (level) | ❌ Unproven | +0.31 [+0.06, +0.55] | Only **754 obs, all 2023-2026, fully backfilled**, one regime; change-form dead. |
| IG OAS (level) | ❌ Unproven | +0.23 (ns) | Same 3-yr backfilled window; only 63d squeaks significant; change-form dead. |
| Copper (level) | ⬜ No edge | +0.06 (ns) | Level & change both insignificant; sub-periods sign-flip. |
| S&P spec positioning | ⬜ No edge | +0.05 (ns) | Insignificant; sub-periods flip (−0.30 → +0.32). |
| 2s10s curve | ⬜ No edge | −0.01 (ns) | Flat everywhere; quantile spread ≈ 0. |
| Dollar (DXY) | ⬜ No edge | −0.03 (ns) | Insignificant; regime-swinging sub-periods. |
| Vol premium (VIX−realized) | ⬜ ~No edge | +0.05 (ns) | Only 1d marginally sig; change-form & sub-periods unstable. |
| **Kritzman turbulence** | ⬜ **Descriptive only** | −0.01 (ns) | No predictive edge at any horizon/form/sign. Only the GFC sub-period is negative (high stress → more drawdown *during* a crisis — a description, not a forecast). |
| **Turbulence stress %ile** | ⬜ **Descriptive only** | +0.01 (ns) | Same. The dashboard's headline "Market stress Nth %ile" measures *current* unusual cross-asset behavior; it does **not** forecast returns. |

*(ns = bootstrap CI straddles zero.)*

## What it means

1. **VIX level is the one signal worth leaning on.** High VIX → higher forward returns (you're paid the
   risk premium for holding when fear is elevated). It's modest (~1.4% per quintile at 21d) and weakest
   exactly when vol is macro-/rate-driven rather than fear-driven (2022-23 IC was ~0), but it's the only
   signal positive in every regime and robust to dropping the two crisis windows. Trust it — modestly,
   and as a *level*, not a daily change.
2. **The 10Y "edge" is a trap as a single number.** The full-sample IC averages two opposite regimes:
   pre-2022 rates-up-equities-down, post-2022 rates-up-equities-up (reflation). Read it *conditionally on
   the inflation regime*, never as one coefficient.
3. **Credit spreads, gold, copper, the dollar, positioning, the curve, the vol premium, and the turbulence
   gauges do not predict forward S&P returns** in this sample. Several *look* significant until you difference
   them (gold) or notice they're a 3-year backfilled window (HY/IG OAS). This is the expected outcome — most
   "signals" are context, not alpha.
4. **For the dashboard:** keep these as what they are — *situational awareness* (where are we vs. history,
   how stressed is the tape right now). The existing Signal-IC panel already shows live IC honestly; this
   study says the right framing is "context," and the only one to read as a forward tilt is VIX level.

## Caveats

- IC/quantile spread are **gross of costs** and are *not* a tradeable strategy — they measure rank
  association, not a backtested P&L.
- **7,147 / 7,150 rows are backfilled** (historical archive, not live daily runs); conclusions are only as
  good as that committed history. Signals with thin, all-backfilled windows (HY/IG OAS) are the least trustworthy.
- The composite **danger flag** is *not* in the timeline (it needs per-day brief fields that aren't all
  stored), so it wasn't directly tested; its components (VIX level ✅, vol premium ⬜, 2s10s ⬜, stock-bond
  corr — untested) were tested individually, and only the VIX-level piece carries predictive weight.
- This is a single market (S&P) and a single target (forward price return). A signal with no edge on S&P
  direction may still be useful for vol, drawdown, or cross-asset timing — not tested here.

## Re-running

`src/backtest.py` is the tested engine; `research/signal_battery.py` runs the full battery over the
current timeline and writes the numbers. Re-run as the timeline accumulates more *live* (non-backfilled)
sessions — the HY/IG OAS verdict in particular should be revisited once there's history beyond 2023.
