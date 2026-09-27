import sys
import os
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/sample_exam_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Clean lines
lines = text.split('\n')
clean_lines = []
for line in lines:
    l_strip = line.strip()
    if re.match(r'^---\s*PAGE\s*\d+\s*---$', l_strip):
        continue
    if re.match(r'^JLPT[・\s]N2[・\s]\d+/\d+', l_strip):
        continue
    if re.match(r'^\d+$', l_strip):
        continue
    clean_lines.append(line)

content = "\n".join(clean_lines)

# Split by question numbers
# In N2, questions are numbered 1 to ~71 consecutively.
# Question starts with: (newline or space) number (space or tab)
# Let's match question blocks:
# e.g. " 1    バスの運賃を払う。"
# Options start with １, ２, ３, ４ or 1, 2, 3, 4

def parse_questions_from_section(sec_num, sec_text):
    # Extract instruction: usually first line
    lines = [l.strip() for l in sec_text.split('\n') if l.strip()]
    if not lines:
        return []
    
    inst = lines[0]
    rest = "\n".join(lines[1:])
    
    # Match questions: lines starting with number
    # regex pattern for question start: ^\s*(\d{1,2})\s+
    q_matches = list(re.finditer(r'(?:^|\n)\s*(\d{1,2})\s+(.*?)(?=(?:\n\s*\d{1,2}\s+[^\d]|\Z))', rest, re.DOTALL))
    
    parsed = []
    for m in q_matches:
        q_num = int(m.group(1))
        body = m.group(2).strip()
        
        # In body, separate question text from 4 options
        # Options usually marked by １, ２, ３, ４ (fullwidth) or 1, 2, 3, 4
        # Pattern: (１|1)\s*(.*?)(?:２|2)\s*(.*?)(?:３|3)\s*(.*?)(?:４|4)\s*(.*)
        # Or options on separate lines
        opt_pattern = r'(?:[１1])\s*(.*?)(?:[２2])\s*(.*?)(?:[３3])\s*(.*?)(?:[４4])\s*(.*)'
        opt_match = re.search(opt_pattern, body, re.DOTALL)
        
        if opt_match:
            q_text = body[:opt_match.start()].strip()
            o1 = opt_match.group(1).strip()
            o2 = opt_match.group(2).strip()
            o3 = opt_match.group(3).strip()
            o4 = opt_match.group(4).strip()
            
            # Clean up line breaks in options
            o1 = re.sub(r'\s+', ' ', o1)
            o2 = re.sub(r'\s+', ' ', o2)
            o3 = re.sub(r'\s+', ' ', o3)
            o4 = re.sub(r'\s+', ' ', o4)
            options = [o1, o2, o3, o4]
        else:
            q_text = body
            options = []
            
        parsed.append({
            'num': q_num,
            'question': q_text,
            'options': options
        })
    return parsed

# Test parsing on Sec 1 to Sec 8
sec_matches = list(re.finditer(r'(?:問題|間題|題題)\s*([0-9０-９一二三四五六七八九]+)(.*?)(?=(?:問題|間題|題題)\s*[0-9０-９一二三四五六七八九]+|\Z)', content, re.DOTALL))
all_q = []
for m in sec_matches:
    raw_num = m.group(1)
    tr = {'１':1, '２':2, '３':3, '４':4, '５':5, '６':6, '７':7, '８':8, '９':9,
          '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, '11':11, '12':12, '13':13, '14':14}
    sec_num = tr.get(raw_num, 0) or (int(raw_num) if raw_num.isdigit() else 0)
    if 1 <= sec_num <= 8:
        qs = parse_questions_from_section(sec_num, m.group(0))
        print(f"Sec {sec_num}: Parsed {len(qs)} questions (Q{qs[0]['num'] if qs else 0}..Q{qs[-1]['num'] if qs else 0})")
        for q in qs[:2]:
            print(f"   Q{q['num']}: {q['question'][:50]} -> Options: {q['options']}")
        all_q.extend(qs)

print(f"\nTotal extracted for Sec 1..8: {len(all_q)} questions")
