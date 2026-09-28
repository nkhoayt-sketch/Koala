import pypdf
import re

r = pypdf.PdfReader('20NgayN1.pdf')

for p in [46, 54, 62, 70, 78, 86, 94, 102, 110, 118, 126, 130, 138]:
    if p < len(r.pages):
        txt = r.pages[p].extract_text()
        print(f"=== PDF Page {p+1} ===")
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        for l in lines[:5]:
            print("  ", l)
