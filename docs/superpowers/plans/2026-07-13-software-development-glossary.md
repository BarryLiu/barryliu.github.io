# Software Development Glossary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a publishable interactive software-development knowledge map whose terms expose concise definitions through accessible tooltips while algorithms, GoF patterns, and comparison topics remain readable as tables.

**Architecture:** Store ordinary glossary terms as typed build-time data grouped by domain, render them through focused Astro components, and compose the long-form article in MDX. Desktop hover and keyboard focus work through CSS, while one delegated client-side handler adds click and Escape behavior for touch devices without registering listeners per term.

**Tech Stack:** Astro 5, TypeScript, MDX via `@astrojs/mdx`, Astro Content Collections, scoped Astro CSS, Node built-in test runner.

---

## File map

- Create `src/data/software-development-glossary.ts`: glossary types plus ordered section and term data.
- Create `src/components/glossary/TermTooltip.astro`: semantic term trigger and tooltip content for one term.
- Create `src/components/glossary/TermGroup.astro`: group heading, description, and compact list rendering.
- Create `src/components/glossary/GlossaryMap.astro`: renders ordered sections and owns the single delegated interaction handler.
- Create `content/posts/tool/software-development-glossary.mdx`: article frontmatter, introduction, interactive glossary, algorithm tables, GoF table, comparison tables, and learning paths.
- Create `tests/software-development-glossary.test.mjs`: structural, coverage, accessibility, and content-regression checks.
- Modify `src/styles/global.css`: only if rendered MDX tables need a shared horizontal-scroll rule that cannot be kept inside the glossary component; prefer component-scoped styles first.

Do not modify the existing `content/posts/ailearn/llm-technology-glossary.md`, Python test deletions, `pyproject.toml`, `uv.lock`, brand assets, deployment configuration, or content migration scripts.

### Task 1: Lock down the glossary data contract and minimum coverage

**Files:**
- Create: `tests/software-development-glossary.test.mjs`
- Create: `src/data/software-development-glossary.ts`

- [ ] **Step 1: Write the failing data-contract and coverage tests**

Create a Node test that reads the TypeScript source as text, following the repository's existing source-level regression-test style:

```js
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (relativePath) => readFile(path.join(repoRoot, relativePath), 'utf8');

test('software glossary defines typed, ordered sections with standalone descriptions', async () => {
  const source = await read('src/data/software-development-glossary.ts');
  assert.match(source, /export interface GlossaryTerm/);
  assert.match(source, /name: string/);
  assert.match(source, /english\?: string/);
  assert.match(source, /description: string/);
  assert.match(source, /export const glossarySections/);
});

test('software glossary covers the major software-development domains', async () => {
  const source = await read('src/data/software-development-glossary.ts');
  const requiredTerms = [
    '链表', '红黑树', '布隆过滤器', '幂等', '限流', '熔断',
    'MVCC', 'CAP', 'Raft', 'OAuth 2.0', 'OpenTelemetry',
    'Kubernetes', 'WebAssembly', 'MCP',
  ];
  for (const term of requiredTerms) assert.match(source, new RegExp(term));
});
```

- [ ] **Step 2: Run the targeted test and confirm it fails**

Run: `node --test tests/software-development-glossary.test.mjs`

Expected: FAIL with `ENOENT` for `src/data/software-development-glossary.ts`.

- [ ] **Step 3: Add the typed data model and the complete ordered section skeleton**

Create the data file with these public types and section identifiers:

