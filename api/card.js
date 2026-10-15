import crypto from 'node:crypto';
import { authed, pushAll, readFeed, writeFeed } from './_lib.js';
var LANES = ['markets', 'insurance', 'fintech', 'ai', 'startups'];
function clean(s, n) { return String(s == null ? '' : s).replace(/\s+/g, ' ').trim().slice(0, n); }
function firstSentence(t, n) {
  var m = String(t).match(/^(.+?[.!?])(\s|$)/); var s = m ? m[1] : String(t);
  return s.length > n ? s.slice(0, n - 1).trim() + '\u2026' : s;
}
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  if (!authed(req)) return res.status(401).json({ error: 'unauthorized' });
  var b = req.body && (typeof req.body === 'string' ? JSON.parse(req.body) : req.body) || {};
  var feed = await readFeed();
  if (b.remove) {
    var n0 = feed.length; feed = feed.filter(function (c) { return c.id !== b.remove; }); await writeFeed(feed);
    return res.status(200).json({ removed: n0 - feed.length });
  }
  var card = {
    lane: LANES.indexOf(b.lane) >= 0 ? b.lane : 'markets',
    tags: (Array.isArray(b.tags) ? b.tags : []).map(function (t) { return clean(t, 16).toUpperCase(); }).filter(Boolean).slice(0, 5),
    headline: clean(b.headline, 140), body: clean(b.body, 700), why: clean(b.why, 320), watch: clean(b.watch, 260),
    sources: (Array.isArray(b.sources) ? b.sources : []).filter(function (s) { return s && /^https:\/\//.test(s.url || ''); }).map(function (s) { return { name: clean(s.name, 40) || 'Source', url: String(s.url).slice(0, 500) }; }).slice(0, 4),
    kind: clean(b.kind, 40), timeLabel: clean(b.timeLabel, 60),
    image: b.image && /^(photos\/[\w.-]+|https:\/\/.+)$/.test(b.image.src || '') ? { src: String(b.image.src).slice(0, 400), credit: clean(b.image.credit, 120) } : null,
    at: clean(b.at, 40)
  };
  if (!card.headline || !card.body || !card.sources.length) return res.status(400).json({ error: 'headline, body and at least one https source required' });
  if (!b.force) {
    var dupe = feed.find(function (c) { return c.headline.toLowerCase() === card.headline.toLowerCase(); });
    if (dupe) return res.status(409).json({ error: 'duplicate headline', id: dupe.id });
  }
  var now = new Date();
  card.id = 'c' + now.toISOString().replace(/[-:T]/g, '').slice(2, 12) + crypto.randomBytes(2).toString('hex');
  card.publishedAt = now.toISOString();
  if (!card.at) card.at = card.publishedAt;
  feed.push(card);
  feed.sort(function (a, c) { return a.publishedAt < c.publishedAt ? 1 : -1; });
  await writeFeed(feed.slice(0, 200));
  var out = { id: card.id, pushed: false };
  if (b.push !== false) {
    out.push = await pushAll({ title: clean(b.pushTitle, 110) || card.headline, body: clean(b.pushGist, 160) || firstSentence(card.body, 150), url: './?c=' + card.id, tag: card.id }, b.force === true);
    out.pushed = true;
  }
  res.status(200).json(out);
}
