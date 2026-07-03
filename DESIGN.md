# DESIGN.md — iterating on the look

The site's styling lives in **one file: `src/site/static/style.css`** (copied to
`site/assets/style.css` by `build_site.py`). The whole palette/type system is driven by CSS
custom properties at the top (`:root { --bg, --accent, ... }`), so a one-line token change
retunes everything. The root-level `styles.css` is the original Ellis-dark token file the
static sheet was ported from — kept as the token reference the design skill and the email
digest mirror; the shipping stylesheet is the one under `src/site/static/`.

## The iteration loop (two speeds)

1. **Instant — browser DevTools.** Open `site/index.html`, press **F12** → **Elements → Styles**,
   select an element, and edit CSS live (zero rebuild). When it looks right, paste the rule into
   `src/site/static/style.css`. Use **F12 → Network → Fonts** to see loaded fonts; **Computed**
   for exact colors.
2. **Fast — edit + rebuild.** Edit `src/site/static/style.css`, rerun `python build_site.py`,
   refresh `site/index.html`. (Serve via `python -m http.server -d site` if you want the PWA/
   service-worker bits active.)

## Where each piece of "look" lives

| Layer | File | Notes |
|---|---|---|
| Stylesheet (type, cards, tabs, spacing) | `src/site/static/style.css` | the main lever; `:root` tokens up top |
| Chart accent / gridlines | `src/dashboard/charts.py` `LINE_COLOR`, plotly `gridcolor`/`fillcolor` | keep in sync with `--accent` |
| Plotly dark page theme | `src/site/render.py` `_themed()` | pins `template="none"` + the branded colorway — figures never inherit an import-side-effect template |
| The "Today's read" hero card | `src/site/render.py` `hero()` (used by `src/site/tabs/overview.py`) | inline HTML; accent left border, serif text |
| Page skeleton (masthead, tab bar, footer) | `src/site/templates/index.html.j2` | fonts loaded from Google Fonts here |

## Targeting the site's elements (stable class names)

The markup is our own (`src/site/render.py` + the Jinja template), so the selectors are
semantic class names that only change if `render.py` changes — no third-party DOM to chase:

`.panel` (titled section) · `.hero` / `.hero-tag` / `.hero-text` / `.hero-foot` (the read card) ·
`.kpi` / `.kpi-label` / `.kpi-value` / `.kpi-delta` (header KPI tiles) · `.cap` (captions) ·
`.chart` (+ `.spark-chart`; the inert figure JSON sits in `script.cdata`) · `.tbl` (Styler tables) ·
`.md` (rendered markdown) · `.grid` / `.grid-2` / `.grid-3` / `.grid-6` / `.grid-auto` ·
`.tabs` / `.tab` / `.tabpanel` (top tab nav) · `.masthead` / `.foot` · `details`/`summary`
(expanders) · tone classes `.up` / `.down` / `.flat`.

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
