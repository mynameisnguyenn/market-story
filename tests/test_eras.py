"""Financial-history era index (pure data + helpers)."""
from src import eras


def test_era_for_known_dates():
    assert eras.era_for("2008-10-15")["key"] == "gfc"
    assert eras.era_for("2020-03-20")["key"] == "covid"
    assert eras.era_for("2000-03-10")["key"] == "dotcom"
    assert eras.era_for("2011-06-01")["key"] == "euro-debt"           # nested era wins over zirp-qe
    assert eras.era_for("2014-01-02")["key"] == "zirp-qe"             # outside euro-debt -> zirp-qe
    assert eras.era_for("2026-06-04")["key"] == "higher-for-longer"   # end=None -> ongoing
    assert eras.era_for("1990-01-01") is None                         # before the index starts
    assert eras.era_for("") is None


def test_bands_and_stress_bands():
    assert len(eras.bands()) == len(eras.ERAS)
    stress = {n for _, _, n in eras.stress_bands()}
    assert any("Financial Crisis" in n for n in stress)
    assert any("COVID" in n for n in stress)
    assert not any("ZIRP" in n for n in stress)                       # easy era is not "stress"


def test_every_era_has_a_knowledge_file():
    import pathlib
    here = pathlib.Path(__file__).resolve().parents[1] / "knowledge" / "eras"
    for e in eras.ERAS:
        assert (here / f"{e['key']}.md").exists(), f"missing knowledge file for {e['key']}"
