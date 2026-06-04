#!/usr/bin/env python
"""One-command local setup for a fresh machine:

    python bootstrap.py

Installs dependencies and creates a `.env` from the template. Idempotent — safe to
re-run. After it, add your free keys to `.env` and run `python run.py`.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    if sys.version_info < (3, 11):
        print(f"! Python {sys.version_info.major}.{sys.version_info.minor} found; 3.11+ recommended.")

    print("Installing dependencies (pip install -r requirements.txt)...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")],
                   check=False)

    env, example = ROOT / ".env", ROOT / ".env.example"
    if env.exists():
        print(".env already exists — leaving it untouched.")
    elif example.exists():
        shutil.copyfile(example, env)
        print(f"Created .env from the template — paste your free keys (see the comments inside).")

    print("\nNext:")
    print("  python run.py                    # build today's brief")
    print("  python -m streamlit run app.py   # open the dashboard")
    print("  # then in `claude`:  narrate today's brief")
    print("\nNo install wanted? Use the hosted app — the URL is in README.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
