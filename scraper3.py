#!/usr/bin/env python3
"""
臺灣史新手村 (Ilha Formosa) 全站爬取腳本 v3
- 等待 /api/cms/{code} 回應
- 解析 CMS JSON 取得完整文章內容
- 正確映射網站結構到目標檔案
"""

import time
import json
import re
import html
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

BASE_URL = "https://ilhaformosa.nmth.gov.tw"
HOME_URL = f"{BASE_URL}/home/zh-tw"
OUTPUT_DIR = Path("/Users/cheyuwu/taiwan-md/data/ilhaformosa")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CRAWL_TIME = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

# Actual site structure discovered from nav links
# Format: (section_code, title, sub_chapters)
SITE_STRUCTURE = [
    ("00-1", "前言 臺灣的特色", []),
    ("01-0", "單元一 原生之島", ["01-1", "01-2", "01-3", "01-4", "01-5"]),
    ("02-0", "單元二 海陸交會", ["02-1", "02-2", "02-3", "02-4", "02-5"]),
    ("03-0", "單元三 在地生根", ["03-1", "03-2", "03-3", "03-4"]),
    ("04-0", "單元四 世界競逐", ["04-1", "04-2", "04-3", "04-4", "04-5"]),
    ("05-0", "單元五 烽火邊緣", ["05-1", "05-2", "05-3", "05-4", "05-5", "05-6"]),
    ("06-0", "單元六 民主轉型", ["06-1", "06-2", "06-3", "06-4", "06-5"]),
    ("07-0", "參考文獻", []),
]

# Output files mapping task spec to actual site sections
OUTPUT_MAPPING = [
    {
        "filename": "00-prehistory.md",
        "title": "史前 / 原生之島",
        "sections": ["00-1", "01-0", "01-1", "01-2", "01-3", "01-4", "01-5"],
    },
    {
        "filename": "01-indigenous.md", 
        "title": "原住民族",
        "sections": ["01-1", "01-4", "01-5"],  # indigenous-focused sub-chapters
    },
    {
        "filename": "02-dutch-spanish.md",
        "title": "荷西時期 / 海陸交會",
        "sections": ["02-0", "02-1", "02-2"],
    },
    {
        "filename": "03-qing.md",
        "title": "清領時期 / 東亞交流 / 在地生根",
        "sections": ["02-3", "02-5", "03-0", "03-1", "03-2", "03-3", "03-4"],
    },
    {
        "filename": "04-koxinga.md",
        "title": "鄭氏王朝 / 東寧王國",
        "sections": ["02-4"],
    },
    {
        "filename": "05-japanese.md",
        "title": "日治時期 / 世界競逐 / 烽火邊緣",
        "sections": ["04-0", "04-1", "04-2", "04-3", "04-4", "04-5",
                     "05-0", "05-1", "05-2", "05-3", "05-4", "05-5", "05-6"],
    },
    {
        "filename": "06-postwar.md",
        "title": "戰後 / 民主轉型前期",
        "sections": ["06-0", "06-1", "06-2", "06-3"],
    },
    {
        "filename": "07-contemporary.md",
        "title": "當代 / 民主轉型後期",
        "sections": ["06-4", "06-5", "07-0"],
    },
]


def strip_html_tags(text):
    """Remove HTML tags and decode entities"""
    # Remove script/style blocks
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Convert common block tags to newlines
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?(?:p|div|h[1-6]|li|tr|td|th|ul|ol|section|article|header|footer)[^>]*>', '\n', text, flags=re.IGNORECASE)
    # Remove remaining tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html.unescape(text)
    # Normalize whitespace
    lines = [l.strip() for l in text.split('\n')]
    # Remove empty/duplicate lines
    result = []
    prev = None
    for line in lines:
        if line and line != prev:
            result.append(line)
            prev = line
        elif not line and prev != '':
            result.append('')
            prev = ''
    return '\n'.join(result).strip()


