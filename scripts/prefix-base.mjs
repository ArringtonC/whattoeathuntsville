// Adds the base path (e.g. /whattoeathuntsville) to root links in the built HTML.
// Pages link to "/restaurants/..." in source; on a GitHub project site those need the repo folder in front.
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const base = (process.env.BASE_PATH ?? '/').replace(/\/$/, '');
if (!base) process.exit(0);

const walk = (dir) => readdirSync(dir).flatMap((f) => {
  const p = join(dir, f);
  return statSync(p).isDirectory() ? walk(p) : p.endsWith('.html') ? [p] : [];
});

const fix = (path) => (path.startsWith(base + '/') || path === base ? path : base + path);
let count = 0;
for (const file of walk('dist')) {
  const html = readFileSync(file, 'utf8')
    .replace(/(href|src|action)="(\/(?!\/)[^"]*)"/g, (_, attr, path) => `${attr}="${fix(path)}"`)
    .replace(/&quot;(\/restaurants\/[^&]*)&quot;/g, (_, path) => `&quot;${fix(path)}&quot;`);
  writeFileSync(file, html);
  count++;
}
console.log(`prefix-base: ${count} pages now use ${base}`);
