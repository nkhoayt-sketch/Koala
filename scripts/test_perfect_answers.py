import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')
ans_pdf = os.path.join('N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)

def parse_answer_page_perfect(p_idx):
    text = reader.pages[p_idx].extract_text()
    chokai_idx = text.find('聴解')
    if chokai_idx != -1:
        text = text[:chokai_idx]
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    cleaned = []
    for l in lines:
        if any(h in l for h in ['JLPT', '文字・語彙', '文法', '読解', 'ĐÁP ÁN']) or re.match(r'^\d{1,2}$', l):
            continue
        cleaned.append(l)

    # Let's inspect numbers in lines
    q_to_ans = {}
    pending_qs = []
    
    for l in cleaned:
        # Split tokens
        # Remove '問題' and kanji numbers
        clean_l = re.sub(r'問題\s*[0-9０-９一二三四五六七八九１-９]*', ' ', l)
        nums = [int(x) for x in re.findall(r'\b\d+\b', clean_l)]
        if not nums:
            continue
        
        # If nums has values > 4, or starts with next expected question:
        next_expected = len(q_to_ans) + len(pending_qs) + 1
        is_q = False
        if any(n > 4 for n in nums):
            is_q = True
        elif nums[0] == next_expected:
            if not pending_qs:
                is_q = True
            elif len(nums) != len(pending_qs):
                # could be more questions?
                pass
        
        if is_q:
            pending_qs.extend(nums)
        else:
            # These are answers for pending_qs!
            for a in nums:
                if pending_qs:
                    q = pending_qs.pop(0)
                    q_to_ans[q] = a
                else:
                    print(f"Warning: excess answer {a} on page {p_idx}")
                    
    return q_to_ans

for p in range(1, len(reader.pages)):
    text = reader.pages[p].extract_text()
    m_ym = re.search(r'(\d{1,2})[/.-](\d{4})|(\d{4})[/.-](\d{1,2})', text)
    year, month = None, None
    if m_ym:
        if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
            month, year = int(m_ym.group(1)), int(m_ym.group(2))
        else:
            year, month = int(m_ym.group(3)), int(m_ym.group(4))
    res = parse_answer_page_perfect(p)
    q_max = max(res.keys()) if res else 0
    q_min = min(res.keys()) if res else 0
    missing = [q for q in range(1, q_max + 1) if q not in res]
    print(f"Page {p:2} ({year}_{month:02d}): total {len(res)} ans | range Q{q_min}-Q{q_max} | missing: {missing}")