def extract_from_cms_json(cms_data):
    """Extract text content from themedata CMS JSON"""
    texts = []
    
    def walk(obj, depth=0):
        if depth > 15:
            return
        if isinstance(obj, dict):
            # Look for content fields
            for key in ['content', 'text', 'html', 'body', 'description', 'title', 'subtitle',
                        'caption', 'intro', 'summary', 'name']:
                val = obj.get(key)
                if isinstance(val, str) and len(val.strip()) > 5:
                    cleaned = strip_html_tags(val)
                    if cleaned and len(cleaned) > 5:
                        texts.append(cleaned)
            for v in obj.values():
                walk(v, depth + 1)
        elif isinstance(obj, list):
            for item in obj:
                walk(item, depth + 1)
    
    walk(cms_data)
    return '\n\n'.join(texts)


def make_frontmatter(title, sections, source_urls):
    sources = ', '.join(source_urls[:3])
    return f"""---
title: "{title}"
sections: "{', '.join(sections)}"
source: "{sources}"
crawled_at: "{CRAWL_TIME}"
copyright: "© 國立臺灣歷史博物館 National Museum of Taiwan History"
license: "本內容版權歸屬國立臺灣歷史博物館，僅供學術研究參考"
---

"""


def scrape_section(context, section_code):
    """Scrape a single section and return its content"""
    url = f"{BASE_URL}/home/zh-tw/{section_code}"
    print(f"    Scraping section {section_code}: {url}")
    
    page = context.new_page()
    cms_data = {}
    menu_data = {}
    page_text = ''
    
    captured = {}
    
    def on_response(resp):
        if resp.status != 200:
            return
        rurl = resp.url
        try:
            ct = resp.headers.get('content-type', '')
            if 'json' in ct:
                if f'/api/cms/{section_code}' in rurl and 'menuSetting' not in rurl:
                    captured['cms'] = resp.json()
                    print(f"      [CMS] Got /api/cms/{section_code}")
                elif f'/api/cms/menuSetting/{section_code}' in rurl:
                    captured['menu'] = resp.json()
                    print(f"      [MENU] Got menuSetting/{section_code}")
        except:
            pass
    
    page.on('response', on_response)
    
    try:
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        
        # Wait for CMS API to be called
        max_wait = 12  # seconds
        waited = 0
        while 'cms' not in captured and waited < max_wait:
            time.sleep(1)
            waited += 1
        
        # Also get rendered text
        page_text = page.evaluate("() => document.body.innerText || ''")
        current_url = page.url
        
        print(f"      URL: {current_url} | Text: {len(page_text)}ch | CMS: {'yes' if 'cms' in captured else 'no'}")
        
        return {
            'code': section_code,
            'url': current_url,
            'page_text': page_text,
            'cms': captured.get('cms'),
            'menu': captured.get('menu'),
        }
        
    except Exception as e:
        print(f"      ERROR: {e}")
        return {
            'code': section_code,
            'url': url,
            'page_text': '',
            'cms': None,
            'menu': None,
            'error': str(e),
        }
    finally:
        try:
            page.close()
        except:
            pass


def build_section_markdown(section_data, heading_prefix="##"):
    """Build markdown content for one section"""
    code = section_data['code']
    cms = section_data.get('cms')
    page_text = section_data.get('page_text', '')
    url = section_data.get('url', '')
    
    lines = []
    
    # Get section title from menu or CMS
    section_title = code
    menu = section_data.get('menu')
    if menu:
        # Try to get title from menu data
        def find_title(obj, depth=0):
            if depth > 8 or not isinstance(obj, (dict, list)):
                return None
            if isinstance(obj, dict):
                for k in ['title', 'name', 'menuName', 'pageName']:
                    v = obj.get(k)
                    if isinstance(v, str) and len(v.strip()) > 1:
                        return v.strip()
                for v in obj.values():
                    r = find_title(v, depth+1)
                    if r:
                        return r
            elif isinstance(obj, list):
                for item in obj:
                    r = find_title(item, depth+1)
                    if r:
                        return r
            return None
        title_found = find_title(menu)
        if title_found:
            section_title = title_found
    
    lines.append(f"{heading_prefix} {section_title} ({code})")
    lines.append("")
    
    # Get content from CMS JSON
    if cms:
        cms_text = extract_from_cms_json(cms)
        if cms_text and len(cms_text) > 50:
            lines.append(cms_text)
            lines.append("")
            return '\n'.join(lines), len(cms_text)
    
    # Fallback: use page text
    if page_text and len(page_text.strip()) > 100:
        # Filter out boilerplate
        skip_patterns = ['跳到主要內容', '建議瀏覽器', 'Copyright ©', 'facebook', 'instagram', 
                        'youtube', '回首頁', '網站導覽', ':::']
        filtered_lines = []
        for line in page_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            if any(p in line for p in skip_patterns):
                continue
            filtered_lines.append(line)
        
        if filtered_lines:
            lines.extend(filtered_lines)
            lines.append("")
            return '\n'.join(lines), len('\n'.join(filtered_lines))
    
    lines.append(f"*（{code} 內容載入失敗）*")
    lines.append("")
    return '\n'.join(lines), 0


