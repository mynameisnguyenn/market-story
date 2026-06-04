"""Track 13F-HR institutional holdings from SEC EDGAR — "follow the smart money".

Quarterly long US-equity holdings of prominent managers, plus the quarter-over-quarter
change (NEW / added / trimmed / EXITED) — the closest public view of big-fund flow.

CAVEATS (state them when surfacing): longs only (no shorts; only listed puts/calls show),
US-listed 13F securities only, and a ~45-day lag after quarter-end. Best-effort — any fetch
failure yields None/[] and never crashes the dashboard.
"""
from __future__ import annotations

import re

import requests

from . import edgar_data

# Curated prominent 13F filers (display name, 10-digit CIK).
FUNDS = [
    ("Berkshire Hathaway · Buffett", "0001067983"),
    ("Scion Asset Mgmt · Burry", "0001649339"),
    ("Pershing Square · Ackman", "0001336528"),
    ("Bridgewater Associates", "0001350694"),
    ("Renaissance Technologies", "0001037389"),
    ("Citadel Advisors", "0001423053"),
    ("Appaloosa · Tepper", "0001656456"),
    ("Tiger Global", "0001167483"),
    ("Duquesne · Druckenmiller", "0001536411"),
    ("Soros Fund Mgmt", "0001029160"),
]
_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"
_INDEX = "https://www.sec.gov/Archives/edgar/data/{cik}/{accno}/index.json"
_FILE = "https://www.sec.gov/Archives/edgar/data/{cik}/{accno}/{name}"
F13_TIMEOUT = 20


def _get(url: str):
    return requests.get(url, headers={"User-Agent": edgar_data._user_agent(),
                                      "Accept-Encoding": "gzip, deflate"}, timeout=F13_TIMEOUT)


def _num(text):
    try:
        return float(str(text).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def parse_infotable(xml: str) -> dict:
    """{CUSIP: {issuer, cusip, value, shares}} aggregated across sub-manager lines. Pure.
    Keyed by CUSIP (stable per security) so issuer-name spelling changes between filings
    don't show up as a fake EXIT + NEW for the same stock."""
    out: dict[str, dict] = {}
    for block in re.findall(r"<(?:\w+:)?infoTable>(.*?)</(?:\w+:)?infoTable>", xml or "", re.DOTALL):
        def field(tag):
            m = re.search(rf"<(?:\w+:)?{tag}>(.*?)</(?:\w+:)?{tag}>", block, re.DOTALL)
            return m.group(1).strip() if m else None
        issuer = field("nameOfIssuer")
        cusip = (field("cusip") or "").upper()
        if not cusip and not issuer:
            continue
        key = cusip or issuer.upper()
        agg = out.setdefault(key, {"issuer": issuer, "cusip": cusip, "value": 0.0, "shares": 0.0})
        agg["value"] += _num(field("value"))
        agg["shares"] += _num(field("sshPrnamt"))
        if issuer and not agg.get("issuer"):
            agg["issuer"] = issuer
    return _normalize_units(out)


def _normalize_units(holdings: dict) -> dict:
    """Most filers report `value` in dollars (post-2023), but some still use THOUSANDS. Detect
    via the implied price (value/shares) — a sub-dollar median means thousands — and scale x1000
    so every fund is comparable in real dollars."""
    prices = sorted(h["value"] / h["shares"] for h in holdings.values()
                    if h["shares"] > 0 and h["value"] > 0)
    if len(prices) >= 5 and prices[len(prices) // 2] < 1.0:   # median implied price < $1 -> thousands
        for h in holdings.values():
            h["value"] *= 1000.0
    return holdings


def diff_holdings(latest: dict, prior: dict, limit: int = 12) -> list[dict]:
    """Quarter-over-quarter moves, largest first: NEW / added / trimmed / EXITED."""
    moves = []
    for key, h in latest.items():
        pv = prior.get(key, {}).get("value", 0.0)
        if pv <= 0:
            moves.append({"issuer": h["issuer"], "action": "NEW", "delta": h["value"]})
        elif h["value"] >= pv * 1.15:
            moves.append({"issuer": h["issuer"], "action": "added", "delta": h["value"] - pv})
        elif h["value"] <= pv * 0.85:
            moves.append({"issuer": h["issuer"], "action": "trimmed", "delta": h["value"] - pv})
    for key, h in prior.items():
        if key not in latest:
            moves.append({"issuer": h["issuer"], "action": "EXITED", "delta": -h["value"]})
    return sorted(moves, key=lambda m: abs(m["delta"]), reverse=True)[:limit]


def _latest_13f(cik: str, n: int = 2) -> list[tuple[str, str]]:
    """[(filing_date, accession_no), ...] for the n most recent 13F-HR. [] on failure."""
    try:
        rec = _get(_SUBMISSIONS.format(cik=cik)).json().get("filings", {}).get("recent", {})
    except Exception:
        return []
    forms, dates, accns = rec.get("form", []), rec.get("filingDate", []), rec.get("accessionNumber", [])
    out = []
    for i, form in enumerate(forms):
        if form == "13F-HR":
            out.append((dates[i] if i < len(dates) else "", accns[i] if i < len(accns) else ""))
            if len(out) >= n:
                break
    return out


def _holdings(cik: str, accno: str) -> dict:
    """Parse the information-table XML for one 13F filing. {} on failure."""
    accno_clean = accno.replace("-", "")
    try:
        items = _get(_INDEX.format(cik=int(cik), accno=accno_clean)).json()["directory"]["item"]
    except Exception:
        return {}
    name = next((it["name"] for it in items
                 if it["name"].lower().endswith(".xml") and "primary_doc" not in it["name"].lower()), None)
    if not name:
        return {}
    try:
        xml = _get(_FILE.format(cik=int(cik), accno=accno_clean, name=name)).text
    except Exception:
        return {}
    return parse_infotable(xml)


def fetch_fund(name: str, cik: str, top_n: int = 10) -> dict | None:
    """Latest 13F holdings + the quarter-over-quarter flow for one manager. None on failure."""
    filings = _latest_13f(cik, 2)
    if not filings:
        return None
    latest = _holdings(cik, filings[0][1])
    if not latest:
        return None
    prior = _holdings(cik, filings[1][1]) if len(filings) > 1 else {}
    total = sum(h["value"] for h in latest.values()) or 1.0
    top = sorted(latest.values(), key=lambda h: h["value"], reverse=True)[:top_n]
    return {
        "name": name, "date": filings[0][0], "positions": len(latest), "total_value": total,
        "top": [{"issuer": h["issuer"], "value": h["value"], "pct": h["value"] / total * 100} for h in top],
        "changes": diff_holdings(latest, prior),
    }
