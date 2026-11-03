# What to Eat Huntsville: start here

This folder is the whole website, **whattoeathuntsville.com**. You only need a few folders. Everything else runs the site, and you can leave it alone.

## The folders you'll use

| Folder | What's inside | Open it when you want to… |
| --- | --- | --- |
| `sheets/` | Spreadsheets you can open in Numbers or Excel | Change tags or labels, check prices and phone numbers |
| `src/content/restaurants/` | One file per restaurant (name, address, tags, and "Our take") | Read or fix one restaurant's page |
| `src/content/guides/` | The guides (Best wings, Date night…) | Read or edit a guide |
| `emails/` | The Weekly Bite email designs and drafts of issues | Plan the next newsletter |
| `docs/` | The launch checklist, the SEO checklist (`SEO-CHECKLIST.md`) and the launch TikTok plan | See what's done and what's left |
| `public/covers/` | The TikTok cover photos the site uses | Find a photo |

## The spreadsheets (`sheets/`)

- **restaurant-tags.xlsx**: one row per restaurant, a yes/no column for each tag. Set the label (great, good, first-look, none) and mark "Reviewed". When you're done, tell Claude **"import the tags"**.
- **restaurant-prices.csv**: price level ($ to $$$$), phone number, and where each came from. Blank price means we couldn't confirm it.
- **restaurants.csv**: a simple list of every restaurant.

Always start from the newest copy in this folder. An old copy can undo newer fixes when it's imported.

## Folders you can ignore

| Folder | What it is |
| --- | --- |
| `research/` | Notes from the AI fact-checks: menu checks, location checks, original captions, transcript notes, SEO ideas |
| `transcripts/` | Text of what we said in each TikTok (made with Whisper) |
| `scripts/` | Small tools that move data between the sheets and the site |
| `src/pages/`, `src/components/`, `src/layouts/`, `src/styles/` | The website's design and code |
| `dist/`, `node_modules/` | Built files. Made automatically. Don't edit |

## Where things live online

- Website: https://whattoeathuntsville.com
- Newsletter sign-ups: Kit (kit.com)
- Domain and hello@whattoeathuntsville.com email: Cloudflare
- Google search reports: Google Search Console
- Ads: Google AdSense (waiting for approval)

## For developers

```sh
npm install
npm run dev      # preview at http://localhost:4321 (shows drafts too)
npm run deploy   # build and publish to GitHub Pages
```

Each restaurant, guide, and story is a Markdown file in `src/content/`. The build stops with a clear message if a field is missing or a restaurant slug is wrong. `draft: true` hides a page from the live site.
