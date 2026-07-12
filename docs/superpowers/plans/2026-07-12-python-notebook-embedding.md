# Python Notebook Embedding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a uv-managed Python demo area and let Astro MDX posts embed repository `.py` and `.ipynb` sources without executing notebooks during builds.

**Architecture:** A Python converter reads allow-listed source directories and writes deterministic JSON plus extracted images. Small Astro components load the generated JSON at build time and render it with the existing blog theme. The normal build checks generated artifacts for drift before Astro builds.

**Tech Stack:** Python 3.12, uv, nbformat, markdown-it-py, Astro 5, MDX, Node test runner

---

### Task 1: Define conversion behavior

**Files:**
- Create: `tests/python-content.test.mjs`
- Create: `pyproject.toml`

- [ ] Write tests asserting source generation, notebook cell filtering, and deterministic check mode.
- [ ] Run `npm test` and confirm the tests fail because the converter does not exist.
- [ ] Add the minimal uv project configuration and converter implementation.
- [ ] Run the focused test and confirm it passes.

### Task 2: Add MDX rendering components

**Files:**
- Create: `src/components/python/PythonSource.astro`
- Create: `src/components/python/Notebook.astro`
- Create: `src/components/python/CodeBlock.astro`
- Test: `tests/python-content.test.mjs`

- [ ] Add failing structural tests for safe generated-content lookup and supported cell rendering.
- [ ] Implement the components using `import.meta.glob` over generated JSON.
- [ ] Run the focused tests and confirm they pass.

### Task 3: Add runnable examples and article

**Files:**
- Create: `app/__init__.py`
- Create: `app/demo.py`
- Create: `notebooks/demo.ipynb`
- Create: `content/posts/ailearn/python-source-and-notebook-demo.mdx`

- [ ] Add a small Python demo and a saved-output Notebook that imports it.
- [ ] Generate and commit the derived JSON/assets.
- [ ] Add an MDX article embedding both sources.

### Task 4: Integrate and verify

**Files:**
- Modify: `package.json`
- Modify: `.gitignore`
- Modify: `src/styles/global.css`

- [ ] Add generation and synchronization-check scripts.
- [ ] Ignore uv environments while retaining generated public assets.
- [ ] Add theme-compatible notebook styles.
- [ ] Run `uv run pytest`, `npm run test`, and `npm run build`.
- [ ] Request the demo article locally and verify the rendered code and Notebook sections.
