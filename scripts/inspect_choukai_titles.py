import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/n2_exams/2025_12.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for q in d['questions']:
    if q.get('number', 0) >= 72:
        print(f"Q{q['number']}: sec='{q.get('section')}' qNum='{q.get('questionNumber')}' title='{q.get('title')}' opts={q.get('options')[:2]}")
