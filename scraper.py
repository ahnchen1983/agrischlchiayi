#!/usr/bin/env python3
"""
臺灣史新手村 (Ilha Formosa) 全站爬取腳本
使用 Playwright 爬取 Angular SPA 內容
"""

import time
import json
import re
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

BASE_URL = "https://ilhaformosa.nmth.gov.tw"
HOME_URL = f"{BASE_URL}/home/zh-tw"
OUTPUT_DIR = Path("/Users/cheyuwu/taiwan-md/data/ilhaformosa")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PERIODS = [
    ("02-0", "史前",    "00-prehistory.md"),
    ("02-1", "原住民族", "01-indigenous.md"),
    ("02-2", "荷西時期", "02-dutch-spanish.md"),
    ("02-3", "清領時期", "03-qing.md"),
    ("02-4", "鄭氏王朝", "04-koxinga.md"),
    ("02-5", "日治時期", "05-japanese.md"),
    ("02-6", "戰後",    "06-postwar.md"),
    ("02-7", "當代",    "07-contemporary.md"),
]

CRAWL_TIME = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

def make_frontmatter(title, period_code, source_url):
    return f"""---
title: "{title}"
period_code: "{period_code}"
source: "{source_url}"
crawled_at: "{CRAWL_TIME}"
copyright: "© 國立臺灣歷史博物館 National Museum of Taiwan History"
license: "本內容版權歸屬國立臺灣歷史博物館，僅供學術研究參考"
---

"""

def clean_text(text):
    """Clean and normalize extracted text"""
    if not text:
        return ""
    # Remove excessive whitespace/newlines
    lines = text.split('\n')
    cleaned = []
    prev_blank = False
    for line in lines:
        line = line.strip()
        if line == "":
            if not prev_blank:
                cleaned.append("")
            prev_blank = True
        else:
            cleaned.append(line)
            prev_blank = False
    return '\n'.join(cleaned).strip()

def extract_page_content(page):
    """Extract meaningful content from the page"""
    # Wait for main content to load
    try:
        page.wait_for_selector('app-root', timeout=15000)
    except PlaywrightTimeout:
        pass
    
    # Try to get structured content
    content_data = page.evaluate("""
    () => {
        const result = {
            title: '',
            headings: [],
            paragraphs: [],
            images: [],
            lists: [],
            fullText: '',
            rawHTML: ''
        };
        
        // Try to find the main content area
        const selectors = [
            '.page-content', '.content-area', '.main-content',
            'main', 'article', '.container', '#content',
            '.ng-star-inserted', 'app-root'
        ];
        
        let contentEl = null;
        for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el && el.innerText && el.innerText.trim().length > 100) {
                contentEl = el;
                break;
            }
        }
        
        if (!contentEl) contentEl = document.body;
        
        // Get title
        const h1 = contentEl.querySelector('h1');
        if (h1) result.title = h1.innerText.trim();
        
        // Get headings
        const headings = contentEl.querySelectorAll('h1, h2, h3, h4, h5, h6');
        headings.forEach(h => {
            result.headings.push({
                level: parseInt(h.tagName[1]),
                text: h.innerText.trim()
            });
        });
        
        // Get paragraphs
        const paras = contentEl.querySelectorAll('p');
        paras.forEach(p => {
            const text = p.innerText.trim();
            if (text.length > 10) result.paragraphs.push(text);
        });
        
        // Get images
        const imgs = contentEl.querySelectorAll('img');
        imgs.forEach(img => {
            result.images.push({
                alt: img.getAttribute('alt') || '',
                src: img.getAttribute('src') || ''
            });
        });
        
        // Get lists
        const lists = contentEl.querySelectorAll('ul, ol');
        lists.forEach(list => {
            const items = [];
            list.querySelectorAll('li').forEach(li => {
                const text = li.innerText.trim();
                if (text) items.push(text);
            });
            if (items.length > 0) result.lists.push(items);
        });
        
        // Full text
        result.fullText = contentEl.innerText || '';
        
        return result;
    }
    """)
    return content_data

