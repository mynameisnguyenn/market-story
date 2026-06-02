"""Entry point: gather market data + macro + news, then write today's brief.

    python run.py

Writes data/briefs/brief_<date>.json and .md. After running, launch the
dashboard (`python -m streamlit run app.py`) and ask Claude to narrate.
"""

from __future__ import annotations

from src import brief as brief_mod


def main() -> int:
    print("Fetching market data, macro series, and news (this takes ~20-40s)...")
    brief = brief_mod.build_brief(fetch=True)
    json_path, md_path = brief_mod.save_brief(brief)

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
