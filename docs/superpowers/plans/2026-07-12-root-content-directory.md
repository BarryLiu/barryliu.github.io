# Root Content Directory Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move authored blog content to root-level `content/` without changing routes, collection APIs, generated asset URLs, or build behavior.

**Architecture:** Keep `src/content/config.ts` as Astro's collection configuration module, but replace implicit `src/content/<collection>` discovery with explicit `glob()` loaders rooted at `content/posts` and `content/drafts`. Update every runtime, migration, asset, test, and documentation path that owns the physical content location.

**Tech Stack:** Astro 5 Content Layer, TypeScript, Node.js built-in test runner, Markdown/MDX, npm scripts

---

### Task 1: Lock the new content-location contract in tests

**Files:**
- Modify: `tests/project-config.test.mjs`
- Modify: `tests/migration.test.mjs`
- Modify: `tests/static-assets.test.mjs`
- Modify: `tests/python-content.test.mjs`

- [ ] Add assertions that collection loaders and production defaults use root `content/posts` and `content/drafts`, while temporary-directory unit tests continue passing explicit fixture paths.
- [ ] Run `npm run test` and confirm the new assertions fail because production code still points at `src/content`.

### Task 2: Configure collections and scripts for root content

**Files:**
- Modify: `src/content/config.ts`
- Modify: `scripts/migrate-posts.mjs`
- Modify: `scripts/copy-static-assets.mjs`
- Modify: `tests/python-content.test.mjs`

- [ ] Import `glob` from `astro/loaders` and configure `posts` and `drafts` with explicit base directories and Markdown/MDX patterns.
- [ ] Change production default paths from `src/content/...` to `content/...` without changing injectable test fixture options.
- [ ] Run focused tests and confirm the path contract passes.

### Task 3: Move authored content and update documentation

**Files:**
- Move: `src/content/posts` to `content/posts`
- Move: `src/content/drafts` to `content/drafts`
- Move: `src/content/diary` to `content/diary`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `docs/superpowers/plans/2026-07-12-python-notebook-embedding.md`

- [ ] Move directories with Git-aware operations so tracked history remains detectable.
- [ ] Update active documentation references to the new authored-content location.
- [ ] Search the repository for remaining runtime references to `src/content/posts`, `src/content/drafts`, or `src/content/diary` and classify any historical references before changing them.

### Task 4: Verify behavior end to end

**Files:**
- Verify only; do not retain generated output.

- [ ] Run `npm run test` and require all tests to pass.
- [ ] Run `npm run build` and require Astro content sync and static generation to succeed.
- [ ] Confirm build output contains the homepage, AI notes, knowledge, about, archive, RSS, and at least one known post route.
- [ ] Review `git diff --stat`, `git status --short`, and targeted diffs to ensure existing unrelated work remains untouched.
