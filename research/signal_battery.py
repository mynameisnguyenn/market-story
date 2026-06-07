"""Full signal-validation battery over the committed timeline.

Reproduces the numbers behind research/signal-validation.md: for every dashboard signal, the
block-bootstrap IC (level + change) across horizons, the top-minus-bottom quintile spread, the
per-era sub-period ICs, and coverage (incl. how much is backfilled). Prints a summary table and
dumps full JSON to the OS temp dir.

    python research/signal_battery.py          # from the repo root

Pure read of committed data + src/backtest.py; no network. Re-run as the timeline accumulates
more live (non-backfilled) sessions — the HY/IG OAS verdict especially should be revisited.
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repo root on path

import pandas as pd

from src import backtest, regime_turbulence, timeline

df = timeline.load_df()
spx = pd.to_numeric(df["spx"], errors="coerce")
backfilled = (df["backfilled"] == True) if "backfilled" in df.columns else pd.Series(False, index=df.index)  # noqa: E712

ERAS = [
    ("1998-2007 pre-GFC", "1998-01-01", "2007-06-30"),
    ("2007-2009 GFC", "2007-07-01", "2009-06-30"),
    ("2010-2019 expansion", "2009-07-01", "2019-12-31"),
    ("2020-2021 COVID", "2020-01-01", "2021-12-31"),
    ("2022-2023 inflation", "2022-01-01", "2023-12-31"),
    ("2024-2026 recent", "2024-01-01", "2026-12-31"),
]

# (column, label, economic hypothesis for the LEVEL IC sign)
STORED = [
    ("vix", "VIX level", "+ (high fear -> mean-reversion up)"),
    ("curve_2s10s", "2s10s curve", "? (inversion = recession risk; ambiguous for returns)"),
    ("vol_premium", "Vol premium (VIX-realized)", "+ (fear priced / protection rich)"),
    ("hy_oas", "HY OAS", "+ buy-fear / - momentum (ambiguous); SHORT SAMPLE"),
    ("ig_oas", "IG OAS", "+ buy-fear / - momentum (ambiguous); SHORT SAMPLE"),
    ("dxy", "Dollar (DXY)", "- (strong dollar -> risk-off)"),
    ("ust10", "10Y yield", "? (rising yields ambiguous)"),
    ("copper", "Copper", "? (Dr Copper: growth proxy)"),
    ("gold", "Gold", "? (safe haven)"),
    ("spx_spec_net", "S&P spec net positioning", "- (crowded long -> contrarian)"),
]


def coverage(s):
    s = pd.to_numeric(s, errors="coerce")
    nn = s.notna()
    return {"n_nonnull": int(nn.sum()),
            "first": str(s[nn].index.min().date()) if nn.any() else None,
            "last": str(s[nn].index.max().date()) if nn.any() else None,
            "n_backfilled": int((nn & backfilled).sum()),
            "n_live": int((nn & ~backfilled).sum())}


def run_signal(sig, label, hyp, do_change=True):
    out = {"label": label, "hypothesis": hyp, "coverage": coverage(sig)}
    out["level"] = backtest.evaluate_signal(sig, spx, periods=ERAS)
    if do_change:
        out["change"] = {"horizons": {h: {"bootstrap": backtest.block_bootstrap_ic(sig.diff(), spx, h, n_boot=600)}
                                      for h in backtest.HORIZONS}}
    return out


def main():
    results = {}
    for col, label, hyp in STORED:
        if col not in df.columns:
            continue
        print(f"running {label} ...", flush=True)
        results[col] = run_signal(pd.to_numeric(df[col], errors="coerce"), label, hyp)

    print("running turbulence ...", flush=True)
    turb = regime_turbulence.turbulence(regime_turbulence.returns_from_timeline(), lookback=252)
    stress = regime_turbulence.stress_percentile(turb, window=252)
    results["turbulence"] = run_signal(turb, "Kritzman turbulence", "- near-term / + longer", do_change=False)
    results["stress_pct"] = run_signal(stress, "Turbulence stress %ile", "- near-term / + longer", do_change=False)

    tests = sum(1 for r in results.values() for d in r["level"]["horizons"].values() if d["bootstrap"])
    sig = sum(1 for r in results.values() for d in r["level"]["horizons"].values()
              if d["bootstrap"] and d["bootstrap"]["significant"])
    results["_meta"] = {"n_level_tests": tests, "n_significant": sig,
                        "expected_false_pos_at_5pct": round(tests * 0.05, 1)}

    path = os.path.join(tempfile.gettempdir(), "signal_battery.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, default=str)

    print("\n=== LEVEL bootstrap IC (* = bootstrap CI excludes 0) ===")
    print(f"{'signal':28} {'cover':>6} " + " ".join(f"{h}d".rjust(16) for h in backtest.HORIZONS))
    for col, r in results.items():
        if col == "_meta":
            continue
        cells = []
        for h in backtest.HORIZONS:
            b = r["level"]["horizons"][h]["bootstrap"]
            cells.append(f"{b['ic']:+.3f}{'*' if b['significant'] else ' '}[{b['ci_lo']:+.2f},{b['ci_hi']:+.2f}]"
                         if b else "n/a")
        print(f"{r['label'][:28]:28} {r['coverage']['n_nonnull']:>6} " + " ".join(c.rjust(16) for c in cells))
    print(f"\nMultiple testing: {sig}/{tests} level tests significant; ~{results['_meta']['expected_false_pos_at_5pct']} "
          f"expected by chance at 5%.\nFull JSON: {path}")


if __name__ == "__main__":
    main()
