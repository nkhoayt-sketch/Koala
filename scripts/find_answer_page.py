import pypdf
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

n2_dir = 'N2_DE_CAC_NAM'
answer_file = None
for f in os.listdir(n2_dir):
    if f.endswith('.pdf') and ('update' in f.lower() or 'dap' in f.lower() or '\u0111\u00e1p' in f.lower() or '\u0110\u00c1P' in f):
        answer_file = os.path.join(n2_dir, f)
        break

print("Found answer file:", answer_file)
if answer_file:
    reader = pypdf.PdfReader(answer_file)
    print(f"Total pages: {len(reader.pages)}")
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ''
        if '2023' in text and '12' in text:
            print(f"\n==================== ANSWER PAGE {i+1} (2023-12) ====================")
            print(text)
