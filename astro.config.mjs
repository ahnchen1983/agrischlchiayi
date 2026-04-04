// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import rehypeExternalLinks from 'rehype-external-links';
import remarkWikilinks from './plugins/remark-wikilinks.mjs';

export default defineConfig({
  site: 'https://ahnchen1983.github.io',
  base: '/agrischlchiayi',
  integrations: [
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
    }),
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-light',
      wrap: true,
    },
    remarkPlugins: [remarkWikilinks],
    rehypePlugins: [
      [
        rehypeExternalLinks,
        { target: '_blank', rel: ['noopener', 'noreferrer'] },
      ],
    ],
  },
});
