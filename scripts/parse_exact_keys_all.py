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

def parse_choukai(c_text, exam_id):
    lines = [l.strip() for l in c_text.split('\n') if l.strip()]
    # Normalize lines: replace '問題\s*\d+'
    norm_lines = []
    for l in lines:
        norm = re.sub(r'問題\s*([0-9]+)', r'問題\1', l)
        if norm.strip():
            norm_lines.append(norm.strip())
            
    # Find M1, M2 answers:
    # They are in lines before '問題3'
    # Find all single digits in those lines after the Q numbers
    # Question numbers in M1 are 1 2 3 4 5, M2 are 1 2 3 4 5 6 (or 1 2 3 4 5 in 2018_12)
    m1_len = 5
    m2_len = 5 if exam_id == '2018_12' else 6
    
    # Let's find answer digits for M1 and M2:
    m1_m2_lines = []
    m3_m4_lines = []
    m5_lines = []
    
    mode = 'm1_m2'
    for l in norm_lines:
        if '問題3' in l:
            mode = 'm3_m4'
        elif '問題5' in l:
            mode = 'm5'
        if mode == 'm1_m2':
            m1_m2_lines.append(l)
        elif mode == 'm3_m4':
            m3_m4_lines.append(l)
        elif mode == 'm5':
            m5_lines.append(l)
            
    # Extract digits from m1_m2:
    all_d1 = []
    for l in m1_m2_lines:
        for t in l.split():
            if t.isdigit() and 1 <= int(t) <= 4:
                all_d1.append(int(t))
    # Note that Q numbers 1 2 3 4 5 and 1 2 3 4 5 (6) also have digits 1..4.
    # But Q numbers appear as [1, 2, 3, 4, 5, 1, 2, 3, 4, ...].
    # Let's strip the leading Q numbers:
    # M1 Q numbers: 1, 2, 3, 4 (5 is not in 1..4)
    # Let's extract digits directly from lines:
    ans_m1 = []
    ans_m2 = []
    # If there is a line with 10 or 11 digits:
    for l in m1_m2_lines:
        # If line contains 10 or 11 digits, or digits at end of line:
        tokens = l.split()
        d_tokens = [int(t) for t in tokens if t.isdigit()]
        # If tokens are all in 1..4 and len is 10 or 11:
        if len(d_tokens) in (10, 11) and all(1 <= d <= 4 for d in d_tokens):
            ans_m1 = d_tokens[:m1_len]
            ans_m2 = d_tokens[m1_len:]
            break
        elif len(d_tokens) >= 16: # e.g. 1 2 3 4 5 6  4 1 3 2 3  1 4 3 2 1 3
            # Q numbers were 1 2 3 4 5 6 (6 digits) + 11 answers = 17 digits
            ans_tokens = d_tokens[m2_len:]
            ans_m1 = ans_tokens[:m1_len]
            ans_m2 = ans_tokens[m1_len:]
            break
            
    # M3 and M4 part 1:
    m3_len = 4 if exam_id == '2012_12' else 5
    ans_m3 = []
    ans_m4_p1 = []
    for l in m3_m4_lines:
        tokens = l.split()
        d_tokens = [int(t) for t in tokens if t.isdigit()]
        if len(d_tokens) in (10, 11) and all(1 <= d <= 4 for d in d_tokens):
            ans_m3 = d_tokens[:m3_len]
            ans_m4_p1 = d_tokens[m3_len:]
            break

    # M4 part 2 and M5:
    ans_m4_p2 = []
    ans_m5 = []
    for l in m5_lines:
        tokens = l.split()
        d_tokens = [int(t) for t in tokens if t.isdigit()]
        if len(d_tokens) >= 5 and any(t in tokens for t in ['1', '2']):
            # This is the line with M5 Qs and M4 p2 answers: e.g. '1 2 3   3 2 2 3 1 3' or '1 2   1 3 2 1 1'
            if d_tokens[:3] == [1, 2, 3]:
                ans_m4_p2 = d_tokens[3:]
            elif d_tokens[:2] == [1, 2]:
                ans_m4_p2 = d_tokens[2:]
        elif len(d_tokens) in (2, 3, 4) and all(1 <= d <= 4 for d in d_tokens):
            ans_m5 = d_tokens

    ans_m4 = ans_m4_p1 + ans_m4_p2
    return ans_m1, ans_m2, ans_m3, ans_m4, ans_m5

# Run extraction across all 31 pages and test against JSON
all_exam_keys = {}
for pidx in range(1, len(r.pages)):
    raw_text = r.pages[pidx].extract_text()
    text = to_half(raw_text)
    
    hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', text)
    if hm:
        m, y = int(hm.group(1)), int(hm.group(2))
    else:
        hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', text)
        y, m = int(hm.group(1)), int(hm.group(2))
    exam_id = f"{y}_{m:02d}"

    g_part = text.split('聴解')[0]
    c_part = text.split('聴解')[1] if '聴解' in text else ''
    
    g_keys = parse_gengo_dokkai(g_part)
    m1, m2, m3, m4, m5 = parse_choukai(c_part, exam_id)
    
    # Read JSON
    json_path = f"public/data/n2_exams/{exam_id}.json"
    with open(json_path, 'r', encoding='utf-8') as fp:
        jdata = json.load(fp)
    j_questions = jdata['questions']
    
    g_json_len = sum(1 for q in j_questions if q.get('sectionGroup') != 'listening')
    c_json_len = sum(1 for q in j_questions if q.get('sectionGroup') == 'listening')
    
    c_keys_total = len(m1) + len(m2) + len(m3) + len(m4) + len(m5)
    
    status = "OK" if len(g_keys) == g_json_len and c_keys_total == c_json_len else "MISMATCH"
    print(f"[{exam_id}] Gengo: PDF {len(g_keys)} vs JSON {g_json_len} | Choukai: PDF {c_keys_total} vs JSON {c_json_len} -> {status}")
    if status == "MISMATCH":
        print(f"   M1:{len(m1)} M2:{len(m2)} M3:{len(m3)} M4:{len(m4)} M5:{len(m5)}")
        
    all_exam_keys[exam_id] = {
        'gengo_dokkai': g_keys,
        'choukai': {
            'm1': m1, 'm2': m2, 'm3': m3, 'm4': m4, 'm5': m5
        }
    }

with open('scripts/parsed_official_keys.json', 'w', encoding='utf-8') as out:
    json.dump(all_exam_keys, out, ensure_ascii=False, indent=2)
print("Saved parsed_official_keys.json")
