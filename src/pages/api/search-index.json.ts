import type { APIRoute } from 'astro';
import { readdir, readFile } from 'fs/promises';
import { resolve, join, basename } from 'path';
import matter from 'gray-matter';

const categoryMapping: Record<string, string> = {
  'agri-basics': 'Agri-Basics',
  'agri-advanced': 'Agri-Advanced',
  'farm-management': 'Farm-Management',
  'crop-production': 'Crop-Production',
  'facility-farming': 'Facility-Farming',
  'smart-farming': 'Smart-Farming',
  'agri-marketing': 'Agri-Marketing',
  'grants-planning': 'Grants-Planning',
  'field-visits': 'Field-Visits',
  'livestock-health': 'Livestock-Health',
  'crop-index': 'Crop-Index',
  'tech-index': 'Tech-Index',
  'learning-paths': 'Learning-Paths',
};

export const GET: APIRoute = async () => {
  const searchIndex: Array<{
    t: string;
    d: string;
    u: string;
    tags: string[];
    lang: string;
  }> = [];

  for (const [slug, folder] of Object.entries(categoryMapping)) {
    // Chinese articles
    try {
      const zhPath = resolve(process.cwd(), 'knowledge', folder);
      const files = await readdir(zhPath);
      for (const file of files.filter(
        (f) => f.endsWith('.md') && !f.startsWith('_'),
      )) {
        try {
          const { data } = matter(await readFile(join(zhPath, file), 'utf-8'));
          const name = basename(file, '.md');
          searchIndex.push({
            t: data.title || name,
            d: data.description || '',
            u: `/${slug}/${name}`,
            tags: data.tags || [],
            lang: 'zh-TW',
          });
        } catch {
          // YAML parse error, skip this file
        }
      }
    } catch {}
    // English articles
    try {
      const enPath = resolve(process.cwd(), 'knowledge', 'en', folder);
      const files = await readdir(enPath);
      for (const file of files.filter(
        (f) => f.endsWith('.md') && !f.startsWith('_'),
      )) {
        try {
          const { data } = matter(await readFile(join(enPath, file), 'utf-8'));
          const name = basename(file, '.md');
          searchIndex.push({
            t: data.title || name,
            d: data.description || '',
            u: `/en/${slug}/${name}`,
            tags: data.tags || [],
            lang: 'en',
          });
        } catch {
          // YAML parse error, skip this file
        }
      }
    } catch {}
  }

  return new Response(JSON.stringify(searchIndex), {
    headers: { 'Content-Type': 'application/json' },
  });
};
