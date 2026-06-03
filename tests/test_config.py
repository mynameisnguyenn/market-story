"""Tests for the custom-watchlist persistence in config (no Streamlit runtime)."""

from src import config


def test_get_watchlist_defaults_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "WATCHLIST_FILE", tmp_path / "none.json")
    assert config.get_watchlist() == config.WATCHLIST


def test_save_and_get_watchlist_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "WATCHLIST_FILE", tmp_path / "wl.json")
    items = [("NVDA", "NVIDIA"), ("ASML", "ASML")]
    config.save_watchlist(items)
    assert config.get_watchlist() == items


def test_get_watchlist_falls_back_on_corrupt(tmp_path, monkeypatch):
    path = tmp_path / "wl.json"
    path.write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(config, "WATCHLIST_FILE", path)
    assert config.get_watchlist() == config.WATCHLIST


def test_group_items_uses_custom_watchlist(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "WATCHLIST_FILE", tmp_path / "wl.json")
    config.save_watchlist([("TSM", "TSMC")])
    assert config.group_items("watchlist") == [("TSM", "TSMC")]
    assert config.group_items("sectors") == config.MARKET_GROUPS["sectors"]["items"]
    assert "TSM" in config.all_symbols()


def test_get_watchlist_reflects_save_after_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "WATCHLIST_FILE", tmp_path / "wl.json")
    config.save_watchlist([("AAA", "Alpha")])
    assert config.get_watchlist() == [("AAA", "Alpha")]   # populates the cache
    config.save_watchlist([("BBB", "Beta")])              # must invalidate it
    assert config.get_watchlist() == [("BBB", "Beta")]
