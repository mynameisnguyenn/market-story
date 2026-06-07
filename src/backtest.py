"""Signal-validation backtest primitives — does a signal actually predict forward S&P returns?

Built to NOT fool itself, because the useful answer is usually "no edge":
  * strictly-FUTURE returns (pct_change(h).shift(-h)) — the last h points get NaN, no lookahead;
  * a moving-BLOCK bootstrap for the IC confidence interval — overlapping forward windows make
    daily samples heavily autocorrelated, so a naive t-stat (or 1/sqrt(n) SE) wildly overstates
    significance; resampling contiguous blocks of ~h preserves that dependence and widens the CI
    honestly. An edge counts only if the bootstrap CI excludes zero;
  * sub-period ICs — an edge that lives entirely in one regime (e.g. 2008) is not an edge.

Pure pandas/numpy + scipy (via signal_ic). No network, no I/O. Every function degrades to
None / {} rather than raising.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import signal_ic

# Forward-return horizons (trading days) the dashboard's signals implicitly claim to inform.
HORIZONS = [1, 5, 21, 63]


def forward_returns(prices: pd.Series, horizon: int) -> pd.Series:
    """Return realised from t to t+horizon, indexed at t (the last `horizon` rows are NaN —
    the future isn't knowable, so they can never leak into a fit)."""
    return signal_ic.forward_returns(prices, horizon)


def _aligned(signal: pd.Series, prices: pd.Series, horizon: int) -> pd.DataFrame:
    """(signal at t, forward return t->t+h) pairs, inner-joined on date, NaNs dropped."""
    fwd = forward_returns(prices, horizon)
    if signal is None or fwd is None or len(fwd) == 0:
        return pd.DataFrame(columns=["s", "f"])
    return pd.concat([signal.rename("s"), fwd.rename("f")], axis=1).dropna()


def information_coefficient(signal: pd.Series, prices: pd.Series, horizon: int):
    """Spearman rank IC between the signal and forward returns. Returns (ic, n) or None."""
    df = _aligned(signal, prices, horizon)
    if len(df) < 10:
        return None
    ic = signal_ic._spearman(df["s"].to_numpy(), df["f"].to_numpy())
    return (ic, len(df)) if ic is not None else None


def block_bootstrap_ic(
    signal: pd.Series,
    prices: pd.Series,
    horizon: int,
    block: int | None = None,
    n_boot: int = 1000,
    seed: int = 0,
    alpha: float = 0.05,
) -> dict | None:
    """Point IC plus a moving-block-bootstrap (1-alpha) CI. `block` defaults to max(horizon, 5)
    so each resampled block spans at least one full forward window. 'significant' = the CI does
    not straddle zero. Returns None when there is too little data."""
    df = _aligned(signal, prices, horizon)
    n = len(df)
    if n < 30:
        return None
    block = block or max(horizon, 5)
    if block >= n:
        return None
    s = df["s"].to_numpy()
    f = df["f"].to_numpy()
    point = signal_ic._spearman(s, f)
    if point is None:
        return None
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block))
    max_start = n - block
    ics = []
    for _ in range(n_boot):
        starts = rng.integers(0, max_start + 1, size=n_blocks)
        idx = np.concatenate([np.arange(st, st + block) for st in starts])[:n]
        ic = signal_ic._spearman(s[idx], f[idx])
        if ic is not None and np.isfinite(ic):
            ics.append(ic)
    if len(ics) < n_boot // 2:
        return None
    lo, hi = (float(x) for x in np.percentile(ics, [100 * alpha / 2, 100 * (1 - alpha / 2)]))
    return {
        "ic": round(float(point), 4), "n": int(n), "ci_lo": round(lo, 4), "ci_hi": round(hi, 4),
        "block": int(block), "n_boot": len(ics), "significant": bool(lo > 0 or hi < 0),
    }


def ic_subperiods(signal: pd.Series, prices: pd.Series, horizon: int,
                  periods: list[tuple[str, str, str]]) -> dict:
    """IC within each (label, start, end) window, attributed by the SIGNAL date (the forward
    return may realise just past the window end — that's correct, it's what the signal foresaw).
    Returns {label: {ic, n}}; a window with too little data yields {ic: None, n: k}."""
    df = _aligned(signal, prices, horizon)
    out: dict[str, dict] = {}
    for label, start, end in periods:
        sub = df.loc[(df.index >= pd.Timestamp(start)) & (df.index <= pd.Timestamp(end))]
        if len(sub) < 10:
            out[label] = {"ic": None, "n": int(len(sub))}
            continue
        ic = signal_ic._spearman(sub["s"].to_numpy(), sub["f"].to_numpy())
        out[label] = {"ic": round(float(ic), 4) if ic is not None else None, "n": int(len(sub))}
    return out


def quantile_spread(signal: pd.Series, prices: pd.Series, horizon: int, q: int = 5) -> float | None:
    """Mean forward return of the top signal-quantile minus the bottom — the economic size of
    any edge (an IC can be 'significant' yet trivially small)."""
    return signal_ic.quantile_spread(signal, prices, horizon, q)


def evaluate_signal(signal: pd.Series, prices: pd.Series,
                    periods: list[tuple[str, str, str]] | None = None,
                    horizons: list[int] | None = None, seed: int = 0) -> dict:
    """Full battery for one signal: per-horizon bootstrap IC + quantile spread, and (if given)
    sub-period ICs at the 21d horizon. Returns a structured, JSON-serialisable verdict."""
    horizons = horizons or HORIZONS
    by_h = {}
    for h in horizons:
        boot = block_bootstrap_ic(signal, prices, h, seed=seed)
        spread = quantile_spread(signal, prices, h)
        by_h[h] = {"bootstrap": boot,
                   "quantile_spread": round(float(spread), 5) if spread is not None else None}
    result = {"horizons": by_h}
    if periods:
        result["subperiods_21d"] = ic_subperiods(signal, prices, 21, periods)
    return result
