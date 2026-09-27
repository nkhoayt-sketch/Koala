import sys
import os
import re
import json
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

ans_pdf = os.path.join('N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)
print(f"Total answer key pages: {len(reader.pages)}")

exam_answers = {}

for p_idx in range(1, len(reader.pages)):
    text = reader.pages[p_idx].extract_text()
    # Match exam title, e.g. "JLPT N2 12/2023" or "JLPT N2 7/2010"
    m = re.search(r'JLPT\s*N2\s*(\d{1,2})[\s/-]*(\d{4})|JLPT\s*N2\s*(\d{4})[\s/-]*(\d{1,2})', text, re.I)
    if not m:
        # Try finding year and month
        m_ym = re.search(r'(\d{1,2})/(\d{4})|(\d{4})/(\d{1,2})', text)
        if m_ym:
            if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
                month, year = int(m_ym.group(1)), int(m_ym.group(2))
            else:
                year, month = int(m_ym.group(3)), int(m_ym.group(4))
        else:
            print(f"Could not parse title on page {p_idx+1}")
            continue
    else:
        if m.group(1):
            month, year = int(m.group(1)), int(m.group(2))
        else:
            year, month = int(m.group(3)), int(m.group(4))

    # Parse question number to answer mapping for questions 1 to 56 (Vocab, Grammar, Reading)
    # Stop before Chokai (聴解)
    chokai_idx = text.find('聴解')
    if chokai_idx != -1:
        lang_text = text[:chokai_idx]
    else:
        lang_text = text

    # In lang_text, lines often have:
    # 1 2 3 4 5
    # 2 3 1 4 2
    # Let's inspect tokens
    print(f"Page {p_idx+1} -> Year: {year}, Month: {month:02d}")
