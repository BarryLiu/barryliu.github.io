import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { describe, it } from 'node:test';

function read(path) {
  const url = new URL(`../${path}`, import.meta.url);
  assert.ok(existsSync(url), `${path} should exist`);
  return readFileSync(url, 'utf8');
}

describe('flying fish brand assets', () => {
  it('ships a consistent transparent SVG logo family', () => {
    const mark = read('public/assets/brand/logo-mark.svg');
    const lockup = read('public/assets/brand/logo.svg');
    const favicon = read('public/assets/brand/favicon.svg');

    assert.match(mark, /viewBox="0 0 120 84"/);
    assert.match(mark, /id="fish-body-gradient"/);
    assert.match(mark, /data-part="pectoral-fin"/);
    assert.match(mark, /data-part="water-arc"/);
    assert.doesNotMatch(mark, /<rect[^>]+(?:width="120"|width="100%")/);

    assert.match(lockup, /viewBox="0 0 360 96"/);
    assert.match(lockup, /想飞的鱼/);
    assert.match(lockup, /Flying Fish Lab/);
    assert.match(lockup, /data-part="pectoral-fin"/);
    assert.doesNotMatch(lockup, /<rect[^>]+(?:width="360"|width="100%")/);

    assert.match(favicon, /viewBox="0 0 64 64"/);
    assert.match(favicon, /data-part="pectoral-fin"/);
    assert.match(favicon, /data-part="water-arc"/);
    assert.doesNotMatch(favicon, /data-part="fin-ray"/);
  });

  it('uses the new mark in the reusable site logo and favicon link', () => {
    const logo = read('src/components/CyberLogo.astro');
    const layout = read('src/layouts/BaseLayout.astro');

    assert.match(logo, /viewBox="0 0 120 84"/);
    assert.match(logo, /class="pectoral-fin"/);
    assert.match(logo, /class="water-arc"/);
    assert.match(logo, /data-i18n-zh="想飞的鱼"/);
    assert.match(layout, /href="\/assets\/brand\/favicon\.svg"/);
  });
});
