#!/usr/bin/env python3
"""
臺灣史新手村 (Ilha Formosa) 全站爬取腳本 v2
正確 URL 格式: /home/zh-tw/{code}
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


def extract_content(page, period_code, period_name):
    """Wait for content and extract structured text"""
    # Give SPA time to render
    time.sleep(5)
    
    result = page.evaluate("""
    (periodCode) => {
        const data = {
            url: window.location.href,
            title: document.title || '',
            pageText: '',
            headings: [],
            paragraphs: [],
            images: [],
            mainContent: '',
            allText: document.body.innerText || ''
        };
        
        // Try various content containers
        const containers = [
            document.querySelector('.content'),
            document.querySelector('.page-content'),
            document.querySelector('main'),
            document.querySelector('article'),
            document.querySelector('[class*="content"]'),
            document.querySelector('[class*="article"]'),
            document.querySelector('[class*="page"]'),
            document.querySelector('app-root'),
            document.body
        ];
        
        let mainEl = null;
        for (const el of containers) {
            if (el && el.innerText && el.innerText.trim().length > 200) {
                mainEl = el;
                break;
            }
        }
        
        if (mainEl) {
            data.mainContent = mainEl.innerText || '';
            
            // Get headings
            mainEl.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => {
                const text = h.innerText.trim();
                if (text && text.length > 0) {
                    data.headings.push({level: parseInt(h.tagName[1]), text});
                }
            });
            
            // Get paragraphs
            mainEl.querySelectorAll('p').forEach(p => {
                const text = p.innerText.trim();
                if (text.length > 20) data.paragraphs.push(text);
            });
            
            // Get images
            mainEl.querySelectorAll('img').forEach(img => {
                const src = img.getAttribute('src') || img.getAttribute('data-src') || '';
                const alt = img.getAttribute('alt') || '';
                if (src && !src.startsWith('data:') && src.length > 5) {
                    data.images.push({alt, src});
                }
            });
        }
        
        return data;
    }
    """, period_code)
    
    return result


def build_markdown(data, period_name, period_code):
    """Build markdown from extracted data"""
    lines = [f"# {period_name}", ""]
    
    full_text = data.get('mainContent', '') or data.get('allText', '')
    
    if not full_text or len(full_text.strip()) < 100:
        lines.append(f"*（{period_name} 內容無法載入）*")
        return '\n'.join(lines)
    
    # Parse the text into meaningful sections
    text_lines = full_text.split('\n')
    
    # Skip lines that are navigation/boilerplate
    skip_patterns = [
        '{{meta', 'PAGE NOT FOUND', '::: JAWS',
        'Skip to main', '跳至主要',
        ':::',
    ]
    
    seen_lines = set()
    output_lines = []
    
    for line in text_lines:
        line = line.strip()
        
        # Skip empty (we'll add our own)
        if not line:
            if output_lines and output_lines[-1] != "":
                output_lines.append("")
            continue
        
        # Skip boilerplate
        skip = False
        for p in skip_patterns:
            if p in line:
                skip = True
                break
        if skip:
            continue
        
        # Avoid exact duplicates for short lines
        if line in seen_lines and len(line) < 80:
            continue
        seen_lines.add(line)
        
        output_lines.append(line)
    
    # Clean up excessive blank lines
    cleaned = []
    blank_run = 0
    for line in output_lines:
        if line == "":
            blank_run += 1
            if blank_run <= 2:
                cleaned.append(line)
        else:
            blank_run = 0
            cleaned.append(line)
    
    lines.extend(cleaned)
    
    # Images section
    images = data.get('images', [])
    if images:
        lines.append("")
        lines.append("## 相關圖片")
        for img in images:
            alt = img.get('alt', '') or '圖片'
            src = img.get('src', '')
            if src:
                if src.startswith('/'):
                    src = BASE_URL + src
                lines.append(f"- ![{alt}]({src})")
    
    return '\n'.join(lines)


def scrape_with_spa_nav(browser_context, period_code, period_name, filename):
    """Navigate within SPA to get content"""
    output_path = OUTPUT_DIR / filename
    
    # The correct URL format from homepage nav links
    period_url = f"{BASE_URL}/home/zh-tw/{period_code}"
    print(f"\n{'='*60}")
    print(f"Period: {period_name} ({period_code})")
    print(f"URL: {period_url}")
    
    page = browser_context.new_page()
    api_data = []
    
    # Capture API responses
    def on_response(resp):
        url = resp.url
        if resp.status == 200 and ('themedata' in url or '/api/' in url):
            try:
                ct = resp.headers.get('content-type', '')
                if 'json' in ct:
                    d = resp.json()
                    api_data.append({'url': url, 'data': d})
                    print(f"  [API] {url[:80]}")
            except:
                pass
    
    page.on('response', on_response)
    
    try:
        # Navigate to period URL
        response = page.goto(period_url, wait_until='domcontentloaded', timeout=30000)
        print(f"  HTTP status: {response.status if response else 'N/A'}")
        
        # Wait for Angular SPA to render
        time.sleep(5)
        
        current_url = page.url
        print(f"  Final URL: {current_url}")
        
        # Check if we got redirected to 404
        if '/404' in current_url:
            print(f"  Got 404! Trying homepage + click navigation...")
            
            # Go to home, then click the period link
            page.goto(HOME_URL, wait_until='networkidle', timeout=30000)
            time.sleep(4)
            
            # Find and click the link for this period
            clicked = page.evaluate(f"""
            () => {{
                const links = document.querySelectorAll('a');
                for (const link of links) {{
                    const href = link.href || '';
                    if (href.includes('{period_code}')) {{
                        link.click();
                        return {{href, text: link.innerText.trim()}};
                    }}
                }}
                return null;
            }}
            """)
            
            if clicked:
                print(f"  Clicked link: {clicked}")
                time.sleep(5)
                current_url = page.url
                print(f"  After click URL: {current_url}")
            else:
                print(f"  No clickable link found for {period_code}")
        
        # Extract content
        data = extract_content(page, period_code, period_name)
        
        main_text = data.get('mainContent', '') or data.get('allText', '')
        print(f"  Content length: {len(main_text)} chars")
        print(f"  API responses captured: {len(api_data)}")
        
        # If we have API data, try to use it
        if api_data and len(main_text) < 500:
            print(f"  Using API data instead...")
            # Dump API data for inspection
            api_dump = json.dumps(api_data, ensure_ascii=False, indent=2)[:3000]
            print(f"  API data preview:\n{api_dump[:500]}")
        
        source_url = data.get('url', period_url)
        md = make_frontmatter(period_name, period_code, source_url)
        md += build_markdown(data, period_name, period_code)
        
        output_path.write_text(md, encoding='utf-8')
        lines = md.count('\n') + 1
        print(f"  ✅ Saved: {filename} ({lines} lines)")
        
        return True, lines, main_text[:200]
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Write error file
        md = make_frontmatter(period_name, period_code, period_url)
        md += f"# {period_name}\n\n*爬取錯誤：{str(e)}*\n"
        output_path.write_text(md, encoding='utf-8')
        return False, 3, str(e)
    finally:
        try:
            page.close()
        except:
            pass


def main():
    print("=" * 60)
    print("臺灣史新手村 (Ilha Formosa) 爬取 v2")
    print(f"開始時間: {CRAWL_TIME}")
    print(f"輸出目錄: {OUTPUT_DIR}")
    print("=" * 60)
    
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        context = browser.new_context(
            viewport={'width': 1280, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-TW',
            java_script_enabled=True,
        )
        
        # First load the homepage to get the SPA initialized  
        print("\n=== Initializing: Loading homepage ===")
        init_page = context.new_page()
        
        # Capture all network requests from homepage
        all_api = []
        def on_resp(r):
            if r.status == 200 and ('themedata' in r.url or 'culture.tw' in r.url or '/api/' in r.url):
                try:
                    ct = r.headers.get('content-type', '')
                    if 'json' in ct:
                        d = r.json()
                        all_api.append({'url': r.url, 'data': d})
                        print(f"  [HOME API] {r.url[:100]}")
                except:
                    pass
        
        init_page.on('response', on_resp)
        init_page.goto(HOME_URL, wait_until='networkidle', timeout=30000)
        time.sleep(6)
        
        home_title = init_page.title()
        home_text = init_page.evaluate("() => document.body.innerText")
        print(f"Homepage title: {home_title}")
        print(f"Homepage text length: {len(home_text)}")
        print(f"Homepage API calls captured: {len(all_api)}")
        
        # Print homepage text preview
        print(f"\nHomepage text preview:\n{home_text[:1000]}")
        
        # Get all navigation links
        nav_links = init_page.evaluate("""
        () => {
            const links = [];
            document.querySelectorAll('a').forEach(a => {
                const h = a.href || '';
                const t = a.innerText.trim();
                if (h && t && (h.includes('02-') || h.includes('/home/'))) {
                    links.push({href: h, text: t.substring(0,80)});
                }
            });
            return links;
        }
        """)
        
        print(f"\nNavigable links:")
        for link in nav_links:
            print(f"  [{link['text'][:50]}] -> {link['href']}")
        
        init_page.close()
        
        # Now scrape each period
        for period_code, period_name, filename in PERIODS:
            success, lines, preview = scrape_with_spa_nav(context, period_code, period_name, filename)
            results.append({
                'code': period_code,
                'name': period_name,
                'file': filename,
                'success': success,
                'lines': lines,
                'preview': preview
            })
            time.sleep(3)
        
        browser.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("最終報告")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r['success'] else "❌"
        preview = (r['preview'] or '').replace('\n', ' ')[:100]
        print(f"\n{status} {r['name']} ({r['code']}): {r['lines']} 行")
        print(f"   {preview}")
    
    success_count = sum(1 for r in results if r['success'])
    print(f"\n✅ 成功: {success_count}/{len(results)}")
    
    print("\n輸出檔案列表：")
    for f in sorted(OUTPUT_DIR.iterdir()):
        if f.suffix == '.md':
            content = f.read_text(encoding='utf-8')
            lines = content.count('\n') + 1
            size = len(content)
            print(f"  {f.name}: {lines} 行 / {size} bytes")


if __name__ == '__main__':
    main()
