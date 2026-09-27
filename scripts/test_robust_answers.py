import sys
import os
import re
import json
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

ans_pdf = os.path.join('N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)

def parse_full_answer_page(p_idx):
    text = reader.pages[p_idx].extract_text()
    chokai_idx = text.find('聴解')
    if chokai_idx != -1:
        text = text[:chokai_idx]
    
    # Strip headers
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Remove lines that are just section headers like "文字・語彙", "文法", "読解", "JLPT...", page numbers
    cleaned_lines = []
    for l in lines:
        if any(h in l for h in ['JLPT', '文字・語彙', '文法', '読解', 'ĐÁP ÁN']) or re.match(r'^\d{1,2}$', l):
            continue
        cleaned_lines.append(l)

    # Now let's extract blocks by 問題
    # Or tokenize everything
    # Let's print cleaned lines for page 28 (12/2023)
    return cleaned_lines

print("Cleaned lines for Page 28 (12/2023):")
cl = parse_full_answer_page(27)
for idx, l in enumerate(cl):
    print(f"{idx}: {repr(l)}")
