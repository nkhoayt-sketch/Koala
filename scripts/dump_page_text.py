import sys, os, re, json, pypdf

sys.stdout.reconfigure(encoding='utf-8')
ans_pdf = os.path.join('N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)

# Check Page 27 (2023_12) and Page 30 (2025_07)
for p in [27, 30]:
    print(f"=== FULL TEXT OF PAGE {p} ===")
    print(reader.pages[p].extract_text())
