import sys
import os
import re
import json
import glob
import pypdf
import pykakasi

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'n2_exams')
PUBLIC_DATA_DIR = os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PUBLIC_DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(ROOT_DIR, 'public', 'data'), exist_ok=True)

kks = pykakasi.kakasi()

# 1. PARSE ALL OFFICIAL ANSWER KEYS
ans_pdf = os.path.join(SOURCE_DIR, 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader_ans = pypdf.PdfReader(ans_pdf)

def parse_answer_page(p_idx):
    text = reader_ans.pages[p_idx].extract_text()
    chokai_idx = text.find('聴解')
    if chokai_idx != -1:
        text = text[:chokai_idx]
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    cleaned = []
    for l in lines:
        if any(h in l for h in ['JLPT', '文字・語彙', '文法', '読解', 'ĐÁP ÁN']) or re.match(r'^\d{1,2}$', l):
            continue
        cleaned.append(l)

    q_to_ans = {}
    pending_qs = []
    for l in cleaned:
        clean_l = re.sub(r'問題\s*[0-9０-９一二三四五六七八九１-９]*', ' ', l)
        nums = [int(x) for x in re.findall(r'\b\d+\b', clean_l)]
        if not nums:
            continue
        next_expected = len(q_to_ans) + len(pending_qs) + 1
        is_q = False
        if any(n > 4 for n in nums):
            is_q = True
        elif nums[0] == next_expected:
            if not pending_qs:
                is_q = True
        if is_q:
            pending_qs.extend(nums)
        else:
            for a in nums:
                if pending_qs:
                    q = pending_qs.pop(0)
                    q_to_ans[q] = a
    return q_to_ans

answer_db = {}
for p in range(1, len(reader_ans.pages)):
    text = reader_ans.pages[p].extract_text()
    m_ym = re.search(r'(\d{1,2})[/.-](\d{4})|(\d{4})[/.-](\d{1,2})', text)
    if m_ym:
        if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
            month, year = int(m_ym.group(1)), int(m_ym.group(2))
        else:
            year, month = int(m_ym.group(3)), int(m_ym.group(4))
        key = f"{year}_{month:02d}"
        answer_db[key] = parse_answer_page(p)

print(f"Loaded answers for {len(answer_db)} exams.")

# 2. HELPER CONSTANTS & FUNCTIONS
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
    10: "次の文章を読んで、後の問いに対する答えとして最もよいものを、1・2・3・4から一つ選びなさい。",
    11: "次の文章を読んで、後の問いに対する答えとして最もよいものを、1・2・3・4から一つ選びなさい。",
    12: "次のAとBの文章を読んで、後の問いに対する答えとして最もよいものを、1・2・3・4から一つ選びなさい。",
    13: "次の文章を読んで、後の問いに対する答えとして最もよいものを、1・2・3・4から一つ選びなさい。",
    14: "下のページを読んで、後の問いに対する答えとして最もよいものを、1・2・3・4から一つ選びなさい。"
}

def clean_furigana(text):
    if not text:
        return ""
    lines = text.split('\n')
    cleaned = []
    for l in lines:
        s = l.strip()
        if s and re.fullmatch(r'[\u3040-\u309F\u30A0-\u30FF]{1,6}', s) and cleaned:
            continue
        cleaned.append(l)
    res = '\n'.join(cleaned)
    res = re.sub(r'([\u4e00-\u9fff])\n([\u4e00-\u9fff])', r'\1\2', res)
    res = re.sub(r'([\u4e00-\u9fff])\n([\u3040-\u309F])', r'\1\2', res)
    return res

def clean_passage(text):
    text = re.sub(r'<<<PAGE_\d+>>>', '', text)
    lines = text.split('\n')
    cleaned = []
    for l in lines:
        s = l.strip()
        if any(h in s for h in ['問題 10', '問題 11', '問題 12', '問題 13', '問題 14', '問題10', '問題11', '問題12', '問題13', '問題14', '読解', '次の(1)から', '次の（１）から', '次の A と B', '次の文章を読んで', '後の問いに対する答えとして', '下のページは', '右のページは', '1・2・3・4 から一つ選びなさい', '１・２・３・４から一つ選びなさい']):
            continue
        cleaned.append(l)
    p = '\n'.join(cleaned).strip()
    return clean_furigana(p)

