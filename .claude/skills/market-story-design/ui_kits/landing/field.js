/* Market Story landing — the live market-field canvas + UTC clock + tape.
   Cursor-reactive parallax; cyan accent to match the product palette. Synthetic
   data (no network). */
(function () {
  // --- UTC clock ---
  function tick() {
    const d = new Date(), p = n => String(n).padStart(2, "0");
    const s = p(d.getUTCHours()) + ":" + p(d.getUTCMinutes()) + ":" + p(d.getUTCSeconds()) + " UTC";
    document.getElementById("clock").textContent = s;
    document.getElementById("clock2").textContent = s;
  }
  tick(); setInterval(tick, 1000);

  // --- synthetic "today's index paths" (seeded walks; one accent S&P line) ---
  function walk(n, drift, vol, seed) {
    let v = 0, out = [], s = seed;
    const rnd = () => { s = (s * 9301 + 49297) % 233280; return s / 233280; };
    for (let i = 0; i < n; i++) { v += drift + (rnd() - 0.5) * vol; out.push(v); }
    return out;
  }
  const SET = [
    { accent: true,  d: 0.9,  v: 2.2, seed: 7 },
    { accent: false, d: 0.7,  v: 3.0, seed: 13 },
    { accent: false, d: 0.4,  v: 3.4, seed: 21 },
    { accent: false, d: 0.6,  v: 2.8, seed: 34 },
    { accent: false, d: -0.2, v: 3.6, seed: 55 },
    { accent: false, d: 0.3,  v: 4.0, seed: 89 },
    { accent: false, d: 0.5,  v: 2.6, seed: 144 },
  ];
  const lines = SET.map((c, i) => {
    const arr = walk(90, c.d, c.v, c.seed);
    const mn = Math.min(...arr), mx = Math.max(...arr), rng = (mx - mn) || 1;
    return { accent: c.accent, depth: c.accent ? 1 : 0.25 + (i / SET.length) * 0.6, y: arr.map(x => 1 - (x - mn) / rng) };
  }).sort((a, b) => a.accent - b.accent);   // accent drawn last, on top

  const cv = document.getElementById("field"), ctx = cv.getContext("2d");
  let W, H, prog = 1, mx = 0.5, my = 0.5, tmx = 0.5, tmy = 0.5;   // fully drawn from first paint
  const ACCENT = "123,234,251", FAINT = "179,170,160";
  function resize() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = cv.width = innerWidth * dpr; H = cv.height = innerHeight * dpr;
    cv.style.width = innerWidth + "px"; cv.style.height = innerHeight + "px";
  }
  resize();
  addEventListener("resize", resize);
  addEventListener("mousemove", e => { tmx = e.clientX / innerWidth; tmy = e.clientY / innerHeight; });

  function frame() {
    mx += (tmx - mx) * 0.06; my += (tmy - my) * 0.06;
    ctx.clearRect(0, 0, W, H);
    const dpr = Math.min(devicePixelRatio || 1, 2);
    const top = H * 0.50, bot = H * 0.13, band = H - top - bot;
    for (const ln of lines) {
      const N = ln.y.length, n = Math.max(2, Math.floor(N * prog));
      const sx = (mx - 0.5) * 46 * ln.depth * dpr, sy = (my - 0.5) * 26 * ln.depth * dpr;
      const px = i => (i / (N - 1)) * W + sx, py = i => top + ln.y[i] * band + sy;
      if (ln.accent) {
        ctx.beginPath(); ctx.moveTo(px(0), py(0));
        for (let i = 1; i < n; i++) ctx.lineTo(px(i), py(i));
        ctx.lineTo(px(n - 1), top + band + sy); ctx.lineTo(px(0), top + band + sy); ctx.closePath();
        const g = ctx.createLinearGradient(0, top, 0, top + band);
        g.addColorStop(0, `rgba(${ACCENT},0.17)`); g.addColorStop(1, `rgba(${ACCENT},0)`);
        ctx.fillStyle = g; ctx.fill();
      }
      ctx.beginPath(); ctx.moveTo(px(0), py(0));
      for (let i = 1; i < n; i++) ctx.lineTo(px(i), py(i));
      ctx.strokeStyle = ln.accent ? `rgba(${ACCENT},0.95)` : `rgba(${FAINT},0.15)`;
      ctx.lineWidth = (ln.accent ? 2.4 : 1.0) * dpr; ctx.stroke();
      if (prog >= 1 && ln.accent) {
        const x = px(n - 1), y = py(n - 1);
        ctx.fillStyle = `rgba(${ACCENT},1)`; ctx.beginPath(); ctx.arc(x, y, 4 * dpr, 0, 7); ctx.fill();
        ctx.strokeStyle = `rgba(${ACCENT},0.35)`; ctx.lineWidth = 1 * dpr; ctx.beginPath(); ctx.arc(x, y, 9 * dpr, 0, 7); ctx.stroke();
      }
    }
    requestAnimationFrame(frame);   // continuous — cursor parallax keeps drifting
  }
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) prog = 1;
  frame();

  // --- tape (static sample values, matching the brief) ---
  const tape = { sp: "7,553.68", spd: "+0.18%", spUp: true, vix: "16.50", vixd: "+2.8%", vixUp: false, ty: "4.491%", br: "4 / 7" };
  const $ = id => document.getElementById(id);
  $("sp").textContent = tape.sp; $("spd").textContent = tape.spd; $("spd").className = "d " + (tape.spUp ? "up" : "down");
  $("vix").textContent = tape.vix; $("vixd").textContent = tape.vixd; $("vixd").className = "d " + (tape.vixUp ? "up" : "down");
  $("ty").textContent = tape.ty;
  $("br").textContent = tape.br;
})();
