---
name: market-story-design
description: Use this skill to generate well-branded interfaces and assets for Market Story — a daily global-markets intelligence tool with a risk lens — for production or for throwaway prototypes/mocks. Contains the design guidelines, colors, type, fonts, iconography, content voice, and UI kit components (the Ellis-dark dashboard + the marketing splash) needed to design in this brand.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files:

- `colors_and_type.css` — the token system (product "Ellis-dark" palette + marketing palette, type families/scale, semantic element styles). Start here.
- `README.md` — product context, **content fundamentals** (the risk-analyst voice), **visual foundations**, and **iconography**.
- `preview/` — small specimen cards (colors, type, spacing, components).
- `ui_kits/dashboard/` — the product: a high-fidelity recreation of the Ellis-dark Streamlit dashboard (KPI strip, the "Today's read" hero, data tables, treemap, tabs, sidebar).
- `ui_kits/landing/` — the marketing splash recreation (animated market-field, uppercase wordmark, live tape).
- `ui_kits/email/` — a sendable daily-brief email digest (email-safe HTML).
- `slides/` — a branded 6-slide deck (title, section, the read, data, watch, closing) built on `deck-stage.js`.
- `assets/` — brand assets (`favicon.svg`, app icons, `market-story-og.png`).

Two surfaces share one DNA but diverge: build the **dashboard / Ellis-dark** system (warm near-black, electric-cyan accent, Instrument Serif over IBM Plex Mono) unless you're making a landing page, in which case use the **marketing** palette (cooler black, blue accent, Clash Display). Keep the spine intact everywhere: one green / one red for gain/loss, mono numerals for all data, borders not shadows, the 3px accent left-bar on cards.

If creating visual artifacts (slides, mocks, throwaway prototypes), copy assets out and create static HTML files for the user to view. If working on production code, copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without other guidance, ask them what they want to build or design, ask a few questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.
