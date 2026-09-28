import json

for exam_id, q_num in [
    ('2010_12', 55),
    ('2011_12', 55),
    ('2015_12', 65),
    ('2016_07', 62),
    ('2017_07', 62),
    ('2018_12', 53),
]:
    with open(f'public/data/n2_exams/{exam_id}.json', 'r', encoding='utf-8') as f:
        exam = json.load(f)
    for q in exam['questions']:
        if q['number'] == q_num:
            print(f"=== {exam_id} Q{q_num} ===")
            for i, opt in enumerate(q['options']):
                print(f"  opt {i+1}: {opt}")
