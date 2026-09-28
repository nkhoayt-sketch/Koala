import json
import os
import re
import pypdf

# Load official answers for all days from PDF
r = pypdf.PdfReader('20NgayN1.pdf')

def get_official_answers(day_num):
    p_num = 150 + ((day_num - 1) // 2) + 1
    is_second_day = (day_num % 2 == 0)
    
    txt = r.pages[p_num - 1].extract_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    
    ans_list = []
    for l in lines:
        if any(h in l for h in ['第', 'p.', '解答']):
            continue
        m = re.search(r'[□回国匝巨匡匿睡睦腱贖鵬醒厘匹國囲図日]\s*([1-4]|\]|‐\s*1)', l)
        if m:
            val = m.group(1)
            ans = 1 if (val == ']' or '1' in val) else int(val)
            ans_list.append(ans)
        elif re.match(r'^[1-4]$', l):
            ans_list.append(int(l))
            
    if is_second_day:
        sub = ans_list[45:90] if len(ans_list) >= 90 else ans_list[-45:]
    else:
        sub = ans_list[:45]
        
    while len(sub) < 45:
        sub.append(1)
    return [x - 1 for x in sub[:45]] # return 0-indexed

print("Official answers loaded for all days.")
