import pypdf
import re

r = pypdf.PdfReader('20NgayN1.pdf')

# Let's inspect Day 9 (starts page 69)
print("=== DAY 9 TEXT SAMPLES ===")
for p in [69, 70, 73, 74, 75, 76, 71, 72]:
    txt = r.pages[p-1].extract_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    print(f"--- Page {p} ({len(lines)} lines) ---")
    for l in lines[:6]:
        print(" ", l)
