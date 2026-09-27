import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

kanji_re = r'[\u4e00-\u9faf]'
kana_re = r'[\u3040-\u309f]+'

pattern = re.compile(f'({kanji_re}+)\\s+({kana_re})')

for fpath in ['data/n2_exams/2023_12.json', 'data/n2_exams/2025_07.json']:
    print('==============================', fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for q in d['questions']:
        matches = pattern.findall(q['question'])
        for opt in q['options']:
            matches += pattern.findall(opt)
        if matches:
            print(f"q{q['number']}: {matches}")
