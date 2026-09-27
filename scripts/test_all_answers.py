import sys
import os
import re
import json
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

ans_pdf = os.path.join('N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)

def parse_page_answers(p_idx):
    text = reader.pages[p_idx].extract_text()
    chokai_idx = text.find('聴解')
    if chokai_idx != -1:
        text = text[:chokai_idx]
    
    # Split into lines
    raw_lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # We will process line by line.
    # When we see numbers, determine if they are question numbers or answers.
    q_to_ans = {}
    pending_questions = []
    
    for l in raw_lines:
        if any(h in l for h in ['JLPT', '文字・語彙', '文法', '読解', 'ĐÁP ÁN']):
            continue
        
        # Remove "問題", "１", "7", etc. if it's a problem header
        l_clean = re.sub(r'問題\s*[0-9０-９一二三四五六七八九１-９]*', '', l).strip()
        if not l_clean:
            continue
        
        nums = [int(x) for x in re.findall(r'\b\d+\b', l_clean)]
        if not nums:
            continue
        
        # Are these question numbers?
        # A question line contains consecutive numbers or numbers > 4, OR if pending_questions is empty and nums starts with expected next question
        next_expected = len(q_to_ans) + len(pending_questions) + 1
        
        # If nums match [next_expected, next_expected+1, ...] or contain numbers > 4
        is_q_line = any(n > 4 for n in nums) or (nums[0] == next_expected and len(nums) > 1 and nums[1] == next_expected + 1) or (nums[0] == next_expected and len(pending_questions) == 0 and not all(1 <= x <= 4 for x in nums))
        
        # But wait! If all numbers are in 1..4, and len(nums) == len(pending_questions): it is definitely an ANSWER line!
        if pending_questions and len(nums) == len(pending_questions) and all(1 <= x <= 4 for x in nums):
            for q, a in zip(pending_questions, nums):
                q_to_ans[q] = a
            pending_questions = []
        elif is_q_line:
            # It's a question numbers line
            # Check if numbers are sequential
            pending_questions.extend(nums)
        elif pending_questions and all(1 <= x <= 4 for x in nums):
            # It's partial answers or full answers
            for a in nums:
                if pending_questions:
                    q = pending_questions.pop(0)
                    q_to_ans[q] = a
        elif not pending_questions and nums[0] == 1 and all(nums[j] == j+1 for j in range(len(nums))):
            pending_questions.extend(nums)
            
    return q_to_ans

# Let's test on all 31 pages!
all_exam_answers = {}
for p_idx in range(1, len(reader.pages)):
    text = reader.pages[p_idx].extract_text()
    m_ym = re.search(r'(\d{1,2})/(\d{4})|(\d{4})/(\d{1,2})', text)
    if m_ym:
        if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
            month, year = int(m_ym.group(1)), int(m_ym.group(2))
        else:
            year, month = int(m_ym.group(3)), int(m_ym.group(4))
    else:
        continue
    
    ans = parse_page_answers(p_idx)
    key = f"{year}_{month:02d}"
    all_exam_answers[key] = ans
    print(f"Exam {key}: {len(ans)} answers parsed (Q1..Q{max(ans.keys(), default=0)})")

print(f"\nTotal exams with answers: {len(all_exam_answers)}")
