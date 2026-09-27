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
    (2010, 7), (2011, 7), (2011, 12), (2012, 7), (2012, 12), (2013, 7),
    (2013, 12), (2014, 7), (2014, 12), (2015, 7), (2015, 12), (2016, 7),
    (2016, 12), (2017, 7), (2017, 12), (2018, 7), (2018, 12), (2019, 7),
    (2019, 12), (2020, 12), (2021, 7), (2021, 12)
]

for y, m in targets:
    p = find_pdf(y, m)
    if not p:
        print(f"Missing PDF: {y}_{m:02d}")
        continue
    r = pypdf.PdfReader(p)
    # search across first 4 pages
    found = False
    for pidx in range(min(5, len(r.pages))):
        text = r.pages[pidx].extract_text()
        if '12' in text and ('問題 3' in text or '問題3' in text or '（   ）' in text or '（  ）' in text):
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if re.search(r'(?:^|\s)(?:12|１２)\s+', line):
                    snippet = '\n'.join(lines[i:min(len(lines), i+3)])
                    print(f"=== {y}_{m:02d} Q12 ===\n{snippet}\n")
                    found = True
                    break
            if found: break