def content_to_markdown(data, period_name, period_code, source_url):
    """Convert extracted content to markdown"""
    lines = []
    
    # Main title
    title = data.get('title', '') or period_name
    lines.append(f"# {period_name}")
    lines.append("")
    
    full_text = data.get('fullText', '').strip()
    
    if full_text and len(full_text) > 200:
        # Structure the full text into markdown
        text_lines = full_text.split('\n')
        processed = []
        seen = set()
        
        for line in text_lines:
            line = line.strip()
            if not line:
                if processed and processed[-1] != "":
                    processed.append("")
                continue
            
            # Skip navigation/footer boilerplate
            skip_patterns = [
                '首頁', 'HOME', ':::',
                'Skip to', '回到頂部', '跳至',
                '版權所有', 'Copyright ©',
                '網站地圖', 'sitemap',
            ]
            if any(p in line for p in skip_patterns):
                continue
            
            # Deduplicate
            if line in seen and len(line) < 50:
                continue
            seen.add(line)
            
            processed.append(line)
        
        # Clean up excessive blank lines
        final = []
        blank_count = 0
        for line in processed:
            if line == "":
                blank_count += 1
                if blank_count <= 2:
                    final.append(line)
            else:
                blank_count = 0
                final.append(line)
        
        lines.extend(final)
    else:
        lines.append(f"*（{period_name}時期內容載入中或暫無資料）*")
    
    # Add images section if any
    images = data.get('images', [])
    if images:
        lines.append("")
        lines.append("## 圖片資料")
        for img in images:
            alt = img.get('alt', '（無說明）') or '（無說明）'
            src = img.get('src', '')
            if src and not src.startswith('data:'):
                if src.startswith('/'):
                    src = BASE_URL + src
                lines.append(f"- ![{alt}]({src})")
    
    return '\n'.join(lines)

def intercept_api_data(page, url):
    """Try to intercept API calls to get JSON data"""
    api_responses = []
    
    def handle_response(response):
        if ('themedata' in response.url or 'api' in response.url.lower()) and response.status == 200:
            try:
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type:
                    data = response.json()
                    api_responses.append({'url': response.url, 'data': data})
            except:
                pass
    
    page.on('response', handle_response)
    return api_responses

def scrape_period(page, period_code, period_name, filename):
    """Scrape a single time period"""
    print(f"\n{'='*60}")
    print(f"Scraping: {period_name} ({period_code})")
    
    output_path = OUTPUT_DIR / filename
    api_responses = []
    
    # Intercept API responses
    def handle_response(response):
        url = response.url
        if response.status == 200 and ('themedata' in url or '/api/' in url):
            try:
                ct = response.headers.get('content-type', '')
                if 'json' in ct:
                    data = response.json()
                    api_responses.append({'url': url, 'data': data})
                    print(f"  [API] Captured: {url[:80]}")
            except:
                pass
    
    page.on('response', handle_response)
    
    # Navigate to the period page
    period_url = f"{BASE_URL}/{period_code}/zh-tw"
    print(f"  URL: {period_url}")
    
    try:
        page.goto(period_url, wait_until='domcontentloaded', timeout=30000)
        # Wait for Angular to render
        time.sleep(4)
        
        # Check if page redirected back to home (404 case)
        current_url = page.url
        print(f"  Current URL: {current_url}")
        
        if '/home/' in current_url and period_code not in current_url:
            print(f"  WARNING: Redirected to home page - trying navigation via menu")
            # Try clicking from the homepage
            # Look for navigation links
            nav_links = page.evaluate("""
            () => {
                const links = [];
                document.querySelectorAll('a').forEach(a => {
                    if (a.href && a.innerText.trim()) {
                        links.push({href: a.href, text: a.innerText.trim()});
                    }
                });
                return links;
            }
            """)
            print(f"  Found {len(nav_links)} links on page")
            
            # Find link for this period
            target_link = None
            for link in nav_links:
                if period_code in link['href']:
                    target_link = link
                    break
            
            if target_link:
                print(f"  Found nav link: {target_link}")
                page.click(f'a[href*="{period_code}"]')
                time.sleep(4)
            else:
                print(f"  No nav link found for {period_code}")
        
        # Extract content
        content_data = extract_page_content(page)
        full_text = content_data.get('fullText', '')
        print(f"  Text length: {len(full_text)} chars")
        
        # Get current page URL for source
        source_url = page.url
        
        # Build markdown
        md_content = make_frontmatter(period_name, period_code, source_url)
        md_content += content_to_markdown(content_data, period_name, period_code, source_url)
        
        # Write file
        output_path.write_text(md_content, encoding='utf-8')
        line_count = md_content.count('\n') + 1
        print(f"  ✅ Written: {output_path.name} ({line_count} lines)")
        
        return True, line_count, full_text[:200]
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        # Write minimal file
        md_content = make_frontmatter(period_name, period_code, period_url)
        md_content += f"# {period_name}\n\n*爬取失敗：{str(e)}*\n"
        output_path.write_text(md_content, encoding='utf-8')
        return False, 0, str(e)
    finally:
        # Remove response handler
        page.remove_listener('response', handle_response)

