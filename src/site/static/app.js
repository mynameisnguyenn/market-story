// Tab navigation + lazy Plotly rendering. Vanilla JS, no build step.
// Figures ship as inert JSON (script.cdata); we call Plotly.newPlot only when a chart's tab is
// first shown, so opening the page initializes just the masthead + the active tab — not all ~19
// charts at once (the mobile-jank win).
(function () {
  "use strict";

  function renderCharts(root) {
    if (!root || !window.Plotly) return;
    root.querySelectorAll(".chart:not([data-rendered])").forEach(function (div) {
      var s = document.querySelector('script.cdata[data-for="' + div.id + '"]');
      if (!s) return;
      var spec;
      try { spec = JSON.parse(s.textContent); } catch (e) { return; }
      var cfg = { displayModeBar: false, responsive: true, scrollZoom: false,
                  staticPlot: div.dataset.static === "1" };
      try { window.Plotly.newPlot(div, spec.data || [], spec.layout || {}, cfg); } catch (e) {}
      div.setAttribute("data-rendered", "1");
    });
  }

  function resizeCharts(root) {
    if (!root || !window.Plotly) return;
    root.querySelectorAll(".chart[data-rendered]").forEach(function (d) {
      try { window.Plotly.Plots.resize(d); } catch (e) {}
    });
  }

  function showTab(id) {
    document.querySelectorAll(".tab").forEach(function (t) {
      t.classList.toggle("active", t.dataset.target === id);
    });
    document.querySelectorAll(".tabpanel").forEach(function (p) {
      p.classList.toggle("active", p.id === id);
    });
    var panel = document.getElementById(id);
    renderCharts(panel);     // first visit: init this tab's charts
    resizeCharts(panel);     // re-fit (Plotly can't size a chart that was display:none)
    if (history.replaceState) history.replaceState(null, "", "#" + id);
  }

  document.querySelectorAll(".tab").forEach(function (tab) {
    tab.addEventListener("click", function () { showTab(tab.dataset.target); });
  });

  function init() {
    renderCharts(document.querySelector(".masthead"));        // sparklines (always visible)
    var hash = (location.hash || "").replace("#", "");
    if (hash && document.getElementById(hash)) showTab(hash);
    else renderCharts(document.querySelector(".tabpanel.active"));
  }

  if (window.Plotly) init();
  else window.addEventListener("load", init);                 // wait for the plotly.js CDN script

  window.addEventListener("resize", function () {
    resizeCharts(document.querySelector(".tabpanel.active"));
  });

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("assets/sw.js").catch(function () {});
    });
  }
})();
