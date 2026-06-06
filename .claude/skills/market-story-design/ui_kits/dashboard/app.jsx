/* Market Story dashboard — bundled component source.
   Concatenated from components / charts / panels / story for reliable single-fetch
   loading (Babel-in-browser XHR was flaky across many files). Edit sections here. */


/* ============================================================
   components.jsx
   ============================================================ */
/* Market Story dashboard — shell components (sidebar, header, KPI strip, read hero, tabs). */
const { useState } = React;

const TONE = { up:"up", down:"down", warn:"warn", neutral:"neutral" };

// tiny sparkline drawn from normalized 0..1 points
function Sparkline({ points, up, big }) {
  const w = 120, h = big ? 64 : 40, pad = 3;
  const n = points.length;
  const px = i => pad + (i / (n - 1)) * (w - pad * 2);
  const py = v => pad + (1 - v) * (h - pad * 2);
  const line = points.map((v, i) => `${i ? "L" : "M"}${px(i).toFixed(1)},${py(v).toFixed(1)}`).join(" ");
  const area = `${line} L${px(n-1).toFixed(1)},${h-pad} L${px(0).toFixed(1)},${h-pad} Z`;
  const c = up ? "var(--up)" : "var(--down)";
  const gid = "g" + Math.random().toString(36).slice(2, 8);
  const lx = px(n - 1), ly = py(points[n - 1]);
  return (
    <svg className="spark" viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" style={{ width:"100%", height:h }}>
      <defs><linearGradient id={gid} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor={c} stopOpacity="0.18" /><stop offset="1" stopColor={c} stopOpacity="0" />
      </linearGradient></defs>
      <path d={area} fill={`url(#${gid})`} />
      <path d={line} fill="none" stroke={c} strokeWidth={big ? 1.8 : 1.4} strokeLinejoin="round" strokeLinecap="round" />
      {big && <circle cx={lx} cy={ly} r="2.6" fill={c} vectorEffect="non-scaling-stroke" />}
    </svg>
  );
}

function Sidebar({ page, setPage, onRefresh, refreshing, ambient, setAmbient }) {
  const icons = {
    show_chart: (
      <svg className="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.1" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <path d="M3.5 16.5 L9 11 L13 14 L20.5 6.5" />
        <path d="M16 6.5 H20.5 V11" />
      </svg>
    ),
    school: (
      <svg className="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <path d="M2.5 9 L12 4.5 L21.5 9 L12 13.5 Z" />
        <path d="M6.5 11.2 V16 C6.5 16 8.7 18 12 18 C15.3 18 17.5 16 17.5 16 V11.2" />
        <path d="M21.5 9 V14.5" />
      </svg>
    ),
  };
  const nav = [
    { id:"brief", label:"Daily Brief", ico:"show_chart" },
    { id:"learn", label:"Learn the Markets", ico:"school" },
  ];
  const levels = [["off","Off"], ["low","Low"], ["high","High"]];
  return (
    <aside className="sidebar">
      <div className="sb-title">Market Story</div>
      <nav aria-label="Primary">
        {nav.map(n => (
          <button key={n.id} type="button" className={"nav-item" + (page === n.id ? " active" : "")}
            aria-current={page === n.id ? "page" : undefined} onClick={() => setPage(n.id)}>
            {icons[n.ico]}
            {n.label}
            <span className="navx" aria-hidden="true">→</span>
          </button>
        ))}
      </nav>
      <div className="sb-sep"></div>
      <button className="btn" type="button" onClick={onRefresh} aria-busy={refreshing}>
        {refreshing ? "Refreshing…" : "Refresh data"}
      </button>
      <div className="amb">
        <div className="aml">Ambient field</div>
        <div className="seg" role="group" aria-label="Ambient field intensity">
          {levels.map(([v, lbl]) => (
            <button key={v} type="button" aria-pressed={ambient === v} onClick={() => setAmbient(v)}>{lbl}</button>
          ))}
        </div>
      </div>
      <div className="sb-cap" style={{ marginTop:14 }}>Scope: US equities &amp; sectors + global macro</div>
      <div className="sb-cap">Sources: yfinance · FRED · 12 RSS feeds</div>
      <div style={{ flex:1 }}></div>
      <div className="sb-cap" style={{ fontFamily:"var(--mono)", opacity:.7 }}>Python · Streamlit · Claude</div>
    </aside>
  );
}

function Header({ d }) {
  return (
    <div className="hd">
      <h1>Global Markets Brief</h1>
      <div className="meta">{d.session_label}  ·  generated {d.generated_at} UTC</div>
    </div>
  );
}

function MetricCard({ k, loading }) {
  const [open, setOpen] = React.useState(false);
  return (
    <div className={"metric" + (loading ? " is-loading" : "")}
      tabIndex={0} role="button" aria-expanded={open}
      aria-label={k.label + " " + k.val + " " + k.delta + " — show intraday"}
      onMouseEnter={() => setOpen(true)} onMouseLeave={() => setOpen(false)}
      onFocus={() => setOpen(true)} onBlur={() => setOpen(false)}>
      <div className="label">{k.label}</div>
      <div className="val">{k.val}</div>
      <div className={"delta " + TONE[k.tone]}>{k.delta}</div>
      {open && !loading && (
        <div className="metric-pop" role="tooltip">
          <div className="mp-head">
            <span>{k.label} · intraday</span>
            <span className={"mono " + TONE[k.tone]}>{k.delta}</span>
          </div>
          <Sparkline points={k.spark} up={k.sparkUp} big />
          <div className="mp-foot mono">
            <span>O {k.val}</span><span className="dim">range shown · 1D</span>
          </div>
        </div>
      )}
    </div>
  );
}

function KpiStrip({ d, loading }) {
  return (
    <React.Fragment>
      <div className="kpis">
        {d.kpis.map(k => <MetricCard key={k.sym} k={k} loading={loading} />)}
      </div>
      <div className="sparks" aria-hidden="true">
        {d.kpis.map(k => <Sparkline key={k.sym} points={k.spark} up={k.sparkUp} />)}
      </div>
      <div className="breadth">
        Sector breadth: <span className="up">{d.stats.sector_advancers} up</span> / <span className="down">{d.stats.sector_decliners} down</span> of {d.stats.sector_count}
      </div>
    </React.Fragment>
  );
}

function ReadHero({ d, onStory }) {
  return (
    <div className="hero">
      <div className="kick">● Today's thesis</div>
      <div className="read">{d.read}</div>
      <div className="more">Full read in the <b style={{ color:"var(--text)" }}>Story</b> tab → <a href="#" onClick={e => { e.preventDefault(); onStory && onStory(); }} style={{ marginLeft:4 }}>open</a></div>
    </div>
  );
}

function Signals({ d }) {
  return (
    <React.Fragment>
      <h2 className="subhead" style={{ marginTop:18 }}>⚡ Today's signal</h2>
      <div className="sigwrap">
        {d.signals.map((s, i) => (
          <div className="sig" key={i}><span className={"dot " + TONE[s.tone]}>●</span>{s.text}</div>
        ))}
      </div>
    </React.Fragment>
  );
}

function Tabs({ tabs, active, setActive }) {
  const onKey = (e) => {
    const i = tabs.indexOf(active);
    let n = null;
    if (e.key === "ArrowRight" || e.key === "ArrowDown") n = (i + 1) % tabs.length;
    else if (e.key === "ArrowLeft" || e.key === "ArrowUp") n = (i - 1 + tabs.length) % tabs.length;
    else if (e.key === "Home") n = 0;
    else if (e.key === "End") n = tabs.length - 1;
    if (n !== null) { e.preventDefault(); setActive(tabs[n]); }
  };
  const slug = t => "tab-" + t.replace(/[^a-z]+/gi, "-").toLowerCase();
  return (
    <div className="tabs" role="tablist" aria-label="Brief sections" onKeyDown={onKey}>
      {tabs.map(t => {
        const on = t === active;
        return (
          <button key={t} id={slug(t)} role="tab" type="button"
            aria-selected={on} aria-controls="tabpane" tabIndex={on ? 0 : -1}
            className={"tab" + (on ? " active" : "")} onClick={() => setActive(t)}>{t}</button>
        );
      })}
    </div>
  );
}

