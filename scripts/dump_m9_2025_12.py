import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'N2_DE_CAC_NAM/17.N2 12-2025/17.N2 12-2025 _260603.pdf'
reader = pypdf.PdfReader(pdf_path)

# Find page with Mondai 9
for p_idx, page in enumerate(reader.pages):
    txt = page.extract_text() or ''
    if '問題 9' in txt or '問題9' in txt or '文章の文法' in txt:
        print(f"=== PAGE {p_idx+1} ===")
        print(txt)
        # also print next page
        if p_idx + 1 < len(reader.pages):
            print(f"=== PAGE {p_idx+2} ===")
            print(reader.pages[p_idx+1].extract_text() or '')
        break
