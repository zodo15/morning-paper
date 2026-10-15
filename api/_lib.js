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
export async function saveSub(sub, quiet) {
  await put(keyFor(sub.endpoint), JSON.stringify({ sub: sub, quiet: !!quiet, at: new Date().toISOString() }), { access: 'private', addRandomSuffix: false, allowOverwrite: true, contentType: 'application/json' });
}
export async function allSubs() {
  var out = [], cursor;
  do {
    var r = await list({ prefix: 'subs/', cursor: cursor, limit: 1000 });
    for (var b of r.blobs) {
      var g = await get(b.pathname, { access: 'private', useCache: false });
      if (!g) continue;
      var txt = await new Response(g.stream).text();
      try { var j = JSON.parse(txt); out.push({ path: b.pathname, sub: j.sub, quiet: !!j.quiet }); } catch (e) {}
    }
    cursor = r.hasMore ? r.cursor : undefined;
  } while (cursor);
  return out;
}
export async function dropSub(path) { await del(path); }
export function vapid() { webpush.setVapidDetails(SUBJECT, PUBLIC_KEY, process.env.VAPID_PRIVATE_KEY); return webpush; }

/* quiet hours: 23:00 to 07:00 India time, only for subscribers who turned the toggle on */
export function isQuietNow() {
  var h = (new Date().getUTCHours() * 60 + new Date().getUTCMinutes() + 330) / 60 % 24;
  return h >= 23 || h < 7;
}
export async function pushAll(payload, force) {
  var wp = vapid(), subs = await allSubs(), quietNow = isQuietNow(), sent = 0, dropped = 0, failed = 0, skipped = 0;
  var body = JSON.stringify(payload);
  for (var s of subs) {
    if (!force && s.quiet && quietNow) { skipped++; continue; }
    try { await wp.sendNotification(s.sub, body, { TTL: 3600, urgency: 'high' }); sent++; }
    catch (e) { if (e.statusCode === 404 || e.statusCode === 410) { await dropSub(s.path); dropped++; } else failed++; }
  }
  return { subscribers: subs.length, sent: sent, dropped: dropped, failed: failed, skippedQuiet: skipped };
}
export function authed(req) {
  var t = process.env.PUSH_SEND_TOKEN || '';
  var h = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  if (!t || h.length !== t.length) return false;
  return crypto.timingSafeEqual(Buffer.from(h), Buffer.from(t));
}
var FEED = 'cards/feed.json';
export async function readFeed() {
  try {
    var g = await get(FEED, { access: 'private', useCache: false });
    if (!g) return [];
    return JSON.parse(await new Response(g.stream).text());
  } catch (e) { return []; }
}
export async function writeFeed(cards) {
  await put(FEED, JSON.stringify(cards), { access: 'private', addRandomSuffix: false, allowOverwrite: true, contentType: 'application/json' });
}
