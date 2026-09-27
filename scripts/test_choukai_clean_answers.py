import sys, os, re, json, pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ans_pdf = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)

def parse_choukai_clean_answers(p_idx):
    txt = reader.pages[p_idx].extract_text()
    chokai_idx = txt.find('聴解')
    if chokai_idx == -1: return []
    c_txt = txt[chokai_idx:]
    
    lines = [l.strip() for l in c_txt.split('\n') if l.strip()]
    cleaned = []
    for l in lines:
        if '聴解' in l or 'ĐÁP ÁN' in l or re.match(r'^\d{1,2}$', l):
            continue
        cleaned.append(l)
        
    # We want to collect only the answer digits!
    # Notice: In Choukai, question headers are:
    # 1 2 3 4 5  問題  1 2 3 4 5 6  (or separate)
    # The answer lines contain numbers all in 1..4 (or 1..3 for M4).
    # Let's extract all numbers from cleaned lines:
    all_ans = []
    
    # We know the structure:
    # M1: 5 answers
    # M2: 6 answers (or 5)
    # M3: 5 answers
    # M4: 11 or 12 answers
    # M5: 3 answers (or 4)
    # Let's look at the answer lines in the dumped text:
    # For page 30 (7/2025):
    # Line 2: answers for M1 & M2: [2, 3, 3, 3, 2, 4, 1, 3, 1, 2, 4] -> exactly 5 + 6 = 11 answers!
    # Line 7: answers for M3: [4, 3, 1, 1, 4] and first 6 of M4: [2, 3, 1, 1, 2, 2]!
    # Line 10: remaining 5 of M4: [3, 1, 2, 3, 2]!
    # Line 11: answers for M5: [3, 1, 2]!
    # Sum: 11 + 5 + 6 + 5 + 3 = 30 answers!
    # Look at how the answer values are formatted:
    # Any line with only digits <= 4 (or ending with digits <= 4) is answers!
    
    # Let's write an extractor:
    # Tokenize words, find sequences of digits <= 4 that follow question lines
    ans_tokens = []
    for l in cleaned:
        # If line contains '問題', remove '問題' and kanji/digits directly after it
        l_no_m = re.sub(r'問題\s*[1-5１-５一二三四五]?', ' ', l)
        nums = [int(x) for x in re.findall(r'\b\d+\b', l_no_m)]
        if not nums: continue
        # If it's a question numbering line like [1, 2, 3, 4, 5] or [1, 2, 3, 4, 5, 6] or [7, 8, 9, 10, 11]
        is_q_header = (nums == list(range(nums[0], nums[0] + len(nums)))) and (nums[0] == 1 or nums[0] == 7 or nums[0] == 6)
        if not is_q_header:
            # Check if all numbers <= 4
            if all(1 <= x <= 4 for x in nums):
                ans_tokens.extend(nums)
            else:
                # Could be a line like '1 2 3   3 2 1 2 2 3'
                # Here [1, 2, 3] is question numbers for M5, and [3, 2, 1, 2, 2, 3] is remaining answers for M4!
                # Split at numbers > 4 or question prefix
                m_lead = re.match(r'^([1-3\s]+)(.*)', l_no_m)
                if m_lead:
                    tail_nums = [int(x) for x in re.findall(r'\b\d+\b', m_lead.group(2))]
                    if tail_nums and all(1 <= x <= 4 for x in tail_nums):
                        ans_tokens.extend(tail_nums)
                        
    return ans_tokens

for p in range(1, len(reader.pages)):
    txt = reader.pages[p].extract_text()
    m_ym = re.search(r'(\d{1,2})[/.-](\d{4})|(\d{4})[/.-](\d{1,2})', txt)
    ans = parse_choukai_clean_answers(p)
    print(f"Page {p:2} ({m_ym.group(0) if m_ym else ''}): {len(ans)} answers: {ans[:10]}...{ans[-5:]}")
