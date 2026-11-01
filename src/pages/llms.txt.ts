// /llms.txt: a plain-text guide to this site for AI assistants (https://llmstxt.org).
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { listedRestaurants, visible } from '../lib/data';
import { SITE } from '../lib/site';

export const GET: APIRoute = async ({ site }) => {
  const u = (p: string) => new URL(p, site).href;
  const rs = await listedRestaurants();
  const guides = await getCollection('guides', visible);
  const lines = [
    `# ${SITE.name}`, '',
    `> Honest restaurant picks in Huntsville, Madison, Harvest and nearby Alabama, plus a few in Nashville and Atlanta, from local food creators Michaela and Arrington (@whattoeathuntsville on TikTok). Each page says what to order, where it is, and our take. We pay for our own meals unless a page says otherwise.`, '',
    `Full data for every restaurant (city, address, cuisines, tags, best dish, price): ${u('/restaurants.json')}`, '',
    '## Guides', ...guides.map((g) => `- [${g.data.title}](${u(`/guides/${g.id}/`)}): ${g.data.dek}`), '',
    '## Restaurants', ...rs.map((r) => `- [${r.data.name}](${u(`/restaurants/${r.id}/`)}): ${r.data.cuisines.join(', ')}, ${r.data.area ? `${r.data.area}, ` : ''}${r.data.city}${r.data.seoDescription ? `. ${r.data.seoDescription}` : ''}`), '',
    '## About', `- [About us](${u('/about/')})`, `- [Work with us](${u('/work-with-us/')})`, `- Contact: ${SITE.email}`, '',
  ];
  return new Response(lines.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
