import pypdf
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'N2_DE_CAC_NAM\ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf'
reader = pypdf.PdfReader(pdf_path)
page = reader.pages[27] # 0-indexed page 28
lines = (page.extract_text() or '').split('\n')

for idx, line in enumerate(lines):
    if '読解' in line or '52' in line or '57' in line or '65' in line or '67' in line or '70' in line:
        for offset in range(max(0, idx - 2), min(len(lines), idx + 8)):
            print(f"{offset}: {lines[offset]}")
        break
