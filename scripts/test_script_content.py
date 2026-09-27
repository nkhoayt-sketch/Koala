import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')

def inspect_script(folder):
    fpath = os.path.join(SOURCE_DIR, folder)
    scripts = [f for f in os.listdir(fpath) if 'script' in f.lower() and f.endswith('.pdf')]
    if not scripts: return
    reader = pypdf.PdfReader(os.path.join(fpath, scripts[0]))
    print(f"\n==================== {folder} ({scripts[0]}, {len(reader.pages)} pages) ====================")
    full_text = ""
    for p in range(min(5, len(reader.pages))):
        full_text += f"\n--- Page {p+1} ---\n" + (reader.pages[p].extract_text() or '')
    print(full_text[:1200] + "...")

inspect_script('15. N2 7-2024')
inspect_script('14. N2 7-2023')
inspect_script('10. N2 7-2019')
inspect_script('1. N2 7-2010')
