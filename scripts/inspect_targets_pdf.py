import os, glob, pypdf, re

def find_pdf_for_exam(year, month):
    patterns = [
        f"N2_DE_CAC_NAM/*{month}-{year}*/*.pdf",
        f"N2_DE_CAC_NAM/*{year}*{month}*/*.pdf",
        f"N2_DE_CAC_NAM/*{month}*{year}*/*.pdf",
    ]
    for pat in patterns:
        matches = glob.glob(pat)
        for m in matches:
            if 'script' not in m.lower():
                return m
    return None

test_cases = [
    (2010, 7, 12),
    (2011, 7, 12),
    (2011, 12, 12),
    (2012, 7, 12),
    (2012, 12, 12),
    (2013, 7, 12),
    (2013, 12, 12),
    (2014, 7, 12),
    (2014, 12, 12),
    (2015, 7, 12),
    (2015, 7, 41),
    (2015, 12, 12),
    (2016, 7, 12),
    (2016, 12, 12),
    (2017, 7, 12),
    (2017, 12, 12),
    (2018, 7, 12),
    (2018, 7, 21),
    (2018, 12, 12),
    (2018, 12, 35),
    (2018, 12, 52),
    (2019, 7, 12),
    (2019, 7, 52),
    (2019, 12, 12),
    (2019, 12, 61),
    (2020, 12, 12),
    (2020, 12, 32),
    (2021, 7, 12),
    (2021, 12, 12),
]

for y, m, qn in test_cases:
    pdf_path = find_pdf_for_exam(y, m)
    if not pdf_path:
        print(f"NOT FOUND PDF: {y}_{m:02d}")
        continue
    r = pypdf.PdfReader(pdf_path)
    found = False
    for idx, page in enumerate(r.pages):
        text = page.extract_text()
        # Look for question number
        if re.search(rf'(?:^|\s|\n)(?:{qn}|{chr(0xff10+qn//10)}{chr(0xff10+qn%10) if qn>=10 else ""})\s+[^\n]+', text):
            # Print matching snippet
            lines = text.split('\n')
            for l_idx, line in enumerate(lines):
                if re.search(rf'(?:^|\s)(?:{qn}|{chr(0xff10+qn//10) if qn>=10 else ""})\s+', line):
                    context = '\n'.join(lines[max(0, l_idx-1):min(len(lines), l_idx+4)])
                    print(f"[{y}_{m:02d} Q{qn} Page {idx+1}]:\n{context}\n")
                    found = True
                    break
            if found:
                break
