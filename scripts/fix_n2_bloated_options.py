import json
import os
import glob
import re

def fix_bloated_n2():
    fixes = {
        ('2010_12', 55, 3): "木々がもともと持っているにおいを消す。",
        ('2011_12', 55, 3): "寒さに耐える強さが身につく。",
        ('2015_12', 65, 3): "価格を高くしても売れる点",
        ('2016_07', 62, 3): "物語としてあまり感動を与えられないこと",
        ('2017_07', 62, 2): "問題を解決する能力が身につけられる。",
        ('2017_07', 62, 3): "勉強の内容を理解するスピードが速くなる。",
        ('2018_12', 53, 3): "自分で選別した情報を他者の情報と比較検討すべきだ。",
    }
    
    for (exam_id, q_num, opt_idx), correct_text in fixes.items():
        for prefix in ['public/data/n2_exams/', 'data/n2_exams/']:
            for name in [f"{exam_id}.json", f"n2_{exam_id}.json"]:
                path = os.path.join(prefix, name)
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as fp:
                        data = json.load(fp)
                    for q in data.get('questions', []):
                        if q.get('number') == q_num:
                            while len(q['options']) <= opt_idx:
                                q['options'].append("")
                            q['options'][opt_idx] = correct_text
                    with open(path, 'w', encoding='utf-8') as fp:
                        json.dump(data, fp, ensure_ascii=False, indent=2)
                    print(f"Fixed {path} Q{q_num} opt {opt_idx+1}")

if __name__ == '__main__':
    fix_bloated_n2()
