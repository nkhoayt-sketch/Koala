import pypdf
import re
import json

r = pypdf.PdfReader('20NgayN1.pdf')

def extract_tokens_from_page(p_idx):
    txt = r.pages[p_idx].extract_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    
    # We want to extract answer numbers from lines
    ans_list = []
    for l in lines:
        # Check if line is a header
        if any(h in l for h in ['第', 'p.', '解答']):
            continue
            
        # Match box + number, or just box + ], or just number
        # e.g., '□ 2', '回 4', '□ ]', '睡∃ 1', '‐□ 1'
        m = re.search(r'[□回国匝巨匡匿睡睦腱贖鵬醒厘匹國囲図日]\s*([1-4]|\]|‐\s*1)', l)
        if m:
            val = m.group(1)
            ans = 1 if (val == ']' or '1' in val) else int(val)
            ans_list.append((ans, l))
        elif re.match(r'^[1-4]$', l):
            ans_list.append((int(l), l))
        elif re.search(r'\]\s*([1-4])', l):
            ans_list.append((int(re.search(r'\]\s*([1-4])', l).group(1)), l))
            
    return ans_list

for p_num in range(151, 161):
    tokens = extract_tokens_from_page(p_num - 1)
    day_a = (p_num - 151) * 2 + 1
    day_b = day_a + 1
    print(f"Page {p_num}: {len(tokens)} answers extracted for Days {day_a} and {day_b}")
