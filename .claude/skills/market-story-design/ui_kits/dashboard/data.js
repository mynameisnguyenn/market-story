/* Market Story — sample brief data (mirrors the brief JSON contract; values
   lifted from the repo's narrative_2026-06-04.md for authenticity). Static. */
window.MS_DATA = {
  date: "2026-06-04",
  session_label: "Pre-US open",
  generated_at: "12:26",
  stats: { sector_advancers: 4, sector_decliners: 7, sector_count: 11 },

  // KPI strip — symbol, label, value, delta, kind, sparkline points (0..1 normalized path)
  kpis: [
    { sym:"^GSPC", label:"S&P 500", val:"7,553.68", delta:"+0.18%", tone:"up", spark:[.2,.35,.3,.5,.45,.62,.58,.7,.66,.8], sparkUp:true },
    { sym:"^IXIC", label:"Nasdaq", val:"26,853.98", delta:"−0.42%", tone:"down", spark:[.7,.62,.66,.5,.55,.4,.45,.32,.36,.28], sparkUp:false },
    { sym:"^TNX", label:"10Y Treasury", val:"4.491%", delta:"+1 bps", tone:"down", spark:[.3,.34,.4,.42,.5,.55,.6,.64,.7,.72], sparkUp:true },
    { sym:"DX-Y.NYB", label:"US Dollar", val:"99.24", delta:"−0.31%", tone:"down", spark:[.7,.66,.6,.62,.55,.5,.46,.4,.38,.34], sparkUp:false },
    { sym:"GC=F", label:"Gold", val:"4,519.70", delta:"+1.24%", tone:"up", spark:[.3,.28,.34,.4,.45,.55,.6,.7,.78,.86], sparkUp:true },
    { sym:"^VIX", label:"VIX", val:"16.5", delta:"+2.8%", tone:"down", spark:[.4,.42,.38,.45,.5,.48,.55,.6,.58,.64], sparkUp:false, invert:true },
  ],

  read: "The oil floor broke while gold caught a simultaneous +$55 bid — that pairing is a demand-concern repricing, not an Iran-risk relief trade; it flips to \u201Cgeopolitical resolved\u201D only if WTI recovers above $95 by the close AND gold gives back gains.",

  signals: [
    { tone:"down", text:"WTI \u2212$3.09 (\u22123.2%) to $92.44 \u2014 the energy hedge that saved the tape is gone." },
    { tone:"warn", text:"Blackstone gates its flagship private credit fund amid $4.5bn of Q2 redemptions." },
    { tone:"down", text:"Broadcom faces a historic gap-down \u2014 a fifth AI-infra name joins the cluster." },
    { tone:"up", text:"Gold +1.24% to $4,519.70 \u2014 the safe-haven bid is absorbing the distrust flow." },
  ],

  leaders: [
    { name:"Energy (XLE)", chg:"+1.29%", tone:"up" },
    { name:"Healthcare (XLV)", chg:"+0.79%", tone:"up" },
    { name:"Staples (XLP)", chg:"+0.40%", tone:"up" },
    { name:"Meta (META)", chg:"+4.20%", tone:"up" },
  ],
  laggards: [
    { name:"Salesforce (CRM)", chg:"−5.10%", tone:"down" },
    { name:"Nvidia (NVDA)", chg:"−3.60%", tone:"down" },
    { name:"Microsoft (MSFT)", chg:"−3.20%", tone:"down" },
    { name:"TSMC", chg:"−2.20%", tone:"down" },
  ],

  sectors: [
    { name:"Energy", chg:1.29 }, { name:"Health", chg:0.79 }, { name:"Staples", chg:0.40 },
    { name:"Utilities", chg:0.12 }, { name:"Materials", chg:-0.34 }, { name:"Financials", chg:-0.58 },
    { name:"Industrials", chg:-0.71 }, { name:"Real Estate", chg:-0.88 }, { name:"Comm Svcs", chg:-1.15 },
    { name:"Discretionary", chg:-1.84 }, { name:"Technology", chg:-2.42 },
  ],

  us_equities: [
    { name:"S&P 500", last:"7,553.68", d1:"+0.18", w1:"−1.42", ytd:"+12.30", t1:"up", tw:"down", ty:"up" },
    { name:"Nasdaq 100", last:"26,853.98", d1:"−0.42", w1:"−2.81", ytd:"+18.40", t1:"down", tw:"down", ty:"up" },
    { name:"Dow Jones", last:"43,118.20", d1:"+0.21", w1:"−0.55", ytd:"+6.10", t1:"up", tw:"down", ty:"up" },
    { name:"Russell 2000", last:"2,284.50", d1:"−0.66", w1:"−1.90", ytd:"+2.70", t1:"down", tw:"down", ty:"up" },
    { name:"VIX", last:"16.50", d1:"+2.80", w1:"+8.10", ytd:"−12.40", t1:"down", tw:"down", ty:"up" },
  ],
  global_indices: [
    { name:"Euro Stoxx 50", last:"5,412.10", d1:"+0.34", w1:"+0.90", ytd:"+9.80", t1:"up", tw:"up", ty:"up" },
    { name:"FTSE 100", last:"8,640.30", d1:"+0.12", w1:"+0.41", ytd:"+5.20", t1:"up", tw:"up", ty:"up" },
    { name:"DAX", last:"19,820.40", d1:"+0.28", w1:"+1.10", ytd:"+11.40", t1:"up", tw:"up", ty:"up" },
    { name:"Nikkei 225", last:"39,104.00", d1:"−1.36", w1:"−2.20", ytd:"+3.90", t1:"down", tw:"down", ty:"up" },
    { name:"Hang Seng", last:"18,442.10", d1:"−1.48", w1:"−2.95", ytd:"−1.10", t1:"down", tw:"down", ty:"down" },
  ],
  rates: [
    { name:"13-week", last:"4.310", d1:"+0.5", w1:"−1.20", ytd:"−8.40", t1:"down", tw:"up", ty:"up" },
    { name:"5-year", last:"4.214", d1:"−0.8", w1:"+2.10", ytd:"+4.30", t1:"up", tw:"down", ty:"down" },
    { name:"10-year", last:"4.491", d1:"+1.0", w1:"+3.40", ytd:"+6.10", t1:"down", tw:"down", ty:"down" },
    { name:"30-year", last:"4.990", d1:"+1.4", w1:"+4.20", ytd:"+7.80", t1:"down", tw:"down", ty:"down" },
  ],
  fx: [
    { name:"EUR/USD", last:"1.0842", d1:"+0.31", w1:"+0.60", ytd:"+1.20", t1:"up", tw:"up", ty:"up" },
    { name:"USD/JPY", last:"152.40", d1:"−0.22", w1:"−0.80", ytd:"+3.40", t1:"down", tw:"down", ty:"up" },
    { name:"GBP/USD", last:"1.2731", d1:"+0.18", w1:"+0.40", ytd:"+0.90", t1:"up", tw:"up", ty:"up" },
    { name:"DXY", last:"99.24", d1:"−0.31", w1:"−0.70", ytd:"−2.10", t1:"down", tw:"down", ty:"down" },
  ],
  commodities: [
    { name:"WTI crude", last:"92.44", d1:"−3.20", w1:"−5.10", ytd:"+14.20", t1:"down", tw:"down", ty:"up" },
    { name:"Brent crude", last:"94.36", d1:"−3.10", w1:"−4.80", ytd:"+13.10", t1:"down", tw:"down", ty:"up" },
    { name:"Gold", last:"4,519.70", d1:"+1.24", w1:"+2.40", ytd:"+22.60", t1:"up", tw:"up", ty:"up" },
    { name:"Silver", last:"38.40", d1:"+0.90", w1:"+1.80", ytd:"+19.30", t1:"up", tw:"up", ty:"up" },
    { name:"Copper", last:"6.52", d1:"+0.62", w1:"+1.10", ytd:"+8.90", t1:"up", tw:"up", ty:"up" },
  ],
  credit: [
    { name:"HYG (HY ETF)", last:"79.68", d1:"+0.02", w1:"−0.10", ytd:"+1.40", t1:"up", tw:"down", ty:"up" },
    { name:"LQD (IG ETF)", last:"108.90", d1:"−0.08", w1:"−0.30", ytd:"+0.80", t1:"down", tw:"down", ty:"up" },
    { name:"TLT (20Y+)", last:"88.20", d1:"−0.34", w1:"−1.20", ytd:"−3.40", t1:"down", tw:"down", ty:"down" },
  ],

  macro: [
    { name:"10Y Treasury", latest:"4.49", chg:"+0.01", pct:"96", t:"down" },
    { name:"2s10s curve", latest:"0.41", chg:"−0.02", pct:"0", t:"down" },
    { name:"HY OAS", latest:"2.71", chg:"0.00", pct:"3", t:"neutral" },
    { name:"IG OAS", latest:"0.74", chg:"+0.01", pct:"3", t:"down" },
    { name:"10Y breakeven", latest:"2.38", chg:"0.00", pct:"71", t:"neutral" },
    { name:"NFCI", latest:"−0.49", chg:"+0.01", pct:"29", t:"down" },
  ],

  extremes: [
    { name:"Copper", last:"6.52", pct:"98", z:"+1.91", t:"up" },
    { name:"10Y yield", last:"4.49", pct:"96", z:"+1.74", t:"down" },
    { name:"HYG", last:"79.68", pct:"95", z:"+1.62", t:"up" },
    { name:"WTI", last:"92.44", pct:"81", z:"+0.88", t:"down" },
    { name:"DXY", last:"99.24", pct:"80", z:"+0.81", t:"down" },
  ],

  regime: [
    { label:"Credit", val:"risk-on", t:"up" },
    { label:"Curve", val:"flat / late", t:"down" },
    { label:"Vol", val:"compressed", t:"up" },
    { label:"Breadth", val:"risk-off", t:"down" },
    { label:"Hedge (stock-bond)", val:"broken +0.76", t:"down" },
  ],

  news: [
    { t:"Broadcom could be headed for one of the worst 1-day destructions in shareholder value ever", s:"Yahoo Finance", d:"2026-06-04 11:40" },
    { t:"Broadcom tumbles on guidance, but Wall Street sees bright outlook", s:"Seeking Alpha", d:"2026-06-04 10:12" },
    { t:"Blackstone caps withdrawals from flagship private credit fund as Q2 redemptions surge to $4.5bn", s:"FT", d:"2026-06-04 09:05" },
    { t:"CrowdStrike falls after Q1 results; analysts bullish but flag high ARR expectations", s:"Seeking Alpha", d:"2026-06-04 08:50" },
    { t:"How single-stock turbulence presents 'asymmetric' downside risk for a calm S&P 500", s:"MarketWatch", d:"2026-06-03 18:30" },
    { t:"Why Meta Platforms stock crushed the market today — Business Agent launch", s:"Nasdaq", d:"2026-06-03 16:20" },
    { t:"Stocks making the biggest moves after hours: Broadcom, CrowdStrike, PVH & more", s:"CNBC", d:"2026-06-03 16:05" },
    { t:"Trump administration turns to a new rationale to justify old tariffs", s:"NYT", d:"2026-06-03 14:10" },
  ],
};
