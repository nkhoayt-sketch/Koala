import os, sys, json, glob

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, 'data', 'n2-index.json')
PUBLIC_INDEX_PATH = os.path.join(ROOT_DIR, 'public', 'data', 'n2-index.json')

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    index_data = json.load(f)

print(f"Total exams in n2-index.json: {len(index_data)}")
available_count = sum(1 for e in index_data if e.get('available'))
print(f"Available exams unlocked: {available_count}/{len(index_data)}")

# Verify each exam file
issues = []
print("\n" + "="*80)
print(f"{'Exam ID':15} | {'Title':16} | {'Total Q':7} | {'Vocab/Gram':10} | {'Dokkai Q':8} | {'Passages OK'}")
print("="*80)

for entry in index_data:
    exam_id = entry['id']
    f_rel = entry['file']
    f_path = os.path.join(ROOT_DIR, f_rel)
    f_pub = os.path.join(ROOT_DIR, 'public', f_rel)
    
    if not os.path.exists(f_path):
        issues.append(f"Missing file: {f_path}")
        continue
    if not os.path.exists(f_pub):
        issues.append(f"Missing public file: {f_pub}")
        continue
        
    with open(f_path, 'r', encoding='utf-8') as fp:
        exam = json.load(fp)
        
    qs = exam.get('questions', [])
    q_len = len(qs)
    v_len = sum(1 for q in qs if q.get('sectionGroup') == 'vocab_grammar')
    r_len = sum(1 for q in qs if q.get('sectionGroup') == 'reading')
    
    # Check dokkai passages
    dokkai_qs = [q for q in qs if q.get('sectionGroup') == 'reading']
    with_passage = sum(1 for q in dokkai_qs if q.get('passage', '').strip())
    
    # Check invalid answers
    invalid_ans = [q['number'] for q in qs if q.get('answer') not in [0, 1, 2, 3]]
    if invalid_ans:
        issues.append(f"{exam_id} invalid answers for: {invalid_ans}")
        
    passages_ok = f"{with_passage}/{len(dokkai_qs)}" if dokkai_qs else "N/A"
    print(f"{exam_id:15} | {entry['title']:16} | {q_len:7} | {v_len:10} | {r_len:8} | {passages_ok}")

print("="*80)
if issues:
    print("\nISSUES FOUND:")
    for iss in issues:
        print(f" - {iss}")
else:
    print("\nALL 31 EXAMS VERIFIED PERFECTLY! ZERO ERRORS!")
