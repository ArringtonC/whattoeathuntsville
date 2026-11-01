// Writes dist/sitemap.xml from the built pages, skipping pages marked noindex.
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const site = (process.env.SITE_URL ?? 'https://whattoeathuntsville.com').replace(/\/$/, '');
const base = (process.env.BASE_PATH ?? '/').replace(/\/$/, '');
const walk = (dir) => readdirSync(dir).flatMap((f) => {
  const p = join(dir, f);
  return statSync(p).isDirectory() ? walk(p) : p.endsWith('index.html') ? [p] : [];
});
const urls = walk('dist')
  .filter((f) => f !== 'dist/404/index.html' && !/<meta name="robots" content="noindex/.test(readFileSync(f, 'utf8')))
  .map((f) => `${site}${base}/${f.slice('dist/'.length, -'index.html'.length)}`)
  .sort();
writeFileSync('dist/sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((u) => `  <url><loc>${u}</loc></url>`).join('\n')}\n</urlset>\n`);
console.log(`sitemap: ${urls.length} pages`);
