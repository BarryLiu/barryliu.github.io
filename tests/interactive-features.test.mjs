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

  it('supports light and dark color themes without a startup flash', () => {
    const layout = read('src/layouts/BaseLayout.astro');
    const nav = read('src/components/CyberNav.astro');
    const toggle = read('src/components/ThemeToggle.astro');
    const tokens = read('src/styles/tokens.css');
    const global = read('src/styles/global.css');

    assert.match(layout, /flying-fish-theme/);
    assert.match(layout, /prefers-color-scheme:\s*dark/);
    assert.match(layout, /data-color-theme/);
    assert.match(nav, /ThemeToggle/);
    assert.match(toggle, /const modes = \['light', 'dark'\]/);
    assert.doesNotMatch(toggle, /data-theme-icon-system/);
    assert.doesNotMatch(toggle, /跟随系统/);
    assert.match(toggle, /light/);
    assert.match(toggle, /dark/);
    assert.match(toggle, /localStorage/);
    assert.match(toggle, /matchMedia/);
    assert.match(toggle, /media\.matches \? 'dark' : 'light'/);
    assert.match(toggle, /flying-fish:theme/);
    assert.match(tokens, /data-color-theme=['"]light['"]/);
    assert.match(global, /--page-background/);
  });

  it('keeps the light cyber palette clean and the desktop header compact', () => {
    const nav = read('src/components/CyberNav.astro');
    const hero = read('src/components/CyberHero.astro');
    const tokens = read('src/styles/tokens.css');

    assert.match(tokens, /--hero-background/);
    assert.match(hero, /var\(--hero-background\)/);
    assert.match(hero, /linear-gradient\(180deg, #fbfdff/);
    assert.match(hero, /linear-gradient\(180deg, #1684a5/);
    assert.doesNotMatch(hero, /background-size:\s*44px 44px/);
    assert.match(hero, /--hero-heading-start/);
    assert.match(nav, /desktop-actions[^}]*theme-toggle/s);
    assert.match(nav, /data-theme-label[^}]*display:\s*none/s);
    assert.match(nav, /rss-link span[^}]*display:\s*none/s);
    assert.match(nav, /contact[^}]*border:\s*0/s);
  });

  it('uses theme-aware surfaces across home search taxonomy and post pages', () => {
    const tokens = read('src/styles/tokens.css');
    const home = read('src/pages/index.astro');
    const search = read('src/components/GlobalSearch.astro');
    const taxonomy = read('src/components/TaxonomySwitch.astro');
    const postLayout = read('src/layouts/PostLayout.astro');
    const postStats = read('src/components/PostStats.astro');
    const postActions = read('src/components/PostFloatingActions.astro');

    assert.match(tokens, /--surface-card/);
    assert.match(tokens, /--surface-soft/);
    assert.match(tokens, /--surface-strong/);
    assert.match(tokens, /--surface-overlay/);
    assert.match(tokens, /--surface-grid/);
    assert.match(home, /var\(--surface-card\)/);
    assert.match(search, /var\(--surface-overlay\)/);
    assert.match(search, /var\(--surface-grid\)/);
    assert.match(taxonomy, /var\(--surface-soft\)/);
    assert.match(postLayout, /var\(--surface-card\)/);
    assert.match(postStats, /var\(--surface-soft\)/);
    assert.match(postActions, /var\(--surface-strong\)/);
  });

  it('presents a structured about page and a visible platform-aware search shortcut', () => {
    const about = read('src/pages/about.astro');
    const nav = read('src/components/CyberNav.astro');
    const search = read('src/components/GlobalSearch.astro');

    assert.match(about, /about-hero/);
    assert.match(about, /capability-model/);
    assert.match(about, /capability-radar/);
    assert.match(about, /radar-label/);
    assert.match(about, /Java 后端<\/text>/);
    assert.match(about, /前端开发<\/text>/);
    assert.match(about, /AI 工程<\/text>/);
    assert.match(about, /系统设计<\/text>/);
    assert.match(about, /自动化运维<\/text>/);
    assert.match(about, /问题排查<\/text>/);
    assert.match(about, /capability-list/);
    assert.match(about, /tech-stack-matrix/);
    assert.match(about, /AI 工程/);
    assert.match(about, /自动化运维/);
    assert.match(about, /前端工程/);
    assert.match(about, /about-achievements/);
    assert.match(about, /about-contact-grid/);
    assert.match(about, /用工程方法学习 AI/);
    assert.match(about, /站点运行环境/);
    assert.doesNotMatch(about, /Site runtime/);
    assert.match(about, /10 年 Java 后端开发经验/);
    assert.match(about, /7 年前端与全栈实践/);
    assert.match(about, /10 年 Java 后端、7 年前端，如今专注 AI 工程与全栈实践。/);
    assert.match(about, /10\+ 年/);
    assert.match(about, /后端开发经验/);
    assert.doesNotMatch(about, /Lv\. 86/);
    assert.match(about, /#006f86/);
    assert.match(about, /Java 后端/);
    assert.match(about, /前端工程/);
    assert.match(about, /AI 工程/);
    assert.match(about, /Cloudflare Pages/);
    assert.match(search, /Ctrl\+K/);
    assert.match(search, /⌘K/);
    assert.match(nav, /search-trigger[^}]*min-width/s);
    assert.match(nav, /@media \(max-width:\s*960px\)[\s\S]*search-trigger kbd[^}]*display:\s*none/);
  });

  it('keeps the homepage structure aligned with the cyber aquarium design file', () => {
    const nav = read('src/components/CyberNav.astro');
    const hero = read('src/components/CyberHero.astro');
    const card = read('src/components/ProjectCard.astro');
    const home = read('src/pages/index.astro');

    assert.match(nav, /nav-panel/);
    assert.match(nav, /min-height:\s*70px/);
    assert.match(hero, /hero-card/);
    assert.match(hero, /border-radius:\s*34px/);
    assert.match(card, /border-radius:\s*28px/);
    assert.match(card, /border-radius:\s*32px/);
    assert.match(home, /home-stage/);
  });

  it('renders a narrative flying-fish motion scene without radar ornaments', () => {
    const hero = read('src/components/CyberHero.astro');

    assert.match(hero, /class="aquarium-scene"/);
    assert.match(hero, /class="flying-fish"/);
    assert.match(hero, /class="fish-wing/);
    assert.match(hero, /class="trail-particle/);
    assert.match(hero, /class="sky-stage"/);
    assert.match(hero, /class="ocean-stage"/);
    assert.match(hero, /class="sea-surface"/);
    assert.match(hero, /class="splash-burst/);
    assert.match(hero, /class="orbit-system"/);
    assert.match(hero, /class="orbit-keyword/);
    assert.match(hero, /JAVA · SPRING/);
    assert.match(hero, /TYPESCRIPT · VUE/);
    assert.match(hero, /PYTHON · FASTAPI/);
    assert.match(hero, /AGENT · RAG/);
    assert.match(hero, /DOCKER · LINUX/);
    assert.match(hero, /class="orbit-keyword orbit-python"/);
    assert.doesNotMatch(hero, />RAG CORE</);
    assert.doesNotMatch(hero, />AGENT OPS</);
    assert.doesNotMatch(hero, />MLOPS</);
    assert.doesNotMatch(hero, />CODE TOOLS</);
    assert.match(hero, /class="fish-artwork"/);
    assert.match(hero, /class="wing-echo/);
    assert.match(hero, /@keyframes fish-flight/);
    assert.match(hero, /@keyframes wing-glide/);
    assert.match(hero, /@keyframes trail-drift/);
    assert.match(hero, /@keyframes camera-rise/);
    assert.match(hero, /@keyframes surface-wave/);
    assert.match(hero, /@keyframes splash-break/);
    assert.match(hero, /@keyframes keyword-orbit/);
    assert.match(hero, /@keyframes wing-echo-flight/);
    assert.match(hero, /\.fish-artwork[^}]*transform:\s*scaleX\(-1\)/s);
    assert.match(hero, /\.orbit-system[^}]*transform:\s*none/s);
    assert.match(hero, /prefers-reduced-motion:\s*reduce/);
    assert.doesNotMatch(hero, /class="ring/);
    assert.doesNotMatch(hero, /class="node/);
    assert.doesNotMatch(hero, /class="hud"/);
    assert.doesNotMatch(hero, /var\(--color-lime\)/);
  });

  it('adds a compact scroll state and shared desktop navigation highlight', () => {
    const nav = read('src/components/CyberNav.astro');
    const tokens = read('src/styles/tokens.css');

    assert.match(nav, /data-nav-shell/);
    assert.match(nav, /data-nav-links/);
    assert.match(nav, /data-nav-highlight/);
    assert.match(nav, /data-compact/);
    assert.match(nav, /window\.scrollY\s*>\s*72/);
    assert.match(nav, /window\.scrollY\s*>\s*24/);
    assert.match(nav, /requestAnimationFrame/);
    assert.match(nav, /--nav-highlight-x/);
    assert.match(nav, /--nav-highlight-width/);
    assert.match(nav, /--nav-expanded-width/);
    assert.match(nav, /--nav-compact-width/);
    assert.match(nav, /box-shadow:[^;]*var\(--nav-item-shadow/s);
    assert.doesNotMatch(nav, /nav-border-scan/);
    assert.doesNotMatch(nav, /nav-breathe/);
    assert.match(tokens, /--nav-background:\s*#[0-9a-f]{6}/i);
    assert.match(tokens, /--nav-background-compact:\s*#[0-9a-f]{6}/i);
    assert.match(tokens, /--nav-item-shadow/);
    assert.match(nav, /height:\s*94px/);
    assert.match(nav, /will-change:\s*width,\s*transform/);
    assert.doesNotMatch(nav, /backdrop-filter/);
  });

  it('keeps header motion accessible and mobile navigation progressively enhanced', () => {
    const nav = read('src/components/CyberNav.astro');

    assert.match(nav, /:focus-visible/);
    assert.match(nav, /prefers-reduced-motion:\s*reduce/);
    assert.match(nav, /details\[open\]/);
    assert.match(nav, /aria-current/);
    assert.match(nav, /passive:\s*true/);
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
