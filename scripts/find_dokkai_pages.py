import pypdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'N2_DE_CAC_NAM/14. N2 12-2023/14.N2 12-2023.pdf'
reader = pypdf.PdfReader(pdf_path)
print(f"Total pages in 14.N2 12-2023.pdf: {len(reader.pages)}")

# Search for Mondai 10, 11, 12, 13, 14
for i, page in enumerate(reader.pages):
    text = page.extract_text() or ''
    for keyword in ['問題10', '問題11', '問題12', '問題13', '問題14']:
        if keyword in text:
            print(f"Page {i+1} mentions {keyword}")
