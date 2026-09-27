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

def parse_gengo_dokkai(gengo_text):
    text = re.sub(r'問題\s*[0-9]+', ' ', gengo_text)
    text = re.sub(r'[文字・語彙文法読解]', ' ', text)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    start = 0
    for i, l in enumerate(lines):
        if re.search(r'JLPT\s*N2', l):
            start = i + 1
            break
            
    q_map = {}
    pending_qs = []
    
    for l in lines[start:]:
        tokens = l.split()
        if not all(t.isdigit() for t in tokens):
            continue
        vals = [int(t) for t in tokens]
        
        if len(pending_qs) > 0 and all(1 <= v <= 4 for v in vals) and len(vals) == len(pending_qs):
            for q_num, ans in zip(pending_qs, vals):
                q_map[q_num] = ans
            pending_qs = []
        elif any(v > 4 for v in vals) or (len(pending_qs) == 0 and vals == list(range(vals[0], vals[0] + len(vals)))):
            pending_qs.extend(vals)
        elif len(pending_qs) > 0 and all(1 <= v <= 4 for v in vals):
            for q_num, ans in zip(pending_qs[:len(vals)], vals):
                q_map[q_num] = ans
            pending_qs = pending_qs[len(vals):]
            
    return q_map

# Load and cross-validate each exam
mismatch_reports = {}

for pidx in range(1, len(r.pages)):
    raw_text = r.pages[pidx].extract_text()
    text = to_half(raw_text)
    
    hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', text)
    if not hm: hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', text)
    y, m = hm.group(2) if int(hm.group(1)) <= 12 else hm.group(1), hm.group(1) if int(hm.group(1)) <= 12 else hm.group(2)
    exam_id = f"{y}_{int(m):02d}"

    g_part = text.split('聴解')[0]
    g_keys = parse_gengo_dokkai(g_part)
    
    with open(f"public/data/n2_exams/{exam_id}.json", 'r', encoding='utf-8') as fp:
        exam_data = json.load(fp)
        
    g_mismatches = []
    for q in exam_data['questions']:
        if q.get('sectionGroup') == 'listening':
            continue
        q_num = q.get('number')
        cur_0_idx = q.get('answer')
        official_1_idx = g_keys.get(q_num)
        
        if official_1_idx is not None:
            expected_0_idx = official_1_idx - 1
            if cur_0_idx != expected_0_idx:
                g_mismatches.append({
                    'id': q.get('id'),
                    'number': q_num,
                    'current_0_idx': cur_0_idx,
                    'official_1_idx': official_1_idx,
                    'expected_0_idx': expected_0_idx
                })
                
    mismatch_reports[exam_id] = g_mismatches

total_mismatches = sum(len(v) for v in mismatch_reports.values())
print(f"Total Gengo/Dokkai mismatches across all 31 exams: {total_mismatches}")
for eid, ms in mismatch_reports.items():
    if ms:
        print(f"  [{eid}]: {len(ms)} mismatches (e.g. Qs: {[m['number'] for m in ms[:5]]})")
