import { authed, pushAll } from './_lib.js';
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  if (!authed(req)) return res.status(401).json({ error: 'unauthorized' });
  var b = req.body && (typeof req.body === 'string' ? JSON.parse(req.body) : req.body) || {};
  var title = String(b.title || '').slice(0, 120), gist = String(b.gist || '').slice(0, 400), url = String(b.url || '/');
  if (!title) return res.status(400).json({ error: 'title required' });
  if (!/^(https:\/\/|\/|#)/.test(url)) url = '/';
  res.status(200).json(await pushAll({ title: title, body: gist, url: url, tag: b.tag || ('alert-' + Date.now()) }, b.force === true));
}
