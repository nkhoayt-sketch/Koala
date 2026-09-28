import json
import os
import re
import glob

# Day configurations
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

print("Day configurations ready.")
