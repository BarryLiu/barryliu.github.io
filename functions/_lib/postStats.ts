export type PostStatsPayload = {
  slug: string;
  views: number;
  likes: number;
  dislikes: number;
};

export type PostStatsStore = {
  get(slug: string): Promise<string | null>;
  put(slug: string, value: string): Promise<void>;
};

const emptyStats = (): PostStatsPayload => ({
  slug: '',
  views: 0,
  likes: 0,
  dislikes: 0,
});

export function normalizeSlug(raw: string | null | undefined) {
  return (raw ?? '').trim().replace(/^\/+|\/+$/g, '');
}

export function parseStats(raw: string | null, slug: string): PostStatsPayload {
  if (!raw) return { ...emptyStats(), slug };
  try {
    const parsed = JSON.parse(raw) as Partial<PostStatsPayload>;
    return {
      slug,
      views: Number(parsed.views ?? 0),
      likes: Number(parsed.likes ?? 0),
      dislikes: Number(parsed.dislikes ?? 0),
    };
  } catch {
    return { ...emptyStats(), slug };
  }
}

export async function readStats(store: PostStatsStore, slug: string) {
  const normalized = normalizeSlug(slug);
  return parseStats(await store.get(normalized), normalized);
}

export async function writeStats(store: PostStatsStore, stats: PostStatsPayload) {
  await store.put(stats.slug, JSON.stringify(stats));
  return stats;
}

export async function incrementView(store: PostStatsStore, slug: string) {
  const stats = await readStats(store, slug);
  stats.views += 1;
  return writeStats(store, stats);
}

export async function applyVote(store: PostStatsStore, slug: string, vote: 'like' | 'dislike') {
  const stats = await readStats(store, slug);
  if (vote === 'like') stats.likes += 1;
  if (vote === 'dislike') stats.dislikes += 1;
  return writeStats(store, stats);
}
