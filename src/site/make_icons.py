"""Generate the PWA app icons (icon-192.png, icon-512.png) into src/site/static/.

A warm near-black rounded tile with the electric-cyan accent rising line — the brand mark,
so the installed app gets a real icon on desktop/phone. Run once; committed thereafter.
    python -m src.site.make_icons
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

_STATIC = Path(__file__).resolve().parent / "static"
_BG = (13, 12, 12)          # --bg  #0d0c0c
_PANEL = (22, 18, 15)       # --surface
_ACCENT = (123, 234, 251)   # --accent #7beafb


def _icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(size * 0.22)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=_BG)
    # inset panel
    pad = int(size * 0.12)
    d.rounded_rectangle([pad, pad, size - pad, size - pad], radius=int(r * 0.6), fill=_PANEL)
    # a rising sparkline (the market line)
    w = max(2, int(size * 0.035))
    pts_x = [0.24, 0.38, 0.50, 0.62, 0.78]
    pts_y = [0.66, 0.58, 0.69, 0.46, 0.34]
    pts = [(size * x, size * y) for x, y in zip(pts_x, pts_y)]
    d.line(pts, fill=_ACCENT, width=w, joint="curve")
    # end dot
    ex, ey = pts[-1]
    rr = int(size * 0.035)
    d.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=_ACCENT)
    return img


def main() -> int:
    _STATIC.mkdir(parents=True, exist_ok=True)
    for size in (192, 512):
        _icon(size).save(_STATIC / f"icon-{size}.png")
    print(f"wrote icon-192.png, icon-512.png -> {_STATIC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
