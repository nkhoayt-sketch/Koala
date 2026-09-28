import json

for d in ['day04.json', 'day06.json']:
    with open('data/n1_20days/' + d, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for q in data['questions']:
        if q['number'] == 21:
            print(f"=== {d} Q21 ===")
            print("Question:", q['question'])
            print("Options:", q['options'])