// dismissible freshness notice — authentic to the product's data caveat
function Notice({ children, onClose }) {
  return (
    <div className="notice" role="status">
      <span className="ndot" aria-hidden="true">●</span>
      <span>{children}</span>
      <button className="nx" type="button" aria-label="Dismiss notice" onClick={onClose}>✕</button>
    </div>
  );
}

// data-load error guard (shown if MS_DATA is missing)
function ErrorBox({ onRetry }) {
  return (
    <div className="errorbox" role="alert">
      <div className="eg" aria-hidden="true">⚠</div>
      <div className="et">Couldn't load today's brief</div>
      <div className="es">The data feed didn't return. Markets data is best-effort from free sources — try again in a moment.</div>
      <button className="btn" type="button" onClick={onRetry}>Retry</button>
    </div>
  );
}

// scroll-reveal wrapper — base state is visible (added by JS), so content never
// hides if scripts fail. Adds `.reveal` on mount, then `.in` when scrolled into view.
function Reveal({ children, className, style }) {
  const ref = React.useRef(null);
  React.useEffect(() => {
    const el = ref.current; if (!el) return;
    el.classList.add("reveal");
    const show = () => el.classList.add("in");
    // above-the-fold → reveal now (gentle fade); below-fold → on scroll; always a safety net
    const r = el.getBoundingClientRect();
    if (r.top < (window.innerHeight || 800) * 0.92) { requestAnimationFrame(show); return; }
    let io;
    try {
      io = new IntersectionObserver((entries) => {
        entries.forEach(e => { if (e.isIntersecting) { show(); io.unobserve(el); } });
      }, { threshold: 0.08, rootMargin: "0px 0px -6% 0px" });
      io.observe(el);
    } catch (_) { show(); }
    const t = setTimeout(show, 2500);
    return () => { if (io) io.disconnect(); clearTimeout(t); };
  }, []);
  return <div ref={ref} className={className} style={style}>{children}</div>;
}