```ts
export interface GlossaryTerm {
  name: string;
  english?: string;
  description: string;
  aliases?: string[];
}

export interface GlossaryGroup {
  title: string;
  description?: string;
  terms: GlossaryTerm[];
}

export interface GlossarySection {
  id: string;
  title: string;
  introduction: string;
  groups: GlossaryGroup[];
}

export const glossarySections: GlossarySection[] = [
  { id: 'software-engineering', title: '软件开发与软件工程', introduction: '描述软件从想法到持续演进所使用的流程、约束与协作机制。', groups: [] },
  { id: 'math-and-computing', title: '数学、计算机组成与操作系统', introduction: '解释程序运行所依赖的数学表达、硬件结构与系统抽象。', groups: [] },
  { id: 'data-structures', title: '数据结构', introduction: '描述数据在内存或存储系统中的组织方式及其操作成本。', groups: [] },
  { id: 'programming-languages', title: '编程语言与编程范式', introduction: '覆盖语言执行、类型、内存、抽象和程序组织方式。', groups: [] },
  { id: 'application-development', title: 'API、前端、后端与客户端开发', introduction: '覆盖现代应用的接口、交互、服务端和跨平台实现机制。', groups: [] },
  { id: 'data-systems', title: '数据库、缓存、搜索与消息系统', introduction: '覆盖数据的持久化、索引、加速、检索和异步传递。', groups: [] },
  { id: 'distributed-architecture', title: '分布式系统与软件架构', introduction: '覆盖跨节点协作、一致性、容错和系统边界设计。', groups: [] },
  { id: 'security-and-quality', title: '安全、测试与代码质量', introduction: '覆盖风险控制、验证策略和长期可维护性。', groups: [] },
  { id: 'delivery-and-cloud', title: 'Git、构建、交付、云原生与运维', introduction: '覆盖从源码到生产环境的自动化、基础设施和运行保障。', groups: [] },
  { id: 'performance-and-data', title: '性能、可观测性与数据工程', introduction: '覆盖系统测量、瓶颈分析和数据处理平台。', groups: [] },
  { id: 'ecosystems-and-frontier', title: '语言生态、框架与前沿技术', introduction: '作为主流技术生态与新兴软件方向的快速索引。', groups: [] },
];
```

Populate every section with clearly named groups and complete `GlossaryTerm` entries. Each `description` must be one self-contained Chinese sentence. Include the full set agreed in the design: development process, mathematics, hardware, operating systems, encoding, data structures, language concepts, paradigms, API/backend/frontend/mobile, databases/NoSQL/search/vector storage/cache/messaging, networking, distributed systems, architecture, concurrency/availability, security, testing, Git/build/CI/CD/Linux, containers/cloud, observability/performance/data engineering, mainstream languages/frameworks, UI/UX/project collaboration, AI-assisted development, and frontier topics.

- [ ] **Step 4: Run the targeted test and confirm it passes**

Run: `node --test tests/software-development-glossary.test.mjs`

Expected: 2 tests PASS.

- [ ] **Step 5: Commit only the data contract and test**

```bash
git add tests/software-development-glossary.test.mjs src/data/software-development-glossary.ts
git commit -m "整理软件开发术语数据"
```

### Task 2: Build the accessible tooltip and group components

**Files:**
- Modify: `tests/software-development-glossary.test.mjs`
- Create: `src/components/glossary/TermTooltip.astro`
- Create: `src/components/glossary/TermGroup.astro`

- [ ] **Step 1: Add failing accessibility and rendering tests**

Append source-level tests:

```js
test('term tooltip supports hover, keyboard focus, and accessible descriptions', async () => {
  const component = await read('src/components/glossary/TermTooltip.astro');
  assert.match(component, /tabindex="0"/);
  assert.match(component, /aria-describedby/);
  assert.match(component, /role="tooltip"/);
  assert.match(component, /:hover/);
  assert.match(component, /:focus-visible/);
});

test('term groups render typed terms without duplicating tooltip markup', async () => {
  const component = await read('src/components/glossary/TermGroup.astro');
  assert.match(component, /TermTooltip/);
  assert.match(component, /terms\.map/);
  assert.match(component, /glossary-term-list/);
});
```

- [ ] **Step 2: Run the test and confirm component files are missing**

Run: `node --test tests/software-development-glossary.test.mjs`

Expected: FAIL with `ENOENT` for `TermTooltip.astro`.

- [ ] **Step 3: Implement `TermTooltip.astro`**

Use stable IDs derived from `Astro.props.id`, semantic description markup, and scoped theme-aware styles:

