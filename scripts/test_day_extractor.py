import pypdf
import re
import json

r = pypdf.PdfReader('20NgayN1.pdf')

def extract_page_text(p_num):
    if p_num <= len(r.pages):
        return r.pages[p_num - 1].extract_text() or ""
    return ""

# Test extracting Day 9 questions
p69 = extract_page_text(69)
# Mondai 1 lines
lines = [l.strip() for l in p69.split('\n') if l.strip()]
print("Page 69 lines:")
for l in lines:
    print("  ", l)