// The cover — the landing folded into the product. Same warm palette + cyan field.
function Cover({ d, out, onEnter, ambient, accentRGB, faintRGB }) {
  const cv = React.useRef(null);
  const btn = React.useRef(null);
  React.useEffect(() => {
    if (!cv.current || !window.startMarketField) return;
    const f = window.startMarketField(cv.current, { topFrac: 0.5, botFrac: 0.13, parallax: 48, intensity: ambient, accentRGB: accentRGB, faintRGB: faintRGB });
    return () => f.destroy();
  }, []);
  React.useEffect(() => {
    const t = setTimeout(() => { try { btn.current && btn.current.focus(); } catch (_) {} }, 200);
    const onKey = (e) => { if (e.key === "Enter" && document.activeElement !== btn.current) onEnter(); };
    window.addEventListener("keydown", onKey);
    return () => { clearTimeout(t); window.removeEventListener("keydown", onKey); };
  }, []);
  const tape = [
    ["S&P 500", d.kpis[0].val, d.kpis[0].delta, d.kpis[0].tone],
    ["VIX", "16.50", "+2.8%", "down"],
    ["US 10Y", "4.491%", "yield", ""],
    ["Sector breadth", "4 / 7", "up / down", ""],
  ];
  return (
    <div className={"cover" + (out ? " gone" : "")} role="region" aria-label="Market Story — cover" aria-hidden={out}>
      <canvas ref={cv} aria-hidden="true"></canvas>
      <div className="cscrim"></div>
      <div className="cwrap">
        <div className="ctop">
          <span className="brand">MARKET STORY<sup>®</sup></span>
          <span className="mid">Daily global-markets intelligence</span>
          <span>{d.date}</span>
        </div>
        <div className="chero">
          <div className="ckick">№ {d.date.replace(/-/g, "")} — Markets, narrated.</div>
          <h1 className="cword">Market<br />Story<sup>®</sup></h1>
          <div className="csub">
            <p className="ctag">A daily global brief with a risk lens — gathered, synthesized by Claude, and built to be questioned and re-run.</p>
            <div>
              <button className="center" type="button" ref={btn} onClick={onEnter}>Enter the brief <span className="ar" aria-hidden="true">→</span></button>
              <div className="chint">Press <kbd>Enter ↵</kbd> to open the brief</div>
            </div>
          </div>
        </div>
        <div className="ctape">
          {tape.map((t, i) => (
            <div className="ctk" key={i}><span className="k">{t[0]}</span><span className="v">{t[1]}</span><span className={"d " + (TONE[t[3]] || "")}>{t[2]}</span></div>
          ))}
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { Sparkline, Sidebar, Header, KpiStrip, ReadHero, Signals, Tabs, Notice, ErrorBox, Reveal, Cover, TONE });


/* ============================================================
   charts.jsx
   ============================================================ */
/* Market Story dashboard — real data-viz: squarified sector treemap, the
   cyan-anchored cross-asset correlation matrix, the Treasury yield curve, and a
   layered Sankey for the Learn page. Plain SVG/divs, on-palette. */

// on-palette diverging color: red <- warm-dark -> cyan/green
function _mix(a, b, t) { return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(",")})`; }
const _DARK = [27, 22, 17], _CYAN = [123, 234, 251], _GREEN = [54, 194, 111], _RED = [255, 92, 108];
function diffColor(v, span, pole) {           // pole: 'green' (treemap) or 'cyan' (corr)
  const t = Math.max(-1, Math.min(1, v / span));
  const up = pole === "cyan" ? _CYAN : _GREEN;
  return t >= 0 ? _mix(_DARK, up, t) : _mix(_DARK, _RED, -t);
}

/* ---- Squarified treemap (sized by index weight, colored by 1-day change) ---- */
const SECTOR_WEIGHT = {
  Technology: 32, Financials: 13, Health: 11, Discretionary: 10.5, "Comm Svcs": 9,
  Industrials: 8, Staples: 6, Energy: 4, Utilities: 2.6, "Real Estate": 2.2, Materials: 2.0,
};
function squarify(items, W, H) {
  const nodes = items.map(d => ({ ...d }));
  const total = nodes.reduce((s, n) => s + n.value, 0) || 1;
  nodes.forEach(n => (n.area = (n.value / total) * W * H));
  const out = [];
  let x = 0, y = 0, w = W, h = H, row = [];
  const remaining = nodes.slice();
  const worst = (r, side) => {
    let sum = 0, mx = -Infinity, mn = Infinity;
    for (const n of r) { sum += n.area; if (n.area > mx) mx = n.area; if (n.area < mn) mn = n.area; }
    const s2 = sum * sum, d2 = side * side;
    return Math.max((d2 * mx) / s2, s2 / (d2 * mn));
  };
  const flush = (r, side, horiz) => {
    const sum = r.reduce((a, n) => a + n.area, 0);
    const thick = sum / side; let pos = horiz ? y : x;
    for (const n of r) {
      const len = n.area / thick;
      out.push({ ...n, x: horiz ? x : pos, y: horiz ? pos : y, w: horiz ? thick : len, h: horiz ? len : thick });
      pos += len;
    }
    if (horiz) { x += thick; w -= thick; } else { y += thick; h -= thick; }
  };
  while (remaining.length) {
    const horiz = w < h, side = horiz ? h : w;
    if (!row.length) { row.push(remaining.shift()); continue; }
    if (worst([...row, remaining[0]], side) <= worst(row, side)) row.push(remaining.shift());
    else { flush(row, side, horiz); row = []; }
  }
  if (row.length) { const horiz = w < h; flush(row, horiz ? h : w, horiz); }
  return out;
}
function SectorTreemap({ sectors }) {
  const W = 1040, H = 380;
  const items = sectors.map(s => ({ name: s.name, chg: s.chg, value: SECTOR_WEIGHT[s.name] || 3 }));
  const tiles = squarify(items, W, H);
  return (
    <div style={{ position: "relative", width: "100%", height: 380, borderRadius: 10, overflow: "hidden" }}>
      {tiles.map((t, i) => {
        const big = t.w > 110 && t.h > 54;
        return (
          <div key={i} style={{
            position: "absolute", left: `${(t.x / W) * 100}%`, top: `${(t.y / H) * 100}%`,
            width: `${(t.w / W) * 100}%`, height: `${(t.h / H) * 100}%`, padding: big ? "10px 12px" : "5px 7px",
            background: diffColor(t.chg, 2.5, "green"), border: "1px solid rgba(13,12,12,.55)",
            display: "flex", flexDirection: "column", justifyContent: "space-between", overflow: "hidden",
          }}>
            <div style={{ fontFamily: "var(--grot)", fontWeight: 600, fontSize: big ? ".82rem" : ".64rem", color: "var(--text)", lineHeight: 1.1 }}>{t.name}</div>
            <div style={{ fontFamily: "var(--mono)", fontSize: big ? ".84rem" : ".62rem", color: t.chg >= 0 ? "var(--up)" : "var(--down)" }}>{t.chg >= 0 ? "+" : ""}{t.chg.toFixed(2)}%</div>
          </div>
        );
      })}
    </div>
  );
}

/* ---- Cross-asset correlation matrix (cyan-anchored: +1 cyan, 0 dark, -1 red) ---- */
const CORR_LABELS = ["S&P", "Nasdaq", "Russell", "10Y", "Dollar", "Gold", "WTI", "HY", "VIX"];
const CORR = [
  [1.00, 0.96, 0.88, -0.42, -0.31, 0.12, 0.18, 0.74, -0.82],
  [0.96, 1.00, 0.82, -0.38, -0.29, 0.08, 0.14, 0.69, -0.79],
  [0.88, 0.82, 1.00, -0.46, -0.22, 0.18, 0.24, 0.71, -0.71],
  [-0.42, -0.38, -0.46, 1.00, 0.54, -0.28, 0.16, -0.34, 0.30],
  [-0.31, -0.29, -0.22, 0.54, 1.00, -0.61, -0.18, -0.26, 0.22],
  [0.12, 0.08, 0.18, -0.28, -0.61, 1.00, 0.34, 0.10, 0.08],
  [0.18, 0.14, 0.24, 0.16, -0.18, 0.34, 1.00, 0.22, -0.12],
  [0.74, 0.69, 0.71, -0.34, -0.26, 0.10, 0.22, 1.00, -0.58],
  [-0.82, -0.79, -0.71, 0.30, 0.22, 0.08, -0.12, -0.58, 1.00],
];
function CorrMatrix() {
  const n = CORR_LABELS.length;
  return (
    <div className="chart">
      <div className="ct">Cross-asset return correlation · last 60 sessions</div>
      <div style={{ display: "grid", gridTemplateColumns: `60px repeat(${n}, 1fr)`, gap: 2, marginTop: 8 }}>
        <div></div>
        {CORR_LABELS.map(l => <div key={l} style={{ fontFamily: "var(--mono)", fontSize: ".6rem", color: "var(--text-dim)", textAlign: "center", paddingBottom: 4 }}>{l}</div>)}
        {CORR.map((row, r) => (
          <React.Fragment key={r}>
            <div style={{ fontFamily: "var(--mono)", fontSize: ".62rem", color: "var(--text-dim)", display: "flex", alignItems: "center", justifyContent: "flex-end", paddingRight: 6 }}>{CORR_LABELS[r]}</div>
            {row.map((v, c) => (
              <div key={c} title={`${CORR_LABELS[r]}·${CORR_LABELS[c]} ${v.toFixed(2)}`} style={{
                background: diffColor(v, 1, "cyan"), aspectRatio: "1 / 1", borderRadius: 3,
                display: "flex", alignItems: "center", justifyContent: "center",
                fontFamily: "var(--mono)", fontSize: ".58rem",
                color: Math.abs(v) > 0.55 ? "rgba(13,12,12,.9)" : "rgba(245,242,239,.62)",
              }}>{v.toFixed(2)}</div>
            ))}
          </React.Fragment>
        ))}
      </div>
      <div className="tcap" style={{ marginTop: 8 }}>Watch for regime shifts — stock–bond decoupling, or everything → +1 in a selloff. S&amp;P–HY at <b style={{ color: "var(--text)" }}>+0.74</b>; S&amp;P–VIX at <b style={{ color: "var(--text)" }}>−0.82</b>.</div>
    </div>
  );
}

/* ---- US Treasury yield curve ---- */
function YieldCurve({ rates }) {
  const mat = { "13-week": 0.25, "5-year": 5, "10-year": 10, "30-year": 30 };
  const lab = { "13-week": "13W", "5-year": "5Y", "10-year": "10Y", "30-year": "30Y" };
  const pts = rates.filter(r => mat[r.name] != null).map(r => ({ x: mat[r.name], y: parseFloat(r.last), l: lab[r.name] })).sort((a, b) => a.x - b.x);
  const W = 520, H = 240, pad = 38;
  const xs = pts.map(p => p.x), ys = pts.map(p => p.y);
  const xmin = 0, xmax = 30, ymin = Math.min(...ys) - 0.15, ymax = Math.max(...ys) + 0.15;
  const px = x => pad + (x - xmin) / (xmax - xmin) * (W - pad * 1.4);
  const py = y => H - pad - (y - ymin) / (ymax - ymin) * (H - pad * 1.6);
  const line = pts.map((p, i) => `${i ? "L" : "M"}${px(p.x).toFixed(1)},${py(p.y).toFixed(1)}`).join(" ");
  const ticks = [ymin, (ymin + ymax) / 2, ymax];
  return (
    <div className="chart">
      <div className="ct">US Treasury yield curve</div>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", height: 240 }}>
        {ticks.map((t, i) => (
          <g key={i}>
            <line x1={pad} x2={W - 8} y1={py(t)} y2={py(t)} stroke="var(--grid)" strokeWidth="1" />
            <text x={6} y={py(t) + 3} fontFamily="var(--mono)" fontSize="10" fill="var(--text-dim)">{t.toFixed(2)}</text>
          </g>
        ))}
        <path d={line} fill="none" stroke="var(--accent)" strokeWidth="2" strokeLinejoin="round" />
        {pts.map((p, i) => (
          <g key={i}>
            <circle cx={px(p.x)} cy={py(p.y)} r="3.5" fill="var(--accent)" />
            <text x={px(p.x)} y={py(p.y) - 9} textAnchor="middle" fontFamily="var(--mono)" fontSize="10" fill="var(--text)">{p.l}</text>
            <text x={px(p.x)} y={H - 14} textAnchor="middle" fontFamily="var(--mono)" fontSize="9.5" fill="var(--text-dim)">{p.y.toFixed(2)}%</text>
          </g>
        ))}
      </svg>
      <div className="tcap">2s10s pinned at <b style={{ color: "var(--text)" }}>0.41%</b> — flattest of the year (0th %ile). The curve isn't steepening.</div>
    </div>
  );
}

/* ---- Layered Sankey (money flow) ---- */
function Sankey({ data, height = 360 }) {
  const W = 900, H = height, pad = 6;
  const layers = {};
  data.nodes.forEach(n => { (layers[n.layer] = layers[n.layer] || []).push(n); });
  const layerKeys = Object.keys(layers).map(Number).sort((a, b) => a - b);
  const colX = l => pad + (l / (layerKeys.length - 1)) * (W - pad * 2 - 120) + 60;
  const nodeW = 13, gap = 16;
  const byId = {};
  // node value = max(in,out)
  data.nodes.forEach(n => { n.in = 0; n.out = 0; });
  data.links.forEach(k => { const s = data.nodes.find(n => n.id === k.source), t = data.nodes.find(n => n.id === k.target); if (s) s.out += k.value; if (t) t.in += k.value; });
  layerKeys.forEach(lk => {
    const ns = layers[lk];
    const totalVal = ns.reduce((a, n) => a + Math.max(n.in, n.out), 0);
    const avail = H - pad * 2 - gap * (ns.length - 1);
    let yy = pad;
    ns.forEach(n => {
      const hh = Math.max(8, (Math.max(n.in, n.out) / totalVal) * avail);
      n._x = colX(lk); n._y = yy; n._h = hh; n._so = 0; n._to = 0;
      byId[n.id] = n; yy += hh + gap;
    });
  });
  const ribbons = data.links.map((k, i) => {
    const s = byId[k.source], t = byId[k.target];
    const sy = s._y + s._so + k.value / Math.max(s.in, s.out) * s._h / 2;
    const ty = t._y + t._to + k.value / Math.max(t.in, t.out) * t._h / 2;
    const th = k.value / Math.max(s.in, s.out) * s._h;
    s._so += k.value / Math.max(s.in, s.out) * s._h;
    t._to += k.value / Math.max(t.in, t.out) * t._h;
    const x0 = s._x + nodeW, x1 = t._x, mx = (x0 + x1) / 2;
    return <path key={i} d={`M${x0},${sy} C${mx},${sy} ${mx},${ty} ${x1},${ty}`} fill="none" stroke="rgba(123,234,251,0.28)" strokeWidth={Math.max(1, th)} />;
  });
  return (
    <div className="chart">
      <div className="ct">{data.title}</div>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", height }}>
        {ribbons}
        {data.nodes.map((n, i) => (
          <g key={i}>
            <rect x={n._x} y={n._y} width={nodeW} height={n._h} rx="2" fill="var(--accent)" opacity="0.92" />
            <text x={n.layer === layerKeys[layerKeys.length - 1] ? n._x - 6 : n._x + nodeW + 6}
              y={n._y + n._h / 2 + 3} textAnchor={n.layer === layerKeys[layerKeys.length - 1] ? "end" : "start"}
              fontFamily="var(--grot)" fontWeight="600" fontSize="11.5" fill="var(--text)">{n.label}</text>
          </g>
        ))}
      </svg>
    </div>
  );
}

Object.assign(window, { SectorTreemap, CorrMatrix, YieldCurve, Sankey, diffColor });


/* ============================================================
   panels.jsx
   ============================================================ */
/* Market Story dashboard — tab panels (data tables, treemap, story, etc.) */

function DataTable({ title, rows, kind, caption, heat }) {
  const cls = (t) => "td " + (window.TONE[t] || "");
  const head = kind === "yield"
    ? ["Instrument","Last","1D bps","1W %","YTD %"]
    : ["Instrument","Last","1D %","1W %","YTD %"];
  const heatBg = (t) => {
    if (!heat) return undefined;
    if (t === "up") return "linear-gradient(90deg, rgba(54,194,111,.13), transparent 60%)";
    if (t === "down") return "linear-gradient(90deg, rgba(255,92,108,.13), transparent 60%)";
    return undefined;
  };
  return (
    <div>
      {title && <h3 className="subhead">{title}</h3>}
      <table className={"tbl" + (heat ? " heat" : "")}>
        <thead><tr>{head.map(h => <th key={h} className={heat && h.startsWith("1D") ? "th-hi" : undefined}>{h}</th>)}</tr></thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i} style={{ background: heatBg(r.t1) }}>
              <td>{r.name}</td>
              <td>{r.last}</td>
              <td className={window.TONE[r.t1]} style={heat ? { fontWeight: 600 } : undefined}>{r.d1}</td>
              <td className={window.TONE[r.tw]}>{r.w1}</td>
              <td className={window.TONE[r.ty]}>{r.ytd}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {caption && <div className="tcap">{caption}</div>}
    </div>
  );
}

// toggle control reused above table pairs
function DiffToggle({ on, set }) {
  return (
    <button type="button" className={"difftoggle" + (on ? " on" : "")} aria-pressed={on} onClick={() => set(!on)}>
      <span className="dt-dot" aria-hidden="true"></span>
      Highlight day change
    </button>
  );
}

// (Sector treemap, correlation matrix & yield curve now live in charts.jsx)

function Movers({ d }) {
  return (
    <div className="two">
      <div>
        <h3 className="subhead">Leaders</h3>
        {d.leaders.map((m,i) => (
          <div className="mover" key={i}><span className="mn">{m.name}</span><span className={"mc " + window.TONE[m.tone]}>{m.chg}</span></div>
        ))}
      </div>
      <div>
        <h3 className="subhead">Laggards</h3>
        {d.laggards.map((m,i) => (
          <div className="mover" key={i}><span className="mn">{m.name}</span><span className={"mc " + window.TONE[m.tone]}>{m.chg}</span></div>
        ))}
      </div>
    </div>
  );
}

// a simple area line chart for "S&P 500"
function BigChart({ title }) {
  const pts = [.30,.42,.38,.50,.46,.40,.55,.62,.58,.70,.66,.74,.69,.80,.76,.85];
  const w=900,h=300,pad=10;
  const px=i=>pad+(i/(pts.length-1))*(w-pad*2), py=v=>pad+(1-v)*(h-pad*2);
  const line=pts.map((v,i)=>`${i?"L":"M"}${px(i).toFixed(1)},${py(v).toFixed(1)}`).join(" ");
  const area=`${line} L${px(pts.length-1)},${h-pad} L${px(0)},${h-pad} Z`;
  return (
    <div className="chart">
      <div className="ct">{title}</div>
      <svg viewBox={`0 0 ${w} ${h}`} style={{ width:"100%", height:300 }} preserveAspectRatio="none">
        {[0,.25,.5,.75,1].map(g => <line key={g} x1={pad} x2={w-pad} y1={pad+g*(h-pad*2)} y2={pad+g*(h-pad*2)} stroke="var(--grid)" strokeWidth="1" />)}
        <defs><linearGradient id="bigfill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="var(--accent)" stopOpacity=".10"/><stop offset="1" stopColor="var(--accent)" stopOpacity="0"/></linearGradient></defs>
        <path d={area} fill="url(#bigfill)" />
        <path d={line} fill="none" stroke="var(--accent)" strokeWidth="2" strokeLinejoin="round" />
      </svg>
    </div>
  );
}

function OverviewTab({ d, onStory }) {
  const Reveal = window.Reveal;
  return (
    <div>
      <ReadHero d={d} onStory={onStory} />
      <Signals d={d} />
      <hr className="hr" />
      <Reveal><Movers d={d} /></Reveal>
      <Reveal><BigChart title="S&P 500" /></Reveal>
    </div>
  );
}

function EquitiesTab({ d }) {
  const [heat, setHeat] = React.useState(false);
  return (
    <div>
      <h2 className="h2">Sector map · 1-day % change</h2>
      <SectorTreemap sectors={d.sectors} />
      <div className="tcap" style={{ marginTop: 8 }}>Tile size = index weight · color = 1-day move (on-palette diverging: red → warm-dark → green).</div>
      <hr className="hr" />
      <div className="tbl-bar">
        <span className="subhead" style={{ margin: 0 }}>Cross-asset tables</span>
        <DiffToggle on={heat} set={setHeat} />
      </div>
      <div className="two">
        <DataTable title="US Equities" rows={d.us_equities} caption="% changes; VIX delta inverts" heat={heat} />
        <div>
          <DataTable title="Commodities" rows={d.commodities} caption="WTI broke its floor overnight" heat={heat} />
        </div>
      </div>
    </div>
  );
}

function MacroTab({ d }) {
  return (
    <div>
      <h3 className="subhead">Risk regime — mixed, late-cycle</h3>
      <div className="regime">
        {d.regime.map((r,i) => (
          <div className="rcell" key={i}><div className="rl">{r.label}</div><div className={"rv " + window.TONE[r.t]}>{r.val}</div></div>
        ))}
      </div>
      <hr className="hr" />
      <div className="two">
        <DataTable title="Global Indices" rows={d.global_indices} />
        <DataTable title="Rates (Treasury yields)" rows={d.rates} kind="yield" caption="Last in %, 1D in bps" />
      </div>
      <hr className="hr" />
      <div className="two">
        <DataTable title="FX" rows={d.fx} />
        <DataTable title="Credit & Bonds" rows={d.credit} />
      </div>
      <hr className="hr" />
      <h3 className="subhead">Macro (FRED) · 1-year percentile</h3>
      <table className="tbl">
        <thead><tr><th>Series</th><th>Latest</th><th>Δ</th><th>1y %ile</th></tr></thead>
        <tbody>
          {d.macro.map((m,i) => (
            <tr key={i}><td>{m.name}</td><td>{m.latest}</td><td className={window.TONE[m.t]}>{m.chg}</td><td className="neutral">{m.pct}</td></tr>
          ))}
        </tbody>
      </table>
      <div className="tcap">Vol risk premium: VIX 16.5 vs 9.9 realized (20d) = +6.6 pts (rich — complacency / cheap-looking hedges).</div>
      <hr className="hr" />
      <div className="two">
        <YieldCurve rates={d.rates} />
        <CorrMatrix />
      </div>
    </div>
  );
}

function TrendsTab({ d }) {
  const metrics = [
    { t:"10Y Treasury yield (%)", v:"4.49", pct:"96", up:true },
    { t:"2s10s curve (pp)", v:"0.41", pct:"0", up:false },
    { t:"HY credit spread (%)", v:"2.71", pct:"3", up:false },
    { t:"VIX", v:"16.5", pct:"34", up:false },
  ];
  const paths = [
    [.5,.45,.4,.5,.55,.6,.66,.7,.74,.8],
    [.8,.7,.62,.5,.42,.35,.28,.2,.14,.08],
    [.7,.6,.5,.4,.32,.25,.18,.12,.08,.05],
    [.4,.5,.45,.6,.55,.7,.5,.6,.45,.5],
  ];
  return (
    <div>
      <div className="tcap" style={{ marginBottom:16 }}>847 sessions · 2022-11-01 → 2026-06-04 — each anchor's path, with today's percentile over the whole window. Faint red = crisis eras.</div>
      <div className="two">
        {metrics.map((m,i) => (
          <div key={i} style={{ marginBottom:18 }}>
            <div style={{ fontWeight:600, fontSize:".92rem", marginBottom:8 }}>{m.t} — <span className="mono" style={{ fontFamily:"var(--mono)" }}>{m.v}</span> · {m.pct}th %ile</div>
            <MiniTrend points={paths[i]} />
          </div>
        ))}
      </div>
    </div>
  );
}
function MiniTrend({ points }) {
  const w=420,h=140,pad=6;
  const px=i=>pad+(i/(points.length-1))*(w-pad*2), py=v=>pad+(1-v)*(h-pad*2);
  const line=points.map((v,i)=>`${i?"L":"M"}${px(i).toFixed(1)},${py(v).toFixed(1)}`).join(" ");
  const area=`${line} L${px(points.length-1)},${h-pad} L${px(0)},${h-pad} Z`;
  const last=points[points.length-1];
  return (
    <svg viewBox={`0 0 ${w} ${h}`} style={{ width:"100%", height:140, background:"var(--surface)", border:"1px solid var(--border)", borderRadius:10 }} preserveAspectRatio="none">
      <defs><linearGradient id={"mt"+points[0]} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="var(--accent)" stopOpacity=".10"/><stop offset="1" stopColor="var(--accent)" stopOpacity="0"/></linearGradient></defs>
      <path d={area} fill={`url(#mt${points[0]})`} />
      <path d={line} fill="none" stroke="var(--accent)" strokeWidth="1.6" strokeLinejoin="round" />
      <line x1={pad} x2={w-pad} y1={py(last)} y2={py(last)} stroke="var(--down)" strokeWidth="1" strokeDasharray="3 3" opacity=".45" />
      <circle cx={px(points.length-1)} cy={py(last)} r="3.5" fill="var(--down)" />
    </svg>
  );
}

