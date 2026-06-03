"""Central configuration: paths, instruments, news feeds, and macro series.

Everything downstream is driven by the lists here, so tuning coverage means
editing this file only. Symbols are validated against live sources before use.
"""

from __future__ import annotations

import json
from pathlib import Path

# --- Paths -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BRIEFS_DIR = DATA_DIR / "briefs"
NARRATIVES_DIR = DATA_DIR / "narratives"
RESULTS_DIR = PROJECT_ROOT / "results"
WATCHLIST_FILE = DATA_DIR / "watchlist.json"   # user's custom watchlist (gitignored)

for _d in (BRIEFS_DIR, NARRATIVES_DIR, RESULTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# --- Constants ---------------------------------------------------------------
TRADING_DAYS = 252
HISTORY_PERIOD = "1y"          # enough for YTD + 1w lookbacks + charts
NEWS_PER_FEED = 12
NEWS_MAX_TOTAL = 70
NEWS_TIMEOUT = 8               # seconds per feed
FRED_TIMEOUT = 15              # seconds per FRED series
# Drop feed noise: SEC filing items and algorithmic technical-alert spam.
NEWS_SKIP_LINK_SUBSTRINGS = ["/news/filings/"]
NEWS_SKIP_AUTHORS = ["BNK Invest"]
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0 Safari/537.36"
)

# --- Instruments: (symbol, display_name) -------------------------------------
US_EQUITIES = [
    ("^GSPC", "S&P 500"),
    ("^IXIC", "Nasdaq Composite"),
    ("^DJI", "Dow Jones"),
    ("^RUT", "Russell 2000"),
    ("^VIX", "VIX"),
]

SECTORS = [
    ("XLK", "Technology"),
    ("XLF", "Financials"),
    ("XLE", "Energy"),
    ("XLV", "Health Care"),
    ("XLI", "Industrials"),
    ("XLY", "Cons. Discretionary"),
    ("XLP", "Cons. Staples"),
    ("XLU", "Utilities"),
    ("XLB", "Materials"),
    ("XLRE", "Real Estate"),
    ("XLC", "Comm. Services"),
]

# Starter growth watchlist (Lone Pine-style large-cap growth/quality). Edit freely.
WATCHLIST = [
    ("NVDA", "NVIDIA"),
    ("MSFT", "Microsoft"),
    ("META", "Meta"),
    ("AMZN", "Amazon"),
    ("GOOGL", "Alphabet"),
    ("NFLX", "Netflix"),
    ("MELI", "MercadoLibre"),
    ("V", "Visa"),
    ("MA", "Mastercard"),
    ("CRM", "Salesforce"),
    ("TSM", "TSMC"),
    ("ASML", "ASML"),
]

GLOBAL_INDICES = [
    ("^STOXX50E", "Euro Stoxx 50"),
    ("^FTSE", "FTSE 100"),
    ("^GDAXI", "DAX"),
    ("^FCHI", "CAC 40"),
    ("^N225", "Nikkei 225"),
    ("^HSI", "Hang Seng"),
    ("000001.SS", "Shanghai Composite"),
]

# Yields. NOTE: Yahoo's ^TNX/^FVX/^TYX/^IRX are quoted directly in percent.
RATES = [
    ("^IRX", "13-Week T-Bill"),
    ("^FVX", "5Y Yield"),
    ("^TNX", "10Y Yield"),
    ("^TYX", "30Y Yield"),
]

FX = [
    ("DX-Y.NYB", "US Dollar Index"),
    ("EURUSD=X", "EUR/USD"),
    ("USDJPY=X", "USD/JPY"),
    ("GBPUSD=X", "GBP/USD"),
    ("USDCNY=X", "USD/CNY"),
]

COMMODITIES = [
    ("CL=F", "WTI Crude"),
    ("BZ=F", "Brent Crude"),
    ("GC=F", "Gold"),
    ("SI=F", "Silver"),
    ("HG=F", "Copper"),
    ("NG=F", "Nat Gas"),
]

CREDIT = [
    ("HYG", "HY Credit (HYG)"),
    ("LQD", "IG Credit (LQD)"),
    ("TLT", "20+Y Treasuries (TLT)"),
    ("AGG", "US Agg Bonds (AGG)"),
]

# group_key -> metadata. `kind` drives formatting (yields shown in bps, etc.).
MARKET_GROUPS = {
    "us_equities": {"label": "US Equities", "kind": "equity", "items": US_EQUITIES},
    "sectors": {"label": "US Sectors", "kind": "equity", "items": SECTORS},
    "watchlist": {"label": "Watchlist (growth)", "kind": "equity", "items": WATCHLIST},
    "global_indices": {"label": "Global Indices", "kind": "equity", "items": GLOBAL_INDICES},
    "rates": {"label": "Rates", "kind": "yield", "items": RATES},
    "fx": {"label": "FX", "kind": "fx", "items": FX},
    "commodities": {"label": "Commodities", "kind": "commodity", "items": COMMODITIES},
    "credit": {"label": "Credit & Bonds", "kind": "credit", "items": CREDIT},
}

