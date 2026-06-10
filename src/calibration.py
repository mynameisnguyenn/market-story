"""Calibration math for the prediction ledger.

Brier score, calibration bins, and record filtering — pure functions over the
scorecard_log.jsonl record list. No I/O, no network calls. Degrade gracefully.
"""
from __future__ import annotations

MIN_N = 30  # minimum graded records for the panel to render


def _usable_prob(r: dict) -> float | None:
    """Extract a valid probability in [0, 1] from a record.

    Resolution order: r['probability'] if it is not None (0.0 counts!), else r['confidence']
    — a present-but-None probability falls through, it doesn't mask a usable confidence.
    Returns None for missing, non-numeric, or out-of-range values.
    """
    raw = r.get("probability") if r.get("probability") is not None else r.get("confidence")
    if raw is None:
        return None
    try:
        p = float(raw)
    except (TypeError, ValueError):
        return None
    if p < 0.0 or p > 1.0:
        return None
    return p


def gradeable(records: list[dict]) -> list[dict]:
    """Records with status in ('triggered', 'missed') AND a usable probability."""
    out = []
    for r in records:
        if r.get("status") not in ("triggered", "missed"):
            continue
        if _usable_prob(r) is None:
            continue
        out.append(r)
    return out


def brier_score(records: list[dict]) -> dict:
    """Mean (p - outcome)^2 over gradeable records.

    Returns {'score': float | None, 'n': int}. score is None when n == 0.
    """
    graded = gradeable(records)
    n = len(graded)
    if n == 0:
        return {"score": None, "n": 0}

    total = 0.0
    for r in graded:
        p = _usable_prob(r)
        outcome = 1.0 if r["status"] == "triggered" else 0.0
        total += (p - outcome) ** 2

    return {"score": total / n, "n": n}


def calibration_bins(records: list[dict], bins: int = 5) -> list[dict]:
    """Equal-width probability bins over [0, 1].

    Returns a list of {bin_lo, bin_hi, n, p_mean, realized} for non-empty bins only.
    realized = fraction of records in the bin with status 'triggered'.
    p=1.0 lands in the top bin (right edge is inclusive for the last bin).
    """
    if bins <= 0:
        return []

    graded = gradeable(records)
    if not graded:
        return []

    width = 1.0 / bins

    # Build bin buckets: list of lists
    buckets: list[list[dict]] = [[] for _ in range(bins)]
    for r in graded:
        p = _usable_prob(r)
        # Assign to bin index. The +1e-9 nudge defeats the float-representation trap where
        # e.g. 0.6 * 5 == 2.9999999999999996 -> int 2 (wrong bin); clamp p=1.0 into the last bin.
        idx = int(p * bins + 1e-9)
        if idx >= bins:
            idx = bins - 1
        buckets[idx].append(r)

    result = []
    for i, bucket in enumerate(buckets):
        if not bucket:
            continue
        bin_lo = round(i * width, 10)
        bin_hi = round((i + 1) * width, 10)
        n = len(bucket)
        p_mean = sum(_usable_prob(r) for r in bucket) / n
        triggered = sum(1 for r in bucket if r["status"] == "triggered")
        realized = triggered / n
        result.append({
            "bin_lo": bin_lo,
            "bin_hi": bin_hi,
            "n": n,
            "p_mean": p_mean,
            "realized": realized,
        })

    return result
