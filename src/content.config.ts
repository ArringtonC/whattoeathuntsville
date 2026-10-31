import { defineCollection, reference } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';
import { CITIES, CUISINES, OCCASIONS } from './lib/site';

const dish = z.object({ name: z.string(), note: z.string().optional() });

// One record per restaurant. Every page that mentions a place reads from here.
const restaurants = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/restaurants' }),
  schema: z.object({
    name: z.string(),
    status: z.enum(['open', 'temporarily-closed', 'closed']).default('open'),
    city: z.enum(CITIES),
    area: z.string().optional(),
    address: z.string().optional(),
    cuisines: z.array(z.enum(CUISINES)).min(1).max(3),
    price: z.number().int().min(1).max(4).optional(),
    occasions: z.array(z.enum(OCCASIONS)).default([]),
    tags: z.array(z.string()).default([]), // free search words: birria, food truck, cash only…
    searchTerms: z.array(z.string()).default([]), // extra words search matches but the page doesn't show
    // great/good are earned ratings; first-look is for new openings; none = not rated yet.
    label: z.enum(['great', 'good', 'first-look', 'none']).default('none'),
    verdict: z.string().optional(),
    bestDish: dish.optional(),
    alsoOrder: z.array(dish).default([]),
    skip: z.string().optional(),
    cover: z.string().optional(), // path under /public, e.g. /covers/north-italia.jpg
    coverFocus: z.enum(['top', 'center', 'bottom']).default('center'),
    website: z.url().optional(),
    menuUrl: z.url().optional(),
    reservationUrl: z.url().optional(),
    mapsUrl: z.url().optional(),
    phone: z.string().optional(),
    lastVerified: z.coerce.date(),
    disclosure: z.enum(['independent', 'hosted', 'sponsored']).default('independent'),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

const videos = defineCollection({
  loader: file('src/content/videos.json'),
  schema: z.object({
    title: z.string(),
    tiktokUrl: z.url(),
    postedDate: z.coerce.date(),
    cover: z.string().optional(),
    restaurants: z.array(reference('restaurants')).default([]),
  }),
});

const guides = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/guides' }),
  schema: z.object({
    title: z.string(),
    dek: z.string(),
    city: z.enum(CITIES),
    updated: z.coerce.date(),
    entries: z.array(z.object({ restaurant: reference('restaurants'), why: z.string(), dish: z.string().optional() })),
    sponsored: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

const stories = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/stories' }),
  schema: z.object({
    title: z.string(),
    dek: z.string(),
    kind: z.enum(['new-opening', 'our-experience', 'food-news', 'travel']),
    published: z.coerce.date(),
    updated: z.coerce.date().optional(),
    readMinutes: z.number().int().default(3),
    restaurants: z.array(reference('restaurants')).default([]),
    video: reference('videos').optional(),
    disclosure: z.string().default('We paid for our meal.'),
    sponsor: z.string().optional(), // business name when the story is paid for
    draft: z.boolean().default(false),
  }),
});

export const collections = { restaurants, videos, guides, stories };
