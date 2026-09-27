import sys
import os
import glob
import re
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

n2_root = None
for name in os.listdir('.'):
    if 'N2' in name and os.path.isdir(name):
        n2_root = name
        break

print(f"N2 Root: {n2_root}")

# Find all exam directories
dirs = sorted([d for d in os.listdir(n2_root) if os.path.isdir(os.path.join(n2_root, d))])
print(f"Total exam folders: {len(dirs)}")
for d in dirs:
    subpath = os.path.join(n2_root, d)
    files = os.listdir(subpath)
    exam_pdfs = [f for f in files if f.endswith('.pdf') and 'script' not in f.lower()]
    print(f"Folder: {d} -> Exam PDF: {exam_pdfs}")

# Find answer key
ans_pdf_path = os.path.join(n2_root, 'DAP AN JLPT N2 (update 10.4.2026).pdf')
if os.path.exists(ans_pdf_path):
    reader = pypdf.PdfReader(ans_pdf_path)
    print(f"\nAnswer Key PDF has {len(reader.pages)} pages")
    for idx, page in enumerate(reader.pages):
        txt = page.extract_text() or ''
        first_line = txt.strip().split('\n')[0] if txt else 'EMPTY'
        # Check if year/month mentions
        years = re.findall(r'(20\d\d)[^\d]*(12|7|07)', txt)
        print(f"Page {idx+1}: {first_line[:80]} | Matches: {years[:3]}")
