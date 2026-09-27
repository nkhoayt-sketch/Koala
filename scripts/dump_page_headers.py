import pypdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'N2_DE_CAC_NAM/14. N2 12-2023/14.N2 12-2023.pdf'
reader = pypdf.PdfReader(pdf_path)

for i in range(len(reader.pages)):
    text = (reader.pages[i].extract_text() or '').strip()
    first_lines = '\n'.join([l.strip() for l in text.split('\n') if l.strip()][:3])
    print(f"=== PAGE {i+1} ===")
    print(first_lines[:150])
