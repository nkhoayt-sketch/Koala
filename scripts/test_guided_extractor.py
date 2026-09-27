import sys
import os
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/sample_exam_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Clean page headers
lines = text.split('\n')
clean_lines = []
for line in lines:
    l_strip = line.strip()
    if re.match(r'^---\s*PAGE\s*\d+\s*---$', l_strip):
        continue
    if re.match(r'^JLPT[・\s]N2[・\s]\d+/\d+', l_strip):
        continue
    if re.match(r'^\d{1,2}$', l_strip):
        continue
    clean_lines.append(line)

content = "\n".join(clean_lines)

# Split sections: 問題 1 to 問題 9
sec_names = {
    1: "問題1: 漢字読み",
    2: "問題2: 表記",
    3: "問題3: 語形成",
    4: "問題4: 文脈規定",
    5: "問題5: 言い換え類義",
    6: "問題6: 用法",
    7: "問題7: 文法形式の判断",
    8: "問題8: 文の組み立て ★",
    9: "問題9: 文章の文法",
    10: "問題10: 短文読解"
}

def extract_questions_guided(full_text, expected_answers):
    # expected_answers is dict: { q_num: answer_choice_1_to_4 }
    questions = []
    
    # We want to extract each question from q_num 1 to 51 (or max vocab_grammar q)
    # Strategy: Find position of each question number `N`
    # Question N begins with ASCII digit N surrounded by word boundary or space, followed by question text
    # then options １, ２, ３, ４
    
    q_nums = sorted([q for q in expected_answers.keys() if q <= 56])
    
    for i, q in enumerate(q_nums):
        next_q = q_nums[i+1] if i+1 < len(q_nums) else None
        
        # Determine section for q
        if q <= 5: sec_num = 1
        elif q <= 10: sec_num = 2
        elif q <= 13: sec_num = 3 # or 15
        elif q <= 20: sec_num = 4
        elif q <= 25: sec_num = 5
        elif q <= 30: sec_num = 6
        elif q <= 42: sec_num = 7
        elif q <= 47: sec_num = 8
        elif q <= 51: sec_num = 9
        else: sec_num = 10
        
        # Regex to find question q block
        # It starts with: `\n\s*q\s+` or `(?:\b|\s)q\s+`
        # and ends before `\n\s*next_q\s+` or `問題` header
        pattern = rf'(?:^|\n)\s*{q}\s+(.*?)(?=(?:\n\s*{next_q}\s+[^\d]|\n\s*(?:問題|間題|題題)|\Z))' if next_q else rf'(?:^|\n)\s*{q}\s+(.*?)(?=(?:\n\s*(?:問題|間題|題題)|\Z))'
        
        m = re.search(pattern, full_text, re.DOTALL)
        if not m:
            # Fallback search
            pattern_fallback = rf'\b{q}\s+(.*?)(?=(?:\b{next_q}\s+|\Z))' if next_q else rf'\b{q}\s+(.*)'
            m = re.search(pattern_fallback, full_text, re.DOTALL)
            
        if m:
            block = m.group(1).strip()
            # Extract 4 options
            opt_m = re.search(r'[１1]\s*(.*?)[２2]\s*(.*?)[３3]\s*(.*?)[４4]\s*(.*)', block, re.DOTALL)
            if opt_m:
                q_text = block[:opt_m.start()].strip()
                opts = [
                    re.sub(r'\s+', ' ', opt_m.group(1).strip()),
                    re.sub(r'\s+', ' ', opt_m.group(2).strip()),
                    re.sub(r'\s+', ' ', opt_m.group(3).strip()),
                    re.sub(r'\s+', ' ', opt_m.group(4).strip())
                ]
            else:
                q_text = block
                opts = []
                
            ans_val = expected_answers.get(q, 1) # 1..4
            ans_idx = ans_val - 1 # 0..3
            
            questions.append({
                'id': f"n2-q{q:02d}",
                'number': q,
                'sectionGroup': 'vocab_grammar' if sec_num <= 9 else 'reading',
                'section': sec_names.get(sec_num, f"問題 {sec_num}"),
                'question': q_text,
                'options': opts,
                'answer': ans_idx,
                'explanation': f"【正解】{ans_val} ({opts[ans_idx] if len(opts) > ans_idx else ''})\n\n• Phân tích kiến thức trọng tâm câu {q}."
            })
            
    return questions

# Test with 2023_07 expected answers
with open('scripts/test_all_answers.py', 'r', encoding='utf-8') as f:
    pass

import pypdf
ans_pdf = os.path.join('N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)
from test_all_answers import parse_page_answers
ans_2307 = parse_page_answers(26) # page 27 is 2023_07 (0-indexed 26)

qs = extract_questions_guided(content, ans_2307)
print(f"Extracted {len(qs)} questions for 2023_07!")
for q in qs[:5]:
    print(f"Q{q['number']}: {q['question']} | Ans: {q['answer']+1} ({q['options'][q['answer']] if q['options'] else 'N/A'})")
print("...")
for q in qs[42:47]:
    print(f"Q{q['number']}: {q['question']} | Ans: {q['answer']+1} ({q['options'][q['answer']] if q['options'] else 'N/A'})")
