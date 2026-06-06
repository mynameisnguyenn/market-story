/* @ds-bundle: {"format":3,"namespace":"MarketStoryDesignSystem_181a31","components":[],"sourceHashes":{"slides/deck-stage.js":"eac2199dccb4","slides/slide-field.js":"1b11c3b4118d","ui_kits/dashboard/app.jsx":"91d87322292e","ui_kits/dashboard/data.js":"908a6de6a19f","ui_kits/dashboard/field.js":"c846d8bd9523","ui_kits/dashboard/tweaks-panel.jsx":"6591467622ed","ui_kits/landing/field.js":"f4f5c85a703e"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.MarketStoryDesignSystem_181a31 = window.MarketStoryDesignSystem_181a31 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// slides/deck-stage.js
try { (() => {
// @ds-adherence-ignore -- omelette starter scaffold (raw elements/hex/px by design)
/* BEGIN USAGE */
/**
 * <deck-stage> — reusable web component for HTML decks.
 *
 * Handles:
 *  (a) speaker notes — reads <script type="application/json" id="speaker-notes">
 *      and posts {slideIndexChanged: N} to the parent window on nav.
 *  (b) keyboard navigation — ←/→, PgUp/PgDn, Space, Home/End, number keys.
 *      On touch devices, tapping the left/right half of the stage goes
 *      prev/next — taps on links, buttons and other interactive slide
 *      content are left alone.
 *  (c) press R to reset to slide 0 (with a tasteful keyboard hint).
 *  (d) bottom-center overlay showing slide count + hints, fades out on idle.
 *  (e) auto-scaling — inner canvas is a fixed design size (default 1920×1080)
 *      scaled with `transform: scale()` to fit the viewport, letterboxed.
 *      Set the `noscale` attribute to render at authored size (1:1) — the
 *      PPTX exporter sets this so its DOM capture sees unscaled geometry.
 *  (f) print — `@media print` lays every slide out as its own page at the
 *      design size, so the browser's Print → Save as PDF produces a clean
 *      one-page-per-slide PDF with no extra setup.
 *  (g) thumbnail rail — resizable left-hand column of per-slide thumbnails
 *      (static clones). Click to navigate; ↑/↓ with a thumbnail focused to
 *      step between slides; drag to reorder; right-click for
 *      Skip / Move up / Move down / Delete (opens a Cancel/Delete confirm
 *      dialog). Drag the rail's right edge to resize; width persists to
 *      localStorage. Skipped slides carry `data-deck-skip`, are dimmed in
 *      the rail, omitted from prev/next navigation, and hidden at print.
 *      The rail is suppressed in presenting mode, in the host's Preview
 *      mode (ViewerMode='none'), on `noscale`, on narrow viewports
 *      (≤640px), and via the `no-rail` attribute. Rail mutations dispatch
 *      a `deckchange`
 *      CustomEvent on the element: detail = {action, from, to, slide}.
 *
 * Slides are HIDDEN, not unmounted. Non-active slides stay in the DOM with
 * `visibility: hidden` + `opacity: 0`, so their state (videos, iframes,
 * form inputs, React trees) is preserved across navigation.
 *
 * Lifecycle event — the component dispatches a `slidechange` CustomEvent on
 * itself whenever the active slide changes (including the initial mount).
 * The event bubbles and composes out of shadow DOM, so you can listen on
 * the <deck-stage> element or on document:
 *
 *   document.querySelector('deck-stage').addEventListener('slidechange', (e) => {
 *     e.detail.index         // new 0-based index
 *     e.detail.previousIndex // previous index, or -1 on init
 *     e.detail.total         // total slide count
 *     e.detail.slide         // the new active slide element
 *     e.detail.previousSlide // the prior slide element, or null on init
 *     e.detail.reason        // 'init' | 'keyboard' | 'click' | 'tap' | 'api'
 *   });
 *
 * Persistence: none at the deck level. The host app keeps the current slide
 * in its own URL (?slide=) and re-delivers it via location.hash on load, so a
 * bare load with no hash always starts at slide 1.
 *
 * Usage:
 *   <style>deck-stage:not(:defined){visibility:hidden}</style>
 *   <deck-stage width="1920" height="1080">
 *     <section data-label="Title">...</section>
 *     <section data-label="Agenda">...</section>
 *   </deck-stage>
 *   <script src="deck-stage.js"></script>
 *
 * The :not(:defined) rule prevents a flash of the first slide at its
 * authored styles before this script runs and attaches the shadow root.
 *
 * Slides are the direct element children of <deck-stage>. Each slide is
 * automatically tagged with:
 *   - data-screen-label="NN Label"   (1-indexed, for comment flow)
 *   - data-om-validate="no_overflowing_text,no_overlapping_text,slide_sized_text"
 *
 * Speaker notes stay in sync because the component posts {slideIndexChanged: N}
 * to the parent — just include the #speaker-notes script tag if asked for notes.
 *
 * Authoring guidance:
 *   - Write slide bodies as static HTML inside <deck-stage>, with sizing via
 *     CSS custom properties in a <style> block rather than JS constants.
 *     Static slide markup is what lets the user click a heading in edit mode
 *     and retype it directly; a slide rendered through <script type="text/babel">,
 *     React, or a loop over a JS array has to round-trip every tweak through a
 *     chat message instead. Reach for script-generated slides only when the
 *     content genuinely needs interactive behaviour static HTML can't express.
 *   - Do NOT set position/inset/width/height on the slide <section> elements —
 *     the component absolutely positions every slotted child for you.
 *   - Entrance animations: make the visible end-state the base style and
 *     animate *from* hidden, so print and reduced-motion show content.
 *     Gate the animation on [data-deck-active] and the motion query, e.g.
 *     `@media (prefers-reduced-motion:no-preference){ [data-deck-active] .x{animation:fade-in .5s both} }`.
 *     Avoid infinite decorative loops on slide content.
 */
/* END USAGE */

