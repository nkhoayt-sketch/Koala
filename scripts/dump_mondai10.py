import pypdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'N2_DE_CAC_NAM\14. N2 12-2023\14.N2 12-2023.pdf'
reader = pypdf.PdfReader(pdf_path)

with open('scripts/mondai10_text.txt', 'w', encoding='utf-8') as f:
    for page_num in range(12, 17):
        f.write(f"\n=== PAGE {page_num} ===\n")
        f.write(reader.pages[page_num - 1].extract_text() or '')

print("Mondai 10 dumped.")
