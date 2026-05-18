import { mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sourceRoot = path.join(repoRoot, '_posts');
const targetRoot = path.join(repoRoot, 'src/content/posts');

const postFilePattern = /^(\d{4})-(\d{1,2})-(\d{1,2})-(.+)\.(md|markdown)$/i;

function toPosix(value) {
  return value.split(path.sep).join('/');
}

function pad2(value) {
  return String(Number(value)).padStart(2, '0');
}

function stripQuotes(value) {
  return String(value ?? '').trim().replace(/^["']|["']$/g, '').trim();
}

function slugify(value) {
  return stripQuotes(value)
    .toLowerCase()
    .replace(/\.(md|markdown)$/i, '')
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/gi, '-')
    .replace(/^-+|-+$/g, '') || 'untitled';
}

function yamlString(value) {
  const text = String(value ?? '');
  return /^[A-Za-z_][A-Za-z0-9_-]*$/.test(text) ? text : JSON.stringify(text);
}

function firstHeading(markdown) {
  const match = markdown.match(/^#{1,3}\s+(.+?)\s*#*\s*$/m);
  return match ? match[1].trim() : '';
}

export function normalizeList(value) {
  if (Array.isArray(value)) {
    return value.map(stripQuotes).filter(Boolean);
  }

  const text = stripQuotes(value);
  if (!text) return [];

  if (text.startsWith('[') && text.endsWith(']')) {
    return text
      .slice(1, -1)
      .split(',')
      .map(stripQuotes)
      .filter(Boolean);
  }

  return text
    .split(/[\s,，]+/)
    .map(stripQuotes)
    .filter(Boolean);
}

export function derivePostIdentity(sourcePath) {
  const normalized = toPosix(sourcePath);
  const relative = normalized.replace(/^.*?_posts\//, '');
  const segments = relative.split('/');
  const file = segments.at(-1);
  const match = file.match(postFilePattern);

  if (!match) {
    const fallbackTopic = segments.length > 1 ? segments[0] : 'notes';
    const fallbackSlug = slugify(file);
    return {
      date: '1970-01-01',
      slug: [...segments.slice(0, -1), fallbackSlug].join('/'),
      outputPath: [...segments.slice(0, -1), `${fallbackSlug}.md`].join('/'),
      topic: fallbackTopic,
    };
  }

  const [, year, month, day, rawSlug] = match;
  const date = `${year}-${pad2(month)}-${pad2(day)}`;
  const topic = segments.length > 1 ? segments[0] : 'notes';
  const outputSegments = [...segments.slice(0, -1), slugify(rawSlug)];

  return {
    date,
    slug: outputSegments.join('/'),
    outputPath: `${outputSegments.join('/')}.md`,
    topic,
  };
}

function parseFrontmatter(raw) {
  const normalized = raw.replace(/\r\n/g, '\n');
  const lines = normalized.split('\n');
  const first = lines[0] ?? '';

  if (!first.match(/^.*---\s*$/)) {
    return { data: {}, body: normalized };
  }

  const openingPrefix = first.replace(/---\s*$/, '').trim();
  const endIndex = lines.findIndex((line, index) => index > 0 && line.trim() === '---');

  if (endIndex === -1) {
    return { data: {}, body: normalized };
  }

  const frontmatterLines = lines.slice(1, endIndex);
  const bodyLines = lines.slice(endIndex + 1);
  const data = {};

  for (const line of frontmatterLines) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) continue;
    const [, key, value] = match;
    data[key] = value.trim();
  }

  const body = [openingPrefix, ...bodyLines].filter(Boolean).join('\n').replace(/^\n+/, '');
  return { data, body };
}

function firstParagraph(markdown) {
  const cleaned = markdown
    .replace(/```[\s\S]*?```/g, '')
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#') && !line.startsWith('![') && line !== '* content');

  return cleaned[0]?.replace(/^>\s*/, '').slice(0, 150) ?? '';
}

function postUrlToPath(postRef) {
  const normalized = postRef.trim().replace(/^\/+/, '');
  const segments = normalized.split('/');
  const file = segments.at(-1) ?? '';
  const match = file.match(/^(\d{4})-(\d{1,2})-(\d{1,2})-(.+)$/);

  if (!match) return `/posts/${normalized}/`;

  const slug = slugify(match[4]);
  return `/posts/${[...segments.slice(0, -1), slug].join('/')}/`;
}

export function rewriteJekyllMarkdown(markdown, options = {}) {
  const sourceDir = options.sourceDir ? toPosix(options.sourceDir).replace(/^.*?_posts\/?/, '') : '';
  const assetPrefix = sourceDir ? `/posts-assets/${sourceDir}/` : '/posts-assets/';

  return markdown
    .replace(/(\]\(|src=["'])([^)"']+)/g, (_match, prefix, url) => `${prefix}${url.replaceAll('\\', '/')}`)
    .replace(/^\s*\*\s+content\s*\n\s*\{:toc\}\s*\n?/gm, '')
    .replace(/^\s*\{:toc\}\s*\n?/gm, '')
    .replace(/\{\{\s*site\.baseurl\s*\}\}\s*\{%\s*post_url\s+([^%]+?)\s*%\}/g, (_match, postRef) =>
      postUrlToPath(postRef),
    )
    .replace(/\{%\s*post_url\s+([^%]+?)\s*%\}/g, (_match, postRef) => postUrlToPath(postRef))
    .replace(/\{\{\s*site\.baseurl\s*\}\}/g, '')
    .replace(/!\[([^\]]*?(?:\.\/)?(?:\.\.\/)+(images|assets)\/[^\]]+)\]\([^)]+\)/g, (_match, alt) =>
      `![${alt}](${alt.replace(/^(?:\.\/)?(?:\.\.\/)+/, '/')})`,
    )
    .replace(/(\]\(|src=["'])(?:\.\/)?(?:\.\.\/)+(images|assets)\//g, '$1/$2/')
    .replace(/(\]\(|src=["'])_posts\/[^)"']*\/([^/"')]+\.(?:png|jpe?g|gif|webp|bmp|svg))/gi, '$1/images/$2')
    .replace(/(\]\(|src=["'])(?:\.\/)?(assets\/[^)"']+)/g, (_match, prefix, url) => `${prefix}${assetPrefix}${url}`)
    .trimStart();
}

function frontmatterBlock(data) {
  const lines = ['---'];
  lines.push(`title: ${yamlString(data.title)}`);
  lines.push(`date: ${data.date}`);
  lines.push(`postSlug: ${yamlString(data.slug)}`);
  lines.push('categories:');

  for (const category of data.categories) {
    lines.push(`  - ${yamlString(category)}`);
  }

  lines.push(data.tags.length ? 'tags:' : 'tags: []');
  for (const tag of data.tags) {
    lines.push(`  - ${yamlString(tag)}`);
  }

  if (data.description) lines.push(`description: ${yamlString(data.description)}`);
  if (data.keywords) lines.push(`keywords: ${yamlString(data.keywords)}`);
  if (data.project) lines.push(`project: ${yamlString(data.project)}`);
  lines.push('featured: false');
  lines.push('---');
  return lines.join('\n');
}

export function buildMigratedPost({ sourcePath, raw }) {
  const identity = derivePostIdentity(sourcePath);
  const { data, body } = parseFrontmatter(raw);
  const sourceDir = path.posix.dirname(toPosix(sourcePath).replace(/^.*?_posts\//, ''));
  const rewrittenBody = rewriteJekyllMarkdown(body, { sourceDir });
  const categories = normalizeList(data.categories ?? data.category);
  const tags = normalizeList(data.tags);
  const title = stripQuotes(data.title) || firstHeading(rewrittenBody) || identity.slug.split('/').at(-1);
  const description = stripQuotes(data.description) || firstParagraph(rewrittenBody);

  return `${frontmatterBlock({
    title,
    date: stripQuotes(data.date).slice(0, 10) || identity.date,
    slug: identity.slug,
    categories: categories.length ? categories : [identity.topic],
    tags,
    description,
    keywords: stripQuotes(data.keywords),
    project: stripQuotes(data.project),
  })}\n\n${rewrittenBody.trimEnd()}\n`;
}

async function walk(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...await walk(fullPath));
    } else if (entry.isFile() && entry.name.match(/\.(md|markdown)$/i)) {
      files.push(fullPath);
    }
  }

  return files;
}

export async function migratePosts() {
  const sourceFiles = await walk(sourceRoot);
  await rm(targetRoot, { recursive: true, force: true });

  for (const sourceFile of sourceFiles) {
    const raw = await readFile(sourceFile, 'utf8');
    const identity = derivePostIdentity(sourceFile);
    const outputPath = path.join(targetRoot, ...identity.outputPath.split('/'));
    await mkdir(path.dirname(outputPath), { recursive: true });
    await writeFile(outputPath, buildMigratedPost({ sourcePath: sourceFile, raw }), 'utf8');
  }

  return sourceFiles.length;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const count = await migratePosts();
  console.log(`Migrated ${count} posts to ${toPosix(path.relative(repoRoot, targetRoot))}`);
}
