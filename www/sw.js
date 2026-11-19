const CACHE_NAME = "mallik-humanity-v1";
const ASSETS = [
  "./",
  "./index.html",
  "./app-download.html",
  "./nepal-banks.html",
  "./mallik-tier-gate.js",
  "./manifest.json"
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
});

self.addEventListener("fetch", (e) => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
