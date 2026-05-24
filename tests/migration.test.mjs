import assert from 'node:assert/strict';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';

import {
  buildMigratedPost,
  derivePostIdentity,
  normalizeList,
  rewriteJekyllMarkdown,
} from '../scripts/migrate-posts.mjs';

describe('post migration helpers', () => {
  it('derives a stable Astro content id from nested Jekyll post paths', () => {
    assert.deepEqual(
      derivePostIdentity('_posts/ailearn/01-numpy-pandas/2026-04-12-numpy-basic.md'),
      {
        date: '2026-04-12',
        slug: 'ailearn/01-numpy-pandas/numpy-basic',
        outputPath: 'ailearn/01-numpy-pandas/numpy-basic.md',
        topic: 'ailearn',
      },
    );

    assert.deepEqual(
      derivePostIdentity('_posts/skill/2016-08-9-sql-note1.md'),
      {
        date: '2016-08-09',
        slug: 'skill/sql-note1',
        outputPath: 'skill/sql-note1.md',
        topic: 'skill',
      },
    );
  });

  it('normalizes scalar and array taxonomy values', () => {
    assert.deepEqual(normalizeList('JavaScript Ajax URL'), ['JavaScript', 'Ajax', 'URL']);
    assert.deepEqual(normalizeList('[Mac, Docker, PHP]'), ['Mac', 'Docker', 'PHP']);
    assert.deepEqual(normalizeList(['AI', 'RAG']), ['AI', 'RAG']);
    assert.deepEqual(normalizeList(''), []);
  });

  it('rewrites Jekyll-only markdown syntax to portable markdown links', () => {
    const source = [
      '* content',
      '{:toc}',
      '[下一篇]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-02-machine-learning %})',
      '![img]({{ site.baseurl }}/images/demo.png)',
      '![old](../../images/fiddler_autoresponder.png)',
      '![alt](./../../images/fiddler_autoresponder.png)',
      '![../../images/skill/jenkins-console.png](jenkins-console.png)',
      '![win](\\images\\bluetooth\\psensor-all.png)',
      '![local](.\\assets\\image.png)',
      '![legacy](_posts/skill/startnginx.png)',
    ].join('\n');

    assert.equal(
      rewriteJekyllMarkdown(source, { sourceDir: 'skill' }),
      [
        '[下一篇](/posts/ailearn/02-machine-learning/)',
        '![img](/images/demo.png)',
        '![old](/images/fiddler_autoresponder.png)',
        '![alt](/images/fiddler_autoresponder.png)',
        '![../../images/skill/jenkins-console.png](/images/skill/jenkins-console.png)',
        '![win](/images/bluetooth/psensor-all.png)',
        '![local](/posts-assets/skill/assets/image.png)',
        '![legacy](/images/startnginx.png)',
      ].join('\n'),
    );
  });

  it('builds normalized frontmatter when the source frontmatter is missing', () => {
    const migrated = buildMigratedPost({
      sourcePath: '_posts/skill/2023-05-25-dingding-login.md',
      raw: '### 钉钉扫码登陆\n\n正文',
    });

    assert.match(migrated, /^---\ntitle: "钉钉扫码登陆"\ndate: 2023-05-25\n/);
    assert.match(migrated, /categories:\n  - skill\n/);
    assert.match(migrated, /tags: \[\]\n/);
    assert.match(migrated, /postSlug: "skill\/dingding-login"\n/);
    assert.match(migrated, /### 钉钉扫码登陆\n\n正文\n$/);
  });

  it('preserves existing Astro posts while migrating remaining Jekyll posts', async () => {
    const { migratePostsInto } = await import('../scripts/migrate-posts.mjs');
    assert.equal(typeof migratePostsInto, 'function');

    const tempRoot = await mkdtemp(path.join(tmpdir(), 'post-migration-'));

    try {
      const sourceRoot = path.join(tempRoot, '_posts');
      const targetRoot = path.join(tempRoot, 'src/content/posts');
      const existingTarget = path.join(targetRoot, 'already-migrated.md');
      const sourcePost = path.join(sourceRoot, 'skill/2024-01-02-new-post.md');

      await mkdir(path.dirname(sourcePost), { recursive: true });
      await mkdir(path.dirname(existingTarget), { recursive: true });
      await writeFile(existingTarget, '---\ntitle: Existing\ndate: 2024-01-01\n---\n\nKeep me\n', 'utf8');
      await writeFile(sourcePost, '---\ntitle: New Post\n---\n\nNew body\n', 'utf8');

      const count = await migratePostsInto({ sourceRoot, targetRoot });

      assert.equal(count, 1);
      assert.equal(await readFile(existingTarget, 'utf8'), '---\ntitle: Existing\ndate: 2024-01-01\n---\n\nKeep me\n');
      assert.match(
        await readFile(path.join(targetRoot, 'skill/new-post.md'), 'utf8'),
        /postSlug: "skill\/new-post"/,
      );
    } finally {
      await rm(tempRoot, { recursive: true, force: true });
    }
  });

  it('treats a removed Jekyll post source directory as no remaining posts', async () => {
    const { migratePostsInto } = await import('../scripts/migrate-posts.mjs');
    const tempRoot = await mkdtemp(path.join(tmpdir(), 'missing-post-source-'));

    try {
      const count = await migratePostsInto({
        sourceRoot: path.join(tempRoot, '_posts'),
        targetRoot: path.join(tempRoot, 'src/content/posts'),
      });

      assert.equal(count, 0);
    } finally {
      await rm(tempRoot, { recursive: true, force: true });
    }
  });

  it('migrates Jekyll drafts into an Astro drafts collection', async () => {
    const { migrateDraftsInto } = await import('../scripts/migrate-posts.mjs');
    assert.equal(typeof migrateDraftsInto, 'function');

    const tempRoot = await mkdtemp(path.join(tmpdir(), 'draft-migration-'));

    try {
      const sourceRoot = path.join(tempRoot, '_drafts');
      const targetRoot = path.join(tempRoot, 'src/content/drafts');
      const sourceDraft = path.join(sourceRoot, 'android/2015-7-13-sample-draft.md');

      await mkdir(path.dirname(sourceDraft), { recursive: true });
      await writeFile(
        sourceDraft,
        '---\ntitle: Sample Draft\ncategory: Android\ntags: Android Test\n---\n\nDraft body\n',
        'utf8',
      );

      const count = await migrateDraftsInto({ sourceRoot, targetRoot });
      const migrated = await readFile(path.join(targetRoot, 'android/sample-draft.md'), 'utf8');

      assert.equal(count, 1);
      assert.match(migrated, /postSlug: "android\/sample-draft"/);
      assert.match(migrated, /categories:\n  - Android\n/);
      assert.match(migrated, /draft: true\n---/);
      assert.match(migrated, /Draft body\n$/);
    } finally {
      await rm(tempRoot, { recursive: true, force: true });
    }
  });
});
