import pypdf
import re

r = pypdf.PdfReader('20NgayN1.pdf')

for p_idx in range(150, 161):
    txt = r.pages[p_idx].extract_text()
    print(f"==================================================")
    print(f"=== ANSWER PAGE {p_idx + 1} ===")
    print(f"==================================================")
    print(txt)
