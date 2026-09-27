import pypdf
import re

r = pypdf.PdfReader('N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')

def parse_gengo_dokkai_page(pidx):
    text = r.pages[pidx].extract_text()
    parts = text.split('聴解')
    gengo_text = parts[0]
    
    # Let's inspect tokens and numbers
    # In each section, there are question number rows, and answer rows.
    # Answer digits are ONLY 1, 2, 3, 4!
    # Question numbers are > 0.
    print(f"=== Page {pidx+1} lines ===")
    lines = [l.strip() for l in gengo_text.split('\n') if l.strip()]
    for idx, l in enumerate(lines):
        print(f"{idx:2d}: {l}")

parse_gengo_dokkai_page(1)
