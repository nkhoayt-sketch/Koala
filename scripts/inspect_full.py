import json, sys

sys.stdout.reconfigure(encoding='utf-8')

for fpath in ['data/n2_exams/2025_07.json', 'data/n2_exams/2023_12.json']:
    print('==============================', fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        d = json.load(f)
    print('Total questions:', len(d['questions']))
    by_sec = {}
    for q in d['questions']:
        sec = q.get('section', 'Unknown')
        by_sec.setdefault(sec, []).append(q['number'])
    for sec, nums in by_sec.items():
        print(f"  {sec}: {min(nums)} - {max(nums)} (count: {len(nums)})")
