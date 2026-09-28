import pypdf
import re
import json

r = pypdf.PdfReader('20NgayN1.pdf')

def clean_line(l):
    return l.strip()

def parse_day_page_range(start_page, end_page):
    """Combine text from start_page to end_page (1-indexed)"""
    all_text = ""
    for p in range(start_page, end_page + 1):
        if p <= len(r.pages):
            txt = r.pages[p - 1].extract_text() or ""
            all_text += f"\n--- PAGE {p} ---\n" + txt
    return all_text

# Inspect Day 9 pages (69 to 76)
d9_txt = parse_day_page_range(69, 76)
print(f"Day 9 text length: {len(d9_txt)}")
# Find all Mondai headers
for m in re.finditer(r'問題\s*([0-9１-９])', d9_txt):
    print(f"Found {m.group(0)} at pos {m.start()}")
