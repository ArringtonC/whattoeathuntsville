# What to Eat Huntsville — website

Restaurant discovery site built with [Astro](https://astro.build). Every page is generated from content files, so adding a restaurant means adding one file.

## Run it

```sh
npm install
npm run dev      # preview at http://localhost:4321
npm run build    # final site goes to dist/
```

## Add content

| What | Where | Notes |
| --- | --- | --- |
| Restaurant | `src/content/restaurants/<slug>.md` | Copy an existing file. `label` is great, good, first-look, or none. Body = your short write-up. |
| TikTok video | `src/content/videos.json` | Link it to restaurants by slug. |
| TikTok cover | `public/covers/<slug>.jpg`, then `cover: /covers/<slug>.jpg` | Without a cover, a tinted placeholder shows. |
| Guide | `src/content/guides/<slug>.md` | Ordered list of restaurant slugs + why each is there. |
| Story | `src/content/stories/<slug>.md` | Short article in Markdown. Set `sponsor:` only for paid stories. |

The build fails with a clear message if a field is missing or a slug is wrong.

## Before launch

- **Upgrade Node.js to 22.23.4 or newer, then switch `astro` in package.json to `^7.4.4`.** Astro 6 (used now because this Mac has Node 22.23.1) has known security issues fixed only in Astro 7.
- Replace all sample content (anything in `[brackets]`, and files named `sample-*`).
- Set the real domain in `astro.config.mjs`.
- Forms (newsletter, suggest, work with us) use Netlify Forms. If you host elsewhere or pick an email service, point the newsletter forms at that service.
- Display ads are off: `ADS_ENABLED` in `src/lib/site.ts`.
- Email templates live in `emails/` (see its README).
