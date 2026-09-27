import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

for folder in ['15. N2 7-2024', '14. N2 7-2023', '10. N2 7-2019', '1. N2 7-2010']:
    fpath = os.path.join('N2_DE_CAC_NAM', folder)
    pdfs = [f for f in os.listdir(fpath) if f.endswith('.pdf') and 'script' not in f.lower()]
    reader = pypdf.PdfReader(os.path.join(fpath, pdfs[0]))
    # Page 1 text
    txt = reader.pages[0].extract_text()
    print(f"=== {folder} Page 1 ===")
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    for l in lines[:25]:
        print(l)
