"""13F parsing + quarter-over-quarter diff (pure, no network)."""
from src import thirteenf

INFOTABLE = """
<informationTable>
<infoTable><nameOfIssuer>APPLE INC</nameOfIssuer><cusip>037833100</cusip><value>1000</value>
  <shrsOrPrnAmt><sshPrnamt>10</sshPrnamt></shrsOrPrnAmt></infoTable>
<infoTable><nameOfIssuer>APPLE INC</nameOfIssuer><cusip>037833100</cusip><value>500</value>
  <shrsOrPrnAmt><sshPrnamt>5</sshPrnamt></shrsOrPrnAmt></infoTable>
<infoTable><nameOfIssuer>COCA COLA CO</nameOfIssuer><cusip>191216100</cusip><value>800</value>
  <shrsOrPrnAmt><sshPrnamt>8</sshPrnamt></shrsOrPrnAmt></infoTable>
</informationTable>"""


def test_parse_infotable_aggregates_by_cusip():
    h = thirteenf.parse_infotable(INFOTABLE)
    assert h["037833100"]["value"] == 1500 and h["037833100"]["shares"] == 15   # two Apple lines summed
    assert h["037833100"]["issuer"] == "APPLE INC"
    assert h["191216100"]["value"] == 800


def test_parse_infotable_namespaced_and_empty():
    ns = ('<ns1:infoTable><ns1:nameOfIssuer>X</ns1:nameOfIssuer><ns1:cusip>123</ns1:cusip>'
          '<ns1:value>9</ns1:value></ns1:infoTable>')
    assert thirteenf.parse_infotable(ns)["123"]["value"] == 9
    assert thirteenf.parse_infotable("") == {}


def test_diff_holdings_classifies_moves():
    latest = {"A": {"issuer": "A", "value": 200}, "B": {"issuer": "B", "value": 100},
              "C": {"issuer": "C", "value": 50}}
    prior = {"A": {"issuer": "A", "value": 100}, "B": {"issuer": "B", "value": 100},
             "D": {"issuer": "D", "value": 80}}
    moves = {m["issuer"]: m["action"] for m in thirteenf.diff_holdings(latest, prior)}
    assert moves["A"] == "added"      # 200 vs 100 (>+15%)
    assert moves["C"] == "NEW"        # absent from prior
    assert moves["D"] == "EXITED"     # gone from latest
    assert "B" not in moves           # ~unchanged within the band
