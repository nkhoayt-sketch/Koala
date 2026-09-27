import os, sys, re, glob

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')

folders = sorted([d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))])
print(f"Total folders: {len(folders)}")

for fld in folders:
    fpath = os.path.join(SOURCE_DIR, fld)
    files = os.listdir(fpath)
    scripts = [f for f in files if 'script' in f.lower() and f.endswith('.pdf')]
    mp3s = [f for f in files if f.endswith('.mp3')]
    exam_pdfs = [f for f in files if f.endswith('.pdf') and 'script' not in f.lower()]
    print(f"Folder: {fld}")
    print(f"  Exam: {exam_pdfs}")
    print(f"  Script: {scripts}")
    print(f"  MP3: {mp3s}")
