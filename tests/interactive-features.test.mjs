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
