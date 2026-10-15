import { okEndpoint, saveSub } from './_lib.js';
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  var b = req.body && (typeof req.body === 'string' ? JSON.parse(req.body) : req.body);
  var s = b && b.subscription ? b.subscription : b;
  if (!s || !s.endpoint || !s.keys || !s.keys.p256dh || !s.keys.auth || !okEndpoint(s.endpoint)) return res.status(400).json({ error: 'bad subscription' });
  try {
    await saveSub({ endpoint: s.endpoint, keys: { p256dh: s.keys.p256dh, auth: s.keys.auth } }, !!(b && b.quiet));
    res.status(200).json({ ok: true });
  } catch (e) { res.status(500).json({ error: 'store failed' }); }
}
