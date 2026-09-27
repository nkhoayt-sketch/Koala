import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

def test_dokkai_structure(folder_name):
    fpath = os.path.join('N2_DE_CAC_NAM', folder_name)
    pdfs = [f for f in os.listdir(fpath) if f.endswith('.pdf') and 'script' not in f.lower()]
    reader = pypdf.PdfReader(os.path.join(fpath, pdfs[0]))
    
    # Collect all text from Dokkai start until Choukai
    dokkai_pages = []
    in_dokkai = False
    for p_idx, page in enumerate(reader.pages):
        txt = page.extract_text() or ''
        if ('読解' in txt or '問題 10' in txt or '問題10' in txt or '問題１０' in txt) and p_idx >= 5:
            in_dokkai = True
        if in_dokkai:
            if '聴解' in txt and ('問題 1' in txt or '問題１' in txt or '問題 １' in txt or p_idx >= len(reader.pages) - 8):
                break
            dokkai_pages.append((p_idx + 1, txt))
            
    print(f"\n==================== {folder_name} (Total Dokkai Pages: {len(dokkai_pages)}) ====================")
    for p_num, txt in dokkai_pages:
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        header = lines[0] if lines else ''
        m_headers = [l for l in lines if any(k in l for k in ['問題 10', '問題 11', '問題 12', '問題 13', '問題 14', '問題10', '問題11', '問題12', '問題13', '問題14', '（１）', '（２）', '（３）', '（４）', '（5）', '（５）'])]
        q_lines = [l for l in lines if re.match(r'^\d{2}\s+', l)]
        print(f"Page {p_num:2}: Headers={m_headers[:3]} | Qs={q_lines}")

test_dokkai_structure('15. N2 7-2024')
test_dokkai_structure('13. N2 7-2022')
test_dokkai_structure('9. N2 7-2018')
test_dokkai_structure('1. N2 7-2010')
