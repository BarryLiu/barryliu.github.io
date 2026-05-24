import { cp, mkdir, readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const defaultRepoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

async function exists(target) {
  try {
    await stat(target);
    return true;
  } catch {
    return false;
  }
}

async function copyIfExists(from, to) {
  if (!await exists(from)) return false;
  await mkdir(path.dirname(to), { recursive: true });
  await cp(from, to, { recursive: true, force: true });
  return true;
}

async function walkAssetDirs(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const dirs = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (!entry.isDirectory()) continue;
    if (entry.name === 'assets') {
      dirs.push(fullPath);
    } else {
      dirs.push(...await walkAssetDirs(fullPath));
    }
  }

  return dirs;
}

export async function copyStaticAssets(options = {}) {
  const repoRoot = options.repoRoot ?? defaultRepoRoot;
  const publicRoot = options.publicRoot ?? path.join(repoRoot, 'public');
  const contentRoot = options.contentRoot ?? path.join(repoRoot, 'src/content/posts');

  await mkdir(publicRoot, { recursive: true });
  const copied = [];

  for (const name of ['images', 'assets']) {
    const didCopy = await copyIfExists(path.join(repoRoot, name), path.join(publicRoot, name));
    if (didCopy) copied.push(name);
  }

  if (await exists(path.join(repoRoot, 'favicon.ico'))) {
    await copyIfExists(path.join(repoRoot, 'favicon.ico'), path.join(publicRoot, 'favicon.ico'));
    copied.push('favicon.ico');
  }

  const postAssetDirs = await walkAssetDirs(contentRoot);
  for (const assetDir of postAssetDirs) {
    const relative = path.relative(contentRoot, assetDir);
    const target = path.join(publicRoot, 'posts-assets', relative);
    await copyIfExists(assetDir, target);
    copied.push(`posts-assets/${relative.split(path.sep).join('/')}`);
  }

  return copied;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const copied = await copyStaticAssets();
  console.log(`Copied static assets: ${copied.join(', ')}`);
}