```astro
---
import type { GlossaryTerm } from '../../data/software-development-glossary';

type Props = { term: GlossaryTerm; id: string };
const { term, id } = Astro.props;
const tooltipId = `term-description-${id}`;
---

<span class="term-tooltip" data-term-tooltip>
  <button
    type="button"
    class="term-tooltip__trigger"
    aria-describedby={tooltipId}
    aria-expanded="false"
    tabindex="0"
    data-term-trigger
  >
    <span>{term.name}</span>
    {term.english && <small>{term.english}</small>}
  </button>
  <span id={tooltipId} class="term-tooltip__content" role="tooltip" data-term-content>
    <strong>{term.name}{term.english ? ` · ${term.english}` : ''}</strong>
    <span>{term.description}</span>
  </span>
</span>
```

Add scoped CSS for relative positioning, a dashed cyan underline, a dark card with cyan border, `:hover`, `:focus-within`, `[data-open='true']`, light-theme colors, a visible focus outline, narrow-screen width using `min(22rem, calc(100vw - 2rem))`, and reduced-motion handling. Keep tooltip content in the DOM and visually hidden until interaction.

- [ ] **Step 4: Implement `TermGroup.astro`**

```astro
---
import type { GlossaryGroup } from '../../data/software-development-glossary';
import TermTooltip from './TermTooltip.astro';

type Props = { group: GlossaryGroup; sectionId: string; groupIndex: number };
const { group, sectionId, groupIndex } = Astro.props;
---

<section class="glossary-group">
  <h4>{group.title}</h4>
  {group.description && <p>{group.description}</p>}
  <ul class="glossary-term-list">
    {group.terms.map((term, termIndex) => (
      <li><TermTooltip term={term} id={`${sectionId}-${groupIndex}-${termIndex}`} /></li>
    ))}
  </ul>
</section>
```

Add compact wrapping-list styles, remove default list bullets, and keep sufficient spacing for focus rings.

- [ ] **Step 5: Run the targeted test**

Run: `node --test tests/software-development-glossary.test.mjs`

Expected: all current tests PASS.

- [ ] **Step 6: Commit the focused components**

```bash
git add tests/software-development-glossary.test.mjs src/components/glossary/TermTooltip.astro src/components/glossary/TermGroup.astro
git commit -m "新增术语悬浮说明组件"
```

### Task 3: Add the knowledge-map renderer and delegated touch behavior

**Files:**
- Modify: `tests/software-development-glossary.test.mjs`
- Create: `src/components/glossary/GlossaryMap.astro`

- [ ] **Step 1: Add a failing interaction test**

```js
test('glossary map uses one delegated handler for touch and Escape behavior', async () => {
  const component = await read('src/components/glossary/GlossaryMap.astro');
  assert.match(component, /data-glossary-map/);
  assert.match(component, /closest\('\[data-term-trigger\]'\)/);
  assert.match(component, /aria-expanded/);
  assert.match(component, /event\.key === 'Escape'/);
  assert.doesNotMatch(component, /querySelectorAll[^\n]+forEach[^\n]+addEventListener/);
});
```

- [ ] **Step 2: Run the test and confirm the renderer is missing**

Run: `node --test tests/software-development-glossary.test.mjs`

Expected: FAIL with `ENOENT` for `GlossaryMap.astro`.

- [ ] **Step 3: Implement the static section renderer**

Render `glossarySections` in order with numbered `h2` headings, section introductions, and `TermGroup` instances. Put the component root on `<div class="glossary-map" data-glossary-map>` and use section IDs for stable anchors.

- [ ] **Step 4: Add one delegated event handler**

Inside the component script, initialize each glossary root once. On click, find `event.target.closest('[data-term-trigger]')`, close any previously open item, toggle `data-open` on its containing `[data-term-tooltip]`, and synchronize `aria-expanded`. On outside click close open items. On `Escape`, close the active item and return focus to its trigger. Register handlers at the glossary root or document level once rather than once per term.

- [ ] **Step 5: Run the targeted test**

Run: `node --test tests/software-development-glossary.test.mjs`

Expected: all tests PASS.

- [ ] **Step 6: Commit the renderer**

```bash
git add tests/software-development-glossary.test.mjs src/components/glossary/GlossaryMap.astro
git commit -m "实现术语知识地图交互"
```

### Task 4: Write the MDX article and expert comparison tables

