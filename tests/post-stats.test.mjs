import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { describe, it } from 'node:test';

function read(path) {
  const url = new URL(`../${path}`, import.meta.url);
  assert.ok(existsSync(url), `${path} should exist`);
  return readFileSync(url, 'utf8');
}

describe('post stats', () => {
  it('adds an article stats component to post pages', () => {
    const layout = read('src/layouts/PostLayout.astro');
    const component = read('src/components/PostStats.astro');
    const site = read('src/data/site.ts');

    assert.match(layout, /import PostStats/);
    assert.match(layout, /import \{ site \}/);
    assert.match(layout, /postStatsEnabled/);
    assert.match(layout, /postStats\?\.\s*enabled\s*===\s*true/);
    assert.match(layout, /variant="inline"/);
    assert.match(layout, /variant="compact"/);
    assert.match(site, /postStats/);
    assert.match(site, /enabled:\s*true/);
    assert.match(component, /variant/);
    assert.match(component, /data-post-stats/);
    assert.match(component, /data-post-stats-variant/);
    assert.match(component, /data-post-views/);
    assert.match(component, /data-post-stat-button/);
    assert.match(component, /data-post-like/);
    assert.match(component, /data-post-dislike/);
    assert.match(component, /viewedSlugs/);
    assert.match(component, /\/api\/post-stats/);
    assert.match(component, /localStorage/);
  });

  it('provides a Cloudflare Pages Function for views likes and dislikes', () => {
    const api = read('functions/api/post-stats.ts');
    const store = read('functions/_lib/postStats.ts');

    assert.match(api, /onRequestGet/);
    assert.match(api, /onRequestPost/);
    assert.match(api, /POST_STATS/);
    assert.match(store, /views/);
    assert.match(store, /likes/);
    assert.match(store, /dislikes/);
    assert.match(store, /incrementView/);
    assert.match(store, /applyVote/);
  });

  it('documents and configures the Cloudflare KV binding', () => {
    const wrangler = read('wrangler.toml');
    const agents = read('AGENTS.md');
    const packageJson = JSON.parse(read('package.json'));

    assert.match(wrangler, /binding = "POST_STATS"/);
    assert.match(wrangler, /preview_id = "local_post_stats_preview"/);
    assert.match(agents, /POST_STATS/);
    assert.match(agents, /api\/post-stats/);
    assert.match(agents, /post-stats/);
    assert.equal(packageJson.scripts['dev:cloudflare'], 'npm run build && wrangler pages dev dist --kv=POST_STATS');
  });
});
