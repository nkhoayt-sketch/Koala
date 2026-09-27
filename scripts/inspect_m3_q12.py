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

all_exams = [
    (2010, 7), (2010, 12), (2011, 7), (2011, 12), (2012, 7), (2012, 12),
    (2013, 7), (2013, 12), (2014, 7), (2014, 12), (2015, 7), (2015, 12),
    (2016, 7), (2016, 12), (2017, 7), (2017, 12), (2018, 7), (2018, 12),
    (2019, 7), (2019, 12), (2020, 12), (2021, 7), (2021, 12), (2022, 7),
    (2022, 12), (2023, 7), (2023, 12), (2024, 7), (2024, 12), (2025, 7), (2025, 12)
]

for y, m in all_exams:
    pdf_path = find_pdf_for_exam(y, m)
    if not pdf_path: continue
    r = pypdf.PdfReader(pdf_path)
    # usually page 2 has Mondai 3
    found_m3 = False
    for p_idx in [1, 2]: # 0-indexed page 2 or 3
        if p_idx >= len(r.pages): continue
        text = r.pages[p_idx].extract_text()
        if '問題 3' in text or '問題3' in text:
            # find 12
            for line in text.split('\n'):
                if re.search(r'(?:12|１２)\s+', line) or '12' in line:
                    print(f"[{y}_{m:02d} M3] {line}")
            found_m3 = True
            break
