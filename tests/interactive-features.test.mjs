import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { describe, it } from 'node:test';

function read(path) {
  const url = new URL(`../${path}`, import.meta.url);
  assert.ok(existsSync(url), `${path} should exist`);
  return readFileSync(url, 'utf8');
}

describe('interactive site features', () => {
  it('exposes a static global search endpoint and reusable navigation trigger', () => {
    const endpoint = read('src/pages/search.json.ts');
    const nav = read('src/components/CyberNav.astro');
    const search = read('src/components/GlobalSearch.astro');

    assert.match(endpoint, /export async function GET/);
    assert.match(endpoint, /getAllPosts/);
    assert.match(endpoint, /postUrl/);
    assert.match(endpoint, /getDescription/);
    assert.match(search, /data-search-root/);
    assert.match(search, /data-search-input/);
    assert.match(search, /\/search\.json/);
    assert.match(nav, /GlobalSearch/);
    assert.match(nav, /data-search-open/);
  });

  it('keeps the global search dialog usable from the mobile menu', () => {
    const nav = read('src/components/CyberNav.astro');
    const search = read('src/components/GlobalSearch.astro');

    assert.match(nav, /<a href="\/archive\/" data-search-open/);
    assert.match(search, /document\.body\.appendChild\(activeDialog\)/);
  });

  it('normalizes global search queries and keeps the JSON index prerendered', () => {
    const endpoint = read('src/pages/search.json.ts');
    const search = read('src/components/GlobalSearch.astro');

    assert.match(endpoint, /export const prerender = true/);
    assert.match(search, /const normalizeSearchQuery/);
    assert.match(search, /\.normalize\('NFKC'\)/);
    assert.match(search, /document\.addEventListener\('input'/);
    assert.match(search, /event\.target\.matches\('\[data-search-input\]'\)/);
    assert.match(search, /query\.split\(\/\\s\+\/\)/);
    assert.match(search, /matchedTokens > 0/);
    assert.match(search, /matchedTokens === tokens\.length/);
  });

  it('adds article floating actions for back to top and GitHub-backed favorite context', () => {
    const layout = read('src/layouts/PostLayout.astro');
    const actions = read('src/components/PostFloatingActions.astro');
    const favorites = read('src/pages/favorites.astro');
    const authStart = read('functions/api/auth/github/start.ts');
    const authCallback = read('functions/api/auth/github/callback.ts');
    const authMe = read('functions/api/auth/me.ts');
    const authLogout = read('functions/api/auth/logout.ts');
    const authHelper = read('functions/_lib/auth.ts');

    assert.match(layout, /PostFloatingActions/);
    assert.match(layout, /postSlug=\{post\.data\.postSlug\}/);
    assert.match(actions, /data-post-actions/);
    assert.match(actions, /data-scroll-top/);
    assert.match(actions, /data-favorite-toggle/);
    assert.match(actions, /data-favorites-link/);
    assert.match(actions, /href="\/favorites\/"/);
    assert.match(actions, /\/api\/auth\/me/);
    assert.match(actions, /\/api\/favorites/);
    assert.match(actions, /\/api\/auth\/github\/start/);
    assert.match(actions, /请先登录 GitHub，同步收藏到账号/);
    assert.match(actions, /已同步到账号收藏/);
    assert.doesNotMatch(actions, /已收藏，登录 GitHub 评论后可同步反应/);
    assert.doesNotMatch(actions, /flying-fish-favorite:/);
    assert.match(favorites, /data-favorites-app/);
    assert.match(favorites, /\/api\/auth\/me/);
    assert.match(favorites, /\/api\/favorites/);
    assert.match(favorites, /\/api\/auth\/github\/start\?returnTo=\/favorites\//);
    assert.match(favorites, /Cloudflare KV/);
    assert.match(favorites, /\.favorites-shell\s+\[hidden\]/);
    assert.doesNotMatch(favorites, /localStorage/);
    assert.match(favorites, /post\.data\.postSlug/);
    assert.match(authStart, /github\.com\/login\/oauth\/authorize/);
    assert.match(authStart, /createStateCookie/);
    assert.match(authHelper, /GITHUB_OAUTH_CLIENT_ID/);
    assert.match(authHelper, /CF_GITHUB_OAUTH_CLIENT_ID/);
    assert.match(authCallback, /github\.com\/login\/oauth\/access_token/);
    assert.match(authCallback, /api\.github\.com\/user/);
    assert.match(authCallback, /createSessionCookie/);
    assert.match(authMe, /authenticated:\s*true/);
    assert.match(authLogout, /clearCookie/);
  });

  it('supports a persistent zh and en UI language switch', () => {
    const site = read('src/data/site.ts');
    const nav = read('src/components/CyberNav.astro');
    const toggle = read('src/components/LanguageToggle.astro');
    const hero = read('src/components/CyberHero.astro');
    const home = read('src/pages/index.astro');
    const footer = read('src/components/CyberFooter.astro');

    assert.match(site, /labelEn/);
    assert.match(nav, /LanguageToggle/);
    assert.match(toggle, /flying-fish-lang/);
    assert.match(toggle, /data-i18n-zh/);
    assert.match(toggle, /data-i18n-en/);
    assert.match(hero, /data-i18n-en/);
    assert.match(home, /data-i18n-en/);
    assert.match(footer, /data-i18n-en/);
  });

  it('keeps the homepage structure aligned with the cyber aquarium design file', () => {
    const nav = read('src/components/CyberNav.astro');
    const hero = read('src/components/CyberHero.astro');
    const card = read('src/components/ProjectCard.astro');
    const home = read('src/pages/index.astro');

    assert.match(nav, /nav-panel/);
    assert.match(nav, /min-height:\s*92px/);
    assert.match(hero, /hero-card/);
    assert.match(hero, /border-radius:\s*34px/);
    assert.match(card, /border-radius:\s*28px/);
    assert.match(card, /border-radius:\s*32px/);
    assert.match(home, /home-stage/);
  });

  it('surfaces RSS in the top header and uses the current contact email everywhere', () => {
    const site = read('src/data/site.ts');
    const nav = read('src/components/CyberNav.astro');
    const comment = read('src/components/CommentPanel.astro');
    const about = read('src/pages/about.astro');

    assert.match(site, /email:\s*'barry\.lyj@outlook\.com'/);
    assert.doesNotMatch(site, /1025587160@qq\.com/);
    assert.match(nav, /href="\/rss\.xml"/);
    assert.match(nav, /data-i18n-zh="RSS 订阅"/);
    assert.match(nav, /data-i18n-en="RSS"/);
    assert.match(nav, /site\.email/);
    assert.match(comment, /site\.email/);
    assert.match(about, /site\.email/);
  });

  it('configures GitHub discussion comments on post pages', () => {
    const site = read('src/data/site.ts');
    const comment = read('src/components/CommentPanel.astro');

    assert.match(site, /comments/);
    assert.match(site, /provider:\s*'giscus'/);
    assert.match(site, /repo:\s*'BarryLiu\/barryliu\.github\.io'/);
    assert.match(site, /repoId:\s*'MDEwOlJlcG9zaXRvcnk0ODA5NTc0OQ=='/);
    assert.match(site, /category:\s*'General'/);
    assert.match(site, /categoryId:\s*'DIC_kwDOAt3iBc4C9uWC'/);
    assert.match(site, /mapping:\s*'pathname'/);
    assert.match(comment, /commentsEnabled/);
    assert.match(comment, /https:\/\/giscus\.app\/client\.js/);
    assert.match(comment, /data-repo=\{comments\.repo\}/);
    assert.match(comment, /data-repo-id=\{comments\.repoId\}/);
    assert.match(comment, /data-category-id=\{comments\.categoryId\}/);
    assert.match(comment, /data-theme=\{comments\.theme\}/);
  });
});
