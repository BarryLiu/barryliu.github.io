import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { describe, it } from 'node:test';

function read(path) {
  const url = new URL(`../${path}`, import.meta.url);
  assert.ok(existsSync(url), `${path} should exist`);
  return readFileSync(url, 'utf8');
}

describe('server synced favorites', () => {
  it('uses GitHub OAuth for identity and Cloudflare KV for favorite storage', () => {
    const auth = read('functions/_lib/auth.ts');
    const favorites = read('functions/_lib/favorites.ts');
    const api = read('functions/api/favorites.ts');
    const start = read('functions/api/auth/github/start.ts');
    const callback = read('functions/api/auth/github/callback.ts');
    const me = read('functions/api/auth/me.ts');
    const logout = read('functions/api/auth/logout.ts');

    assert.match(start, /github\.com\/login\/oauth\/authorize/);
    assert.match(start, /getGitHubOAuthConfig\(env\)/);
    assert.match(callback, /github\.com\/login\/oauth\/access_token/);
    assert.match(callback, /api\.github\.com\/user/);
    assert.match(callback, /getGitHubOAuthConfig\(env\)/);
    assert.match(auth, /GITHUB_OAUTH_CLIENT_ID/);
    assert.match(auth, /GITHUB_OAUTH_CLIENT_SECRET/);
    assert.match(auth, /AUTH_COOKIE_SECRET/);
    assert.match(auth, /HttpOnly/);
    assert.match(auth, /SameSite=Lax/);
    assert.match(auth, /crypto\.subtle/);
    assert.match(auth, /sanitizeReturnTo/);
    assert.match(me, /authenticated:\s*true/);
    assert.match(logout, /clearCookie\(authCookieName,\s*request\)/);
    assert.match(api, /POST_FAVORITES/);
    assert.match(api, /readSession/);
    assert.match(api, /onRequestGet/);
    assert.match(api, /onRequestPost/);
    assert.match(api, /status:\s*401/);
    assert.match(favorites, /favoritesKey/);
    assert.match(favorites, /github:\$\{githubUserId\}/);
    assert.match(favorites, /setFavorite/);
  });

  it('configures local Cloudflare preview for favorites and documents required secrets', () => {
    const wrangler = read('wrangler.toml');
    const agents = read('AGENTS.md');
    const packageJson = JSON.parse(read('package.json'));

    assert.match(wrangler, /binding = "POST_FAVORITES"/);
    assert.match(wrangler, /id = "[a-f0-9]{32}"/);
    assert.match(wrangler, /preview_id = "[a-f0-9]{32}"/);
    assert.match(agents, /POST_FAVORITES/);
    assert.match(agents, /GITHUB_OAUTH_CLIENT_ID/);
    assert.match(agents, /GITHUB_OAUTH_CLIENT_SECRET/);
    assert.match(agents, /AUTH_COOKIE_SECRET/);
    assert.equal(packageJson.scripts['dev:cloudflare'], 'npm run build && wrangler pages dev dist --kv=POST_STATS --kv=POST_FAVORITES');
  });
});
