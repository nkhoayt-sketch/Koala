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

for pidx in range(1, len(r.pages)):
    t = to_half(r.pages[pidx].extract_text())
    hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', t)
    if not hm: hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', t)
    y, m = hm.group(2) if int(hm.group(1)) <= 12 else hm.group(1), hm.group(1) if int(hm.group(1)) <= 12 else hm.group(2)
    exam_id = f"{y}_{int(m):02d}"
    
    # Read JSON
    with open(f"public/data/n2_exams/{exam_id}.json", 'r', encoding='utf-8') as fp:
        d = json.load(fp)
    c_qs = [q for q in d['questions'] if q.get('sectionGroup') == 'listening']
    
    # Check explanations in Choukai
    has_exp = sum(1 for q in c_qs if re.search(r'【正解】([1-4])', q.get('explanation', '')))
    print(f"[{exam_id}] JSON Choukai: {len(c_qs)} questions. Explanations with 【正解】: {has_exp}/{len(c_qs)}")
