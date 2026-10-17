import crypto from 'node:crypto';
import { authed, pushAll, readFeed, writeFeed } from './_lib.js';
import { put } from '@vercel/blob';
var LANES = ['markets', 'insurance', 'fintech', 'ai', 'startups'];
function clean(s, n) { return String(s == null ? '' : s).replace(/\s+/g, ' ').trim().slice(0, n); }
var LIM = { headline: 140, body: 900, why: 450, watch: 600, source_name: 60, watch_next: 120, wrong_if: 120, market_reaction: 160 };
function over(b, keys) { for (var k of keys) { if (b[k] != null && String(b[k]).replace(/\s+/g, ' ').trim().length > LIM[k]) return k + ' is over ' + LIM[k] + ' characters (not truncated; shorten it)'; } return null; }
function firstSentence(t, n) {
  var m = String(t).match(/^(.+?[.!?])(\s|$)/); var s = m ? m[1] : String(t);
  return s.length > n ? s.slice(0, n - 1).trim() + '\u2026' : s;
}
function sniff(buf) {
  if (buf.length > 12 && buf[0] === 0xFF && buf[1] === 0xD8) return 'jpg';
  if (buf.length > 12 && buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4E) return 'png';
  if (buf.length > 12 && buf.slice(0, 4).toString() === 'RIFF' && buf.slice(8, 12).toString() === 'WEBP') return 'webp';
  return null;
}
/* image: {url | data(base64), credit, page}. Fetched or decoded here, checked by magic bytes, stored in private Blob, served by /api/img. */
async function ingestImage(id, im) {
  if (!im) return null;
  var pos = /^(left|center|right)( (top|center|bottom))?$/.test(im.pos || '') ? im.pos : '';
  var credit = clean(im.credit, 120), page = /^https:\/\//.test(im.page || '') ? String(im.page).slice(0, 500) : '';
  if (typeof im.src === 'string' && /^photos\/[\w.-]+$/.test(im.src)) return { src: im.src, credit: credit, page: page, pos: pos };
  var buf;
  if (im.data) buf = Buffer.from(String(im.data), 'base64');
  else if (/^https:\/\//.test(im.url || '')) {
    var r = await fetch(im.url, { headers: { 'User-Agent': 'Mozilla/5.0 (compatible; MorningPaper/1.0)', Accept: 'image/*', Referer: im.page || im.url }, redirect: 'follow' });
    if (!r.ok) throw new Error('image fetch ' + r.status);
    buf = Buffer.from(await r.arrayBuffer());
  } else return null;
  if (!buf || buf.length < 2000 || buf.length > 3500000) throw new Error('image size ' + (buf ? buf.length : 0));
  var ext = sniff(buf); if (!ext) throw new Error('not a jpg/png/webp');
  var path = 'img/' + id + '.' + ext;
  await put(path, buf, { access: 'private', addRandomSuffix: false, allowOverwrite: true, contentType: ext === 'jpg' ? 'image/jpeg' : 'image/' + ext });
  return { src: 'api/img?p=' + path, credit: credit, page: page, pos: pos };
}

/* optional card metadata: provenance + depth fields (all optional; old cards lack them) */
function applyMeta(b, card) {
  if (typeof b.source_name === 'string' && b.source_name.trim()) card.source_name = clean(b.source_name, LIM.source_name);
  if (typeof b.watch_next === 'string' && b.watch_next.trim()) card.watch_next = clean(b.watch_next, LIM.watch_next);
  if (typeof b.wrong_if === 'string' && b.wrong_if.trim()) card.wrong_if = clean(b.wrong_if, LIM.wrong_if);
  if (typeof b.market_reaction === 'string' && b.market_reaction.trim()) card.market_reaction = clean(b.market_reaction, LIM.market_reaction);
  if (typeof b.published_at_source === 'string') {
    var v = b.published_at_source.trim();
    if ((/^\d{4}-\d{2}-\d{2}$/.test(v) || !isNaN(Date.parse(v))) && v.length <= 40) card.published_at_source = v;
  }
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
  if (b.pushOnly) {
    var pu = String(b.url || ''); if (!/^(\.\/|\.\/\?c=c[a-z0-9]+)$/.test(pu)) return res.status(400).json({ error: 'url must be ./ or ./?c=<card id>' });
    var pr = await pushAll({ title: clean(b.pushTitle, 110), body: clean(b.pushGist, 160), url: pu, tag: clean(b.tag, 60) || undefined }, b.force === true);
    return res.status(200).json({ pushOnly: true, push: pr });
  }
  var tooLong = over(b, ['headline', 'body', 'why', 'watch', 'source_name', 'watch_next', 'wrong_if', 'market_reaction']);
  if (tooLong) return res.status(400).json({ error: tooLong });
  if (b.update) {
    var tgt = feed.find(function (x) { return x.id === b.update; });
    if (!tgt) return res.status(404).json({ error: 'no such card' });
    ['headline', 'body', 'why', 'watch'].forEach(function (k) { if (b[k] != null) tgt[k] = clean(b[k], LIM[k]); });
    applyMeta(b, tgt);
    try { var im0 = await ingestImage(tgt.id, b.image); if (im0) tgt.image = im0; } catch (e) { return res.status(422).json({ error: String(e.message || e) }); }
    await writeFeed(feed);
    return res.status(200).json({ updated: tgt.id, image: tgt.image || null });
  }
  var card = {
    lane: LANES.indexOf(b.lane) >= 0 ? b.lane : 'markets',
    tags: (Array.isArray(b.tags) ? b.tags : []).map(function (t) { return clean(t, 16).toUpperCase(); }).filter(Boolean).slice(0, 5),
    headline: clean(b.headline, LIM.headline), body: clean(b.body, LIM.body), why: clean(b.why, LIM.why), watch: clean(b.watch, LIM.watch),
    sources: (Array.isArray(b.sources) ? b.sources : []).filter(function (s) { return s && /^https:\/\//.test(s.url || ''); }).map(function (s) { return { name: clean(s.name, 40) || 'Source', url: String(s.url).slice(0, 500) }; }).slice(0, 4),
    kind: clean(b.kind, 40), timeLabel: clean(b.timeLabel, 60),
    image: null,
    at: clean(b.at, 40)
  };
  applyMeta(b, card);
  if (!card.headline || !card.body || !card.sources.length) return res.status(400).json({ error: 'headline, body and at least one https source required' });
  if (!b.force) {
    var dupe = feed.find(function (c) { return c.headline.toLowerCase() === card.headline.toLowerCase(); });
    if (dupe) return res.status(409).json({ error: 'duplicate headline', id: dupe.id });
  }
  var now = new Date();
  card.id = 'c' + now.toISOString().replace(/[-:T]/g, '').slice(2, 12) + crypto.randomBytes(2).toString('hex');
  card.publishedAt = now.toISOString();
  if (!card.at) card.at = card.publishedAt;
  var imgWarn = null;
  try { card.image = await ingestImage(card.id, b.image); } catch (e) { imgWarn = String(e.message || e); }
  feed.push(card);
  feed.sort(function (a, c) { return a.publishedAt < c.publishedAt ? 1 : -1; });
  await writeFeed(feed.slice(0, 200));
  var out = { id: card.id, pushed: false, image: card.image ? card.image.src : null };
  if (imgWarn) out.imageWarning = imgWarn;
  if (b.push !== false) {
    out.push = await pushAll({ title: clean(b.pushTitle, 110) || card.headline, body: clean(b.pushGist, 160) || firstSentence(card.body, 150), url: './?c=' + card.id, tag: card.id }, b.force === true);
    out.pushed = true;
  }
  res.status(200).json(out);
}
