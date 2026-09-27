import sys, os, re, json, pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ans_pdf = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)

def parse_choukai_robust(p_idx):
    txt = reader.pages[p_idx].extract_text()
    chokai_idx = txt.find('聴解')
    if chokai_idx == -1: return {}
    c_txt = txt[chokai_idx:]
    
    # Strip headers
    lines = [l.strip() for l in c_txt.split('\n') if l.strip()]
    cleaned = []
    for l in lines:
        if '聴解' in l or 'ĐÁP ÁN' in l or re.match(r'^\d{1,2}$', l):
            continue
        cleaned.append(l)
        
    # We want to extract (Mondai, Question_in_mondai) -> answer
    # Notice the numbers pattern in Choukai:
    # Let's inspect tokens and parse them sequentially
    # In each answer page, the answer values are in 1..4 (or 1..3 for M4)
    # Let's collect all blocks
    return cleaned

for p in [1, 5, 10, 15, 20, 25, 27, 30]:
    txt = reader.pages[p].extract_text()
    m_ym = re.search(r'(\d{1,2})[/.-](\d{4})|(\d{4})[/.-](\d{1,2})', txt)
    print(f"\n=== PAGE {p} ({m_ym.group(0) if m_ym else ''}) ===")
    cl = parse_choukai_robust(p)
    for idx, l in enumerate(cl):
        print(f"  {idx:2}: {repr(l)}")
