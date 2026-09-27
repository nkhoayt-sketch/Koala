import glob, json

for f in sorted(glob.glob('public/data/n2_exams/20*.json'))[4:9]:
    d = json.load(open(f, encoding='utf-8'))
    m5 = [q for q in d['questions'] if '問題5' in q.get('section', '')]
    print(f)
    for q in m5:
        ans_idx = q.get('answer', 0)
        opts = q.get('options', [])
        ans_opt = opts[ans_idx] if ans_idx < len(opts) else ''
        print(f"  Q{q['number']}: {q['question']} -> Ans: {ans_opt}")
