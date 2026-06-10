"""Tests for src/calibration.py — pure unit tests, synthetic data only."""
from __future__ import annotations

import numpy as np
import pytest

from src.calibration import MIN_N, brier_score, calibration_bins, gradeable


# ---------------------------------------------------------------------------
# Helpers to build synthetic records
# ---------------------------------------------------------------------------

def _rec(status: str, prob=None, confidence=None) -> dict:
    """Minimal record with the given status and optional probability/confidence."""
    r = {"status": status}
    if prob is not None:
        r["probability"] = prob
    if confidence is not None:
        r["confidence"] = confidence
    return r


# ---------------------------------------------------------------------------
# MIN_N export
# ---------------------------------------------------------------------------

def test_min_n_exported():
    assert MIN_N == 30


# ---------------------------------------------------------------------------
# gradeable()
# ---------------------------------------------------------------------------

def test_gradeable_excludes_pending_unresolved():
    recs = [
        _rec("pending", prob=0.7),
        _rec("unresolved", prob=0.3),
        _rec("triggered", prob=0.8),
        _rec("missed", prob=0.2),
    ]
    g = gradeable(recs)
    assert len(g) == 2
    assert all(r["status"] in ("triggered", "missed") for r in g)


def test_gradeable_includes_probability_zero():
    """p=0.0 is a valid probability — the falsy-zero trap."""
    recs = [_rec("missed", prob=0.0)]
    g = gradeable(recs)
    assert len(g) == 1


def test_gradeable_uses_probability_key_over_confidence():
    """probability key takes precedence; confidence is fallback."""
    r = _rec("triggered", prob=0.6, confidence=0.9)
    g = gradeable([r])
    assert len(g) == 1


def test_gradeable_falls_back_to_confidence():
    """When probability key is absent, confidence is used."""
    r = _rec("triggered", confidence=0.5)
    g = gradeable([r])
    assert len(g) == 1


def test_gradeable_discards_out_of_range_probability():
    recs = [
        _rec("triggered", prob=1.2),
        _rec("missed", prob=-0.1),
    ]
    assert gradeable(recs) == []


def test_gradeable_discards_non_numeric_probability():
    recs = [
        _rec("triggered", prob="high"),
        _rec("missed", confidence="medium"),
    ]
    assert gradeable(recs) == []


def test_gradeable_discards_none_probability_and_no_confidence():
    recs = [_rec("triggered")]
    assert gradeable(recs) == []


