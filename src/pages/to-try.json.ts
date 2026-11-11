// Places we have not tried, loaded by /eat-next only after a visitor searches (kept out of the page so Google does not read it as copied content).
import type { APIRoute } from 'astro';
import toTry from '../data/to-try.json';

export const GET: APIRoute = () =>
  new Response(JSON.stringify(toTry.map((r) => ({ n: r.name, c: r.cuisine, city: r.city }))), { headers: { 'Content-Type': 'application/json' } });
