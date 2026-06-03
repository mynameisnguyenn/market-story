"""Recent SEC filings for the watchlist via the keyless EDGAR REST API.

SEC requires a descriptive User-Agent identifying the caller; a missing UA
returns 403, and the fair-access limit is 10 requests/second per IP. We send a
compliant UA (override with SEC_USER_AGENT in .env) and pace requests. The
two-step flow: company_tickers.json maps ticker -> CIK, then
data.sec.gov/submissions/CIK<10-digit>.json lists recent filings. Best-effort.
"""
from __future__ import annotations

import os
import time

import requests

from . import config

_DEFAULT_UA = "market-story dashboard https://github.com/mynameisnguyenn/market-story"


def _resolve_ua() -> str:
    """SEC User-Agent from env var, then .env, else the default (env > .env > default)."""
    ua = os.environ.get("SEC_USER_AGENT")
    if ua:
        return ua
    env_path = config.PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            name, sep, value = line.strip().partition("=")
            if sep and name.strip() == "SEC_USER_AGENT" and value.strip():
                return value.strip()
    return _DEFAULT_UA


_ua_cache: str | None = None


def _user_agent() -> str:
    """Resolved UA, cached after first use (resolved lazily so env set at
    startup — e.g. bridged from Streamlit Cloud secrets — is honored)."""
    global _ua_cache
    if _ua_cache is None:
        _ua_cache = _resolve_ua()
    return _ua_cache


TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
EDGAR_TIMEOUT = 12
MATERIAL_FORMS = ("8-K", "10-Q", "10-K", "6-K", "S-1", "424B")

_cik_cache: dict[str, str] | None = None


def _headers() -> dict:
    return {"User-Agent": _user_agent(), "Accept-Encoding": "gzip, deflate"}


def _ticker_cik_map() -> dict[str, str]:
    """{TICKER: 10-digit CIK} from SEC's ticker file (fetched once, cached)."""
    global _cik_cache
    if _cik_cache is not None:
        return _cik_cache
    try:
        resp = requests.get(TICKERS_URL, headers=_headers(), timeout=EDGAR_TIMEOUT)
        resp.raise_for_status()
        raw = resp.json()
    except Exception:
        return {}
    out = {}
    for entry in raw.values():
        ticker = str(entry.get("ticker", "")).upper()
        if ticker:
            out[ticker] = str(entry.get("cik_str", "")).zfill(10)
    _cik_cache = out
    return out


def _form_matches(form: str, forms) -> bool:
    """Family match so amendments and prospectuses aren't silently dropped:
    '10-K/A' -> '10-K' (keep amendments); '424B5' -> '424B' (prefix for prospectuses)."""
    if not forms:
        return True
    base = str(form).split("/")[0]                 # drop the amendment suffix (/A)
    return base in forms or (base.startswith("424B") and "424B" in forms)


def _filings_for_cik(cik: str, forms, per_symbol: int) -> list[dict]:
    """Recent filings for one CIK (newest-first), filtered to `forms`."""
    try:
        resp = requests.get(SUBMISSIONS_URL.format(cik=cik), headers=_headers(), timeout=EDGAR_TIMEOUT)
        resp.raise_for_status()
        recent = resp.json().get("filings", {}).get("recent", {})
    except Exception:
        return []
    forms_list = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accns = recent.get("accessionNumber", [])
    docs = recent.get("primaryDocument", [])
    descs = recent.get("primaryDocDescription", [])
    cik_int = int(cik)
    out = []
    for i, form in enumerate(forms_list):
        if not _form_matches(form, forms):
            continue
        accno = accns[i] if i < len(accns) else ""
        doc = docs[i] if i < len(docs) else ""
        if not accno:                          # ragged payload -> no usable link; skip
            continue
        out.append({
            "form": form,
            "date": dates[i] if i < len(dates) else "",
            "desc": (descs[i] if i < len(descs) else "") or form,
            "link": f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{accno.replace('-', '')}/{doc}",
        })
        if len(out) >= per_symbol:
            break
    return out


def recent_filings(symbols, forms=MATERIAL_FORMS, per_symbol: int = 4) -> list[dict]:
    """Recent EDGAR filings for each symbol, newest-first. Best-effort, paced."""
    cik_map = _ticker_cik_map()
    rows = []
    for sym in symbols:
        cik = cik_map.get(str(sym).upper())
        if not cik:
            continue
        for filing in _filings_for_cik(cik, forms, per_symbol):
            rows.append({"symbol": str(sym).upper(), **filing})
        time.sleep(0.15)   # stay well under SEC's 10 req/s fair-access limit
    rows.sort(key=lambda r: r["date"], reverse=True)
    return rows