(() => {
  const DESIGN_W_DEFAULT = 1920;
  const DESIGN_H_DEFAULT = 1080;
  const OVERLAY_HIDE_MS = 1800;
  const VALIDATE_ATTR = 'no_overflowing_text,no_overlapping_text,slide_sized_text';
  const FINE_POINTER_MQ = matchMedia('(hover: hover) and (pointer: fine)');
  const NARROW_MQ = matchMedia('(max-width: 640px)');
  // Slide-authored controls that should keep a tap instead of it navigating.
  const INTERACTIVE_SEL = 'a[href], button, input, select, textarea, summary, label, video[controls], audio[controls], [role="button"], [onclick], [tabindex]:not([tabindex^="-"]), [contenteditable]:not([contenteditable="false" i])';
  const pad2 = n => String(n).padStart(2, '0');

  // Label precedence: data-label → data-screen-label (number stripped) → first heading → "Slide".
  const getSlideLabel = el => {
    const explicit = el.getAttribute('data-label');
    if (explicit) return explicit;
    const existing = el.getAttribute('data-screen-label');
    if (existing) return existing.replace(/^\s*\d+\s*/, '').trim() || existing;
    const h = el.querySelector('h1, h2, h3, [data-title]');
    const t = h && (h.textContent || '').trim().slice(0, 40);
    if (t) return t;
    return 'Slide';
  };
  const stylesheet = `
    :host {
      position: fixed;
      inset: 0;
      display: block;
      background: #000;
      color: #fff;
      font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif;
      overflow: hidden;
      -webkit-tap-highlight-color: transparent;
    }
    /* connectedCallback holds this until document.fonts.ready (capped 2s) so
     * the first visible paint has the deck's real typography + final rail
     * layout. opacity (not visibility) so the active slide can't un-hide
     * itself via the ::slotted([data-deck-active]) visibility:visible rule.
     * Only the stage/rail hide — the black :host background stays, so the
     * iframe doesn't flash the page's default white. */
    :host([data-fonts-pending]) .stage,
    :host([data-fonts-pending]) .rail { opacity: 0; pointer-events: none; }

    .stage {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .canvas {
      position: relative;
      transform-origin: center center;
      flex-shrink: 0;
      background: #fff;
      will-change: transform;
    }

    /* Slides live in light DOM (via <slot>) so authored CSS still applies.
       We absolutely position each slotted child to stack them. */
    ::slotted(*) {
      position: absolute !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      box-sizing: border-box !important;
      overflow: hidden;
      opacity: 0;
      pointer-events: none;
      visibility: hidden;
    }
    ::slotted([data-deck-active]) {
      opacity: 1;
      pointer-events: auto;
      visibility: visible;
    }

    .overlay {
      position: fixed;
      left: 50%;
      bottom: 22px;
      transform: translate(-50%, 6px) scale(0.92);
      filter: blur(6px);
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 4px;
      background: #000;
      color: #fff;
      border-radius: 999px;
      font-size: 12px;
      font-feature-settings: "tnum" 1;
      letter-spacing: 0.01em;
      opacity: 0;
      pointer-events: none;
      transition: opacity 260ms ease, transform 260ms cubic-bezier(.2,.8,.2,1), filter 260ms ease;
      transform-origin: center bottom;
      z-index: 2147483000;
      user-select: none;
    }
    .overlay[data-visible] {
      opacity: 1;
      pointer-events: auto;
      transform: translate(-50%, 0) scale(1);
      filter: blur(0);
    }

    .btn {
      appearance: none;
      -webkit-appearance: none;
      background: transparent;
      border: 0;
      margin: 0;
      padding: 0;
      color: inherit;
      font: inherit;
      cursor: default;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      height: 28px;
      min-width: 28px;
      border-radius: 999px;
      color: rgba(255,255,255,0.72);
      transition: background 140ms ease, color 140ms ease;
      -webkit-tap-highlight-color: transparent;
    }
    .btn:hover { background: rgba(255,255,255,0.12); color: #fff; }
    .btn:active { background: rgba(255,255,255,0.18); }
    .btn:focus { outline: none; }
    .btn:focus-visible { outline: none; }
    .btn::-moz-focus-inner { border: 0; }
    .btn svg { width: 14px; height: 14px; display: block; }
    .btn.reset {
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.02em;
      padding: 0 10px 0 12px;
      gap: 6px;
      color: rgba(255,255,255,0.72);
    }
    .btn.reset .kbd {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 16px;
      height: 16px;
      padding: 0 4px;
      font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
      font-size: 10px;
      line-height: 1;
      color: rgba(255,255,255,0.88);
      background: rgba(255,255,255,0.12);
      border-radius: 4px;
    }

    .count {
      font-variant-numeric: tabular-nums;
      color: #fff;
      font-weight: 500;
      padding: 0 8px;
      min-width: 42px;
      text-align: center;
      font-size: 12px;
    }
    .count .sep { color: rgba(255,255,255,0.45); margin: 0 3px; font-weight: 400; }
    .count .total { color: rgba(255,255,255,0.55); }

    .divider {
      width: 1px;
      height: 14px;
      background: rgba(255,255,255,0.18);
      margin: 0 2px;
    }

    /* ── Thumbnail rail ──────────────────────────────────────────────────
       Fixed column on the left; each thumbnail is a static deep-clone of
       the light-DOM slide scaled into a 16:9 (or design-aspect) frame. The
       stage re-fits around it (see _fit); hidden during present / noscale
       / print so capture geometry and fullscreen output are unchanged. */
    .rail {
      position: fixed;
      left: 0;
      top: 0;
      bottom: 0;
      width: var(--deck-rail-w, 188px);
      background: #141414;
      border-right: 1px solid rgba(255,255,255,0.08);
      overflow-y: auto;
      overflow-x: hidden;
      padding: 12px 10px;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      gap: 12px;
      z-index: 2147482500;
      scrollbar-width: thin;
      scrollbar-color: rgba(255,255,255,0.18) transparent;
    }
    .rail::-webkit-scrollbar { width: 8px; }
    .rail::-webkit-scrollbar-track { background: transparent; margin: 2px; }
    .rail::-webkit-scrollbar-thumb {
      background: rgba(255,255,255,0.18);
      border-radius: 4px;
      border: 2px solid transparent;
      background-clip: content-box;
    }
    .rail::-webkit-scrollbar-thumb:hover {
      background: rgba(255,255,255,0.28);
      border: 2px solid transparent;
      background-clip: content-box;
    }
    :host([no-rail]) .rail,
    :host([noscale]) .rail { display: none; }
    .rail[data-presenting] { display: none; }
    @media (max-width: 640px) {
      .rail, .rail-resize { display: none; }
    }
    /* User-driven show/hide (the TweaksPanel toggle) slides instead of
       popping. Transitions are gated on :host([data-rail-anim]) — set only
       for the 200ms around the toggle — so window-resize and rail-width
       drag (which also call _fit) don't lag behind the cursor. */
    .rail[data-user-hidden] { transform: translateX(-100%); }
    :host([data-rail-anim]) .rail { transition: transform 200ms cubic-bezier(.3,.7,.4,1); }
    :host([data-rail-anim]) .stage { transition: left 200ms cubic-bezier(.3,.7,.4,1); }
    :host([data-rail-anim]) .canvas { transition: transform 200ms cubic-bezier(.3,.7,.4,1); }
    /* transition shorthand replaces rather than merges — repeat the base
       .overlay opacity/transform/filter transitions so visibility changes
       during the 200ms toggle window still fade instead of popping. */
    :host([data-rail-anim]) .overlay {
      transition: margin-left 200ms cubic-bezier(.3,.7,.4,1),
                  opacity 260ms ease,
                  transform 260ms cubic-bezier(.2,.8,.2,1),
                  filter 260ms ease;
    }

    .thumb {
      position: relative;
      display: flex;
      align-items: flex-start;
      gap: 8px;
      cursor: pointer;
      user-select: none;
    }
    .thumb .num {
      width: 16px;
      flex-shrink: 0;
      font-size: 11px;
      font-weight: 500;
      text-align: right;
      color: rgba(255,255,255,0.55);
      padding-top: 2px;
      font-variant-numeric: tabular-nums;
    }
    .thumb .frame {
      position: relative;
      flex: 1;
      min-width: 0;
      aspect-ratio: var(--deck-aspect);
      background: #fff;
      border-radius: 4px;
      outline: 2px solid transparent;
      outline-offset: 0;
      overflow: hidden;
      transition: outline-color 120ms ease;
    }
    .thumb:hover .frame { outline-color: rgba(255,255,255,0.25); }
    .thumb { outline: none; }
    .thumb:focus-visible .frame { outline-color: rgba(255,255,255,0.5); }
    .thumb[data-current] .num { color: #fff; }
    .thumb[data-current] .frame { outline-color: #D97757; }
    .thumb[data-dragging] { opacity: 0.35; }
    .thumb::before {
      content: '';
      position: absolute;
      left: 24px;
      right: 0;
      height: 3px;
      border-radius: 2px;
      background: #D97757;
      opacity: 0;
      pointer-events: none;
    }
    .thumb[data-drop="before"]::before { top: -8px; opacity: 1; }
    .thumb[data-drop="after"]::before { bottom: -8px; opacity: 1; }
    .thumb[data-skip] .frame { opacity: 0.35; }
    .thumb[data-skip] .frame::after {
      content: 'Skipped';
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(0,0,0,0.45);
      color: #fff;
      font-size: 10px;
      font-weight: 500;
      letter-spacing: 0.04em;
    }

    .ctxmenu {
      position: fixed;
      min-width: 150px;
      padding: 4px;
      background: #242424;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 7px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.45);
      z-index: 2147483100;
      display: none;
      font-size: 12px;
    }
    .ctxmenu[data-open] { display: block; }
    .ctxmenu button {
      display: block;
      width: 100%;
      appearance: none;
      border: 0;
      background: transparent;
      color: #e8e8e8;
      font: inherit;
      text-align: left;
      padding: 6px 10px;
      border-radius: 4px;
      cursor: pointer;
    }
    .ctxmenu button:hover:not(:disabled) { background: rgba(255,255,255,0.08); }
    .ctxmenu button:disabled { opacity: 0.35; cursor: default; }
    .ctxmenu hr {
      border: 0;
      border-top: 1px solid rgba(255,255,255,0.1);
      margin: 4px 2px;
    }

    .rail-resize {
      position: fixed;
      left: calc(var(--deck-rail-w, 188px) - 3px);
      top: 0;
      bottom: 0;
      width: 6px;
      cursor: col-resize;
      z-index: 2147482600;
      touch-action: none;
    }
    .rail-resize:hover,
    .rail-resize[data-dragging] { background: rgba(255,255,255,0.12); }
    :host([no-rail]) .rail-resize,
    :host([noscale]) .rail-resize,
    .rail[data-presenting] + .rail-resize,
    .rail[data-user-hidden] + .rail-resize { display: none; }

    /* Delete-confirm popup — matches the SPA's ConfirmDialog layout
       (title + message body, depressed footer with Cancel / Delete). */
    .confirm-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.45);
      z-index: 2147483200;
      display: none;
      align-items: center;
      justify-content: center;
    }
    .confirm-backdrop[data-open] { display: flex; }
    .confirm {
      width: 320px;
      max-width: calc(100vw - 32px);
      background: #2a2a2a;
      color: #e8e8e8;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 12px;
      box-shadow: 0 12px 32px rgba(0,0,0,0.5);
      overflow: hidden;
      font-family: inherit;
      animation: deck-confirm-in 0.18s ease;
    }
    @keyframes deck-confirm-in {
      from { opacity: 0; transform: scale(0.96); }
      to { opacity: 1; transform: scale(1); }
    }
    .confirm .body { padding: 20px 20px 16px; }
    .confirm .title { font-size: 14px; font-weight: 600; margin-bottom: 4px; }
    .confirm .msg { font-size: 13px; line-height: 1.5; color: rgba(255,255,255,0.65); }
    .confirm .footer {
      padding: 14px 20px;
      background: #1f1f1f;
      border-top: 1px solid rgba(255,255,255,0.08);
      display: flex;
      justify-content: flex-end;
      gap: 8px;
    }
    .confirm button {
      appearance: none;
      font: inherit;
      font-size: 13px;
      font-weight: 500;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
    }
    .confirm .cancel {
      background: transparent;
      border: 0;
      color: rgba(255,255,255,0.8);
    }
    .confirm .cancel:hover { background: rgba(255,255,255,0.08); }
    .confirm .danger {
      background: #c96442;
      border: 1px solid rgba(0,0,0,0.15);
      color: #fff;
      box-shadow: 0 1px 3px rgba(166,50,68,0.3), 0 2px 6px rgba(166,50,68,0.18);
    }
    .confirm .danger:hover { background: #b5563a; }

    /* ── Print: one page per slide, no chrome ────────────────────────────
       The screen layout stacks every slide at inset:0 inside a scaled
       canvas; for print we want them in document flow at the authored
       design size so the browser paginates one slide per sheet. The
       @page size is set from the width/height attributes via the inline
       <style id="deck-stage-print-page"> that connectedCallback injects
       into <head> (the @page at-rule has no effect inside shadow DOM). */
    @media print {
      :host {
        position: static;
        inset: auto;
        background: none;
        overflow: visible;
        color: inherit;
      }
      .stage { position: static; display: block; }
      .canvas {
        transform: none !important;
        width: auto !important;
        height: auto !important;
        background: none;
        will-change: auto;
      }
      ::slotted(*) {
        position: relative !important;
        inset: auto !important;
        width: var(--deck-design-w) !important;
        height: var(--deck-design-h) !important;
        box-sizing: border-box !important;
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto;
        break-after: page;
        page-break-after: always;
        break-inside: avoid;
        overflow: hidden;
      }
      /* :last-child alone isn't enough once data-deck-skip hides the
         trailing slide(s) — the last *visible* slide still carries
         break-after:page and prints a blank sheet. _markLastVisible()
         maintains data-deck-last-visible on the last non-skipped slide. */
      ::slotted(*:last-child),
      ::slotted([data-deck-last-visible]) {
        break-after: auto;
        page-break-after: auto;
      }
      ::slotted([data-deck-skip]) { display: none !important; }
      .overlay, .rail, .rail-resize, .ctxmenu, .confirm-backdrop { display: none !important; }
    }
  `;
  class DeckStage extends HTMLElement {
    static get observedAttributes() {
      return ['width', 'height', 'noscale', 'no-rail'];
    }
    constructor() {
      super();
      this._root = this.attachShadow({
        mode: 'open'
      });
      this._index = 0;
      this._slides = [];
      this._notes = [];
      this._hideTimer = null;
      this._mouseIdleTimer = null;
      this._menuIndex = -1;
      this._onKey = this._onKey.bind(this);
      this._onResize = this._onResize.bind(this);
      this._onSlotChange = this._onSlotChange.bind(this);
      this._onMouseMove = this._onMouseMove.bind(this);
      this._onTap = this._onTap.bind(this);
      this._onMessage = this._onMessage.bind(this);
      // Capture-phase close so a click anywhere dismisses the menu, but
      // ignore clicks that land inside the menu itself — otherwise the
      // capture handler runs before the menu's own (bubble) handler and
      // clears _menuIndex out from under it.
      this._onDocClick = e => {
        if (this._menu && e.composedPath && e.composedPath().includes(this._menu)) return;
        this._closeMenu();
      };
    }
    get designWidth() {
      return parseInt(this.getAttribute('width'), 10) || DESIGN_W_DEFAULT;
    }
    get designHeight() {
      return parseInt(this.getAttribute('height'), 10) || DESIGN_H_DEFAULT;
    }
    connectedCallback() {
      // Presenter-view popup loads deckUrl?_snthumb=...#N for its prev/cur/
      // next thumbnails — the rail has no business rendering inside those
      // (wrong scale, and it offsets the stage so the thumb shows a gutter).
      if (/[?&]_snthumb=/.test(location.search)) this.setAttribute('no-rail', '');
      this._render();
      this._loadNotes();
      this._syncPrintPageRule();
      window.addEventListener('keydown', this._onKey);
      window.addEventListener('resize', this._onResize);
      window.addEventListener('mousemove', this._onMouseMove, {
        passive: true
      });
      window.addEventListener('message', this._onMessage);
      window.addEventListener('click', this._onDocClick, true);
      this.addEventListener('click', this._onTap);
      // Print lays every slide out as its own page, so [data-deck-active]-
      // gated entrance styles need the attribute on every slide (not just
      // the current one) or their content prints at the hidden base style.
      // The transient freeze style lands BEFORE the attributes so any
      // attribute-keyed transition fires at 0s (changing transition-
      // duration after a transition has started doesn't affect it).
      this._onBeforePrint = () => {
        if (this._freezeStyle) this._freezeStyle.remove();
        this._freezeStyle = document.createElement('style');
        this._freezeStyle.textContent = '*,*::before,*::after{transition-duration:0s !important}';
        document.head.appendChild(this._freezeStyle);
        this._slides.forEach(s => s.setAttribute('data-deck-active', ''));
      };
      this._onAfterPrint = () => {
        this._applyIndex({
          showOverlay: false,
          broadcast: false
        });
        if (this._freezeStyle) {
          this._freezeStyle.remove();
          this._freezeStyle = null;
        }
      };
      window.addEventListener('beforeprint', this._onBeforePrint);
      window.addEventListener('afterprint', this._onAfterPrint);
      // Initial collection + layout happens via slotchange, which fires on mount.
      this._enableRail();
      // Hold the stage hidden until webfonts are ready so the first visible
      // paint has the deck's real typography — the :not(:defined) guard in
      // the page HTML only covers custom-element upgrade, not font load.
      // Capped so a 404'd font URL can't blank the deck indefinitely.
      this.setAttribute('data-fonts-pending', '');
      const reveal = () => this.removeAttribute('data-fonts-pending');
      // rAF first: fonts.ready is a pre-resolved promise until layout has
      // resolved the slotted text's font-family and pushed a FontFace into
      // 'loading'. Reading it here in connectedCallback (parse-time) would
      // settle the race in a microtask before any font fetch starts.
      requestAnimationFrame(() => {
        Promise.race([document.fonts ? document.fonts.ready : Promise.resolve(), new Promise(r => setTimeout(r, 2000))]).then(reveal, reveal);
      });
    }
    _enableRail() {
      // Idempotent — older host builds still post __omelette_rail_enabled.
      // no-rail guard keeps the observers/stylesheet walk off the cheap path
      // for presenter-popup thumbnail iframes (up to 9 per view).
      if (this._railEnabled || this.hasAttribute('no-rail')) return;
      this._railEnabled = true;
      // Per-viewer preference — restored alongside rail width. Default on;
      // only a stored '0' (from the TweaksPanel toggle) hides it.
      this._railVisible = true;
      try {
        if (localStorage.getItem('deck-stage.railVisible') === '0') this._railVisible = false;
      } catch (e) {}
      // Live thumbnail updates: watch the light-DOM slides for content
      // edits and re-clone just the affected thumb(s), debounced. Ignore
      // the data-deck-* / data-screen-label / data-om-validate attributes
      // this component itself writes so nav and skip don't trigger
      // spurious refreshes.
      const OWN_ATTRS = /^data-(deck-|screen-label$|om-validate$)/;
      this._liveDirty = new Set();
      this._liveObserver = new MutationObserver(records => {
        for (const r of records) {
          if (r.type === 'attributes' && OWN_ATTRS.test(r.attributeName || '')) continue;
          let n = r.target;
          while (n && n.parentElement !== this) n = n.parentElement;
          if (n && this._slideSet && this._slideSet.has(n)) this._liveDirty.add(n);
        }
        if (this._liveDirty.size && !this._liveTimer) {
          this._liveTimer = setTimeout(() => {
            this._liveTimer = null;
            this._liveDirty.forEach(s => this._refreshThumb(s));
            this._liveDirty.clear();
          }, 200);
        }
      });
      this._liveObserver.observe(this, {
        subtree: true,
        childList: true,
        characterData: true,
        attributes: true
      });
      // Lazy thumbnail materialization — clone the slide only when its
      // frame scrolls into (or near) the rail viewport. rootMargin gives
      // ~4 thumbs of pre-load so fast scrolling doesn't flash blanks.
      this._railObserver = new IntersectionObserver(entries => {
        entries.forEach(e => {
          if (e.isIntersecting && e.target.__deckThumb) {
            this._materialize(e.target.__deckThumb);
          }
        });
      }, {
        root: this._rail,
        rootMargin: '400px 0px'
      });
      // Tweaks typically change CSS vars / attrs OUTSIDE <deck-stage>
      // (on <html>, <body>, a wrapper div, or a <style> tag), which
      // _liveObserver can't see. Re-snapshot author CSS (constructable
      // sheet is shared by reference, so one replaceSync updates every
      // thumb shadow root) and re-sync each thumb host's attrs + custom
      // properties. In-slide DOM mutations are _liveObserver's job.
      // Debounced so slider drags don't thrash.
      this._onTweakChange = () => {
        clearTimeout(this._tweakTimer);
        this._tweakTimer = setTimeout(() => {
          this._snapshotAuthorCss();
          // One getComputedStyle for the whole batch — each
          // getPropertyValue read below reuses the same computed style
          // as long as nothing invalidates layout between thumbs.
          const cs = getComputedStyle(this);
          (this._thumbs || []).forEach(t => {
            if (t.host) this._syncThumbHostAttrs(t.host, cs);
          });
        }, 120);
      };
      window.addEventListener('tweakchange', this._onTweakChange);
      this._snapshotAuthorCss();
      // Build the rail now that it's enabled — slotchange already fired,
      // so _renderRail's early-return skipped the initial build.
      this._syncRailHidden();
      this._renderRail();
      this._fit();
    }

    /** Snapshot document stylesheets into a constructable sheet that each
     *  thumbnail's nested shadow root adopts — so author CSS styles the
     *  cloned slide content without touching this component's chrome.
     *  Cross-origin sheets throw on .cssRules — skip them. Re-callable:
     *  the existing constructable sheet is reused via replaceSync so every
     *  already-adopted shadow root picks up the fresh CSS without re-adopt. */
    _snapshotAuthorCss() {
      // :root in an adopted sheet inside a shadow root matches nothing
      // (only the document root qualifies), so author rules like
      // `:root[data-voice="modern"] .serif` never reach the clones.
      // Rewrite :root → :host and mirror <html>'s data-*/class/lang onto
      // each thumb host (see _syncThumbHostAttrs) so the same selectors
      // match inside the thumbnail's shadow tree.
      const authorCss = Array.from(document.styleSheets).map(sh => {
        try {
          return Array.from(sh.cssRules).map(r => r.cssText).join('\n');
        } catch (e) {
          return '';
        }
      }).join('\n')
      // The shadow host is featureless outside the functional :host(...)
      // form, so any compound on :root — [attr], .class, #id, :pseudo —
      // must become :host(<compound>) not :host<compound>. Same for the
      // html type selector (Tailwind class-strategy dark mode emits
      // html.dark; Pico uses html[data-theme]), which has nothing to
      // match inside the thumb's shadow tree.
      .replace(/:root((?:\[[^\]]*\]|[.#][-\w]+|:[-\w]+(?:\([^)]*\))?)+)/g, ':host($1)').replace(/:root\b/g, ':host').replace(/(^|[\s,>~+(}])html((?:\[[^\]]*\]|[.#][-\w]+|:[-\w]+(?:\([^)]*\))?)+)(?![-\w])/g, '$1:host($2)').replace(/(^|[\s,>~+(}])html(?![-\w])/g, '$1:host');
      // Every custom property the author references. _syncThumbHostAttrs
      // mirrors each one's *computed* value at <deck-stage> onto the
      // thumb host so the live value wins over the :host default above
      // regardless of which ancestor the tweak wrote to (<html>, <body>,
      // a wrapper div, or the deck-stage element itself all inherit
      // down to getComputedStyle(this)).
      this._authorVars = new Set(authorCss.match(/--[\w-]+/g) || []);
      try {
        if (!this._adoptedSheet) this._adoptedSheet = new CSSStyleSheet();
        this._adoptedSheet.replaceSync(authorCss);
      } catch (e) {
        this._adoptedSheet = null;
        this._authorCss = authorCss;
      }
    }
    _syncThumbHostAttrs(host, cs) {
      const de = document.documentElement;
      // setAttribute overwrites but can't delete — an attr removed from
      // <html> (toggleAttribute off, classList emptied) would linger on
      // the host and :host([data-*]) / :host(.foo) rules would keep
      // matching. Remove stale mirrored attrs first; iterate backward
      // because removeAttribute mutates the live NamedNodeMap.
      for (let i = host.attributes.length - 1; i >= 0; i--) {
        const n = host.attributes[i].name;
        if ((n.startsWith('data-') || n === 'class' || n === 'lang') && !de.hasAttribute(n)) {
          host.removeAttribute(n);
        }
      }
      for (const a of de.attributes) {
        if (a.name.startsWith('data-') || a.name === 'class' || a.name === 'lang') {
          host.setAttribute(a.name, a.value);
        }
      }
      // The :root→:host rewrite in _snapshotAuthorCss pins each custom
      // property to its stylesheet default on the thumb host, shadowing
      // the live value that would otherwise inherit. Tweaks can write the
      // live value on any ancestor — <html>, <body>, a wrapper div, the
      // deck-stage element — so read it as the *computed* value at
      // <deck-stage> (which sees the whole inheritance chain) rather than
      // trying to guess which element the author wrote to. Inline on the
      // host beats the :host{} rule. remove-stale covers vars dropped
      // from the stylesheet between snapshots.
      const vars = this._authorVars || new Set();
      for (let i = host.style.length - 1; i >= 0; i--) {
        const p = host.style[i];
        if (p.startsWith('--') && !vars.has(p)) host.style.removeProperty(p);
      }
      const live = cs || getComputedStyle(this);
      vars.forEach(p => {
        const v = live.getPropertyValue(p);
        if (v) host.style.setProperty(p, v.trim());else host.style.removeProperty(p);
      });
    }
    disconnectedCallback() {
      window.removeEventListener('keydown', this._onKey);
      window.removeEventListener('resize', this._onResize);
      window.removeEventListener('mousemove', this._onMouseMove);
      window.removeEventListener('message', this._onMessage);
      window.removeEventListener('click', this._onDocClick, true);
      window.removeEventListener('beforeprint', this._onBeforePrint);
      window.removeEventListener('afterprint', this._onAfterPrint);
      if (this._freezeStyle) {
        this._freezeStyle.remove();
        this._freezeStyle = null;
      }
      this.removeEventListener('click', this._onTap);
      if (this._hideTimer) clearTimeout(this._hideTimer);
      if (this._mouseIdleTimer) clearTimeout(this._mouseIdleTimer);
      if (this._liveTimer) clearTimeout(this._liveTimer);
      if (this._tweakTimer) clearTimeout(this._tweakTimer);
      if (this._railAnimTimer) clearTimeout(this._railAnimTimer);
      if (this._scaleRaf) cancelAnimationFrame(this._scaleRaf);
      if (this._liveObserver) this._liveObserver.disconnect();
      if (this._railObserver) this._railObserver.disconnect();
      if (this._onTweakChange) window.removeEventListener('tweakchange', this._onTweakChange);
    }
    attributeChangedCallback() {
      if (this._canvas) {
        this._canvas.style.width = this.designWidth + 'px';
        this._canvas.style.height = this.designHeight + 'px';
        this._canvas.style.setProperty('--deck-design-w', this.designWidth + 'px');
        this._canvas.style.setProperty('--deck-design-h', this.designHeight + 'px');
        if (this._rail) {
          this._rail.style.setProperty('--deck-aspect', this.designWidth + '/' + this.designHeight);
        }
        this._fit();
        this._scaleThumbs();
        this._syncPrintPageRule();
      }
    }
    _render() {
      const style = document.createElement('style');
      style.textContent = stylesheet;
      const stage = document.createElement('div');
      stage.className = 'stage';
      const canvas = document.createElement('div');
      canvas.className = 'canvas';
      canvas.style.width = this.designWidth + 'px';
      canvas.style.height = this.designHeight + 'px';
      canvas.style.setProperty('--deck-design-w', this.designWidth + 'px');
      canvas.style.setProperty('--deck-design-h', this.designHeight + 'px');
      const slot = document.createElement('slot');
      slot.addEventListener('slotchange', this._onSlotChange);
      canvas.appendChild(slot);
      stage.appendChild(canvas);

      // Overlay: compact, solid black, with clickable controls.
      const overlay = document.createElement('div');
      overlay.className = 'overlay export-hidden';
      overlay.setAttribute('role', 'toolbar');
      overlay.setAttribute('aria-label', 'Deck controls');
      overlay.setAttribute('data-omelette-chrome', '');
      overlay.innerHTML = `
        <button class="btn prev" type="button" aria-label="Previous slide" title="Previous (←)">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 3L5 8l5 5"/></svg>
        </button>
        <span class="count" aria-live="polite"><span class="current">1</span><span class="sep">/</span><span class="total">1</span></span>
        <button class="btn next" type="button" aria-label="Next slide" title="Next (→)">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>
        </button>
        <span class="divider"></span>
        <button class="btn reset" type="button" aria-label="Reset to first slide" title="Reset (R)">Reset<span class="kbd">R</span></button>
      `;
      overlay.querySelector('.prev').addEventListener('click', () => this._advance(-1, 'click'));
      overlay.querySelector('.next').addEventListener('click', () => this._advance(1, 'click'));
      overlay.querySelector('.reset').addEventListener('click', () => this._go(0, 'click'));

      // Thumbnail rail + context menu. Thumbnails are populated in
      // _renderRail() after _collectSlides().
      const rail = document.createElement('div');
      rail.className = 'rail export-hidden';
      rail.setAttribute('data-omelette-chrome', '');
      rail.style.setProperty('--deck-aspect', this.designWidth + '/' + this.designHeight);
      // Edge auto-scroll while dragging a thumb near the rail's top/bottom
      // so off-screen drop targets are reachable. Native dragover fires
      // continuously while the pointer is stationary, so a per-event nudge
      // (ramped by edge proximity) is enough — no rAF loop needed.
      rail.addEventListener('dragover', e => {
        if (this._dragFrom == null) return;
        const r = rail.getBoundingClientRect();
        const EDGE = 40;
        const dt = e.clientY - r.top;
        const db = r.bottom - e.clientY;
        if (dt < EDGE) rail.scrollTop -= Math.ceil((EDGE - dt) / 3);else if (db < EDGE) rail.scrollTop += Math.ceil((EDGE - db) / 3);
      });
      const menu = document.createElement('div');
      menu.className = 'ctxmenu export-hidden';
      menu.setAttribute('data-omelette-chrome', '');
      menu.innerHTML = `
        <button type="button" data-act="skip">Skip slide</button>
        <button type="button" data-act="up">Move up</button>
        <button type="button" data-act="down">Move down</button>
        <hr>
        <button type="button" data-act="delete">Delete slide</button>
      `;
      menu.addEventListener('click', e => {
        const act = e.target && e.target.getAttribute && e.target.getAttribute('data-act');
        if (!act) return;
        const i = this._menuIndex;
        this._closeMenu();
        if (act === 'skip') this._toggleSkip(i);else if (act === 'up') this._moveSlide(i, i - 1);else if (act === 'down') this._moveSlide(i, i + 1);else if (act === 'delete') this._openConfirm(i);
      });
      menu.addEventListener('contextmenu', e => e.preventDefault());

      // Rail resize handle — drag to set --deck-rail-w, persisted to
      // localStorage so the width survives reloads.
      const resize = document.createElement('div');
      resize.className = 'rail-resize export-hidden';
      resize.setAttribute('data-omelette-chrome', '');
      resize.addEventListener('pointerdown', e => {
        e.preventDefault();
        resize.setPointerCapture(e.pointerId);
        resize.setAttribute('data-dragging', '');
        const move = ev => this._setRailWidth(ev.clientX);
        const up = () => {
          resize.removeEventListener('pointermove', move);
          resize.removeEventListener('pointerup', up);
          resize.removeEventListener('pointercancel', up);
          resize.removeAttribute('data-dragging');
          try {
            localStorage.setItem('deck-stage.railWidth', String(this._railPx));
          } catch (err) {}
        };
        resize.addEventListener('pointermove', move);
        resize.addEventListener('pointerup', up);
        resize.addEventListener('pointercancel', up);
      });

      // Delete-confirm dialog — mirrors the SPA's ConfirmDialog layout.
      const confirm = document.createElement('div');
      confirm.className = 'confirm-backdrop export-hidden';
      confirm.setAttribute('data-omelette-chrome', '');
      confirm.innerHTML = `
        <div class="confirm" role="dialog" aria-modal="true">
          <div class="body">
            <div class="title">Delete slide?</div>
            <div class="msg">This slide will be removed from the deck.</div>
          </div>
          <div class="footer">
            <button type="button" class="cancel">Cancel</button>
            <button type="button" class="danger">Delete</button>
          </div>
        </div>
      `;
      confirm.addEventListener('click', e => {
        if (e.target === confirm) this._closeConfirm();
      });
      confirm.querySelector('.cancel').addEventListener('click', () => this._closeConfirm());
      confirm.querySelector('.danger').addEventListener('click', () => {
        const i = this._confirmIndex;
        this._closeConfirm();
        this._deleteSlide(i);
      });
      this._root.append(style, rail, resize, stage, overlay, menu, confirm);
      this._canvas = canvas;
      this._stage = stage;
      this._slot = slot;
      this._overlay = overlay;
      this._rail = rail;
      this._resize = resize;
      this._menu = menu;
      this._confirm = confirm;
      this._countEl = overlay.querySelector('.current');
      this._totalEl = overlay.querySelector('.total');

      // Restore persisted rail width.
      let rw = 188;
      try {
        const s = localStorage.getItem('deck-stage.railWidth');
        if (s) rw = parseInt(s, 10) || rw;
      } catch (err) {}
      this._setRailWidth(rw);
      this._syncRailHidden();
    }
    _setRailWidth(px) {
      const w = Math.max(120, Math.min(360, Math.round(px)));
      this._railPx = w;
      this.style.setProperty('--deck-rail-w', w + 'px');
      this._fit();
      // _scaleThumbs forces a sync layout (frame.offsetWidth) then writes
      // N transforms. During a resize drag this runs per-pointermove;
      // coalesce to one per frame.
      if (!this._scaleRaf) {
        this._scaleRaf = requestAnimationFrame(() => {
          this._scaleRaf = null;
          this._scaleThumbs();
        });
      }
    }

    /** @page must live in the document stylesheet — it's a no-op inside
     *  shadow DOM. Inject/update a single <head> style tag so the print
     *  sheet matches the design size and Save-as-PDF yields one slide per
     *  page with no margins. */
    _syncPrintPageRule() {
      const id = 'deck-stage-print-page';
      let tag = document.getElementById(id);
      if (!tag) {
        tag = document.createElement('style');
        tag.id = id;
        document.head.appendChild(tag);
      }
      tag.textContent = '@page { size: ' + this.designWidth + 'px ' + this.designHeight + 'px; margin: 0; } ' + '@media print { html, body { margin: 0 !important; padding: 0 !important; background: none !important; overflow: visible !important; height: auto !important; } ' + '* { -webkit-print-color-adjust: exact; print-color-adjust: exact; } ' +
      // Jump authored animations/transitions to their end state so print
      // never captures mid-entrance — pairs with the beforeprint handler
      // in connectedCallback that sets data-deck-active on every slide.
      '*, *::before, *::after { animation-delay: -99s !important; animation-duration: .001s !important; ' + 'animation-iteration-count: 1 !important; animation-fill-mode: both !important; ' + 'animation-play-state: running !important; transition-duration: 0s !important; } }';
    }
    _onSlotChange() {
      // Rail mutations (delete/move) already reconcile synchronously and
      // emit slidechange with reason 'api'; skip the async slotchange that
      // would otherwise re-broadcast with reason 'init'.
      if (this._squelchSlotChange) {
        this._squelchSlotChange = false;
        return;
      }
      this._collectSlides();
      this._restoreIndex();
      this._applyIndex({
        showOverlay: false,
        broadcast: true,
        reason: 'init'
      });
      this._fit();
    }
    _collectSlides() {
      const assigned = this._slot.assignedElements({
        flatten: true
      });
      this._slides = assigned.filter(el => {
        // Skip template/style/script nodes even if someone slots them.
        const tag = el.tagName;
        return tag !== 'TEMPLATE' && tag !== 'SCRIPT' && tag !== 'STYLE';
      });
      this._slideSet = new Set(this._slides);
      this._slides.forEach((slide, i) => {
        const n = i + 1;
        slide.setAttribute('data-screen-label', `${pad2(n)} ${getSlideLabel(slide)}`);

        // Validation attribute for comment flow / auto-checks.
        if (!slide.hasAttribute('data-om-validate')) {
          slide.setAttribute('data-om-validate', VALIDATE_ATTR);
        }
        slide.setAttribute('data-deck-slide', String(i));
      });
      if (this._totalEl) this._totalEl.textContent = String(this._slides.length || 1);
      if (this._index >= this._slides.length) this._index = Math.max(0, this._slides.length - 1);
      this._markLastVisible();
      this._renderRail();
    }

    /** Tag the last non-skipped slide so print CSS can drop its
     *  break-after (see the @media print comment above — :last-child
     *  alone matches a hidden skipped slide). */
    _markLastVisible() {
      let last = null;
      this._slides.forEach(s => {
        s.removeAttribute('data-deck-last-visible');
        if (!s.hasAttribute('data-deck-skip')) last = s;
      });
      if (last) last.setAttribute('data-deck-last-visible', '');
    }
    _loadNotes() {
      const tag = document.getElementById('speaker-notes');
      if (!tag) {
        this._notes = [];
        return;
      }
      try {
        const parsed = JSON.parse(tag.textContent || '[]');
        if (Array.isArray(parsed)) this._notes = parsed;
      } catch (e) {
        console.warn('[deck-stage] Failed to parse #speaker-notes JSON:', e);
        this._notes = [];
      }
    }
    _restoreIndex() {
      // The host's ?slide= param is delivered as a #<int> hash (1-indexed) on
      // the iframe src. No hash → slide 1; the deck itself keeps no position
      // state across loads.
      const h = (location.hash || '').match(/^#(\d+)$/);
      if (h) {
        const n = parseInt(h[1], 10) - 1;
        if (n >= 0 && n < this._slides.length) this._index = n;
      }
    }
    _applyIndex({
      showOverlay = true,
      broadcast = true,
      reason = 'init'
    } = {}) {
      if (!this._slides.length) return;
      const prev = this._prevIndex == null ? -1 : this._prevIndex;
      const curr = this._index;
      // Keep the iframe's own hash in sync so an in-iframe location.reload()
      // (reload banner path in viewer-handle.ts) lands on the current slide,
      // not the stale deep-link hash from initial load.
      try {
        history.replaceState(null, '', '#' + (curr + 1));
      } catch (e) {}
      this._slides.forEach((s, i) => {
        if (i === curr) s.setAttribute('data-deck-active', '');else s.removeAttribute('data-deck-active');
      });
      if (this._countEl) this._countEl.textContent = String(curr + 1);
      // Follow-scroll on every navigation (init deep-link, keyboard, click,
      // tap, external goTo) — the only time we *don't* want the rail to
      // track current is after a rail-internal mutation, where _renderRail
      // has already restored the user's scroll position and yanking back to
      // current would undo it.
      this._syncRail(reason !== 'mutation');
      if (broadcast) {
        // (1) Legacy: host-window postMessage for speaker-notes renderers.
        try {
          window.postMessage({
            slideIndexChanged: curr,
            deckTotal: this._slides.length,
            deckSkipped: this._skippedIndices()
          }, '*');
        } catch (e) {}

        // (2) In-page CustomEvent on the <deck-stage> element itself.
        //     Bubbles and composes out of shadow DOM so slide code can listen:
        //       document.querySelector('deck-stage').addEventListener('slidechange', e => {
        //         e.detail.index, e.detail.previousIndex, e.detail.total, e.detail.slide, e.detail.reason
        //       });
        const detail = {
          index: curr,
          previousIndex: prev,
          total: this._slides.length,
          slide: this._slides[curr] || null,
          previousSlide: prev >= 0 ? this._slides[prev] || null : null,
          reason: reason // 'init' | 'keyboard' | 'click' | 'tap' | 'api'
        };
        this.dispatchEvent(new CustomEvent('slidechange', {
          detail,
          bubbles: true,
          composed: true
        }));
      }
      this._prevIndex = curr;
      if (showOverlay) this._flashOverlay();
    }
    _flashOverlay() {
      // Host posts __omelette_presenting while in fullscreen/tab presentation
      // mode — suppress the nav footer entirely (both hover and slide-change
      // flash) so the audience sees clean slides.
      if (!this._overlay || this._presenting) return;
      this._overlay.setAttribute('data-visible', '');
      if (this._hideTimer) clearTimeout(this._hideTimer);
      this._hideTimer = setTimeout(() => {
        this._overlay.removeAttribute('data-visible');
      }, OVERLAY_HIDE_MS);
    }
    _railWidth() {
      // State-based, no offsetWidth: the first _fit() can run before the
      // rail has had layout on some load paths, and a 0 there paints the
      // slide full-width for one frame before the post-slotchange _fit()
      // corrects it.
      if (!this._railEnabled || !this._railVisible || this.hasAttribute('no-rail') || this.hasAttribute('noscale') || this._presenting || this._previewMode || NARROW_MQ.matches) return 0;
      return this._railPx || 0;
    }
    _fit() {
      if (!this._canvas) return;
      const stage = this._canvas.parentElement;
      // PPTX export sets noscale so the DOM capture sees authored-size
      // geometry — the scaled canvas is in shadow DOM, so the exporter's
      // resetTransformSelector can't reach .canvas.style.transform directly.
      if (this.hasAttribute('noscale')) {
        this._canvas.style.transform = 'none';
        if (stage) stage.style.left = '0';
        if (this._overlay) this._overlay.style.marginLeft = '0';
        return;
      }
      const rw = this._railWidth();
      if (stage) stage.style.left = rw + 'px';
      // Overlay is centred on the viewport via left:50% + translate(-50%);
      // marginLeft shifts the centre by rw/2 so it lands in the middle of
      // the [rw, innerWidth] stage region.
      if (this._overlay) this._overlay.style.marginLeft = rw / 2 + 'px';
      const vw = window.innerWidth - rw;
      const vh = window.innerHeight;
      const s = Math.min(vw / this.designWidth, vh / this.designHeight);
      this._canvas.style.transform = `scale(${s})`;
    }
    _onResize() {
      this._fit();
      // Crossing the narrow-viewport breakpoint reveals the rail — rerun the
      // thumbnail scale the same way _setRailWidth does.
      if (!this._scaleRaf) {
        this._scaleRaf = requestAnimationFrame(() => {
          this._scaleRaf = null;
          this._scaleThumbs();
        });
      }
    }
    _onMouseMove() {
      // Keep overlay visible while mouse moves; hide after idle.
      this._flashOverlay();
    }
    _onMessage(e) {
      const d = e.data;
      if (d && typeof d.__omelette_presenting === 'boolean') {
        this._presenting = d.__omelette_presenting;
        if (this._presenting && this._overlay) {
          this._overlay.removeAttribute('data-visible');
          if (this._hideTimer) clearTimeout(this._hideTimer);
        }
        this._syncRailHidden();
        this._closeMenu();
        this._closeConfirm();
        this._fit();
        this._scaleThumbs();
      }
      // Host's Preview segment (ViewerMode='none'): the rail's drag-reorder /
      // right-click skip-delete affordances are editing chrome, so hide it
      // while the user is just looking at the deck. Same hard-hide path as
      // presenting; independent of the user's _railVisible preference so
      // returning to Edit restores whatever they had.
      if (d && typeof d.__omelette_preview_mode === 'boolean') {
        if (d.__omelette_preview_mode === this._previewMode) return;
        this._previewMode = d.__omelette_preview_mode;
        this._syncRailHidden();
        this._closeMenu();
        this._closeConfirm();
        this._fit();
        this._scaleThumbs();
      }
      // Per-viewer show/hide, driven by the TweaksPanel's auto-injected
      // "Thumbnail rail" toggle (or any author script). Independent of
      // whether the Tweaks panel itself is open — closing the panel
      // doesn't change rail visibility. Persists alongside rail width.
      if (d && d.type === '__deck_rail_visible' && typeof d.on === 'boolean') {
        if (d.on === this._railVisible) return;
        this._railVisible = d.on;
        try {
          localStorage.setItem('deck-stage.railVisible', d.on ? '1' : '0');
        } catch (e) {}
        // Arm the transition, commit it, then flip state — otherwise the
        // browser coalesces both writes and nothing animates on show.
        this.setAttribute('data-rail-anim', '');
        void (this._rail && this._rail.offsetHeight);
        this._syncRailHidden();
        this._fit();
        this._scaleThumbs();
        clearTimeout(this._railAnimTimer);
        this._railAnimTimer = setTimeout(() => this.removeAttribute('data-rail-anim'), 220);
      }
      if (d && d.type === '__omelette_rail_enabled') this._enableRail();
    }
    _syncRailHidden() {
      if (!this._rail) return;
      // data-presenting is the hard hide (display:none) for flag-off,
      // presentation mode, and the host's Preview segment — instant, no
      // transition. data-user-hidden is the soft hide (translateX(-100%))
      // for the viewer's rail toggle, so show/hide slides under
      // :host([data-rail-anim]).
      const hard = !this._railEnabled || this._presenting || this._previewMode;
      if (hard) this._rail.setAttribute('data-presenting', '');else this._rail.removeAttribute('data-presenting');
      if (!this._railVisible) this._rail.setAttribute('data-user-hidden', '');else this._rail.removeAttribute('data-user-hidden');
      // translateX hide leaves thumbs (tabIndex=0) in the tab order —
      // inert keeps them unfocusable while the rail is off-screen.
      this._rail.inert = hard || !this._railVisible;
    }
    _onTap(e) {
      // Touch-only — keyboard + the overlay toolbar cover nav on desktop.
      if (FINE_POINTER_MQ.matches) return;
      // Only taps that land on the stage (slide content or letterbox); the
      // overlay / rail / menus are siblings with their own click handlers.
      const path = e.composedPath();
      if (!this._stage || !path.includes(this._stage)) return;
      // Let interactive slide content keep the tap. composedPath (not
      // e.target.closest) so we see through open shadow roots — a <button>
      // inside a slide-authored custom element retargets e.target to the
      // host but still appears in the composed path.
      if (e.defaultPrevented) return;
      for (const n of path) {
        if (n === this._stage) break;
        if (n.matches && n.matches(INTERACTIVE_SEL)) return;
      }
      e.preventDefault();
      const rw = this._railWidth();
      const mid = rw + (window.innerWidth - rw) / 2;
      this._advance(e.clientX < mid ? -1 : 1, 'tap');
    }
    _onKey(e) {
      // Ignore when the user is typing.
      const t = e.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      // Confirm dialog swallows nav keys while open; Escape cancels. Enter
      // is left to the focused button's native activation so Tab→Cancel
      // →Enter activates Cancel, not the window-level confirm path.
      if (this._confirm && this._confirm.hasAttribute('data-open')) {
        if (e.key === 'Escape') {
          this._closeConfirm();
          e.preventDefault();
        }
        return;
      }
      if (e.key === 'Escape' && this._menu && this._menu.hasAttribute('data-open')) {
        this._closeMenu();
        e.preventDefault();
        return;
      }
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const key = e.key;
      let handled = true;
      if (key === 'ArrowRight' || key === 'PageDown' || key === ' ' || key === 'Spacebar') {
        this._advance(1, 'keyboard');
      } else if (key === 'ArrowLeft' || key === 'PageUp') {
        this._advance(-1, 'keyboard');
      } else if (key === 'Home') {
        this._go(0, 'keyboard');
      } else if (key === 'End') {
        this._go(this._slides.length - 1, 'keyboard');
      } else if (key === 'r' || key === 'R') {
        this._go(0, 'keyboard');
      } else if (/^[0-9]$/.test(key)) {
        // 1..9 jump to that slide; 0 jumps to 10.
        const n = key === '0' ? 9 : parseInt(key, 10) - 1;
        if (n < this._slides.length) this._go(n, 'keyboard');
      } else {
        handled = false;
      }
      if (handled) {
        e.preventDefault();
        this._flashOverlay();
      }
    }
    _go(i, reason = 'api') {
      if (!this._slides.length) return;
      const clamped = Math.max(0, Math.min(this._slides.length - 1, i));
      if (clamped === this._index) {
        this._flashOverlay();
        return;
      }
      this._index = clamped;
      this._applyIndex({
        showOverlay: true,
        broadcast: true,
        reason
      });
    }

    /** Step forward/back skipping any slide marked data-deck-skip. Falls
     *  back to _go's clamp-at-ends behaviour (flash overlay) when there's
     *  nothing further in that direction. */
    _advance(dir, reason) {
      if (!this._slides.length) return;
      let i = this._index + dir;
      while (i >= 0 && i < this._slides.length && this._slides[i].hasAttribute('data-deck-skip')) {
        i += dir;
      }
      if (i < 0 || i >= this._slides.length) {
        this._flashOverlay();
        return;
      }
      this._go(i, reason);
    }

    // ── Thumbnail rail ────────────────────────────────────────────────────
    //
    // Thumbs are keyed by slide element and reused across _renderRail()
    // calls, so a reorder/delete is an O(changed) DOM shuffle instead of an
    // O(N) teardown-and-re-clone. Each thumb starts as a lightweight shell
    // (num + empty frame); the clone is materialized lazily by an
    // IntersectionObserver when the frame scrolls into (or near) view, so
    // only visible-ish slides pay the clone + image-decode cost.

    _renderRail() {
      if (!this._rail || !this._railEnabled) {
        this._thumbs = [];
        return;
      }
      // FLIP: record each *materialized* thumb's top before the reconcile.
      // Off-screen (non-materialized) thumbs don't need the animation and
      // skipping their getBoundingClientRect saves a forced layout per
      // off-screen thumb on large decks.
      const prevTops = new Map();
      (this._thumbs || []).forEach(({
        thumb,
        slide,
        host
      }) => {
        if (host) prevTops.set(slide, thumb.getBoundingClientRect().top);
      });
      const st = this._rail.scrollTop;

      // Reconcile: reuse thumbs that already exist for a slide, create
      // shells for new slides, drop thumbs for removed slides.
      const bySlide = new Map();
      (this._thumbs || []).forEach(t => bySlide.set(t.slide, t));
      const next = [];
      this._slides.forEach(slide => {
        let t = bySlide.get(slide);
        if (t) bySlide.delete(slide);else t = this._makeThumb(slide);
        next.push(t);
      });
      // Orphans — slides removed since last render.
      bySlide.forEach(t => {
        if (this._railObserver) this._railObserver.unobserve(t.frame);
        t.thumb.remove();
      });
      // Put thumbs into document order to match _slides. insertBefore on
      // an already-correctly-placed node is a no-op, so this is cheap
      // when nothing moved.
      next.forEach((t, i) => {
        const want = t.thumb;
        const at = this._rail.children[i];
        if (at !== want) this._rail.insertBefore(want, at || null);
        t.i = i;
        t.num.textContent = String(i + 1);
        if (t.slide.hasAttribute('data-deck-skip')) t.thumb.setAttribute('data-skip', '');else t.thumb.removeAttribute('data-skip');
      });
      this._thumbs = next;
      this._rail.scrollTop = st;
      if (prevTops.size) {
        const moved = [];
        this._thumbs.forEach(({
          thumb,
          slide
        }) => {
          const old = prevTops.get(slide);
          if (old == null) return;
          const dy = old - thumb.getBoundingClientRect().top;
          if (Math.abs(dy) < 1) return;
          thumb.style.transition = 'none';
          thumb.style.transform = `translateY(${dy}px)`;
          moved.push(thumb);
        });
        if (moved.length) {
          // Commit the inverted positions before flipping the transition
          // on — otherwise the browser coalesces both style writes and
          // nothing animates.
          void this._rail.offsetHeight;
          moved.forEach(t => {
            t.style.transition = 'transform 180ms cubic-bezier(.2,.7,.3,1)';
            t.style.transform = '';
          });
          setTimeout(() => moved.forEach(t => {
            t.style.transition = '';
          }), 220);
        }
      }
      requestAnimationFrame(() => this._scaleThumbs());
      this._syncRail(false);
    }

    /** Create a lightweight thumb shell for one slide. The clone is
     *  materialized later by the IntersectionObserver. Event handlers
     *  look up the thumb's *current* index (via _thumbs.indexOf) so the
     *  same element can be reused across reorders. */
    _makeThumb(slide) {
      const thumb = document.createElement('div');
      thumb.className = 'thumb';
      thumb.tabIndex = 0;
      const num = document.createElement('div');
      num.className = 'num';
      const frame = document.createElement('div');
      frame.className = 'frame';
      thumb.append(num, frame);
      const entry = {
        thumb,
        num,
        frame,
        slide,
        clone: null,
        host: null,
        i: -1
      };
      // entry.i is refreshed on every _renderRail reconcile pass, so
      // handlers read the thumb's current position without an O(N) scan.
      const idx = () => entry.i;
      thumb.addEventListener('click', () => this._go(idx(), 'click'));
      // ↑/↓ step through the rail when a thumb has focus. _go clamps at the
      // ends and _applyIndex→_syncRail scrolls the new current thumb into
      // view; we move focus to it (preventScroll — _syncRail already
      // scrolled) so a held key walks the whole list. stopPropagation keeps
      // this out of the window-level _onKey nav handler.
      thumb.addEventListener('keydown', e => {
        if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return;
        if (e.metaKey || e.ctrlKey || e.altKey) return;
        e.preventDefault();
        e.stopPropagation();
        this._go(idx() + (e.key === 'ArrowDown' ? 1 : -1), 'keyboard');
        const cur = this._thumbs && this._thumbs[this._index];
        if (cur) cur.thumb.focus({
          preventScroll: true
        });
      });
      thumb.addEventListener('contextmenu', e => {
        e.preventDefault();
        this._openMenu(idx(), e.clientX, e.clientY);
      });
      thumb.draggable = true;
      thumb.addEventListener('dragstart', e => {
        this._dragFrom = idx();
        thumb.setAttribute('data-dragging', '');
        e.dataTransfer.effectAllowed = 'move';
        try {
          e.dataTransfer.setData('text/plain', String(this._dragFrom));
        } catch (err) {}
      });
      thumb.addEventListener('dragend', () => {
        thumb.removeAttribute('data-dragging');
        this._clearDrop();
        this._dragFrom = null;
      });
      thumb.addEventListener('dragover', e => {
        if (this._dragFrom == null) return;
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        const r = thumb.getBoundingClientRect();
        this._setDrop(idx(), e.clientY < r.top + r.height / 2 ? 'before' : 'after');
      });
      thumb.addEventListener('drop', e => {
        if (this._dragFrom == null) return;
        e.preventDefault();
        const i = idx();
        const r = thumb.getBoundingClientRect();
        let to = e.clientY >= r.top + r.height / 2 ? i + 1 : i;
        if (this._dragFrom < to) to--;
        const from = this._dragFrom;
        this._clearDrop();
        this._dragFrom = null;
        if (to !== from) this._moveSlide(from, to);
      });
      if (this._railObserver) this._railObserver.observe(frame);
      frame.__deckThumb = entry;
      return entry;
    }

    /** Lazily build the clone for a thumb that has scrolled into view. */
    _materialize(entry) {
      if (entry.host) return;
      const dw = this.designWidth,
        dh = this.designHeight;
      let clone = entry.slide.cloneNode(true);
      clone.removeAttribute('id');
      clone.removeAttribute('data-deck-active');
      clone.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
      // Neuter heavy media; replace <video> with its poster so the box
      // keeps a visual. <iframe>/<audio> become empty placeholders.
      clone.querySelectorAll('iframe, audio, object, embed').forEach(el => {
        el.removeAttribute('src');
        el.removeAttribute('srcdoc');
        el.removeAttribute('data');
        el.innerHTML = '';
      });
      clone.querySelectorAll('video').forEach(el => {
        if (!el.poster) {
          el.removeAttribute('src');
          el.innerHTML = '';
          return;
        }
        const img = document.createElement('img');
        img.src = el.poster;
        img.alt = '';
        img.style.cssText = el.style.cssText + ';object-fit:cover;width:100%;height:100%;';
        img.className = el.className;
        el.replaceWith(img);
      });
      // Images: defer decode and let the browser pick the smallest
      // srcset candidate for the ~140px thumb. Same-URL clones reuse the
      // slide's decoded bitmap (URL-keyed cache), so the remaining cost
      // is paint/composite — lazy+async keeps that off the main thread.
      clone.querySelectorAll('img').forEach(el => {
        el.loading = 'lazy';
        el.decoding = 'async';
        if (el.srcset) el.sizes = (this._railPx || 188) + 'px';
      });
      // Custom elements inside the slide would have their
      // connectedCallback fire when the clone is appended. Replace them
      // with inert boxes so a component-heavy deck doesn't run N copies
      // of each component's mount logic in the rail. Children are
      // preserved so layout-wrapper elements (<my-column><h2>…</h2>)
      // still show their authored content; the querySelectorAll NodeList
      // is static, so nested custom elements in the moved subtree are
      // still visited on later iterations.
      const neuter = el => {
        const box = document.createElement('div');
        box.style.cssText = (el.getAttribute('style') || '') + ';background:rgba(0,0,0,0.06);border:1px dashed rgba(0,0,0,0.15);';
        box.className = el.className;
        // Preserve theming/i18n hooks so [data-*] / :lang() / [dir]
        // descendant selectors still match the neutered root.
        for (const a of el.attributes) {
          const n = a.name;
          if (n.startsWith('data-') || n.startsWith('aria-') || n === 'lang' || n === 'dir' || n === 'role' || n === 'title') {
            box.setAttribute(n, a.value);
          }
        }
        while (el.firstChild) box.appendChild(el.firstChild);
        return box;
      };
      // querySelectorAll('*') returns descendants only — a custom-element
      // slide root (<my-slide>…</my-slide>) would slip through and upgrade
      // on append. Swap the root first.
      if (clone.tagName.includes('-')) clone = neuter(clone);
      clone.querySelectorAll('*').forEach(el => {
        if (el.tagName.includes('-')) el.replaceWith(neuter(el));
      });
      clone.style.cssText += ';position:absolute;top:0;left:0;transform-origin:0 0;' + 'pointer-events:none;width:' + dw + 'px;height:' + dh + 'px;' + 'box-sizing:border-box;overflow:hidden;visibility:visible;opacity:1;';
      const host = document.createElement('div');
      host.style.cssText = 'position:absolute;inset:0;';
      this._syncThumbHostAttrs(host);
      const sr = host.attachShadow({
        mode: 'open'
      });
      if (this._adoptedSheet) sr.adoptedStyleSheets = [this._adoptedSheet];else {
        const st = document.createElement('style');
        st.textContent = this._authorCss || '';
        sr.appendChild(st);
      }
      sr.appendChild(clone);
      entry.frame.appendChild(host);
      entry.host = host;
      entry.clone = clone;
      if (this._thumbScale) clone.style.transform = 'scale(' + this._thumbScale + ')';
      // Once materialized the IO callback is a no-op early-return —
      // unobserve so scroll doesn't keep firing it.
      if (this._railObserver) this._railObserver.unobserve(entry.frame);
    }

    /** Re-clone a single thumb (live-update path). No-op if the thumb
     *  hasn't been materialized yet — it'll pick up current content when
     *  it scrolls into view. */
    _refreshThumb(slide) {
      const entry = (this._thumbs || []).find(t => t.slide === slide);
      if (!entry || !entry.host) return;
      entry.host.remove();
      entry.host = entry.clone = null;
      this._materialize(entry);
    }
    _scaleThumbs() {
      if (!this._thumbs || !this._thumbs.length) return;
      // Every frame is the same width; if it reads 0 the rail is
      // display:none (noscale / no-rail / presenting / print) — leave the
      // clones as-is and re-run when the rail is revealed.
      const fw = this._thumbs[0].frame.offsetWidth;
      if (!fw) return;
      this._thumbScale = fw / this.designWidth;
      this._thumbs.forEach(({
        clone
      }) => {
        if (clone) clone.style.transform = 'scale(' + this._thumbScale + ')';
      });
    }
    _setDrop(i, where) {
      // dragover fires at pointer-event rate; touch only the previous
      // and new target rather than sweeping all N thumbs.
      const t = this._thumbs && this._thumbs[i];
      if (this._dropOn && this._dropOn !== t) {
        this._dropOn.thumb.removeAttribute('data-drop');
      }
      if (t) t.thumb.setAttribute('data-drop', where);
      this._dropOn = t || null;
    }
    _clearDrop() {
      if (this._dropOn) this._dropOn.thumb.removeAttribute('data-drop');
      this._dropOn = null;
    }
    _syncRail(follow) {
      if (!this._thumbs) return;
      this._thumbs.forEach(({
        thumb
      }, i) => {
        if (i === this._index) {
          thumb.setAttribute('data-current', '');
          if (follow && typeof thumb.scrollIntoView === 'function') {
            thumb.scrollIntoView({
              block: 'nearest'
            });
          }
        } else {
          thumb.removeAttribute('data-current');
        }
      });
    }
    _openMenu(i, x, y) {
      if (!this._menu) return;
      this._menuIndex = i;
      const slide = this._slides[i];
      const skip = slide && slide.hasAttribute('data-deck-skip');
      this._menu.querySelector('[data-act="skip"]').textContent = skip ? 'Unskip slide' : 'Skip slide';
      this._menu.querySelector('[data-act="up"]').disabled = i <= 0;
      this._menu.querySelector('[data-act="down"]').disabled = i >= this._slides.length - 1;
      this._menu.querySelector('[data-act="delete"]').disabled = this._slides.length <= 1;
      // Place, then clamp to viewport after it's measurable.
      this._menu.style.left = x + 'px';
      this._menu.style.top = y + 'px';
      this._menu.setAttribute('data-open', '');
      const r = this._menu.getBoundingClientRect();
      const nx = Math.min(x, window.innerWidth - r.width - 4);
      const ny = Math.min(y, window.innerHeight - r.height - 4);
      this._menu.style.left = Math.max(4, nx) + 'px';
      this._menu.style.top = Math.max(4, ny) + 'px';
    }
    _closeMenu() {
      if (this._menu) this._menu.removeAttribute('data-open');
      this._menuIndex = -1;
    }
    _openConfirm(i) {
      if (!this._confirm) return;
      this._confirmIndex = i;
      this._confirm.querySelector('.title').textContent = 'Delete slide ' + (i + 1) + '?';
      this._confirm.setAttribute('data-open', '');
      const btn = this._confirm.querySelector('.danger');
      if (btn && btn.focus) btn.focus();
    }
    _closeConfirm() {
      if (this._confirm) this._confirm.removeAttribute('data-open');
      this._confirmIndex = -1;
    }
    _emitDeckChange(detail) {
      this.dispatchEvent(new CustomEvent('deckchange', {
        detail,
        bubbles: true,
        composed: true
      }));
    }
    _deleteSlide(i) {
      const slide = this._slides[i];
      if (!slide || this._slides.length <= 1) return;
      const wasCurrent = i === this._index;
      if (i < this._index || wasCurrent && i === this._slides.length - 1) this._index--;
      this._squelchSlotChange = true;
      slide.remove();
      this._emitDeckChange({
        action: 'delete',
        from: i,
        slide
      });
      this._collectSlides();
      this._applyIndex({
        showOverlay: true,
        broadcast: true,
        reason: 'mutation'
      });
    }
    _toggleSkip(i) {
      const slide = this._slides[i];
      if (!slide) return;
      const on = !slide.hasAttribute('data-deck-skip');
      if (on) slide.setAttribute('data-deck-skip', '');else slide.removeAttribute('data-deck-skip');
      if (this._thumbs && this._thumbs[i]) {
        if (on) this._thumbs[i].thumb.setAttribute('data-skip', '');else this._thumbs[i].thumb.removeAttribute('data-skip');
      }
      this._markLastVisible();
      this._emitDeckChange({
        action: on ? 'skip' : 'unskip',
        from: i,
        slide
      });
      // Re-broadcast so the presenter popup's prev/next thumbnails re-pick
      // the nearest non-skipped slide without waiting for a nav event.
      try {
        window.postMessage({
          slideIndexChanged: this._index,
          deckTotal: this._slides.length,
          deckSkipped: this._skippedIndices()
        }, '*');
      } catch (e) {}
    }
    _skippedIndices() {
      const out = [];
      for (let i = 0; i < this._slides.length; i++) {
        if (this._slides[i].hasAttribute('data-deck-skip')) out.push(i);
      }
      return out;
    }
    _moveSlide(i, j) {
      if (j < 0 || j >= this._slides.length || j === i) return;
      const slide = this._slides[i];
      const ref = j < i ? this._slides[j] : this._slides[j].nextSibling;
      // Track the active slide across the reorder so the same content
      // stays on screen.
      const cur = this._index;
      if (cur === i) this._index = j;else if (i < cur && j >= cur) this._index = cur - 1;else if (i > cur && j <= cur) this._index = cur + 1;
      this._squelchSlotChange = true;
      this.insertBefore(slide, ref);
      this._emitDeckChange({
        action: 'move',
        from: i,
        to: j,
        slide
      });
      this._collectSlides();
      this._applyIndex({
        showOverlay: false,
        broadcast: true,
        reason: 'mutation'
      });
    }

    // Public API ------------------------------------------------------------

    /** Current slide index (0-based). */
    get index() {
      return this._index;
    }
    /** Total slide count. */
    get length() {
      return this._slides.length;
    }
    /** Programmatically navigate. */
    goTo(i) {
      this._go(i, 'api');
    }
    next() {
      this._advance(1, 'api');
    }
    prev() {
      this._advance(-1, 'api');
    }
    reset() {
      this._go(0, 'api');
    }
  }
  if (!customElements.get('deck-stage')) {
    customElements.define('deck-stage', DeckStage);
  }
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "slides/deck-stage.js", error: String((e && e.message) || e) }); }

// slides/slide-field.js
try { (() => {
/* Market Story slides — static market-field motif on title/section/closing.
   Draws once per canvas[data-field]; redraws on resize + slide activation. */
(function () {
  const ACCENT = "123,234,251",
    FAINT = "179,170,160";
  function walk(n, drift, vol, seed) {
    let v = 0,
      o = [],
      s = seed;
    const r = () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
    for (let i = 0; i < n; i++) {
      v += drift + (r() - 0.5) * vol;
      o.push(v);
    }
    return o;
  }
  const SET = [{
    a: 1,
    d: 0.9,
    v: 2.2,
    s: 7
  }, {
    a: 0,
    d: 0.7,
    v: 3,
    s: 13
  }, {
    a: 0,
    d: 0.4,
    v: 3.4,
    s: 21
  }, {
    a: 0,
    d: 0.6,
    v: 2.8,
    s: 34
  }, {
    a: 0,
    d: -0.2,
    v: 3.6,
    s: 55
  }, {
    a: 0,
    d: 0.3,
    v: 4,
    s: 89
  }, {
    a: 0,
    d: 0.5,
    v: 2.6,
    s: 144
  }];
  const lines = SET.map(c => {
    const arr = walk(90, c.d, c.v, c.s);
    const mn = Math.min(...arr),
      mx = Math.max(...arr),
      rg = mx - mn || 1;
    return {
      a: c.a,
      y: arr.map(x => 1 - (x - mn) / rg)
    };
  }).sort((p, q) => p.a - q.a);
  function draw(cv) {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    const w = cv.clientWidth || 1920,
      h = cv.clientHeight || 1080;
    if (!w || !h) return;
    cv.width = w * dpr;
    cv.height = h * dpr;
    const W = cv.width,
      H = cv.height,
      ctx = cv.getContext("2d");
    ctx.clearRect(0, 0, W, H);
    const top = H * 0.46,
      band = H - top - H * 0.10;
    for (const ln of lines) {
      const N = ln.y.length,
        px = i => i / (N - 1) * W,
        py = i => top + ln.y[i] * band;
      if (ln.a) {
        ctx.beginPath();
        ctx.moveTo(px(0), py(0));
        for (let i = 1; i < N; i++) ctx.lineTo(px(i), py(i));
        ctx.lineTo(px(N - 1), top + band);
        ctx.lineTo(px(0), top + band);
        ctx.closePath();
        const g = ctx.createLinearGradient(0, top, 0, top + band);
        g.addColorStop(0, `rgba(${ACCENT},0.16)`);
        g.addColorStop(1, `rgba(${ACCENT},0)`);
        ctx.fillStyle = g;
        ctx.fill();
      }
      ctx.beginPath();
      ctx.moveTo(px(0), py(0));
      for (let i = 1; i < N; i++) ctx.lineTo(px(i), py(i));
      ctx.strokeStyle = ln.a ? `rgba(${ACCENT},0.95)` : `rgba(${FAINT},0.15)`;
      ctx.lineWidth = (ln.a ? 3 : 1.4) * dpr;
      ctx.stroke();
      if (ln.a) {
        const x = px(N - 1),
          y = py(N - 1);
        ctx.fillStyle = `rgba(${ACCENT},1)`;
        ctx.beginPath();
        ctx.arc(x, y, 6 * dpr, 0, 7);
        ctx.fill();
        ctx.strokeStyle = `rgba(${ACCENT},0.35)`;
        ctx.lineWidth = 1.5 * dpr;
        ctx.beginPath();
        ctx.arc(x, y, 13 * dpr, 0, 7);
        ctx.stroke();
      }
    }
  }
  function drawAll() {
    document.querySelectorAll("canvas[data-field]").forEach(draw);
  }
  // initial (deck-stage scales after define) + on resize + on slide change
  const kick = () => requestAnimationFrame(() => setTimeout(drawAll, 60));
  if (document.readyState !== "loading") kick();else addEventListener("DOMContentLoaded", kick);
  addEventListener("resize", drawAll);
  const stage = document.querySelector("deck-stage");
  if (stage) stage.addEventListener("slidechange", kick);
  setTimeout(drawAll, 400);
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "slides/slide-field.js", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/app.jsx
try { (() => {
/* Market Story dashboard — bundled component source.
   Concatenated from components / charts / panels / story for reliable single-fetch
   loading (Babel-in-browser XHR was flaky across many files). Edit sections here. */

/* ============================================================
   components.jsx
   ============================================================ */
/* Market Story dashboard — shell components (sidebar, header, KPI strip, read hero, tabs). */
const {
  useState
} = React;
const TONE = {
  up: "up",
  down: "down",
  warn: "warn",
  neutral: "neutral"
};

// tiny sparkline drawn from normalized 0..1 points
function Sparkline({
  points,
  up,
  big
}) {
  const w = 120,
    h = big ? 64 : 40,
    pad = 3;
  const n = points.length;
  const px = i => pad + i / (n - 1) * (w - pad * 2);
  const py = v => pad + (1 - v) * (h - pad * 2);
  const line = points.map((v, i) => `${i ? "L" : "M"}${px(i).toFixed(1)},${py(v).toFixed(1)}`).join(" ");
  const area = `${line} L${px(n - 1).toFixed(1)},${h - pad} L${px(0).toFixed(1)},${h - pad} Z`;
  const c = up ? "var(--up)" : "var(--down)";
  const gid = "g" + Math.random().toString(36).slice(2, 8);
  const lx = px(n - 1),
    ly = py(points[n - 1]);
  return /*#__PURE__*/React.createElement("svg", {
    className: "spark",
    viewBox: `0 0 ${w} ${h}`,
    preserveAspectRatio: "none",
    style: {
      width: "100%",
      height: h
    }
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
    id: gid,
    x1: "0",
    y1: "0",
    x2: "0",
    y2: "1"
  }, /*#__PURE__*/React.createElement("stop", {
    offset: "0",
    stopColor: c,
    stopOpacity: "0.18"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: "1",
    stopColor: c,
    stopOpacity: "0"
  }))), /*#__PURE__*/React.createElement("path", {
    d: area,
    fill: `url(#${gid})`
  }), /*#__PURE__*/React.createElement("path", {
    d: line,
    fill: "none",
    stroke: c,
    strokeWidth: big ? 1.8 : 1.4,
    strokeLinejoin: "round",
    strokeLinecap: "round"
  }), big && /*#__PURE__*/React.createElement("circle", {
    cx: lx,
    cy: ly,
    r: "2.6",
    fill: c,
    vectorEffect: "non-scaling-stroke"
  }));
}
function Sidebar({
  page,
  setPage,
  onRefresh,
  refreshing,
  ambient,
  setAmbient
}) {
  const icons = {
    show_chart: /*#__PURE__*/React.createElement("svg", {
      className: "ico",
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      strokeWidth: "2.1",
      strokeLinecap: "round",
      strokeLinejoin: "round",
      "aria-hidden": "true"
    }, /*#__PURE__*/React.createElement("path", {
      d: "M3.5 16.5 L9 11 L13 14 L20.5 6.5"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M16 6.5 H20.5 V11"
    })),
    school: /*#__PURE__*/React.createElement("svg", {
      className: "ico",
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      strokeWidth: "2",
      strokeLinecap: "round",
      strokeLinejoin: "round",
      "aria-hidden": "true"
    }, /*#__PURE__*/React.createElement("path", {
      d: "M2.5 9 L12 4.5 L21.5 9 L12 13.5 Z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M6.5 11.2 V16 C6.5 16 8.7 18 12 18 C15.3 18 17.5 16 17.5 16 V11.2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M21.5 9 V14.5"
    }))
  };
  const nav = [{
    id: "brief",
    label: "Daily Brief",
    ico: "show_chart"
  }, {
    id: "learn",
    label: "Learn the Markets",
    ico: "school"
  }];
  const levels = [["off", "Off"], ["low", "Low"], ["high", "High"]];
  return /*#__PURE__*/React.createElement("aside", {
    className: "sidebar"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sb-title"
  }, "Market Story"), /*#__PURE__*/React.createElement("nav", {
    "aria-label": "Primary"
  }, nav.map(n => /*#__PURE__*/React.createElement("button", {
    key: n.id,
    type: "button",
    className: "nav-item" + (page === n.id ? " active" : ""),
    "aria-current": page === n.id ? "page" : undefined,
    onClick: () => setPage(n.id)
  }, icons[n.ico], n.label, /*#__PURE__*/React.createElement("span", {
    className: "navx",
    "aria-hidden": "true"
  }, "\u2192")))), /*#__PURE__*/React.createElement("div", {
    className: "sb-sep"
  }), /*#__PURE__*/React.createElement("button", {
    className: "btn",
    type: "button",
    onClick: onRefresh,
    "aria-busy": refreshing
  }, refreshing ? "Refreshing…" : "Refresh data"), /*#__PURE__*/React.createElement("div", {
    className: "amb"
  }, /*#__PURE__*/React.createElement("div", {
    className: "aml"
  }, "Ambient field"), /*#__PURE__*/React.createElement("div", {
    className: "seg",
    role: "group",
    "aria-label": "Ambient field intensity"
  }, levels.map(([v, lbl]) => /*#__PURE__*/React.createElement("button", {
    key: v,
    type: "button",
    "aria-pressed": ambient === v,
    onClick: () => setAmbient(v)
  }, lbl)))), /*#__PURE__*/React.createElement("div", {
    className: "sb-cap",
    style: {
      marginTop: 14
    }
  }, "Scope: US equities & sectors + global macro"), /*#__PURE__*/React.createElement("div", {
    className: "sb-cap"
  }, "Sources: yfinance \xB7 FRED \xB7 12 RSS feeds"), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "sb-cap",
    style: {
      fontFamily: "var(--mono)",
      opacity: .7
    }
  }, "Python \xB7 Streamlit \xB7 Claude"));
}
function Header({
  d
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "hd"
  }, /*#__PURE__*/React.createElement("h1", null, "Global Markets Brief"), /*#__PURE__*/React.createElement("div", {
    className: "meta"
  }, d.session_label, "  \xB7  generated ", d.generated_at, " UTC"));
}
function MetricCard({
  k,
  loading
}) {
  const [open, setOpen] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    className: "metric" + (loading ? " is-loading" : ""),
    tabIndex: 0,
    role: "button",
    "aria-expanded": open,
    "aria-label": k.label + " " + k.val + " " + k.delta + " — show intraday",
    onMouseEnter: () => setOpen(true),
    onMouseLeave: () => setOpen(false),
    onFocus: () => setOpen(true),
    onBlur: () => setOpen(false)
  }, /*#__PURE__*/React.createElement("div", {
    className: "label"
  }, k.label), /*#__PURE__*/React.createElement("div", {
    className: "val"
  }, k.val), /*#__PURE__*/React.createElement("div", {
    className: "delta " + TONE[k.tone]
  }, k.delta), open && !loading && /*#__PURE__*/React.createElement("div", {
    className: "metric-pop",
    role: "tooltip"
  }, /*#__PURE__*/React.createElement("div", {
    className: "mp-head"
  }, /*#__PURE__*/React.createElement("span", null, k.label, " \xB7 intraday"), /*#__PURE__*/React.createElement("span", {
    className: "mono " + TONE[k.tone]
  }, k.delta)), /*#__PURE__*/React.createElement(Sparkline, {
    points: k.spark,
    up: k.sparkUp,
    big: true
  }), /*#__PURE__*/React.createElement("div", {
    className: "mp-foot mono"
  }, /*#__PURE__*/React.createElement("span", null, "O ", k.val), /*#__PURE__*/React.createElement("span", {
    className: "dim"
  }, "range shown \xB7 1D"))));
}
function KpiStrip({
  d,
  loading
}) {
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "kpis"
  }, d.kpis.map(k => /*#__PURE__*/React.createElement(MetricCard, {
    key: k.sym,
    k: k,
    loading: loading
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sparks",
    "aria-hidden": "true"
  }, d.kpis.map(k => /*#__PURE__*/React.createElement(Sparkline, {
    key: k.sym,
    points: k.spark,
    up: k.sparkUp
  }))), /*#__PURE__*/React.createElement("div", {
    className: "breadth"
  }, "Sector breadth: ", /*#__PURE__*/React.createElement("span", {
    className: "up"
  }, d.stats.sector_advancers, " up"), " / ", /*#__PURE__*/React.createElement("span", {
    className: "down"
  }, d.stats.sector_decliners, " down"), " of ", d.stats.sector_count));
}
function ReadHero({
  d,
  onStory
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "hero"
  }, /*#__PURE__*/React.createElement("div", {
    className: "kick"
  }, "\u25CF Today's thesis"), /*#__PURE__*/React.createElement("div", {
    className: "read"
  }, d.read), /*#__PURE__*/React.createElement("div", {
    className: "more"
  }, "Full read in the ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: "var(--text)"
    }
  }, "Story"), " tab \u2192 ", /*#__PURE__*/React.createElement("a", {
    href: "#",
    onClick: e => {
      e.preventDefault();
      onStory && onStory();
    },
    style: {
      marginLeft: 4
    }
  }, "open")));
}
function Signals({
  d
}) {
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("h2", {
    className: "subhead",
    style: {
      marginTop: 18
    }
  }, "\u26A1 Today's signal"), /*#__PURE__*/React.createElement("div", {
    className: "sigwrap"
  }, d.signals.map((s, i) => /*#__PURE__*/React.createElement("div", {
    className: "sig",
    key: i
  }, /*#__PURE__*/React.createElement("span", {
    className: "dot " + TONE[s.tone]
  }, "\u25CF"), s.text))));
}
function Tabs({
  tabs,
  active,
  setActive
}) {
  const onKey = e => {
    const i = tabs.indexOf(active);
    let n = null;
    if (e.key === "ArrowRight" || e.key === "ArrowDown") n = (i + 1) % tabs.length;else if (e.key === "ArrowLeft" || e.key === "ArrowUp") n = (i - 1 + tabs.length) % tabs.length;else if (e.key === "Home") n = 0;else if (e.key === "End") n = tabs.length - 1;
    if (n !== null) {
      e.preventDefault();
      setActive(tabs[n]);
    }
  };
  const slug = t => "tab-" + t.replace(/[^a-z]+/gi, "-").toLowerCase();
  return /*#__PURE__*/React.createElement("div", {
    className: "tabs",
    role: "tablist",
    "aria-label": "Brief sections",
    onKeyDown: onKey
  }, tabs.map(t => {
    const on = t === active;
    return /*#__PURE__*/React.createElement("button", {
      key: t,
      id: slug(t),
      role: "tab",
      type: "button",
      "aria-selected": on,
      "aria-controls": "tabpane",
      tabIndex: on ? 0 : -1,
      className: "tab" + (on ? " active" : ""),
      onClick: () => setActive(t)
    }, t);
  }));
}

