"""Tests for news cleaning, noise filtering, and de-duplication."""

from src import news


def test_clean_strips_html_and_clamps():
    assert news._clean("<p>Hello <b>world</b></p>") == "Hello world"
    assert len(news._clean("x" * 500)) == 280


def test_is_noise_filings_link():
    assert news._is_noise({"link": "https://www.investing.com/news/filings/form-144", "author": ""})


def test_is_noise_blocked_author():
    assert news._is_noise({"link": "https://x.com/a", "author": "BNK Invest"})


def test_is_noise_allows_normal_item():
    assert not news._is_noise({"link": "https://cnbc.com/markets/story", "author": "Jane Doe"})


def test_normalize_dedupes_by_title():
    seen = set()
    first = news._normalize({"title": "Fed holds rates", "link": "a", "summary": ""}, "CNBC", seen)
    second = news._normalize({"title": "Fed holds rates", "link": "b", "summary": ""}, "WSJ", seen)
    assert first is not None
    assert second is None  # duplicate title dropped


def test_normalize_skips_empty_title():
    assert news._normalize({"title": "   ", "link": "a"}, "CNBC", set()) is None


def test_entry_time_interprets_struct_as_utc():
    import time as _time
    from datetime import timezone
    struct = _time.struct_time((2026, 6, 2, 12, 0, 0, 0, 0, 0))   # 2026-06-02 12:00 UTC
    dt = news._entry_time({"published_parsed": struct})
    assert dt is not None and dt.tzinfo == timezone.utc
    assert dt.isoformat() == "2026-06-02T12:00:00+00:00"          # not shifted by local offset
