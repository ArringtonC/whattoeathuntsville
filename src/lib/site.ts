import type { CollectionEntry } from 'astro:content';

export const SITE = {
  name: 'What to Eat Huntsville',
  tiktok: 'https://www.tiktok.com/@whattoeathuntsville',
  instagram: 'https://www.instagram.com/whattoeathuntsville',
  facebook: 'https://www.facebook.com/Whattoeathuntsville',
  threads: 'https://www.threads.net/@whattoeathuntsville',
  tagline: 'Local roots. Global taste.',
  newsletter: 'The Weekly Bite',
  email: 'hello@whattoeathuntsville.com',
  formEndpoint: 'https://formsubmit.co/ajax/hello@whattoeathuntsville.com', // suggest + work-with-us forms (FormSubmit, no account)
  kitForm: 'https://app.kit.com/forms/10126403/subscriptions', // Kit form "The Weekly Bite"
};

// Display ads stay off until traffic qualifies for an ad network (v3 ad rules).
export const ADS_ENABLED = false;

export const CITIES = ['Huntsville', 'Madison', 'Decatur', 'Athens', 'Nashville', 'Atlanta'] as const;
export const LOCAL_CITIES = ['Huntsville', 'Madison', 'Decatur', 'Athens'];
export const TRAVEL_CITIES = ['Nashville', 'Atlanta'];

export const CUISINES = [
  'Mexican', 'Wings', 'Soul food', 'BBQ', 'Asian', 'Italian', 'Pizza', 'Chicken', 'Sweet treats',
  'Breakfast', 'American', 'Seafood', 'Sandwiches', 'Mediterranean', 'Cajun', 'Caribbean', 'Latin', 'Vegan',
] as const;

export const OCCASIONS = ['Date night', 'Brunch', 'Family', 'Quick lunch', 'Late night', 'Group', 'Cheap eats', 'Birthday'] as const;

export const slugify = (s: string) => s.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

export const priceText = (p?: number) => (p ? '$'.repeat(p) : '');
// Joins the parts of a meta line, skipping blanks: "Mexican · Madison · $".
export const metaLine = (...parts: (string | undefined)[]) => parts.filter(Boolean).join(' · ');

export const mapsUrl = (r: CollectionEntry<'restaurants'>['data']) =>
  r.mapsUrl ?? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${r.name} ${r.address ?? r.city}`)}`;

export const fmtDate = (d: Date) => d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });

// Placeholder tones until real TikTok covers are added.
const TONES = ['#D9B48F', '#E8D5BC', '#C98E5E', '#EADFCF', '#BFCBB0', '#E3C7B5', '#CDA987'];
export const toneFor = (id: string) => TONES[[...id].reduce((a, c) => a + c.charCodeAt(0), 0) % TONES.length];

// Guides under 10 places get 1 ad after the first third; 10+ get 2, at least 4 entries apart.
export const guideAdSlots = (n: number) => {
  if (n < 4) return [];
  if (n < 10) return [Math.ceil(n / 3)];
  return [Math.ceil(n / 3), Math.ceil(n / 3) + Math.max(4, Math.ceil(n / 3))].filter((i) => i < n);
};
