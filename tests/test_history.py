"""Tests for day-over-day snapshot persistence (temp SQLite, no network)."""
from src import history


def _brief(d, levels):
    return {
        "date": d,
        "markets": {"us_equities": [{"symbol": s, "last": v} for s, v in levels.items()]},
        "stats": {},
    }


def test_save_and_previous_snapshot(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "DB_PATH", tmp_path / "h.db")
    history.save_today(_brief("2026-06-01", {"^GSPC": 5000.0}))
    history.save_today(_brief("2026-06-02", {"^GSPC": 5050.0}))
    prev = history.previous_snapshot("2026-06-02")
    assert prev is not None and prev[0] == "2026-06-01"
    assert prev[1]["levels"]["^GSPC"] == 5000.0


def test_save_today_upserts_same_date(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "DB_PATH", tmp_path / "h.db")
    history.save_today(_brief("2026-06-02", {"^GSPC": 5000.0}))
    history.save_today(_brief("2026-06-02", {"^GSPC": 5075.0}))  # same date -> overwrite
    history.save_today(_brief("2026-06-01", {"^GSPC": 4900.0}))
    prev = history.previous_snapshot("2026-06-03")
    assert prev[0] == "2026-06-02" and prev[1]["levels"]["^GSPC"] == 5075.0


def test_deltas_vs_prior(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "DB_PATH", tmp_path / "h.db")
    history.save_today(_brief("2026-06-01", {"^GSPC": 5000.0, "^VIX": 20.0}))
    result = history.deltas(_brief("2026-06-02", {"^GSPC": 5050.0, "^VIX": 18.0}), ["^GSPC", "^VIX"])
    assert result is not None
    prior_date, rows = result
    assert prior_date == "2026-06-01"
    gspc = next(r for r in rows if r["symbol"] == "^GSPC")
    assert gspc["change"] == 50.0 and abs(gspc["change_pct"] - 1.0) < 1e-9


def test_deltas_none_without_prior(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "DB_PATH", tmp_path / "h.db")
    assert history.deltas(_brief("2026-06-02", {"^GSPC": 5050.0}), ["^GSPC"]) is None
