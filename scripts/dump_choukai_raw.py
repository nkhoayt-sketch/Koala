import pypdf
import re

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

with open('scripts/all_choukai_raw.txt', 'w', encoding='utf-8') as out:
    for pidx in range(1, len(r.pages)):
        text = to_half(r.pages[pidx].extract_text())
        hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', text)
        if not hm:
            hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', text)
            y, m = hm.group(1), hm.group(2)
        else:
            m, y = hm.group(1), hm.group(2)
            
        y_m = f"{y}_{int(m):02d}"
        c_part = text.split('聴解')[1] if '聴解' in text else ''
        out.write(f"================ {y_m} ================\n")
        out.write(c_part.strip() + "\n\n")

print("Saved all_choukai_raw.txt")