def extract_options(block):
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
    lines = block.split('\n')
    opt_lines = [l.strip() for l in lines if re.match(r'^[1234１２３４]\s+', l.strip())]
    if len(opt_lines) >= 4:
        first_opt_idx = next(i for i, l in enumerate(lines) if re.match(r'^[1234１２３４]\s+', l.strip()))
        q_text = '\n'.join(lines[:first_opt_idx]).strip()
        opts = [re.sub(r'^[1234１２３４]\s+', '', l).strip() for l in opt_lines[:4]]
        return q_text, opts
    return block.strip(), []

def underline_m1(sentence, options):
    if '<u>' in sentence or not options:
        return sentence
    conv = kks.convert(sentence)
    for item in conv:
        orig = item['orig']
        hira = item['hira']
        if re.search(r'[\u4e00-\u9fff]', orig):
            if any(hira == opt or hira in opt or opt in hira for opt in options):
                return sentence.replace(orig, f"<u>{orig}</u>", 1)
    return sentence

def underline_m2(sentence, options):
    if '<u>' in sentence or not options:
        return sentence
    for opt in options:
        conv = kks.convert(opt)
        h = ''.join(c['hira'] for c in conv)
        if h and h in sentence and len(h) >= 2:
            return sentence.replace(h, f"<u>{h}</u>", 1)
    return sentence

def underline_m5(sentence, options):
    if '<u>' in sentence or not options:
        return sentence
    conv = kks.convert(sentence)
    for item in conv:
        orig = item['orig']
        if len(orig) >= 2 and orig in sentence:
            # Check if orig matches semantic stem
            pass
    return sentence

def get_sec_num(q, total_q):
    if total_q >= 74: # 2010-2017
        if q <= 5: return 1
        elif q <= 10: return 2
        elif q <= 15: return 3
        elif q <= 22: return 4
        elif q <= 27: return 5
        elif q <= 32: return 6
        elif q <= 44: return 7
        elif q <= 49: return 8
        elif q <= 54: return 9
        elif q <= 59: return 10
        elif q <= 68: return 11
        elif q <= 70: return 12
        elif q <= 73: return 13
        else: return 14
    elif total_q >= 72: # 2018-2021
        if q <= 5: return 1
        elif q <= 10: return 2
        elif q <= 13: return 3
        elif q <= 20: return 4
        elif q <= 25: return 5
        elif q <= 30: return 6
        elif q <= 42: return 7
        elif q <= 47: return 8
        elif q <= 51: return 9
        elif q <= 56: return 10
        elif q <= 64: return 11
        elif q <= 66: return 12
        elif q <= 69: return 13
        else: return 14
    else: # 2021-2025 standard (71 questions)
        if q <= 5: return 1
        elif q <= 10: return 2
        elif q <= 13: return 3
        elif q <= 20: return 4
        elif q <= 25: return 5
        elif q <= 30: return 6
        elif q <= 42: return 7
        elif q <= 47: return 8
        elif q <= 51: return 9
        elif q <= 56: return 10
        elif q <= 64: return 11
        elif q <= 66: return 12
        elif q <= 69: return 13
        else: return 14

