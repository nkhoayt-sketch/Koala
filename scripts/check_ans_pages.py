import os, re, glob
import pypdf

ans_pdf = 'N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf'
reader = pypdf.PdfReader(ans_pdf)
print(f"Total pages: {len(reader.pages)}")

# Extract text from all pages and test answer extraction
for p_idx in range(len(reader.pages)):
    text = reader.pages[p_idx].extract_text()
    m_ym = re.search(r'(\d{1,2})[/.-](\d{4})|(\d{4})[/.-](\d{1,2})', text)
    year, month = None, None
    if m_ym:
        if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
            month, year = int(m_ym.group(1)), int(m_ym.group(2))
        elif m_ym.group(3) and int(m_ym.group(3)) >= 2010:
            year, month = int(m_ym.group(3)), int(m_ym.group(4))
    first_line = text.split('\n')[0] if text else ''
    print(f"Page {p_idx:2}: detected {year}_{month if month else 0:02d} | Header: {first_line[:50]}")