def main():
    print("=" * 60)
    print("臺灣史新手村 (Ilha Formosa) 爬取 v3")
    print(f"開始時間: {CRAWL_TIME}")
    print("=" * 60)
    
    # Collect all unique section codes needed
    all_sections = set()
    for mapping in OUTPUT_MAPPING:
        for code in mapping['sections']:
            all_sections.add(code)
    
    print(f"\n需要爬取 {len(all_sections)} 個頁面: {sorted(all_sections)}")
    
    scraped = {}  # code -> data
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        context = browser.new_context(
            viewport={'width': 1280, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-TW',
        )
        
        # First load homepage to init cookies/session
        print("\n=== 初始化：載入首頁 ===")
        init_page = context.new_page()
        init_page.goto(HOME_URL, wait_until='networkidle', timeout=30000)
        time.sleep(3)
        init_page.close()
        
        # Scrape each section
        print(f"\n=== 開始爬取各頁面 ===")
        for code in sorted(all_sections):
            data = scrape_section(context, code)
            scraped[code] = data
            time.sleep(2)  # Gentle pacing
        
        browser.close()
    
    # Now build output files
    print(f"\n=== 建立輸出檔案 ===")
    results = []
    
    for mapping in OUTPUT_MAPPING:
        filename = mapping['filename']
        title = mapping['title']
        sections = mapping['sections']
        output_path = OUTPUT_DIR / filename
        
        print(f"\n{filename}: {title}")
        print(f"  Sections: {sections}")
        
        # Collect source URLs
        source_urls = []
        for code in sections:
            if code in scraped:
                url = scraped[code].get('url', f"{BASE_URL}/home/zh-tw/{code}")
                if url not in source_urls:
                    source_urls.append(url)
        
        # Build markdown
        md_lines = []
        md_lines.append(make_frontmatter(title, sections, source_urls))
        md_lines.append(f"# {title}")
        md_lines.append("")
        
        total_content_chars = 0
        
        for i, code in enumerate(sections):
            if code not in scraped:
                print(f"  WARNING: Section {code} not scraped")
                continue
            
            data = scraped[code]
            section_md, char_count = build_section_markdown(data, heading_prefix="##")
            md_lines.append(section_md)
            total_content_chars += char_count
            
            if char_count > 0:
                print(f"  ✅ {code}: {char_count} chars")
            else:
                print(f"  ⚠️  {code}: no content")
        
        full_md = '\n'.join(md_lines)
        output_path.write_text(full_md, encoding='utf-8')
        lines = full_md.count('\n') + 1
        size = len(full_md)
        
        print(f"  📝 {filename}: {lines} 行 / {size} bytes / {total_content_chars} content chars")
        
        results.append({
            'filename': filename,
            'title': title,
            'lines': lines,
            'size': size,
            'content_chars': total_content_chars,
            'sections': sections,
        })
    
    # Final report
    print("\n" + "=" * 60)
    print("最終報告")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r['content_chars'] > 100 else "⚠️ "
        print(f"\n{status} {r['filename']}")
        print(f"   標題: {r['title']}")
        print(f"   行數: {r['lines']} / 大小: {r['size']} bytes")
        print(f"   內容字數: {r['content_chars']}")
        print(f"   區段: {', '.join(r['sections'])}")
    
    # Show first few lines of each file
    print("\n=== 各檔案內容預覽 ===")
    for r in results:
        path = OUTPUT_DIR / r['filename']
        content = path.read_text(encoding='utf-8')
        # Skip frontmatter
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            body = parts[2].strip()
        else:
            body = content.strip()
        preview = body[:300].replace('\n', ' | ')
        print(f"\n{r['filename']}:")
        print(f"  {preview}")


if __name__ == '__main__':
    main()
