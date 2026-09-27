import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'n2_exams')
PUBLIC_DATA_DIR = os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams')

exams = ['2022_07', '2022_12', '2023_07', '2023_12', '2024_07', '2024_12']

all_passed = True
print("=== VERIFYING BATCH 1 QUALITY ===")

for ex in exams:
    p1 = os.path.join(DATA_DIR, f"{ex}.json")
    p2 = os.path.join(PUBLIC_DATA_DIR, f"{ex}.json")
    
    assert os.path.exists(p1), f"Missing {p1}"
    assert os.path.exists(p2), f"Missing {p2}"
    
    with open(p1, 'r', encoding='utf-8') as f:
        d = json.load(f)
        
    qs = d.get('questions', [])
    assert len(qs) == 101, f"{ex} has {len(qs)} questions, expected 101"
    
    empty_q = [q['number'] for q in qs if not q.get('question', '').strip()]
    assert len(empty_q) == 0, f"{ex} has empty questions: {empty_q}"
    
    vn_opts = []
    for q in qs:
        for opt in q.get('options', []):
            if any(w in opt for w in ['Phương án', 'lựa chọn', 'Lựa chọn', 'Đáp án']):
                vn_opts.append((q['number'], opt))
    assert len(vn_opts) == 0, f"{ex} has VN in options: {vn_opts}"
    
    # Check Mondai 9 passage
    m9_qs = [q for q in qs if 48 <= q['number'] <= 51]
    for q in m9_qs:
        assert len(q.get('passage', '').strip()) > 100, f"{ex} Q{q['number']} missing M9 passage"
        
    # Check Dokkai passage
    dokkai_qs = [q for q in qs if 52 <= q['number'] <= 71]
    for q in dokkai_qs:
        assert len(q.get('passage', '').strip()) > 50, f"{ex} Q{q['number']} missing Dokkai passage"
        
    # Check Choukai metadata
    choukai_qs = [q for q in qs if q['number'] >= 72]
    assert len(choukai_qs) == 30, f"{ex} Choukai has {len(choukai_qs)} questions, expected 30"
    for q in choukai_qs:
        assert q.get('questionNumber'), f"{ex} Q{q['number']} missing questionNumber"
        assert q.get('title'), f"{ex} Q{q['number']} missing title"
        assert q.get('audio'), f"{ex} Q{q['number']} missing audio"
        assert q.get('script'), f"{ex} Q{q['number']} missing script"
        
    print(f"PASSED {ex}: 101 câu chuẩn, M9 & Dokkai Split-View OK, Choukai 30 câu metadata chuẩn, 0 lỗi.")

print("\nALL BATCH 1 TESTS PASSED PERFECTLY!")
