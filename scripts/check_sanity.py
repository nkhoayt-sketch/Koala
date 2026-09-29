import json
import glob
import os
import sys

# Configure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_exam_folder(folder_path, label="Exam"):
    files = sorted(glob.glob(os.path.join(folder_path, '*.json')))
    # Exclude index files and alt files to avoid duplicate counts
    exam_files = [f for f in files if 'index' not in os.path.basename(f) and not os.path.basename(f).startswith('n2_')]
    
    total_exams = len(exam_files)
    total_questions = 0
    star_questions_count = 0
    star_issues = []
    general_issues = []

    print(f"\n=======================================================")
    print(f" KIỂM TRA TOÀN VẸN DỮ LIỆU: {label} ({total_exams} đề/ngày)")
    print(f"=======================================================")

    for fpath in exam_files:
        fname = os.path.basename(fpath)
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            qs = data
        elif isinstance(data, dict):
            qs = data.get('questions', [])
            if not qs and 'sections' in data:
                for s in data['sections']:
                    qs.extend(s.get('questions', []))
        else:
            qs = []

        for idx, q in enumerate(qs):
            total_questions += 1
            q_num = q.get('number', idx + 1)
            q_id = q.get('id', f'{fname}_{q_num}')
            opts = q.get('options', [])
            ans = q.get('answer')
            q_text = q.get('question', '')
            section = q.get('section', '')
            group = q.get('sectionGroup', '')

            is_star = '★' in q_text or '問題8' in section or '並べ' in q.get('instruction', '')
            is_choukai_m4 = '問題4' in section and ('listening' in group or '聴解' in section)

            expected_opts = 3 if is_choukai_m4 else 4

            if is_star:
                star_questions_count += 1

            # Check options count
            opts_len = len(opts) if isinstance(opts, list) else 0
            if opts_len != expected_opts:
                issue = {
                    'file': fname,
                    'num': q_num,
                    'id': q_id,
                    'section': section,
                    'desc': f'Số lượng options = {opts_len} (yêu cầu {expected_opts})',
                    'options': opts,
                    'is_star': is_star
                }
                if is_star:
                    star_issues.append(issue)
                else:
                    general_issues.append(issue)
                continue

            # Check empty or whitespace-only options
            has_empty = any(opt is None or (isinstance(opt, str) and not opt.strip()) for opt in opts)
            if has_empty:
                issue = {
                    'file': fname,
                    'num': q_num,
                    'id': q_id,
                    'section': section,
                    'desc': f'Có option rỗng hoặc null: {opts}',
                    'options': opts,
                    'is_star': is_star
                }
                if is_star:
                    star_issues.append(issue)
                else:
                    general_issues.append(issue)
                continue

            # Check answer index range [0, len(opts)-1]
            if not isinstance(ans, int) or ans < 0 or ans >= len(opts):
                issue = {
                    'file': fname,
                    'num': q_num,
                    'id': q_id,
                    'section': section,
                    'desc': f'Giá trị answer không hợp lệ: {ans} (options: {len(opts)})',
                    'options': opts,
                    'is_star': is_star
                }
                if is_star:
                    star_issues.append(issue)
                else:
                    general_issues.append(issue)

    print(f"• Tổng số câu hỏi đã rà soát: {total_questions}")
    print(f"• Tổng số câu ghép sao (★): {star_questions_count}")
    print(f"• Số lỗi câu ghép sao (★): {len(star_issues)}")
    if star_issues:
        print("  [CẢNH BÁO] Danh sách câu ghép sao lỗi:")
        for iss in star_issues:
            print(f"   - [{iss['file']}] Câu {iss['num']} ({iss['section']}): {iss['desc']}")
    else:
        print("  ✅ 100% CÂU GHÉP SAO (★) ĐẠT CHUẨN ĐỦ 4 OPTIONS & ĐÁP ÁN CHÍNH XÁC!")

    return len(star_issues)

if __name__ == '__main__':
    n2_star_issues = check_exam_folder(os.path.join(ROOT_DIR, 'data', 'n2_exams'), "JLPT N2 (Tất cả các năm)")
    n1_star_issues = check_exam_folder(os.path.join(ROOT_DIR, 'data', 'n1_20days'), "20 Ngày Đỗ N1")

    print("\n=======================================================")
    if n2_star_issues == 0 and n1_star_issues == 0:
        print("🎉 TẤT CẢ CÂU HỎI GHÉP SAO ĐÃ ĐẠT CHUẨN 100%!")
    else:
        print(f"⚠️ Còn {n2_star_issues + n1_star_issues} câu sao chưa đạt chuẩn.")
    print("=======================================================\n")
