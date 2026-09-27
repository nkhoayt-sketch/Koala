import glob, json, os

files = sorted(glob.glob('public/data/n2_exams/[0-9]*.json'))
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        d = json.load(fp)
    fname = os.path.basename(f)
    for q in d['questions']:
        if q.get('sectionGroup') == 'vocab_grammar' and '問題5' in q.get('section', ''):
            if '<u>' not in q.get('question', ''):
                print(f"{fname} | Q{q.get('number')} | {q.get('question')} | {q.get('options')}")