function HeadlinesTab({ d }) {
  const [q, setQ] = useState("");
  const items = d.news.filter(n => !q.trim() || (n.t + n.s).toLowerCase().includes(q.toLowerCase()));
  return (
    <div>
      <label htmlFor="hfilter" className="sr-only">Filter headlines</label>
      <input id="hfilter" className="field" type="search" placeholder="Filter headlines — e.g. Fed, oil, NVDA…" value={q} onChange={e => setQ(e.target.value)} />
      <div className="tcap" style={{ marginBottom:10 }} role="status" aria-live="polite">{items.length} {q.trim() ? `of ${d.news.length} matching “${q.trim()}”` : "headlines across 12 feeds"}</div>
      {items.length === 0 ? (
        <div className="empty">
          <div className="eg" aria-hidden="true">⌕</div>
          <div className="et">No headlines match “{q.trim()}”</div>
          <div className="es">Try a ticker (NVDA), an asset (oil, gold), or a theme (Fed, credit).</div>
          <button className="btn-ghost" type="button" onClick={() => setQ("")}>Clear filter</button>
        </div>
      ) : (
        <div className="news">
          {items.map((n,i) => (
            <div className="newsitem" key={i}><div className="nt">{n.t}</div><div className="nm">{n.s} · {n.d}</div></div>
          ))}
        </div>
      )}
    </div>
  );
}

