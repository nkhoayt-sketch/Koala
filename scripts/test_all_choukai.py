import pypdf
import re
import json

r = pypdf.PdfReader('N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')

def to_half(s):
    res = []
    for c in s:
        code = ord(c)
        if 0xff10 <= code <= 0xff19:
            res.append(chr(code - 0xfee0))
        elif c == '　':
            res.append(' ')
        else:
            res.append(c)
    return ''.join(res)

def parse_choukai_answers(c_raw):
    # Normalize
    text = re.sub(r'問題\s*[\r\n]+\s*', '問題', c_raw)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # 1. M1 & M2:
    # Find all digits in lines between '問題1' and '問題3'
    m1_m2_text = ''
    m3_m4_text = ''
    m4_m5_text = ''
    
    stage = 0
    for l in lines:
        if '問題1' in l:
            stage = 1
        elif '問題3' in l:
            stage = 3
        elif '問題5' in l:
            stage = 5
            
        if stage == 1:
            m1_m2_text += ' ' + l
        elif stage == 3:
            m3_m4_text += ' ' + l
        elif stage == 5:
            m4_m5_text += ' ' + l
            
    # In M1 & M2:
    # Extract answers. Question numbers are 1..5, 1..6 (or 1..5).
    # If answers are at end of line or next line:
    # Let's find answer digits:
    # Look at M1: always 5 questions.
    # Look at M2: 6 questions (5 in 2018_12).
    # Let's search for the sequence of answers:
    # In m1_m2_text:
    # It has '1 2 3 4 5' (Qs for M1)
    # and '1 2 3 4 5 6' (Qs for M2)
    # The remaining numbers are the answers!
    tokens = m1_m2_text.split()
    # Remove '問題1', '問題2'
    nums = [int(t) for t in tokens if t.isdigit()]
    # nums begins with 1, 2, 3, 4, 5 (M1 Qs), then 1, 2, 3, 4, 5, 6 (or 5) (M2 Qs)
    # Then the answers!
    # Let's find where the question numbers end:
    q_len = 5 + (5 if '1 2 3 4 5  問題2\n1 2 3 4 5' in text or '2018_12' in text else 6)
    # But wait, nums[0..4] == 1..5. nums[5..10] == 1..6.
    m2_q_len = 6
    if nums[5:10] == [1, 2, 3, 4, 5] and (len(nums) <= 10 or nums[10] != 6):
        m2_q_len = 5
    elif nums[5:11] == [1, 2, 3, 4, 5, 6]:
        m2_q_len = 6
        
    ans_m1_m2 = nums[5 + m2_q_len:]
    ans_m1 = ans_m1_m2[:5]
    ans_m2 = ans_m1_m2[5:]

    # In M3 & M4 (part 1):
    # M3 Qs: 1..5 (or 1..4 in 2012_12)
    # M4 Qs: 1..6
    tokens3 = m3_m4_text.split()
    nums3 = [int(t) for t in tokens3 if t.isdigit()]
    m3_q_len = 5
    if nums3[:4] == [1, 2, 3, 4] and (len(nums3) <= 4 or nums3[4] != 5):
        m3_q_len = 4
    ans_m3_m4_part1 = nums3[m3_q_len + 6:] # skip M3 Qs and M4 Qs 1..6
    ans_m3 = ans_m3_m4_part1[:m3_q_len]
    ans_m4_p1 = ans_m3_m4_part1[m3_q_len:]

    # In M4 (part 2) & M5:
    # It has M4 Qs 7..11 or 7..12
    # M5 Qs: 1 2 3 or 1 2
    # Then answers for M4 p2, and answers for M5!
    tokens5 = m4_m5_text.split()
    # Wait, 7 8 9 10 11 (12) might be in m3_m4_text or m4_m5_text
    # Let's inspect where 7 8 9 10 is:
    all_text = m3_m4_text + ' ' + m4_m5_text
    # Let's find 7 8 9 10 11 (12):
    m_p2_q = re.search(r'7\s+8\s+9\s+10\s+11(?:\s+12)?', all_text)
    m4_p2_q_count = 6 if '12' in m_p2_q.group(0) else 5
    
    # After M5 Qs (1 2 3 or 1 2):
    # In m4_m5_text, we have answers for M4 p2 (m4_p2_q_count digits) and answers for M5 (3 or 4 digits)
    nums5 = [int(t) for t in tokens5 if t.isdigit()]
    # Remove M5 Q numbers: if '1 2 3', remove 1, 2, 3; if '1 2', remove 1, 2
    # But wait, 7..11 or 7..12 might be before '問題5':
    # Let's check:
    m5_lines = [l.strip() for l in m4_m5_text.split('\n') if l.strip()]
    # Line 1 usually has: '1 2 3   3 2 2 3 1 3' or '1 2   1 3 2 1 1'
    # The digits at end of Line 1 are M4 p2 answers!
    # And the next line has M5 answers!
    digits_last_lines = []
    for l in m5_lines:
        dgts = [int(t) for t in l.split() if t.isdigit()]
        if dgts:
            digits_last_lines.append(dgts)
            
    # Usually: digits_last_lines[0] has M5 Qs + M4 p2 answers!
    # digits_last_lines[1] has M5 answers!
    m5_q_line = digits_last_lines[0]
    # If m5_q_line starts with [1, 2, 3]:
    if m5_q_line[:3] == [1, 2, 3]:
        ans_m4_p2 = m5_q_line[3:]
    elif m5_q_line[:2] == [1, 2]:
        ans_m4_p2 = m5_q_line[2:]
    else:
        ans_m4_p2 = m5_q_line
        
    ans_m4 = ans_m4_p1 + ans_m4_p2
    ans_m5 = digits_last_lines[1]
    
    return ans_m1, ans_m2, ans_m3, ans_m4, ans_m5

# Test across all 31 exams
for p in range(1, len(r.pages)):
    t = to_half(r.pages[p].extract_text())
    hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', t)
    if not hm: hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', t)
    y, m = hm.group(2) if int(hm.group(1)) <= 12 else hm.group(1), hm.group(1) if int(hm.group(1)) <= 12 else hm.group(2)
    c_raw = t.split('聴解')[1] if '聴解' in t else ''
    m1, m2, m3, m4, m5 = parse_choukai_answers(c_raw)
    total_c = len(m1) + len(m2) + len(m3) + len(m4) + len(m5)
    print(f"[{y}_{int(m):02d}] Choukai: M1({len(m1)}) M2({len(m2)}) M3({len(m3)}) M4({len(m4)}) M5({len(m5)}) = {total_c} answers")
