import { readFeed } from './_lib.js';
export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  var feed = await readFeed();
  feed.sort(function (a, b) { return a.publishedAt < b.publishedAt ? 1 : -1; });
  res.status(200).json({ cards: feed.slice(0, 80) });
}
