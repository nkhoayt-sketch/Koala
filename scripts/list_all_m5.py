import glob, json

files = sorted(glob.glob('public/data/n2_exams/20*.json'))
all_m5 = []

for f in files:
    d = json.load(open(f, encoding='utf-8'))
    for q in d['questions']:
        sec = q.get('section', '')
        if '問題5' in sec and q.get('sectionGroup') == 'vocab_grammar':
            all_m5.append({
                'exam': f.split('/')[-1].split('\\')[-1],
                'number': q['number'],
                'question': q['question'],
                'options': q['options'],
                'answer': q['answer']
            })

print(f"Total Mondai 5 questions found: {len(all_m5)}")
for item in all_m5[:15]:
    correct_opt = item['options'][item['answer']] if item['answer'] < len(item['options']) else ''
    print(f"{item['exam']} Q{item['number']}: {item['question']} -> Ans: {correct_opt}")