// dismissible freshness notice — authentic to the product's data caveat
function Notice({
  children,
  onClose
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "notice",
    role: "status"
  }, /*#__PURE__*/React.createElement("span", {
    className: "ndot",
    "aria-hidden": "true"
  }, "\u25CF"), /*#__PURE__*/React.createElement("span", null, children), /*#__PURE__*/React.createElement("button", {
    className: "nx",
    type: "button",
    "aria-label": "Dismiss notice",
    onClick: onClose
  }, "\u2715"));
}

// data-load error guard (shown if MS_DATA is missing)
function ErrorBox({
  onRetry
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "errorbox",
    role: "alert"
  }, /*#__PURE__*/React.createElement("div", {
    className: "eg",
    "aria-hidden": "true"
  }, "\u26A0"), /*#__PURE__*/React.createElement("div", {
    className: "et"
  }, "Couldn't load today's brief"), /*#__PURE__*/React.createElement("div", {
    className: "es"
  }, "The data feed didn't return. Markets data is best-effort from free sources \u2014 try again in a moment."), /*#__PURE__*/React.createElement("button", {
    className: "btn",
    type: "button",
    onClick: onRetry
  }, "Retry"));
}

// scroll-reveal wrapper — base state is visible (added by JS), so content never
// hides if scripts fail. Adds `.reveal` on mount, then `.in` when scrolled into view.
function Reveal({
  children,
  className,
  style
}) {
  const ref = React.useRef(null);
  React.useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.classList.add("reveal");
    const show = () => el.classList.add("in");
    // above-the-fold → reveal now (gentle fade); below-fold → on scroll; always a safety net
    const r = el.getBoundingClientRect();
    if (r.top < (window.innerHeight || 800) * 0.92) {
      requestAnimationFrame(show);
      return;
    }
    let io;
    try {
      io = new IntersectionObserver(entries => {
        entries.forEach(e => {
          if (e.isIntersecting) {
            show();
            io.unobserve(el);
          }
        });
      }, {
        threshold: 0.08,
        rootMargin: "0px 0px -6% 0px"
      });
      io.observe(el);
    } catch (_) {
      show();
    }
    const t = setTimeout(show, 2500);
    return () => {
      if (io) io.disconnect();
      clearTimeout(t);
    };
  }, []);
  return /*#__PURE__*/React.createElement("div", {
    ref: ref,
    className: className,
    style: style
  }, children);
}

