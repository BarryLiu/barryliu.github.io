import assert from 'node:assert/strict';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';

import { copyStaticAssets } from '../scripts/copy-static-assets.mjs';

describe('static asset copying', () => {
  it('copies colocated Astro post assets into public posts-assets', async () => {
    const tempRoot = await mkdtemp(path.join(tmpdir(), 'static-assets-'));

    try {
      const contentRoot = path.join(tempRoot, 'src/content/posts');
      const publicRoot = path.join(tempRoot, 'public');
      const workAsset = path.join(contentRoot, 'work/assets/image.png');
      const mysqlAsset = path.join(contentRoot, 'skill/mysql/assets/index.png');

      await mkdir(path.dirname(workAsset), { recursive: true });
      await mkdir(path.dirname(mysqlAsset), { recursive: true });
      await writeFile(workAsset, 'work image', 'utf8');
      await writeFile(mysqlAsset, 'mysql image', 'utf8');

      const copied = await copyStaticAssets({ contentRoot, publicRoot, repoRoot: tempRoot });

      assert.deepEqual(copied.sort(), [
        'posts-assets/skill/mysql/assets',
        'posts-assets/work/assets',
      ]);
      assert.equal(
        await readFile(path.join(publicRoot, 'posts-assets/work/assets/image.png'), 'utf8'),
        'work image',
      );
      assert.equal(
        await readFile(path.join(publicRoot, 'posts-assets/skill/mysql/assets/index.png'), 'utf8'),
        'mysql image',
      );
    } finally {
      await rm(tempRoot, { recursive: true, force: true });
    }
  });

  it('ignores legacy Jekyll include images when root images are the active source', async () => {
    const tempRoot = await mkdtemp(path.join(tmpdir(), 'legacy-static-assets-'));

    try {
      const contentRoot = path.join(tempRoot, 'src/content/posts');
      const publicRoot = path.join(tempRoot, 'public');
      const rootImage = path.join(tempRoot, 'images/startnginx.png');
      const legacyImage = path.join(tempRoot, '_includes/images/startnginx.png');

      await mkdir(path.dirname(rootImage), { recursive: true });
      await mkdir(path.dirname(legacyImage), { recursive: true });
      await mkdir(contentRoot, { recursive: true });
      await writeFile(rootImage, 'root image', 'utf8');
      await writeFile(legacyImage, 'legacy image', 'utf8');

      const copied = await copyStaticAssets({ contentRoot, publicRoot, repoRoot: tempRoot });

      assert.deepEqual(copied, ['images']);
      assert.equal(await readFile(path.join(publicRoot, 'images/startnginx.png'), 'utf8'), 'root image');
    } finally {
      await rm(tempRoot, { recursive: true, force: true });
    }
  });
});
