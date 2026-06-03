"""Fetch speculative positioning from the CFTC Commitments of Traders report.

The Traders in Financial Futures (TFF) report breaks futures open interest into
who holds it: dealers, asset managers (real money), and leveraged funds (hedge
funds / specs). The signal a risk analyst watches is the leveraged-fund NET
position and its week-over-week change — e.g. specs sitting net short E-mini S&P
is a squeeze/positioning risk. Pulled keyless from the CFTC public Socrata API;
best-effort, returns [] on failure so the panel simply hides.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import requests

TFF_URL = "https://publicreporting.cftc.gov/resource/gpe5-46if.json"
CFTC_TIMEOUT = 20
CFTC_UA = "market-story (https://github.com/mynameisnguyenn/market-story)"

# (exact contract_market_name, display_name). Risk-relevant financial futures.
CFTC_CONTRACTS = [
    ("E-MINI S&P 500", "S&P 500 (e-mini)"),
    ("NASDAQ MINI", "Nasdaq-100 (e-mini)"),
    ("VIX FUTURES", "VIX futures"),
    ("ULTRA UST 10Y", "Ultra 10Y Treasury"),
    ("ULTRA UST BOND", "Ultra T-Bond"),
]


def fetch_cftc(contracts: list[tuple[str, str]] = CFTC_CONTRACTS) -> list[dict]:
    """Latest speculative-positioning snapshot for each contract. Best-effort."""
    with ThreadPoolExecutor(max_workers=min(8, len(contracts) or 1)) as pool:
        futures = {pool.submit(_fetch_latest, cm): (cm, name) for cm, name in contracts}
        rows_by_contract = {}
        for future, (cm, name) in futures.items():
            try:
                rows_by_contract[cm] = future.result()
            except Exception:
                rows_by_contract[cm] = None
    return [_snapshot(name, rows_by_contract.get(cm)) for cm, name in contracts]


def _fetch_latest(contract_market_name: str, timeout: int = CFTC_TIMEOUT) -> dict | None:
    """Most recent weekly report row for one contract. None on any failure."""
    params = {
        "$where": f"contract_market_name='{contract_market_name}'",
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$limit": "1",
    }
    try:
        resp = requests.get(TFF_URL, params=params,
                            headers={"User-Agent": CFTC_UA}, timeout=timeout)
        resp.raise_for_status()
        rows = resp.json()
    except Exception:
        return None
    return rows[0] if rows else None


def _num(row: dict, key: str):
    try:
        return float(str(row.get(key)).replace(",", ""))
    except (TypeError, ValueError, AttributeError):
        return None


def _net(long_v, short_v):
    if long_v is None or short_v is None:
        return None
    return long_v - short_v


def _snapshot(name: str, row: dict | None) -> dict:
    """Leveraged-fund net position (+ weekly change) and asset-manager net."""
    if not row:
        return {"name": name, "lev_net": None, "lev_net_chg": None,
                "asset_net": None, "oi": None, "date": None}
    lev_net = _net(_num(row, "lev_money_positions_long"), _num(row, "lev_money_positions_short"))
    lev_chg = _net(_num(row, "change_in_lev_money_long"), _num(row, "change_in_lev_money_short"))
    asset_net = _net(_num(row, "asset_mgr_positions_long"), _num(row, "asset_mgr_positions_short"))
    date = row.get("report_date_as_yyyy_mm_dd")
    return {
        "name": name,
        "lev_net": lev_net,
        "lev_net_chg": lev_chg,
        "asset_net": asset_net,
        "oi": _num(row, "open_interest_all"),
        "date": date[:10] if isinstance(date, str) else None,
    }
