import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const postSchema = z.object({
  title: z.string(),
  date: z.coerce.date(),
  postSlug: z.string(),
  categories: z.array(z.string()).default([]),
  tags: z.array(z.string()).default([]),
  description: z.string().optional(),
  keywords: z.union([z.string(), z.array(z.string())]).optional(),
  cover: z.string().optional(),
  featured: z.boolean().default(false),
  draft: z.boolean().default(false),
  readingTime: z.number().optional(),
  project: z.string().optional(),
});

const posts = defineCollection({
  loader: glob({
    base: './content/posts',
    pattern: '**/*.{md,mdx}',
  }),
  schema: postSchema,
});

const drafts = defineCollection({
  loader: glob({
    base: './content/drafts',
    pattern: '**/*.{md,mdx}',
  }),
  schema: postSchema,
});

export const collections = { posts, drafts };
