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

def parse_choukai_robust(c_raw, exam_id):
    text = to_half(c_raw)
    text = re.sub(r'問題\s*[\r\n]+\s*([0-9]+)', r'問題\1 ', text)
    text = re.sub(r'問題\s*([0-9]+)', r'問題\1 ', text)
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # In JSON, let's see how many questions each Mondai actually has
    with open(f"public/data/n2_exams/{exam_id}.json", 'r', encoding='utf-8') as fp:
        j_qs = [q for q in json.load(fp)['questions'] if q.get('sectionGroup') == 'listening']
        
    m1_target = sum(1 for q in j_qs if '問題1' in q.get('section', ''))
    m2_target = sum(1 for q in j_qs if '問題2' in q.get('section', ''))
    m3_target = sum(1 for q in j_qs if '問題3' in q.get('section', ''))
    m4_target = sum(1 for q in j_qs if '問題4' in q.get('section', ''))
    m5_target = sum(1 for q in j_qs if '問題5' in q.get('section', ''))

    m1_m2_text = []
    m3_m4_text = []
    m5_text = []
    
    mode = 'm1_m2'
    for l in lines:
        if '問題3' in l:
            mode = 'm3_m4'
        elif '問題5' in l:
            mode = 'm5'
            
        if mode == 'm1_m2':
            m1_m2_text.append(l)
        elif mode == 'm3_m4':
            m3_m4_text.append(l)
        elif mode == 'm5':
            m5_text.append(l)
            
    # 1. Parse M1 & M2:
    ans_m1 = []
    ans_m2 = []
    for l in m1_m2_text:
        tokens = l.split()
        d_tokens = [int(t) for t in tokens if t.isdigit()]
        if len(d_tokens) == (m1_target + m2_target) and all(1 <= d <= 4 for d in d_tokens):
            ans_m1 = d_tokens[:m1_target]
            ans_m2 = d_tokens[m1_target:]
            break
        elif len(d_tokens) >= (m1_target + m2_target + m2_target):
            # Qs + answers
            ans_tokens = d_tokens[- (m1_target + m2_target):]
            ans_m1 = ans_tokens[:m1_target]
            ans_m2 = ans_tokens[m1_target:]
            break
            
    # 2. Parse M3 & M4 (part 1):
    m4_p1_len = 6
    ans_m3 = []
    ans_m4_p1 = []
    for l in m3_m4_text:
        tokens = l.split()
        d_tokens = [int(t) for t in tokens if t.isdigit()]
        if len(d_tokens) == (m3_target + m4_p1_len) and all(1 <= d <= 4 for d in d_tokens):
            ans_m3 = d_tokens[:m3_target]
            ans_m4_p1 = d_tokens[m3_target:]
            break

    # 3. Parse M4 (part 2) & M5:
    m4_p2_len = m4_target - m4_p1_len
    ans_m4_p2 = []
    ans_m5 = []
    for l in m5_text:
        tokens = l.split()
        d_tokens = [int(t) for t in tokens if t.isdigit()]
        if len(d_tokens) >= m4_p2_len and any(t in tokens for t in ['1', '2']):
            # M4 p2 answers are the last m4_p2_len digits of this line!
            ans_m4_p2 = d_tokens[-m4_p2_len:]
        elif len(d_tokens) == m5_target and all(1 <= d <= 4 for d in d_tokens):
            ans_m5 = d_tokens

    ans_m4 = ans_m4_p1 + ans_m4_p2
    return ans_m1, ans_m2, ans_m3, ans_m4, ans_m5

# Test across all 31 pages
for pidx in range(1, len(r.pages)):
    t = r.pages[pidx].extract_text()
    hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', t)
    if not hm: hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', t)
    y, m = hm.group(2) if int(hm.group(1)) <= 12 else hm.group(1), hm.group(1) if int(hm.group(1)) <= 12 else hm.group(2)
    exam_id = f"{y}_{int(m):02d}"
    c_raw = t.split('聴解')[1] if '聴解' in t else ''
    
    m1, m2, m3, m4, m5 = parse_choukai_robust(c_raw, exam_id)
    c_total = len(m1) + len(m2) + len(m3) + len(m4) + len(m5)
    
    with open(f"public/data/n2_exams/{exam_id}.json", 'r', encoding='utf-8') as fp:
        j_c_len = sum(1 for q in json.load(fp)['questions'] if q.get('sectionGroup') == 'listening')
        
    status = "OK" if c_total == j_c_len else f"MISMATCH ({c_total} vs {j_c_len})"
    print(f"[{exam_id}] Choukai: M1:{len(m1)} M2:{len(m2)} M3:{len(m3)} M4:{len(m4)} M5:{len(m5)} = {c_total} -> {status}")
