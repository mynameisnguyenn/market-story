"""Tests for SEC EDGAR filing retrieval (requests mocked, no network)."""
from src import edgar_data

_TICKERS = {
    "0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."},
    "1": {"cik_str": 1045810, "ticker": "NVDA", "title": "NVIDIA CORP"},
}
_SUBMISSIONS = {"filings": {"recent": {
    "form": ["8-K", "4", "10-Q"],
    "filingDate": ["2026-05-20", "2026-05-19", "2026-05-01"],
    "accessionNumber": ["0000320193-26-000050", "0000320193-26-000049", "0000320193-26-000045"],
    "primaryDocument": ["aapl-8k.htm", "form4.xml", "aapl-10q.htm"],
    "primaryDocDescription": ["8-K", "FORM 4", "10-Q"],
}}}


class _Resp:
    def __init__(self, payload): self._p = payload
    def raise_for_status(self): pass
    def json(self): return self._p


def _route(url, **kwargs):
    return _Resp(_TICKERS if "company_tickers" in url else _SUBMISSIONS)


def test_ticker_cik_map_zero_pads(monkeypatch):
    edgar_data._cik_cache = None
    monkeypatch.setattr(edgar_data.requests, "get", _route)
    m = edgar_data._ticker_cik_map()
    assert m["AAPL"] == "0000320193" and m["NVDA"] == "0001045810"


def test_recent_filings_filters_builds_link_and_sorts(monkeypatch):
    edgar_data._cik_cache = None
    monkeypatch.setattr(edgar_data.requests, "get", _route)
    monkeypatch.setattr(edgar_data.time, "sleep", lambda s: None)
    rows = edgar_data.recent_filings(["AAPL"], forms=("8-K", "10-Q"), per_symbol=4)
    forms = [r["form"] for r in rows]
    assert "4" not in forms and "8-K" in forms and "10-Q" in forms     # Form 4 filtered out
    eightk = next(r for r in rows if r["form"] == "8-K")
    assert eightk["link"] == ("https://www.sec.gov/Archives/edgar/data/"
                              "320193/000032019326000050/aapl-8k.htm")
    assert [r["date"] for r in rows] == sorted([r["date"] for r in rows], reverse=True)


def test_recent_filings_best_effort_on_failure(monkeypatch):
    edgar_data._cik_cache = None

    def _boom(*a, **k):
        raise RuntimeError("network down")
    monkeypatch.setattr(edgar_data.requests, "get", _boom)
    assert edgar_data.recent_filings(["AAPL"]) == []     # degrades, no raise
