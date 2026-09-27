import json

d = json.load(open('public/data/n2_exams/2025_12.json', encoding='utf-8'))
for q in d['questions'][:15]:
    print(f"Q{q['number']}: q={q['question']} opts={q['options']}")