# Symbols Yahoo serves unreliably -> stooq symbol fallback (filled from recon).
STOOQ_FALLBACK: dict[str, str] = {}


_watchlist_cache: tuple[tuple[str, float], list[tuple[str, str]]] | None = None


def get_watchlist() -> list[tuple[str, str]]:
    """The user's custom watchlist from WATCHLIST_FILE, or the default WATCHLIST.

    Cached by (path, mtime) so per-symbol loops don't re-read/parse the file.
    """
    global _watchlist_cache
    if not WATCHLIST_FILE.exists():
        return WATCHLIST
    try:
        key = (str(WATCHLIST_FILE), WATCHLIST_FILE.stat().st_mtime)
    except OSError:
        return WATCHLIST
    if _watchlist_cache is not None and _watchlist_cache[0] == key:
        return _watchlist_cache[1]
    try:
        raw = json.loads(WATCHLIST_FILE.read_text(encoding="utf-8"))
        items = [(d["symbol"].upper(), d.get("name") or d["symbol"].upper())
                 for d in raw if isinstance(d, dict) and d.get("symbol")]
        if items:
            _watchlist_cache = (key, items)
            return items
    except (json.JSONDecodeError, OSError, AttributeError, TypeError):
        pass
    return WATCHLIST


def save_watchlist(items: list[tuple[str, str]]) -> None:
    """Persist the custom watchlist as JSON (invalidates the read cache)."""
    global _watchlist_cache
    WATCHLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = [{"symbol": s, "name": n} for s, n in items]
    WATCHLIST_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    _watchlist_cache = None


def group_items(key: str) -> list[tuple[str, str]]:
    """Instruments for a market group, resolving the watchlist dynamically."""
    if key == "watchlist":
        return get_watchlist()
    return MARKET_GROUPS[key]["items"]


def all_symbols() -> list[str]:
    """Unique list of every instrument symbol across all groups."""
    seen: dict[str, None] = {}
    for key in MARKET_GROUPS:
        for symbol, _name in group_items(key):
            seen.setdefault(symbol, None)
    return list(seen)


def display_name(symbol: str) -> str:
    """Friendly name for a symbol, falling back to the symbol itself."""
    for key in MARKET_GROUPS:
        for sym, name in group_items(key):
            if sym == symbol:
                return name
    return symbol


# --- News feeds: (publisher, rss_url) ----------------------------------------
# All 12 validated LIVE on 2026-06-02. Excluded as dead/frozen: every WSJ
# feeds.a.dj.com feed (stale since Jan 2025), Reuters legacy (DNS gone),
# MarketWatch marketpulse (frozen content behind a fresh timestamp).
FEEDS = [
    ("CNBC Finance", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664"),
    ("CNBC Economy", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258"),
    ("MarketWatch Top Stories", "https://feeds.content.dowjones.io/public/rss/mw_topstories"),
    ("MarketWatch Bulletins", "https://feeds.content.dowjones.io/public/rss/mw_bulletins"),
    ("FT International", "https://www.ft.com/rss/home/international"),
    ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
    ("Investing.com Markets", "https://www.investing.com/rss/news_25.rss"),
    ("NYT Economy", "https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml"),
    ("Federal Reserve Press", "https://www.federalreserve.gov/feeds/press_all.xml"),
    ("Nasdaq Markets", "https://www.nasdaq.com/feed/rssoutbound?category=Markets"),
    ("BBC Business", "http://feeds.bbci.co.uk/news/business/rss.xml"),
    ("Seeking Alpha", "https://seekingalpha.com/market_currents.xml"),
]

# --- FRED macro series: (series_id, display_name) -----------------------------
# Curated risk-analyst set; pulled keyless via fredgraph CSV (no API key needed).
FRED_SERIES = [
    ("DGS10", "10Y Treasury Yield"),
    ("DGS2", "2Y Treasury Yield"),
    ("T10Y2Y", "10Y-2Y Spread"),
    ("T10Y3M", "10Y-3M Spread"),
    ("EFFR", "Effective Fed Funds Rate"),
    ("SOFR", "SOFR (secured funding)"),
    ("T10YIE", "10Y Breakeven Inflation"),
    ("BAMLH0A0HYM2", "HY Credit Spread (OAS)"),
    ("BAMLC0A0CM", "IG Credit Spread (OAS)"),
    ("NFCI", "Chicago Fed Financial Conditions"),
    ("VIXCLS", "VIX (close)"),
    ("DTWEXBGS", "Broad USD Index"),
    ("CPIAUCSL", "CPI (all items)"),
    ("PCEPILFE", "Core PCE Price Index"),
    ("UNRATE", "Unemployment Rate"),
    ("PAYEMS", "Nonfarm Payrolls"),
    ("ICSA", "Initial Jobless Claims"),
    ("INDPRO", "Industrial Production"),
]

# FRED keyless CSV endpoint (no API key required).
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
