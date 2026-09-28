import pypdf
import re
import json

r = pypdf.PdfReader('20NgayN1.pdf')

def parse_answer_tokens(lines):
    answers = []
    for l in lines:
        l = l.strip()
        # Check if line contains an answer token
        # Pattern: box symbol then digit or ']' (which represents 1)
        # Or line is just a digit 1..4
        # Or '] 1' or '‐ 1'
        m = re.search(r'[□回国匝巨匡匿睡睦腱贖鵬醒厘匹國囲図日]\s*([1-4]|\]|‐\s*1)', l)
        if m:
            val = m.group(1)
            if val == ']' or '1' in val:
                answers.append(1)
            else:
                answers.append(int(val))
        elif re.match(r'^[1-4]$', l):
            answers.append(int(l))
    return answers

# Test on page 154 (Days 7 and 8)
txt154 = r.pages[153].extract_text()
lines154 = [l.strip() for l in txt154.split('\n') if l.strip()]

# Find split point between Day 7 and Day 8:
# Notice on page 154: '第 7国 p.54-61' is in the middle!
# Let's inspect where '第' or '問題 1' or '問題 ]' appears
for i, l in enumerate(lines154):
    if '問題' in l or '第' in l or 'p.' in l:
        print(f"Line {i:2d}: {l}")
