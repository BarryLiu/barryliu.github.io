import assert from 'node:assert/strict';
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
});