// The cover — the landing folded into the product. Same warm palette + cyan field.
function Cover({
  d,
  out,
  onEnter,
  ambient,
  accentRGB,
  faintRGB
}) {
  const cv = React.useRef(null);
  const btn = React.useRef(null);
  React.useEffect(() => {
    if (!cv.current || !window.startMarketField) return;
    const f = window.startMarketField(cv.current, {
      topFrac: 0.5,
      botFrac: 0.13,
      parallax: 48,
      intensity: ambient,
      accentRGB: accentRGB,
      faintRGB: faintRGB
    });
    return () => f.destroy();
  }, []);
  React.useEffect(() => {
    const t = setTimeout(() => {
      try {
        btn.current && btn.current.focus();
      } catch (_) {}
    }, 200);
    const onKey = e => {
      if (e.key === "Enter" && document.activeElement !== btn.current) onEnter();
    };
    window.addEventListener("keydown", onKey);
    return () => {
      clearTimeout(t);
      window.removeEventListener("keydown", onKey);
    };
  }, []);
  const tape = [["S&P 500", d.kpis[0].val, d.kpis[0].delta, d.kpis[0].tone], ["VIX", "16.50", "+2.8%", "down"], ["US 10Y", "4.491%", "yield", ""], ["Sector breadth", "4 / 7", "up / down", ""]];
  return /*#__PURE__*/React.createElement("div", {
    className: "cover" + (out ? " gone" : ""),
    role: "region",
    "aria-label": "Market Story \u2014 cover",
    "aria-hidden": out
  }, /*#__PURE__*/React.createElement("canvas", {
    ref: cv,
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("div", {
    className: "cscrim"
  }), /*#__PURE__*/React.createElement("div", {
    className: "cwrap"
  }, /*#__PURE__*/React.createElement("div", {
    className: "ctop"
  }, /*#__PURE__*/React.createElement("span", {
    className: "brand"
  }, "MARKET STORY", /*#__PURE__*/React.createElement("sup", null, "\xAE")), /*#__PURE__*/React.createElement("span", {
    className: "mid"
  }, "Daily global-markets intelligence"), /*#__PURE__*/React.createElement("span", null, d.date)), /*#__PURE__*/React.createElement("div", {
    className: "chero"
  }, /*#__PURE__*/React.createElement("div", {
    className: "ckick"
  }, "\u2116 ", d.date.replace(/-/g, ""), " \u2014 Markets, narrated."), /*#__PURE__*/React.createElement("h1", {
    className: "cword"
  }, "Market", /*#__PURE__*/React.createElement("br", null), "Story", /*#__PURE__*/React.createElement("sup", null, "\xAE")), /*#__PURE__*/React.createElement("div", {
    className: "csub"
  }, /*#__PURE__*/React.createElement("p", {
    className: "ctag"
  }, "A daily global brief with a risk lens \u2014 gathered, synthesized by Claude, and built to be questioned and re-run."), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("button", {
    className: "center",
    type: "button",
    ref: btn,
    onClick: onEnter
  }, "Enter the brief ", /*#__PURE__*/React.createElement("span", {
    className: "ar",
    "aria-hidden": "true"
  }, "\u2192")), /*#__PURE__*/React.createElement("div", {
    className: "chint"
  }, "Press ", /*#__PURE__*/React.createElement("kbd", null, "Enter \u21B5"), " to open the brief")))), /*#__PURE__*/React.createElement("div", {
    className: "ctape"
  }, tape.map((t, i) => /*#__PURE__*/React.createElement("div", {
    className: "ctk",
    key: i
  }, /*#__PURE__*/React.createElement("span", {
    className: "k"
  }, t[0]), /*#__PURE__*/React.createElement("span", {
    className: "v"
  }, t[1]), /*#__PURE__*/React.createElement("span", {
    className: "d " + (TONE[t[3]] || "")
  }, t[2]))))));
}
Object.assign(window, {
  Sparkline,
  Sidebar,
  Header,
  KpiStrip,
  ReadHero,
  Signals,
  Tabs,
  Notice,
  ErrorBox,
  Reveal,
  Cover,
  TONE
});

/* ============================================================
   charts.jsx
   ============================================================ */
/* Market Story dashboard — real data-viz: squarified sector treemap, the
   cyan-anchored cross-asset correlation matrix, the Treasury yield curve, and a
   layered Sankey for the Learn page. Plain SVG/divs, on-palette. */

// on-palette diverging color: red <- warm-dark -> cyan/green
function _mix(a, b, t) {
  return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(",")})`;
}
const _DARK = [27, 22, 17],
  _CYAN = [123, 234, 251],
  _GREEN = [54, 194, 111],
  _RED = [255, 92, 108];
function diffColor(v, span, pole) {
  // pole: 'green' (treemap) or 'cyan' (corr)
  const t = Math.max(-1, Math.min(1, v / span));
  const up = pole === "cyan" ? _CYAN : _GREEN;
  return t >= 0 ? _mix(_DARK, up, t) : _mix(_DARK, _RED, -t);
}

/* ---- Squarified treemap (sized by index weight, colored by 1-day change) ---- */
const SECTOR_WEIGHT = {
  Technology: 32,
  Financials: 13,
  Health: 11,
  Discretionary: 10.5,
  "Comm Svcs": 9,
  Industrials: 8,
  Staples: 6,
  Energy: 4,
  Utilities: 2.6,
  "Real Estate": 2.2,
  Materials: 2.0
};
function squarify(items, W, H) {
  const nodes = items.map(d => ({
    ...d
  }));
  const total = nodes.reduce((s, n) => s + n.value, 0) || 1;
  nodes.forEach(n => n.area = n.value / total * W * H);
  const out = [];
  let x = 0,
    y = 0,
    w = W,
    h = H,
    row = [];
  const remaining = nodes.slice();
  const worst = (r, side) => {
    let sum = 0,
      mx = -Infinity,
      mn = Infinity;
    for (const n of r) {
      sum += n.area;
      if (n.area > mx) mx = n.area;
      if (n.area < mn) mn = n.area;
    }
    const s2 = sum * sum,
      d2 = side * side;
    return Math.max(d2 * mx / s2, s2 / (d2 * mn));
  };
  const flush = (r, side, horiz) => {
    const sum = r.reduce((a, n) => a + n.area, 0);
    const thick = sum / side;
    let pos = horiz ? y : x;
    for (const n of r) {
      const len = n.area / thick;
      out.push({
        ...n,
        x: horiz ? x : pos,
        y: horiz ? pos : y,
        w: horiz ? thick : len,
        h: horiz ? len : thick
      });
      pos += len;
    }
    if (horiz) {
      x += thick;
      w -= thick;
    } else {
      y += thick;
      h -= thick;
    }
  };
  while (remaining.length) {
    const horiz = w < h,
      side = horiz ? h : w;
    if (!row.length) {
      row.push(remaining.shift());
      continue;
    }
    if (worst([...row, remaining[0]], side) <= worst(row, side)) row.push(remaining.shift());else {
      flush(row, side, horiz);
      row = [];
    }
  }
  if (row.length) {
    const horiz = w < h;
    flush(row, horiz ? h : w, horiz);
  }
  return out;
}
function SectorTreemap({
  sectors
}) {
  const W = 1040,
    H = 380;
  const items = sectors.map(s => ({
    name: s.name,
    chg: s.chg,
    value: SECTOR_WEIGHT[s.name] || 3
  }));
  const tiles = squarify(items, W, H);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      width: "100%",
      height: 380,
      borderRadius: 10,
      overflow: "hidden"
    }
  }, tiles.map((t, i) => {
    const big = t.w > 110 && t.h > 54;
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      style: {
        position: "absolute",
        left: `${t.x / W * 100}%`,
        top: `${t.y / H * 100}%`,
        width: `${t.w / W * 100}%`,
        height: `${t.h / H * 100}%`,
        padding: big ? "10px 12px" : "5px 7px",
        background: diffColor(t.chg, 2.5, "green"),
        border: "1px solid rgba(13,12,12,.55)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        overflow: "hidden"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontFamily: "var(--grot)",
        fontWeight: 600,
        fontSize: big ? ".82rem" : ".64rem",
        color: "var(--text)",
        lineHeight: 1.1
      }
    }, t.name), /*#__PURE__*/React.createElement("div", {
      style: {
        fontFamily: "var(--mono)",
        fontSize: big ? ".84rem" : ".62rem",
        color: t.chg >= 0 ? "var(--up)" : "var(--down)"
      }
    }, t.chg >= 0 ? "+" : "", t.chg.toFixed(2), "%"));
  }));
}

/* ---- Cross-asset correlation matrix (cyan-anchored: +1 cyan, 0 dark, -1 red) ---- */
const CORR_LABELS = ["S&P", "Nasdaq", "Russell", "10Y", "Dollar", "Gold", "WTI", "HY", "VIX"];
const CORR = [[1.00, 0.96, 0.88, -0.42, -0.31, 0.12, 0.18, 0.74, -0.82], [0.96, 1.00, 0.82, -0.38, -0.29, 0.08, 0.14, 0.69, -0.79], [0.88, 0.82, 1.00, -0.46, -0.22, 0.18, 0.24, 0.71, -0.71], [-0.42, -0.38, -0.46, 1.00, 0.54, -0.28, 0.16, -0.34, 0.30], [-0.31, -0.29, -0.22, 0.54, 1.00, -0.61, -0.18, -0.26, 0.22], [0.12, 0.08, 0.18, -0.28, -0.61, 1.00, 0.34, 0.10, 0.08], [0.18, 0.14, 0.24, 0.16, -0.18, 0.34, 1.00, 0.22, -0.12], [0.74, 0.69, 0.71, -0.34, -0.26, 0.10, 0.22, 1.00, -0.58], [-0.82, -0.79, -0.71, 0.30, 0.22, 0.08, -0.12, -0.58, 1.00]];
function CorrMatrix() {
  const n = CORR_LABELS.length;
  return /*#__PURE__*/React.createElement("div", {
    className: "chart"
  }, /*#__PURE__*/React.createElement("div", {
    className: "ct"
  }, "Cross-asset return correlation \xB7 last 60 sessions"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: `60px repeat(${n}, 1fr)`,
      gap: 2,
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement("div", null), CORR_LABELS.map(l => /*#__PURE__*/React.createElement("div", {
    key: l,
    style: {
      fontFamily: "var(--mono)",
      fontSize: ".6rem",
      color: "var(--text-dim)",
      textAlign: "center",
      paddingBottom: 4
    }
  }, l)), CORR.map((row, r) => /*#__PURE__*/React.createElement(React.Fragment, {
    key: r
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--mono)",
      fontSize: ".62rem",
      color: "var(--text-dim)",
      display: "flex",
      alignItems: "center",
      justifyContent: "flex-end",
      paddingRight: 6
    }
  }, CORR_LABELS[r]), row.map((v, c) => /*#__PURE__*/React.createElement("div", {
    key: c,
    title: `${CORR_LABELS[r]}·${CORR_LABELS[c]} ${v.toFixed(2)}`,
    style: {
      background: diffColor(v, 1, "cyan"),
      aspectRatio: "1 / 1",
      borderRadius: 3,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "var(--mono)",
      fontSize: ".58rem",
      color: Math.abs(v) > 0.55 ? "rgba(13,12,12,.9)" : "rgba(245,242,239,.62)"
    }
  }, v.toFixed(2)))))), /*#__PURE__*/React.createElement("div", {
    className: "tcap",
    style: {
      marginTop: 8
    }
  }, "Watch for regime shifts \u2014 stock\u2013bond decoupling, or everything \u2192 +1 in a selloff. S&P\u2013HY at ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: "var(--text)"
    }
  }, "+0.74"), "; S&P\u2013VIX at ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: "var(--text)"
    }
  }, "\u22120.82"), "."));
}

/* ---- US Treasury yield curve ---- */
function YieldCurve({
  rates
}) {
  const mat = {
    "13-week": 0.25,
    "5-year": 5,
    "10-year": 10,
    "30-year": 30
  };
  const lab = {
    "13-week": "13W",
    "5-year": "5Y",
    "10-year": "10Y",
    "30-year": "30Y"
  };
  const pts = rates.filter(r => mat[r.name] != null).map(r => ({
    x: mat[r.name],
    y: parseFloat(r.last),
    l: lab[r.name]
  })).sort((a, b) => a.x - b.x);
  const W = 520,
    H = 240,
    pad = 38;
  const xs = pts.map(p => p.x),
    ys = pts.map(p => p.y);
  const xmin = 0,
    xmax = 30,
    ymin = Math.min(...ys) - 0.15,
    ymax = Math.max(...ys) + 0.15;
  const px = x => pad + (x - xmin) / (xmax - xmin) * (W - pad * 1.4);
  const py = y => H - pad - (y - ymin) / (ymax - ymin) * (H - pad * 1.6);
  const line = pts.map((p, i) => `${i ? "L" : "M"}${px(p.x).toFixed(1)},${py(p.y).toFixed(1)}`).join(" ");
  const ticks = [ymin, (ymin + ymax) / 2, ymax];
  return /*#__PURE__*/React.createElement("div", {
    className: "chart"
  }, /*#__PURE__*/React.createElement("div", {
    className: "ct"
  }, "US Treasury yield curve"), /*#__PURE__*/React.createElement("svg", {
    viewBox: `0 0 ${W} ${H}`,
    style: {
      width: "100%",
      height: 240
    }
  }, ticks.map((t, i) => /*#__PURE__*/React.createElement("g", {
    key: i
  }, /*#__PURE__*/React.createElement("line", {
    x1: pad,
    x2: W - 8,
    y1: py(t),
    y2: py(t),
    stroke: "var(--grid)",
    strokeWidth: "1"
  }), /*#__PURE__*/React.createElement("text", {
    x: 6,
    y: py(t) + 3,
    fontFamily: "var(--mono)",
    fontSize: "10",
    fill: "var(--text-dim)"
  }, t.toFixed(2)))), /*#__PURE__*/React.createElement("path", {
    d: line,
    fill: "none",
    stroke: "var(--accent)",
    strokeWidth: "2",
    strokeLinejoin: "round"
  }), pts.map((p, i) => /*#__PURE__*/React.createElement("g", {
    key: i
  }, /*#__PURE__*/React.createElement("circle", {
    cx: px(p.x),
    cy: py(p.y),
    r: "3.5",
    fill: "var(--accent)"
  }), /*#__PURE__*/React.createElement("text", {
    x: px(p.x),
    y: py(p.y) - 9,
    textAnchor: "middle",
    fontFamily: "var(--mono)",
    fontSize: "10",
    fill: "var(--text)"
  }, p.l), /*#__PURE__*/React.createElement("text", {
    x: px(p.x),
    y: H - 14,
    textAnchor: "middle",
    fontFamily: "var(--mono)",
    fontSize: "9.5",
    fill: "var(--text-dim)"
  }, p.y.toFixed(2), "%")))), /*#__PURE__*/React.createElement("div", {
    className: "tcap"
  }, "2s10s pinned at ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: "var(--text)"
    }
  }, "0.41%"), " \u2014 flattest of the year (0th %ile). The curve isn't steepening."));
}

/* ---- Layered Sankey (money flow) ---- */
function Sankey({
  data,
  height = 360
}) {
  const W = 900,
    H = height,
    pad = 6;
  const layers = {};
  data.nodes.forEach(n => {
    (layers[n.layer] = layers[n.layer] || []).push(n);
  });
  const layerKeys = Object.keys(layers).map(Number).sort((a, b) => a - b);
  const colX = l => pad + l / (layerKeys.length - 1) * (W - pad * 2 - 120) + 60;
  const nodeW = 13,
    gap = 16;
  const byId = {};
  // node value = max(in,out)
  data.nodes.forEach(n => {
    n.in = 0;
    n.out = 0;
  });
  data.links.forEach(k => {
    const s = data.nodes.find(n => n.id === k.source),
      t = data.nodes.find(n => n.id === k.target);
    if (s) s.out += k.value;
    if (t) t.in += k.value;
  });
  layerKeys.forEach(lk => {
    const ns = layers[lk];
    const totalVal = ns.reduce((a, n) => a + Math.max(n.in, n.out), 0);
    const avail = H - pad * 2 - gap * (ns.length - 1);
    let yy = pad;
    ns.forEach(n => {
      const hh = Math.max(8, Math.max(n.in, n.out) / totalVal * avail);
      n._x = colX(lk);
      n._y = yy;
      n._h = hh;
      n._so = 0;
      n._to = 0;
      byId[n.id] = n;
      yy += hh + gap;
    });
  });
  const ribbons = data.links.map((k, i) => {
    const s = byId[k.source],
      t = byId[k.target];
    const sy = s._y + s._so + k.value / Math.max(s.in, s.out) * s._h / 2;
    const ty = t._y + t._to + k.value / Math.max(t.in, t.out) * t._h / 2;
    const th = k.value / Math.max(s.in, s.out) * s._h;
    s._so += k.value / Math.max(s.in, s.out) * s._h;
    t._to += k.value / Math.max(t.in, t.out) * t._h;
    const x0 = s._x + nodeW,
      x1 = t._x,
      mx = (x0 + x1) / 2;
    return /*#__PURE__*/React.createElement("path", {
      key: i,
      d: `M${x0},${sy} C${mx},${sy} ${mx},${ty} ${x1},${ty}`,
      fill: "none",
      stroke: "rgba(123,234,251,0.28)",
      strokeWidth: Math.max(1, th)
    });
  });
  return /*#__PURE__*/React.createElement("div", {
    className: "chart"
  }, /*#__PURE__*/React.createElement("div", {
    className: "ct"
  }, data.title), /*#__PURE__*/React.createElement("svg", {
    viewBox: `0 0 ${W} ${H}`,
    style: {
      width: "100%",
      height
    }
  }, ribbons, data.nodes.map((n, i) => /*#__PURE__*/React.createElement("g", {
    key: i
  }, /*#__PURE__*/React.createElement("rect", {
    x: n._x,
    y: n._y,
    width: nodeW,
    height: n._h,
    rx: "2",
    fill: "var(--accent)",
    opacity: "0.92"
  }), /*#__PURE__*/React.createElement("text", {
    x: n.layer === layerKeys[layerKeys.length - 1] ? n._x - 6 : n._x + nodeW + 6,
    y: n._y + n._h / 2 + 3,
    textAnchor: n.layer === layerKeys[layerKeys.length - 1] ? "end" : "start",
    fontFamily: "var(--grot)",
    fontWeight: "600",
    fontSize: "11.5",
    fill: "var(--text)"
  }, n.label)))));
}
Object.assign(window, {
  SectorTreemap,
  CorrMatrix,
  YieldCurve,
  Sankey,
  diffColor
});

/* ============================================================
   panels.jsx
   ============================================================ */
/* Market Story dashboard — tab panels (data tables, treemap, story, etc.) */

function DataTable({
  title,
  rows,
  kind,
  caption,
  heat
}) {
  const cls = t => "td " + (window.TONE[t] || "");
  const head = kind === "yield" ? ["Instrument", "Last", "1D bps", "1W %", "YTD %"] : ["Instrument", "Last", "1D %", "1W %", "YTD %"];
  const heatBg = t => {
    if (!heat) return undefined;
    if (t === "up") return "linear-gradient(90deg, rgba(54,194,111,.13), transparent 60%)";
    if (t === "down") return "linear-gradient(90deg, rgba(255,92,108,.13), transparent 60%)";
    return undefined;
  };
  return /*#__PURE__*/React.createElement("div", null, title && /*#__PURE__*/React.createElement("h3", {
    className: "subhead"
  }, title), /*#__PURE__*/React.createElement("table", {
    className: "tbl" + (heat ? " heat" : "")
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, head.map(h => /*#__PURE__*/React.createElement("th", {
    key: h,
    className: heat && h.startsWith("1D") ? "th-hi" : undefined
  }, h)))), /*#__PURE__*/React.createElement("tbody", null, rows.map((r, i) => /*#__PURE__*/React.createElement("tr", {
    key: i,
    style: {
      background: heatBg(r.t1)
    }
  }, /*#__PURE__*/React.createElement("td", null, r.name), /*#__PURE__*/React.createElement("td", null, r.last), /*#__PURE__*/React.createElement("td", {
    className: window.TONE[r.t1],
    style: heat ? {
      fontWeight: 600
    } : undefined
  }, r.d1), /*#__PURE__*/React.createElement("td", {
    className: window.TONE[r.tw]
  }, r.w1), /*#__PURE__*/React.createElement("td", {
    className: window.TONE[r.ty]
  }, r.ytd))))), caption && /*#__PURE__*/React.createElement("div", {
    className: "tcap"
  }, caption));
}

// toggle control reused above table pairs
function DiffToggle({
  on,
  set
}) {
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "difftoggle" + (on ? " on" : ""),
    "aria-pressed": on,
    onClick: () => set(!on)
  }, /*#__PURE__*/React.createElement("span", {
    className: "dt-dot",
    "aria-hidden": "true"
  }), "Highlight day change");
}

// (Sector treemap, correlation matrix & yield curve now live in charts.jsx)

function Movers({
  d
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "two"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h3", {
    className: "subhead"
  }, "Leaders"), d.leaders.map((m, i) => /*#__PURE__*/React.createElement("div", {
    className: "mover",
    key: i
  }, /*#__PURE__*/React.createElement("span", {
    className: "mn"
  }, m.name), /*#__PURE__*/React.createElement("span", {
    className: "mc " + window.TONE[m.tone]
  }, m.chg)))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h3", {
    className: "subhead"
  }, "Laggards"), d.laggards.map((m, i) => /*#__PURE__*/React.createElement("div", {
    className: "mover",
    key: i
  }, /*#__PURE__*/React.createElement("span", {
    className: "mn"
  }, m.name), /*#__PURE__*/React.createElement("span", {
    className: "mc " + window.TONE[m.tone]
  }, m.chg)))));
}

// a simple area line chart for "S&P 500"
function BigChart({
  title
}) {
  const pts = [.30, .42, .38, .50, .46, .40, .55, .62, .58, .70, .66, .74, .69, .80, .76, .85];
  const w = 900,
    h = 300,
    pad = 10;
  const px = i => pad + i / (pts.length - 1) * (w - pad * 2),
    py = v => pad + (1 - v) * (h - pad * 2);
  const line = pts.map((v, i) => `${i ? "L" : "M"}${px(i).toFixed(1)},${py(v).toFixed(1)}`).join(" ");
  const area = `${line} L${px(pts.length - 1)},${h - pad} L${px(0)},${h - pad} Z`;
  return /*#__PURE__*/React.createElement("div", {
    className: "chart"
  }, /*#__PURE__*/React.createElement("div", {
    className: "ct"
  }, title), /*#__PURE__*/React.createElement("svg", {
    viewBox: `0 0 ${w} ${h}`,
    style: {
      width: "100%",
      height: 300
    },
    preserveAspectRatio: "none"
  }, [0, .25, .5, .75, 1].map(g => /*#__PURE__*/React.createElement("line", {
    key: g,
    x1: pad,
    x2: w - pad,
    y1: pad + g * (h - pad * 2),
    y2: pad + g * (h - pad * 2),
    stroke: "var(--grid)",
    strokeWidth: "1"
  })), /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
    id: "bigfill",
    x1: "0",
    y1: "0",
    x2: "0",
    y2: "1"
  }, /*#__PURE__*/React.createElement("stop", {
    offset: "0",
    stopColor: "var(--accent)",
    stopOpacity: ".10"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: "1",
    stopColor: "var(--accent)",
    stopOpacity: "0"
  }))), /*#__PURE__*/React.createElement("path", {
    d: area,
    fill: "url(#bigfill)"
  }), /*#__PURE__*/React.createElement("path", {
    d: line,
    fill: "none",
    stroke: "var(--accent)",
    strokeWidth: "2",
    strokeLinejoin: "round"
  })));
}
function OverviewTab({
  d,
  onStory
}) {
  const Reveal = window.Reveal;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(ReadHero, {
    d: d,
    onStory: onStory
  }), /*#__PURE__*/React.createElement(Signals, {
    d: d
  }), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement(Reveal, null, /*#__PURE__*/React.createElement(Movers, {
    d: d
  })), /*#__PURE__*/React.createElement(Reveal, null, /*#__PURE__*/React.createElement(BigChart, {
    title: "S&P 500"
  })));
}
function EquitiesTab({
  d
}) {
  const [heat, setHeat] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h2", {
    className: "h2"
  }, "Sector map \xB7 1-day % change"), /*#__PURE__*/React.createElement(SectorTreemap, {
    sectors: d.sectors
  }), /*#__PURE__*/React.createElement("div", {
    className: "tcap",
    style: {
      marginTop: 8
    }
  }, "Tile size = index weight \xB7 color = 1-day move (on-palette diverging: red \u2192 warm-dark \u2192 green)."), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("div", {
    className: "tbl-bar"
  }, /*#__PURE__*/React.createElement("span", {
    className: "subhead",
    style: {
      margin: 0
    }
  }, "Cross-asset tables"), /*#__PURE__*/React.createElement(DiffToggle, {
    on: heat,
    set: setHeat
  })), /*#__PURE__*/React.createElement("div", {
    className: "two"
  }, /*#__PURE__*/React.createElement(DataTable, {
    title: "US Equities",
    rows: d.us_equities,
    caption: "% changes; VIX delta inverts",
    heat: heat
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(DataTable, {
    title: "Commodities",
    rows: d.commodities,
    caption: "WTI broke its floor overnight",
    heat: heat
  }))));
}
function MacroTab({
  d
}) {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h3", {
    className: "subhead"
  }, "Risk regime \u2014 mixed, late-cycle"), /*#__PURE__*/React.createElement("div", {
    className: "regime"
  }, d.regime.map((r, i) => /*#__PURE__*/React.createElement("div", {
    className: "rcell",
    key: i
  }, /*#__PURE__*/React.createElement("div", {
    className: "rl"
  }, r.label), /*#__PURE__*/React.createElement("div", {
    className: "rv " + window.TONE[r.t]
  }, r.val)))), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("div", {
    className: "two"
  }, /*#__PURE__*/React.createElement(DataTable, {
    title: "Global Indices",
    rows: d.global_indices
  }), /*#__PURE__*/React.createElement(DataTable, {
    title: "Rates (Treasury yields)",
    rows: d.rates,
    kind: "yield",
    caption: "Last in %, 1D in bps"
  })), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("div", {
    className: "two"
  }, /*#__PURE__*/React.createElement(DataTable, {
    title: "FX",
    rows: d.fx
  }), /*#__PURE__*/React.createElement(DataTable, {
    title: "Credit & Bonds",
    rows: d.credit
  })), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("h3", {
    className: "subhead"
  }, "Macro (FRED) \xB7 1-year percentile"), /*#__PURE__*/React.createElement("table", {
    className: "tbl"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Series"), /*#__PURE__*/React.createElement("th", null, "Latest"), /*#__PURE__*/React.createElement("th", null, "\u0394"), /*#__PURE__*/React.createElement("th", null, "1y %ile"))), /*#__PURE__*/React.createElement("tbody", null, d.macro.map((m, i) => /*#__PURE__*/React.createElement("tr", {
    key: i
  }, /*#__PURE__*/React.createElement("td", null, m.name), /*#__PURE__*/React.createElement("td", null, m.latest), /*#__PURE__*/React.createElement("td", {
    className: window.TONE[m.t]
  }, m.chg), /*#__PURE__*/React.createElement("td", {
    className: "neutral"
  }, m.pct))))), /*#__PURE__*/React.createElement("div", {
    className: "tcap"
  }, "Vol risk premium: VIX 16.5 vs 9.9 realized (20d) = +6.6 pts (rich \u2014 complacency / cheap-looking hedges)."), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("div", {
    className: "two"
  }, /*#__PURE__*/React.createElement(YieldCurve, {
    rates: d.rates
  }), /*#__PURE__*/React.createElement(CorrMatrix, null)));
}
function TrendsTab({
  d
}) {
  const metrics = [{
    t: "10Y Treasury yield (%)",
    v: "4.49",
    pct: "96",
    up: true
  }, {
    t: "2s10s curve (pp)",
    v: "0.41",
    pct: "0",
    up: false
  }, {
    t: "HY credit spread (%)",
    v: "2.71",
    pct: "3",
    up: false
  }, {
    t: "VIX",
    v: "16.5",
    pct: "34",
    up: false
  }];
  const paths = [[.5, .45, .4, .5, .55, .6, .66, .7, .74, .8], [.8, .7, .62, .5, .42, .35, .28, .2, .14, .08], [.7, .6, .5, .4, .32, .25, .18, .12, .08, .05], [.4, .5, .45, .6, .55, .7, .5, .6, .45, .5]];
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "tcap",
    style: {
      marginBottom: 16
    }
  }, "847 sessions \xB7 2022-11-01 \u2192 2026-06-04 \u2014 each anchor's path, with today's percentile over the whole window. Faint red = crisis eras."), /*#__PURE__*/React.createElement("div", {
    className: "two"
  }, metrics.map((m, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      marginBottom: 18
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontWeight: 600,
      fontSize: ".92rem",
      marginBottom: 8
    }
  }, m.t, " \u2014 ", /*#__PURE__*/React.createElement("span", {
    className: "mono",
    style: {
      fontFamily: "var(--mono)"
    }
  }, m.v), " \xB7 ", m.pct, "th %ile"), /*#__PURE__*/React.createElement(MiniTrend, {
    points: paths[i]
  })))));
}
function MiniTrend({
  points
}) {
  const w = 420,
    h = 140,
    pad = 6;
  const px = i => pad + i / (points.length - 1) * (w - pad * 2),
    py = v => pad + (1 - v) * (h - pad * 2);
  const line = points.map((v, i) => `${i ? "L" : "M"}${px(i).toFixed(1)},${py(v).toFixed(1)}`).join(" ");
  const area = `${line} L${px(points.length - 1)},${h - pad} L${px(0)},${h - pad} Z`;
  const last = points[points.length - 1];
  return /*#__PURE__*/React.createElement("svg", {
    viewBox: `0 0 ${w} ${h}`,
    style: {
      width: "100%",
      height: 140,
      background: "var(--surface)",
      border: "1px solid var(--border)",
      borderRadius: 10
    },
    preserveAspectRatio: "none"
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
    id: "mt" + points[0],
    x1: "0",
    y1: "0",
    x2: "0",
    y2: "1"
  }, /*#__PURE__*/React.createElement("stop", {
    offset: "0",
    stopColor: "var(--accent)",
    stopOpacity: ".10"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: "1",
    stopColor: "var(--accent)",
    stopOpacity: "0"
  }))), /*#__PURE__*/React.createElement("path", {
    d: area,
    fill: `url(#mt${points[0]})`
  }), /*#__PURE__*/React.createElement("path", {
    d: line,
    fill: "none",
    stroke: "var(--accent)",
    strokeWidth: "1.6",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("line", {
    x1: pad,
    x2: w - pad,
    y1: py(last),
    y2: py(last),
    stroke: "var(--down)",
    strokeWidth: "1",
    strokeDasharray: "3 3",
    opacity: ".45"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: px(points.length - 1),
    cy: py(last),
    r: "3.5",
    fill: "var(--down)"
  }));
}
function HeadlinesTab({
  d
}) {
  const [q, setQ] = useState("");
  const items = d.news.filter(n => !q.trim() || (n.t + n.s).toLowerCase().includes(q.toLowerCase()));
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
    htmlFor: "hfilter",
    className: "sr-only"
  }, "Filter headlines"), /*#__PURE__*/React.createElement("input", {
    id: "hfilter",
    className: "field",
    type: "search",
    placeholder: "Filter headlines \u2014 e.g. Fed, oil, NVDA\u2026",
    value: q,
    onChange: e => setQ(e.target.value)
  }), /*#__PURE__*/React.createElement("div", {
    className: "tcap",
    style: {
      marginBottom: 10
    },
    role: "status",
    "aria-live": "polite"
  }, items.length, " ", q.trim() ? `of ${d.news.length} matching “${q.trim()}”` : "headlines across 12 feeds"), items.length === 0 ? /*#__PURE__*/React.createElement("div", {
    className: "empty"
  }, /*#__PURE__*/React.createElement("div", {
    className: "eg",
    "aria-hidden": "true"
  }, "\u2315"), /*#__PURE__*/React.createElement("div", {
    className: "et"
  }, "No headlines match \u201C", q.trim(), "\u201D"), /*#__PURE__*/React.createElement("div", {
    className: "es"
  }, "Try a ticker (NVDA), an asset (oil, gold), or a theme (Fed, credit)."), /*#__PURE__*/React.createElement("button", {
    className: "btn-ghost",
    type: "button",
    onClick: () => setQ("")
  }, "Clear filter")) : /*#__PURE__*/React.createElement("div", {
    className: "news"
  }, items.map((n, i) => /*#__PURE__*/React.createElement("div", {
    className: "newsitem",
    key: i
  }, /*#__PURE__*/React.createElement("div", {
    className: "nt"
  }, n.t), /*#__PURE__*/React.createElement("div", {
    className: "nm"
  }, n.s, " \xB7 ", n.d)))));
}
function CalendarTab({
  d
}) {
  const econ = [{
    name: "May Nonfarm Payrolls",
    date: "2026-06-05",
    in: "tomorrow ⚠️"
  }, {
    name: "CPI (May)",
    date: "2026-06-11",
    in: "7 days"
  }, {
    name: "FOMC decision",
    date: "2026-06-17",
    in: "13 days"
  }, {
    name: "Core PCE (May)",
    date: "2026-06-26",
    in: "22 days"
  }];
  const extremes = d.extremes;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h3", {
    className: "subhead"
  }, "Economic releases \u2014 the data the market trades around"), /*#__PURE__*/React.createElement("table", {
    className: "tbl"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Release"), /*#__PURE__*/React.createElement("th", null, "Date"), /*#__PURE__*/React.createElement("th", null, "In"))), /*#__PURE__*/React.createElement("tbody", null, econ.map((e, i) => /*#__PURE__*/React.createElement("tr", {
    key: i
  }, /*#__PURE__*/React.createElement("td", null, e.name), /*#__PURE__*/React.createElement("td", null, e.date), /*#__PURE__*/React.createElement("td", {
    className: e.in.includes("⚠️") ? "warn" : "neutral"
  }, e.in))))), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("h3", {
    className: "subhead"
  }, "Cross-asset extremes \u2014 where key markets sit in their ~1y range"), /*#__PURE__*/React.createElement("table", {
    className: "tbl"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Anchor"), /*#__PURE__*/React.createElement("th", null, "Last"), /*#__PURE__*/React.createElement("th", null, "1y %ile"), /*#__PURE__*/React.createElement("th", null, "z"))), /*#__PURE__*/React.createElement("tbody", null, extremes.map((e, i) => /*#__PURE__*/React.createElement("tr", {
    key: i
  }, /*#__PURE__*/React.createElement("td", null, e.name), /*#__PURE__*/React.createElement("td", null, e.last), /*#__PURE__*/React.createElement("td", {
    className: "neutral"
  }, e.pct), /*#__PURE__*/React.createElement("td", {
    className: window.TONE[e.t]
  }, e.z))))));
}
Object.assign(window, {
  DataTable,
  Movers,
  BigChart,
  OverviewTab,
  EquitiesTab,
  MacroTab,
  TrendsTab,
  HeadlinesTab,
  CalendarTab
});

