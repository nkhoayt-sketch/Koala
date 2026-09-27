import pypdf
import re
import json

r = pypdf.PdfReader('N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')

def extract_answers_from_page(page_idx):
    text = r.pages[page_idx].extract_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Extract year & month
    header = ''
    for l in lines[:5]:
        m = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', l)
        if m:
            month = int(m.group(1))
            year = int(m.group(2))
            header = f"{year}_{month:02d}"
            break
    if not header:
        # try reverse order 2010/7
        for l in lines[:5]:
            m = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', l)
            if m:
                year = int(m.group(1))
                month = int(m.group(2))
                header = f"{year}_{month:02d}"
                break
                
    return header, lines

for p in range(1, len(r.pages)):
    h, l = extract_answers_from_page(p)
    print(f"Page {p+1}: {h} ({len(l)} lines)")
