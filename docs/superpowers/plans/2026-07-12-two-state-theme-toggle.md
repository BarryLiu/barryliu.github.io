# Two-State Theme Toggle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the user-selectable system theme mode so the theme control switches only between light and dark.

**Architecture:** Keep system color preference only as the fallback used when no valid saved preference exists. Normalize the active and persisted mode to `light` or `dark`, and keep the existing theme event and localized control labels.

**Tech Stack:** Astro, inline browser JavaScript, Node built-in test runner

---

### Task 1: Add the two-state theme regression

**Files:**
- Modify: `tests/interactive-features.test.mjs`

- [ ] Replace the three-state theme test with assertions that the modes array contains only `light` and `dark`, the system icon and system label are absent, invalid or legacy values resolve through `prefers-color-scheme`, and theme persistence/events remain present.
- [ ] Run `node --test --test-name-pattern="light and dark color themes" tests/interactive-features.test.mjs` and confirm it fails because the current component still exposes the system mode.

### Task 2: Implement two-state initialization and switching

**Files:**
- Modify: `src/layouts/BaseLayout.astro`
- Modify: `src/components/ThemeToggle.astro`

- [ ] Set the static document theme mode to `dark`, while the inline startup script resolves a saved `light`/`dark` value or uses `prefers-color-scheme` once as the fallback.
- [ ] Remove the system icon, label, mode entry, resolver, and media-change listener from `ThemeToggle.astro`.
- [ ] Make `readMode()` return only `light` or `dark`, make `applyTheme()` normalize invalid input through the current system preference, and make `toggle()` switch directly between the two modes.
- [ ] Run the focused Node test and confirm it passes.

### Task 3: Verify the repository and rendered control

**Files:**
- Verify only

- [ ] Run `npm run test` and confirm all tests pass.
- [ ] Run `npm run build` and confirm the Astro build succeeds.
- [ ] Refresh `/` and verify the theme button exposes only light/dark labels and alternates directly between the two appearances.
