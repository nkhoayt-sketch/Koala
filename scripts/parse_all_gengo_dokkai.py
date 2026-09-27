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

def parse_gengo_dokkai(gengo_text):
    # Normalize: strip problem headers
    text = re.sub(r'問題\s*[0-9]+', ' ', gengo_text)
    text = re.sub(r'[文字・語彙文法読解]', ' ', text)
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    # Skip title lines
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
        
        # Are these question numbers or answers?
        # If any value is > 4, they are definitely question numbers!
        # If pending_qs is not empty, and all values are in 1..4, and len(vals) == len(pending_qs):
        if len(pending_qs) > 0 and all(1 <= v <= 4 for v in vals) and len(vals) == len(pending_qs):
            # Perfect match!
            for q_num, ans in zip(pending_qs, vals):
                q_map[q_num] = ans
            pending_qs = []
        elif any(v > 4 for v in vals) or (len(pending_qs) == 0 and vals == list(range(vals[0], vals[0] + len(vals)))):
            # Sequential numbers or numbers > 4 are question numbers
            pending_qs.extend(vals)
        elif len(pending_qs) > 0 and all(1 <= v <= 4 for v in vals):
            # Answer line
            for q_num, ans in zip(pending_qs[:len(vals)], vals):
                q_map[q_num] = ans
            pending_qs = pending_qs[len(vals):]
            
    return q_map

# Test on all 31 pages
all_results = {}
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
    q_map = parse_gengo_dokkai(g_part)
    all_results[exam_id] = q_map
    
    q_nums = sorted(list(q_map.keys()))
    min_q = q_nums[0] if q_nums else 0
    max_q = q_nums[-1] if q_nums else 0
    print(f"[{exam_id}] Extracted {len(q_map)} questions: Q{min_q}..Q{max_q}")
