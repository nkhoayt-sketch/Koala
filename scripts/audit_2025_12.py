import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/n2_exams/2025_12.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('Exam Title:', d.get('title'))
print('Total questions:', len(d['questions']))

for q in d['questions']:
    issues = []
    num = q.get('number')
    q_txt = q.get('question', '')
    opts = q.get('options', [])
    p_len = len(q.get('passage', ''))
    sec = q.get('section', '')
    sec_grp = q.get('sectionGroup', '')
    
    if not q_txt:
        issues.append('EMPTY_QUESTION')
    if len(opts) != 4 and sec_grp != 'choukai':
        issues.append(f'OPTS_LEN_{len(opts)}')
    if any(opt.startswith('Phương án') for opt in opts):
        issues.append('PLACEHOLDER_OPTION')
    if any(len(opt) > 120 for opt in opts) and sec_grp == 'vocab_grammar':
        issues.append('SUPER_LONG_OPTION')
    if num in [48, 49, 50, 51] and p_len == 0:
        issues.append('M9_NO_PASSAGE')
    if num in range(72, 83):
        if any(len(opt) <= 1 for opt in opts if not opt.isdigit()):
            issues.append('CHOUKAI_SHORT_OPTION')
            
    if issues:
        print(f"Q{num} ({sec}): {issues}")
        print(f"   Q: {repr(q_txt[:60])}")
        print(f"   Opts: {opts}")
