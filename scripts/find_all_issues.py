import json
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = sorted(glob.glob('data/n2_exams/20*.json'))
print('Total N2 exams (YYYY_MM):', len(files))

all_issues = []
for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    qs = data.get('questions', [])
    for idx, q in enumerate(qs):
        opts = q.get('options', [])
        ans = q.get('answer')
        q_num = q.get('number', idx + 1)
        q_id = q.get('id', f'{fname}_{q_num}')
        q_text = q.get('question', '')
        section = q.get('section', '')
        group = q.get('sectionGroup', '')

        opts_len = len(opts) if isinstance(opts, list) else 0
        has_empty = any(opt is None or (isinstance(opt, str) and not opt.strip()) for opt in (opts if isinstance(opts, list) else []))
        
        if opts_len != 4 or has_empty:
            all_issues.append({
                'file': fname,
                'num': q_num,
                'id': q_id,
                'group': group,
                'section': section,
                'opts_len': opts_len,
                'has_empty': has_empty,
                'opts': opts,
                'q_text': q_text[:60]
            })

print(f'Total issues: {len(all_issues)}')
print('\n=== Non-listening issues (Vocab / Grammar / Star / Reading) ===')
non_listening = [iss for iss in all_issues if 'listening' not in iss['group'] and '聴解' not in iss['section']]
print(f'Count: {len(non_listening)}')
for iss in non_listening:
    print(f"[{iss['file']}] Q#{iss['num']} (Sec: {iss['section']}) -> opts_len={iss['opts_len']}, has_empty={iss['has_empty']}")
    print(f"   Q: {iss['q_text']}")
    print(f"   opts: {iss['opts']}")

print('\n=== Listening issues ===')
listening = [iss for iss in all_issues if 'listening' in iss['group'] or '聴解' in iss['section']]
print(f'Count: {len(listening)}')
listening_by_sec = {}
for iss in listening:
    s = iss['section']
    listening_by_sec[s] = listening_by_sec.get(s, 0) + 1
print('Listening issues breakdown by section:', listening_by_sec)
