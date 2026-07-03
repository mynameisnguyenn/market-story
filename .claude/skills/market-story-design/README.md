# Market Story — Design System

A design system distilled from **Market Story**, a daily global-markets
intelligence tool built for a hedge-fund **risk analyst**. The product scrapes
free market data, macro series, and financial news every day, assembles a
structured **brief**, and turns it into a written **market story with a risk
lens** — gathered by a Python pipeline, rendered as a static site, *synthesized
by Claude*.

> "Markets, narrated. A daily global brief with a risk lens — gathered,
> synthesized, and built to be questioned and re-run."

This folder gives a design agent everything needed to build new, well-branded
Market Story surfaces — colors, type, fonts, iconography, the content voice, and
high-fidelity UI kit recreations of the actual product.

---

## Product context

Market Story is **two deliberately-split layers**:

1. **Gather + render** — a Python pipeline + a **static, framework-free site**
   (GitHub Pages): KPI strip, charts, sector treemap, rates/FX/commodities
   tables, a 70-headline feed, a cross-asset correlation matrix, and a "Trends"
   time-machine. No LLM here.
2. **Synthesize** — *Claude is the brain.* The pipeline writes a structured
   brief; the user asks Claude to narrate it. The written **read** is the actual
   product — the site is the evidence behind it.

The brief renders as a single page of seven tabs (Overview / Story / Equities &
Sectors / Global & Macro / Trends / Headlines / Calendar). A branded **cover**
fronts the brief.

### Surfaces (one language, two expressions)

| Surface | Where | Expression |
|---|---|---|
| **The site** ("Ellis-dark") | The product — the shipping static site (GitHub Pages / PWA) | Warm near-black, electric-cyan accent, serif headline over mono data. **The canonical system.** |
| **The cover** | The branded entry that flows into the dashboard (also deployable standalone as a marketing/OG page) | Same warm palette + cyan, expressed as a full-bleed cursor-reactive market-field behind a huge uppercase **Clash Display** wordmark. |

> **Unified.** Originally the cover was a separate GitHub-Pages splash in a
> cooler blue palette in front of the Streamlit app — an accident of tooling, not
> a design decision. It's now folded into the product as the dashboard's **cover**
> (one continuous experience, one palette). Both surfaces share the spine: a warm
> near-black ground, **exactly one green and one red** for every gain/loss cue,
> **mono numerals everywhere data lives**, and the **electric-cyan accent**. The
> cover differs only typographically (the uppercase Clash Display wordmark) and
> compositionally (the market-field hero) — never in color.

### Sources used to build this design system

