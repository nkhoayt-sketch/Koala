import pypdf
import re

r = pypdf.PdfReader('N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')

def analyze_page_blocks(pidx):
    text = r.pages[pidx].extract_text()
    # Separate into Gengo/Dokkai part and Choukai part
    parts = text.split('聴解')
    gengo_dokkai = parts[0]
    choukai = parts[1] if len(parts) > 1 else ''
    
    print(f"=== Page {pidx+1} ===")
    print("--- Gengo Dokkai Raw ---")
    print(gengo_dokkai[:500])
    print("--- Choukai Raw ---")
    print(choukai)

analyze_page_blocks(1) # 2010_07
analyze_page_blocks(31) # 2025_12
