import pypdf
import json
import re

r = pypdf.PdfReader('20NgayN1.pdf')
print(f"Total pages in 20NgayN1.pdf: {len(r.pages)}")

# Print TOC (page 6 in PDF = index 5)
print("=== TOC ===")
print(r.pages[5].extract_text())

# Print sample text from answer pages (pages 151 to 160 = index 150 to 159)
for idx in range(150, len(r.pages)):
    txt = r.pages[idx].extract_text()
    first_line = txt.strip().split('\n')[0] if txt else 'EMPTY'
    print(f"Answer page {idx+1}: {first_line[:60]}")
