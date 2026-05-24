import { applyVote, incrementView, normalizeSlug, readStats, type PostVote } from '../_lib/postStats';

type Env = {
  POST_STATS: KVNamespace;
};

function json(body: unknown, init: ResponseInit = {}) {
  return new Response(JSON.stringify(body), {
    ...init,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store',
      ...(init.headers ?? {}),
    },
  });
}

export const onRequestGet = async ({ request, env }: { request: Request; env: Env }) => {
  const url = new URL(request.url);
  const slug = normalizeSlug(url.searchParams.get('slug'));
  if (!slug) return json({ error: 'missing_slug' }, { status: 400 });
  const stats = await readStats(env.POST_STATS, slug);
  return json(stats);
};

function parseVote(raw: unknown): PostVote | undefined {
  return raw === 'like' || raw === 'dislike' ? raw : undefined;
}

export const onRequestPost = async ({ request, env }: { request: Request; env: Env }) => {
  const body = (await request.json().catch(() => ({}))) as { slug?: string; action?: string; previousVote?: string };
  const slug = normalizeSlug(body.slug);
  if (!slug) return json({ error: 'missing_slug' }, { status: 400 });
  if (body.action === 'view') return json(await incrementView(env.POST_STATS, slug));
  if (body.action === 'like' || body.action === 'dislike') {
    return json(await applyVote(env.POST_STATS, slug, body.action, parseVote(body.previousVote)));
  }
  return json({ error: 'invalid_action' }, { status: 400 });
};
