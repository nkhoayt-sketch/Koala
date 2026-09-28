import pypdf
import re

r = pypdf.PdfReader('20NgayN1.pdf')

mondai1_pages = []
for p in range(len(r.pages)):
    txt = r.pages[p].extract_text()
    if txt and ('問題 1' in txt or '問題1' in txt or '問題 ]' in txt or '問題]' in txt):
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        # check if it is reading question (読み方 or 漢字)
        first_few = " ".join(lines[:4])
        if '読み方' in first_few or '言葉の読み方' in first_few or '最もよいもの' in first_few:
            # check if it is the start of a day
            mondai1_pages.append((p + 1, lines[0] if lines else '', lines[1] if len(lines) > 1 else ''))

print(f"Total Mondai 1 pages found: {len(mondai1_pages)}")
for p, l1, l2 in mondai1_pages:
    print(f"Page {p:3d}: {l1[:40]} | {l2[:50]}")
