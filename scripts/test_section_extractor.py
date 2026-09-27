import pypdf
import re
import json

r = pypdf.PdfReader('N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')

def to_half(s):
    res = []
    for c in s:
        code = ord(c)
        if 0xff10 <= code <= 0xff19:
            res.append(chr(code - 0xfee0))
        elif c == '　':
            res.append(' ')
        else:
            res.append(c)
    return ''.join(res)

def extract_pdf_page_keys(pidx):
    raw_text = r.pages[pidx].extract_text()
    text = to_half(raw_text)
    
    # Header: Year and month
    hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', text)
    if hm:
        m, y = int(hm.group(1)), int(hm.group(2))
    else:
        hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', text)
        y, m = int(hm.group(1)), int(hm.group(2))
    exam_id = f"{y}_{m:02d}"

    # Split into Gengo+Dokkai and Choukai
    parts = text.split('聴解')
    gengo_text = parts[0]
    choukai_text = parts[1] if len(parts) > 1 else ''

    # Clean Gengo text
    # Replace 問題\n with 問題
    gt = re.sub(r'問題\s*[\r\n]+\s*', '問題', gengo_text)
    
    # In Gengo text, we have sections:
    # 問題1, 問題2, ... 問題14
    # Let's inspect the sections
    print(f"================ {exam_id} (Page {pidx+1}) ================")
    # Print lines
    lines = [l.strip() for l in gt.split('\n') if l.strip()]
    for i, l in enumerate(lines[:30]):
        print(f"{i:2d}: {l}")

extract_pdf_page_keys(1)
extract_pdf_page_keys(31)
