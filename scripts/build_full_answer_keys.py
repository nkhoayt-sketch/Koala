import pypdf
import re
import json
import glob
import os

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

# Let's inspect each page and see how we can extract all answers
# Let's write an extractor that parses each section table
for pidx in range(1, len(r.pages)):
    text = to_half(r.pages[pidx].extract_text())
    
    # Header: Year and month
    hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', text)
    if hm:
        m, y = int(hm.group(1)), int(hm.group(2))
    else:
        hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', text)
        y, m = int(hm.group(1)), int(hm.group(2))
    exam_id = f"{y}_{m:02d}"

    # Also load the existing exam json
    json_path = f"public/data/n2_exams/{exam_id}.json"
    if not os.path.exists(json_path):
        print(f"Missing json: {json_path}")
        continue
    with open(json_path, 'r', encoding='utf-8') as fp:
        exam_data = json.load(fp)
    
    total_q = len(exam_data['questions'])
    print(f"[{exam_id}] Page {pidx+1}: {total_q} questions in JSON")
