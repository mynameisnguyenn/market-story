"""Entry point: gather market data + macro + news, then write today's brief.

    python run.py

Writes data/briefs/brief_<date>.json and .md. After running, launch the
dashboard (`python -m streamlit run app.py`) and ask Claude to narrate.
"""

from __future__ import annotations

from src import brief as brief_mod
from src import ledger


def main() -> int:
    print("Fetching market data, macro series, and news (this takes ~20-40s)...")
    brief = brief_mod.build_brief(fetch=True)
    json_path, md_path = brief_mod.save_brief(brief)

    try:                                              # grade matured watch calls as archives refresh
        s = ledger.backfill_from_narratives()
        rate = "n/a" if s["hit_rate"] is None else f"{s['hit_rate'] * 100:.0f}%"
        print(f"Ledger: {s['triggered']} hit / {s['missed']} miss / {s['pending']} pending | hit-rate {rate}")
        ledger.log_stances_from_narratives()          # paper P&L: log new stances, settle matured
        ledger.settle_stances()
        ss = ledger.stance_stats()
        if ss["n_logged"]:
            wr = "n/a" if ss["win_rate"] is None else f"{ss['win_rate'] * 100:.0f}%"
            print(f"Stance: {ss['n_directional']} directional settled | win-rate {wr} | "
                  f"{ss['n_flat']} flat | {ss['n_omitted']} omitted")
    except Exception as exc:
        print(f"Ledger update skipped: {exc}")

    stats = brief["stats"]
    print(f"\nBrief written:\n  {json_path}\n  {md_path}")
    print(
        f"\nVIX {stats.get('vix')!r} | sectors up/down "
        f"{stats.get('sector_advancers')}/{stats.get('sector_decliners')} | "
        f"{len(brief['news'])} headlines"
    )
    print("\nNext:")
    print("  python -m streamlit run app.py")
    print("  then in claude:  narrate today's brief   (or /narrate)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
