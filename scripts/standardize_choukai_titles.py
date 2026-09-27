# -*- coding: utf-8 -*-
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Choukai metadata mapping for questions 72 to 101
CHOUKAI_META = {
    72: {"mondai": "問題1", "sec_title": "聴解 - 問題1: 課題理解", "q_num": "1番", "title": "問題1 - 1番"},
    73: {"mondai": "問題1", "sec_title": "聴解 - 問題1: 課題理解", "q_num": "2番", "title": "問題1 - 2番"},
    74: {"mondai": "問題1", "sec_title": "聴解 - 問題1: 課題理解", "q_num": "3番", "title": "問題1 - 3番"},
    75: {"mondai": "問題1", "sec_title": "聴解 - 問題1: 課題理解", "q_num": "4番", "title": "問題1 - 4番"},
    76: {"mondai": "問題1", "sec_title": "聴解 - 問題1: 課題理解", "q_num": "5番", "title": "問題1 - 5番"},

    77: {"mondai": "問題2", "sec_title": "聴解 - 問題2: ポイント理解", "q_num": "1番", "title": "問題2 - 1番"},
    78: {"mondai": "問題2", "sec_title": "聴解 - 問題2: ポイント理解", "q_num": "2番", "title": "問題2 - 2番"},
    79: {"mondai": "問題2", "sec_title": "聴解 - 問題2: ポイント理解", "q_num": "3番", "title": "問題2 - 3番"},
    80: {"mondai": "問題2", "sec_title": "聴解 - 問題2: ポイント理解", "q_num": "4番", "title": "問題2 - 4番"},
    81: {"mondai": "問題2", "sec_title": "聴解 - 問題2: ポイント理解", "q_num": "5番", "title": "問題2 - 5番"},
    82: {"mondai": "問題2", "sec_title": "聴解 - 問題2: ポイント理解", "q_num": "6番", "title": "問題2 - 6番"},

    83: {"mondai": "問題3", "sec_title": "聴解 - 問題3: 概要理解", "q_num": "1番", "title": "問題3 - 1番"},
    84: {"mondai": "問題3", "sec_title": "聴解 - 問題3: 概要理解", "q_num": "2番", "title": "問題3 - 2番"},
    85: {"mondai": "問題3", "sec_title": "聴解 - 問題3: 概要理解", "q_num": "3番", "title": "問題3 - 3番"},
    86: {"mondai": "問題3", "sec_title": "聴解 - 問題3: 概要理解", "q_num": "4番", "title": "問題3 - 4番"},
    87: {"mondai": "問題3", "sec_title": "聴解 - 問題3: 概要理解", "q_num": "5番", "title": "問題3 - 5番"},

    88: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "1番", "title": "問題4 - 1番"},
    89: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "2番", "title": "問題4 - 2番"},
    90: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "3番", "title": "問題4 - 3番"},
    91: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "4番", "title": "問題4 - 4番"},
    92: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "5番", "title": "問題4 - 5番"},
    93: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "6番", "title": "問題4 - 6番"},
    94: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "7番", "title": "問題4 - 7番"},
    95: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "8番", "title": "問題4 - 8番"},
    96: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "9番", "title": "問題4 - 9番"},
    97: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "10番", "title": "問題4 - 10番"},
    98: {"mondai": "問題4", "sec_title": "聴解 - 問題4: 即時応答", "q_num": "11番", "title": "問題4 - 11番"},

    99: {"mondai": "問題5", "sec_title": "聴解 - 問題5: 統合理解", "q_num": "1番", "title": "問題5 - 1番"},
    100: {"mondai": "問題5", "sec_title": "聴解 - 問題5: 統合理解", "q_num": "2番 (質問1)", "title": "問題5 - 2番 (質問1)"},
    101: {"mondai": "問題5", "sec_title": "聴解 - 問題5: 統合理解", "q_num": "2番 (質問2)", "title": "問題5 - 2番 (質問2)"}
}

def clean_option_text(text):
    if not isinstance(text, str):
        return text
    # Strip leading numbers followed by dot/comma: e.g. "1. " or "1、"
    text = re.sub(r'^[1-4１-４][.、]\s*', '', text)
    # Strip Vietnamese in parentheses like "(Lau/dọn bàn ăn)"
    text = re.sub(r'\s*\([A-Za-zÀ-ỹ0-9\s/,\-–\.]+\)', '', text)
    return text.strip()

def process_file(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for q in data.get('questions', []):
        num = q.get('number')
        
        # Clean options for all questions
        if 'options' in q and isinstance(q['options'], list):
            q['options'] = [clean_option_text(opt) for opt in q['options']]
            
        # Choukai questions
        if num in CHOUKAI_META:
            meta = CHOUKAI_META[num]
            q['sectionGroup'] = 'listening'
            q['section'] = meta['sec_title']
            q['questionNumber'] = meta['q_num']
            q['title'] = meta['title']
            
            # Explicit pure Japanese options for Q73, Q100, Q101
            if num == 73:
                q['options'] = [
                    "テーブルを拭く",
                    "サラダの準備をする",
                    "お客さんを席に案内する",
                    "待っているお客さんにメニューを配る"
                ]
                q['explanation'] = (
                    "【正解】2 (サラダの準備をする)\n\n"
                    "• Ý nghĩa các phương án hình minh họa:\n"
                    "  1. テーブルを拭く (Lau/dọn bàn ăn)\n"
                    "  2. サラダの準備をする (Chuẩn bị rau/salad trong bếp)\n"
                    "  3. お客さんを席に案内する (Dẫn khách vào bàn)\n"
                    "  4. 待っているお客さんにメニューを配る (Phát menu cho khách chờ)\n\n"
                    "• Lời thoại bài nghe:\n"
                    "Quản lý dặn nhân viên nam: Bàn ghế đã lau sạch rồi, khách bên ngoài đang đợi nhưng trước khi mở cửa đón khách thì hãy vào bếp chuẩn bị sẵn món salad chia vào từng đĩa nhỏ trước. Do đó hành động cần làm đầu tiên là chuẩn bị salad."
                )
            elif num in [100, 101]:
                q['options'] = [
                    "1番の自転車",
                    "2番の自転車",
                    "3番の自転車",
                    "4番の自転車"
                ]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Standardized Choukai in: {file_path}")

targets = [
    os.path.join(ROOT_DIR, 'data', 'n2_exams', '2025_12.json'),
    os.path.join(ROOT_DIR, 'data', 'n2_exams', 'n2_2025_12.json'),
    os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams', '2025_12.json'),
    os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams', 'n2_2025_12.json'),
]

for t in targets:
    process_file(t)

print("All Choukai metadata standardized successfully!")