/* ============================================================
   story.jsx
   ============================================================ */
/* Market Story dashboard — the Story tab (the written read). */
function StoryTab() {
  const grades = [{
    s: "miss",
    claim: "WTI holds $95 — the oil bid is intact",
    metric: "CL=F",
    trig: "> 95",
    now: "92.44"
  }, {
    s: "watch",
    claim: "HY OAS widens → credit de-risking",
    metric: "BAMLH0A0HYM2",
    trig: "> 2.85",
    now: "2.71"
  }, {
    s: "watch",
    claim: "10Y makes a decisive break above 4.5%",
    metric: "DGS10",
    trig: "> 4.5",
    now: "4.49"
  }, {
    s: "trig",
    claim: "2s10s re-steepens off the 0th %ile",
    metric: "T10Y2Y",
    trig: "> 0.55",
    now: "0.41"
  }];
  const watch = [{
    claim: "AVGO gaps >10% → the AI-capex cluster is a trend, not noise",
    metric: "AVGO:change_pct",
    trig: "< −10",
    h: "today open"
  }, {
    claim: "WTI recovers above $95 = positioning unwind, not demand",
    metric: "CL=F:last",
    trig: "> 95",
    h: "2 sessions"
  }, {
    claim: "HY OAS holds the de-risking line",
    metric: "BAMLH0A0HYM2",
    trig: "> 2.85",
    h: "next week"
  }, {
    claim: "10Y breaks 4.5% post-payroll = more rate pain for tech",
    metric: "DGS10",
    trig: "> 4.5",
    h: "Fri close"
  }, {
    claim: "Gold holds >$4,500 on an oil bounce = geopolitical floor",
    metric: "GC=F:last",
    trig: "> 4500",
    h: "next session"
  }];
  const badge = {
    miss: "MISS",
    watch: "WATCHING",
    hit: "HIT",
    trig: "TRIGGERED"
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "story"
  }, /*#__PURE__*/React.createElement("div", {
    className: "meta-row"
  }, /*#__PURE__*/React.createElement("span", null, "Source: ", /*#__PURE__*/React.createElement("b", null, "narrative_2026-06-04.md")), /*#__PURE__*/React.createElement("span", null, "Session: ", /*#__PURE__*/React.createElement("b", null, "Pre-US open")), /*#__PURE__*/React.createElement("span", null, "Grading prior: ", /*#__PURE__*/React.createElement("b", null, "0 hit \xB7 1 inverted \xB7 2 miss"))), /*#__PURE__*/React.createElement("h2", {
    style: {
      marginTop: 0
    }
  }, "Since last time"), /*#__PURE__*/React.createElement("p", {
    className: "cap",
    style: {
      marginBottom: 4
    }
  }, "Grading yesterday's ", /*#__PURE__*/React.createElement("code", null, "watch"), " block against today's brief \u2014 the read is accountable."), /*#__PURE__*/React.createElement("table", {
    className: "grade-tbl"
  }, /*#__PURE__*/React.createElement("tbody", null, grades.map((g, i) => /*#__PURE__*/React.createElement("tr", {
    key: i
  }, /*#__PURE__*/React.createElement("td", {
    style: {
      width: 96
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "badge " + g.s
  }, badge[g.s])), /*#__PURE__*/React.createElement("td", null, g.claim), /*#__PURE__*/React.createElement("td", {
    className: "gm"
  }, g.metric, " ", g.trig), /*#__PURE__*/React.createElement("td", {
    className: "gnow"
  }, "now ", g.now))))), /*#__PURE__*/React.createElement("h2", null, "Today in one line"), /*#__PURE__*/React.createElement("div", {
    className: "thesis-hero"
  }, /*#__PURE__*/React.createElement("div", {
    className: "te"
  }, "\u25CF The thesis \xB7 with its flip condition"), /*#__PURE__*/React.createElement("div", {
    className: "lead",
    style: {
      margin: 0
    }
  }, "The oil floor broke while gold caught a simultaneous +$55 bid \u2014 that pairing is a demand-concern repricing, not an Iran-risk relief trade; it flips to \u201Cgeopolitical resolved\u201D only if WTI recovers above $95 by the close ", /*#__PURE__*/React.createElement("i", null, "and"), " gold gives back gains.")), /*#__PURE__*/React.createElement("h2", null, "TL;DR"), /*#__PURE__*/React.createElement("ul", null, /*#__PURE__*/React.createElement("li", null, /*#__PURE__*/React.createElement("b", null, "WTI \u22123.2% to $92.44 overnight"), " while gold +1.2% to $4,520 \u2014 if this were Iran de-escalation, gold falls with oil; instead gold bids. ", /*#__PURE__*/React.createElement("i", null, "Consequence:"), " the XLE hedge that saved the tape yesterday is gone."), /*#__PURE__*/React.createElement("li", null, /*#__PURE__*/React.createElement("b", null, "Broadcom faces a historic gap-down at open"), " \u2014 a fifth large-cap AI-infra name joins the cluster (after CRM \u22125.1%, NVDA \u22123.6%, MSFT \u22123.2%, TSMC \u22122.2%). ", /*#__PURE__*/React.createElement("i", null, "Consequence:"), " this has crossed from idiosyncratic to a trend."), /*#__PURE__*/React.createElement("li", null, /*#__PURE__*/React.createElement("b", null, "Blackstone gates its flagship private credit fund"), " amid $4.5bn of Q2 redemptions. ", /*#__PURE__*/React.createElement("i", null, "Consequence:"), " private gates historically precede public spread widening by 2\u20134 weeks.")), /*#__PURE__*/React.createElement("h2", null, "What moved & why"), /*#__PURE__*/React.createElement("h3", null, "Commodities & credit"), /*#__PURE__*/React.createElement("p", null, "The session's dominant cross-asset signal: ", /*#__PURE__*/React.createElement("b", null, "WTI \u2212$3.09 (\u22123.2%) to $92.44; Brent \u2212$2.99 (\u22123.1%) to $94.36."), " The key analytical question is ", /*#__PURE__*/React.createElement("i", null, "why gold rose simultaneously"), " \u2014 gold +$55.30 (+1.24%) to $4,519.70 while DXY fell. This combination is inconsistent with a simple Iran-risk-off. The most likely read: leveraged long-oil positions unwinding, while gold absorbs the \u201CI don't trust this resolution\u201D flow and copper (98th %ile) hasn't caught the memo."), /*#__PURE__*/React.createElement("h3", null, "Equities & sectors"), /*#__PURE__*/React.createElement("p", null, "US equities are stale in this pre-market snapshot; the directional signal comes from the newsflow. Five of the eight most important AI-infra names are now in confirmed downtrend. That is not noise. Yesterday's only offensive winners \u2014 Energy (+1.29%) and Healthcare (+0.79%) \u2014 lose their function as WTI breaks lower."), /*#__PURE__*/React.createElement("h2", null, "Risk lens"), /*#__PURE__*/React.createElement("p", null, "The Broadcom cluster changes the risk calculus. The combined pressure of higher-for-longer rates (10Y at the 96th %ile) ", /*#__PURE__*/React.createElement("i", null, "and"), " capex-cycle deceleration is precisely what consensus didn't price. ", /*#__PURE__*/React.createElement("b", null, "Leveraged funds net short \u2212458k S&P contracts"), " \u2014 the fast money was ahead of this; the squeeze fuel for a soft payroll is still in place."), /*#__PURE__*/React.createElement("p", null, /*#__PURE__*/React.createElement("b", null, "Portfolio hedge map is now worse:"), " (1) duration doesn't work (stock-bond corr +0.76); (2) energy just lost its hedge function; (3) credit too tight to add protection. Cash and possibly gold are the only clean defensive plays."), /*#__PURE__*/React.createElement("h2", null, "What to watch"), /*#__PURE__*/React.createElement("ol", null, /*#__PURE__*/React.createElement("li", null, "Broadcom's actual open print \u2014 does AVGO gap >\u221210%? Watch HY OAS simultaneously."), /*#__PURE__*/React.createElement("li", null, "WTI recovery above $95 \u2014 a bounce = positioning unwind; holds $91\u201393 into payrolls = demand concern."), /*#__PURE__*/React.createElement("li", null, "Friday May payrolls \u2014 the single highest-stakes data point.")), /*#__PURE__*/React.createElement("p", {
    className: "cap",
    style: {
      margin: "14px 0 4px"
    }
  }, "The machine-readable ", /*#__PURE__*/React.createElement("code", null, "watch"), " block \u2014 the next session grades these:"), /*#__PURE__*/React.createElement("div", {
    className: "watch-block"
  }, /*#__PURE__*/React.createElement("table", null, /*#__PURE__*/React.createElement("tbody", null, watch.map((w, i) => /*#__PURE__*/React.createElement("tr", {
    key: i
  }, /*#__PURE__*/React.createElement("td", null, w.claim), /*#__PURE__*/React.createElement("td", {
    className: "wm"
  }, w.metric, " ", w.trig), /*#__PURE__*/React.createElement("td", {
    className: "wh"
  }, w.h)))))), /*#__PURE__*/React.createElement("h2", null, "Sources"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: ".84rem",
      color: "var(--text-dim)"
    }
  }, "Broadcom (Seeking Alpha \xB7 Yahoo Finance) \xB7 Blackstone private credit gate (FT) \xB7 CrowdStrike Q1 (Seeking Alpha) \xB7 asymmetric downside (MarketWatch) \xB7 Meta Business Agent (Nasdaq) \u2014 all 2026-06-03/04."));
}

