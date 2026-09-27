import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/n2_exams/2023_12.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total questions in 2023_12.json: {len(d.get('questions', []))}")
for q in d.get('questions', []):
    num = q.get('number')
    sec = q.get('section')
    sec_grp = q.get('sectionGroup')
    p_len = len(q.get('passage', ''))
    ans = q.get('answer')
    q_txt = q.get('question', '').replace('\n', ' ')[:50]
    print(f"Q{num:02d} | Sec: {sec} | Grp: {sec_grp} | PassLen: {p_len} | Ans: {ans} | {q_txt}")
