// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages serves the site from /whattoeathuntsville until a custom domain is connected.
// Set SITE_URL and BASE_PATH in the deploy workflow; locally both default to the root.
export default defineConfig({
  site: process.env.SITE_URL ?? 'https://example.com',
  base: process.env.BASE_PATH ?? '/',
});
