import json
import os
import re
import glob

def validate_n2_exam(exam):
    errors = []
    qs = exam.get('questions', [])
    if not qs:
        return False, ["Exam has no questions"]
        
    for q in qs:
        num = q.get('number')
        opts = q.get('options', [])
        ans = q.get('answer')
        sec = q.get('section', '')
        is_listening = q.get('sectionGroup') == 'listening'
        is_m4_listening = is_listening and '問題4' in sec
        
        # 1. Option count
        expected_opts = 3 if is_m4_listening else 4
        if len(opts) != expected_opts:
            errors.append(f"Q{num}: Expected {expected_opts} options, got {len(opts)}")
            
        # 2. Option content sanity
        for idx, opt in enumerate(opts):
            if not isinstance(opt, str):
                errors.append(f"Q{num} opt {idx+1}: not a string")
            elif len(opt) > 150:
                errors.append(f"Q{num} opt {idx+1}: length {len(opt)} > 150")
            elif re.search(r'問題\s*[0-9１-９]|から一つ選', opt):
                errors.append(f"Q{num} opt {idx+1}: contains problem header text")
                
        # 3. Answer sanity
        if ans is None or not isinstance(ans, int) or ans < 0 or ans >= len(opts):
            errors.append(f"Q{num}: invalid answer {ans} for len {len(opts)}")
            
        # 4. Choukai questionNumber
        if is_listening:
            qn = q.get('questionNumber')
            if not qn or '番' not in str(qn):
                errors.append(f"Q{num} (Choukai): missing or invalid questionNumber: {qn}")
                
    return len(errors) == 0, errors

def validate_n1_day(day_data):
    errors = []
    qs = day_data.get('questions', [])
    if not qs:
        return False, ["Day has no questions"]
        
    for q in qs:
        num = q.get('number')
        opts = q.get('options', [])
        ans = q.get('answer')
        sec = q.get('section', '')
        
        # 1. Option count
        if len(opts) != 4:
            errors.append(f"Q{num}: Expected 4 options, got {len(opts)}")
            
        # 2. Option content sanity
        for idx, opt in enumerate(opts):
            if not isinstance(opt, str):
                errors.append(f"Q{num} opt {idx+1}: not a string")
            elif len(opt) > 150:
                errors.append(f"Q{num} opt {idx+1}: length {len(opt)} > 150")
            elif re.search(r'問題\s*[0-9１-９]|から一つ選', opt):
                errors.append(f"Q{num} opt {idx+1}: contains problem header text")
                
        # 3. Answer sanity
        if ans is None or not isinstance(ans, int) or ans < 0 or ans >= 4:
            errors.append(f"Q{num}: invalid answer {ans}")
            
        # 4. Mondai 7 passage check
        if '問題7' in sec:
            passage = q.get('passage', '')
            if not passage or len(passage.strip()) < 10:
                errors.append(f"Q{num} (Mondai 7): missing or empty passage")
                
    return len(errors) == 0, errors

if __name__ == '__main__':
    # Test current N2 exams
    n2_files = sorted(glob.glob('public/data/n2_exams/[0-9]*.json'))
    print(f"Testing {len(n2_files)} N2 exams against Validation Gate...")
    all_n2_pass = True
    for f in n2_files:
        exam_id = os.path.basename(f).replace('.json', '')
        with open(f, 'r', encoding='utf-8') as fp:
            exam = json.load(fp)
        ok, errs = validate_n2_exam(exam)
        if not ok:
            print(f"FAILED {exam_id}: {errs[:3]}")
            all_n2_pass = False

    if all_n2_pass:
        print(f"ALL {len(n2_files)} N2 EXAMS PASSED VALIDATION GATE 100%!")
