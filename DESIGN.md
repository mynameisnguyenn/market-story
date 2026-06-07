# DESIGN.md — iterating on the look

The dashboard's styling lives in **one file: `styles.css`** (loaded by `app.py`'s `_load_css()`).
Edit it, save, and the app reloads — no Python-string escaping. The whole palette/type system is
driven by CSS custom properties at the top of `styles.css` (`:root { --bg, --accent, ... }`), so a
one-line token change retunes everything.

## The iteration loop (three speeds)

1. **Instant — browser DevTools.** Run the app, press **F12** → **Elements → Styles**, select an
   element, and edit CSS live (zero reload). When it looks right, paste the rule into `styles.css`.
   Use **F12 → Network → Fonts** to see loaded fonts; **Computed** for exact colors.
2. **Fast — edit + save.** `runOnSave = true` (`.streamlit/config.toml`), so saving `styles.css`
   (touch `app.py` if a CSS-only save doesn't trigger a rerun) repaints the app.
3. **Isolated — the sandbox.** `python -m streamlit run style_lab.py` renders every component
   (headline, metrics, table, tabs, chart, the "Today's read" card, controls) on one screen, so you
   tune the design system without clicking through tabs. It loads the same `styles.css`.

## Where each piece of "look" lives

| Layer | File | Notes |
|---|---|---|
| Stylesheet (type, cards, tabs, spacing) | `styles.css` | the main lever; `:root` tokens up top |
| Theme (app bg, sidebar, text, primary) | `.streamlit/config.toml` `[theme]` | `primaryColor` drives tab underline + widgets |
| Chart accent / gridlines | `src/dashboard/charts.py` `LINE_COLOR`, plotly `gridcolor`/`fillcolor` | keep in sync with `--accent` |
| The "Today's read" hero card | `src/dashboard/panels/overview.py` `signals_strip()` | inline HTML; uses `var(--surface)` etc. |
| Knowledge-graph colors | `src/learn.py` `NODE_COLOR` / `CATEGORY_COLORS` | |

## Targeting Streamlit elements (stable selectors)

CSS overrides hook Streamlit's `data-testid` attributes (confirm exact names in DevTools for your
version — currently Streamlit 1.58):

`[data-testid="stMetric"]` · `stMetricValue` · `stMetricLabel` · `stMetricDelta` ·
`[data-testid="stDataFrame"]` · `[data-testid="stTabs"] button[role="tab"]` (and `[aria-selected="true"]`) ·
`section[data-testid="stSidebar"]` · `[data-testid="stExpander"]` · `.block-container` · `h1/h2/h3` · `a`.

> Selectors can shift across Streamlit versions — pin the version, and re-check in DevTools after upgrades.

## Current direction — "Ellis-dark"

Borrowed from [ellis.com](https://www.ellis.com/) (a Next.js/Tailwind/Vercel site), adapted to dark:

- **Accent** electric cyan `#7beafb` (was `#4C9AFF`)
- **Semantics** ONE green `#36C26F` (`--up`) / ONE red `#FF5C6C` (`--down`) for every gain/loss cue —
  tables, sparklines, the hero, signal dots, treemap, correlation — sourced from `src/formatting.py`
- **Palette** warm near-black `#0d0c0c` bg, warm cards `#16120f`, warm off-white `#f5f2ef` text
- **Type** serif display headline (Instrument Serif ~ Ellis's *Atacama*) over mono data (IBM Plex Mono),
  grotesk subheads (Space Grotesk) with tight negative tracking
- **Shape** 10px card radii, cyan accent bar on metric cards

What deliberately did **not** come from Ellis: its paid fonts (Monument Grotesk / Atacama — free
near-equals used instead) and its marketing-site genre (3D hero renders, scroll motion).
