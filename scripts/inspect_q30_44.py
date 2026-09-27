import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/n2_exams/2025_12.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for q in d['questions']:
    if 30 <= q['number'] <= 44:
        print(f"\n--- Q{q['number']} ---")
        print("Q:", repr(q['question']))
        print("Opts:", repr(q['options']))
