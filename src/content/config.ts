import { defineCollection, z } from 'astro:content';

const zhTWCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    tags: z.array(z.string()).optional(),
    date: z.coerce.date().optional(),
    draft: z.boolean().optional(),
    category: z.string().optional(),
    author: z.string().optional(),
    readingTime: z.number().optional(),
    featured: z.boolean().optional(),
    status: z
      .enum(['draft', 'published', 'archived'])
      .optional()
      .default('published'),
    subcategory: z.string().optional().default(''),
    level: z.enum(['初階', '進階', '卓越']).optional().default('初階'),
    crop: z.array(z.string()).optional().default([]),
    tech: z.array(z.string()).optional().default([]),
    year: z.number().optional(),
    source: z.string().optional().default(''),
    courseDate: z.coerce.date().optional(),
    instructor: z.string().optional(),
    accupassUrl: z.string().optional(),
  }),
});

export const collections = {
  'zh-TW': zhTWCollection,
};
