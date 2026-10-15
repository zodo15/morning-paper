import crypto from 'node:crypto';
import { allSubs, dropSub, vapid } from './_lib.js';
function authed(req) {
  var t = process.env.PUSH_SEND_TOKEN || '';
  var h = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  if (!t || h.length !== t.length) return false;
  return crypto.timingSafeEqual(Buffer.from(h), Buffer.from(t));
}
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  if (!authed(req)) return res.status(401).json({ error: 'unauthorized' });
  var b = req.body && (typeof req.body === 'string' ? JSON.parse(req.body) : req.body) || {};
  var title = String(b.title || '').slice(0, 120), gist = String(b.gist || '').slice(0, 400), url = String(b.url || '/');
  if (!title) return res.status(400).json({ error: 'title required' });
  if (!/^(https:\/\/|\/|#)/.test(url)) url = '/';
  var payload = JSON.stringify({ title: title, body: gist, url: url, tag: b.tag || ('alert-' + Date.now()) });
  var wp = vapid(), subs = await allSubs(), sent = 0, dropped = 0, failed = 0;
  for (var s of subs) {
    try { await wp.sendNotification(s.sub, payload, { TTL: 3600, urgency: 'high' }); sent++; }
    catch (e) { if (e.statusCode === 404 || e.statusCode === 410) { await dropSub(s.path); dropped++; } else failed++; }
  }
  res.status(200).json({ subscribers: subs.length, sent: sent, dropped: dropped, failed: failed });
}
