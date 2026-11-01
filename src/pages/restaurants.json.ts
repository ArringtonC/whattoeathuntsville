// Machine-readable list of every open restaurant, for AI assistants and other tools (linked from /llms.txt).
import type { APIRoute } from 'astro';
import { getEntry } from 'astro:content';
import { listedRestaurants } from '../lib/data';

export const GET: APIRoute = async ({ site }) => {
  const rs = await listedRestaurants();
  const out = await Promise.all(rs.map(async (r) => {
    const d = r.data;
    return {
      name: d.name, url: new URL(`/restaurants/${r.id}/`, site).href, status: d.status,
      city: d.city, area: d.area, address: d.address, cuisines: d.cuisines, tags: d.tags, occasions: d.occasions,
      price: d.price ? '$'.repeat(d.price) : undefined, ourLabel: d.label, bestDish: d.bestDish?.name,
      alsoOrder: d.alsoOrder.map((x) => x.name), summary: d.seoDescription, website: d.website, lastVisited: d.lastVerified.toISOString().slice(0, 10),
    };
  }));
  return new Response(JSON.stringify({ site: 'What to Eat Huntsville', updated: new Date().toISOString().slice(0, 10), restaurants: out }, null, 1), { headers: { 'Content-Type': 'application/json' } });
};
