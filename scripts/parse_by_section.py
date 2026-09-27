import pypdf
import re
import json

r = pypdf.PdfReader('N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')

def parse_page(pidx):
    text = r.pages[pidx].extract_text()
    
    header_match = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', text)
    if header_match:
        month = int(header_match.group(1))
        year = int(header_match.group(2))
    else:
        header_match = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', text)
        year = int(header_match.group(1))
        month = int(header_match.group(2))
    exam_id = f"{year}_{month:02d}"

    # Split into Gengo+Dokkai and Choukai
    parts = text.split('聴解')
    gengo_text = parts[0]
    choukai_text = parts[1] if len(parts) > 1 else ''

    # Let's inspect tokens in gengo_text
    # Replace '問題\n\d' with '問題\d'
    norm = re.sub(r'問題\s*[\r\n]+\s*([0-9１-９]+)', r'問題\1 ', gengo_text)
    norm = re.sub(r'(\d+)\s*問題\s*([0-9１-９]+)', r'\1 問題\2', norm)
    
    return exam_id, norm, choukai_text

exam_id, g_norm, c_norm = parse_page(1)
print(f"=== {exam_id} Normalized ===")
for l in g_norm.split('\n')[:35]:
    if l.strip():
        print(l.strip())
