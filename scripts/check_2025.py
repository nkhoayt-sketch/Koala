import json, sys

sys.stdout.reconfigure(encoding='utf-8')
with open('data/n2_exams/2025_07.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for q in d['questions']:
    print(f"q{q['number']}: {q['question']}")
    print(f"   opts: {q['options']}")
