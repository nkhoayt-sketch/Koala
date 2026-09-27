import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/n2_exams/2025_12.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

vn_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'

for q in d['questions']:
    for idx, opt in enumerate(q.get('options', [])):
        if any(c in opt.lower() for c in vn_chars) or ('(' in opt and ')' in opt and q['sectionGroup'] == 'listening'):
            print(f"Q{q['number']} opt[{idx}]: {opt}")
