"""Financial-history eras — the structured spine of the learning layer.

A curated, dated timeline of US market regimes (dotcom, GFC, ZIRP, Euro debt, COVID,
the inflation shock...). The app shades these on the trend charts and the `/finance`
learning agent reads them (plus the deep prose in `knowledge/eras/<key>.md`) to teach the
history. `end: None` means "ongoing". Pure data + small helpers, no I/O.
"""
from __future__ import annotations

# Each era: key, name, [start, end), regime, the Fed's stance, and a one-line hook.
# The deep narrative for each lives in knowledge/eras/<key>.md.
ERAS = [
    {"key": "dotcom", "name": "Dotcom boom & bust", "start": "1998-01-01", "end": "2002-10-31",
     "regime": "bubble → bust", "fed": "hiked to 6.5% by 2000, then cut to 1.75% in 2001",
     "blurb": "Internet mania and 'irrational exuberance'; the Nasdaq peaks Mar 2000 and falls ~78%; 9/11; the 2001 recession."},
    {"key": "housing-boom", "name": "Housing boom & easy money", "start": "2002-11-01", "end": "2007-06-30",
     "regime": "expansion / credit boom", "fed": "1% in 2003–04, then hiked to 5.25% by 2006",
     "blurb": "Ultra-low rates fuel a housing and credit bubble; subprime + securitization; the Greenspan→Bernanke handoff."},
    {"key": "gfc", "name": "Global Financial Crisis", "start": "2007-07-01", "end": "2009-06-30",
     "regime": "systemic crisis", "fed": "cut to 0–0.25% (ZIRP) and launched QE1",
     "blurb": "Subprime implosion → Bear Stearns (Mar '08), Lehman (Sep '08), AIG, TARP; the Fed to zero + first QE; the ARRA stimulus."},
    {"key": "zirp-qe", "name": "ZIRP & QE recovery", "start": "2009-07-01", "end": "2015-11-30",
     "regime": "reflation / easy money", "fed": "0% with QE1/2/3 and Operation Twist",
     "blurb": "Zero rates and balance-sheet expansion drive a long, slow recovery; the 2013 'taper tantrum'; low growth, low inflation."},
    {"key": "euro-debt", "name": "European sovereign-debt crisis", "start": "2010-04-01", "end": "2012-09-30",
     "regime": "crisis (Europe)", "fed": "ECB-led; Draghi's 'whatever it takes' (Jul 2012)",
     "blurb": "Greece/PIIGS, bailouts and redenomination fears; Draghi's pledge + OMT backstop the euro. (Overlaps ZIRP in the US.)"},
    {"key": "normalization", "name": "Liftoff & normalization", "start": "2015-12-01", "end": "2020-02-29",
     "regime": "gradual tightening", "fed": "hiked 0→2.5% (2015–18), QT, then 2019 'insurance' cuts",
     "blurb": "The first hikes since the GFC and balance-sheet runoff; the Q4-2018 selloff forces a dovish 2019 pivot."},
    {"key": "covid", "name": "COVID crash & response", "start": "2020-03-01", "end": "2021-03-31",
     "regime": "crisis → all-in stimulus", "fed": "back to ZIRP + unlimited QE",
     "blurb": "The fastest-ever bear market (Mar 2020), then the largest combined monetary+fiscal response in history (CARES Act $2T+)."},
    {"key": "inflation", "name": "Post-COVID inflation & tightening", "start": "2021-04-01", "end": "2023-10-31",
     "regime": "inflation shock / tightening", "fed": "hiked 0→5.5%, the fastest pace since the 1980s",
     "blurb": "Reopening + stimulus + supply shocks push CPI to ~9% (2022); the fastest hiking cycle in 40 years; the 2022 bear market."},
    {"key": "higher-for-longer", "name": "Higher-for-longer", "start": "2023-11-01", "end": None,
     "regime": "restrictive / disinflation", "fed": "holding near a ~5.5% peak",
     "blurb": "Disinflation without recession (so far); a deeply inverted curve; the soft-landing debate. The current regime."},
]


def era_for(date_str: str) -> dict | None:
    """The era a YYYY-MM-DD date falls in (first match; eras can overlap). None if before 1998."""
    if not date_str:
        return None
    for era in ERAS:
        end = era["end"] or "9999-99-99"
        if era["start"] <= date_str <= end:
            return era
    return None


def bands():
    """[(start, end, name)] for shading charts; open-ended eras clipped to None."""
    return [(e["start"], e["end"], e["name"]) for e in ERAS]


_STRESS_WORDS = ("crisis", "bust", "shock")


def stress_bands():
    """[(start, end, name)] for the stress/crisis eras only — faint red regions on the charts."""
    return [(e["start"], e["end"], e["name"]) for e in ERAS
            if any(w in e["regime"] for w in _STRESS_WORDS)]
