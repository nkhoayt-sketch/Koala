import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')

def inspect_booklet_choukai(folder):
    fpath = os.path.join(SOURCE_DIR, folder)
    pdfs = [f for f in os.listdir(fpath) if f.endswith('.pdf') and 'script' not in f.lower()]
    if not pdfs: return
    reader = pypdf.PdfReader(os.path.join(fpath, pdfs[0]))
    
    # Choukai pages are the last few pages
    print(f"\n==================== {folder} ({pdfs[0]}, {len(reader.pages)} pages) ====================")
    for p_idx in range(len(reader.pages) - 7, len(reader.pages)):
        if p_idx < 0: continue
        txt = reader.pages[p_idx].extract_text() or ''
        if '聴解' in txt or '問題 1' in txt or '問題１' in txt:
            print(f"--- Page {p_idx+1} ---")
            print(txt[:600] + "...\n")

inspect_booklet_choukai('15. N2 7-2024')
inspect_booklet_choukai('14. N2 7-2023')
