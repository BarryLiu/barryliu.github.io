import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { site } from '../data/site';
import { getAllPosts, getDescription, postUrl } from '../utils/posts';

export async function GET(context: APIContext) {
  const posts = await getAllPosts();

  return rss({
    title: site.title,
    description: site.description,
    site: context.site ?? new URL(site.url),
    items: posts.map((post) => ({
      title: post.data.title,
      description: getDescription(post),
      pubDate: post.data.date,
      link: postUrl(post),
      categories: [...post.data.categories, ...post.data.tags],
    })),
  });
}
