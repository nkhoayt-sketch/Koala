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

def parse_choukai(c_text):
    # Normalize
    text = re.sub(r'問題\s*[\r\n]+\s*', '問題', c_text)
    
    # We want answers for M1 (5), M2 (5 or 6), M3 (4 or 5), M4 (11 or 12), M5 (3 or 4)
    # Let's inspect all lines in c_text
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Find all tokens that are single digits 1..4 representing answers
    # Notice: Lines that contain '問題' or '1 2 3 4 5' might have answers mixed or on next line.
    
    # Let's see:
    # M1 & M2:
    # e.g.:
    # 問題1
    # 1 2 3 4 5 問題2
    # 1 2 3 4 5 6
    # 4 3 2 3 3  3 2 2 2 2 4
    # OR in 2022_07:
    # 1 2 3 4 5 6  4 1 3 2 3  1 4 3 2 1 3
    
    ans_m1, ans_m2, ans_m3, ans_m4, ans_m5 = [], [], [], [], []
    
    # Let's extract by searching for the answer patterns
    # In Choukai:
    # All answers are in [1, 2, 3, 4]
    return lines

for p in [1, 6, 18, 24, 31]:
    t = to_half(r.pages[p].extract_text())
    c_part = t.split('聴解')[1] if '聴解' in t else ''
    print(f"=== Page {p+1} ===")
    lines = parse_choukai(c_part)
    for l in lines:
        print(repr(l))