def process_single_exam(pdf_path, year, month, answers):
    reader = pypdf.PdfReader(pdf_path)
    
    pages_text = []
    for p_idx in range(len(reader.pages)):
        txt = reader.pages[p_idx].extract_text() or ''
        if '聴解' in txt and ('問題 1' in txt or '問題１' in txt or '問題 １' in txt or p_idx >= len(reader.pages) - 8):
            break
        pages_text.append(f"\n<<<PAGE_{p_idx+1}>>>\n" + txt)
        
    full_text = "\n".join(pages_text)
    
    # Clean page headers
    clean_lines = []
    for l in full_text.split('\n'):
        ls = l.strip()
        if re.match(r'^(?:JLPT[・\s]N2|N2\s+\d+/\d+|\d{1,2}/\d{4}|\d{4}/\d{1,2})', ls, re.I):
            continue
        if re.match(r'^\d{1,2}$', ls): # page numbers
            continue
        clean_lines.append(l)
    text = "\n".join(clean_lines)

    total_q = max(answers.keys()) if answers else 71
    q_nums = sorted([q for q in answers.keys()])

    # Find position of each question
    positions = {}
    for q in q_nums:
        q_zen = str(q).translate(str.maketrans('0123456789', '０１２３４５６７８９'))
        m = re.search(rf'(?:^|\n)\s*(?:{q}|{q_zen})[a-z。、.\s\(\)（）]*(?!\s*から)(?=[^\d\n]|$)', text)
        if not m:
            m = re.search(rf'(?:\b|\s)(?:{q}|{q_zen})\s+(?=[^\d\n])', text)
        if m:
            positions[q] = m.start()

    # Extract Mondai 9 passage
    m9_passage = ""
    # Find Mondai 9 start
    m9_idx = text.find('問題 9')
    if m9_idx == -1: m9_idx = text.find('問題9')
    if m9_idx == -1: m9_idx = text.find('問題 ９')
    if m9_idx == -1: m9_idx = text.find('問題９')
    
    # First question of M9
    first_m9_q = next((q for q in q_nums if get_sec_num(q, total_q) == 9), None)
    if m9_idx != -1 and first_m9_q and first_m9_q in positions:
        raw_m9 = text[m9_idx:positions[first_m9_q]]
        # Clean header
        lines_m9 = raw_m9.split('\n')
        clean_m9_lines = [l for l in lines_m9 if not any(h in l for h in ['問題 9', '問題9', '問題 ９', '問題９', '文章全体の内容を考えて', 'から一つ選びなさい'])]
        m9_passage = clean_passage('\n'.join(clean_m9_lines))

    # Determine first Dokkai question
    first_dokkai_q = next((q for q in q_nums if get_sec_num(q, total_q) >= 10), None)

    # Initial Dokkai passage (Mondai 10 (1))
    current_dokkai_passage = ""
    if first_dokkai_q and first_dokkai_q in positions:
        m10_idx = text.find('問題 10')
        if m10_idx == -1: m10_idx = text.find('問題10')
        if m10_idx == -1: m10_idx = text.find('問題 １０')
        if m10_idx == -1: m10_idx = text.find('問題１０')
        if m10_idx == -1: m10_idx = text.find('読解')
        if m10_idx != -1 and m10_idx < positions[first_dokkai_q]:
            raw_m10 = text[m10_idx:positions[first_dokkai_q]]
            current_dokkai_passage = clean_passage(raw_m10)

    # Find Mondai 14 poster passage if placed at end
    m14_passage = ""
    last_q = q_nums[-1]
    if last_q in positions:
        # Check text after last question
        opt4_last = re.search(r'[４4]\s*(.*?)(?=\n<<<PAGE_|\Z)', text[positions[last_q]:], re.DOTALL)
        if opt4_last:
            tail = text[positions[last_q] + opt4_last.end():]
            clean_tail = clean_passage(tail)
            if len(clean_tail) > 100:
                m14_passage = clean_tail

    questions = []
    for idx, q in enumerate(q_nums):
        sec_num = get_sec_num(q, total_q)
        next_q = q_nums[idx+1] if idx+1 < len(q_nums) else None
        
        q_start = positions.get(q)
        # Find next valid end position
        q_end = next((positions[future_q] for future_q in q_nums[idx+1:] if positions.get(future_q) is not None), len(text))
        
        if q_start is not None and q_end > q_start:
            chunk = text[q_start:q_end]
            
            # Find option 4 boundary
            opt4_m = re.search(r'(?:^|\n)\s*[４4]\s*(.*?)(?=(?:\n\s*(?:（[１-９\d]+）|\([１-９\d]+\)|問題|\bA\b|\bB\b)|\n<<<PAGE_|\Z))', chunk, re.DOTALL)
            if opt4_m:
                q_opts_block = chunk[:opt4_m.end()].strip()
                following_text = chunk[opt4_m.end():].strip()
            else:
                q_opts_block = chunk.strip()
                following_text = ""
                
            q_text, opts = extract_options(q_opts_block)
            
            # If this is Dokkai and following_text has a new passage, update current_dokkai_passage
            if sec_num >= 10 and following_text:
                cleaned_next = clean_passage(following_text)
                if len(cleaned_next) > 30:
                    current_dokkai_passage = cleaned_next
        else:
            q_text = f"Câu hỏi {q}"
            opts = ["1", "2", "3", "4"]

        # Clean q_text: remove leading question number and artifacts
        q_text = re.sub(r'^\s*[\d１-９]{1,2}[a-z。、.\s\(\)（）]*', '', q_text).strip()
        q_text = clean_furigana(q_text)
        opts = [clean_furigana(opt) for opt in opts]
        if len(opts) < 4:
            opts = opts + [f"Phương án {j+1}" for j in range(len(opts), 4)]

        # Specific section styling
        passage_str = ""
        if sec_num == 1:
            q_text = underline_m1(q_text, opts)
        elif sec_num == 2:
            q_text = underline_m2(q_text, opts)
        elif sec_num == 5:
            q_text = underline_m5(q_text, opts)
        elif sec_num == 6:
            # Enclose word in 【word】
            if not q_text.startswith('【'):
                word_clean = q_text.replace('【','').replace('】','').strip()
                if len(word_clean) < 15:
                    q_text = f"【{word_clean}】"
        elif sec_num == 8:
            if '★' not in q_text:
                q_text += " ＿＿ ＿＿ ＿★＿ ＿＿"
            else:
                # Standardize 4 blanks with star
                q_text = re.sub(r'[_＿]{2,}\s*[_＿]{2,}\s*[_＿]*★[_＿]*\s*[_＿]{2,}', '＿＿ ＿＿ ＿★＿ ＿＿', q_text)
        elif sec_num == 9:
            passage_str = m9_passage
            if f"【{q}】" not in q_text and f"({q})" not in q_text and f"（{q}）" not in q_text:
                q_text = f"【{q}】に入る最も適当なものはどれか。"
        elif sec_num >= 10:
            if sec_num == 14 and m14_passage:
                passage_str = m14_passage
            else:
                passage_str = current_dokkai_passage

        ans_val = answers.get(q, 1) # 1..4
        ans_idx = max(0, min(3, ans_val - 1))
        correct_text = opts[ans_idx] if len(opts) > ans_idx else f"Phương án {ans_val}"

        q_item = {
            "id": f"n2-{year}{month:02d}-q{q:02d}",
            "number": q,
            "sectionGroup": "vocab_grammar" if sec_num <= 9 else "reading",
            "section": SEC_NAMES.get(sec_num, f"問題 {sec_num}"),
            "instruction": SEC_INSTRUCTIONS.get(sec_num, ""),
            "question": q_text,
            "options": opts[:4],
            "answer": ans_idx,
            "explanation": f"【正解】{ans_val} ({correct_text})\n\n• Giải thích kiến thức và ngữ cảnh câu {q} trong đề thi JLPT N2 {month:02d}/{year}."
        }
        if passage_str:
            q_item["passage"] = passage_str

        questions.append(q_item)

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
            "reading": 70,
            "full": 105
        },
        "questions": questions
    }
    return exam_json

