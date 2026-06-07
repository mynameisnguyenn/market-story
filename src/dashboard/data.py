"""Cached data loaders + the brief/closes plumbing for the dashboard.

Every loader is an `@st.cache_data` wrapper over a plain `src.*` fetch/read, so the
panels never hit the network or re-parse a committed archive on a Streamlit rerun.
The functions are imported by name elsewhere, so `app.get_fred_history.clear()` (used in
the render-smoke test) and a panel's `get_fred_history()` reference the same object.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import streamlit as st

from src import brief as brief_mod
from src import (bls_data, brief_access, calendar_data, cftc_data, config, edgar_data,
                 eia_data, ledger, macro_data, market_data, news, thesis, thirteenf, timeline)


@st.cache_data(ttl=900, show_spinner="Loading the latest brief...")
def get_data(nonce: int):
    """Return (brief_dict, {symbol: close Series}).

    Instant load: on first paint (nonce 0) serve the last saved/committed brief
    from disk — charts rebuilt from its embedded history, no live network pull.
    The 'Refresh data' button (nonce>0) does the live fetch.
    """
    if nonce == 0:
        saved = brief_mod.load_latest_brief()
        if saved and saved.get("markets"):
            return saved, brief_mod.closes_from_brief(saved)
    return _fetch_live()


def _fetch_live():
    """Live pull of everything (concurrent), persisted so the next load is instant."""
    with ThreadPoolExecutor(max_workers=3) as pool:
        fut_history = pool.submit(market_data.download_history, config.all_symbols())
        fut_macro = pool.submit(macro_data.fetch_macro)
        fut_news = pool.submit(news.fetch_news)
        history = fut_history.result()
        macro = fut_macro.result()
        news_items = fut_news.result()
    sections = market_data.build_market_sections(history)
    brief = brief_mod.build_brief(history, sections, macro, news_items,
                                  bls=get_bls(), energy=get_energy(),
                                  positioning=get_positioning(), fetch=False)
    closes = {symbol: frame["Close"] for symbol, frame in history.items()}
    return brief, closes


@st.cache_data(ttl=21600, show_spinner=False)
def get_bls() -> list[dict]:
    """BLS prints, cached 6h — monthly data, and keeps us under the keyless daily cap."""
    return bls_data.fetch_bls()


@st.cache_data(ttl=21600, show_spinner=False)
def get_energy() -> list[dict]:
    """EIA weekly inventories, cached 6h — the report only updates once a week."""
    return eia_data.fetch_eia()


@st.cache_data(ttl=21600, show_spinner=False)
def get_positioning() -> list[dict]:
    """CFTC speculative positioning, cached 6h — the COT report is weekly (Fri)."""
    return cftc_data.fetch_cftc()


@st.cache_data(ttl=21600, show_spinner=False)
def get_energy_history() -> list[dict]:
    """Full committed EIA weekly history — cached so the Macro tab doesn't re-read the archive."""
    return eia_data.load_history()


@st.cache_data(ttl=21600, show_spinner=False)
def get_fred_history() -> list[dict]:
    """Full committed FRED history (data/history/macro.jsonl), cached per render."""
    return macro_data.load_fred_history()


@st.cache_data(ttl=21600, show_spinner=False)
def get_bls_history() -> list[dict]:
    """Full committed BLS history (data/history/labor.jsonl), cached per render."""
    return bls_data.load_bls_history()


@st.cache_data(ttl=900, show_spinner=False)
def get_running_thesis() -> str | None:
    """The standing cross-session running thesis (data/running_thesis.md), cached per render."""
    return thesis.load_running_thesis()


@st.cache_data(ttl=900, show_spinner=False)
def get_ledger():
    """The prediction ledger records + running track-record stats, cached per render."""
    return ledger.load(), ledger.stats()


@st.cache_data(ttl=900, show_spinner=False)
def get_timeline_df():
    """The committed cross-asset metrics timeline as a DataFrame, cached per render — the
    Trends tab reads ~7k rows; don't re-parse the whole file on every Streamlit rerun."""
    return timeline.load_df()


def persist(brief: dict) -> None:
    """Save the brief to disk once per refresh so Claude can read it."""
    stamp = brief.get("generated_at_utc")
    if st.session_state.get("_saved_stamp") != stamp:
        brief_mod.save_brief(brief)
        st.session_state["_saved_stamp"] = stamp


@st.cache_data(ttl=3600, show_spinner="Fetching upcoming earnings dates...")
def get_earnings(symbols: tuple) -> list[dict]:
    """Cached upcoming-earnings lookup for a set of symbols."""
    return calendar_data.fetch_earnings(list(symbols))


@st.cache_data(ttl=21600, show_spinner="Fetching recent SEC filings...")
def get_filings(symbols: tuple) -> list[dict]:
    """Cached recent-EDGAR-filings lookup for the watchlist (6h)."""
    return edgar_data.recent_filings(list(symbols))


@st.cache_data(ttl=21600, show_spinner=False)
def get_econ() -> list[dict]:
    """Upcoming key economic releases (FRED schedule), cached 6h."""
    return calendar_data.fetch_econ_releases()


@st.cache_data(ttl=86400, show_spinner="Pulling the 13F filing...")
def get_13f(name: str, cik: str) -> dict | None:
    """A manager's latest 13F holdings + Q/Q flow, cached 24h (filings are quarterly)."""
    return thirteenf.fetch_fund(name, cik)


def row_for(brief: dict, symbol: str) -> dict | None:
    """First market row whose 'symbol' matches (shared accessor in brief_access)."""
    return brief_access.market_row(brief, symbol)
