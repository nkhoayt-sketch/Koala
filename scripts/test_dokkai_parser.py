import sys, os, re, json, pypdf

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/exam_2024_07_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's write an extractor for Dokkai
# Dokkai starts at "読解" or "問題 10" / "問題10"
# Ends before "聴解"

def clean_furigana(t):
    lines = t.split('\n')
    cleaned = []
    for l in lines:
        s = l.strip()
        # If line is only 1-5 hiragana/katakana or furigana artifact
        if s and re.fullmatch(r'[\u3040-\u309F\u30A0-\u30FF]{1,6}', s) and cleaned:
            continue
        cleaned.append(l)
    res = '\n'.join(cleaned)
    res = re.sub(r'([\u4e00-\u9fff])\n([\u4e00-\u9fff])', r'\1\2', res)
    res = re.sub(r'([\u4e00-\u9fff])\n([\u3040-\u309F])', r'\1\2', res)
    return res

# Find all questions in text:
# Each question is a number like: \n\s*(\d{2})\s+...
# followed by options 1, 2, 3, 4
q_matches = list(re.finditer(r'(?:^|\n)\s*(\d{2})\s+(.*?)(?=(?:\n\s*\d{2}\s+[^\d]|\n\s*問題|\n<<<PAGE_|\Z))', text, re.DOTALL))
print(f"Total question regex matches: {len(q_matches)}")
for m in q_matches:
    num = int(m.group(1))
    if 52 <= num <= 71:
        snippet = m.group(2)[:60].replace('\n', ' ')
        print(f"  Q{num:2}: {snippet}")