def try_homepage_navigation(page):
    """Navigate from homepage and extract navigation structure"""
    print(f"\nLoading homepage: {HOME_URL}")
    page.goto(HOME_URL, wait_until='networkidle', timeout=30000)
    time.sleep(5)
    
    print("Page loaded. Extracting navigation...")
    
    # Get all links and nav structure
    nav_data = page.evaluate("""
    () => {
        const data = {
            title: document.title,
            links: [],
            navItems: [],
            bodyText: document.body.innerText.substring(0, 2000)
        };
        
        // Get all links
        document.querySelectorAll('a').forEach(a => {
            const href = a.href || '';
            const text = a.innerText.trim();
            if (text && href && !href.startsWith('javascript')) {
                data.links.push({href, text: text.substring(0, 100)});
            }
        });
        
        // Look for nav/menu items
        document.querySelectorAll('nav a, .nav a, .menu a, .sidebar a').forEach(a => {
            data.navItems.push({
                href: a.href,
                text: a.innerText.trim()
            });
        });
        
        return data;
    }
    """)
    
    print(f"Page title: {nav_data.get('title', 'N/A')}")
    print(f"Total links: {len(nav_data.get('links', []))}")
    print(f"Nav items: {len(nav_data.get('navItems', []))}")
    
    # Show links containing period codes
    for link in nav_data.get('links', []):
        for code in ['02-0', '02-1', '02-2', '02-3', '02-4', '02-5', '02-6', '02-7']:
            if code in link['href']:
                print(f"  Period link: {link['text'][:50]} -> {link['href']}")
                break
    
    return nav_data

def main():
    print("=" * 60)
    print("臺灣史新手村 (Ilha Formosa) 爬取開始")
    print(f"時間: {CRAWL_TIME}")
    print(f"輸出目錄: {OUTPUT_DIR}")
    print("=" * 60)
    
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-TW'
        )
        page = context.new_page()
        
        # First, load the homepage to understand navigation
        nav_data = try_homepage_navigation(page)
        
        # Scrape each period
        for period_code, period_name, filename in PERIODS:
            success, lines, preview = scrape_period(page, period_code, period_name, filename)
            results.append({
                'code': period_code,
                'name': period_name,
                'file': filename,
                'success': success,
                'lines': lines,
                'preview': preview[:150] if preview else ''
            })
            time.sleep(3)  # Gentle pacing
        
        browser.close()
    
    # Print summary
    print("\n" + "=" * 60)
    print("爬取完成 - 摘要報告")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r['success'] else "❌"
        print(f"\n{status} {r['name']} ({r['code']}) -> {r['file']}")
        print(f"   行數: {r['lines']}")
        if r['preview']:
            preview_clean = r['preview'].replace('\n', ' ')[:120]
            print(f"   摘要: {preview_clean}...")
    
    # Count successes
    succeeded = sum(1 for r in results if r['success'])
    print(f"\n總計: {succeeded}/{len(results)} 個時代分期成功爬取")
    
    # List all output files
    print("\n輸出檔案：")
    for f in sorted(OUTPUT_DIR.iterdir()):
        if f.suffix == '.md':
            size = f.stat().st_size
            lines = f.read_text(encoding='utf-8').count('\n')
            print(f"  {f.name}: {lines} 行, {size} bytes")

if __name__ == '__main__':
    main()
