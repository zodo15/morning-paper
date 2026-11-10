import crypto from 'node:crypto';
import { readFileSync } from 'node:fs';
import { getJSON, putJSON, readSubs, mutateSubs } from './_github-state.js';
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
  const path = keyFor(sub.endpoint);
  await mutateSubs(items => {
    const old = items.find(s => s.path === path);
    if (old && JSON.stringify(old.sub) === JSON.stringify(sub) && old.quiet === !!quiet) return items;
    return items.filter(s => s.path !== path).concat([{ path, sub, quiet: !!quiet, at: new Date().toISOString() }]);
  });
}
export async function allSubs() { return (await readSubs()).value; }
export async function dropSub(path) { await mutateSubs(items => items.filter(s => s.path !== path)); }
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
// Last-good feed survives provider failures; writes require a fresh remote revision.
let feedCache = null;
function validFeed(cards) {
  if (!Array.isArray(cards) || cards.length === 0 || cards.some(c => !c.id || !c.headline || !c.publishedAt) || new Set(cards.map(c => c.id)).size !== cards.length) throw new Error('Cards state unavailable or invalid');
  return cards;
}
export async function loadFeed({ strict = false } = {}) {
  if (!strict && feedCache && Date.now() - feedCache.at < 30000) return { cards: structuredClone(feedCache.cards), sha: feedCache.sha, source: 'github-cache' };
  try {
    const r = await getJSON('morning-paper', 'cards/feed.json', 'cards-data');
    validFeed(r.value); feedCache = { cards: r.value, sha: r.sha, at: Date.now() };
    return { cards: structuredClone(r.value), sha: r.sha, source: 'github' };
  } catch (e) {
    if (strict) throw e;
    if (feedCache) return { cards: structuredClone(feedCache.cards), source: 'last-good' };
    const cards = validFeed(JSON.parse(readFileSync(process.cwd() + '/data/cards-feed.json', 'utf8')));
    return { cards, source: 'snapshot' };
  }
}
export async function readFeed(options) { return (await loadFeed(options)).cards; }
export async function writeFeed(cards, sha) {
  validFeed(cards);
  await putJSON('morning-paper','cards/feed.json','cards-data',cards,sha,'Update Cards feed');
  feedCache = null;
}