**Files:**
- Modify: `tests/software-development-glossary.test.mjs`
- Create: `content/posts/tool/software-development-glossary.mdx`

- [ ] **Step 1: Add failing article structure and completeness tests**

```js
test('software glossary article has valid metadata and renders the interactive map', async () => {
  const article = await read('content/posts/tool/software-development-glossary.mdx');
  assert.match(article, /title: "软件开发技术术语大全/);
  assert.match(article, /postSlug: "tool\/software-development-glossary"/);
  assert.match(article, /from '@components\/glossary\/GlossaryMap\.astro'/);
  assert.match(article, /<GlossaryMap \/>/);
});

test('software glossary article includes algorithms, all GoF patterns, comparisons, and learning paths', async () => {
  const article = await read('content/posts/tool/software-development-glossary.mdx');
  const gofPatterns = [
    '单例', '工厂方法', '抽象工厂', '建造者', '原型',
    '适配器', '桥接', '组合', '装饰器', '外观', '享元', '代理',
    '责任链', '命令', '解释器', '迭代器', '中介者', '备忘录',
    '观察者', '状态', '策略', '模板方法', '访问者',
  ];
  for (const pattern of gofPatterns) assert.match(article, new RegExp(pattern));
  assert.match(article, /## 算法知识体系/);
  assert.match(article, /## 常见概念辨析/);
  assert.match(article, /## 分角色学习路径/);
});
```

- [ ] **Step 2: Run the test and confirm the article is missing**

Run: `node --test tests/software-development-glossary.test.mjs`

Expected: FAIL with `ENOENT` for the MDX article.

- [ ] **Step 3: Add valid frontmatter and imports**

Use:

```mdx
---
title: "软件开发技术术语大全：从计算机基础到云原生与 AI 工程"
date: 2026-07-13
postSlug: "tool/software-development-glossary"
categories:
  - "技术"
  - "软件工程"
tags:
  - 软件开发
  - 算法
  - 设计模式
  - 系统架构
  - 云原生
description: "一份覆盖计算机基础、算法、设计模式、前后端、数据库、分布式系统、安全、测试、DevOps、云原生和 AI 工程的软件开发技术知识地图。"
keywords: "软件开发术语, 数据结构, 算法, 设计模式, 后端技术, 分布式系统, DevOps, 云原生"
featured: false
---

import GlossaryMap from '@components/glossary/GlossaryMap.astro';
```

- [ ] **Step 4: Write the introduction and usage guide**

Explain that the article is a map rather than a mastery checklist; hover, focus, or tap terms to read definitions; tables stay visible for comparisons; products and frameworks are ecosystem examples rather than universal abstractions; and the AI section links conceptually to the existing LLM glossary without duplicating it.

- [ ] **Step 5: Render the interactive domain map**

Insert `<GlossaryMap />` beneath the usage guide. Add a short sentence before it explaining that every underlined term is interactive.

- [ ] **Step 6: Write the algorithm knowledge-system tables**

Create visible tables for algorithmic strategies; sorting; searching; strings; trees and graphs; dynamic programming, greedy and backtracking; number theory and geometry; probabilistic algorithms; distributed consensus; and concurrency algorithms. Each row must give the algorithm name, core idea, typical use, and complexity or key caveat. Include at least the named algorithms from the approved design: binary search, merge sort, quicksort, heapsort, KMP, Boyer–Moore, Rabin–Karp, AC automaton, Manacher, BFS, DFS, topological sort, Dijkstra, Bellman–Ford, Floyd–Warshall, A*, Prim, Kruskal, maximum flow, union-find, Euclidean algorithm, fast exponentiation, sieve, convex hull, reservoir sampling, Paxos, Raft, CAS, and lock-free algorithms.

- [ ] **Step 7: Write the complete GoF 23-pattern table**

Use separate creating, structural, and behavioral tables. Every pattern row must include intent, typical scenario, and common misuse. Ensure exactly the agreed 5 creating, 7 structural, and 11 behavioral patterns are present.

- [ ] **Step 8: Write architecture-pattern and concept-comparison tables**

