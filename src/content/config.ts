import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    postSlug: z.string(),
    categories: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    description: z.string().optional(),
    keywords: z.union([z.string(), z.array(z.string())]).optional(),
    cover: z.string().optional(),
    featured: z.boolean().default(false),
    readingTime: z.number().optional(),
    project: z.string().optional(),
  }),
});

export const collections = { posts };
