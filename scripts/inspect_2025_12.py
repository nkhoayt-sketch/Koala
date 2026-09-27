import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/n2_exams/2025_12.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("Title:", d.get('title'))
print("Total questions:", len(d['questions']))

# Check questions 35..52
for q in d['questions']:
    if 35 <= q['number'] <= 52:
        print(f"\n--- Q{q['number']} ({q['section']}) ---")
        print("Question:", repr(q['question']))
        print("Options:", repr(q['options']))
        print("Passage len:", len(q.get('passage', '')))

# Check Choukai questions 72..78
for q in d['questions']:
    if 72 <= q['number'] <= 78:
        print(f"\n--- Choukai Q{q['number']} ({q['section']}) ---")
        print("Question:", repr(q['question']))
        print("Options:", repr(q['options']))
        print("Script len:", len(q.get('script', '')))
