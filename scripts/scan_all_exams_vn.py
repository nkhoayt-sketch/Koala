import glob, json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

vn_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'

files = sorted(glob.glob('data/n2_exams/20*.json'))
print(f"Scanning {len(files)} exam files for Vietnamese in options...")

found_any = False
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        d = json.load(fp)
    for q in d.get('questions', []):
        for idx, opt in enumerate(q.get('options', [])):
            if any(c in opt.lower() for c in vn_chars):
                print(f"[{os.path.basename(f)}] Q{q['number']} opt[{idx}]: {opt}")
                found_any = True

if not found_any:
    print("ALL EXAM FILES ARE 100% FREE OF VIETNAMESE IN OPTIONS!")
