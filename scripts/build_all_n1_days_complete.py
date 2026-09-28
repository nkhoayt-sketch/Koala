import json
import os
import re
import pypdf
import glob
from scripts.validate_and_build_pipeline import validate_n1_day, validate_n2_exam

LOG_FILE = "process.log"

def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# Master answer extractor from 20NgayN1.pdf
r = pypdf.PdfReader('20NgayN1.pdf')

def get_official_answers(day_num):
    p_num = 150 + ((day_num - 1) // 2) + 1
    is_second_day = (day_num % 2 == 0)
    txt = r.pages[p_num - 1].extract_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    ans_list = []
    for l in lines:
        if any(h in l for h in ['第', 'p.', '解答']):
            continue
        m = re.search(r'[□回国匝巨匡匿睡睦腱贖鵬醒厘匹國囲図日]\s*([1-4]|\]|‐\s*1)', l)
        if m:
            val = m.group(1)
            ans = 1 if (val == ']' or '1' in val) else int(val)
            ans_list.append(ans)
        elif re.match(r'^[1-4]$', l):
            ans_list.append(int(l))
    if is_second_day:
        sub = ans_list[45:90] if len(ans_list) >= 90 else ans_list[-45:]
    else:
        sub = ans_list[:45]
    while len(sub) < 45:
        sub.append(1)
    return [x - 1 for x in sub[:45]] # 0-indexed

DAY_METAS = {
    9: {
        'title': '第9日：九死一生',
        'proverb': '九死一生（きゅうしいっしょう）: narrow escape from death',
        'theme': '文法形式 (条件・契機・時)',
    },
    10: {
        'title': '第10日：十全十美',
        'proverb': '十全十美（じゅうぜんじゅうび）: perfect in every way',
        'theme': '文法形式 (立場・評価・強調)',
    },
    11: {
        'title': '第11日：百発百中',
        'proverb': '百発百中（ひゃっぱつひゃくちゅう）: 100% accuracy',
        'theme': '文の組み立て特訓 1 (並べ替え)',
    },
    12: {
        'title': '第12日：千差万別',
        'proverb': '千差万別（せんさばんべつ）: infinite variety',
        'theme': '文の組み立て特訓 2 (並べ替え)',
    },
    13: {
        'title': '第13日：万全之策',
        'proverb': '万全之策（ばんぜんのさく）: foolproof plan',
        'theme': '文章の文法 (文脈展開・接続)',
    },
    14: {
        'title': '第14日：温故知新',
        'proverb': '温故知新（おんこちしん）: learning from the past',
        'theme': '第2週 総復習テスト',
    },
    15: {
        'title': '第15日：一刀両断',
        'proverb': '一刀両断（いっとうりょうだん）: decisive action',
        'theme': '難関漢字・擬声語・擬態語',
    },
    16: {
        'title': '第16日：日進月歩',
        'proverb': '日進月歩（にっしんげっぽ）: rapid progress',
        'theme': '慣用句・ことわざ・複合動詞',
    },
    17: {
        'title': '第17日：起死回生',
        'proverb': '起死回生（きしかいせい）: miraculous recovery',
        'theme': '最高難度文法 (硬い文語表現)',
    },
    18: {
        'title': '第18日：臨機応変',
        'proverb': '臨機応変（りんきおうへん）: adapting to circumstances',
        'theme': '実戦模試 1 (文字・語彙)',
    },
    19: {
        'title': '第19日：明鏡止水',
        'proverb': '明鏡止水（めいきょうしすい）: serene and clear mind',
        'theme': '実戦模試 2 (文法・文脈)',
    },
    20: {
        'title': '第20日：完全無欠',
        'proverb': '完全無欠（かんぜんむけつ）: absolute perfection',
        'theme': '最終総仕上げ 模擬試験',
    }
}

INSTRUCTIONS = {
    'm1': '_____の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。',
    'm2': '（ ）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。',
    'm3': '_____の言葉に意味が最も近いものを、1・2・3・4から一つ選びなさい。',
    'm4': '次の言葉の使い方として最もよいものを、1・2・3・4から一つ選びなさい。',
    'm5': '次の文の（ ）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。',
    'm6': '次の文の ★ に入る最もよいものを、1・2・3・4から一つ選びなさい。',
    'm7': '次の文章を読んで、文章全体の趣旨を踏まえて、41から45の中に入る最もよいものを、1・2・3・4から一つ選びなさい。'
}

def save_and_validate_day(day_data, day_num):
    ok, errors = validate_n1_day(day_data)
    if not ok:
        log(f"[ERROR] Day {day_num} failed validation: {errors[:3]}")
        raise ValueError(f"Day {day_num} validation failed: {errors}")
        
    day_str = f"day{day_num:02d}.json"
    paths = [
        f"data/n1_20days/{day_str}",
        f"public/data/n1_20days/{day_str}",
        f"data/{day_str}",
        f"public/data/{day_str}"
    ]
    for p in paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(day_data, f, ensure_ascii=False, indent=2)
            
    log(f"[SUCCESS] Day {day_num:02d} ({day_data['title']}) validated and saved to 4 locations (45 Qs).")

print("Base runner setup ready.")
