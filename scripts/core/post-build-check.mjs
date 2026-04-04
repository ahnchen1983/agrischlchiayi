/**
 * Post-build smoke test for agrischlchiayi
 *
 * Runs after `npm run build` to catch silent failures.
 * Exit code 1 = CI should NOT deploy.
 */

import { readdir, readFile, stat } from 'node:fs/promises';
import { resolve, join } from 'node:path';

const DIST = resolve(process.cwd(), 'dist');
const MIN_TOTAL_PAGES = 20;
const MIN_ARTICLES_PER_CATEGORY = 1;
const CATEGORIES = [
  'agri-basics',
  'agri-advanced',
  'farm-management',
  'crop-production',
  'facility-farming',
  'smart-farming',
  'agri-marketing',
  'grants-planning',
  'field-visits',
  'livestock-health',
];

let errors = [];
let warnings = [];

// ── 1. Count total HTML pages ──

async function countHtml(dir) {
  let count = 0;
  try {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) {
        count += await countHtml(full);
      } else if (entry.name.endsWith('.html')) {
        count++;
      }
    }
  } catch {}
  return count;
}

const totalPages = await countHtml(DIST);
console.log(`📊 Total HTML pages: ${totalPages}`);

if (totalPages < MIN_TOTAL_PAGES) {
  errors.push(
    `Total pages (${totalPages}) below minimum (${MIN_TOTAL_PAGES}). Likely a getStaticPaths failure.`,
  );
}

// ── 2. Check each category has article pages ──

for (const cat of CATEGORIES) {
  const catDir = join(DIST, cat);
  try {
    const entries = await readdir(catDir, { withFileTypes: true });
    const articleDirs = entries.filter(
      (e) => e.isDirectory() && e.name !== 'index',
    );
    const articleCount = articleDirs.length;

    if (articleCount < MIN_ARTICLES_PER_CATEGORY) {
      warnings.push(
        `/${cat}/ has only ${articleCount} article pages (min: ${MIN_ARTICLES_PER_CATEGORY})`,
      );
    } else {
      console.log(`  ✅ /${cat}/: ${articleCount} articles`);
    }
  } catch {
    errors.push(`/${cat}/ directory missing in dist/`);
  }
}

// ── Report ──

console.log('');
if (warnings.length > 0) {
  console.log(`⚠️  ${warnings.length} warning(s):`);
  warnings.forEach((w) => console.log(`   - ${w}`));
}

if (errors.length > 0) {
  console.log(`\n🔴 ${errors.length} CRITICAL error(s):`);
  errors.forEach((e) => console.log(`   - ${e}`));
  console.log('\n❌ Post-build check FAILED. Deploy blocked.');
  process.exit(1);
} else {
  console.log(
    `\n✅ Post-build check passed. ${totalPages} pages, all categories healthy.`,
  );
}
