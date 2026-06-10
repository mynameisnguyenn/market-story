"""Build the static market-story site from the latest committed brief.

    python build_site.py [out_dir]      # default: ./site

No network, no Streamlit — just renders the committed data to a self-contained site/
you can open as a file, host anywhere static, or install as a PWA on desktop/phone.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("STREAMLIT_LOGGER_LEVEL", "error")   # silence cache "no runtime" warnings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.site.build import build


def main() -> int:
    out = build(sys.argv[1] if len(sys.argv) > 1 else None)
    index = out / "index.html"
    print(f"Built static site -> {out}")
    print(f"  open: {index}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
