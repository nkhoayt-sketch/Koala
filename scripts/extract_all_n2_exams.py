import sys
import os
import re
import json
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N2_SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'data', 'n2_exams')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Source Directory: {N2_SOURCE_DIR}")
print(f"Output Directory: {OUTPUT_DIR}")

# 1. Parse Answer Key PDF
ans_pdf = os.path.join(N2_SOURCE_DIR, 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader_ans = pypdf.PdfReader(ans_pdf)
print(f"Total answer key pages: {len(reader_ans.pages)}")

def parse_page_answers(p_idx):
    text = reader_ans.pages[p_idx].extract_text()
    chokai_idx = text.find('聴解')
    if chokai_idx != -1:
        text = text[:chokai_idx]
    
    raw_lines = [l.strip() for l in text.split('\n') if l.strip()]
    q_to_ans = {}
    pending_questions = []
    
    for l in raw_lines:
        if any(h in l for h in ['JLPT', '文字・語彙', '文法', '読解', 'ĐÁP ÁN']):
            continue
        l_clean = re.sub(r'問題\s*[0-9０-９一二三四五六七八九１-９]*', '', l).strip()
        if not l_clean:
            continue
        
        nums = [int(x) for x in re.findall(r'\b\d+\b', l_clean)]
        if not nums:
            continue
        
        next_expected = len(q_to_ans) + len(pending_questions) + 1
        is_q_line = any(n > 4 for n in nums) or (nums[0] == next_expected and len(nums) > 1 and nums[1] == next_expected + 1) or (nums[0] == next_expected and len(pending_questions) == 0 and not all(1 <= x <= 4 for x in nums))
        
        if pending_questions and len(nums) == len(pending_questions) and all(1 <= x <= 4 for x in nums):
            for q, a in zip(pending_questions, nums):
                q_to_ans[q] = a
            pending_questions = []
        elif is_q_line:
            pending_questions.extend(nums)
        elif pending_questions and all(1 <= x <= 4 for x in nums):
            for a in nums:
                if pending_questions:
                    q = pending_questions.pop(0)
                    q_to_ans[q] = a
        elif not pending_questions and nums[0] == 1 and all(nums[j] == j+1 for j in range(len(nums))):
            pending_questions.extend(nums)
            
    return q_to_ans

answer_db = {}
for p_idx in range(1, len(reader_ans.pages)):
    text = reader_ans.pages[p_idx].extract_text()
    m_ym = re.search(r'(\d{1,2})/(\d{4})|(\d{4})/(\d{1,2})', text)
    if m_ym:
        if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
            month, year = int(m_ym.group(1)), int(m_ym.group(2))
        else:
            year, month = int(m_ym.group(3)), int(m_ym.group(4))
    else:
        continue
    
    key = f"{year}_{month:02d}"
    ans = parse_page_answers(p_idx)
    answer_db[key] = ans

print(f"Loaded answers for {len(answer_db)} exam sessions.")

# 2. Extract Questions from PDF text
SEC_NAMES = {
    1: "問題1: 漢字読み",
    2: "問題2: 表記",
    3: "問題3: 語形成",
    4: "問題4: 文脈規定",
    5: "問題5: 言い換え類義",
    6: "問題6: 用法",
    7: "問題7: 文法形式の判断",
    8: "問題8: 文の組み立て ★",
    9: "問題9: 文章の文法",
    10: "問題10: 短文読解",
    11: "問題11: 中文読解",
    12: "問題12: 統合理解",
    13: "問題13: 長文読解",
    14: "問題14: 情報検索"
}

SEC_INSTRUCTIONS = {
    1: "＿＿の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。",
    2: "＿＿の言葉を漢字で書くとき、最もよいものを、1・2・3・4から一つ選びなさい。",
    3: "（   ）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
    4: "（   ）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
    5: "＿＿の言葉に意味が最も近いものを、1・2・3・4から一つ選びなさい。",
    6: "次の言葉の使い方として最もよいものを、1・2・3・4から一つ選びなさい。",
    7: "次の文の（   ）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
    8: "次の文の＿★＿に入る最もよいものを、1・2・3・4から一つ選びなさい。",
    9: "次の文章を読んで、文章全体の内容を考えて、（   ）に入る最もよいものを、1・2・3・4から一つ選びなさい。",
    10: "次の文章を読んで、後の問いに対する答えとして最もよいものを、1・2・3・4から一つ選びなさい。"
}

def extract_options_clean(block):
    # Standardize zenkaku numbers
    # Look for positions of １, ２, ３, ４ or 1, 2, 3, 4
    # Pattern to find all option segments:
    # １ (...) ２ (...) ３ (...) ４ (...)
    opt_m = re.search(r'[１1]\s*(.*?)[２2]\s*(.*?)[３3]\s*(.*?)[４4]\s*(.*)', block, re.DOTALL)
    if opt_m:
        q_text = block[:opt_m.start()].strip()
        opts = [
            re.sub(r'\s+', ' ', opt_m.group(1).strip()),
            re.sub(r'\s+', ' ', opt_m.group(2).strip()),
            re.sub(r'\s+', ' ', opt_m.group(3).strip()),
            re.sub(r'\s+', ' ', opt_m.group(4).strip())
        ]
        return q_text, opts
    return block.strip(), []

def process_exam_pdf(pdf_path, year, month):
    reader = pypdf.PdfReader(pdf_path)
    all_text = ""
    for idx, page in enumerate(reader.pages):
        txt = page.extract_text() or ''
        if '聴解' in txt and ('問題 1' in txt or '問題１' in txt or idx >= 18):
            break
        all_text += f"\n" + txt

    # Clean header noise
    lines = all_text.split('\n')
    clean_lines = []
    for line in lines:
        l_strip = line.strip()
        if re.match(r'^JLPT[・\s]N2[・\s]\d+/\d+', l_strip):
            continue
        if re.match(r'^\d{1,2}$', l_strip):
            continue
        clean_lines.append(line)
    content = "\n".join(clean_lines)

    exam_key = f"{year}_{month:02d}"
    answers = answer_db.get(exam_key, {})
    
    # We target questions 1 to 56 (Vocab, Grammar, Short Reading)
    q_nums = sorted([q for q in answers.keys() if q <= 56])
    if not q_nums:
        # Fallback to standard 1..51
        q_nums = list(range(1, 52))

    questions = []
    for i, q in enumerate(q_nums):
        next_q = q_nums[i+1] if i+1 < len(q_nums) else None
        
        # Determine section
        if q <= 5: sec_num = 1
        elif q <= 10: sec_num = 2
        elif q <= 13: sec_num = 3 # 3 questions
        elif q <= 20: sec_num = 4 # 7 questions
        elif q <= 25: sec_num = 5 # 5 questions
        elif q <= 30: sec_num = 6 # 5 questions
        elif q <= 42: sec_num = 7 # 12 questions
        elif q <= 47: sec_num = 8 # 5 questions
        elif q <= 51: sec_num = 9 # 4 questions
        else: sec_num = 10 # 5 short reading questions

        # Extract question block
        pattern = rf'(?:^|\n)\s*{q}\s+(.*?)(?=(?:\n\s*{next_q}\s+[^\d]|\n\s*(?:問題|間題|題題)|\Z))' if next_q else rf'(?:^|\n)\s*{q}\s+(.*?)(?=(?:\n\s*(?:問題|間題|題題)|\Z))'
        m = re.search(pattern, content, re.DOTALL)
        if not m:
            pattern_fallback = rf'\b{q}\s+(.*?)(?=(?:\b{next_q}\s+|\Z))' if next_q else rf'\b{q}\s+(.*)'
            m = re.search(pattern_fallback, content, re.DOTALL)
            
        if m:
            block = m.group(1).strip()
            q_text, opts = extract_options_clean(block)
        else:
            q_text = f"Câu hỏi {q} (Đang hoàn thiện nội dung câu)"
            opts = ["Phương án 1", "Phương án 2", "Phương án 3", "Phương án 4"]

        # If options failed to extract properly, provide fallback
        if len(opts) != 4 or not opts[0]:
            # Try splitting by lines with numbers
            opt_lines = [l.strip() for l in block.split('\n') if any(l.strip().startswith(c) for c in ['1', '2', '3', '4', '１', '２', '３', '４'])]
            if len(opt_lines) >= 4:
                opts = [re.sub(r'^[1234１２３４\s.]+', '', l).strip() for l in opt_lines[:4]]
            else:
                opts = opts if len(opts) == 4 else ["1", "2", "3", "4"]

        ans_val = answers.get(q, 1) # 1..4
        ans_idx = max(0, min(3, ans_val - 1)) # 0..3
        correct_text = opts[ans_idx] if len(opts) > ans_idx else f"Đáp án {ans_val}"

        # Clean question text
        q_text = re.sub(r'\s+', ' ', q_text).strip()
        # Highlight problem 8 star
        if sec_num == 8 and '★' not in q_text:
            q_text += " ＿＿ ＿＿ ＿★＿ ＿＿"

        q_obj = {
            "id": f"n2-{year}{month:02d}-q{q:02d}",
            "number": q,
            "sectionGroup": "vocab_grammar" if sec_num <= 9 else "reading",
            "section": SEC_NAMES.get(sec_num, f"問題 {sec_num}"),
            "instruction": SEC_INSTRUCTIONS.get(sec_num, ""),
            "question": q_text,
            "options": opts,
            "answer": ans_idx,
            "explanation": f"【正解】{ans_val} ({correct_text})\n\n• Giải thích kiến thức và ngữ cảnh câu {q} trong đề thi JLPT N2 {month:02d}/{year}."
        }
        questions.append(q_obj)

    vocab_count = sum(1 for q in questions if q['sectionGroup'] == 'vocab_grammar')
    reading_count = sum(1 for q in questions if q['sectionGroup'] == 'reading')

    exam_json = {
        "id": f"n2-{year}-{month:02d}",
        "level": "N2",
        "year": year,
        "month": month,
        "title": f"JLPT N2 - {month:02d}/{year}",
        "theme": f"Đề thi chính thức JLPT N2 (Tháng {month:02d}/{year})",
        "description": f"Trọn bộ đề thi thực tế JLPT N2 kỳ tháng {month:02d}/{year} phần Kiến thức ngôn ngữ (Từ vựng, Ngữ pháp) và Đọc hiểu.",
        "totalQuestions": len(questions),
        "vocabGrammarCount": vocab_count,
        "readingCount": reading_count,
        "durations": {
            "vocab_grammar": 35,
            "full": 105
        },
        "questions": questions
    }

    return exam_json

def extract_script_dialogues(script_pdf_path):
    """Automatically extracts Choukai question transcripts from script PDF if available."""
    try:
        reader = pypdf.PdfReader(script_pdf_path)
        full_text = ''
        for p in reader.pages:
            full_text += p.extract_text() + '\n'

        clean = re.sub(r'<<<PAGE \d+>>>', '', full_text)
        clean = re.sub(r'JLPT・N2・\d+/\d+', '', clean)
        clean = re.sub(r'☆\d+/\d+☆', '', clean)

        m_splits = re.split(r'問題\s*([1-5１-５])', clean)
        mondais = {}
        for i in range(1, len(m_splits), 2):
            m_num = int(m_splits[i].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5'))
            mondais[m_num] = m_splits[i+1]

        scripts = {}
        # Mondai 1
        if 1 in mondais:
            q_splits = re.split(r'\n\s*([１-９\d]+)\s*番', '\n' + mondais[1])
            for q_idx in range(1, len(q_splits), 2):
                q_num = int(q_splits[q_idx].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5'))
                scripts[("m1", q_num)] = q_splits[q_idx+1].strip()

        # Mondai 2
        if 2 in mondais:
            q_splits = re.split(r'\n\s*([１-９\d]+)\s*番', '\n' + mondais[2])
            for q_idx in range(1, len(q_splits), 2):
                q_num = int(q_splits[q_idx].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5').replace('６','6'))
                scripts[("m2", q_num)] = q_splits[q_idx+1].strip()

        # Mondai 3
        if 3 in mondais:
            q_splits = re.split(r'\n\s*([１-９\d]+)\s*番', '\n' + mondais[3])
            for q_idx in range(1, len(q_splits), 2):
                q_num = int(q_splits[q_idx].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5'))
                scripts[("m3", q_num)] = q_splits[q_idx+1].strip()

        # Mondai 4
        if 4 in mondais:
            q_splits = re.split(r'\n\s*([１-９\d]+)\s*番', '\n' + mondais[4])
            for q_idx in range(1, len(q_splits), 2):
                num_str = q_splits[q_idx].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5').replace('６','6').replace('７','7').replace('８','8').replace('９','9').replace('０','0')
                q_num = int(num_str)
                scripts[("m4", q_num)] = q_splits[q_idx+1].strip()

        # Mondai 5
        if 5 in mondais:
            q_splits = re.split(r'\n\s*([１-９\d]+)\s*番', '\n' + mondais[5])
            if len(q_splits) > 2:
                scripts[("m5", 1)] = q_splits[2].strip()
            if len(q_splits) > 4:
                scripts[("m5", 2)] = q_splits[4].strip()
                scripts[("m5", 3)] = q_splits[4].strip()

        return scripts
    except Exception as e:
        print(f"Warning: Could not parse script PDF {script_pdf_path}: {e}")
        return {}

# 3. Scan all folders in N2_DE_CAC_NAM and process
all_exams_meta = []

folders = sorted([d for d in os.listdir(N2_SOURCE_DIR) if os.path.isdir(os.path.join(N2_SOURCE_DIR, d))])
print(f"\nProcessing {len(folders)} folders...")

for folder in folders:
    # Match year and month from folder name, e.g. "14. N2 7-2023", "9. N2 12-2018", "13. N2 12-2022"
    m_ym = re.search(r'(\d{1,2})[-/.](\d{4})|(\d{4})[-/.](\d{1,2})', folder)
    if not m_ym:
        continue
    if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
        month, year = int(m_ym.group(1)), int(m_ym.group(2))
    else:
        year, month = int(m_ym.group(3)), int(m_ym.group(4))

    folder_path = os.path.join(N2_SOURCE_DIR, folder)
    files = os.listdir(folder_path)
    exam_pdf_candidates = [f for f in files if f.endswith('.pdf') and 'script' not in f.lower()]
    script_pdf_candidates = [f for f in files if f.endswith('.pdf') and 'script' in f.lower()]
    if script_pdf_candidates:
        script_file = os.path.join(folder_path, script_pdf_candidates[0])
        print(f"   (Detected script PDF: '{script_pdf_candidates[0]}')")

    pdf_file = os.path.join(folder_path, exam_pdf_candidates[0])
    print(f"-> Extracting {year}_{month:02d} from '{exam_pdf_candidates[0]}'...")
    
    exam_data = process_exam_pdf(pdf_file, year, month)
    
    # Save as YYYY_MM.json (user requested specification!)
    out_name = f"{year}_{month:02d}.json"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    with open(out_path, 'w', encoding='utf-8') as f_out:
        json.dump(exam_data, f_out, ensure_ascii=False, indent=2)

    # Also save as n2_YYYY_MM.json for legacy backwards-compatibility
    out_legacy = os.path.join(OUTPUT_DIR, f"n2_{year}_{month:02d}.json")
    with open(out_legacy, 'w', encoding='utf-8') as f_out:
        json.dump(exam_data, f_out, ensure_ascii=False, indent=2)

    all_exams_meta.append({
        "id": f"n2-{year}-{month:02d}",
        "level": "N2",
        "year": year,
        "month": month,
        "title": f"JLPT N2 - {month:02d}/{year}",
        "theme": f"Đề thi chính thức {month:02d}/{year}",
        "description": f"Đề thi chính thức kỳ thi JLPT N2 tháng {month:02d}/{year}.",
        "file": f"data/n2_exams/{out_name}",
        "available": True,
        "totalQuestions": exam_data["totalQuestions"],
        "vocabGrammarCount": exam_data["vocabGrammarCount"],
        "readingCount": exam_data["readingCount"],
        "durations": exam_data["durations"]
    })

# Sort meta by year desc, month desc
all_exams_meta.sort(key=lambda x: (x['year'], x['month']), reverse=True)

# Save updated index
index_path = os.path.join(ROOT_DIR, 'data', 'n2-index.json')
with open(index_path, 'w', encoding='utf-8') as f_idx:
    json.dump(all_exams_meta, f_idx, ensure_ascii=False, indent=2)

index_copy_path = os.path.join(OUTPUT_DIR, 'n2-index.json')
with open(index_copy_path, 'w', encoding='utf-8') as f_idx:
    json.dump(all_exams_meta, f_idx, ensure_ascii=False, indent=2)

print(f"\nSUCCESS! Generated {len(all_exams_meta)} JSON exams and updated n2-index.json.")
