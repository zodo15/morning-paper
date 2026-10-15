import crypto from 'node:crypto';
import { allSubs } from './_lib.js';
export default async function handler(req, res) {
  var t = process.env.PUSH_SEND_TOKEN || '', h = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  if (!t || h.length !== t.length || !crypto.timingSafeEqual(Buffer.from(h), Buffer.from(t))) return res.status(401).json({ error: 'unauthorized' });
  res.status(200).json({ subscribers: (await allSubs()).length });
}
