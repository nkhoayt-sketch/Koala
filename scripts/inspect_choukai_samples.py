import pypdf
import re

r = pypdf.PdfReader('N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')

def print_choukai_lines(pidx):
    t = r.pages[pidx].extract_text()
    ct = re.sub(r'問題\s*[\r\n]+\s*', '問題', t.split('聴解')[1])
    lines = [l.strip() for l in ct.split('\n') if l.strip()]
    hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', t)
    y_m = f"{hm.group(2)}_{int(hm.group(1)):02d}" if hm else f"page_{pidx+1}"
    print(f"=== {y_m} CHOUKAI ({len(lines)} lines) ===")
    for i, l in enumerate(lines):
        print(f"{i:2d}: {l}")

for p in [1, 6, 12, 18, 24, 31]:
    print_choukai_lines(p)
