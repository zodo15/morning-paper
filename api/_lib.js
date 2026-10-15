import crypto from 'node:crypto';
import { put, list, get, del } from '@vercel/blob';
import webpush from 'web-push';

export const PUBLIC_KEY = 'BKIAqnNG4K7Qxkbcbj8XLbnb43KoCy3IOqfV6g1qbpPUI34Wd5KymGHi059nlcSQbxx5K1mK5hykqhVg55pwgyM';
export const SUBJECT = 'mailto:bozosoup@gmail.com';

const HOSTS = [/(^|\.)push\.apple\.com$/, /(^|\.)googleapis\.com$/, /(^|\.)push\.services\.mozilla\.com$/, /(^|\.)notify\.windows\.com$/];
export function okEndpoint(u) {
  try { var x = new URL(u); return x.protocol === 'https:' && HOSTS.some(function (r) { return r.test(x.hostname); }); } catch (e) { return false; }
}
export function keyFor(endpoint) { return 'subs/' + crypto.createHash('sha256').update(endpoint).digest('hex') + '.json'; }
export async function saveSub(sub) {
  await put(keyFor(sub.endpoint), JSON.stringify({ sub: sub, at: new Date().toISOString() }), { access: 'private', addRandomSuffix: false, allowOverwrite: true, contentType: 'application/json' });
}
export async function allSubs() {
  var out = [], cursor;
  do {
    var r = await list({ prefix: 'subs/', cursor: cursor, limit: 1000 });
    for (var b of r.blobs) {
      var g = await get(b.pathname, { access: 'private', useCache: false });
      if (!g) continue;
      var txt = await new Response(g.stream).text();
      try { out.push({ path: b.pathname, sub: JSON.parse(txt).sub }); } catch (e) {}
    }
    cursor = r.hasMore ? r.cursor : undefined;
  } while (cursor);
  return out;
}
export async function dropSub(path) { await del(path); }
export function vapid() { webpush.setVapidDetails(SUBJECT, PUBLIC_KEY, process.env.VAPID_PRIVATE_KEY); return webpush; }
