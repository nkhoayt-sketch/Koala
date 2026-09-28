import pypdf

r = pypdf.PdfReader('20NgayN1.pdf')
p70 = r.pages[69].extract_text()
for l in [x.strip() for x in p70.split('\n') if x.strip()]:
    print(" ", l)
