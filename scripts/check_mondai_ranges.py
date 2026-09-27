import sys, os, re, json, pypdf

sys.stdout.reconfigure(encoding='utf-8')

ans_pdf = os.path.join('N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)

def parse_exam_mondai_ranges(p_idx):
    text = reader.pages[p_idx].extract_text()
    chokai_idx = text.find('聴解')
    if chokai_idx != -1:
        text = text[:chokai_idx]
    
    # We want to map each Mondai 1..14 to its list of question numbers
    # Pattern: "問題 [number]" followed by question numbers
    # Let's inspect tokens
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    cleaned = []
    for l in lines:
        if any(h in l for h in ['JLPT', '文字・語彙', '文法', '読解', 'ĐÁP ÁN']) or re.match(r'^\d{1,2}$', l):
            continue
        cleaned.append(l)
    return cleaned

for p in [1, 10, 18, 20, 27, 30]:
    txt = reader.pages[p].extract_text()
    m_ym = re.search(r'(\d{1,2})[/.-](\d{4})|(\d{4})[/.-](\d{1,2})', txt)
    print(f"\n=== PAGE {p} ({m_ym.group(0) if m_ym else ''}) ===")
    cl = parse_exam_mondai_ranges(p)
    print("Cleaned lines sample:")
    for l in cl[:15]:
        print(" ", repr(l))
