import pypdf
import re
import json

r = pypdf.PdfReader('20NgayN1.pdf')

def get_day_answers(day_num):
    # Answer pages:
    # Page 151: Days 1, 2
    # Page 152: Days 3, 4
    # Page 153: Days 5, 6
    # Page 154: Days 7, 8
    # Page 155: Days 9, 10
    # Page 156: Days 11, 12
    # Page 157: Days 13, 14
    # Page 158: Days 15, 16
    # Page 159: Days 17, 18
    # Page 160: Days 19, 20
    p_num = 150 + ((day_num - 1) // 2) + 1
    is_second_day = (day_num % 2 == 0)
    
    txt = r.pages[p_num - 1].extract_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    
    # Extract all answers on this page
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
            
    # Typically 82-90 answers per page (45 for day A, 45 for day B)
    if is_second_day:
        return ans_list[45:90] if len(ans_list) >= 90 else ans_list[-45:]
    else:
        return ans_list[:45]

for d in range(9, 21):
    ans = get_day_answers(d)
    print(f"Day {d}: {len(ans)} answers: {ans[:10]}...")
