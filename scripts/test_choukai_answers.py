import sys, os, re, json, pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ans_pdf = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)

def parse_choukai_page_answers(p_idx):
    text = reader.pages[p_idx].extract_text()
    chokai_idx = text.find('聴解')
    if chokai_idx == -1:
        return {}
    chokai_text = text[chokai_idx:]
    
    # Split by 問題 1..5
    m_splits = re.split(r'(?:^|\n)\s*問題\s*([1-5１-５一二三四五]+)', chokai_text)
    mondais = {}
    for i in range(1, len(m_splits), 2):
        m_num = int(m_splits[i].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5'))
        mondais[m_num] = m_splits[i+1]
        
    choukai_ans = {}
    # Parse answers for each mondai
    for m_num, m_txt in mondais.items():
        # Look for numbers
        lines = [l.strip() for l in m_txt.split('\n') if l.strip()]
        # Extract pairs of (question_num_line, answer_line)
        # Or parse all numbers
        nums_lines = []
        for l in lines:
            nums = [int(x) for x in re.findall(r'\b\d+\b', l)]
            if nums:
                nums_lines.append(nums)
        # In JLPT answer keys: question line is followed by answer line
        # e.g.:
        # [1, 2, 3, 4, 5]
        # [4, 3, 2, 3, 3]
        m_ans = {}
        pending_q = []
        for nums in nums_lines:
            if pending_q:
                # these are answers
                for q, a in zip(pending_q, nums):
                    m_ans[q] = a
                pending_q = []
            else:
                # question numbers
                if nums[0] == 1 or (len(m_ans) > 0 and nums[0] == len(m_ans) + 1):
                    pending_q = nums
        choukai_ans[m_num] = m_ans
    return choukai_ans

for p in range(1, len(reader.pages)):
    text = reader.pages[p].extract_text()
    m_ym = re.search(r'(\d{1,2})[/.-](\d{4})|(\d{4})[/.-](\d{1,2})', text)
    year, month = None, None
    if m_ym:
        if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
            month, year = int(m_ym.group(1)), int(m_ym.group(2))
        else:
            year, month = int(m_ym.group(3)), int(m_ym.group(4))
    res = parse_choukai_page_answers(p)
    counts = {m: len(ans) for m, ans in res.items()}
    total = sum(counts.values())
    print(f"Page {p:2} ({year}_{month:02d}): Choukai total={total:2} | M1={counts.get(1,0)}, M2={counts.get(2,0)}, M3={counts.get(3,0)}, M4={counts.get(4,0)}, M5={counts.get(5,0)}")
