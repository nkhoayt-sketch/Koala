import json, sys

sys.stdout.reconfigure(encoding='utf-8')

for fpath in ['data/n2_exams/2025_07.json', 'data/n2_exams/2023_12.json']:
    print('==============================', fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for q in d['questions'][30:47]:
        print(f"[{q['number']}] {q['section']}: {q['question']}")
        print(f"   opts: {q['options']}")
