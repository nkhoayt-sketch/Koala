import pypdf
import re

r = pypdf.PdfReader('20NgayN1.pdf')

# Let's inspect the page blocks for days 9 to 20
# Day 9 starts at PDF page 69
# Let's inspect pages 69 to 146
print("Inspecting pages 69 to 146...")

# Let's find every "問題" in pages 69 to 146
for p_idx in range(68, 147):
    txt = r.pages[p_idx].extract_text()
    if not txt:
        print(f"Page {p_idx+1}: EMPTY")
        continue
    # Find all Mondai occurrences
    m_matches = re.findall(r'問題\s*[0-9１-９\]フ]', txt)
    first_few = txt.strip().split('\n')[0][:50]
    print(f"Page {p_idx+1:3d}: Mondais={m_matches} | {first_few}")