def test_gradeable_does_not_use_or_chaining_for_zero():
    """Explicitly confirm that a probability of exactly 0.0 is NOT discarded.
    This would fail if the implementation used `r.get('probability') or r.get('confidence')`."""
    # record has probability=0.0 and confidence=0.9; should use probability=0.0, not confidence
    r = {"status": "missed", "probability": 0.0, "confidence": 0.9}
    g = gradeable([r])
    assert len(g) == 1
    # Verify _usable_prob actually returned 0.0 (not 0.9) by checking brier score
    result = brier_score([r])
    # outcome=0 (missed), p=0.0 => (0.0 - 0)^2 = 0.0
    assert result["score"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# brier_score()
# ---------------------------------------------------------------------------

def test_brier_score_empty():
    assert brier_score([]) == {"score": None, "n": 0}


def test_brier_score_pending_only():
    recs = [_rec("pending", prob=0.5), _rec("unresolved", prob=0.4)]
    assert brier_score(recs) == {"score": None, "n": 0}


def test_brier_score_always_wrong():
    """Always-wrong forecaster: p=1.0 on every missed, p=0.0 on every triggered.
    Expected score: always (1-0)^2=1 for p=1/missed, (0-1)^2=1 for p=0/triggered => ~1."""
    recs = [_rec("missed", prob=1.0) for _ in range(10)]
    result = brier_score(recs)
    assert result["n"] == 10
    assert result["score"] == pytest.approx(1.0)


def test_brier_score_always_wrong_triggered():
    recs = [_rec("triggered", prob=0.0) for _ in range(5)]
    result = brier_score(recs)
    assert result["score"] == pytest.approx(1.0)


def test_brier_score_perfect():
    """Perfect forecaster: p=1.0 triggered, p=0.0 missed => score=0."""
    recs = (
        [_rec("triggered", prob=1.0) for _ in range(5)]
        + [_rec("missed", prob=0.0) for _ in range(5)]
    )
    result = brier_score(recs)
    assert result["score"] == pytest.approx(0.0)
    assert result["n"] == 10


def test_brier_score_known_value():
    # p=0.7, outcome=triggered: (0.7 - 1)^2 = 0.09
    # p=0.3, outcome=missed:    (0.3 - 0)^2 = 0.09
    recs = [_rec("triggered", prob=0.7), _rec("missed", prob=0.3)]
    result = brier_score(recs)
    assert result["score"] == pytest.approx(0.09)
    assert result["n"] == 2


def test_brier_score_uses_probability_zero():
    """p=0.0 on a missed record: (0.0 - 0)^2 = 0.0."""
    recs = [_rec("missed", prob=0.0)]
    result = brier_score(recs)
    assert result["score"] == pytest.approx(0.0)
    assert result["n"] == 1


def test_brier_score_discards_invalid():
    recs = [
        _rec("triggered", prob=1.2),   # out of range
        _rec("missed", prob="high"),    # non-numeric
        _rec("triggered", prob=0.5),    # valid
    ]
    result = brier_score(recs)
    assert result["n"] == 1
    # (0.5 - 1)^2 = 0.25
    assert result["score"] == pytest.approx(0.25)


# ---------------------------------------------------------------------------
# calibration_bins()
# ---------------------------------------------------------------------------

def test_calibration_bins_empty():
    assert calibration_bins([]) == []


def test_calibration_bins_pending_only():
    recs = [_rec("pending", prob=0.5)]
    assert calibration_bins(recs) == []


def test_calibration_bins_non_empty_only():
    """Only bins with records are returned."""
    # All records at p=0.9 (top bin)
    recs = [_rec("triggered", prob=0.9) for _ in range(3)]
    result = calibration_bins(recs, bins=5)
    assert len(result) == 1
    assert result[0]["n"] == 3


def test_calibration_bins_p1_in_top_bin():
    """p=1.0 must land in the top bin, not overflow."""
    recs = [_rec("triggered", prob=1.0)]
    result = calibration_bins(recs, bins=5)
    assert len(result) == 1
    b = result[0]
    # Top bin for 5 bins is [0.8, 1.0]
    assert b["bin_lo"] == pytest.approx(0.8)
    assert b["bin_hi"] == pytest.approx(1.0)
    assert b["n"] == 1


def test_calibration_bins_p0_in_bottom_bin():
    """p=0.0 lands in the first bin."""
    recs = [_rec("missed", prob=0.0)]
    result = calibration_bins(recs, bins=5)
    assert len(result) == 1
    b = result[0]
    assert b["bin_lo"] == pytest.approx(0.0)
    assert b["bin_hi"] == pytest.approx(0.2)


def test_calibration_bins_realized_fraction():
    """realized = fraction triggered in the bin."""
    recs = (
        [_rec("triggered", prob=0.5) for _ in range(3)]
        + [_rec("missed", prob=0.5) for _ in range(1)]
    )
    result = calibration_bins(recs, bins=5)
    assert len(result) == 1
    assert result[0]["realized"] == pytest.approx(0.75)
    assert result[0]["n"] == 4


def test_calibration_bins_structure():
    """Each bin dict has the required keys."""
    recs = [_rec("triggered", prob=0.5), _rec("missed", prob=0.2)]
    result = calibration_bins(recs, bins=5)
    for b in result:
        for key in ("bin_lo", "bin_hi", "n", "p_mean", "realized"):
            assert key in b, f"Missing key: {key}"


def test_calibration_bins_p_mean():
    """p_mean is the mean of probabilities in the bin."""
    recs = [_rec("triggered", prob=0.6), _rec("missed", prob=0.7)]
    result = calibration_bins(recs, bins=5)
    assert len(result) == 1
    assert result[0]["p_mean"] == pytest.approx(0.65)


def test_calibration_bins_perfectly_calibrated_brier_approx():
    """A perfectly calibrated set: p=k/10 records with realized rate ~p.
    For each bin the expected Brier contribution is p*(1-p) (variance of a Bernoulli).
    We check that the overall Brier score approximates sum(p*(1-p)*weight) ~ 0.25 for p=0.5."""
    np.random.seed(42)
    recs = []
    # Build 500 records: p drawn uniformly, outcome sampled from Bernoulli(p)
    probs = np.random.uniform(0.0, 1.0, 500)
    for p in probs:
        outcome = np.random.binomial(1, p)
        status = "triggered" if outcome == 1 else "missed"
        recs.append(_rec(status, prob=round(float(p), 4)))

    result = calibration_bins(recs, bins=5)
    bs = brier_score(recs)

    # For a well-calibrated forecaster, Brier score ~ mean p*(1-p) which for Uniform(0,1) = 1/6 ~ 0.167
    # Allow generous tolerance given finite sample
    assert bs["score"] is not None
    assert 0.10 < bs["score"] < 0.25, f"Brier score {bs['score']} outside expected range for calibrated set"

    # Each non-empty bin should have realized ≈ p_mean (within sampling noise)
    for b in result:
        # For 5 equal-width bins with ~100 records each, allow ±0.15
        assert abs(b["realized"] - b["p_mean"]) < 0.15, (
            f"Bin [{b['bin_lo']:.1f},{b['bin_hi']:.1f}]: "
            f"realized={b['realized']:.3f} vs p_mean={b['p_mean']:.3f}"
        )


def test_calibration_bins_all_five_filled():
    """With uniform spread of p, all 5 bins are populated."""
    np.random.seed(42)
    probs = [0.1, 0.3, 0.5, 0.7, 0.9]
    recs = []
    for p in probs:
        for _ in range(10):
            recs.append(_rec("triggered", prob=p))
    result = calibration_bins(recs, bins=5)
    assert len(result) == 5


def test_calibration_bins_includes_probability_zero_records():
    """p=0.0 records ARE included in the calibration bins (falsy-zero trap)."""
    recs = [_rec("missed", prob=0.0) for _ in range(5)]
    result = calibration_bins(recs, bins=5)
    assert len(result) == 1
    assert result[0]["n"] == 5
    assert result[0]["p_mean"] == pytest.approx(0.0)
    assert result[0]["realized"] == pytest.approx(0.0)


def test_calibration_bins_custom_bin_count():
    """bins parameter is respected — different bin counts yield different bin widths."""
    recs = [_rec("triggered", prob=0.5) for _ in range(4)]
    result_5 = calibration_bins(recs, bins=5)
    result_10 = calibration_bins(recs, bins=10)
    # Both have exactly 1 non-empty bin
    assert len(result_5) == 1
    assert len(result_10) == 1
    # bins=5 width=0.2 → bin_lo=0.4; bins=10 width=0.1 → bin_lo=0.5
    assert result_5[0]["bin_lo"] != result_10[0]["bin_lo"]


def test_calibration_bins_invalid_bins_param():
    """bins <= 0 returns empty list gracefully."""
    recs = [_rec("triggered", prob=0.5)]
    assert calibration_bins(recs, bins=0) == []
    assert calibration_bins(recs, bins=-1) == []


def test_brier_score_and_bins_consistent():
    """n in brier_score matches total n across all bins."""
    np.random.seed(42)
    recs = [_rec("triggered" if np.random.rand() > 0.5 else "missed",
                 prob=round(float(np.random.rand()), 2)) for _ in range(50)]
    bs = brier_score(recs)
    bins = calibration_bins(recs, bins=5)
    total_in_bins = sum(b["n"] for b in bins)
    assert bs["n"] == total_in_bins
