import os, glob, pypdf, re

def find_pdf(year, month):
    patterns = [
        f"N2_DE_CAC_NAM/*{month}-{year}*/*.pdf",
        f"N2_DE_CAC_NAM/*{year}*{month}*/*.pdf",
        f"N2_DE_CAC_NAM/*{month}*{year}*/*.pdf",
    ]
    for pat in patterns:
        for m in glob.glob(pat):
            if 'script' not in m.lower():
                return m
    return None

targets = [
    (2015, 7, 41),
    (2018, 7, 21),
    (2018, 12, 35),
    (2018, 12, 52),
    (2019, 7, 52),
    (2019, 12, 61),
    (2020, 12, 32),
]

for y, m, qn in targets:
    p = find_pdf(y, m)
    r = pypdf.PdfReader(p)
    found = False
    for pidx, page in enumerate(r.pages):
        text = page.extract_text()
        for i, line in enumerate(text.split('\n')):
            if re.search(rf'(?:^|\s)(?:{qn}|{chr(0xff10+qn//10)}{chr(0xff10+qn%10)})\s+', line):
                lines = text.split('\n')
                snippet = '\n'.join(lines[max(0, i-1):min(len(lines), i+6)])
                print(f"=== {y}_{m:02d} Q{qn} Page {pidx+1} ===\n{snippet}\n")
                found = True
                break
        if found: break
