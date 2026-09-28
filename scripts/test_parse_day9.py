import pypdf
import re
import json

r = pypdf.PdfReader('20NgayN1.pdf')

# Day 9 pages:
# P69: M1 (Q1..6)
# P70: M2 (Q7..13)
# P73: M3 (Q14..19), M4 (Q20..22)
# P74: M4 (Q23..25)
# P75: M5 (Q26..35)
# P76: M6 (Q36..40)
# P71-72: M7 (Q41..45 with passage)

def print_page_clean(p_num):
    txt = r.pages[p_num - 1].extract_text()
    print(f"=== Page {p_num} ===")
    print(txt[:600])

for p in [69, 70, 73, 74, 75, 76, 71]:
    print_page_clean(p)
