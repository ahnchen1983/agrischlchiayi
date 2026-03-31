#!/usr/bin/env python3
"""
Post-process scraped files to clean navigation boilerplate
and produce clean, structured markdown.
"""
import re
from pathlib import Path

INPUT_DIR = Path("/Users/cheyuwu/taiwan-md/data/ilhaformosa")

# Navigation boilerplate patterns to remove
NAV_PATTERNS = [
    r'^前言 臺灣的特色$',
    r'^單元[一二三四五六七] .+$',
    r'^參考文獻$',
    r'^寫作團隊$',
    r'^首頁  .+',
    r'^觀看次數$',
    r'^\d+$',  # standalone numbers
    r'^友善列印$',
    r'^分享到FB$',
    r'^分享到Twitter$',
    r'^分享到Line$',
    r'^字級加大$',
    r'^字級縮小$',
    r'^回到頂部$',
    r'^跳到主要內容$',
    r'^跳到主要內容區塊$',
    r'^回首頁$',
    r'^網站導覽$',
    r'^English$',
    r'^Español$',
    r'^Français$',
    r'^日本語$',
    r'^中文$',
    r'^facebook$',
    r'^instagram$',
    r'^youtube$',
    r'^建議瀏覽器.*$',
    r'^Copyright ©.*$',
    r'^網站說明$',
    r'^:::$',
    r'^研究組.*提供.*更新$',
]
NAV_RE = [re.compile(p) for p in NAV_PATTERNS]

def is_nav_line(line):
    stripped = line.strip()
    for pat in NAV_RE:
        if pat.match(stripped):
            return True
    return False

def clean_section_content(lines):
    """Remove navigation from a block of text lines"""
    cleaned = []
    for line in lines:
        if is_nav_line(line):
            continue
        cleaned.append(line)
    
    # Remove excessive blank lines
    result = []
    blank_run = 0
    for line in cleaned:
        if line.strip() == '':
            blank_run += 1
            if blank_run <= 1:
                result.append('')
        else:
            blank_run = 0
            result.append(line)
    
    return result

def process_file(path):
    content = path.read_text(encoding='utf-8')
    
    # Split frontmatter from body
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            frontmatter = '---\n' + parts[1] + '---\n'
            body = parts[2]
        else:
            frontmatter = ''
            body = content
    else:
        frontmatter = ''
        body = content
    
    # Process body: split into sections by ## headers
    lines = body.split('\n')
    
    new_lines = []
    in_section_content = False
    section_lines = []
    current_header = None
    
    for line in lines:
        if line.startswith('## '):
            # Save previous section
            if current_header is not None:
                cleaned = clean_section_content(section_lines)
                # Only add section if it has real content
                non_empty = [l for l in cleaned if l.strip()]
                if non_empty:
                    new_lines.append(current_header)
                    new_lines.append('')
                    new_lines.extend(cleaned)
                    new_lines.append('')
            current_header = line
            section_lines = []
        elif line.startswith('# ') and not new_lines:
            # Main title
            new_lines.append(line)
            new_lines.append('')
        else:
            if current_header is not None:
                section_lines.append(line)
            else:
                # Before any section header (preamble)
                if not is_nav_line(line):
                    new_lines.append(line)
    
    # Don't forget last section
    if current_header and section_lines:
        cleaned = clean_section_content(section_lines)
        non_empty = [l for l in cleaned if l.strip()]
        if non_empty:
            new_lines.append(current_header)
            new_lines.append('')
            new_lines.extend(cleaned)
    
    # Final cleanup
    result_lines = []
    blank_run = 0
    for line in new_lines:
        if line == '':
            blank_run += 1
            if blank_run <= 2:
                result_lines.append(line)
        else:
            blank_run = 0
            result_lines.append(line)
    
    new_body = '\n'.join(result_lines)
    new_content = frontmatter + '\n' + new_body.strip() + '\n'
    
    path.write_text(new_content, encoding='utf-8')
    return len(new_content.split('\n'))

def main():
    print("Cleaning output files...")
    for md_file in sorted(INPUT_DIR.glob('*.md')):
        orig_lines = len(md_file.read_text(encoding='utf-8').split('\n'))
        new_lines = process_file(md_file)
        print(f"  {md_file.name}: {orig_lines} -> {new_lines} lines")
    
    print("\nContent previews:")
    for md_file in sorted(INPUT_DIR.glob('*.md')):
        content = md_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        # Find first real paragraph (after frontmatter and headers)
        in_fm = False
        fm_done = False
        preview = ''
        for i, line in enumerate(lines):
            if i == 0 and line == '---':
                in_fm = True
                continue
            if in_fm and line == '---':
                in_fm = False
                fm_done = True
                continue
            if fm_done and line.strip() and not line.startswith('#'):
                preview = line[:150]
                break
        print(f"\n{md_file.name} ({len(lines)} lines):")
        print(f"  {preview}")

if __name__ == '__main__':
    main()
