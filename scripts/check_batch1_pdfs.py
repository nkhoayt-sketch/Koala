import os, sys, pypdf, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N2_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')

folders = {
    '2024_07': '15. N2 7-2024',
    '2024_12': '15. N2 12-2024',
    '2023_07': '14. N2 7-2023',
    '2023_12': '14. N2 12-2023',
    '2022_07': '13. N2 7-2022',
    '2022_12': '13. N2 12-2022'
}

for exam, folder in folders.items():
    fpath = os.path.join(N2_DIR, folder)
    pdfs = [f for f in os.listdir(fpath) if f.endswith('.pdf')]
    booklet = [f for f in pdfs if 'script' not in f.lower()][0]
    script = [f for f in pdfs if 'script' in f.lower()][0]
    
    b_reader = pypdf.PdfReader(os.path.join(fpath, booklet))
    s_reader = pypdf.PdfReader(os.path.join(fpath, script))
    
    print(f"[{exam}] Booklet: {booklet} ({len(b_reader.pages)} pages) | Script: {script} ({len(s_reader.pages)} pages)")
