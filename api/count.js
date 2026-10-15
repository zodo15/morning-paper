import { authed, allSubs, readFeed } from './_lib.js';
export default async function handler(req, res) {
  if (!authed(req)) return res.status(401).json({ error: 'unauthorized' });
  var subs = await allSubs(), feed = await readFeed();
  res.status(200).json({ subscribers: subs.length, quietOn: subs.filter(function (s) { return s.quiet; }).length, cards: feed.length });
}
