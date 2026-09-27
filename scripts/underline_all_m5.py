import glob, json, os

M5_TARGET_MAP = [
    'ことなります', 'たまたま', 'あきらかな', 'そうぞうしく', '所有している',
    'おそらく', '収納していない', '小柄', '無口', 'やや', 'テンポ', '妙な',
    'ささやくように', 'かつて', '注目した', 'じかに', '衝突する', 'ひきょうな',
    '愉快な', 'やむをえない', '息抜き', 'ついていた', 'あやまり', '臆病',
    'とっくに', 'ゆずりました', '記憶している', '不平', 'むかつく', 'まれな',
    '当てて', 'あわれな', '当分', '一転した', 'じたばたしても', '利口な',
    'くどくて', '落ち込んだ', '精いっぱい', '同情した', '定める', 'ハードだ',
    '動揺した', '引き返した', '一層', 'かかりつけの', '真剣に', 'まれ',
    '終日', 'いじっていた', 'とりかかります', '人柄', '案の定', 'くるんで',
    '最寄りの', '指図される', '欠かせない', '依然', '衝突しそう', 'でたらめ',
    'さわがしい', 'テクニック', '書籍', 'とがっている', 'くだらない', '惜しい',
    '概要', '油断していた', '行儀', 'いばっている', '収納して', 'ガイドして',
    '修正した', '徐々に', 'はげている', 'しぐさ'
]

# Sort by length descending
M5_TARGET_MAP.sort(key=len, reverse=True)

dirs = ['public/data/n2_exams', 'data/n2_exams']

total_fixed = 0
for d in dirs:
    files = sorted(glob.glob(os.path.join(d, '[0-9]*.json')))
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        changed = False
        for q in data.get('questions', []):
            if q.get('sectionGroup') == 'vocab_grammar' and '問題5' in q.get('section', ''):
                qtext = q.get('question', '')
                if '<u>' not in qtext:
                    for kw in M5_TARGET_MAP:
                        if kw in qtext:
                            q['question'] = qtext.replace(kw, f'<u>{kw}</u>', 1)
                            changed = True
                            total_fixed += 1
                            break
        if changed:
            with open(f, 'w', encoding='utf-8') as fp:
                json.dump(data, fp, ensure_ascii=False, indent=2)

print(f"Total M5 questions underlined: {total_fixed}")
