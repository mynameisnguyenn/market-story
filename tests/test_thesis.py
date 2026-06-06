"""Running-thesis loader — synthetic file on a tmp path, no network."""
from src import thesis


def _seed(tmp_path, monkeypatch, text):
    p = tmp_path / "running_thesis.md"
    p.write_text(text, encoding="utf-8")
    monkeypatch.setattr(thesis, "RUNNING_THESIS_PATH", p)


def test_load_and_sections(tmp_path, monkeypatch):
    _seed(tmp_path, monkeypatch,
          "# Running Thesis\n\n## Current thesis\nFragility regime; flips if OAS >2.80.\n\n"
          "## Regime\nHigher-for-longer.\n\n## Lessons / WHYs\n- Read the cluster.\n")
    assert "Fragility regime" in thesis.load_running_thesis()
    assert thesis.current_thesis() == "Fragility regime; flips if OAS >2.80."
    assert thesis.section("regime") == "Higher-for-longer."          # case-insensitive
    assert thesis.section("Nonexistent") is None


def test_missing_file_returns_none(tmp_path, monkeypatch):
    monkeypatch.setattr(thesis, "RUNNING_THESIS_PATH", tmp_path / "absent.md")
    assert thesis.load_running_thesis() is None
    assert thesis.current_thesis() is None
