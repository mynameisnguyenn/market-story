/* Market Story — reusable market-field canvas engine.
   Draws today's (synthetic) index paths with a cursor-reactive parallax drift.
   Used prominently on the cover, and faintly as an ambient layer behind the
   dashboard. window.startMarketField(canvas, opts) -> { destroy() }. */
window.startMarketField = function (canvas, opts) {
  opts = opts || {};
  let accentRGB = opts.accentRGB || "123,234,251";   // cyan (mutable via setAccent)
  let faintRGB  = opts.faintRGB  || "179,170,160";    // warm grey (mutable via setFaint)
  const topFrac   = opts.topFrac != null ? opts.topFrac : 0.5;
  const botFrac   = opts.botFrac != null ? opts.botFrac : 0.13;
  const lineScale = opts.lineScale || 1;
  const parallax  = opts.parallax != null ? opts.parallax : 44;
  const reduce    = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // intensity: 'off' | 'low' | 'high' (or a numeric base alpha). Maps to an alpha multiplier.
  const ALPHA = { off: 0, low: 0.42, high: 0.85 };
  let baseAlpha = opts.alpha != null ? opts.alpha : 1;
  let intensity = opts.intensity || null;
  function effAlpha() { return intensity != null ? (ALPHA[intensity] != null ? ALPHA[intensity] : baseAlpha) : baseAlpha; }

  const ctx = canvas.getContext("2d");
  let W, H, raf, prog = 1;   // fully drawn from first paint (never a blank hero); parallax stays live
  let mx = 0.5, my = 0.5, tmx = 0.5, tmy = 0.5;   // eased vs target cursor

  function walk(n, drift, vol, seed) {
    let v = 0, out = [], s = seed;
    const rnd = () => { s = (s * 9301 + 49297) % 233280; return s / 233280; };
    for (let i = 0; i < n; i++) { v += drift + (rnd() - 0.5) * vol; out.push(v); }
    return out;
  }
  const SET = [
    { accent:true,  d:0.9,  v:2.2, seed:7 },
    { accent:false, d:0.7,  v:3.0, seed:13 },
    { accent:false, d:0.4,  v:3.4, seed:21 },
    { accent:false, d:0.6,  v:2.8, seed:34 },
    { accent:false, d:-0.2, v:3.6, seed:55 },
    { accent:false, d:0.3,  v:4.0, seed:89 },
    { accent:false, d:0.5,  v:2.6, seed:144 },
  ];
  const lines = SET.map((c, i) => {
    const arr = walk(90, c.d, c.v, c.seed);
    const mn = Math.min(...arr), mx2 = Math.max(...arr), rng = (mx2 - mn) || 1;
    return { accent:c.accent, depth: c.accent ? 1 : 0.25 + (i / SET.length) * 0.6, y: arr.map(x => 1 - (x - mn) / rng) };
  }).sort((a, b) => a.accent - b.accent);   // accent line drawn last, on top

  function resize() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = canvas.width = Math.max(1, canvas.clientWidth) * dpr;
    H = canvas.height = Math.max(1, canvas.clientHeight) * dpr;
  }
  function onMove(e) { tmx = e.clientX / innerWidth; tmy = e.clientY / innerHeight; }

  function frame() {
    const alpha = effAlpha();
    const dpr = Math.min(devicePixelRatio || 1, 2);
    // self-heal: if the canvas box changed (or wasn't laid out at init), re-fit the buffer
    if (canvas.clientWidth * dpr !== W || canvas.clientHeight * dpr !== H) resize();
    if (alpha <= 0.001) { ctx.clearRect(0, 0, W, H); raf = requestAnimationFrame(frame); return; }
    if (!reduce) { mx += (tmx - mx) * 0.06; my += (tmy - my) * 0.06; } else { mx = 0.5; my = 0.5; }
    ctx.clearRect(0, 0, W, H);
    const top = H * topFrac, bot = H * botFrac, band = H - top - bot;
    const par = reduce ? 0 : parallax;
    for (const ln of lines) {
      const N = ln.y.length, n = Math.max(2, Math.floor(N * prog));
      const sx = (mx - 0.5) * par * ln.depth * dpr;
      const sy = (my - 0.5) * par * 0.55 * ln.depth * dpr;
      const px = i => (i / (N - 1)) * W + sx;
      const py = i => top + ln.y[i] * band + sy;
      if (ln.accent) {
        ctx.beginPath(); ctx.moveTo(px(0), py(0));
        for (let i = 1; i < n; i++) ctx.lineTo(px(i), py(i));
        ctx.lineTo(px(n - 1), top + band + sy); ctx.lineTo(px(0), top + band + sy); ctx.closePath();
        const g = ctx.createLinearGradient(0, top, 0, top + band);
        g.addColorStop(0, `rgba(${accentRGB},${0.17 * alpha})`); g.addColorStop(1, `rgba(${accentRGB},0)`);
        ctx.fillStyle = g; ctx.fill();
      }
      ctx.beginPath(); ctx.moveTo(px(0), py(0));
      for (let i = 1; i < n; i++) ctx.lineTo(px(i), py(i));
      ctx.strokeStyle = ln.accent ? `rgba(${accentRGB},${0.95 * alpha})` : `rgba(${faintRGB},${0.16 * alpha})`;
      ctx.lineWidth = (ln.accent ? 2.4 : 1.0) * lineScale * dpr; ctx.stroke();
      if (prog >= 1 && ln.accent) {
        const x = px(n - 1), y = py(n - 1);
        ctx.fillStyle = `rgba(${accentRGB},${alpha})`; ctx.beginPath(); ctx.arc(x, y, 4 * dpr, 0, 7); ctx.fill();
        ctx.strokeStyle = `rgba(${accentRGB},${0.35 * alpha})`; ctx.lineWidth = 1 * dpr; ctx.beginPath(); ctx.arc(x, y, 9 * dpr, 0, 7); ctx.stroke();
      }
    }
    raf = requestAnimationFrame(frame);
  }

  resize();
  addEventListener("resize", resize);
  addEventListener("mousemove", onMove);
  frame();
  return {
    setIntensity(v) { intensity = v; },
    setAccent(rgb) { if (rgb) accentRGB = rgb; },
    setFaint(rgb) { if (rgb) faintRGB = rgb; },
    destroy() { cancelAnimationFrame(raf); removeEventListener("resize", resize); removeEventListener("mousemove", onMove); }
  };
};
