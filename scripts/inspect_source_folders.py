import os, re, glob
import pypdf

SOURCE_DIR = 'N2_DE_CAC_NAM'
folders = sorted([d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))])
print(f"Total folders: {len(folders)}")

ans_pdf = os.path.join(SOURCE_DIR, 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader_ans = pypdf.PdfReader(ans_pdf)
print(f"Answer key pages: {len(reader_ans.pages)}")

# Check what each folder contains
for fld in folders[:10]:
    fpath = os.path.join(SOURCE_DIR, fld)
    files = os.listdir(fpath)
    pdfs = [f for f in files if f.endswith('.pdf')]
    mp3s = [f for f in files if f.endswith('.mp3')]
    print(f"\nFolder: {fld}")
    print(f"  PDFs: {pdfs}")
    print(f"  MP3s: {mp3s}")