# 3. BATCH PROCESS ALL 31 EXAMS
folders = sorted([d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))])
print(f"\nProcessing {len(folders)} folders...")

all_exams_meta = []
GOLDEN_TEMPLATES = {"2023_12", "2025_07"}

for folder in folders:
    m_ym = re.search(r'(\d{1,2})[-/.](\d{4})|(\d{4})[-/.](\d{1,2})', folder)
    if not m_ym:
        continue
    if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
        month, year = int(m_ym.group(1)), int(m_ym.group(2))
    else:
        year, month = int(m_ym.group(3)), int(m_ym.group(4))

    key = f"{year}_{month:02d}"
    out_name = f"{year}_{month:02d}.json"
    legacy_name = f"n2_{year}_{month:02d}.json"
    
    # 3.1 If golden template, load existing and preserve
    if key in GOLDEN_TEMPLATES:
        template_file = os.path.join(DATA_DIR, out_name)
        with open(template_file, 'r', encoding='utf-8') as f_gold:
            gold_data = json.load(f_gold)
        
        # Save to public directory as well
        with open(os.path.join(PUBLIC_DATA_DIR, out_name), 'w', encoding='utf-8') as f_out:
            json.dump(gold_data, f_out, ensure_ascii=False, indent=2)
        with open(os.path.join(PUBLIC_DATA_DIR, legacy_name), 'w', encoding='utf-8') as f_out:
            json.dump(gold_data, f_out, ensure_ascii=False, indent=2)
            
        print(f"[PRESERVED GOLDEN] {key}: {len(gold_data['questions'])} questions preserved.")
        
        meta_entry = {
            "id": gold_data.get("id", f"n2-{year}-{month:02d}"),
            "level": "N2",
            "year": year,
            "month": month,
            "title": gold_data.get("title", f"JLPT N2 - {month:02d}/{year}"),
            "theme": gold_data.get("theme", f"Đề thi chính thức {month:02d}/{year}"),
            "description": gold_data.get("description", f"Đề thi chính thức kỳ thi JLPT N2 tháng {month:02d}/{year}."),
            "file": f"data/n2_exams/{out_name}",
            "available": True,
            "totalQuestions": gold_data["totalQuestions"],
            "vocabGrammarCount": gold_data.get("vocabGrammarCount", 51),
            "readingCount": gold_data.get("readingCount", 20),
            "listeningCount": gold_data.get("listeningCount", 30 if gold_data.get("hasAudio") else 0),
            "hasAudio": gold_data.get("hasAudio", False),
            "durations": gold_data.get("durations", {"vocab_grammar": 35, "reading": 70, "full": 105})
        }
        if gold_data.get("audio"):
            meta_entry["audio"] = gold_data["audio"]
            meta_entry["hasAudio"] = True
        all_exams_meta.append(meta_entry)
        continue

    # 3.2 Process remaining exams
    folder_path = os.path.join(SOURCE_DIR, folder)
    files = os.listdir(folder_path)
    exam_pdfs = [f for f in files if f.endswith('.pdf') and 'script' not in f.lower()]
    if not exam_pdfs:
        print(f"Warning: No exam pdf in {folder}")
        continue
        
    pdf_path = os.path.join(folder_path, exam_pdfs[0])
    answers = answer_db.get(key, {})
    if not answers:
        print(f"Warning: No answers found for {key}")
        continue
        
    print(f"-> Processing {key} ({len(answers)} questions from {exam_pdfs[0]})...")
    exam_data = process_single_exam(pdf_path, year, month, answers)
    
    # Save to data/n2_exams/
    with open(os.path.join(DATA_DIR, out_name), 'w', encoding='utf-8') as f_out:
        json.dump(exam_data, f_out, ensure_ascii=False, indent=2)
    with open(os.path.join(DATA_DIR, legacy_name), 'w', encoding='utf-8') as f_out:
        json.dump(exam_data, f_out, ensure_ascii=False, indent=2)

    # Save to public/data/n2_exams/
    with open(os.path.join(PUBLIC_DATA_DIR, out_name), 'w', encoding='utf-8') as f_out:
        json.dump(exam_data, f_out, ensure_ascii=False, indent=2)
    with open(os.path.join(PUBLIC_DATA_DIR, legacy_name), 'w', encoding='utf-8') as f_out:
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

# 4. SAVE UPDATED REGISTRY TO ALL TARGET LOCATIONS
target_index_paths = [
    os.path.join(ROOT_DIR, 'data', 'n2-index.json'),
    os.path.join(DATA_DIR, 'n2-index.json'),
    os.path.join(ROOT_DIR, 'public', 'data', 'n2-index.json'),
    os.path.join(PUBLIC_DATA_DIR, 'n2-index.json'),
]

for idx_path in target_index_paths:
    with open(idx_path, 'w', encoding='utf-8') as f_idx:
        json.dump(all_exams_meta, f_idx, ensure_ascii=False, indent=2)

print(f"\n=======================================================")
print(f"BATCH CONVERSION COMPLETE!")
print(f"Successfully processed and unlocked all {len(all_exams_meta)} exams!")
print(f"=======================================================")
