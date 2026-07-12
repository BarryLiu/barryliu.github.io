import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtemp, mkdir, readFile, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

const repoRoot = path.resolve(import.meta.dirname, '..');

test('converter renders Python source and filters hidden notebook cells', async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'python-content-'));
  await mkdir(path.join(root, 'app'), { recursive: true });
  await mkdir(path.join(root, 'notebooks'), { recursive: true });
  await writeFile(path.join(root, 'app', 'demo.py'), 'def greet(name: str) -> str:\n    return f"Hello, {name}!"\n');
  await writeFile(path.join(root, 'notebooks', 'demo.ipynb'), JSON.stringify({
    nbformat: 4,
    nbformat_minor: 5,
    metadata: { kernelspec: { display_name: 'Python 3', language: 'python', name: 'python3' } },
    cells: [
      { cell_type: 'markdown', metadata: {}, source: ['# Demo\n', 'Rendered text.'] },
      { cell_type: 'code', execution_count: 1, metadata: {}, source: ['print("visible")'], outputs: [{ output_type: 'stream', name: 'stdout', text: ['visible\\n'] }] },
      { cell_type: 'code', execution_count: 2, metadata: { tags: ['blog-ignore'] }, source: ['print("secret")'], outputs: [] },
    ],
  }));

  execFileSync('python3', [path.join(repoRoot, 'scripts/render_python_content.py'), '--root', root]);

  const source = JSON.parse(await readFile(path.join(root, 'src/generated/python-content/app/demo.py.json'), 'utf8'));
  const notebook = JSON.parse(await readFile(path.join(root, 'src/generated/python-content/notebooks/demo.ipynb.json'), 'utf8'));
  assert.equal(source.language, 'python');
  assert.match(source.code, /def greet/);
  assert.equal(notebook.cells.length, 2);
  assert.equal(notebook.cells[1].outputs[0].text, 'visible\\n');
  assert.doesNotMatch(JSON.stringify(notebook), /secret/);
});

test('embedding components only load generated content', async () => {
  const pythonSource = await readFile(path.join(repoRoot, 'src/components/python/PythonSource.astro'), 'utf8');
  const notebook = await readFile(path.join(repoRoot, 'src/components/python/Notebook.astro'), 'utf8');
  assert.match(pythonSource, /generated\/python-content/);
  assert.match(notebook, /generated\/python-content/);
  assert.doesNotMatch(pythonSource, /readFile|node:fs/);
  assert.match(notebook, /markdown|code|output/);
});

test('MDX articles import Python embeds through the components alias', async () => {
  const article = await readFile(path.join(repoRoot, 'content/posts/ailearn/python-source-and-notebook-demo.mdx'), 'utf8');
  assert.match(article, /from '@components\/python\/PythonSource\.astro'/);
  assert.match(article, /from '@components\/python\/Notebook\.astro'/);
  assert.doesNotMatch(article, /\.\.\/\.\.\/\.\.\/components\/python/);
});
