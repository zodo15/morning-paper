/* The Morning Paper service worker.
   - Shell + data: network first (a new edition shows up the moment it is published), cached copy when offline.
   - Fonts, photos, icons: cache first, filled as you read (so every edition you opened works offline).
   - Audio: never cached here (large, range requests); it needs a connection. */
var VERSION = 'mp-v1';
var SHELL = ['./', 'index.html', 'styles.css', 'app.js', 'data/editions.js', 'data/lraudio.js', 'manifest.webmanifest',
  'icons/icon-192.png', 'icons/apple-touch-icon.png',
  'fonts/fraunces-var.woff2', 'fonts/inter-var.woff2', 'fonts/sourceserif4-var.woff2'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(VERSION).then(function (c) {
    return Promise.all(SHELL.map(function (u) { return c.add(u).catch(function () {}); }));
  }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k !== VERSION; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
function networkFirst(req) {
  return fetch(req).then(function (res) {
    if (res && res.ok) { var copy = res.clone(); caches.open(VERSION).then(function (c) { c.put(req, copy); }); }
    return res;
  }).catch(function () {
    return caches.match(req).then(function (hit) {
      return hit || (req.mode === 'navigate' ? caches.match('index.html') : Response.error());
    });
  });
}
function cacheFirst(req) {
  return caches.match(req).then(function (hit) {
    if (hit) return hit;
    return fetch(req).then(function (res) {
      if (res && res.ok) { var copy = res.clone(); caches.open(VERSION).then(function (c) { c.put(req, copy); }); }
      return res;
    });
  });
}
self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.origin !== location.origin) return;
  if (/\.(m4a|mp3|ogg|wav)$/i.test(url.pathname) || req.headers.get('range')) return;  // audio streams from the network
  if (/\.(woff2?|jpg|jpeg|png|webp|svg|gif)$/i.test(url.pathname)) { e.respondWith(cacheFirst(req)); return; }
  e.respondWith(networkFirst(req));
});
