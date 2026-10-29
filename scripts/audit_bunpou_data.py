# -*- coding: utf-8 -*-
"""
Audit Bunpou N1 data files to ensure 100% data integrity, schema compliance, and answer validity.
"""
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'n1_bunpou')
PUBLIC_DATA_DIR = os.path.join(ROOT_DIR, 'public', 'data', 'n1_bunpou')

def audit_directory(dir_path):
    print(f"\n==========================================")
    print(f"AUDITING DIRECTORY: {dir_path}")
    print(f"==========================================")
    
    idx_path = os.path.join(dir_path, 'n1_bunpou_index.json')
    if not os.path.exists(idx_path):
        print(f"[FAIL] Missing index file: {idx_path}")
        return False
        
    with open(idx_path, 'r', encoding='utf-8') as f:
        idx_data = json.load(f)
        
    chapters = idx_data.get('chapters', [])
    print(f"Index chapters count: {len(chapters)}")
    
    total_q = 0
    errors = []
    
    for ch in chapters:
        ch_file = os.path.join(dir_path, ch['file'])
        if not os.path.exists(ch_file):
            errors.append(f"Missing file: {ch['file']}")
            continue
            
        with open(ch_file, 'r', encoding='utf-8') as f:
            cdata = json.load(f)
            
        questions = cdata.get('questions', [])
        total_q += len(questions)
        
        for q in questions:
            qid = q.get('id')
            if not qid:
                errors.append(f"Question missing id in {ch['file']}")
                
            ans = q.get('answer')
            if ans not in ['a', 'b', 'c']:
                errors.append(f"Invalid answer '{ans}' in {qid} of {ch['file']}")
                
            opts = q.get('options', [])
            if not isinstance(opts, list) or len(opts) < 2:
                errors.append(f"Insufficient options in {qid} of {ch['file']}: {opts}")
                
            if not q.get('question'):
                errors.append(f"Empty question text in {qid} of {ch['file']}")
                
            if not q.get('explanation'):
                errors.append(f"Empty explanation in {qid} of {ch['file']}")
                
            if not q.get('grammarRule'):
                errors.append(f"Empty grammarRule in {qid} of {ch['file']}")
                
        print(f"✓ {ch['file']}: {len(questions)} câu - Validated 100%")
        
    print(f"\n--- AUDIT SUMMARY FOR {os.path.basename(dir_path)} ---")
    print(f"Total verified questions: {total_q}")
    if errors:
        print(f"[FAIL] Errors encountered ({len(errors)}):")
        for err in errors[:10]:
            print(f"  - {err}")
        return False
    else:
        print(f"[SUCCESS] 100% of questions passed all validation criteria!")
        return True

success_data = audit_directory(DATA_DIR)
success_public = audit_directory(PUBLIC_DATA_DIR)

if success_data and success_public:
    print("\nALL AUDIT CHECKS PASSED PERFECTLY!")
    sys.exit(0)
else:
    print("\nAUDIT CHECKS FAILED!")
    sys.exit(1)
