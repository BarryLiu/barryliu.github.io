import { getAllPosts, getDescription, getPrimaryCategory, postUrl } from '../utils/posts';

export const prerender = true;

function toSearchText(value: string) {
  return value
    .normalize('NFKC')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/!\[[^\]]*\]\([^)]+\)/g, ' ')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .replace(/\s+/g, ' ')
    .toLowerCase()
    .trim()
    .slice(0, 3600);
}

export async function GET() {
  const posts = await getAllPosts();
  const items = posts.map((post) => {
    const description = getDescription(post);
    return {
      title: post.data.title,
      description,
      url: postUrl(post),
      date: post.data.date.toISOString().slice(0, 10),
      category: getPrimaryCategory(post),
      categories: post.data.categories,
      tags: post.data.tags,
      text: toSearchText(`${post.data.title} ${description} ${post.data.postSlug} ${post.body ?? ''}`),
    };
  });

  return new Response(JSON.stringify(items), {
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'public, max-age=300',
    },
  });
}
