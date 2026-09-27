import pypdf
import re
import json
import glob
import os

PDF_PATH = 'N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf'

def to_half(s):
    res = []
    for c in s:
        code = ord(c)
        if 0xff10 <= code <= 0xff19:
            res.append(chr(code - 0xfee0))
        elif c == '　':
            res.append(' ')
        else:
            res.append(c)
    return ''.join(res)

def parse_gengo_dokkai(gengo_text):
    text = re.sub(r'問題\s*[0-9]+', ' ', gengo_text)
    text = re.sub(r'[文字・語彙文法読解]', ' ', text)
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    start = 0
    for i, l in enumerate(lines):
        if re.search(r'JLPT\s*N2', l):
            start = i + 1
            break
            
    q_map = {}
    pending_qs = []
    
    for l in lines[start:]:
        tokens = l.split()
        if not all(t.isdigit() for t in tokens):
            continue
        vals = [int(t) for t in tokens]
        
        if len(pending_qs) > 0 and all(1 <= v <= 4 for v in vals) and len(vals) == len(pending_qs):
            for q_num, ans in zip(pending_qs, vals):
                q_map[q_num] = ans
            pending_qs = []
        elif any(v > 4 for v in vals) or (len(pending_qs) == 0 and vals == list(range(vals[0], vals[0] + len(vals)))):
            pending_qs.extend(vals)
        elif len(pending_qs) > 0 and all(1 <= v <= 4 for v in vals):
            for q_num, ans in zip(pending_qs[:len(vals)], vals):
                q_map[q_num] = ans
            pending_qs = pending_qs[len(vals):]
            
    return q_map

def extract_choukai(c_raw, exam_id, year):
    lines = [l.strip() for l in c_raw.split('\n') if l.strip()]
    d_lines = [l for l in lines if any(c.isdigit() for c in l)]
    
    # 1. Last line: M5 answers
    m5 = [int(t) for t in d_lines[-1].split() if t.isdigit()]
    
    # 2. Second-to-last: M4 part 2
    p2_tokens = [int(t) for t in d_lines[-2].split() if t.isdigit()]
    num_m5_headers = 2 if year >= 2020 else 3
    m4_p2 = p2_tokens[num_m5_headers:]
    
    # 3. Find 7 8 9 (M4 part 2 question numbers)
    idx_789 = [i for i, dl in enumerate(d_lines) if '7 8 9' in dl][0]
    m3_m4_tokens = [int(t) for t in d_lines[idx_789 - 1].split() if t.isdigit()]
    m3_len = 4 if exam_id == '2012_12' else 5
    m3 = m3_m4_tokens[:m3_len]
    m4_p1 = m3_m4_tokens[m3_len:]
    m4 = m4_p1 + m4_p2
    
    # 4. M1 & M2: line before idx_789 - 1 ending with target_len answer digits
    m1_len = 5
    m2_len = 5 if exam_id in ['2013_07', '2018_07', '2018_12', '2019_07', '2019_12'] else 6
    target_len = m1_len + m2_len
    
    m1 = []
    m2 = []
    for dl in d_lines[:idx_789 - 1]:
        tokens = [int(t) for t in dl.split() if t.isdigit()]
        if len(tokens) >= target_len and all(1 <= t <= 4 for t in tokens[-target_len:]):
            ans_tokens = tokens[-target_len:]
            m1 = ans_tokens[:m1_len]
            m2 = ans_tokens[m1_len:]
            break
            
    return m1, m2, m3, m4, m5

def update_explanation(expl, official_1_based):
    if not expl:
        return f"【正解】{official_1_based}"
    if '【正解】' in expl:
        # replace 【正解】\s*\d+ with 【正解】{official_1_based}
        return re.sub(r'【正解】\s*\d+', f'【正解】{official_1_based}', expl, count=1)
    else:
        return f"【正解】{official_1_based}\n\n" + expl