/* ---- Learn: The investment clock (radial regime map) ---- */
function CycleClock() {
  const cx = 175,
    cy = 175,
    ro = 152,
    ri = 80;
  // quadrants in math angles (CCW from east), y flipped on render
  const quads = [{
    name: "Recovery",
    lead: "Stocks lead",
    sub: "growth ↑ · inflation ↓",
    a0: 90,
    a1: 180,
    color: "#36c26f"
  }, {
    name: "Overheat",
    lead: "Commodities lead",
    sub: "growth ↑ · inflation ↑",
    a0: 0,
    a1: 90,
    color: "#f5a623"
  }, {
    name: "Stagflation",
    lead: "Cash leads",
    sub: "growth ↓ · inflation ↑",
    a0: -90,
    a1: 0,
    color: "#ff5c6c"
  }, {
    name: "Reflation",
    lead: "Bonds lead",
    sub: "growth ↓ · inflation ↓",
    a0: 180,
    a1: 270,
    color: "#7beafb"
  }];
  const pt = (ang, r) => [cx + r * Math.cos(ang * Math.PI / 180), cy - r * Math.sin(ang * Math.PI / 180)];
  const ring = (a0, a1) => {
    const N = 24,
      out = [],
      inn = [];
    for (let i = 0; i <= N; i++) {
      const a = a0 + (a1 - a0) * i / N;
      out.push(pt(a, ro));
    }
    for (let i = N; i >= 0; i--) {
      const a = a0 + (a1 - a0) * i / N;
      inn.push(pt(a, ri));
    }
    return [...out, ...inn].map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" ") + "Z";
  };
  const nowAng = -28; // late Overheat rotating into Stagflation
  const tip = pt(nowAng, ro - 10),
    base = pt(nowAng + 180, ri - 30);
  return /*#__PURE__*/React.createElement("div", {
    className: "chart",
    style: {
      display: "flex",
      gap: 28,
      flexWrap: "wrap",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 350 350",
    style: {
      width: 300,
      height: 300,
      flex: "0 0 auto"
    }
  }, quads.map((q, i) => {
    const mid = (q.a0 + q.a1) / 2,
      lp = pt(mid, (ro + ri) / 2);
    return /*#__PURE__*/React.createElement("g", {
      key: i
    }, /*#__PURE__*/React.createElement("path", {
      d: ring(q.a0, q.a1),
      fill: q.color,
      fillOpacity: "0.13",
      stroke: q.color,
      strokeOpacity: "0.4",
      strokeWidth: "1"
    }), /*#__PURE__*/React.createElement("text", {
      x: lp[0],
      y: lp[1] - 8,
      textAnchor: "middle",
      fontFamily: "var(--grot)",
      fontWeight: "600",
      fontSize: "13",
      fill: q.color
    }, q.name), /*#__PURE__*/React.createElement("text", {
      x: lp[0],
      y: lp[1] + 9,
      textAnchor: "middle",
      fontFamily: "var(--mono)",
      fontSize: "9.5",
      fill: "var(--text-dim)"
    }, q.lead));
  }), /*#__PURE__*/React.createElement("line", {
    x1: cx,
    y1: cy - ro,
    x2: cx,
    y2: cy + ro,
    stroke: "var(--grid)",
    strokeWidth: "1"
  }), /*#__PURE__*/React.createElement("line", {
    x1: cx - ro,
    y1: cy,
    x2: cx + ro,
    y2: cy,
    stroke: "var(--grid)",
    strokeWidth: "1"
  }), /*#__PURE__*/React.createElement("text", {
    x: cx + 4,
    y: cy - ro + 2,
    fontFamily: "var(--mono)",
    fontSize: "9",
    fill: "var(--text-dim)"
  }, "GROWTH \u2191"), /*#__PURE__*/React.createElement("text", {
    x: cx + ro - 2,
    y: cy - 6,
    textAnchor: "end",
    fontFamily: "var(--mono)",
    fontSize: "9",
    fill: "var(--text-dim)"
  }, "INFLATION \u2192"), /*#__PURE__*/React.createElement("line", {
    x1: base[0],
    y1: base[1],
    x2: tip[0],
    y2: tip[1],
    stroke: "var(--text)",
    strokeWidth: "2.5",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: cx,
    cy: cy,
    r: "6",
    fill: "var(--text)"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: tip[0],
    cy: tip[1],
    r: "5",
    fill: "var(--text)"
  }), /*#__PURE__*/React.createElement("text", {
    x: tip[0] + 6,
    y: tip[1] + 14,
    fontFamily: "var(--mono)",
    fontSize: "10",
    fill: "var(--text)"
  }, "NOW")), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 240
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "ct"
  }, "The investment clock \xB7 where the cycle leads capital"), /*#__PURE__*/React.createElement("p", {
    className: "cap",
    style: {
      margin: "8px 0 0"
    }
  }, "Two axes \u2014 growth and inflation \u2014 carve the cycle into four regimes, each favoring a different asset. Today the needle sits in ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: "var(--warn)"
    }
  }, "late Overheat"), " rotating toward ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: "var(--down)"
    }
  }, "Stagflation"), ": oil breaking on demand fear (growth turning down) while gold bids (inflation/debasement hedge still on). That rotation is why the read favors cash and gold over cyclicals.")));
}

/* ---- Learn: Anatomy of a yield (decomposition bar) ---- */
function YieldStack() {
  const scaleMax = 5;
  const parts = [{
    label: "Real yield",
    note: "10Y TIPS",
    val: 2.11,
    color: "#7beafb"
  }, {
    label: "Breakeven inflation",
    note: "expected CPI + risk prem.",
    val: 2.38,
    color: "#f5a623"
  }];
  const total = parts.reduce((s, p) => s + p.val, 0);
  return /*#__PURE__*/React.createElement("div", {
    className: "chart"
  }, /*#__PURE__*/React.createElement("div", {
    className: "ct"
  }, "Anatomy of a yield \xB7 the 10Y, taken apart"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      height: 46,
      borderRadius: 8,
      overflow: "hidden",
      marginTop: 14,
      border: "1px solid var(--border)"
    }
  }, parts.map((p, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    title: `${p.label} ${p.val}%`,
    style: {
      width: `${p.val / scaleMax * 100}%`,
      background: p.color,
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--mono)",
      fontSize: ".82rem",
      color: "rgba(13,12,12,.85)",
      fontWeight: 600
    }
  }, p.val.toFixed(2), "%"))), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      background: "var(--surface-2)",
      display: "flex",
      alignItems: "center",
      paddingLeft: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--mono)",
      fontSize: ".72rem",
      color: "var(--text-dim)"
    }
  }, "head-room to 5%"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 20,
      flexWrap: "wrap",
      marginTop: 12
    }
  }, parts.map((p, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      display: "flex",
      gap: 8,
      alignItems: "baseline"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 10,
      height: 10,
      borderRadius: 2,
      background: p.color,
      alignSelf: "center"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--grot)",
      fontWeight: 600,
      fontSize: ".82rem",
      color: "var(--text)"
    }
  }, p.label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--mono)",
      fontSize: ".72rem",
      color: "var(--text-dim)"
    }
  }, p.note))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: "auto",
      fontFamily: "var(--mono)",
      fontSize: ".82rem",
      color: "var(--text)"
    }
  }, "= ", total.toFixed(2), "% nominal")), /*#__PURE__*/React.createElement("p", {
    className: "cap",
    style: {
      margin: "12px 0 0"
    }
  }, "A nominal yield is just ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: "var(--text)"
    }
  }, "real rate + expected inflation"), ". When the 10Y rises, ask ", /*#__PURE__*/React.createElement("i", null, "which piece moved"), ": a real-rate jump tightens financial conditions (bad for equities); a breakeven jump is an inflation-scare. Today's 4.49% is mostly real \u2014 a higher-for-longer story, not a runaway-inflation one."));
}

