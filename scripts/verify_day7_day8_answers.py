import json
import pypdf
import re

with open('data/n1_20days/day07.json', 'r', encoding='utf-8') as f:
    d7 = json.load(f)
with open('data/n1_20days/day08.json', 'r', encoding='utf-8') as f:
    d8 = json.load(f)

d7_ans = [q['answer'] + 1 for q in d7['questions']] # 1-indexed
d8_ans = [q['answer'] + 1 for q in d8['questions']]

print(f"Day 7 answers in JSON ({len(d7_ans)}):", d7_ans)
print(f"Day 8 answers in JSON ({len(d8_ans)}):", d8_ans)
