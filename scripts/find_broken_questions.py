import os, sys, glob, json

sys.stdout.reconfigure(encoding='utf-8')

pattern = os.path.join('data', 'n2_exams', '20*.json')
files = sorted(glob.glob(pattern))
print(f"Checking {len(files)} files...")

for f in files:
    fname = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fp:
        d = json.load(fp)
    for q in d.get('questions', []):
        opts = q.get('options', [])
        q_txt = q.get('question', '')
        
        # Check for 先着
        if '先着' in q_txt or any('先着' in opt for opt in opts):
            print(f"[{fname}] Q{q['number']} has 先着:")
            print("  Q:", repr(q_txt))
            print("  Opts:", repr(opts))

        # Check for empty question
        if not q_txt and q['sectionGroup'] == 'vocab_grammar':
            print(f"[{fname}] Q{q['number']} EMPTY QUESTION:")
            print("  Opts:", repr(opts))

        # Check for options with len > 100 in vocab_grammar
        long_opts = [opt for opt in opts if len(opt) > 100]
        if long_opts and q['sectionGroup'] == 'vocab_grammar':
            print(f"[{fname}] Q{q['number']} LONG OPTION (len={len(long_opts[0])})")
            print("  Preview:", repr(long_opts[0][:80]))
