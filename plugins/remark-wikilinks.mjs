/**
 * Remark plugin: convert [[wikilinks]] to <a> tags pointing to the correct article URL.
 * Builds a title→URL map from knowledge/ directory at startup.
 */
import { readdirSync, readFileSync, statSync } from 'fs';
import { join, basename } from 'path';
import { visit } from 'unist-util-visit';

const categorySlugMap = {
  'Agri-Basics': 'agri-basics',
  'Agri-Advanced': 'agri-advanced',
  'Farm-Management': 'farm-management',
  'Crop-Production': 'crop-production',
  'Facility-Farming': 'facility-farming',
  'Smart-Farming': 'smart-farming',
  'Agri-Marketing': 'agri-marketing',
  'Grants-Planning': 'grants-planning',
  'Field-Visits': 'field-visits',
  'Livestock-Health': 'livestock-health',
  'Crop-Index': 'crop-index',
  'Tech-Index': 'tech-index',
  'Learning-Paths': 'learning-paths',
};

let titleToUrl = null;

function buildMap() {
  if (titleToUrl) return titleToUrl;
  titleToUrl = new Map();
  const knowledgeDir = join(process.cwd(), 'knowledge');

  for (const [folder, slug] of Object.entries(categorySlugMap)) {
    const dir = join(knowledgeDir, folder);
    try {
      const files = readdirSync(dir);
      for (const file of files) {
        if (!file.endsWith('.md') || file.startsWith('_')) continue;
        const name = basename(file, '.md');
        titleToUrl.set(name, `/${slug}/${encodeURIComponent(name)}`);
      }
    } catch {}
  }
  return titleToUrl;
}

export default function remarkWikilinks() {
  return (tree) => {
    const map = buildMap();

    visit(tree, 'text', (node, index, parent) => {
      if (!node.value || !node.value.includes('[[')) return;

      // Match **[[X]]** (bold+wikilink) and [[X]] (plain wikilink)
      const regex = /\*\*\[\[([^\]]+)\]\]\*\*|\[\[([^\]]+)\]\]/g;
      const parts = [];
      let lastIndex = 0;
      let match;

      while ((match = regex.exec(node.value)) !== null) {
        // Text before the match
        if (match.index > lastIndex) {
          parts.push({
            type: 'text',
            value: node.value.slice(lastIndex, match.index),
          });
        }

        const isBold = match[1] !== undefined;
        const title = isBold ? match[1] : match[2];
        const url = map.get(title);

        let linkOrText;
        if (url) {
          linkOrText = {
            type: 'link',
            url,
            children: [{ type: 'text', value: title }],
          };
        } else {
          linkOrText = { type: 'text', value: title };
        }

        if (isBold) {
          parts.push({
            type: 'strong',
            children: [linkOrText],
          });
        } else {
          parts.push(linkOrText);
        }

        lastIndex = match.index + match[0].length;
      }

      // Remaining text
      if (lastIndex < node.value.length) {
        parts.push({ type: 'text', value: node.value.slice(lastIndex) });
      }

      if (parts.length > 0 && lastIndex > 0) {
        parent.children.splice(index, 1, ...parts);
        return index + parts.length;
      }
    });
  };
}
