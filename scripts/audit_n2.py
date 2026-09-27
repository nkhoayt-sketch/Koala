import json, sys

sys.stdout.reconfigure(encoding='utf-8')

for year_file in ['data/n2_exams/2025_07.json', 'data/n2_exams/2023_12.json']:
    print(f"\n=================== {year_file} ===================")
    with open(year_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for q in data.get('questions', []):
        num = q.get('number')
        opts = q.get('options', [])
        question = q.get('question', '')
        
        has_garbage = 'N2 ' in question or any(f' {i} ' in question for i in [1, 2, 3, 4])
        long_opts = [o for o in opts if len(o) > 40]
        is_mondai9 = '問題9' in q.get('section', '') or num in [48, 49, 50, 51]
        
        if has_garbage or len(opts) != 4 or long_opts or is_mondai9:
            print(f"\n[Câu {num}] section={q.get('section')}")
            print(f"  Q: {question}")
            for i, opt in enumerate(opts):
                print(f"    ({i+1}) {opt[:80]}")
