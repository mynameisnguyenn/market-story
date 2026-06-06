/* Market Story slides — static market-field motif on title/section/closing.
   Draws once per canvas[data-field]; redraws on resize + slide activation. */
(function () {
  const ACCENT = "123,234,251", FAINT = "179,170,160";
  function walk(n, drift, vol, seed) {
    let v = 0, o = [], s = seed;
    const r = () => { s = (s * 9301 + 49297) % 233280; return s / 233280; };
    for (let i = 0; i < n; i++) { v += drift + (r() - 0.5) * vol; o.push(v); }
    return o;
  }
  const SET = [
    { a:1, d:0.9, v:2.2, s:7 }, { a:0, d:0.7, v:3, s:13 }, { a:0, d:0.4, v:3.4, s:21 },
    { a:0, d:0.6, v:2.8, s:34 }, { a:0, d:-0.2, v:3.6, s:55 }, { a:0, d:0.3, v:4, s:89 }, { a:0, d:0.5, v:2.6, s:144 },
  ];
  const lines = SET.map(c => {
    const arr = walk(90, c.d, c.v, c.s);
    const mn = Math.min(...arr), mx = Math.max(...arr), rg = (mx - mn) || 1;
    return { a: c.a, y: arr.map(x => 1 - (x - mn) / rg) };
  }).sort((p, q) => p.a - q.a);

  function draw(cv) {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    const w = cv.clientWidth || 1920, h = cv.clientHeight || 1080;
    if (!w || !h) return;
    cv.width = w * dpr; cv.height = h * dpr;
    const W = cv.width, H = cv.height, ctx = cv.getContext("2d");
    ctx.clearRect(0, 0, W, H);
    const top = H * 0.46, band = H - top - H * 0.10;
    for (const ln of lines) {
      const N = ln.y.length, px = i => (i / (N - 1)) * W, py = i => top + ln.y[i] * band;
      if (ln.a) {
        ctx.beginPath(); ctx.moveTo(px(0), py(0));
        for (let i = 1; i < N; i++) ctx.lineTo(px(i), py(i));
        ctx.lineTo(px(N - 1), top + band); ctx.lineTo(px(0), top + band); ctx.closePath();
        const g = ctx.createLinearGradient(0, top, 0, top + band);
        g.addColorStop(0, `rgba(${ACCENT},0.16)`); g.addColorStop(1, `rgba(${ACCENT},0)`);
        ctx.fillStyle = g; ctx.fill();
      }
      ctx.beginPath(); ctx.moveTo(px(0), py(0));
      for (let i = 1; i < N; i++) ctx.lineTo(px(i), py(i));
      ctx.strokeStyle = ln.a ? `rgba(${ACCENT},0.95)` : `rgba(${FAINT},0.15)`;
      ctx.lineWidth = (ln.a ? 3 : 1.4) * dpr; ctx.stroke();
      if (ln.a) {
        const x = px(N - 1), y = py(N - 1);
        ctx.fillStyle = `rgba(${ACCENT},1)`; ctx.beginPath(); ctx.arc(x, y, 6 * dpr, 0, 7); ctx.fill();
        ctx.strokeStyle = `rgba(${ACCENT},0.35)`; ctx.lineWidth = 1.5 * dpr; ctx.beginPath(); ctx.arc(x, y, 13 * dpr, 0, 7); ctx.stroke();
      }
    }
  }
  function drawAll() { document.querySelectorAll("canvas[data-field]").forEach(draw); }
  // initial (deck-stage scales after define) + on resize + on slide change
  const kick = () => requestAnimationFrame(() => setTimeout(drawAll, 60));
  if (document.readyState !== "loading") kick(); else addEventListener("DOMContentLoaded", kick);
  addEventListener("resize", drawAll);
  const stage = document.querySelector("deck-stage");
  if (stage) stage.addEventListener("slidechange", kick);
  setTimeout(drawAll, 400);
})();
