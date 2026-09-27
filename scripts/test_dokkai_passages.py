import sys, os, re, json

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/exam_2024_07_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find positions of all questions from 52 to 71
q_positions = {}
for q in range(52, 72):
    m = re.search(rf'(?:^|\n)\s*{q}\s+', text)
    if m:
        q_positions[q] = m.start()

print(f"Found positions for {len(q_positions)} questions (52..71)")

# Extract passage between headers/questions
def clean_passage(raw):
    # Remove page markers, instruction lines
    raw = re.sub(r'<<<PAGE_\d+>>>', '', raw)
    lines = raw.split('\n')
    cleaned = []
    for l in lines:
        s = l.strip()
        if any(h in s for h in ['問題 10', '問題 11', '問題 12', '問題 13', '問題 14', '読解', '次の文章を読んで', '次の(1)から', '次の（１）から', '次の A と B']):
            continue
        cleaned.append(l)
    p = '\n'.join(cleaned).strip()
    # clean furigana
    lines = p.split('\n')
    non_furigana = []
    for l in lines:
        s = l.strip()
        if s and re.fullmatch(r'[\u3040-\u309F\u30A0-\u30FF]{1,6}', s) and non_furigana:
            continue
        non_furigana.append(l)
    res = '\n'.join(non_furigana)
    res = re.sub(r'([\u4e00-\u9fff])\n([\u4e00-\u9fff])', r'\1\2', res)
    res = re.sub(r'([\u4e00-\u9fff])\n([\u3040-\u309F])', r'\1\2', res)
    return res.strip()

# Let's check passage for each Dokkai question
# For Q52: between "問題 10" and Q52
m10_idx = text.find('問題 10')
p52 = clean_passage(text[m10_idx:q_positions[52]])
print("\n--- Passage for Q52 ---")
print(p52[:150] + "...")

# For Q53: between Q52 options and Q53
p53 = clean_passage(text[q_positions[52]:q_positions[53]])
# remove Q52 question and options
opt4_52 = re.search(r'[４4]\s*.*', text[q_positions[52]:q_positions[53]])
if opt4_52:
    p53 = clean_passage(text[q_positions[52] + opt4_52.end():q_positions[53]])
print("\n--- Passage for Q53 ---")
print(p53[:150] + "...")

# For Q57 & Q58: between Q56 options and Q57
opt4_56 = re.search(r'[４4]\s*.*', text[q_positions[56]:q_positions[57]])
p57 = clean_passage(text[q_positions[56] + opt4_56.end():q_positions[57]]) if opt4_56 else ""
print("\n--- Passage for Q57/Q58 ---")
print(p57[:150] + "...")
