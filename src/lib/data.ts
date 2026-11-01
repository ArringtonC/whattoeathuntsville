import { getCollection } from 'astro:content';

// Drafts show in the local preview (npm run dev) and the private preview build, never in the public build.
export const visible = ({ data }: { data: { draft: boolean } }) => !data.draft || import.meta.env.DEV || import.meta.env.PUBLIC_SHOW_DRAFTS === 'true';

const labelRank = { great: 0, good: 1, 'first-look': 2, none: 3 } as const;

// Published restaurants. Closed places keep their page but leave search and lists.
export const allRestaurants = () => getCollection('restaurants', visible);
export const listedRestaurants = async () =>
  (await allRestaurants())
    .filter((r) => r.data.status !== 'closed')
    .sort((a, b) => labelRank[a.data.label] - labelRank[b.data.label] || +b.data.lastVerified - +a.data.lastVerified);

export const videosFor = async (restaurantId: string) =>
  (await getCollection('videos'))
    .filter((v) => v.data.restaurants.some((ref) => ref.id === restaurantId))
    .sort((a, b) => +b.data.postedDate - +a.data.postedDate);

export const guidesFor = async (restaurantId: string) =>
  (await getCollection('guides', visible)).filter((g) => g.data.entries.some((e) => e.restaurant.id === restaurantId));

export const storiesFor = async (restaurantId: string) =>
  (await getCollection('stories', visible)).filter((s) => s.data.restaurants.some((ref) => ref.id === restaurantId));

// Card images: a guide uses its first place's cover, a story its video's cover.
export const guideCover = async (g: { data: { cover?: string; entries: { restaurant: { id: string } }[] } }) =>
  g.data.cover ?? (await allRestaurants()).find((r) => r.id === g.data.entries[0]?.restaurant.id)?.data.cover;
export const storyCover = async (s: { data: { video?: { id: string } } }) =>
  s.data.video ? (await getCollection('videos')).find((v) => v.id === s.data.video!.id)?.data.cover : undefined;
