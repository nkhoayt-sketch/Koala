import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

for folder in ['15. N2 7-2024', '14. N2 7-2023']:
    fpath = os.path.join('N2_DE_CAC_NAM', folder)
    pdfs = [f for f in os.listdir(fpath) if f.endswith('.pdf') and 'script' not in f.lower()]
    reader = pypdf.PdfReader(os.path.join(fpath, pdfs[0]))
    for p_idx in range(len(reader.pages)):
        txt = reader.pages[p_idx].extract_text() or ''
        if '問題 5' in txt or '問題５' in txt:
            print(f"=== {folder} Page {p_idx+1} ===")
            print('\n'.join(txt.split('\n')[:25]))
            break