function CalendarTab({ d }) {
  const econ = [
    { name:"May Nonfarm Payrolls", date:"2026-06-05", in:"tomorrow ⚠️" },
    { name:"CPI (May)", date:"2026-06-11", in:"7 days" },
    { name:"FOMC decision", date:"2026-06-17", in:"13 days" },
    { name:"Core PCE (May)", date:"2026-06-26", in:"22 days" },
  ];
  const extremes = d.extremes;
  return (
    <div>
      <h3 className="subhead">Economic releases — the data the market trades around</h3>
      <table className="tbl">
        <thead><tr><th>Release</th><th>Date</th><th>In</th></tr></thead>
        <tbody>{econ.map((e,i) => (
          <tr key={i}><td>{e.name}</td><td>{e.date}</td><td className={e.in.includes("⚠️") ? "warn" : "neutral"}>{e.in}</td></tr>
        ))}</tbody>
      </table>
      <hr className="hr" />
      <h3 className="subhead">Cross-asset extremes — where key markets sit in their ~1y range</h3>
      <table className="tbl">
        <thead><tr><th>Anchor</th><th>Last</th><th>1y %ile</th><th>z</th></tr></thead>
        <tbody>{extremes.map((e,i) => (
          <tr key={i}><td>{e.name}</td><td>{e.last}</td><td className="neutral">{e.pct}</td><td className={window.TONE[e.t]}>{e.z}</td></tr>
        ))}</tbody>
      </table>
    </div>
  );
}

