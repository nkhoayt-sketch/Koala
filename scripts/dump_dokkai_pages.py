import pypdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'N2_DE_CAC_NAM/14. N2 12-2023/14.N2 12-2023.pdf'
reader = pypdf.PdfReader(pdf_path)

for page_num in range(17, 32):
    print(f"\n#################### PAGE {page_num} ####################")
    print(reader.pages[page_num - 1].extract_text() or '')
