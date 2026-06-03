"""Thesis-scorecard: parse a narrative's watch block and grade it (no I/O)."""
from src import scorecard

NARRATIVE = """# Market Story — 2026-06-03
## What to watch
- stuff
```watch
[
  {"claim": "HY OAS widening flips to de-risking", "metric": "macro:BAMLH0A0HYM2", "trigger": ">2.85", "horizon": "next session"},
  {"claim": "10Y break above 4.5% pressures tech", "metric": "macro:DGS10", "trigger": ">4.5", "horizon": "next session"},
  {"claim": "WTI holds the bid", "metric": "market:CL=F:last", "trigger": ">95", "horizon": "next session"}
]
```
## Sources
"""

BRIEF = {
    "macro": [{"id": "BAMLH0A0HYM2", "name": "HY OAS", "latest": 2.71},
              {"id": "DGS10", "name": "10Y", "latest": 4.49}],
    "markets": {"commodities": [{"symbol": "CL=F", "name": "WTI", "last": 96.2}]},
}


def test_parse_watch_extracts_items():
    items = scorecard.parse_watch(NARRATIVE)
    assert len(items) == 3
    assert items[0]["metric"] == "macro:BAMLH0A0HYM2"


def test_parse_watch_empty_when_no_block():
    assert scorecard.parse_watch("no watch block here") == []
    assert scorecard.parse_watch("```watch\nnot json\n```") == []


def test_resolve_metric_macro_and_market():
    assert scorecard.resolve_metric(BRIEF, "macro:DGS10") == 4.49
    assert scorecard.resolve_metric(BRIEF, "market:CL=F:last") == 96.2
    assert scorecard.resolve_metric(BRIEF, "macro:NOPE") is None
    assert scorecard.resolve_metric(BRIEF, "garbage") is None


def test_evaluate_operators():
    assert scorecard._evaluate(4.49, ">4.5") is False
    assert scorecard._evaluate(4.49, "<4.5") is True
    assert scorecard._evaluate(2.71, ">=2.71") is True
    assert scorecard._evaluate(None, ">1") is None
    assert scorecard._evaluate(1.0, "bad") is None


def test_grade_and_summary():
    result = scorecard.score_prior(NARRATIVE, BRIEF)
    by_claim = {g["claim"]: g for g in result["graded"]}
    assert by_claim["HY OAS widening flips to de-risking"]["status"] == "watching"   # 2.71 not > 2.85
    assert by_claim["10Y break above 4.5% pressures tech"]["status"] == "watching"   # 4.49 not > 4.5
    assert by_claim["WTI holds the bid"]["status"] == "triggered"                    # 96.2 > 95
    assert result["summary"] == {"total": 3, "resolved": 3, "triggered": 1}


def test_parse_watch_tolerates_language_tag():
    txt = '```watch json\n[{"claim": "x", "metric": "macro:DGS10", "trigger": ">4"}]\n```'
    items = scorecard.parse_watch(txt)
    assert len(items) == 1 and items[0]["metric"] == "macro:DGS10"


def test_evaluate_rejects_non_finite():
    assert scorecard._evaluate(float("nan"), ">2.85") is None   # not a false 'watching'
    assert scorecard._evaluate(float("inf"), ">2.85") is None


def test_score_prior_handles_missing_narrative():
    res = scorecard.score_prior("", BRIEF)
    assert res["graded"] == [] and res["summary"]["total"] == 0
