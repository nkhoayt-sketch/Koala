# -*- coding: utf-8 -*-
"""
Build full Bunpou N1 suite (20 chapters + review) into data/n1_bunpou and public/data/n1_bunpou.
"""
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIRS = [
    os.path.join(ROOT_DIR, 'data', 'n1_bunpou'),
    os.path.join(ROOT_DIR, 'public', 'data', 'n1_bunpou')
]

from data_bunpou_ch01_ch07 import CHAPTERS_01_07
from data_bunpou_ch08_ch13 import CHAPTERS_08_13
from data_bunpou_ch14_ch20 import CHAPTERS_14_20
from data_bunpou_review import REVIEW_DATA

all_chapters = {}
all_chapters.update(CHAPTERS_01_07)
all_chapters.update(CHAPTERS_08_13)
all_chapters.update(CHAPTERS_14_20)

index_list = []
total_questions = 0

for ch_num in range(1, 21):
    ch_id = f"ch{ch_num:02d}"
    data = all_chapters.get(ch_id)
    if not data:
        raise ValueError(f"Missing chapter data for {ch_id}")
    
    file_name = f"shinkanzen_b_{ch_id}.json"
    q_count = len(data["questions"])
    total_questions += q_count
    
    index_list.append({
        "id": ch_id,
        "file": file_name,
        "lesson": data["lesson"],
        "title": data["title"],
        "theme": data["theme"],
        "group": data["group"],
        "questionCount": q_count,
        "description": data["description"]
    })
    
    for tdir in TARGET_DIRS:
        os.makedirs(tdir, exist_ok=True)
        out_path = os.path.join(tdir, file_name)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# Save review data
review_file = "shinkanzen_b_review.json"
q_count_rev = len(REVIEW_DATA["questions"])
total_questions += q_count_rev

index_list.append({
    "id": "review",
    "file": review_file,
    "lesson": REVIEW_DATA["lesson"],
    "title": REVIEW_DATA["title"],
    "theme": REVIEW_DATA["theme"],
    "group": REVIEW_DATA["group"],
    "questionCount": q_count_rev,
    "description": REVIEW_DATA["description"]
})

for tdir in TARGET_DIRS:
    out_path = os.path.join(tdir, review_file)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(REVIEW_DATA, f, ensure_ascii=False, indent=2)

# Save index
index_payload = {
    "totalChapters": 20,
    "totalExercises": len(index_list),
    "totalQuestions": total_questions,
    "categories": [
        {"id": "all", "label": "Tất cả (20 Bài)", "group": None},
        {"id": "group1", "label": "Nhóm I: Sự việc (1~7)", "group": "group1"},
        {"id": "group2", "label": "Nhóm II: Chủ quan (8~16)", "group": "group2"},
        {"id": "group3", "label": "Nhóm III: Bày tỏ (17~20)", "group": "group3"},
        {"id": "review", "label": "Bài tổng hợp", "group": "review"}
    ],
    "chapters": index_list
}

for tdir in TARGET_DIRS:
    idx_path = os.path.join(tdir, "n1_bunpou_index.json")
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump(index_payload, f, ensure_ascii=False, indent=2)

print(f"Build complete! Successfully generated 20 chapters + 1 review set.")
print(f"Total questions: {total_questions}")
for item in index_list:
    print(f" - {item['file']}: {item['questionCount']} câu ({item['title']})")
