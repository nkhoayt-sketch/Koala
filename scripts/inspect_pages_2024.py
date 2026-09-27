import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'N2_DE_CAC_NAM/15. N2 7-2024/15. N2 7.2024.pdf'
reader = pypdf.PdfReader(pdf_path)

for p in [9, 10, 11, 12, 13, 16, 17, 24, 25, 26, 27, 28, 29]:
    txt = reader.pages[p].extract_text()
    first_few = '\n'.join(txt.split('\n')[:8])
    print(f"--- PAGE {p+1} ---")
    print(first_few)
