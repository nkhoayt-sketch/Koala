import sys
import os
import re
import json
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = os.path.join('N2_DE_CAC_NAM', '14. N2 7-2023', '14. N2 7-2023.pdf')
reader = pypdf.PdfReader(pdf_path)

# Let's extract text of all pages until 聴解 or 読解
all_text = ""
for idx, page in enumerate(reader.pages):
    txt = page.extract_text() or ''
    # If this page is listening, stop
    if '聴解' in txt and ('問題 1' in txt or '問題１' in txt):
        print(f"Listening section found at page {idx+1}")
        break
    all_text += f"\n--- PAGE {idx+1} ---\n" + txt

print(f"Total extracted chars: {len(all_text)}")

# Let's write all_text to a sample file to see the patterns
with open('scripts/sample_exam_text.txt', 'w', encoding='utf-8') as f:
    f.write(all_text)

print("Saved sample exam text to scripts/sample_exam_text.txt")
