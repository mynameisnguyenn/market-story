# Landing UI kit — the cover (standalone)

The **cover** as its own page. In the unified system the cover is normally the
branded entry that flows straight into the dashboard (see `ui_kits/dashboard/`);
this kit is that same cover deployed **standalone** — useful as a marketing / OG
page, or as a fast front door in front of a slow-booting hosted app (which is why
the real product shipped it as a separate GitHub-Pages splash).

It now shares the **product palette** — warm near-black `#0d0c0c` + electric-cyan
`#7beafb` (originally a cooler blue; unified). A huge uppercase **Clash Display**
wordmark sits over a **cursor-reactive** full-bleed **market-field** canvas.

Open `index.html`.

## What's here

| File | Role |
|---|---|
| `index.html` | The splash markup — top bar, hero wordmark, live tape, the "A terminal that tells the story" sections, footer. |
| `landing.css` | The marketing stylesheet (cooler palette, Clash Display / Cabinet Grotesk / IBM Plex Mono). |
| `field.js` | The cursor-reactive `<canvas>` market-field (synthetic index walks — no network), the UTC clock, and the tape values. |

## Faithful to the source, with deliberate changes

- **Unified palette.** Re-skinned from the original cool blue to the product's
  warm near-black + cyan, so the cover and dashboard read as one brand.
- **Cursor parallax.** The market-field lines drift toward the cursor (by depth),
  a continuous-rAF technique layered onto the original draw-in.
- **Synthetic data.** The real splash fetched the latest committed brief JSON from
  GitHub for real index paths + live tape. This kit uses seeded random walks and
  static sample values so it runs offline. The drawing logic is otherwise a port.
- **Entrance animation fill-mode.** Default fill (base state visible) so the hero
  never renders blank if the animation is interrupted. `prefers-reduced-motion`
  is respected.

## Signature details

- **Uppercase wordmark**, `line-height:.84`, `letter-spacing:-.035em`, with one
  soft `text-shadow` for depth (the rare shadow in this system).
- **IBM Plex Mono** for everything small: the kicker (`№ 20260604 — MARKETS,
  NARRATED.`), the tape, the section labels (`GATHER / SYNTHESIZE / COMPOUND`),
  the footer.
- **Left-weighted scrim** gradient over the canvas for legibility; a barely-there
  **SVG grain** overlay (`opacity ~.025`, `mix-blend-mode: overlay`).
- The accent S&P line gets a gradient area-fill + a glowing end-dot; the other
  index lines are faint grey.
- Hover: "Enter the brief" underline → accent, arrow nudges `+5px`.

> The OG/social card (`assets/market-story-og.png` at the project root) is the
> still-frame reference for this exact composition.
