import { get } from '@vercel/blob';
var TYPES = { jpg: 'image/jpeg', png: 'image/png', webp: 'image/webp' };
export default async function handler(req, res) {
  var p = String((req.query && req.query.p) || '');
  var m = p.match(/^img\/(c[a-z0-9]+)\.(jpg|png|webp)$/);
  if (!m) return res.status(400).end('bad path');
  try {
    var g = await get(p, { access: 'private', useCache: false });
    if (!g) return res.status(404).end('not found');
    var buf = Buffer.from(await new Response(g.stream).arrayBuffer());
    res.setHeader('Content-Type', TYPES[m[2]]);
    res.setHeader('Cache-Control', 'public, max-age=86400, s-maxage=604800');
    res.status(200).end(buf);
  } catch (e) { res.status(404).end('not found'); }
}
