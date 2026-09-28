import pypdf

r = pypdf.PdfReader('20NgayN1.pdf')
for p in range(130, 151):
    txt = r.pages[p].extract_text()
    first_line = txt.strip().split('\n')[0] if txt else 'EMPTY'
    print(f"Page {p+1}: {first_line[:80]}")
