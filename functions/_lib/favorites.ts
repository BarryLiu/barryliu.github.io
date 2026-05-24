import { normalizeSlug } from './postStats';

export type FavoritesStore = {
  get(key: string): Promise<string | null>;
  put(key: string, value: string): Promise<void>;
};

export type FavoritesPayload = {
  slugs: string[];
  updatedAt: string;
};

export function favoritesKey(githubUserId: number | string) {
  return `github:${githubUserId}`;
}

export function parseFavorites(raw: string | null): FavoritesPayload {
  if (!raw) return { slugs: [], updatedAt: new Date(0).toISOString() };
  try {
    const parsed = JSON.parse(raw) as Partial<FavoritesPayload>;
    const slugs = Array.isArray(parsed.slugs)
      ? parsed.slugs.map((slug) => normalizeSlug(String(slug))).filter(Boolean)
      : [];
    return {
      slugs: Array.from(new Set(slugs)),
      updatedAt: typeof parsed.updatedAt === 'string' ? parsed.updatedAt : new Date(0).toISOString(),
    };
  } catch {
    return { slugs: [], updatedAt: new Date(0).toISOString() };
  }
}

export async function readFavorites(store: FavoritesStore, githubUserId: number) {
  return parseFavorites(await store.get(favoritesKey(githubUserId)));
}

export async function writeFavorites(store: FavoritesStore, githubUserId: number | string, slugs: string[], username?: string) {
  const payload: FavoritesPayload & { username?: string } = {
    slugs: Array.from(new Set(slugs.map((slug) => normalizeSlug(slug)).filter(Boolean))),
    updatedAt: new Date().toISOString(),
  };
  if (username) payload.username = username;
  await store.put(favoritesKey(githubUserId), JSON.stringify(payload));
  return payload;
}

export async function setFavorite(store: FavoritesStore, githubUserId: number | string, slug: string, favorited: boolean, username?: string) {
  const normalized = normalizeSlug(slug);
  const current = await readFavorites(store, githubUserId);
  const nextSlugs = favorited
    ? Array.from(new Set([...current.slugs, normalized]))
    : current.slugs.filter((item) => item !== normalized);
  return writeFavorites(store, githubUserId, nextSlugs, username);
}

export async function readFavoritesWithUsername(store: FavoritesStore, githubUserId: number | string): Promise<{ payload: FavoritesPayload; username?: string }> {
  const raw = await store.get(favoritesKey(githubUserId));
  if (!raw) return { payload: { slugs: [], updatedAt: new Date(0).toISOString() }, username: undefined };
  try {
    const parsed = JSON.parse(raw);
    const username = parsed.username;
    return {
      payload: parseFavorites(raw),
      username: typeof username === 'string' ? username : undefined,
    };
  } catch {
    return { payload: parseFavorites(raw), username: undefined };
  }
}
