import glob, json, os

M_TARGETS = {
    ('2010_07.json', 1): '相互',
    ('2011_07.json', 1): '敗れて',
    ('2015_12.json', 10): 'あざやか',
    ('2017_07.json', 6): 'こおった',
    ('2017_12.json', 1): '乱れて',
    ('2019_07.json', 1): '憎んで',
    ('2020_12.json', 6): 'あざやか',
    ('2021_07.json', 5): '破片',
    ('2024_07.json', 5): '鮮やか',
}

dirs = ['public/data/n2_exams', 'data/n2_exams']

for d in dirs:
    for (fname, qnum), kw in M_TARGETS.items():
        fpath = os.path.join(d, fname)
        if not os.path.exists(fpath): continue
        with open(fpath, 'r', encoding='utf-8') as fp: data = json.load(fp)
        for q in data.get('questions', []):
            if q.get('number') == qnum:
                q['question'] = q['question'].replace(kw, f'<u>{kw}</u>', 1)
                break
        with open(fpath, 'w', encoding='utf-8') as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)

print("100% underline achieved!")