Cover MVC/MVP/MVVM; layered/hexagonal/onion/clean architecture; Repository/Unit of Work; CQRS/Event Sourcing; Saga/Outbox/Inbox; Actor/Reactor/Proactor; retry/timeout/circuit breaker/bulkhead/fallback. Add explicit comparison tables for process/thread/coroutine, concurrency/parallelism, sync/async, blocking/non-blocking, library/framework, SDK/API, authentication/authorization, Cookie/Session/Token, REST/RPC/GraphQL/WebSocket, optimistic/pessimistic locking, ACID/CAP/BASE, strong/eventual consistency, cache penetration/breakdown/avalanche, message/event/command, monolith/SOA/microservices, VM/container, CI/delivery/deployment, logs/metrics/traces, and high availability/disaster recovery/backup.

- [ ] **Step 9: Add role-based learning paths and maintenance notes**

Provide concise staged paths for beginners, frontend, backend, mobile, architecture, DevOps/SRE, data engineering, and security. End with a note that the map is intentionally extensible and new terms should preserve the one-sentence-description rule.

- [ ] **Step 10: Run the targeted test**

Run: `node --test tests/software-development-glossary.test.mjs`

Expected: all tests PASS.

- [ ] **Step 11: Commit the article**

```bash
git add tests/software-development-glossary.test.mjs content/posts/tool/software-development-glossary.mdx
git commit -m "新增软件开发技术术语大全"
```

### Task 5: Verify rendering, responsive behavior, and repository boundaries

**Files:**
- Modify if required: `src/components/glossary/TermTooltip.astro`
- Modify if required: `src/components/glossary/TermGroup.astro`
- Modify if required: `src/components/glossary/GlossaryMap.astro`
- Modify only if component styles cannot solve table overflow: `src/styles/global.css`

- [ ] **Step 1: Run the focused glossary test**

Run: `node --test tests/software-development-glossary.test.mjs`

Expected: all glossary tests PASS.

- [ ] **Step 2: Perform TypeScript and content compilation through Astro build**

Run: `npm run build`

Expected: build exits 0 and emits `/posts/tool/software-development-glossary/` into `dist`.

If the user keeps the earlier “正文 only, no build” instruction, skip this command and report it explicitly as not run; do not claim the page compiles.

- [ ] **Step 3: Run the repository test suite**

Run: `npm run test`

Expected: all Node tests PASS.

If the user keeps the earlier “正文 only, no tests” instruction, skip this command and report it explicitly as not run.

- [ ] **Step 4: Inspect the working-tree scope**

Run:

```bash
git status --short
git diff --stat HEAD
git diff --name-only HEAD
```

Expected glossary scope: the article, glossary data, glossary components, and glossary test. Existing unrelated changes remain present but unchanged. No generated `dist/`, `.astro/`, `public/images/`, or `public/posts-assets/` files are staged.

- [ ] **Step 5: If browser verification is authorized, inspect interaction states**

Open `/posts/tool/software-development-glossary/` and check desktop hover, keyboard Tab/focus, Escape close, mobile-width click behavior, dark/light themes, wide tables, and viewport-edge tooltips. Capture a screenshot for the PR description if visual verification is performed.

- [ ] **Step 6: Commit any narrowly scoped verification fixes**

```bash
git add src/components/glossary/TermTooltip.astro src/components/glossary/TermGroup.astro src/components/glossary/GlossaryMap.astro src/styles/global.css
git commit -m "优化术语知识地图交互"
```

Only include files that actually changed; omit `src/styles/global.css` if component-scoped styles are sufficient.

## Completion checklist

- [ ] The glossary data covers every approved top-level domain and gives each ordinary term a standalone one-sentence description.
- [ ] The Tooltip works with mouse hover, keyboard focus, touch click, outside click, and Escape.
- [ ] Algorithms, GoF 23 patterns, architecture patterns, and common comparisons remain visible in tables.
- [ ] The article uses valid Content Collection frontmatter and the approved `tool/software-development-glossary` slug.
- [ ] Existing unrelated changes are untouched and excluded from glossary commits.
- [ ] Final reporting distinguishes tests actually run from tests deliberately skipped.
