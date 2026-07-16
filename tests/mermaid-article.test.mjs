import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { describe, it } from 'node:test';
import purify from 'dompurify';

purify.addHook ??= () => {};
purify.sanitize ??= (value) => value;
globalThis.location ??= new URL('https://www.mrlyj.com/');
globalThis.localStorage ??= {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {},
};

const { default: mermaid } = await import('mermaid');
const { default: zenuml } = await import('@mermaid-js/mermaid-zenuml');
await mermaid.registerExternalDiagrams([zenuml]);

const articleUrl = new URL('../content/posts/tool/mermaid-complete-guide.md', import.meta.url);
const requiredTypes = [
  'Flowchart',
  'Swimlanes',
  'Sequence',
  'Class',
  'Entity Relationship',
  'State',
  'Mindmap',
  'Architecture',
  'Block',
  'C4',
  'Cynefin Framework',
  'Event Modeling',
  'Gantt',
  'Git Graph',
  'Ishikawa',
  'Kanban',
  'Packet',
  'Pie',
  'Quadrant',
  'Radar',
  'Railroad ABNF',
  'Railroad EBNF',
  'Railroad IR',
  'Railroad PEG',
  'Requirement',
  'Sankey',
  'Timeline',
  'TreeView',
  'Treemap',
  'User Journey',
  'Venn',
  'Wardley Map',
  'XY Chart',
  'ZenUML',
];

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function article() {
  assert.ok(existsSync(articleUrl), 'Mermaid guide article should exist');
  return readFileSync(articleUrl, 'utf8');
}

function mermaidBlocks(markdown) {
  return [...markdown.matchAll(/```mermaid\s*\n([\s\S]*?)```/g)].map((match) => match[1].trim());
}

describe('Mermaid complete guide', () => {
  it('uses valid post metadata and covers every documented guide section', () => {
    const markdown = article();

    assert.match(markdown, /^---\n[\s\S]*title:\s*.+Mermaid[\s\S]*date:\s*2026-07-16[\s\S]*postSlug:\s*tool\/mermaid-complete-guide[\s\S]*---/);
    assert.match(markdown, /https:\/\/mermaid\.live\/edit/);
    assert.match(markdown, /https:\/\/mermaid\.js\.org\//);
    assert.match(markdown, /图表选择速查表/);
    assert.match(markdown, /主题与配置/);
    assert.match(markdown, /安全级别/);
    assert.match(markdown, /常见错误/);
    assert.match(markdown, /Review,Revise,2\nRevise,Publish,2/, 'Sankey example must not contain a circular link');

    for (const type of requiredTypes) {
      assert.match(markdown, new RegExp(`^### .+${escapeRegExp(type)}`, 'm'), `${type} section should exist`);
    }

    assert.ok(mermaidBlocks(markdown).length >= requiredTypes.length, 'each diagram type needs a Mermaid example');
  });

  it('parses every Mermaid fenced block with the pinned runtime', async () => {
    const blocks = mermaidBlocks(article());
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'strict',
      suppressErrorRendering: true,
    });

    for (const [index, source] of blocks.entries()) {
      await assert.doesNotReject(
        () => mermaid.parse(source),
        `Mermaid example ${index + 1} failed to parse:\n${source}`,
      );
    }
  });
});