- **GitHub repo:** <https://github.com/mynameisnguyenn/market-story> — explore it
  further to design with higher fidelity. Especially useful:
  - `src/site/static/style.css` — the Ellis-dark `:root` token system (the
    site's single design lever; ported from the original root `styles.css`).
  - `DESIGN.md` — the design rationale ("Current direction — Ellis-dark"),
    borrowed from [ellis.com](https://www.ellis.com/) and adapted to dark.
  - `src/site/` — the site render code (`render.py` HTML primitives: KPI cards,
    the "Today's read" hero, tables, tabs; `tabs/` — one module per tab).
  - `src/formatting.py` — the single source of truth for the green/red semantics.
  - `docs/index.html` + `docs/og.png` — the original splash and social card (the cover's source; re-skinned to the product palette here).
  - `data/narratives/narrative_*.md` — real written "reads" (the copy voice).
  - `CLAUDE.md` — how the narrative is written (tone, structure, the risk lens).

The live site: the GitHub Pages static site itself —
<https://mynameisnguyenn.github.io/market-story/> (no separate splash-plus-app split).

---

## CONTENT FUNDAMENTALS — how Market Story writes

The voice is a **sharp, senior buy-side risk analyst** talking to a peer. Dense,
declarative, numerate, faintly skeptical. It earns trust by being specific and
falsifiable, never breezy or promotional. Read `data/narratives/narrative_*.md`
and `CLAUDE.md` for the canonical voice.

**Tone & stance**
- Analytical and risk-first, not bullish or cheerful. The job is to find what
  could break, not to cheerlead the tape.
- **Falsifiable, not vague.** Every read states a thesis *and its flip condition*
  ("…it flips to 'geopolitical resolved' only if WTI recovers above $95 by the
  close"). Calls are graded against the next session ("0 hit / 1 inverted / 2 miss").
- Skeptical of consensus; explicitly names what the evidence *rules out*.
- Self-aware about data limits ("US equity prices are yesterday's close; commodity
  moves are live intraday").

**Person & address**
- Mostly **impersonal / third-person** about the market ("the curve is not
  steepening", "leveraged funds net short −458k contracts").
- Uses an implied **"you"** for the analyst's portfolio ("your Treasury hedge is
  broken", "the XLE hedge that saved the tape yesterday is gone"). Rarely "I/we".

**Casing & mechanics**
- **Sentence case** for product UI and prose. **UPPERCASE** is reserved for the
  marketing wordmark (MARKET STORY) and tiny mono eyebrows/labels.
- Tiny labels are uppercase mono with wide tracking: `TODAY'S READ`, `GATHER`,
  `S&P 500`, `SECTOR BREADTH`.
- Numbers are exact and signed: `+0.42%`, `−3.2%`, `+2 bps`, `4.491%`,
  `−458k contracts`, `3rd %ile`, `−2.05σ`. Tabular, mono, never rounded away.
- Em-dashes and semicolons carry the density; bullets each end on a **consequence**
  ("consequence: the XLE hedge … is gone").
- British-ish "colour" appears in code comments but UI copy is US English.

**Vocabulary** — the register is fluent markets jargon, used precisely: *risk
lens, regime, 2s10s, percentile/z-score, vol risk premium, draw/build, net long/
short, OAS, basis points, duration unwind, squeeze setup, mark-to-model.*

**Emoji** — used **sparingly as functional wayfinding markers only**, never
decoratively: `📈` data/charts, `📅` calendar/era, `⚡` "Today's signal",
`📋` scorecard, `🕰` time machine, `✏️` edit, `📚` Learn. Section dots use `●`.
Never emoji in the analytical prose itself. (The marketing splash uses **zero**
emoji.) When in doubt, omit.

**Example lines (verbatim, for calibration)**
- *"The oil floor broke while gold caught a simultaneous +$55 bid — that pairing
  is a demand-concern repricing, not an Iran-risk relief trade."*
- *"Public credit sees nothing. The private credit market has just shown a gate."*
- *"Risk is rich and hedges look cheap — VIX at 16 sits below 20-day realized vol."*
- Marketing: *"A terminal that tells the story."* · *"The part no dashboard gives you."*

---

## VISUAL FOUNDATIONS

### Mood
A **Bloomberg-terminal-at-night** seriousness, warmed up and de-cluttered. Calm,
expensive, data-forward. Near-black grounds make a single accent and the green/red
semantics pop. Nothing is rounded-and-friendly; nothing is loud. The serif
headline adds an editorial, "this is a written read" gravity that separates it
from a generic fintech dashboard.

### Color
- **Grounds are near-black, not grey.** Product = *warm* near-black `#0d0c0c`
  with warmer surfaces `#16120f` / `#1b1611`. The cover uses the same warm ground.
- **One accent, everywhere.** Electric cyan `#7beafb` (hover `#a6f1ff`) — across
  both the dashboard and the cover. It drives links, the metric-card left bar, the
  active tab underline, chart lines, the market-field accent line, focus rings —
  and almost nothing else. (The cover was once blue `#5aa0ff`; unified to cyan.)
- **One green, one red, everywhere.** `--up #36c26f` / `--down #ff5c6c` are the
  *single source of truth* (`src/formatting.py`) for every gain/loss cue: table
  cells, sparklines, signal dots, the treemap diverging scale, the correlation
  heatmap's −1 pole. Never introduce a second green or red.
- **VIX inverts.** For the VIX metric, down is good — its delta color is flipped.
- **Amber `#f5a623`** for caution only. **Neutral `#b3aaa0`** for unchanged/n/a.
- Diverging scales stay on-palette: red → warm-dark `#1b1611` → green (no
  off-brand RdYlGn yellow). The correlation matrix anchors +1 on **cyan**, not green.
- Knowledge-timeline categories have their own set (founding cyan, crash red,
  reform teal, innovation purple, boom orange) — from the retired Learn page;
  reuse only for educational/timeline surfaces.

### Type
- **Display = Instrument Serif** (product) — a high-contrast serif at weight 400,
  used large for H1 and for the "Today's read" hero line. Tight tracking `-.01em`.
  An editorial signature; the free near-equal of Ellis's *Atacama*.
- **Subheads = Space Grotesk** — H2/H3, metric labels, kickers. Weight 600, very
  tight negative tracking (H2 `-.03em`). Labels are uppercase, small, wide-tracked.
- **Data = IBM Plex Mono** — *all* numbers, with `font-variant-numeric: tabular-nums`
  so columns align. Also the kickers/eyebrows.
- **Marketing display = Clash Display** (uppercase, 500–700, line-height `.84`,
  letter-spacing `-.035em`) over **Cabinet Grotesk** body; IBM Plex Mono for tape
  + labels.
- Hierarchy is driven by **family + size**, not many weights. Serif vs grotesk vs
  mono does the heavy lifting.

### Spacing, shape, elevation
- **Corner radius is restrained: 10px** for cards/metrics/the hero (`--radius`).
  Marketing rows are flat with hairline rules — no rounding at all.
- **Borders over shadows.** The product uses **warm hairline borders** (`#2b2620`,
  hover `#3a332b`) to separate surfaces — essentially **no drop shadows** in the
  dashboard. (The marketing H1 has one soft text-shadow for depth; that's the
  exception.) Elevation is communicated by surface warmth + a 1px border, not blur.
- **The signature card detail: a 3px accent-colored LEFT border** on every metric
  card (4px on the read hero). This is the most recognizable Market Story motif.
- Generous block padding (`2rem` top), max content width ~1240px (product) /
  1500px (marketing). Tables are dense with small (`.84rem`) tabular type.
- Dividers are thin `1px` rules in `--grid #241f1a`.

### Backgrounds & texture
- **Flat near-black.** No gradients on product surfaces, no busy imagery.
- The **marketing splash** is the one place with motion + texture: a live
  full-bleed `<canvas>` drawing **today's real index paths** (faint grey lines +
  one bright accent S&P line with a gradient area-fill), a left-weighted
  scrim gradient for legibility, and a barely-there **SVG grain overlay**
  (`opacity ~.025`, `mix-blend-mode: overlay`). Subtle, not decorative.

### Animation & motion
- **Restrained and quick.** Product transitions are ~`.15s` on border-color (the
  card hover lift). No bounces, no spring, no infinite loops.
- The marketing splash has tasteful entrance animations: `rise` (20px up + fade,
  `.9s`) staggered on the H1/sub, and `f` (fade-only) on the kicker + tape; the
  canvas market-field draws in progressively. Respect `prefers-reduced-motion`.

### Hover / press states
- **Hover = border brightens** (metric card: left bar → `--accent-bright`, border
  → `--border-strong`). Links → `--accent-bright`. Marketing "Enter the brief"
  underline → accent, with its arrow nudging `+5px` right.
- Tabs: active tab text → accent, underline follows the primary color automatically.
- No documented dramatic press/active state — keep press subtle (slight dim) if needed.

### Transparency & blur
- Used **only for chart fills**: accent area-fills at very low alpha
  (`rgba(123,234,251,0.07)`), sparkline transparency, the marketing scrim. No
  frosted-glass / backdrop-blur panels anywhere. Solid surfaces are the norm.

### Layout rules
- Single column, max-width ~1240px, with a **top tab bar** (horizontally
  scrollable when it overflows). KPI strip of 6 metric cards across the top with
  **sparklines directly beneath each**. Tabbed content below. Two-column splits
  for table pairs (`.grid-2`).
- Mobile: a CSS grid breakpoint at 760px — the KPI strip drops 6 → 2 columns,
  3- and 6-column grids drop to 2, pairs stack to one; type/padding/tables shrink.

---

## ICONOGRAPHY

Market Story is **deliberately icon-light** — it leans on type, color, and tiny
mono labels rather than an icon set. There is **no custom icon font or SVG sprite**
in the product.

- **Material Symbols (Google Fonts CDN).** The designated icon system. The
  shipping site's tab nav uses plain text labels — no icons at all. If a new
  surface needs UI glyphs, match this set — **rounded/outlined Material
  Symbols**, thin stroke, sourced directly from the Google Fonts Material
  Symbols CDN.
- **Unicode glyphs as micro-icons.** Used inline throughout: `●` (signal/section
  dots, colored by semantic tone), `→` (links, "Enter the brief"), `▲ ▼ →`
  (directional change arrows, from `formatting.arrow()`), `↗` (external link),
  superscript `®` on the wordmark, `ᵗʰ` for "3rd %ile".
- **Functional emoji as wayfinding only** (see Content Fundamentals): `📈 📅 ⚡ 📋
  🕰 ✏️ 📚`. Never decorative, never in prose. Omit when unsure.
- **Charts are Plotly**, themed to the palette (accent line `#7beafb`, gridlines
  `#241f1a`, on-palette diverging treemap/heatmap, Sankey nodes in accent).
- **The "logo" is a wordmark**, not a mark: `MARKET STORY` (uppercase, Clash
  Display on marketing; the app title is "Market Story" with a `📈` page icon) with
  a superscript `®`. The favicon is a tiny inline SVG: a rounded-square dark tile
  with an accent up-and-to-the-right line chart.

Assets in `assets/`:
- `market-story-og.png` — the social/OG card (1200×630, **cyan**): the wordmark over
  the market-field. The best single reference image for the cover. Regenerated in
  the unified cyan palette (the original repo `og.png` was blue).
- `og-card.html` — the live, editable source for that card (real Clash Display
  wordmark + a static market-field draw). Re-export to refresh the PNG.

> If you need icons the product doesn't ship, use **Material Symbols** from the
> Google Fonts CDN — don't introduce a different family. The product itself
> ships no icon font or SVG sprite.

---

## Index — what's in this folder

| Path | What |
|---|---|
| `README.md` | This file — context, content & visual foundations, iconography, index. |
| `colors_and_type.css` | The token system: product (Ellis-dark) + marketing palettes, type families/scale, and semantic element styles. **Start here.** |
| `SKILL.md` | Agent-Skill front-matter wrapper so this system can be used in Claude Code. |
| `assets/` | Brand assets — `favicon.svg`, `app-icon-180/512.png`, `market-story-og.png` (cyan social card) + `og-card.html` (its editable source). |
| `preview/` | Small HTML cards rendered in the Design System tab (colors, type, components). |
| `ui_kits/dashboard/` | **The product.** High-fidelity recreation of the Ellis-dark Streamlit dashboard — KPI strip (with hover intraday popovers), the "Today's read" hero, data tables (with a day-change heat toggle), treemap, correlation matrix, yield curve, Sankey, tabs, sidebar. `index.html` + `app.jsx`. Live **Tweaks**: fonts / accent / ground (incl. Paper light mode) / density. | components. |
| `ui_kits/dashboard/` (cont.) | Now opens on the **cover** (cursor-reactive market-field + wordmark) that transitions into the dashboard; the dashboard carries a faint ambient field + scroll-reveal. |
| `ui_kits/landing/` | The **cover, standalone** — same warm/cyan palette, animated cursor-reactive market-field, live tape, "A terminal that tells the story" sections. Use when you want the cover a
| `ui_kits/email/` | The **daily-brief email digest** — a sendable, email-safe HTML layout (the read, KPI tape, signals, watch block). `index.html`. |
| `slides/` | A **branded slide deck** — 6 slides (title, section, the read, data, what-to-watch, closing) on the market-field motif. `index.html` (uses `deck-stage.js`). |s its own marketing/OG page. `index.html` + `field.js`. |

These `slides/` and `ui_kits/email/` surfaces don't ship with the product itself —
they're additional brand surfaces built on the same foundations.

### Fonts
All faces are free and CDN-hosted — these are the **real** product fonts, no
substitutions:
- **Google Fonts:** Instrument Serif, Space Grotesk, IBM Plex Mono.
- **Fontshare:** Clash Display, Cabinet Grotesk (marketing only).

`colors_and_type.css` imports them. (No local `fonts/` folder is needed — but if
you ship offline, self-host these from the same sources.)
