import glob, json, os

files = sorted(glob.glob('public/data/n2_exams/20*.json'))
for f in files:
    with open(f, encoding='utf-8') as fp:
        d = json.load(fp)
    qs = d.get('questions', [])
    bad_opts = []
    for q in qs:
        for i, opt in enumerate(q.get('options', [])):
            if any(c in opt for c in 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'):
                bad_opts.append((q['number'], i, opt))
    if bad_opts:
        print(f"=== {os.path.basename(f)} ({len(bad_opts)} bad options) ===")
        for qnum, idx, opt in bad_opts[:5]:
            print(f"  Q{qnum} opt[{idx}]: {opt}")
