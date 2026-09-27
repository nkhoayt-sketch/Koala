import glob, json, os

files = sorted(glob.glob('public/data/n2_exams/[0-9]*.json'))
targets = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        d = json.load(fp)
    fname = os.path.basename(f)
    for q in d.get('questions', []):
        if not q.get('question') and q.get('sectionGroup') != 'listening':
            targets.append((fname, q.get('number'), q.get('id'), q.get('options')))

print(f"Total targets: {len(targets)}")
for t in targets:
    print(f"{t[0]} | Q{t[1]} | {t[2]} | {t[3]}")
