import sys
import os
import pypdf
import re

sys.stdout.reconfigure(encoding='utf-8')

ans_pdf = os.path.join('N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)
print(f"Total pages: {len(reader.pages)}")

# Print preview of each page
for i in range(len(reader.pages)):
    txt = reader.pages[i].extract_text() or ''
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    header = " | ".join(lines[:3]) if lines else "EMPTY"
    print(f"Page {i+1}: {header[:120]}")
