import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { describe, it } from 'node:test';

function read(path) {
  const url = new URL(`../${path}`, import.meta.url);
  assert.ok(existsSync(url), `${path} should exist`);
  return readFileSync(url, 'utf8');
}

describe('Mermaid article rendering', () => {
  it('pins Mermaid and loads the renderer from the post layout', () => {
    const packageJson = JSON.parse(read('package.json'));
    const layout = read('src/layouts/PostLayout.astro');

    assert.equal(packageJson.dependencies.mermaid, '11.16.0');
    assert.match(layout, /import MermaidRenderer from ['"]\.\.\/components\/MermaidRenderer\.astro['"]/);
    assert.match(layout, /<MermaidRenderer\s*\/>/);
  });

  it('renders fenced Mermaid source safely and keeps a readable fallback', () => {
    const renderer = read('src/components/MermaidRenderer.astro');

    assert.match(renderer, /code\.language-mermaid/);
    assert.match(renderer, /await import\(['"]mermaid['"]\)/);
    assert.match(renderer, /securityLevel:\s*['"]strict['"]/);
    assert.match(renderer, /startOnLoad:\s*false/);
    assert.match(renderer, /suppressErrorRendering:\s*true/);
    assert.match(renderer, /mermaid\.render/);
    assert.match(renderer, /data-mermaid-processed/);
    assert.match(renderer, /mermaid-source/);
    assert.match(renderer, /data-mermaid-copy/);
    assert.match(renderer, /navigator\.clipboard/);
    assert.match(renderer, /mermaid-error/);
    assert.match(renderer, /overflow-x:\s*auto/);
    assert.match(renderer, /var\(--color-cyan\)/);
    assert.match(renderer, /var\(--color-magenta\)/);
  });
});
