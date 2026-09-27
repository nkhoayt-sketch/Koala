import glob, json, os

files = sorted(glob.glob('public/data/n2_exams/[0-9]*.json'))
all_m5_unlined = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        d = json.load(fp)
    fname = os.path.basename(f)
    for q in d['questions']:
        if q.get('sectionGroup') == 'vocab_grammar' and '問題5' in q.get('section', ''):
            if '<u>' not in q.get('question', ''):
                all_m5_unlined.append((fname, q.get('number'), q.get('question'), q.get('options')))

print(f"Remaining M5 (40 to {len(all_m5_unlined)}):")
for item in all_m5_unlined[40:]:
    print(f"('{item[0]}', {item[1]}): '{item[2]}', # {item[3]}")
