import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { describe, it } from 'node:test';

function read(path) {
  return readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
}

describe('project configuration', () => {
  it('documents Astro and Cloudflare Pages as the active stack', () => {
    const agents = read('AGENTS.md');

    assert.match(agents, /Astro/);
    assert.match(agents, /Cloudflare Pages/);
    assert.doesNotMatch(agents, /Jekyll \/ GitHub Pages 博客/);
    assert.doesNotMatch(agents, /docker compose run --rm jekyll jekyll build/);
  });

  it('uses an Astro Docker Compose service instead of the old Jekyll container', () => {
    const compose = read('docker-compose.yml');

    assert.match(compose, /astro:/);
    assert.match(compose, /npm run dev/);
    assert.match(compose, /4321:4321/);
    assert.doesNotMatch(compose, /jekyll/);
  });

  it('keeps Cloudflare deployment configuration in source control', () => {
    const workflow = read('.github/workflows/pages.yml');
    const wrangler = read('wrangler.toml');
    const packageJson = JSON.parse(read('package.json'));

    assert.match(workflow, /Cloudflare Pages/);
    assert.match(workflow, /cloudflare\/wrangler-action/);
    assert.match(wrangler, /pages_build_output_dir = "dist"/);
    assert.equal(packageJson.scripts['deploy:cloudflare'], 'npm run build && wrangler pages deploy dist');
  });

  it('keeps homepage project data aligned with the design sections', () => {
    const projects = read('src/data/projects.ts');

    assert.match(projects, /ai-knowledge-navigator/);
    assert.match(projects, /code-assistant/);
    assert.match(projects, /model-deploy/);
    assert.match(projects, /sign-tool/);
    assert.match(projects, /ai-roadmap/);
  });
});
