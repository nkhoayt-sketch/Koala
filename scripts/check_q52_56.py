import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/n2_exams/2023_12.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for q in d['questions']:
    if q['number'] >= 52:
        num = q['number']
        ans = q['answer']
        question = q['question'][:40]
        print(f"Q{num}: answer index = {ans} (option {ans + 1}) | {question}")
