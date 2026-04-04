import { defineCollection, z } from 'astro:content';

// 定義通用的 content collection schema
const baseContentSchema = z.object({
  title: z.string(),
  description: z.string(),
  date: z.coerce.date(),
  tags: z.array(z.string()).default([]),
  author: z.string().optional().default('嘉義國本學堂'),
  difficulty: z
    .enum(['beginner', 'intermediate', 'advanced'])
    .optional()
    .default('beginner'),
  readingTime: z.number().optional().default(5),
  featured: z.boolean().optional().default(false),
  status: z
    .enum(['draft', 'published', 'archived'])
    .optional()
    .default('published'),
  lastUpdated: z.coerce.date().optional(),
  relatedTopics: z.array(z.string()).optional().default([]),
  sources: z.array(z.string()).optional().default([]),
  subcategory: z.string().optional().default(''),
  // 農業學堂專用欄位
  level: z.enum(['初階', '進階', '卓越']).optional().default('初階'),
  crop: z.array(z.string()).optional().default([]),
  tech: z.array(z.string()).optional().default([]),
  year: z.number().optional(),
  source: z.string().optional().default(''),
  courseDate: z.coerce.date().optional(),
  instructor: z.string().optional(),
  accupassUrl: z.string().optional(),
});

// 中文內容 collection
const zhTWCollection = defineCollection({
  type: 'content',
  schema: baseContentSchema,
});

// 導出 collections
export const collections = {
  'zh-TW': zhTWCollection,
};
