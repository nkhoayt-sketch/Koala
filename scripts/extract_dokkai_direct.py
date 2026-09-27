import pypdf
import os

pdf_path = r'N2_DE_CAC_NAM\14. N2 12-2023\14.N2 12-2023.pdf'
reader = pypdf.PdfReader(pdf_path)

with open('scripts/dokkai_direct.txt', 'w', encoding='utf-8') as out:
    for page_num in range(17, 32):
        out.write(f"\n\n#################### PAGE {page_num} ####################\n\n")
        text = reader.pages[page_num - 1].extract_text() or ''
        out.write(text)

print("Extracted successfully!")
