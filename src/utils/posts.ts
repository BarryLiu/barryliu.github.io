import { getCollection, type CollectionEntry } from 'astro:content';

export type Post = CollectionEntry<'posts'>;
export type TaxonomyKind = 'categories' | 'tags';

export async function getAllPosts() {
  const posts = await getCollection('posts');
  return posts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export function formatDate(date: Date) {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(date);
}

export function getReadingTime(post: Post) {
  if (post.data.readingTime) return post.data.readingTime;
  const text = (post.body ?? post.data.description ?? '').replace(/```[\s\S]*?```/g, '').replace(/\s+/g, '');
  return Math.max(1, Math.ceil(text.length / 500));
}

export function getDescription(post: Post) {
  if (post.data.description) return post.data.description;
  return (post.body ?? '')
    .replace(/```[\s\S]*?```/g, '')
    .split('\n')
    .map((line) => line.trim())
    .find((line) => line && !line.startsWith('#') && !line.startsWith('!['))
    ?.slice(0, 150) ?? '';
}

export function getPrimaryCategory(post: Post) {
  return post.data.categories[0] ?? 'notes';
}

export function taxonomySlug(value: string) {
  return value
    .trim()
    .toLowerCase()
    .replace(/\+/g, ' plus ')
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/gi, '-')
    .replace(/^-+|-+$/g, '') || 'untitled';
}

export function getTaxonomyCounts(posts: Post[], kind: TaxonomyKind) {
  const counts = new Map<string, { name: string; count: number; slug: string }>();
  for (const post of posts) {
    for (const item of post.data[kind]) {
      const slug = taxonomySlug(item);
      const current = counts.get(slug);
      counts.set(slug, {
        name: current?.name ?? item,
        count: (current?.count ?? 0) + 1,
        slug,
      });
    }
  }
  return [...counts.values()]
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name, 'zh-CN'));
}

export function groupPostsByYear(posts: Post[]) {
  const groups = new Map<string, Post[]>();
  for (const post of posts) {
    const year = String(post.data.date.getFullYear());
    groups.set(year, [...(groups.get(year) ?? []), post]);
  }
  return [...groups.entries()].sort((a, b) => Number(b[0]) - Number(a[0]));
}

export function postsWithTaxonomy(posts: Post[], kind: TaxonomyKind, value: string) {
  return posts.filter((post) => post.data[kind].some((item) => taxonomySlug(item) === value));
}

export function postUrl(post: Post) {
  return `/posts/${post.data.postSlug}/`;
}
