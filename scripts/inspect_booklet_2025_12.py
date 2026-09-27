import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'N2_DE_CAC_NAM/17.N2 12-2025/17.N2 12-2025 _260603.pdf'
reader = pypdf.PdfReader(pdf_path)

print(f"Total pages: {len(reader.pages)}")
# Search for Choukai in booklet
for p_idx, p in enumerate(reader.pages):
    txt = p.extract_text() or ''
    if '聴解' in txt or '問題 1' in txt or '問題１' in txt:
        print(f"Page {p_idx+1}: {txt[:150].replace('\n', ' ')}")
