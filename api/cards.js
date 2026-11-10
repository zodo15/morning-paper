import { loadFeed } from './_lib.js';
export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'public, s-maxage=30, stale-while-revalidate=60');
  try {
    const state = await loadFeed();
    state.cards.sort((a,b) => a.publishedAt < b.publishedAt ? 1 : -1);
    res.setHeader('X-Cards-Source', state.source);
    res.status(200).json({ cards: state.cards.slice(0,80) });
  } catch (e) { res.setHeader('Cache-Control','no-store'); res.status(503).json({ error: 'Cards temporarily unavailable' }); }
}
