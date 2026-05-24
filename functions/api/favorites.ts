import { readSession, type AuthEnv } from '../_lib/auth';
import { readFavorites, setFavorite } from '../_lib/favorites';
import { json } from '../_lib/http';
import { normalizeSlug } from '../_lib/postStats';

type Env = AuthEnv & {
  POST_FAVORITES: KVNamespace;
};

function favoriteResponse(payload: { slugs: string[]; updatedAt: string }) {
  return {
    slugs: payload.slugs,
    count: payload.slugs.length,
    updatedAt: payload.updatedAt,
  };
}

export const onRequestGet = async ({ request, env }: { request: Request; env: Env }) => {
  const session = await readSession(request, env);
  if (!session) return json({ error: 'unauthorized' }, { status: 401 });
  return json(favoriteResponse(await readFavorites(env.POST_FAVORITES, session.user.id)));
};

export const onRequestPost = async ({ request, env }: { request: Request; env: Env }) => {
  const session = await readSession(request, env);

  const body = (await request.json().catch(() => ({}))) as { slug?: string; favorited?: boolean; giscusUser?: { id?: string | number; username?: string } };
  const slug = normalizeSlug(body.slug);
  if (!slug) return json({ error: 'missing_slug' }, { status: 400 });
  if (typeof body.favorited !== 'boolean') return json({ error: 'missing_favorited' }, { status: 400 });

  const giscusUserId = body.giscusUser?.id ? String(body.giscusUser.id) : null;
  const username = body.giscusUser?.username;

  if (!session && !giscusUserId) return json({ error: 'unauthorized' }, { status: 401 });

  const userId = giscusUserId || String(session!.user.id);
  return json(favoriteResponse(await setFavorite(env.POST_FAVORITES, userId, slug, body.favorited, username)));
};
