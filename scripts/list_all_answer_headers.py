import pypdf
import re

r = pypdf.PdfReader('20NgayN1.pdf')

for p in range(154, 160):
    txt = r.pages[p].extract_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    day_a = (p - 150) * 2 + 1
    day_b = day_a + 1
    print(f"\n==================================================")
    print(f"=== Page {p+1} (Day {day_a} & Day {day_b}) ===")
    print(f"==================================================")
    for i, l in enumerate(lines):
        if re.search(r'問題|鵬|腱|間圏|m|醒|第|p\.|寵|騨|躙', l):
            print(f"  Line {i:2d}: {l}")
