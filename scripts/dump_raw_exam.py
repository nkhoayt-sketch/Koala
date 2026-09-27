import sys, os, re, json, pypdf

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect the exact text of 15. N2 7-2024 from page 1 to 30
pdf_path = 'N2_DE_CAC_NAM/15. N2 7-2024/15. N2 7.2024.pdf'
reader = pypdf.PdfReader(pdf_path)

full_text_pages = []
for p in range(len(reader.pages)):
    txt = reader.pages[p].extract_text() or ''
    if '聴解' in txt and ('問題 1' in txt or '問題１' in txt or p >= 30):
        break
    full_text_pages.append((p+1, txt))

print(f"Loaded {len(full_text_pages)} pages for exam before Choukai.")

# Let's check how questions are matched
all_text = ""
for p_num, txt in full_text_pages:
    lines = txt.split('\n')
    clean = []
    for l in lines:
        ls = l.strip()
        if re.match(r'^N2\s+\d+/\d+', ls) or re.match(r'^JLPT[・\s]N2', ls):
            continue
        if re.match(r'^\d{1,2}$', ls): # page number
            continue
        clean.append(l)
    all_text += f"\n<<<PAGE_{p_num}>>>\n" + "\n".join(clean)

with open('scripts/exam_2024_07_raw.txt', 'w', encoding='utf-8') as f:
    f.write(all_text)

print("Wrote exam_2024_07_raw.txt, size:", len(all_text))
