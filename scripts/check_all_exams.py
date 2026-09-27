import os, json, glob

files = sorted(glob.glob('data/n2_exams/20*.json'))
print(f"Total exam files: {len(files)}")
summary = []
for f in files:
    name = os.path.basename(f)
    try:
        with open(f, 'r', encoding='utf-8') as fp:
            d = json.load(fp)
            q_len = len(d.get('questions', []))
            sections = set(q.get('section', '') for q in d.get('questions', []))
            has_dokkai = any('読解' in s for s in sections)
            has_choukai = any('聴解' in s for s in sections)
            summary.append((name, q_len, has_dokkai, has_choukai, d.get('totalQuestions', 0)))
    except Exception as e:
        summary.append((name, f"Error: {e}", False, False, 0))

for name, q_len, dokkai, choukai, total in summary:
    print(f"{name:15} | Questions: {q_len:3} | TotalMeta: {total:3} | Dokkai: {str(dokkai):5} | Choukai: {str(choukai):5}")
