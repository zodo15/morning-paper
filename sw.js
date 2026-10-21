/* The Morning Paper service worker.
   - Shell + data: network first (a new edition shows up the moment it is published), cached copy when offline.
   - Fonts, photos, icons: cache first, filled as you read (so every edition you opened works offline).
   - Audio: never cached here (large, range requests); it needs a connection. */
var VERSION = 'mp-v18';
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
    return Promise.all(ks.filter(function (k) { return k !== VERSION && k !== 'mp-nav'; }).map(function (k) { return caches.delete(k); }));
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
  if (url.pathname.indexOf('/api/') === 0) return;
  if (/\.(m4a|mp3|ogg|wav)$/i.test(url.pathname) || req.headers.get('range')) return;  // audio streams from the network
  if (/\.(woff2?|jpg|jpeg|png|webp|svg|gif)$/i.test(url.pathname)) { e.respondWith(cacheFirst(req)); return; }
  e.respondWith(networkFirst(req));
});

/* Web Push: show the alert, and open the page or article when it is tapped. */
self.addEventListener('push', function (e) {
  var d = {};
  try { d = e.data ? e.data.json() : {}; } catch (x) { d = { title: 'The Morning Paper', body: e.data ? e.data.text() : '' }; }
  e.waitUntil(self.registration.showNotification(d.title || 'The Morning Paper', {
    body: d.body || '', tag: d.tag || undefined, icon: 'icons/icon-192.png', badge: 'icons/icon-192.png', data: { url: d.url || './' }
  }));
});
self.addEventListener('notificationclick', function (e) {
  e.notification.close();
  var target = (e.notification.data && e.notification.data.url) || './';
  var abs = new URL(target, self.registration.scope);
  var hm = abs.hash.match(/^#\/cards\/(c[a-z0-9]+)$/);
  if (hm) { abs.hash = ''; abs.search = '?c=' + hm[1]; }
  abs = abs.href;
  var internal = abs.indexOf(self.registration.scope) === 0;
  /* iOS can open the installed app at its start page and ignore the URL, so also leave a note the page reads on launch / resume. */
  var note = internal ? caches.open('mp-nav').then(function (c) { return c.put('/__nav', new Response(JSON.stringify({ u: abs, t: Date.now() }))); }).catch(function () {}) : Promise.resolve();
  e.waitUntil(note.then(function () { return self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (cs) {
    if (internal) {
      for (var i = 0; i < cs.length; i++) {
        if (cs[i].url.indexOf(self.registration.scope) === 0 && 'focus' in cs[i]) {
          return cs[i].focus().then(function (c) { c.postMessage({ type: 'nav', url: abs }); if ('navigate' in c) return c.navigate(abs).catch(function () {}); });
        }
      }
    }
    return self.clients.openWindow(abs);
  }); }));
});
