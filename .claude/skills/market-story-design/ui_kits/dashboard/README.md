# Dashboard UI kit — Market Story (Ellis-dark)

A high-fidelity, click-through recreation of the **Market Story Streamlit
dashboard** — the product itself. Built from the repo's `app.py`, `styles.css`,
and `.streamlit/config.toml`, so the look is lifted from source, not a screenshot.

Open `index.html`. You land on the **cover** — a cursor-reactive market-field
behind the wordmark; "Enter the brief" transitions you into a faithful "Daily
Brief" view with working tab navigation, a sidebar page switch (Daily Brief ↔
Learn the Markets), a filterable headline feed, an expandable scorecard, and a
"Refresh data" affordance.

## Motion (added in the unified pass)

- **Cover → dashboard** as one document — the landing is folded in as the entry,
  not a separate page. The cover fades/scales out as the dashboard fades in.
- **Cursor-reactive market-field** (`field.js`, `window.startMarketField`) —
  prominent on the cover, and a faint **ambient** layer drifting behind the
  dashboard. Index lines parallax by depth toward the cursor. The field draws
  **fully on first paint** (no progressive draw-in) so the hero is never blank;
  only the parallax is live.
- **Scroll-reveal** (`Reveal`) — panels fade/rise in. Above-the-fold content
  reveals immediately and there's a safety timeout, so nothing can stay hidden if
  IntersectionObserver doesn't fire. Respects `prefers-reduced-motion`.

## UX & accessibility (A+ pass)

- **Keyboard & a11y:** tabs are a real `role="tablist"` with arrow/Home/End key
  navigation, roving `tabindex`, and `aria-selected`; the panel is an
  `aria-labelledby` tabpanel. Sidebar nav are `<button>`s with `aria-current`.
  A **skip-to-content** link, visible **`:focus-visible`** rings, an `aria-busy`
  refresh button, and `aria-live` status text round it out.
- **Loading state:** the **Refresh data** button shows a top **load bar** + a
  **skeleton shimmer** over the KPI strip while data "loads."
- **Empty state:** the Headlines filter shows a styled empty state with a
  **Clear filter** recovery when nothing matches.
- **Notice & error states:** a dismissible **freshness banner** (authentic to the
  product's "pre-open prices are stale" caveat) and an **`ErrorBox`** (shown if the
  brief data fails to load) with a Retry.
- **Ambient control:** a sidebar **Off / Low / High** segmented control tunes the
  ambient field; the choice persists in `localStorage`. `prefers-reduced-motion`
  freezes the parallax automatically.

## Tweaks — explore design directions live

Toggle **Tweaks** from the toolbar to open an in-product panel
(`tweaks-panel.jsx`) that re-skins the dashboard instantly via CSS variables:

- **Font pairing** — `Editorial` (Instrument Serif · Space Grotesk · IBM Plex
  Mono — the default), `Terminal` (Space Grotesk · Space Mono — no serif, pure
  terminal), `Broadsheet` (Newsreader · Hanken Grotesk · JetBrains Mono —
  newspaper-finance), `Swiss` (Archivo — bold, modern). The Clash Display
  wordmark stays fixed; data always stays mono.
- **Accent** — cyan (default), amber, violet, coral. Drives the UI *and* the
  ambient market-field line.
- **Ground** — Warm / Cool / True black near-black variants.
- **Density** — Comfortable / Compact (a denser, Bloomberg-wire feel).

Defaults live in the `TWEAK_DEFAULTS` block in `index.html`; the apply logic is a
single `useEffect` that sets `--serif/--grot/--mono`, `--accent`, the ground
vars, and a `data-density` attribute. Add a direction by extending the `FONTS` /
`ACCENTS` / `GROUNDS` maps.

## What's here

| File | Role |
|---|---|
| `index.html` | Mounts the app (React 18 + Babel). Cover + ambient field + sidebar + header + KPI strip + tabs. |
| `dashboard.css` | The Ellis-dark stylesheet — tokens mirror the repo's `styles.css`; plus cover, ambient, and reveal styles. |
| `field.js` | `window.startMarketField(canvas, opts)` — the cursor-reactive market-field engine (cover + ambient). |
| `data.js` | Sample brief (`window.MS_DATA`), values lifted from `narrative_2026-06-04.md`. |
| `app.jsx` | **All components, one file** (bundled for reliable single-fetch loading): shell (`Sidebar`, `Header`, `KpiStrip`, `Sparkline`, `ReadHero`, `Signals`, `Tabs`, `Reveal`, `Cover`), charts (`SectorTreemap`, `CorrMatrix`, `YieldCurve`, `Sankey`), tab panels, and the `StoryTab` + `LearnPage`. Edit the sections in place. |

## Screens covered

- **Overview** — the "Today's thesis" serif hero, the signal strip, leaders/laggards, the S&P area chart.
- **Story** — the written narrative with a gradeable watch-scorecard (the product's reason for being).
- **Equities & Sectors** — a squarified **sector treemap** (sized by index weight, on-palette diverging color) + dense data tables.
- **Global & Macro** — risk-regime cells, rates/FX/credit tables, the FRED percentile table, the **Treasury yield curve**, and the cyan-anchored **cross-asset correlation matrix**.
- **Trends** — small-multiple anchor charts with percentile labels.
- **Headlines** — the filterable RSS feed.
- **Calendar** — econ releases + cross-asset extremes.
- **Learn the Markets** — the history timeline with category-colored nodes, **the investment clock** (radial growth/inflation regime map with a "now" needle), **anatomy of a yield** (real + breakeven decomposition), **who owns the market** (composition bar), and two **Sankey** diagrams (money flow + Fed policy transmission).

## Signature details to preserve

- **3px cyan accent left-bar** on every KPI metric card (4px on the read hero).
- **Mono numerals** (`IBM Plex Mono`, tabular) for every value; **serif** (`Instrument
  Serif`) for headlines + the read; **grotesk** (`Space Grotesk`) for subheads/labels.
- **One green / one red** for all change cues; **VIX delta inverts**.
- Borders, not shadows. Hover brightens the border. 10px radii.

## Building with it

Compose screens from the exported components (all on `window`). Swap `MS_DATA`
to re-skin with different markets. The components are cosmetic recreations — they
don't fetch or compute; wire real data in if you need a live surface.

> Charts here are hand-built SVG/CSS — a squarified treemap, a cyan-anchored
> correlation matrix, the yield curve, sparklines, and a layered Sankey — standing
> in for the product's Plotly figures, on the exact palette (accent line
> `#7beafb`, gridlines `#241f1a`, on-palette diverging scales).
