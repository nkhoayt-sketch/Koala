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

def parse_full_page(pidx):
    raw_text = r.pages[pidx].extract_text()
    text = to_half(raw_text)
    
    # Year and Month
    hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', text)
    if hm:
        m, y = int(hm.group(1)), int(hm.group(2))
    else:
        hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', text)
        y, m = int(hm.group(1)), int(hm.group(2))
    exam_id = f"{y}_{m:02d}"

    parts = text.split('聴解')
    gengo_raw = parts[0]
    choukai_raw = parts[1] if len(parts) > 1 else ''

    # Clean Gengo
    g_text = re.sub(r'問題\s*[\r\n]+\s*', '問題', gengo_raw)
    g_lines = [l.strip() for l in g_text.split('\n') if l.strip()]

    # Extract all answers for Gengo / Dokkai
    # Look at the structure of lines:
    # 1) Line containing '問題1' ... '問題2'
    # 2) Line containing '1 2 3 4 5'
    # 3) Line containing '6 7 8 9 10'
    # 4) Answer line: 10 numbers for Q1..10
    # Let's write a robust regex/digit extractor for each known block
    
    gengo_keys = {}
    
    # Let's inspect all digit-only tokens on lines:
    # Notice: In the PDF, answers for each problem block are separated.
    # Block 1 (M1 & M2):
    # Questions are 1..5 and 6..10.
    # Answer line has 10 digits in 1..4.
    
    # Block 2 (M3 & M4):
    # Questions are 11..13 (or 15) and 14..20 (or 16..22).
    # Then answers.
    # If 21 22 exists, then its answers.
    
    # Block 3 (M5 & M6):
    # Questions are 21..25 (or 23..27) and 26..30 (or 28..32).
    # Then 10 answers.
    
    # Block 4 (M7):
    # Questions 31..42 (or 33..44).
    # Then 12 answers.
    
    # Block 5 (M8 & M9):
    # Questions 43..47 (or 45..49) and 48..51 (or 50..54).
    # Then 9 (or 10) answers.
    
    # Block 6 (M10 & M11):
    # Questions 52..56 (or 55..59) and 57..62 (or 60..65).
    # Then 11 answers.
    # Followed by 63..64 (or 66..68) and their answers (2 or 3 answers).
    
    # Block 7 (M12, M13, M14):
    # Questions 65..66, 67..69, 70..71 (or 69..70, 71..73, 74..75).
    # Then 7 answers (2 + 3 + 2).
    
    return exam_id, g_lines, choukai_raw

exam_id, g_lines, c_raw = parse_full_page(1)
print(f"Page 2 successfully parsed for {exam_id}")
