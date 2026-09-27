import glob
import json
import re

files = sorted(glob.glob('public/data/n2_exams/[0-9]*.json'))
print(f"Auditing all {len(files)} official exam files...")

header_leaks = []
empty_questions = []
invalid_options_len = []
choukai_missing_qn = []
m1_with_u, m1_total = 0, 0
m2_with_u, m2_total = 0, 0
m5_with_u, m5_total = 0, 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    questions = data.get('questions', [])
    for q in questions:
        sec = q.get('section', '')
        sgroup = q.get('sectionGroup', '')
        qtext = q.get('question', '')
        qid = q.get('id', '')
        opts = q.get('options', [])
        
        if sgroup == 'vocab_grammar':
            if '問題1' in sec:
                m1_total += 1
                if '<u>' in qtext: m1_with_u += 1
            elif '問題2' in sec:
                m2_total += 1
                if '<u>' in qtext: m2_with_u += 1
            elif '問題5' in sec:
                m5_total += 1
                if '<u>' in qtext: m5_with_u += 1
            
        if sgroup == 'listening':
            if not q.get('questionNumber'):
                choukai_missing_qn.append((f, qid))
        else:
            if not qtext:
                empty_questions.append((f, qid))
                
        if len(opts) not in (3, 4):
            invalid_options_len.append((f, qid, len(opts)))
            
        for opt in opts:
            if re.search(r'問題\s*[1-9]|最もよいもの|選びなさい|<<<PAGE', opt):
                header_leaks.append((f, qid, opt))

print("================ AUDIT SUMMARY ================")
print(f"Total exam files checked: {len(files)}")
print(f"Header leaks in options: {len(header_leaks)}")
print(f"Empty question text (vocab/grammar/reading): {len(empty_questions)}")
print(f"Invalid options length (!= 3 or 4): {len(invalid_options_len)}")
print(f"Choukai missing questionNumber: {len(choukai_missing_qn)}")
print(f"Mondai 1 underline coverage: {m1_with_u}/{m1_total} ({m1_with_u/max(1,m1_total)*100:.1f}%)")
print(f"Mondai 2 underline coverage: {m2_with_u}/{m2_total} ({m2_with_u/max(1,m2_total)*100:.1f}%)")
print(f"Mondai 5 underline coverage: {m5_with_u}/{m5_total} ({m5_with_u/max(1,m5_total)*100:.1f}%)")
print("===============================================")
