// market-story service worker — installable PWA + offline.
// Cache-first for the app shell so the last build opens with no network; the daily
// rebuild changes CACHE so a new version supersedes the old on next load.
var CACHE = "market-story-v1";
var SHELL = [
  "./",
  "./index.html",
  "./assets/style.css",
  "./assets/app.js",
  "./assets/manifest.webmanifest",
  "./assets/icon-192.png",
  "./assets/icon-512.png"
];

self.addEventListener("install", function (e) {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function (c) {
    // best-effort: a missing asset must not abort the whole install
    return Promise.all(SHELL.map(function (u) {
      return c.add(u).catch(function () {});
    }));
  }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; })
                             .map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then(function (hit) {
      if (hit) return hit;
      return fetch(e.request).then(function (resp) {
        // cache same-origin successes so the shell + assets stay available offline
        if (resp && resp.status === 200 && e.request.url.indexOf(self.location.origin) === 0) {
          var copy = resp.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
        }
        return resp;
      }).catch(function () { return caches.match("./index.html"); });
    })
  );
});
