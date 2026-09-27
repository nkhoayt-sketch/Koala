import urllib.request, json, sys

sys.stdout.reconfigure(encoding='utf-8')

resp = urllib.request.urlopen('http://localhost:5500/data/n2_exams/2025_12.json')
d = json.loads(resp.read().decode('utf-8'))
print('Exam Title:', d['title'], 'Total questions:', len(d['questions']))
for num in [12, 31, 41, 48, 49, 50, 51, 61, 64, 71, 72, 73]:
    q = next(x for x in d['questions'] if x['number'] == num)
    print(f"Q{num}: q={repr(q['question'][:40])} opts={q['options']} ans={q['answer']}")
    if q.get('passage'):
        print(f"   Passage len={len(q['passage'])}")
