import json
import os

dirs = ['public/data/n2_exams', 'data/n2_exams']

for d in dirs:
    # 1. 2010_12
    p_2010_12 = os.path.join(d, '2010_12.json')
    if os.path.exists(p_2010_12):
        with open(p_2010_12, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for q in data.get('questions', []):
            if q.get('number') == 11 or q.get('id') == 'n2-201012-q11':
                q['question'] = '昨日の試合は、私たちのチームが２（   ）１で勝った。'
                q['options'] = ['反', '比', '差', '対']
                q['answer'] = 3
            elif q.get('number') == 12 or q.get('id') == 'n2-201012-q12':
                q['question'] = '１年前のテレビドラマが、来週から（   ）放送される。'
                q['options'] = ['改', '再', '更', '復']
                q['answer'] = 1
        with open(p_2010_12, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Fixed 2010_12 in {d}")

    # 2. 2012_12
    p_2012_12 = os.path.join(d, '2012_12.json')
    if os.path.exists(p_2012_12):
        with open(p_2012_12, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for q in data.get('questions', []):
            if q.get('number') == 61 or q.get('id') == 'n2-201212-q61':
                q['options'] = [
                    '必要な情報を先に伝えて、自分の考えを述べること。',
                    '参加者が不満をもたないよう、十分情報を伝えること。',
                    '多くのアイディアを提案して、参加者の意見を求めること。',
                    '他の出席者が積極的に参加できるよう、発言を避けること。'
                ]
                q['answer'] = 0
        with open(p_2012_12, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Fixed 2012_12 in {d}")

    # 3. 2018_07
    p_2018_07 = os.path.join(d, '2018_07.json')
    if os.path.exists(p_2018_07):
        with open(p_2018_07, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for q in data.get('questions', []):
            if q.get('number') == 13 or q.get('id') == 'n2-201807-q13':
                q['question'] = 'この高校は進学（   ）が非常に高く、ほとんどの生徒が大学に進む。'
                q['options'] = ['量', '値', '率', '割']
                q['answer'] = 2
        with open(p_2018_07, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Fixed 2018_07 in {d}")

    # 4. 2018_12
    p_2018_12 = os.path.join(d, '2018_12.json')
    if os.path.exists(p_2018_12):
        with open(p_2018_12, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for q in data.get('questions', []):
            if q.get('number') == 102 or q.get('id') == 'n2-201812-q102':
                q['question'] = '女の生徒はどの先輩の話を聞きに行きますか。'
                q['options'] = ['1', '2', '3', '4']
                q['answer'] = 3
        with open(p_2018_12, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Fixed 2018_12 in {d}")