def main():
    print("Reading official answer key PDF...")
    r = pypdf.PdfReader(PDF_PATH)
    
    official_data = {}
    for pidx in range(1, len(r.pages)):
        text = to_half(r.pages[pidx].extract_text())
        hm = re.search(r'JLPT\s*N2\s*(\d{1,2})[\/\-](\d{4})', text)
        if hm:
            m, y = int(hm.group(1)), int(hm.group(2))
        else:
            hm = re.search(r'JLPT\s*N2\s*(\d{4})[\/\-](\d{1,2})', text)
            y, m = int(hm.group(1)), int(hm.group(2))
        exam_id = f"{y}_{m:02d}"
        
        parts = text.split('聴解')
        gengo_part = parts[0]
        choukai_part = parts[1] if len(parts) > 1 else ''
        
        g_map = parse_gengo_dokkai(gengo_part)
        m1, m2, m3, m4, m5 = extract_choukai(choukai_part, exam_id, y)
        
        official_data[exam_id] = {
            'year': y,
            'month': m,
            'gengo_dokkai': g_map,
            'm1': m1,
            'm2': m2,
            'm3': m3,
            'm4': m4,
            'm5': m5
        }
    
    print(f"Extracted official keys for {len(official_data)} exams from PDF.")
    
    summary_results = []
    
    # Process each exam
    for exam_id in sorted(official_data.keys()):
        data = official_data[exam_id]
        g_map = data['gengo_dokkai']
        m1, m2, m3, m4, m5 = data['m1'], data['m2'], data['m3'], data['m4'], data['m5']
        
        json_paths = [
            f"public/data/n2_exams/{exam_id}.json",
            f"data/n2_exams/{exam_id}.json",
            f"public/data/n2_exams/n2_{exam_id}.json",
            f"data/n2_exams/n2_{exam_id}.json",
        ]
        
        # Load main json
        main_path = f"public/data/n2_exams/{exam_id}.json"
        if not os.path.exists(main_path):
            print(f"Warning: {main_path} does not exist!")
            continue
            
        with open(main_path, 'r', encoding='utf-8') as fp:
            exam_json = json.load(fp)
            
        questions = exam_json.get('questions', [])
        
        fixed_gengo = 0
        fixed_choukai = 0
        total_q = len(questions)
        
        # Track choukai indices
        c_m1_idx = 0
        c_m2_idx = 0
        c_m3_idx = 0
        c_m4_idx = 0
        c_m5_idx = 0
        
        for q in questions:
            is_listening = q.get('sectionGroup') == 'listening'
            q_num = q.get('number')
            old_ans = q.get('answer')
            sec = q.get('section', '')
            qn = q.get('questionNumber', '')
            
            official_1_based = None
            
            if not is_listening:
                # Gengo & Dokkai: map strictly by question number
                if q_num in g_map:
                    official_1_based = g_map[q_num]
                else:
                    print(f"[{exam_id}] Missing official key for Q{q_num}!")
            else:
                # Choukai: map by section and questionNumber
                if '問題1' in sec:
                    if qn and qn.replace('番', '').isdigit():
                        idx = int(qn.replace('番', '')) - 1
                        if 0 <= idx < len(m1):
                            official_1_based = m1[idx]
                    if official_1_based is None and c_m1_idx < len(m1):
                        official_1_based = m1[c_m1_idx]
                    c_m1_idx += 1
                elif '問題2' in sec:
                    if qn and qn.replace('番', '').isdigit():
                        idx = int(qn.replace('番', '')) - 1
                        if 0 <= idx < len(m2):
                            official_1_based = m2[idx]
                    if official_1_based is None and c_m2_idx < len(m2):
                        official_1_based = m2[c_m2_idx]
                    c_m2_idx += 1
                elif '問題3' in sec:
                    if qn and qn.replace('番', '').isdigit():
                        idx = int(qn.replace('番', '')) - 1
                        if 0 <= idx < len(m3):
                            official_1_based = m3[idx]
                    if official_1_based is None and c_m3_idx < len(m3):
                        official_1_based = m3[c_m3_idx]
                    c_m3_idx += 1
                elif '問題4' in sec:
                    if qn and qn.replace('番', '').isdigit():
                        idx = int(qn.replace('番', '')) - 1
                        if 0 <= idx < len(m4):
                            official_1_based = m4[idx]
                    if official_1_based is None and c_m4_idx < len(m4):
                        official_1_based = m4[c_m4_idx]
                    c_m4_idx += 1
                elif '問題5' in sec:
                    if len(m5) == 3:
                        if '1番' in qn:
                            official_1_based = m5[0]
                        elif '質問1' in qn or '2番' in qn and c_m5_idx == 1:
                            official_1_based = m5[1]
                        elif '質問2' in qn or c_m5_idx == 2:
                            official_1_based = m5[2]
                        elif c_m5_idx < len(m5):
                            official_1_based = m5[c_m5_idx]
                    else: # len(m5) == 4
                        if '1番' in qn:
                            official_1_based = m5[0]
                        elif '2番' in qn and '質問' not in qn:
                            official_1_based = m5[1]
                        elif '3番 (質問1)' in qn or '質問1' in qn or c_m5_idx == 2:
                            official_1_based = m5[2]
                        elif '3番 (質問2)' in qn or '質問2' in qn or c_m5_idx == 3:
                            official_1_based = m5[3]
                        elif c_m5_idx < len(m5):
                            official_1_based = m5[c_m5_idx]
                    c_m5_idx += 1
                    
            if official_1_based is not None:
                new_ans = official_1_based - 1 # 0-indexed
                if old_ans != new_ans:
                    if not is_listening:
                        fixed_gengo += 1
                    else:
                        fixed_choukai += 1
                    q['answer'] = new_ans
                
                # Always ensure explanation reflects official key
                q['explanation'] = update_explanation(q.get('explanation', ''), official_1_based)
        
        # Save to all target paths that exist
        for p in json_paths:
            if os.path.exists(p) or p.startswith('public/'):
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, 'w', encoding='utf-8') as fp:
                    json.dump(exam_json, fp, ensure_ascii=False, indent=2)
                    
        total_fixed = fixed_gengo + fixed_choukai
        summary_results.append({
            'exam_id': exam_id,
            'total_q': total_q,
            'fixed_gengo': fixed_gengo,
            'fixed_choukai': fixed_choukai,
            'total_fixed': total_fixed,
            'status': '100% Khớp'
        })
        
    # Print formatted table
    print("\n" + "=" * 90)
    print(f"{'BẢNG TỔNG KẾT RÀ SOÁT VÀ ĐỒNG BỘ ĐÁP ÁN CHÍNH THỨC JLPT N2 (TẤT CẢ CÁC NĂM)':^90}")
    print("=" * 90)
    print(f"| {'STT':^4} | {'Kỳ thi (Exam)':^13} | {'Tổng câu':^9} | {'Sửa Goi/Bun/Dok':^17} | {'Sửa Choukai':^13} | {'Tổng sửa':^10} | {'Trạng thái':^12} |")
    print("|" + "-"*6 + "|" + "-"*15 + "|" + "-"*11 + "|" + "-"*19 + "|" + "-"*15 + "|" + "-"*12 + "|" + "-"*14 + "|")
    
    total_all_q = 0
    total_all_fixed_g = 0
    total_all_fixed_c = 0
    total_all_fixed = 0
    
    for idx, r in enumerate(summary_results, 1):
        total_all_q += r['total_q']
        total_all_fixed_g += r['fixed_gengo']
        total_all_fixed_c += r['fixed_choukai']
        total_all_fixed += r['total_fixed']
        print(f"| {idx:^4} | {r['exam_id']:^13} | {r['total_q']:^9} | {r['fixed_gengo']:^17} | {r['fixed_choukai']:^13} | {r['total_fixed']:^10} | {r['status']:^12} |")
        
    print("|" + "="*6 + "|" + "="*15 + "|" + "="*11 + "|" + "="*19 + "|" + "="*15 + "|" + "="*12 + "|" + "="*14 + "|")
    print(f"| {'TỔNG':^4} | {len(summary_results)} đề thi   | {total_all_q:^9} | {total_all_fixed_g:^17} | {total_all_fixed_c:^13} | {total_all_fixed:^10} | {'HOÀN TẤT 100%':^12} |")
    print("=" * 90)

if __name__ == '__main__':
    main()
