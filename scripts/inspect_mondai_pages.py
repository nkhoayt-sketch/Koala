import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

def inspect_exam(folder_name):
    fpath = os.path.join('N2_DE_CAC_NAM', folder_name)
    pdfs = [f for f in os.listdir(fpath) if f.endswith('.pdf') and 'script' not in f.lower()]
    if not pdfs:
        print(f"No exam pdf in {folder_name}")
        return
    pdf_path = os.path.join(fpath, pdfs[0])
    reader = pypdf.PdfReader(pdf_path)
    print(f"=== {folder_name} : {pdfs[0]} ({len(reader.pages)} pages) ===")
    
    # Let's search for Mondai headers across pages
    for p_idx, page in enumerate(reader.pages):
        txt = page.extract_text() or ''
        m = re.findall(r'(問題\s*[1-9１-９一二三四五六七八九]+)', txt)
        if m:
            print(f"  Page {p_idx+1}: {m}")

inspect_exam('15. N2 7-2024')
inspect_exam('14. N2 7-2023')
inspect_exam('10. N2 7-2019')
inspect_exam('1. N2 7-2010')