Object.assign(window, { DataTable, Movers, BigChart, OverviewTab, EquitiesTab, MacroTab, TrendsTab, HeadlinesTab, CalendarTab });


/* ============================================================
   story.jsx
   ============================================================ */
/* Market Story dashboard — the Story tab (the written read). */
function StoryTab() {
  const grades = [
    { s: "miss", claim: "WTI holds $95 — the oil bid is intact", metric: "CL=F", trig: "> 95", now: "92.44" },
    { s: "watch", claim: "HY OAS widens → credit de-risking", metric: "BAMLH0A0HYM2", trig: "> 2.85", now: "2.71" },
    { s: "watch", claim: "10Y makes a decisive break above 4.5%", metric: "DGS10", trig: "> 4.5", now: "4.49" },
    { s: "trig", claim: "2s10s re-steepens off the 0th %ile", metric: "T10Y2Y", trig: "> 0.55", now: "0.41" },
  ];
  const watch = [
    { claim: "AVGO gaps >10% → the AI-capex cluster is a trend, not noise", metric: "AVGO:change_pct", trig: "< −10", h: "today open" },
    { claim: "WTI recovers above $95 = positioning unwind, not demand", metric: "CL=F:last", trig: "> 95", h: "2 sessions" },
    { claim: "HY OAS holds the de-risking line", metric: "BAMLH0A0HYM2", trig: "> 2.85", h: "next week" },
    { claim: "10Y breaks 4.5% post-payroll = more rate pain for tech", metric: "DGS10", trig: "> 4.5", h: "Fri close" },
    { claim: "Gold holds >$4,500 on an oil bounce = geopolitical floor", metric: "GC=F:last", trig: "> 4500", h: "next session" },
  ];
  const badge = { miss: "MISS", watch: "WATCHING", hit: "HIT", trig: "TRIGGERED" };
  return (
    <div className="story">
      <div className="meta-row">
        <span>Source: <b>narrative_2026-06-04.md</b></span>
        <span>Session: <b>Pre-US open</b></span>
        <span>Grading prior: <b>0 hit · 1 inverted · 2 miss</b></span>
      </div>

      <h2 style={{ marginTop: 0 }}>Since last time</h2>
      <p className="cap" style={{ marginBottom: 4 }}>Grading yesterday's <code>watch</code> block against today's brief — the read is accountable.</p>
      <table className="grade-tbl">
        <tbody>
          {grades.map((g, i) => (
            <tr key={i}>
              <td style={{ width: 96 }}><span className={"badge " + g.s}>{badge[g.s]}</span></td>
              <td>{g.claim}</td>
              <td className="gm">{g.metric} {g.trig}</td>
              <td className="gnow">now {g.now}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Today in one line</h2>
      <div className="thesis-hero">
        <div className="te">● The thesis · with its flip condition</div>
        <div className="lead" style={{ margin: 0 }}>The oil floor broke while gold caught a simultaneous +$55 bid — that pairing is a demand-concern repricing, not an Iran-risk relief trade; it flips to “geopolitical resolved” only if WTI recovers above $95 by the close <i>and</i> gold gives back gains.</div>
      </div>

      <h2>TL;DR</h2>
      <ul>
        <li><b>WTI −3.2% to $92.44 overnight</b> while gold +1.2% to $4,520 — if this were Iran de-escalation, gold falls with oil; instead gold bids. <i>Consequence:</i> the XLE hedge that saved the tape yesterday is gone.</li>
        <li><b>Broadcom faces a historic gap-down at open</b> — a fifth large-cap AI-infra name joins the cluster (after CRM −5.1%, NVDA −3.6%, MSFT −3.2%, TSMC −2.2%). <i>Consequence:</i> this has crossed from idiosyncratic to a trend.</li>
        <li><b>Blackstone gates its flagship private credit fund</b> amid $4.5bn of Q2 redemptions. <i>Consequence:</i> private gates historically precede public spread widening by 2–4 weeks.</li>
      </ul>

      <h2>What moved &amp; why</h2>
      <h3>Commodities &amp; credit</h3>
      <p>The session's dominant cross-asset signal: <b>WTI −$3.09 (−3.2%) to $92.44; Brent −$2.99 (−3.1%) to $94.36.</b> The key analytical question is <i>why gold rose simultaneously</i> — gold +$55.30 (+1.24%) to $4,519.70 while DXY fell. This combination is inconsistent with a simple Iran-risk-off. The most likely read: leveraged long-oil positions unwinding, while gold absorbs the “I don't trust this resolution” flow and copper (98th %ile) hasn't caught the memo.</p>
      <h3>Equities &amp; sectors</h3>
      <p>US equities are stale in this pre-market snapshot; the directional signal comes from the newsflow. Five of the eight most important AI-infra names are now in confirmed downtrend. That is not noise. Yesterday's only offensive winners — Energy (+1.29%) and Healthcare (+0.79%) — lose their function as WTI breaks lower.</p>

      <h2>Risk lens</h2>
      <p>The Broadcom cluster changes the risk calculus. The combined pressure of higher-for-longer rates (10Y at the 96th %ile) <i>and</i> capex-cycle deceleration is precisely what consensus didn't price. <b>Leveraged funds net short −458k S&amp;P contracts</b> — the fast money was ahead of this; the squeeze fuel for a soft payroll is still in place.</p>
      <p><b>Portfolio hedge map is now worse:</b> (1) duration doesn't work (stock-bond corr +0.76); (2) energy just lost its hedge function; (3) credit too tight to add protection. Cash and possibly gold are the only clean defensive plays.</p>

      <h2>What to watch</h2>
      <ol>
        <li>Broadcom's actual open print — does AVGO gap &gt;−10%? Watch HY OAS simultaneously.</li>
        <li>WTI recovery above $95 — a bounce = positioning unwind; holds $91–93 into payrolls = demand concern.</li>
        <li>Friday May payrolls — the single highest-stakes data point.</li>
      </ol>
      <p className="cap" style={{ margin: "14px 0 4px" }}>The machine-readable <code>watch</code> block — the next session grades these:</p>
      <div className="watch-block">
        <table>
          <tbody>
            {watch.map((w, i) => (
              <tr key={i}>
                <td>{w.claim}</td>
                <td className="wm">{w.metric} {w.trig}</td>
                <td className="wh">{w.h}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>Sources</h2>
      <p style={{ fontSize: ".84rem", color: "var(--text-dim)" }}>Broadcom (Seeking Alpha · Yahoo Finance) · Blackstone private credit gate (FT) · CrowdStrike Q1 (Seeking Alpha) · asymmetric downside (MarketWatch) · Meta Business Agent (Nasdaq) — all 2026-06-03/04.</p>
    </div>
  );
}

/* ---- Learn: The investment clock (radial regime map) ---- */
function CycleClock() {
  const cx = 175, cy = 175, ro = 152, ri = 80;
  // quadrants in math angles (CCW from east), y flipped on render
  const quads = [
    { name:"Recovery",    lead:"Stocks lead",      sub:"growth ↑ · inflation ↓", a0:90,  a1:180, color:"#36c26f" },
    { name:"Overheat",    lead:"Commodities lead", sub:"growth ↑ · inflation ↑", a0:0,   a1:90,  color:"#f5a623" },
    { name:"Stagflation", lead:"Cash leads",       sub:"growth ↓ · inflation ↑", a0:-90, a1:0,   color:"#ff5c6c" },
    { name:"Reflation",   lead:"Bonds lead",       sub:"growth ↓ · inflation ↓", a0:180, a1:270, color:"#7beafb" },
  ];
  const pt = (ang, r) => [cx + r * Math.cos(ang * Math.PI / 180), cy - r * Math.sin(ang * Math.PI / 180)];
  const ring = (a0, a1) => {
    const N = 24, out = [], inn = [];
    for (let i = 0; i <= N; i++) { const a = a0 + (a1 - a0) * i / N; out.push(pt(a, ro)); }
    for (let i = N; i >= 0; i--) { const a = a0 + (a1 - a0) * i / N; inn.push(pt(a, ri)); }
    return [...out, ...inn].map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" ") + "Z";
  };
  const nowAng = -28; // late Overheat rotating into Stagflation
  const tip = pt(nowAng, ro - 10), base = pt(nowAng + 180, ri - 30);
  return (
    <div className="chart" style={{ display:"flex", gap:28, flexWrap:"wrap", alignItems:"center" }}>
      <svg viewBox="0 0 350 350" style={{ width:300, height:300, flex:"0 0 auto" }}>
        {quads.map((q, i) => {
          const mid = (q.a0 + q.a1) / 2, lp = pt(mid, (ro + ri) / 2);
          return (
            <g key={i}>
              <path d={ring(q.a0, q.a1)} fill={q.color} fillOpacity="0.13" stroke={q.color} strokeOpacity="0.4" strokeWidth="1" />
              <text x={lp[0]} y={lp[1] - 8} textAnchor="middle" fontFamily="var(--grot)" fontWeight="600" fontSize="13" fill={q.color}>{q.name}</text>
              <text x={lp[0]} y={lp[1] + 9} textAnchor="middle" fontFamily="var(--mono)" fontSize="9.5" fill="var(--text-dim)">{q.lead}</text>
            </g>
          );
        })}
        {/* axes */}
        <line x1={cx} y1={cy - ro} x2={cx} y2={cy + ro} stroke="var(--grid)" strokeWidth="1" />
        <line x1={cx - ro} y1={cy} x2={cx + ro} y2={cy} stroke="var(--grid)" strokeWidth="1" />
        <text x={cx + 4} y={cy - ro + 2} fontFamily="var(--mono)" fontSize="9" fill="var(--text-dim)">GROWTH ↑</text>
        <text x={cx + ro - 2} y={cy - 6} textAnchor="end" fontFamily="var(--mono)" fontSize="9" fill="var(--text-dim)">INFLATION →</text>
        {/* needle */}
        <line x1={base[0]} y1={base[1]} x2={tip[0]} y2={tip[1]} stroke="var(--text)" strokeWidth="2.5" strokeLinecap="round" />
        <circle cx={cx} cy={cy} r="6" fill="var(--text)" />
        <circle cx={tip[0]} cy={tip[1]} r="5" fill="var(--text)" />
        <text x={tip[0] + 6} y={tip[1] + 14} fontFamily="var(--mono)" fontSize="10" fill="var(--text)">NOW</text>
      </svg>
      <div style={{ flex:1, minWidth:240 }}>
        <div className="ct">The investment clock · where the cycle leads capital</div>
        <p className="cap" style={{ margin:"8px 0 0" }}>Two axes — growth and inflation — carve the cycle into four regimes, each favoring a different asset. Today the needle sits in <b style={{ color:"var(--warn)" }}>late Overheat</b> rotating toward <b style={{ color:"var(--down)" }}>Stagflation</b>: oil breaking on demand fear (growth turning down) while gold bids (inflation/debasement hedge still on). That rotation is why the read favors cash and gold over cyclicals.</p>
      </div>
    </div>
  );
}

/* ---- Learn: Anatomy of a yield (decomposition bar) ---- */
function YieldStack() {
  const scaleMax = 5;
  const parts = [
    { label:"Real yield", note:"10Y TIPS", val:2.11, color:"#7beafb" },
    { label:"Breakeven inflation", note:"expected CPI + risk prem.", val:2.38, color:"#f5a623" },
  ];
  const total = parts.reduce((s, p) => s + p.val, 0);
  return (
    <div className="chart">
      <div className="ct">Anatomy of a yield · the 10Y, taken apart</div>
      <div style={{ display:"flex", height:46, borderRadius:8, overflow:"hidden", marginTop:14, border:"1px solid var(--border)" }}>
        {parts.map((p, i) => (
          <div key={i} title={`${p.label} ${p.val}%`} style={{ width:`${(p.val / scaleMax) * 100}%`, background:p.color, display:"flex", alignItems:"center", justifyContent:"center" }}>
            <span style={{ fontFamily:"var(--mono)", fontSize:".82rem", color:"rgba(13,12,12,.85)", fontWeight:600 }}>{p.val.toFixed(2)}%</span>
          </div>
        ))}
        <div style={{ flex:1, background:"var(--surface-2)", display:"flex", alignItems:"center", paddingLeft:10 }}>
          <span style={{ fontFamily:"var(--mono)", fontSize:".72rem", color:"var(--text-dim)" }}>head-room to 5%</span>
        </div>
      </div>
      <div style={{ display:"flex", gap:20, flexWrap:"wrap", marginTop:12 }}>
        {parts.map((p, i) => (
          <div key={i} style={{ display:"flex", gap:8, alignItems:"baseline" }}>
            <span style={{ width:10, height:10, borderRadius:2, background:p.color, alignSelf:"center" }}></span>
            <span style={{ fontFamily:"var(--grot)", fontWeight:600, fontSize:".82rem", color:"var(--text)" }}>{p.label}</span>
            <span style={{ fontFamily:"var(--mono)", fontSize:".72rem", color:"var(--text-dim)" }}>{p.note}</span>
          </div>
        ))}
        <div style={{ marginLeft:"auto", fontFamily:"var(--mono)", fontSize:".82rem", color:"var(--text)" }}>= {total.toFixed(2)}% nominal</div>
      </div>
      <p className="cap" style={{ margin:"12px 0 0" }}>A nominal yield is just <b style={{ color:"var(--text)" }}>real rate + expected inflation</b>. When the 10Y rises, ask <i>which piece moved</i>: a real-rate jump tightens financial conditions (bad for equities); a breakeven jump is an inflation-scare. Today's 4.49% is mostly real — a higher-for-longer story, not a runaway-inflation one.</p>
    </div>
  );
}

/* ---- Learn: Who owns the US stock market (composition bar) ---- */
function OwnersBar() {
  const owners = [
    { name:"Households (direct)", pct:38, color:"#7beafb" },
    { name:"Mutual funds", pct:20, color:"#6fb6c9" },
    { name:"Foreign investors", pct:17, color:"#5aa0a8" },
    { name:"Retirement & pensions", pct:14, color:"#cf9f5a" },
    { name:"ETFs", pct:7, color:"#f5a623" },
    { name:"Hedge funds & other", pct:4, color:"#b3aaa0" },
  ];
  return (
    <div className="chart">
      <div className="ct">Who owns the US stock market</div>
      <div style={{ display:"flex", height:38, borderRadius:8, overflow:"hidden", marginTop:14, border:"1px solid var(--border)" }}>
        {owners.map((o, i) => (
          <div key={i} title={`${o.name} ~${o.pct}%`} style={{ width:`${o.pct}%`, background:o.color, display:"flex", alignItems:"center", justifyContent:"center" }}>
            {o.pct >= 9 && <span style={{ fontFamily:"var(--mono)", fontSize:".72rem", color:"rgba(13,12,12,.8)", fontWeight:600 }}>{o.pct}%</span>}
          </div>
        ))}
      </div>
      <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit, minmax(150px, 1fr))", gap:"6px 16px", marginTop:12 }}>
        {owners.map((o, i) => (
          <div key={i} style={{ display:"flex", gap:8, alignItems:"center" }}>
            <span style={{ width:10, height:10, borderRadius:2, background:o.color }}></span>
            <span style={{ fontFamily:"var(--grot)", fontSize:".78rem", color:"var(--text)" }}>{o.name}</span>
            <span style={{ fontFamily:"var(--mono)", fontSize:".72rem", color:"var(--text-dim)", marginLeft:"auto" }}>{o.pct}%</span>
          </div>
        ))}
      </div>
      <p className="cap" style={{ margin:"12px 0 0" }}>Households still hold the plurality directly — which is why a sharp drawdown is a <i>consumer-confidence</i> event, not just a Wall Street one. Foreign ownership (~17%) is the channel a dollar crisis would transmit through. <span style={{ color:"var(--text-dim)" }}>Approximate, Fed Financial Accounts style.</span></p>
    </div>
  );
}

function LearnPage() {
  const events = [
    { y:"1792", t:"Buttonwood Agreement", c:"cat-founding" },
    { y:"1929", t:"Wall Street Crash", c:"cat-crash" },
    { y:"1933", t:"Glass–Steagall", c:"cat-reform" },
    { y:"1971", t:"Nixon ends gold standard", c:"cat-reform" },
    { y:"1987", t:"Black Monday", c:"cat-crash" },
    { y:"2008", t:"Global Financial Crisis", c:"cat-crash" },
    { y:"2010", t:"Dodd–Frank", c:"cat-reform" },
    { y:"2020", t:"COVID crash & recovery", c:"cat-crash" },
  ];
  const cat = { "cat-founding":"#7beafb","cat-crash":"#ef5350","cat-reform":"#26a69a","cat-innovation":"#ab47bc","cat-boom":"#ffa726" };
  return (
    <div className="main">
      <div className="hd"><h1>📚 Learn the Markets</h1></div>
      <div className="tcap" style={{ marginTop:6 }}>Foundations for a risk analyst — researched and fact-checked.</div>
      <hr className="hr" />
      <h2 className="h2">Market history · 1792 → today</h2>
      <div style={{ display:"flex", gap:0, alignItems:"center", margin:"24px 0", position:"relative", borderTop:"1px solid var(--border)", paddingTop:30 }}>
        {events.map((e,i) => (
          <div key={i} style={{ flex:1, textAlign:"center", position:"relative" }}>
            <div style={{ width:14, height:14, borderRadius:"50%", background:cat[e.c], margin:"0 auto 10px" }}></div>
            <div style={{ fontFamily:"var(--mono)", fontSize:".74rem", color:"var(--text)" }}>{e.y}</div>
            <div style={{ fontSize:".68rem", color:"var(--text-dim)", marginTop:3, padding:"0 4px" }}>{e.t}</div>
          </div>
        ))}
      </div>
      <div style={{ display:"flex", gap:16, flexWrap:"wrap", marginTop:8 }}>
        {Object.entries({ Founding:"#7beafb", Crash:"#ef5350", Reform:"#26a69a", Innovation:"#ab47bc", Boom:"#ffa726" }).map(([k,v]) => (
          <span key={k} style={{ display:"flex", alignItems:"center", gap:7, fontSize:".74rem", color:"var(--text-dim)" }}>
            <span style={{ width:10, height:10, borderRadius:"50%", background:v }}></span>{k}
          </span>
        ))}
      </div>
      <hr className="hr" />
      <h2 className="h2">The cycle &amp; what leads it</h2>
      <CycleClock />
      <hr className="hr" />
      <h2 className="h2">Rates, taken apart</h2>
      <YieldStack />
      <hr className="hr" />
      <h2 className="h2">The players</h2>
      <OwnersBar />
      <hr className="hr" />
      <p style={{ color:"var(--text)", maxWidth:680 }}>A market is a venue where buyers and sellers discover a price. The Learn page pairs researched prose with diagrams that reveal <i>how the system is wired</i> — capital flows, policy transmission, the cycle, and what sits inside a number.</p>
      <h2 className="h2" style={{ marginTop:28 }}>How money moves through the system</h2>
      <Sankey data={{
        title: "Savings → intermediaries → markets",
        nodes: [
          { id:"hh", label:"Households", layer:0 },
          { id:"pen", label:"Pensions & insurers", layer:0 },
          { id:"fgn", label:"Foreign official", layer:0 },
          { id:"bank", label:"Banks", layer:1 },
          { id:"am", label:"Asset managers", layer:1 },
          { id:"dlr", label:"Dealers", layer:1 },
          { id:"eq", label:"Equities", layer:2 },
          { id:"ust", label:"Treasuries", layer:2 },
          { id:"cr", label:"Credit", layer:2 },
          { id:"csh", label:"Cash & bills", layer:2 },
        ],
        links: [
          { source:"hh", target:"bank", value:30 }, { source:"hh", target:"am", value:42 },
          { source:"pen", target:"am", value:48 }, { source:"pen", target:"dlr", value:14 },
          { source:"fgn", target:"dlr", value:22 }, { source:"fgn", target:"bank", value:10 },
          { source:"bank", target:"cr", value:18 }, { source:"bank", target:"csh", value:22 },
          { source:"am", target:"eq", value:52 }, { source:"am", target:"ust", value:24 }, { source:"am", target:"cr", value:14 },
          { source:"dlr", target:"ust", value:26 }, { source:"dlr", target:"eq", value:10 },
        ],
      }} />
      <h2 className="h2" style={{ marginTop:28 }}>How a Fed rate decision reaches the economy</h2>
      <Sankey height={400} data={{
        title: "Policy transmission · rate → channels → real economy",
        nodes: [
          { id:"ff", label:"Fed funds rate", layer:0 },
          { id:"bk", label:"Bank lending rates", layer:1 },
          { id:"by", label:"Bond yields", layer:1 },
          { id:"ap", label:"Asset prices", layer:1 },
          { id:"fx", label:"US dollar", layer:1 },
          { id:"ex", label:"Expectations", layer:1 },
          { id:"inv", label:"Investment", layer:2 },
          { id:"con", label:"Consumption", layer:2 },
          { id:"nx", label:"Net exports", layer:2 },
          { id:"emp", label:"Employment", layer:2 },
          { id:"inf", label:"Inflation", layer:2 },
        ],
        links: [
          { source:"ff", target:"bk", value:30 }, { source:"ff", target:"by", value:26 },
          { source:"ff", target:"ap", value:20 }, { source:"ff", target:"fx", value:14 }, { source:"ff", target:"ex", value:18 },
          { source:"bk", target:"inv", value:16 }, { source:"bk", target:"con", value:14 },
          { source:"by", target:"inv", value:14 }, { source:"by", target:"ap", value:8 },
          { source:"ap", target:"con", value:16 }, { source:"ap", target:"inv", value:8 },
          { source:"fx", target:"nx", value:14 },
          { source:"ex", target:"inf", value:12 }, { source:"ex", target:"con", value:6 },
          { source:"inv", target:"emp", value:24 }, { source:"con", target:"emp", value:22 },
          { source:"nx", target:"emp", value:10 }, { source:"emp", target:"inf", value:18 },
        ],
      }} />
      <p className="cap" style={{ margin:"12px 0 0", maxWidth:680 }}>The lags are long and variable — a hike takes ~12–18 months to fully reach employment and inflation. That's why the brief watches the <i>channels</i> (yields, the dollar, asset prices) for early signal rather than waiting on the lagging real-economy data.</p>
    </div>
  );
}

Object.assign(window, { StoryTab, LearnPage });

