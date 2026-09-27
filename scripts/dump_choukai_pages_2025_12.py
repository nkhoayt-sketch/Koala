import sys, pypdf

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'N2_DE_CAC_NAM/17.N2 12-2025/17.N2 12-2025 _260603.pdf'
reader = pypdf.PdfReader(pdf_path)

for p in range(31, len(reader.pages)):
    print(f"\n==================== PAGE {p+1} ====================")
    print(reader.pages[p].extract_text())
