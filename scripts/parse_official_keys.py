import pypdf
import re
import json

r = pypdf.PdfReader('N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')

def to_half_width(s):
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

def parse_exam_page(pidx):
    raw_text = r.pages[pidx].extract_text()
    text = to_half_width(raw_text)
    
    # Get Year and Month
    hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', text)
    if hm:
        m, y = int(hm.group(1)), int(hm.group(2))
    else:
        hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', text)
        y, m = int(hm.group(1)), int(hm.group(2))
    exam_id = f"{y}_{m:02d}"

    parts = text.split('聴解')
    gengo_dokkai_text = parts[0]
    choukai_text = parts[1] if len(parts) > 1 else ''

    # Clean text: replace newlines inside '問題\n\d'
    g_text = re.sub(r'問題\s*[\r\n]+\s*([0-9]+)', r'問題\1 ', gengo_dokkai_text)
    g_lines = [l.strip() for l in g_text.split('\n') if l.strip()]

    # Parse Gengo & Dokkai
    # We can collect all question sequences and all answer sequences
    # Let's inspect the sections in Gengo Dokkai:
    # Notice: All questions are numbered 1 to N sequentially!
    # Let's see if we can extract pairs of (list_of_questions, list_of_answers)
    
    pairs = []
    # Let's run a state machine or block extractor
    return exam_id, g_lines, choukai_text

exam_id, g_lines, c_text = parse_exam_page(1)
print(f"Loaded {exam_id}")