/* ---- Learn: Who owns the US stock market (composition bar) ---- */
function OwnersBar() {
  const owners = [{
    name: "Households (direct)",
    pct: 38,
    color: "#7beafb"
  }, {
    name: "Mutual funds",
    pct: 20,
    color: "#6fb6c9"
  }, {
    name: "Foreign investors",
    pct: 17,
    color: "#5aa0a8"
  }, {
    name: "Retirement & pensions",
    pct: 14,
    color: "#cf9f5a"
  }, {
    name: "ETFs",
    pct: 7,
    color: "#f5a623"
  }, {
    name: "Hedge funds & other",
    pct: 4,
    color: "#b3aaa0"
  }];
  return /*#__PURE__*/React.createElement("div", {
    className: "chart"
  }, /*#__PURE__*/React.createElement("div", {
    className: "ct"
  }, "Who owns the US stock market"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      height: 38,
      borderRadius: 8,
      overflow: "hidden",
      marginTop: 14,
      border: "1px solid var(--border)"
    }
  }, owners.map((o, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    title: `${o.name} ~${o.pct}%`,
    style: {
      width: `${o.pct}%`,
      background: o.color,
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    }
  }, o.pct >= 9 && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--mono)",
      fontSize: ".72rem",
      color: "rgba(13,12,12,.8)",
      fontWeight: 600
    }
  }, o.pct, "%")))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
      gap: "6px 16px",
      marginTop: 12
    }
  }, owners.map((o, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      display: "flex",
      gap: 8,
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 10,
      height: 10,
      borderRadius: 2,
      background: o.color
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--grot)",
      fontSize: ".78rem",
      color: "var(--text)"
    }
  }, o.name), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--mono)",
      fontSize: ".72rem",
      color: "var(--text-dim)",
      marginLeft: "auto"
    }
  }, o.pct, "%")))), /*#__PURE__*/React.createElement("p", {
    className: "cap",
    style: {
      margin: "12px 0 0"
    }
  }, "Households still hold the plurality directly \u2014 which is why a sharp drawdown is a ", /*#__PURE__*/React.createElement("i", null, "consumer-confidence"), " event, not just a Wall Street one. Foreign ownership (~17%) is the channel a dollar crisis would transmit through. ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--text-dim)"
    }
  }, "Approximate, Fed Financial Accounts style.")));
}
function LearnPage() {
  const events = [{
    y: "1792",
    t: "Buttonwood Agreement",
    c: "cat-founding"
  }, {
    y: "1929",
    t: "Wall Street Crash",
    c: "cat-crash"
  }, {
    y: "1933",
    t: "Glass–Steagall",
    c: "cat-reform"
  }, {
    y: "1971",
    t: "Nixon ends gold standard",
    c: "cat-reform"
  }, {
    y: "1987",
    t: "Black Monday",
    c: "cat-crash"
  }, {
    y: "2008",
    t: "Global Financial Crisis",
    c: "cat-crash"
  }, {
    y: "2010",
    t: "Dodd–Frank",
    c: "cat-reform"
  }, {
    y: "2020",
    t: "COVID crash & recovery",
    c: "cat-crash"
  }];
  const cat = {
    "cat-founding": "#7beafb",
    "cat-crash": "#ef5350",
    "cat-reform": "#26a69a",
    "cat-innovation": "#ab47bc",
    "cat-boom": "#ffa726"
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "main"
  }, /*#__PURE__*/React.createElement("div", {
    className: "hd"
  }, /*#__PURE__*/React.createElement("h1", null, "\uD83D\uDCDA Learn the Markets")), /*#__PURE__*/React.createElement("div", {
    className: "tcap",
    style: {
      marginTop: 6
    }
  }, "Foundations for a risk analyst \u2014 researched and fact-checked."), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("h2", {
    className: "h2"
  }, "Market history \xB7 1792 \u2192 today"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 0,
      alignItems: "center",
      margin: "24px 0",
      position: "relative",
      borderTop: "1px solid var(--border)",
      paddingTop: 30
    }
  }, events.map((e, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      flex: 1,
      textAlign: "center",
      position: "relative"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 14,
      height: 14,
      borderRadius: "50%",
      background: cat[e.c],
      margin: "0 auto 10px"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--mono)",
      fontSize: ".74rem",
      color: "var(--text)"
    }
  }, e.y), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: ".68rem",
      color: "var(--text-dim)",
      marginTop: 3,
      padding: "0 4px"
    }
  }, e.t)))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 16,
      flexWrap: "wrap",
      marginTop: 8
    }
  }, Object.entries({
    Founding: "#7beafb",
    Crash: "#ef5350",
    Reform: "#26a69a",
    Innovation: "#ab47bc",
    Boom: "#ffa726"
  }).map(([k, v]) => /*#__PURE__*/React.createElement("span", {
    key: k,
    style: {
      display: "flex",
      alignItems: "center",
      gap: 7,
      fontSize: ".74rem",
      color: "var(--text-dim)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 10,
      height: 10,
      borderRadius: "50%",
      background: v
    }
  }), k))), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("h2", {
    className: "h2"
  }, "The cycle & what leads it"), /*#__PURE__*/React.createElement(CycleClock, null), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("h2", {
    className: "h2"
  }, "Rates, taken apart"), /*#__PURE__*/React.createElement(YieldStack, null), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("h2", {
    className: "h2"
  }, "The players"), /*#__PURE__*/React.createElement(OwnersBar, null), /*#__PURE__*/React.createElement("hr", {
    className: "hr"
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      color: "var(--text)",
      maxWidth: 680
    }
  }, "A market is a venue where buyers and sellers discover a price. The Learn page pairs researched prose with diagrams that reveal ", /*#__PURE__*/React.createElement("i", null, "how the system is wired"), " \u2014 capital flows, policy transmission, the cycle, and what sits inside a number."), /*#__PURE__*/React.createElement("h2", {
    className: "h2",
    style: {
      marginTop: 28
    }
  }, "How money moves through the system"), /*#__PURE__*/React.createElement(Sankey, {
    data: {
      title: "Savings → intermediaries → markets",
      nodes: [{
        id: "hh",
        label: "Households",
        layer: 0
      }, {
        id: "pen",
        label: "Pensions & insurers",
        layer: 0
      }, {
        id: "fgn",
        label: "Foreign official",
        layer: 0
      }, {
        id: "bank",
        label: "Banks",
        layer: 1
      }, {
        id: "am",
        label: "Asset managers",
        layer: 1
      }, {
        id: "dlr",
        label: "Dealers",
        layer: 1
      }, {
        id: "eq",
        label: "Equities",
        layer: 2
      }, {
        id: "ust",
        label: "Treasuries",
        layer: 2
      }, {
        id: "cr",
        label: "Credit",
        layer: 2
      }, {
        id: "csh",
        label: "Cash & bills",
        layer: 2
      }],
      links: [{
        source: "hh",
        target: "bank",
        value: 30
      }, {
        source: "hh",
        target: "am",
        value: 42
      }, {
        source: "pen",
        target: "am",
        value: 48
      }, {
        source: "pen",
        target: "dlr",
        value: 14
      }, {
        source: "fgn",
        target: "dlr",
        value: 22
      }, {
        source: "fgn",
        target: "bank",
        value: 10
      }, {
        source: "bank",
        target: "cr",
        value: 18
      }, {
        source: "bank",
        target: "csh",
        value: 22
      }, {
        source: "am",
        target: "eq",
        value: 52
      }, {
        source: "am",
        target: "ust",
        value: 24
      }, {
        source: "am",
        target: "cr",
        value: 14
      }, {
        source: "dlr",
        target: "ust",
        value: 26
      }, {
        source: "dlr",
        target: "eq",
        value: 10
      }]
    }
  }), /*#__PURE__*/React.createElement("h2", {
    className: "h2",
    style: {
      marginTop: 28
    }
  }, "How a Fed rate decision reaches the economy"), /*#__PURE__*/React.createElement(Sankey, {
    height: 400,
    data: {
      title: "Policy transmission · rate → channels → real economy",
      nodes: [{
        id: "ff",
        label: "Fed funds rate",
        layer: 0
      }, {
        id: "bk",
        label: "Bank lending rates",
        layer: 1
      }, {
        id: "by",
        label: "Bond yields",
        layer: 1
      }, {
        id: "ap",
        label: "Asset prices",
        layer: 1
      }, {
        id: "fx",
        label: "US dollar",
        layer: 1
      }, {
        id: "ex",
        label: "Expectations",
        layer: 1
      }, {
        id: "inv",
        label: "Investment",
        layer: 2
      }, {
        id: "con",
        label: "Consumption",
        layer: 2
      }, {
        id: "nx",
        label: "Net exports",
        layer: 2
      }, {
        id: "emp",
        label: "Employment",
        layer: 2
      }, {
        id: "inf",
        label: "Inflation",
        layer: 2
      }],
      links: [{
        source: "ff",
        target: "bk",
        value: 30
      }, {
        source: "ff",
        target: "by",
        value: 26
      }, {
        source: "ff",
        target: "ap",
        value: 20
      }, {
        source: "ff",
        target: "fx",
        value: 14
      }, {
        source: "ff",
        target: "ex",
        value: 18
      }, {
        source: "bk",
        target: "inv",
        value: 16
      }, {
        source: "bk",
        target: "con",
        value: 14
      }, {
        source: "by",
        target: "inv",
        value: 14
      }, {
        source: "by",
        target: "ap",
        value: 8
      }, {
        source: "ap",
        target: "con",
        value: 16
      }, {
        source: "ap",
        target: "inv",
        value: 8
      }, {
        source: "fx",
        target: "nx",
        value: 14
      }, {
        source: "ex",
        target: "inf",
        value: 12
      }, {
        source: "ex",
        target: "con",
        value: 6
      }, {
        source: "inv",
        target: "emp",
        value: 24
      }, {
        source: "con",
        target: "emp",
        value: 22
      }, {
        source: "nx",
        target: "emp",
        value: 10
      }, {
        source: "emp",
        target: "inf",
        value: 18
      }]
    }
  }), /*#__PURE__*/React.createElement("p", {
    className: "cap",
    style: {
      margin: "12px 0 0",
      maxWidth: 680
    }
  }, "The lags are long and variable \u2014 a hike takes ~12\u201318 months to fully reach employment and inflation. That's why the brief watches the ", /*#__PURE__*/React.createElement("i", null, "channels"), " (yields, the dollar, asset prices) for early signal rather than waiting on the lagging real-economy data."));
}
Object.assign(window, {
  StoryTab,
  LearnPage
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/app.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/data.js
try { (() => {
/* Market Story — sample brief data (mirrors the brief JSON contract; values
   lifted from the repo's narrative_2026-06-04.md for authenticity). Static. */
window.MS_DATA = {
  date: "2026-06-04",
  session_label: "Pre-US open",
  generated_at: "12:26",
  stats: {
    sector_advancers: 4,
    sector_decliners: 7,
    sector_count: 11
  },
  // KPI strip — symbol, label, value, delta, kind, sparkline points (0..1 normalized path)
  kpis: [{
    sym: "^GSPC",
    label: "S&P 500",
    val: "7,553.68",
    delta: "+0.18%",
    tone: "up",
    spark: [.2, .35, .3, .5, .45, .62, .58, .7, .66, .8],
    sparkUp: true
  }, {
    sym: "^IXIC",
    label: "Nasdaq",
    val: "26,853.98",
    delta: "−0.42%",
    tone: "down",
    spark: [.7, .62, .66, .5, .55, .4, .45, .32, .36, .28],
    sparkUp: false
  }, {
    sym: "^TNX",
    label: "10Y Treasury",
    val: "4.491%",
    delta: "+1 bps",
    tone: "down",
    spark: [.3, .34, .4, .42, .5, .55, .6, .64, .7, .72],
    sparkUp: true
  }, {
    sym: "DX-Y.NYB",
    label: "US Dollar",
    val: "99.24",
    delta: "−0.31%",
    tone: "down",
    spark: [.7, .66, .6, .62, .55, .5, .46, .4, .38, .34],
    sparkUp: false
  }, {
    sym: "GC=F",
    label: "Gold",
    val: "4,519.70",
    delta: "+1.24%",
    tone: "up",
    spark: [.3, .28, .34, .4, .45, .55, .6, .7, .78, .86],
    sparkUp: true
  }, {
    sym: "^VIX",
    label: "VIX",
    val: "16.5",
    delta: "+2.8%",
    tone: "down",
    spark: [.4, .42, .38, .45, .5, .48, .55, .6, .58, .64],
    sparkUp: false,
    invert: true
  }],
  read: "The oil floor broke while gold caught a simultaneous +$55 bid — that pairing is a demand-concern repricing, not an Iran-risk relief trade; it flips to \u201Cgeopolitical resolved\u201D only if WTI recovers above $95 by the close AND gold gives back gains.",
  signals: [{
    tone: "down",
    text: "WTI \u2212$3.09 (\u22123.2%) to $92.44 \u2014 the energy hedge that saved the tape is gone."
  }, {
    tone: "warn",
    text: "Blackstone gates its flagship private credit fund amid $4.5bn of Q2 redemptions."
  }, {
    tone: "down",
    text: "Broadcom faces a historic gap-down \u2014 a fifth AI-infra name joins the cluster."
  }, {
    tone: "up",
    text: "Gold +1.24% to $4,519.70 \u2014 the safe-haven bid is absorbing the distrust flow."
  }],
  leaders: [{
    name: "Energy (XLE)",
    chg: "+1.29%",
    tone: "up"
  }, {
    name: "Healthcare (XLV)",
    chg: "+0.79%",
    tone: "up"
  }, {
    name: "Staples (XLP)",
    chg: "+0.40%",
    tone: "up"
  }, {
    name: "Meta (META)",
    chg: "+4.20%",
    tone: "up"
  }],
  laggards: [{
    name: "Salesforce (CRM)",
    chg: "−5.10%",
    tone: "down"
  }, {
    name: "Nvidia (NVDA)",
    chg: "−3.60%",
    tone: "down"
  }, {
    name: "Microsoft (MSFT)",
    chg: "−3.20%",
    tone: "down"
  }, {
    name: "TSMC",
    chg: "−2.20%",
    tone: "down"
  }],
  sectors: [{
    name: "Energy",
    chg: 1.29
  }, {
    name: "Health",
    chg: 0.79
  }, {
    name: "Staples",
    chg: 0.40
  }, {
    name: "Utilities",
    chg: 0.12
  }, {
    name: "Materials",
    chg: -0.34
  }, {
    name: "Financials",
    chg: -0.58
  }, {
    name: "Industrials",
    chg: -0.71
  }, {
    name: "Real Estate",
    chg: -0.88
  }, {
    name: "Comm Svcs",
    chg: -1.15
  }, {
    name: "Discretionary",
    chg: -1.84
  }, {
    name: "Technology",
    chg: -2.42
  }],
  us_equities: [{
    name: "S&P 500",
    last: "7,553.68",
    d1: "+0.18",
    w1: "−1.42",
    ytd: "+12.30",
    t1: "up",
    tw: "down",
    ty: "up"
  }, {
    name: "Nasdaq 100",
    last: "26,853.98",
    d1: "−0.42",
    w1: "−2.81",
    ytd: "+18.40",
    t1: "down",
    tw: "down",
    ty: "up"
  }, {
    name: "Dow Jones",
    last: "43,118.20",
    d1: "+0.21",
    w1: "−0.55",
    ytd: "+6.10",
    t1: "up",
    tw: "down",
    ty: "up"
  }, {
    name: "Russell 2000",
    last: "2,284.50",
    d1: "−0.66",
    w1: "−1.90",
    ytd: "+2.70",
    t1: "down",
    tw: "down",
    ty: "up"
  }, {
    name: "VIX",
    last: "16.50",
    d1: "+2.80",
    w1: "+8.10",
    ytd: "−12.40",
    t1: "down",
    tw: "down",
    ty: "up"
  }],
  global_indices: [{
    name: "Euro Stoxx 50",
    last: "5,412.10",
    d1: "+0.34",
    w1: "+0.90",
    ytd: "+9.80",
    t1: "up",
    tw: "up",
    ty: "up"
  }, {
    name: "FTSE 100",
    last: "8,640.30",
    d1: "+0.12",
    w1: "+0.41",
    ytd: "+5.20",
    t1: "up",
    tw: "up",
    ty: "up"
  }, {
    name: "DAX",
    last: "19,820.40",
    d1: "+0.28",
    w1: "+1.10",
    ytd: "+11.40",
    t1: "up",
    tw: "up",
    ty: "up"
  }, {
    name: "Nikkei 225",
    last: "39,104.00",
    d1: "−1.36",
    w1: "−2.20",
    ytd: "+3.90",
    t1: "down",
    tw: "down",
    ty: "up"
  }, {
    name: "Hang Seng",
    last: "18,442.10",
    d1: "−1.48",
    w1: "−2.95",
    ytd: "−1.10",
    t1: "down",
    tw: "down",
    ty: "down"
  }],
  rates: [{
    name: "13-week",
    last: "4.310",
    d1: "+0.5",
    w1: "−1.20",
    ytd: "−8.40",
    t1: "down",
    tw: "up",
    ty: "up"
  }, {
    name: "5-year",
    last: "4.214",
    d1: "−0.8",
    w1: "+2.10",
    ytd: "+4.30",
    t1: "up",
    tw: "down",
    ty: "down"
  }, {
    name: "10-year",
    last: "4.491",
    d1: "+1.0",
    w1: "+3.40",
    ytd: "+6.10",
    t1: "down",
    tw: "down",
    ty: "down"
  }, {
    name: "30-year",
    last: "4.990",
    d1: "+1.4",
    w1: "+4.20",
    ytd: "+7.80",
    t1: "down",
    tw: "down",
    ty: "down"
  }],
  fx: [{
    name: "EUR/USD",
    last: "1.0842",
    d1: "+0.31",
    w1: "+0.60",
    ytd: "+1.20",
    t1: "up",
    tw: "up",
    ty: "up"
  }, {
    name: "USD/JPY",
    last: "152.40",
    d1: "−0.22",
    w1: "−0.80",
    ytd: "+3.40",
    t1: "down",
    tw: "down",
    ty: "up"
  }, {
    name: "GBP/USD",
    last: "1.2731",
    d1: "+0.18",
    w1: "+0.40",
    ytd: "+0.90",
    t1: "up",
    tw: "up",
    ty: "up"
  }, {
    name: "DXY",
    last: "99.24",
    d1: "−0.31",
    w1: "−0.70",
    ytd: "−2.10",
    t1: "down",
    tw: "down",
    ty: "down"
  }],
  commodities: [{
    name: "WTI crude",
    last: "92.44",
    d1: "−3.20",
    w1: "−5.10",
    ytd: "+14.20",
    t1: "down",
    tw: "down",
    ty: "up"
  }, {
    name: "Brent crude",
    last: "94.36",
    d1: "−3.10",
    w1: "−4.80",
    ytd: "+13.10",
    t1: "down",
    tw: "down",
    ty: "up"
  }, {
    name: "Gold",
    last: "4,519.70",
    d1: "+1.24",
    w1: "+2.40",
    ytd: "+22.60",
    t1: "up",
    tw: "up",
    ty: "up"
  }, {
    name: "Silver",
    last: "38.40",
    d1: "+0.90",
    w1: "+1.80",
    ytd: "+19.30",
    t1: "up",
    tw: "up",
    ty: "up"
  }, {
    name: "Copper",
    last: "6.52",
    d1: "+0.62",
    w1: "+1.10",
    ytd: "+8.90",
    t1: "up",
    tw: "up",
    ty: "up"
  }],
  credit: [{
    name: "HYG (HY ETF)",
    last: "79.68",
    d1: "+0.02",
    w1: "−0.10",
    ytd: "+1.40",
    t1: "up",
    tw: "down",
    ty: "up"
  }, {
    name: "LQD (IG ETF)",
    last: "108.90",
    d1: "−0.08",
    w1: "−0.30",
    ytd: "+0.80",
    t1: "down",
    tw: "down",
    ty: "up"
  }, {
    name: "TLT (20Y+)",
    last: "88.20",
    d1: "−0.34",
    w1: "−1.20",
    ytd: "−3.40",
    t1: "down",
    tw: "down",
    ty: "down"
  }],
  macro: [{
    name: "10Y Treasury",
    latest: "4.49",
    chg: "+0.01",
    pct: "96",
    t: "down"
  }, {
    name: "2s10s curve",
    latest: "0.41",
    chg: "−0.02",
    pct: "0",
    t: "down"
  }, {
    name: "HY OAS",
    latest: "2.71",
    chg: "0.00",
    pct: "3",
    t: "neutral"
  }, {
    name: "IG OAS",
    latest: "0.74",
    chg: "+0.01",
    pct: "3",
    t: "down"
  }, {
    name: "10Y breakeven",
    latest: "2.38",
    chg: "0.00",
    pct: "71",
    t: "neutral"
  }, {
    name: "NFCI",
    latest: "−0.49",
    chg: "+0.01",
    pct: "29",
    t: "down"
  }],
  extremes: [{
    name: "Copper",
    last: "6.52",
    pct: "98",
    z: "+1.91",
    t: "up"
  }, {
    name: "10Y yield",
    last: "4.49",
    pct: "96",
    z: "+1.74",
    t: "down"
  }, {
    name: "HYG",
    last: "79.68",
    pct: "95",
    z: "+1.62",
    t: "up"
  }, {
    name: "WTI",
    last: "92.44",
    pct: "81",
    z: "+0.88",
    t: "down"
  }, {
    name: "DXY",
    last: "99.24",
    pct: "80",
    z: "+0.81",
    t: "down"
  }],
  regime: [{
    label: "Credit",
    val: "risk-on",
    t: "up"
  }, {
    label: "Curve",
    val: "flat / late",
    t: "down"
  }, {
    label: "Vol",
    val: "compressed",
    t: "up"
  }, {
    label: "Breadth",
    val: "risk-off",
    t: "down"
  }, {
    label: "Hedge (stock-bond)",
    val: "broken +0.76",
    t: "down"
  }],
  news: [{
    t: "Broadcom could be headed for one of the worst 1-day destructions in shareholder value ever",
    s: "Yahoo Finance",
    d: "2026-06-04 11:40"
  }, {
    t: "Broadcom tumbles on guidance, but Wall Street sees bright outlook",
    s: "Seeking Alpha",
    d: "2026-06-04 10:12"
  }, {
    t: "Blackstone caps withdrawals from flagship private credit fund as Q2 redemptions surge to $4.5bn",
    s: "FT",
    d: "2026-06-04 09:05"
  }, {
    t: "CrowdStrike falls after Q1 results; analysts bullish but flag high ARR expectations",
    s: "Seeking Alpha",
    d: "2026-06-04 08:50"
  }, {
    t: "How single-stock turbulence presents 'asymmetric' downside risk for a calm S&P 500",
    s: "MarketWatch",
    d: "2026-06-03 18:30"
  }, {
    t: "Why Meta Platforms stock crushed the market today — Business Agent launch",
    s: "Nasdaq",
    d: "2026-06-03 16:20"
  }, {
    t: "Stocks making the biggest moves after hours: Broadcom, CrowdStrike, PVH & more",
    s: "CNBC",
    d: "2026-06-03 16:05"
  }, {
    t: "Trump administration turns to a new rationale to justify old tariffs",
    s: "NYT",
    d: "2026-06-03 14:10"
  }]
};
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/data.js", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/field.js
try { (() => {
/* Market Story — reusable market-field canvas engine.
   Draws today's (synthetic) index paths with a cursor-reactive parallax drift.
   Used prominently on the cover, and faintly as an ambient layer behind the
   dashboard. window.startMarketField(canvas, opts) -> { destroy() }. */
window.startMarketField = function (canvas, opts) {
  opts = opts || {};
  let accentRGB = opts.accentRGB || "123,234,251"; // cyan (mutable via setAccent)
  let faintRGB = opts.faintRGB || "179,170,160"; // warm grey (mutable via setFaint)
  const topFrac = opts.topFrac != null ? opts.topFrac : 0.5;
  const botFrac = opts.botFrac != null ? opts.botFrac : 0.13;
  const lineScale = opts.lineScale || 1;
  const parallax = opts.parallax != null ? opts.parallax : 44;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // intensity: 'off' | 'low' | 'high' (or a numeric base alpha). Maps to an alpha multiplier.
  const ALPHA = {
    off: 0,
    low: 0.42,
    high: 0.85
  };
  let baseAlpha = opts.alpha != null ? opts.alpha : 1;
  let intensity = opts.intensity || null;
  function effAlpha() {
    return intensity != null ? ALPHA[intensity] != null ? ALPHA[intensity] : baseAlpha : baseAlpha;
  }
  const ctx = canvas.getContext("2d");
  let W,
    H,
    raf,
    prog = 1; // fully drawn from first paint (never a blank hero); parallax stays live
  let mx = 0.5,
    my = 0.5,
    tmx = 0.5,
    tmy = 0.5; // eased vs target cursor

  function walk(n, drift, vol, seed) {
    let v = 0,
      out = [],
      s = seed;
    const rnd = () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
    for (let i = 0; i < n; i++) {
      v += drift + (rnd() - 0.5) * vol;
      out.push(v);
    }
    return out;
  }
  const SET = [{
    accent: true,
    d: 0.9,
    v: 2.2,
    seed: 7
  }, {
    accent: false,
    d: 0.7,
    v: 3.0,
    seed: 13
  }, {
    accent: false,
    d: 0.4,
    v: 3.4,
    seed: 21
  }, {
    accent: false,
    d: 0.6,
    v: 2.8,
    seed: 34
  }, {
    accent: false,
    d: -0.2,
    v: 3.6,
    seed: 55
  }, {
    accent: false,
    d: 0.3,
    v: 4.0,
    seed: 89
  }, {
    accent: false,
    d: 0.5,
    v: 2.6,
    seed: 144
  }];
  const lines = SET.map((c, i) => {
    const arr = walk(90, c.d, c.v, c.seed);
    const mn = Math.min(...arr),
      mx2 = Math.max(...arr),
      rng = mx2 - mn || 1;
    return {
      accent: c.accent,
      depth: c.accent ? 1 : 0.25 + i / SET.length * 0.6,
      y: arr.map(x => 1 - (x - mn) / rng)
    };
  }).sort((a, b) => a.accent - b.accent); // accent line drawn last, on top

  function resize() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = canvas.width = Math.max(1, canvas.clientWidth) * dpr;
    H = canvas.height = Math.max(1, canvas.clientHeight) * dpr;
  }
  function onMove(e) {
    tmx = e.clientX / innerWidth;
    tmy = e.clientY / innerHeight;
  }
  function frame() {
    const alpha = effAlpha();
    const dpr = Math.min(devicePixelRatio || 1, 2);
    // self-heal: if the canvas box changed (or wasn't laid out at init), re-fit the buffer
    if (canvas.clientWidth * dpr !== W || canvas.clientHeight * dpr !== H) resize();
    if (alpha <= 0.001) {
      ctx.clearRect(0, 0, W, H);
      raf = requestAnimationFrame(frame);
      return;
    }
    if (!reduce) {
      mx += (tmx - mx) * 0.06;
      my += (tmy - my) * 0.06;
    } else {
      mx = 0.5;
      my = 0.5;
    }
    ctx.clearRect(0, 0, W, H);
    const top = H * topFrac,
      bot = H * botFrac,
      band = H - top - bot;
    const par = reduce ? 0 : parallax;
    for (const ln of lines) {
      const N = ln.y.length,
        n = Math.max(2, Math.floor(N * prog));
      const sx = (mx - 0.5) * par * ln.depth * dpr;
      const sy = (my - 0.5) * par * 0.55 * ln.depth * dpr;
      const px = i => i / (N - 1) * W + sx;
      const py = i => top + ln.y[i] * band + sy;
      if (ln.accent) {
        ctx.beginPath();
        ctx.moveTo(px(0), py(0));
        for (let i = 1; i < n; i++) ctx.lineTo(px(i), py(i));
        ctx.lineTo(px(n - 1), top + band + sy);
        ctx.lineTo(px(0), top + band + sy);
        ctx.closePath();
        const g = ctx.createLinearGradient(0, top, 0, top + band);
        g.addColorStop(0, `rgba(${accentRGB},${0.17 * alpha})`);
        g.addColorStop(1, `rgba(${accentRGB},0)`);
        ctx.fillStyle = g;
        ctx.fill();
      }
      ctx.beginPath();
      ctx.moveTo(px(0), py(0));
      for (let i = 1; i < n; i++) ctx.lineTo(px(i), py(i));
      ctx.strokeStyle = ln.accent ? `rgba(${accentRGB},${0.95 * alpha})` : `rgba(${faintRGB},${0.16 * alpha})`;
      ctx.lineWidth = (ln.accent ? 2.4 : 1.0) * lineScale * dpr;
      ctx.stroke();
      if (prog >= 1 && ln.accent) {
        const x = px(n - 1),
          y = py(n - 1);
        ctx.fillStyle = `rgba(${accentRGB},${alpha})`;
        ctx.beginPath();
        ctx.arc(x, y, 4 * dpr, 0, 7);
        ctx.fill();
        ctx.strokeStyle = `rgba(${accentRGB},${0.35 * alpha})`;
        ctx.lineWidth = 1 * dpr;
        ctx.beginPath();
        ctx.arc(x, y, 9 * dpr, 0, 7);
        ctx.stroke();
      }
    }
    raf = requestAnimationFrame(frame);
  }
  resize();
  addEventListener("resize", resize);
  addEventListener("mousemove", onMove);
  frame();
  return {
    setIntensity(v) {
      intensity = v;
    },
    setAccent(rgb) {
      if (rgb) accentRGB = rgb;
    },
    setFaint(rgb) {
      if (rgb) faintRGB = rgb;
    },
    destroy() {
      cancelAnimationFrame(raf);
      removeEventListener("resize", resize);
      removeEventListener("mousemove", onMove);
    }
  };
};
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/field.js", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/tweaks-panel.jsx
try { (() => {
// @ds-adherence-ignore -- omelette starter scaffold (raw elements/hex/px by design)

/* BEGIN USAGE */
// tweaks-panel.jsx
// Reusable Tweaks shell + form-control helpers.
// Exports (to window): useTweaks, TweaksPanel, TweakSection, TweakRow, TweakSlider,
//   TweakToggle, TweakRadio, TweakSelect, TweakText, TweakNumber, TweakColor, TweakButton.
//
// Owns the host protocol (listens for __activate_edit_mode / __deactivate_edit_mode,
// posts __edit_mode_available / __edit_mode_set_keys / __edit_mode_dismissed) so
// individual prototypes don't re-roll it. Ships a consistent set of controls so you
// don't hand-draw <input type="range">, segmented radios, steppers, etc.
//
// Usage (in an HTML file that loads React + Babel):
//
//   const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
//     "primaryColor": "#D97757",
//     "palette": ["#D97757", "#29261b", "#f6f4ef"],
//     "fontSize": 16,
//     "density": "regular",
//     "dark": false
//   }/*EDITMODE-END*/;
//
//   function App() {
//     const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
//     return (
//       <div style={{ fontSize: t.fontSize, color: t.primaryColor }}>
//         Hello
//         <TweaksPanel>
//           <TweakSection label="Typography" />
//           <TweakSlider label="Font size" value={t.fontSize} min={10} max={32} unit="px"
//                        onChange={(v) => setTweak('fontSize', v)} />
//           <TweakRadio  label="Density" value={t.density}
//                        options={['compact', 'regular', 'comfy']}
//                        onChange={(v) => setTweak('density', v)} />
//           <TweakSection label="Theme" />
//           <TweakColor  label="Primary" value={t.primaryColor}
//                        options={['#D97757', '#2A6FDB', '#1F8A5B', '#7A5AE0']}
//                        onChange={(v) => setTweak('primaryColor', v)} />
//           <TweakColor  label="Palette" value={t.palette}
//                        options={[['#D97757', '#29261b', '#f6f4ef'],
//                                  ['#475569', '#0f172a', '#f1f5f9']]}
//                        onChange={(v) => setTweak('palette', v)} />
//           <TweakToggle label="Dark mode" value={t.dark}
//                        onChange={(v) => setTweak('dark', v)} />
//         </TweaksPanel>
//       </div>
//     );
//   }
//
// TweakRadio is the segmented control for 2–3 short options (auto-falls-back to
// TweakSelect past ~16/~10 chars per label); reach for TweakSelect directly when
// options are many or long. For color tweaks always curate 3-4 options rather than
// a free picker; an option can also be a whole 2–5 color palette (the stored value
// is the array). The Tweak* controls are a floor, not a ceiling — build custom
// controls inside the panel if a tweak calls for UI they don't cover.
/* END USAGE */
// ─────────────────────────────────────────────────────────────────────────────

const __TWEAKS_STYLE = `
  .twk-panel{position:fixed;right:16px;bottom:16px;z-index:2147483646;width:280px;
    max-height:calc(100vh - 32px);display:flex;flex-direction:column;
    transform:scale(var(--dc-inv-zoom,1));transform-origin:bottom right;
    background:rgba(250,249,247,.78);color:#29261b;
    -webkit-backdrop-filter:blur(24px) saturate(160%);backdrop-filter:blur(24px) saturate(160%);
    border:.5px solid rgba(255,255,255,.6);border-radius:14px;
    box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 12px 40px rgba(0,0,0,.18);
    font:11.5px/1.4 ui-sans-serif,system-ui,-apple-system,sans-serif;overflow:hidden}
  .twk-hd{display:flex;align-items:center;justify-content:space-between;
    padding:10px 8px 10px 14px;cursor:move;user-select:none}
  .twk-hd b{font-size:12px;font-weight:600;letter-spacing:.01em}
  .twk-x{appearance:none;border:0;background:transparent;color:rgba(41,38,27,.55);
    width:22px;height:22px;border-radius:6px;cursor:default;font-size:13px;line-height:1}
  .twk-x:hover{background:rgba(0,0,0,.06);color:#29261b}
  .twk-body{padding:2px 14px 14px;display:flex;flex-direction:column;gap:10px;
    overflow-y:auto;overflow-x:hidden;min-height:0;
    scrollbar-width:thin;scrollbar-color:rgba(0,0,0,.15) transparent}
  .twk-body::-webkit-scrollbar{width:8px}
  .twk-body::-webkit-scrollbar-track{background:transparent;margin:2px}
  .twk-body::-webkit-scrollbar-thumb{background:rgba(0,0,0,.15);border-radius:4px;
    border:2px solid transparent;background-clip:content-box}
  .twk-body::-webkit-scrollbar-thumb:hover{background:rgba(0,0,0,.25);
    border:2px solid transparent;background-clip:content-box}
  .twk-row{display:flex;flex-direction:column;gap:5px}
  .twk-row-h{flex-direction:row;align-items:center;justify-content:space-between;gap:10px}
  .twk-lbl{display:flex;justify-content:space-between;align-items:baseline;
    color:rgba(41,38,27,.72)}
  .twk-lbl>span:first-child{font-weight:500}
  .twk-val{color:rgba(41,38,27,.5);font-variant-numeric:tabular-nums}

  .twk-sect{font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
    color:rgba(41,38,27,.45);padding:10px 0 0}
  .twk-sect:first-child{padding-top:0}

  .twk-field{appearance:none;box-sizing:border-box;width:100%;min-width:0;height:26px;padding:0 8px;
    border:.5px solid rgba(0,0,0,.1);border-radius:7px;
    background:rgba(255,255,255,.6);color:inherit;font:inherit;outline:none}
  .twk-field:focus{border-color:rgba(0,0,0,.25);background:rgba(255,255,255,.85)}
  select.twk-field{padding-right:22px;
    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'><path fill='rgba(0,0,0,.5)' d='M0 0h10L5 6z'/></svg>");
    background-repeat:no-repeat;background-position:right 8px center}

  .twk-slider{appearance:none;-webkit-appearance:none;width:100%;height:4px;margin:6px 0;
    border-radius:999px;background:rgba(0,0,0,.12);outline:none}
  .twk-slider::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;
    width:14px;height:14px;border-radius:50%;background:#fff;
    border:.5px solid rgba(0,0,0,.12);box-shadow:0 1px 3px rgba(0,0,0,.2);cursor:default}
  .twk-slider::-moz-range-thumb{width:14px;height:14px;border-radius:50%;
    background:#fff;border:.5px solid rgba(0,0,0,.12);box-shadow:0 1px 3px rgba(0,0,0,.2);cursor:default}

  .twk-seg{position:relative;display:flex;padding:2px;border-radius:8px;
    background:rgba(0,0,0,.06);user-select:none}
  .twk-seg-thumb{position:absolute;top:2px;bottom:2px;border-radius:6px;
    background:rgba(255,255,255,.9);box-shadow:0 1px 2px rgba(0,0,0,.12);
    transition:left .15s cubic-bezier(.3,.7,.4,1),width .15s}
  .twk-seg.dragging .twk-seg-thumb{transition:none}
  .twk-seg button{appearance:none;position:relative;z-index:1;flex:1;border:0;
    background:transparent;color:inherit;font:inherit;font-weight:500;min-height:22px;
    border-radius:6px;cursor:default;padding:4px 6px;line-height:1.2;
    overflow-wrap:anywhere}

  .twk-toggle{position:relative;width:32px;height:18px;border:0;border-radius:999px;
    background:rgba(0,0,0,.15);transition:background .15s;cursor:default;padding:0}
  .twk-toggle[data-on="1"]{background:#34c759}
  .twk-toggle i{position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;
    background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.25);transition:transform .15s}
  .twk-toggle[data-on="1"] i{transform:translateX(14px)}

  .twk-num{display:flex;align-items:center;box-sizing:border-box;min-width:0;height:26px;padding:0 0 0 8px;
    border:.5px solid rgba(0,0,0,.1);border-radius:7px;background:rgba(255,255,255,.6)}
  .twk-num-lbl{font-weight:500;color:rgba(41,38,27,.6);cursor:ew-resize;
    user-select:none;padding-right:8px}
  .twk-num input{flex:1;min-width:0;height:100%;border:0;background:transparent;
    font:inherit;font-variant-numeric:tabular-nums;text-align:right;padding:0 8px 0 0;
    outline:none;color:inherit;-moz-appearance:textfield}
  .twk-num input::-webkit-inner-spin-button,.twk-num input::-webkit-outer-spin-button{
    -webkit-appearance:none;margin:0}
  .twk-num-unit{padding-right:8px;color:rgba(41,38,27,.45)}

  .twk-btn{appearance:none;height:26px;padding:0 12px;border:0;border-radius:7px;
    background:rgba(0,0,0,.78);color:#fff;font:inherit;font-weight:500;cursor:default}
  .twk-btn:hover{background:rgba(0,0,0,.88)}
  .twk-btn.secondary{background:rgba(0,0,0,.06);color:inherit}
  .twk-btn.secondary:hover{background:rgba(0,0,0,.1)}

  .twk-swatch{appearance:none;-webkit-appearance:none;width:56px;height:22px;
    border:.5px solid rgba(0,0,0,.1);border-radius:6px;padding:0;cursor:default;
    background:transparent;flex-shrink:0}
  .twk-swatch::-webkit-color-swatch-wrapper{padding:0}
  .twk-swatch::-webkit-color-swatch{border:0;border-radius:5.5px}
  .twk-swatch::-moz-color-swatch{border:0;border-radius:5.5px}

  .twk-chips{display:flex;gap:6px}
  .twk-chip{position:relative;appearance:none;flex:1;min-width:0;height:46px;
    padding:0;border:0;border-radius:6px;overflow:hidden;cursor:default;
    box-shadow:0 0 0 .5px rgba(0,0,0,.12),0 1px 2px rgba(0,0,0,.06);
    transition:transform .12s cubic-bezier(.3,.7,.4,1),box-shadow .12s}
  .twk-chip:hover{transform:translateY(-1px);
    box-shadow:0 0 0 .5px rgba(0,0,0,.18),0 4px 10px rgba(0,0,0,.12)}
  .twk-chip[data-on="1"]{box-shadow:0 0 0 1.5px rgba(0,0,0,.85),
    0 2px 6px rgba(0,0,0,.15)}
  .twk-chip>span{position:absolute;top:0;bottom:0;right:0;width:34%;
    display:flex;flex-direction:column;box-shadow:-1px 0 0 rgba(0,0,0,.1)}
  .twk-chip>span>i{flex:1;box-shadow:0 -1px 0 rgba(0,0,0,.1)}
  .twk-chip>span>i:first-child{box-shadow:none}
  .twk-chip svg{position:absolute;top:6px;left:6px;width:13px;height:13px;
    filter:drop-shadow(0 1px 1px rgba(0,0,0,.3))}
`;

// ── useTweaks ───────────────────────────────────────────────────────────────
// Single source of truth for tweak values. setTweak persists via the host
// (__edit_mode_set_keys → host rewrites the EDITMODE block on disk).
function useTweaks(defaults) {
  const [values, setValues] = React.useState(defaults);
  // Accepts either setTweak('key', value) or setTweak({ key: value, ... }) so a
  // useState-style call doesn't write a "[object Object]" key into the persisted
  // JSON block.
  const setTweak = React.useCallback((keyOrEdits, val) => {
    const edits = typeof keyOrEdits === 'object' && keyOrEdits !== null ? keyOrEdits : {
      [keyOrEdits]: val
    };
    setValues(prev => ({
      ...prev,
      ...edits
    }));
    window.parent.postMessage({
      type: '__edit_mode_set_keys',
      edits
    }, '*');
    // Same-window signal so in-page listeners (deck-stage rail thumbnails)
    // can react — the parent message only reaches the host, not peers.
    window.dispatchEvent(new CustomEvent('tweakchange', {
      detail: edits
    }));
  }, []);
  return [values, setTweak];
}

// ── TweaksPanel ─────────────────────────────────────────────────────────────
// Floating shell. Registers the protocol listener BEFORE announcing
// availability — if the announce ran first, the host's activate could land
// before our handler exists and the toolbar toggle would silently no-op.
// The close button posts __edit_mode_dismissed so the host's toolbar toggle
// flips off in lockstep; the host echoes __deactivate_edit_mode back which
// is what actually hides the panel.
function TweaksPanel({
  title = 'Tweaks',
  children
}) {
  const [open, setOpen] = React.useState(false);
  const dragRef = React.useRef(null);
  const offsetRef = React.useRef({
    x: 16,
    y: 16
  });
  const PAD = 16;
  const clampToViewport = React.useCallback(() => {
    const panel = dragRef.current;
    if (!panel) return;
    const w = panel.offsetWidth,
      h = panel.offsetHeight;
    const maxRight = Math.max(PAD, window.innerWidth - w - PAD);
    const maxBottom = Math.max(PAD, window.innerHeight - h - PAD);
    offsetRef.current = {
      x: Math.min(maxRight, Math.max(PAD, offsetRef.current.x)),
      y: Math.min(maxBottom, Math.max(PAD, offsetRef.current.y))
    };
    panel.style.right = offsetRef.current.x + 'px';
    panel.style.bottom = offsetRef.current.y + 'px';
  }, []);
  React.useEffect(() => {
    if (!open) return;
    clampToViewport();
    if (typeof ResizeObserver === 'undefined') {
      window.addEventListener('resize', clampToViewport);
      return () => window.removeEventListener('resize', clampToViewport);
    }
    const ro = new ResizeObserver(clampToViewport);
    ro.observe(document.documentElement);
    return () => ro.disconnect();
  }, [open, clampToViewport]);
  React.useEffect(() => {
    const onMsg = e => {
      const t = e?.data?.type;
      if (t === '__activate_edit_mode') setOpen(true);else if (t === '__deactivate_edit_mode') setOpen(false);
    };
    window.addEventListener('message', onMsg);
    window.parent.postMessage({
      type: '__edit_mode_available'
    }, '*');
    return () => window.removeEventListener('message', onMsg);
  }, []);
  const dismiss = () => {
    setOpen(false);
    window.parent.postMessage({
      type: '__edit_mode_dismissed'
    }, '*');
  };
  const onDragStart = e => {
    const panel = dragRef.current;
    if (!panel) return;
    const r = panel.getBoundingClientRect();
    const sx = e.clientX,
      sy = e.clientY;
    const startRight = window.innerWidth - r.right;
    const startBottom = window.innerHeight - r.bottom;
    const move = ev => {
      offsetRef.current = {
        x: startRight - (ev.clientX - sx),
        y: startBottom - (ev.clientY - sy)
      };
      clampToViewport();
    };
    const up = () => {
      window.removeEventListener('mousemove', move);
      window.removeEventListener('mouseup', up);
    };
    window.addEventListener('mousemove', move);
    window.addEventListener('mouseup', up);
  };
  if (!open) return null;
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("style", null, __TWEAKS_STYLE), /*#__PURE__*/React.createElement("div", {
    ref: dragRef,
    className: "twk-panel",
    "data-omelette-chrome": "",
    style: {
      right: offsetRef.current.x,
      bottom: offsetRef.current.y
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "twk-hd",
    onMouseDown: onDragStart
  }, /*#__PURE__*/React.createElement("b", null, title), /*#__PURE__*/React.createElement("button", {
    className: "twk-x",
    "aria-label": "Close tweaks",
    onMouseDown: e => e.stopPropagation(),
    onClick: dismiss
  }, "\u2715")), /*#__PURE__*/React.createElement("div", {
    className: "twk-body"
  }, children)));
}

// ── Layout helpers ──────────────────────────────────────────────────────────

function TweakSection({
  label,
  children
}) {
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "twk-sect"
  }, label), children);
}
function TweakRow({
  label,
  value,
  children,
  inline = false
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: inline ? 'twk-row twk-row-h' : 'twk-row'
  }, /*#__PURE__*/React.createElement("div", {
    className: "twk-lbl"
  }, /*#__PURE__*/React.createElement("span", null, label), value != null && /*#__PURE__*/React.createElement("span", {
    className: "twk-val"
  }, value)), children);
}

// ── Controls ────────────────────────────────────────────────────────────────

function TweakSlider({
  label,
  value,
  min = 0,
  max = 100,
  step = 1,
  unit = '',
  onChange
}) {
  return /*#__PURE__*/React.createElement(TweakRow, {
    label: label,
    value: `${value}${unit}`
  }, /*#__PURE__*/React.createElement("input", {
    type: "range",
    className: "twk-slider",
    min: min,
    max: max,
    step: step,
    value: value,
    onChange: e => onChange(Number(e.target.value))
  }));
}
function TweakToggle({
  label,
  value,
  onChange
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "twk-row twk-row-h"
  }, /*#__PURE__*/React.createElement("div", {
    className: "twk-lbl"
  }, /*#__PURE__*/React.createElement("span", null, label)), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "twk-toggle",
    "data-on": value ? '1' : '0',
    role: "switch",
    "aria-checked": !!value,
    onClick: () => onChange(!value)
  }, /*#__PURE__*/React.createElement("i", null)));
}
function TweakRadio({
  label,
  value,
  options,
  onChange
}) {
  const trackRef = React.useRef(null);
  const [dragging, setDragging] = React.useState(false);
  // The active value is read by pointer-move handlers attached for the lifetime
  // of a drag — ref it so a stale closure doesn't fire onChange for every move.
  const valueRef = React.useRef(value);
  valueRef.current = value;

  // Segments wrap mid-word once per-segment width runs out. The track is
  // ~248px (280 panel − 28 body pad − 4 seg pad), each button loses 12px
  // to its own padding, and 11.5px system-ui averages ~6.3px/char — so 2
  // options fit ~16 chars each, 3 fit ~10. Past that (or >3 options), fall
  // back to a dropdown rather than wrap.
  const labelLen = o => String(typeof o === 'object' ? o.label : o).length;
  const maxLen = options.reduce((m, o) => Math.max(m, labelLen(o)), 0);
  const fitsAsSegments = maxLen <= ({
    2: 16,
    3: 10
  }[options.length] ?? 0);
  if (!fitsAsSegments) {
    // <select> emits strings — map back to the original option value so the
    // fallback stays type-preserving (numbers, booleans) like the segment path.
    const resolve = s => {
      const m = options.find(o => String(typeof o === 'object' ? o.value : o) === s);
      return m === undefined ? s : typeof m === 'object' ? m.value : m;
    };
    return /*#__PURE__*/React.createElement(TweakSelect, {
      label: label,
      value: value,
      options: options,
      onChange: s => onChange(resolve(s))
    });
  }
  const opts = options.map(o => typeof o === 'object' ? o : {
    value: o,
    label: o
  });
  const idx = Math.max(0, opts.findIndex(o => o.value === value));
  const n = opts.length;
  const segAt = clientX => {
    const r = trackRef.current.getBoundingClientRect();
    const inner = r.width - 4;
    const i = Math.floor((clientX - r.left - 2) / inner * n);
    return opts[Math.max(0, Math.min(n - 1, i))].value;
  };
  const onPointerDown = e => {
    setDragging(true);
    const v0 = segAt(e.clientX);
    if (v0 !== valueRef.current) onChange(v0);
    const move = ev => {
      if (!trackRef.current) return;
      const v = segAt(ev.clientX);
      if (v !== valueRef.current) onChange(v);
    };
    const up = () => {
      setDragging(false);
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
    };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
  };
  return /*#__PURE__*/React.createElement(TweakRow, {
    label: label
  }, /*#__PURE__*/React.createElement("div", {
    ref: trackRef,
    role: "radiogroup",
    onPointerDown: onPointerDown,
    className: dragging ? 'twk-seg dragging' : 'twk-seg'
  }, /*#__PURE__*/React.createElement("div", {
    className: "twk-seg-thumb",
    style: {
      left: `calc(2px + ${idx} * (100% - 4px) / ${n})`,
      width: `calc((100% - 4px) / ${n})`
    }
  }), opts.map(o => /*#__PURE__*/React.createElement("button", {
    key: o.value,
    type: "button",
    role: "radio",
    "aria-checked": o.value === value
  }, o.label))));
}
function TweakSelect({
  label,
  value,
  options,
  onChange
}) {
  return /*#__PURE__*/React.createElement(TweakRow, {
    label: label
  }, /*#__PURE__*/React.createElement("select", {
    className: "twk-field",
    value: value,
    onChange: e => onChange(e.target.value)
  }, options.map(o => {
    const v = typeof o === 'object' ? o.value : o;
    const l = typeof o === 'object' ? o.label : o;
    return /*#__PURE__*/React.createElement("option", {
      key: v,
      value: v
    }, l);
  })));
}
function TweakText({
  label,
  value,
  placeholder,
  onChange
}) {
  return /*#__PURE__*/React.createElement(TweakRow, {
    label: label
  }, /*#__PURE__*/React.createElement("input", {
    className: "twk-field",
    type: "text",
    value: value,
    placeholder: placeholder,
    onChange: e => onChange(e.target.value)
  }));
}
function TweakNumber({
  label,
  value,
  min,
  max,
  step = 1,
  unit = '',
  onChange
}) {
  const clamp = n => {
    if (min != null && n < min) return min;
    if (max != null && n > max) return max;
    return n;
  };
  const startRef = React.useRef({
    x: 0,
    val: 0
  });
  const onScrubStart = e => {
    e.preventDefault();
    startRef.current = {
      x: e.clientX,
      val: value
    };
    const decimals = (String(step).split('.')[1] || '').length;
    const move = ev => {
      const dx = ev.clientX - startRef.current.x;
      const raw = startRef.current.val + dx * step;
      const snapped = Math.round(raw / step) * step;
      onChange(clamp(Number(snapped.toFixed(decimals))));
    };
    const up = () => {
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
    };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "twk-num"
  }, /*#__PURE__*/React.createElement("span", {
    className: "twk-num-lbl",
    onPointerDown: onScrubStart
  }, label), /*#__PURE__*/React.createElement("input", {
    type: "number",
    value: value,
    min: min,
    max: max,
    step: step,
    onChange: e => onChange(clamp(Number(e.target.value)))
  }), unit && /*#__PURE__*/React.createElement("span", {
    className: "twk-num-unit"
  }, unit));
}

// Relative-luminance contrast pick — checkmarks drawn over a swatch need to
// read on both #111 and #fafafa without per-option configuration. Hex input
// only (#rgb / #rrggbb); named or rgb()/hsl() colors fall through to "light".
function __twkIsLight(hex) {
  const h = String(hex).replace('#', '');
  const x = h.length === 3 ? h.replace(/./g, c => c + c) : h.padEnd(6, '0');
  const n = parseInt(x.slice(0, 6), 16);
  if (Number.isNaN(n)) return true;
  const r = n >> 16 & 255,
    g = n >> 8 & 255,
    b = n & 255;
  return r * 299 + g * 587 + b * 114 > 148000;
}
const __TwkCheck = ({
  light
}) => /*#__PURE__*/React.createElement("svg", {
  viewBox: "0 0 14 14",
  "aria-hidden": "true"
}, /*#__PURE__*/React.createElement("path", {
  d: "M3 7.2 5.8 10 11 4.2",
  fill: "none",
  strokeWidth: "2.2",
  strokeLinecap: "round",
  strokeLinejoin: "round",
  stroke: light ? 'rgba(0,0,0,.78)' : '#fff'
}));

// TweakColor — curated color/palette picker. Each option is either a single
// hex string or an array of 1-5 hex strings; the card adapts — a lone color
// renders solid, a palette renders colors[0] as the hero (left ~2/3) with the
// rest stacked in a sharp column on the right. onChange emits the
// option in the shape it was passed (string stays string, array stays array).
// Without options it falls back to the native color input for back-compat.
function TweakColor({
  label,
  value,
  options,
  onChange
}) {
  if (!options || !options.length) {
    return /*#__PURE__*/React.createElement("div", {
      className: "twk-row twk-row-h"
    }, /*#__PURE__*/React.createElement("div", {
      className: "twk-lbl"
    }, /*#__PURE__*/React.createElement("span", null, label)), /*#__PURE__*/React.createElement("input", {
      type: "color",
      className: "twk-swatch",
      value: value,
      onChange: e => onChange(e.target.value)
    }));
  }
  // Native <input type=color> emits lowercase hex per the HTML spec, so
  // compare case-insensitively. String() guards JSON.stringify(undefined),
  // which returns the primitive undefined (no .toLowerCase).
  const key = o => String(JSON.stringify(o)).toLowerCase();
  const cur = key(value);
  return /*#__PURE__*/React.createElement(TweakRow, {
    label: label
  }, /*#__PURE__*/React.createElement("div", {
    className: "twk-chips",
    role: "radiogroup"
  }, options.map((o, i) => {
    const colors = Array.isArray(o) ? o : [o];
    const [hero, ...rest] = colors;
    const sup = rest.slice(0, 4);
    const on = key(o) === cur;
    return /*#__PURE__*/React.createElement("button", {
      key: i,
      type: "button",
      className: "twk-chip",
      role: "radio",
      "aria-checked": on,
      "data-on": on ? '1' : '0',
      "aria-label": colors.join(', '),
      title: colors.join(' · '),
      style: {
        background: hero
      },
      onClick: () => onChange(o)
    }, sup.length > 0 && /*#__PURE__*/React.createElement("span", null, sup.map((c, j) => /*#__PURE__*/React.createElement("i", {
      key: j,
      style: {
        background: c
      }
    }))), on && /*#__PURE__*/React.createElement(__TwkCheck, {
      light: __twkIsLight(hero)
    }));
  })));
}
function TweakButton({
  label,
  onClick,
  secondary = false
}) {
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: secondary ? 'twk-btn secondary' : 'twk-btn',
    onClick: onClick
  }, label);
}
Object.assign(window, {
  useTweaks,
  TweaksPanel,
  TweakSection,
  TweakRow,
  TweakSlider,
  TweakToggle,
  TweakRadio,
  TweakSelect,
  TweakText,
  TweakNumber,
  TweakColor,
  TweakButton
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/tweaks-panel.jsx", error: String((e && e.message) || e) }); }

// ui_kits/landing/field.js
try { (() => {
/* Market Story landing — the live market-field canvas + UTC clock + tape.
   Cursor-reactive parallax; cyan accent to match the product palette. Synthetic
   data (no network). */
(function () {
  // --- UTC clock ---
  function tick() {
    const d = new Date(),
      p = n => String(n).padStart(2, "0");
    const s = p(d.getUTCHours()) + ":" + p(d.getUTCMinutes()) + ":" + p(d.getUTCSeconds()) + " UTC";
    document.getElementById("clock").textContent = s;
    document.getElementById("clock2").textContent = s;
  }
  tick();
  setInterval(tick, 1000);

  // --- synthetic "today's index paths" (seeded walks; one accent S&P line) ---
  function walk(n, drift, vol, seed) {
    let v = 0,
      out = [],
      s = seed;
    const rnd = () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
    for (let i = 0; i < n; i++) {
      v += drift + (rnd() - 0.5) * vol;
      out.push(v);
    }
    return out;
  }
  const SET = [{
    accent: true,
    d: 0.9,
    v: 2.2,
    seed: 7
  }, {
    accent: false,
    d: 0.7,
    v: 3.0,
    seed: 13
  }, {
    accent: false,
    d: 0.4,
    v: 3.4,
    seed: 21
  }, {
    accent: false,
    d: 0.6,
    v: 2.8,
    seed: 34
  }, {
    accent: false,
    d: -0.2,
    v: 3.6,
    seed: 55
  }, {
    accent: false,
    d: 0.3,
    v: 4.0,
    seed: 89
  }, {
    accent: false,
    d: 0.5,
    v: 2.6,
    seed: 144
  }];
  const lines = SET.map((c, i) => {
    const arr = walk(90, c.d, c.v, c.seed);
    const mn = Math.min(...arr),
      mx = Math.max(...arr),
      rng = mx - mn || 1;
    return {
      accent: c.accent,
      depth: c.accent ? 1 : 0.25 + i / SET.length * 0.6,
      y: arr.map(x => 1 - (x - mn) / rng)
    };
  }).sort((a, b) => a.accent - b.accent); // accent drawn last, on top

  const cv = document.getElementById("field"),
    ctx = cv.getContext("2d");
  let W,
    H,
    prog = 1,
    mx = 0.5,
    my = 0.5,
    tmx = 0.5,
    tmy = 0.5; // fully drawn from first paint
  const ACCENT = "123,234,251",
    FAINT = "179,170,160";
  function resize() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = cv.width = innerWidth * dpr;
    H = cv.height = innerHeight * dpr;
    cv.style.width = innerWidth + "px";
    cv.style.height = innerHeight + "px";
  }
  resize();
  addEventListener("resize", resize);
  addEventListener("mousemove", e => {
    tmx = e.clientX / innerWidth;
    tmy = e.clientY / innerHeight;
  });
  function frame() {
    mx += (tmx - mx) * 0.06;
    my += (tmy - my) * 0.06;
    ctx.clearRect(0, 0, W, H);
    const dpr = Math.min(devicePixelRatio || 1, 2);
    const top = H * 0.50,
      bot = H * 0.13,
      band = H - top - bot;
    for (const ln of lines) {
      const N = ln.y.length,
        n = Math.max(2, Math.floor(N * prog));
      const sx = (mx - 0.5) * 46 * ln.depth * dpr,
        sy = (my - 0.5) * 26 * ln.depth * dpr;
      const px = i => i / (N - 1) * W + sx,
        py = i => top + ln.y[i] * band + sy;
      if (ln.accent) {
        ctx.beginPath();
        ctx.moveTo(px(0), py(0));
        for (let i = 1; i < n; i++) ctx.lineTo(px(i), py(i));
        ctx.lineTo(px(n - 1), top + band + sy);
        ctx.lineTo(px(0), top + band + sy);
        ctx.closePath();
        const g = ctx.createLinearGradient(0, top, 0, top + band);
        g.addColorStop(0, `rgba(${ACCENT},0.17)`);
        g.addColorStop(1, `rgba(${ACCENT},0)`);
        ctx.fillStyle = g;
        ctx.fill();
      }
      ctx.beginPath();
      ctx.moveTo(px(0), py(0));
      for (let i = 1; i < n; i++) ctx.lineTo(px(i), py(i));
      ctx.strokeStyle = ln.accent ? `rgba(${ACCENT},0.95)` : `rgba(${FAINT},0.15)`;
      ctx.lineWidth = (ln.accent ? 2.4 : 1.0) * dpr;
      ctx.stroke();
      if (prog >= 1 && ln.accent) {
        const x = px(n - 1),
          y = py(n - 1);
        ctx.fillStyle = `rgba(${ACCENT},1)`;
        ctx.beginPath();
        ctx.arc(x, y, 4 * dpr, 0, 7);
        ctx.fill();
        ctx.strokeStyle = `rgba(${ACCENT},0.35)`;
        ctx.lineWidth = 1 * dpr;
        ctx.beginPath();
        ctx.arc(x, y, 9 * dpr, 0, 7);
        ctx.stroke();
      }
    }
    requestAnimationFrame(frame); // continuous — cursor parallax keeps drifting
  }
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) prog = 1;
  frame();

  // --- tape (static sample values, matching the brief) ---
  const tape = {
    sp: "7,553.68",
    spd: "+0.18%",
    spUp: true,
    vix: "16.50",
    vixd: "+2.8%",
    vixUp: false,
    ty: "4.491%",
    br: "4 / 7"
  };
  const $ = id => document.getElementById(id);
  $("sp").textContent = tape.sp;
  $("spd").textContent = tape.spd;
  $("spd").className = "d " + (tape.spUp ? "up" : "down");
  $("vix").textContent = tape.vix;
  $("vixd").textContent = tape.vixd;
  $("vixd").className = "d " + (tape.vixUp ? "up" : "down");
  $("ty").textContent = tape.ty;
  $("br").textContent = tape.br;
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/landing/field.js", error: String((e && e.message) || e) }); }

})();
