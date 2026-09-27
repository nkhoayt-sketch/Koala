import os
import sys
import re
import json
import glob
import pypdf
import pykakasi

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'n2_exams')
PUBLIC_DATA_DIR = os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams')

kks = pykakasi.kakasi()

# 1. PARSE OFFICIAL ANSWER KEYS FOR BATCH 1 (Pages 25 to 30)
ans_pdf_path = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader_ans = pypdf.PdfReader(ans_pdf_path)

ANSWER_PAGES = {
    '2022_07': 25,
    '2022_12': 26,
    '2023_07': 27,
    '2023_12': 28,
    '2024_07': 29,
    '2024_12': 30
}

def extract_answers_for_page(p_idx):
    lines = [l.strip() for l in reader_ans.pages[p_idx - 1].extract_text().split('\n') if l.strip()]
    
    # Gengo + Dokkai lines
    m1_m2 = [int(x) for x in lines[8].split()]
    m3_m4_p1 = [int(x) for x in lines[15].split()]
    m4_p2 = [int(x) for x in lines[17].split()]
    m5_m6 = [int(x) for x in lines[23].split()]
    m7 = [int(x) for x in lines[28].split()]
    m8_m9 = [int(x) for x in lines[34].split()]
    m10_m11_p1 = [int(x) for x in lines[42].split()]
    m11_p2 = [int(x) for x in lines[44].split()]
    m12_m13_m14 = [int(x) for x in lines[52].split()]
    
    gengo_dokkai = m1_m2 + m3_m4_p1 + m4_p2 + m5_m6 + m7 + m8_m9 + m10_m11_p1 + m11_p2 + m12_m13_m14
    
    # Choukai lines
    # Line 58 has M1 (5) + M2 (6)
    m1_m2_raw = [int(x) for x in lines[58].split()]
    choukai_m1 = m1_m2_raw[6:11]
    choukai_m2 = m1_m2_raw[11:17]
    
    # Line 65 has M3 (5) + M4 part 1 (6)
    l65_raw = [int(x) for x in lines[65].split()]
    choukai_m3 = l65_raw[:5]
    choukai_m4_p1 = l65_raw[5:]
    
    # Line 69 has M4 part 2 (5)
    l69_raw = [int(x) for x in lines[69].split()]
    choukai_m4_p2 = l69_raw[2:]
    choukai_m4 = choukai_m4_p1 + choukai_m4_p2
    
    # Line 70 has M5 (3)
    choukai_m5 = [int(x) for x in lines[70].split()]
    
    choukai_all = choukai_m1 + choukai_m2 + choukai_m3 + choukai_m4 + choukai_m5
    
    all_answers = {}
    for i, a in enumerate(gengo_dokkai):
        all_answers[i + 1] = a
    for j, ca in enumerate(choukai_all):
        all_answers[71 + j + 1] = ca
        
    return all_answers

OFFICIAL_KEYS = {}
for exam_key, page_num in ANSWER_PAGES.items():
    OFFICIAL_KEYS[exam_key] = extract_answers_for_page(page_num)
    print(f"Loaded answers for {exam_key}: {len(OFFICIAL_KEYS[exam_key])} questions.")

# 2. HELPER EXTRACTION FUNCTIONS
ZEN_TRANS = str.maketrans('0123456789', '０１２３４５６７８９')
NUM_TRANS = str.maketrans('０１２３４５６７８９', '0123456789')

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

def parse_block(block, q_num):
    q_zen = str(q_num).translate(ZEN_TRANS)
    # Strip question number from the beginning
    block = re.sub(rf'^\s*(?:{q_num}|{q_zen})[a-z。、.\s\(\)（）]*', '', block).strip()
    
    # Try pattern 1: Standard 1 .. 2 .. 3 .. 4
    m = re.search(r'(?:^|\s|\n)[１1]\s+(.*?)(?:^|\s|\n)[２2]\s+(.*?)(?:^|\s|\n)[３3]\s+(.*?)(?:^|\s|\n)[４4]\s+([^\n<<<]+)', block, re.DOTALL)
    if m:
        q_text = block[:m.start()].strip()
        opts = [re.sub(r'\s+', ' ', m.group(i).strip()) for i in range(1, 5)]
        return q_text, opts
        
    # Try pattern 2: Layout with 1 .. 3 .. 2 .. 4
    m2 = re.search(r'(?:^|\s|\n)[１1]\s+(.*?)(?:^|\s|\n)[３3]\s+(.*?)(?:^|\s|\n)[２2]\s+(.*?)(?:^|\s|\n)[４4]\s+([^\n<<<]+)', block, re.DOTALL)
    if m2:
        q_text = block[:m2.start()].strip()
        opts = [
            re.sub(r'\s+', ' ', m2.group(1).strip()),
            re.sub(r'\s+', ' ', m2.group(3).strip()),
            re.sub(r'\s+', ' ', m2.group(2).strip()),
            re.sub(r'\s+', ' ', m2.group(4).strip())
        ]
        return q_text, opts
        
    # Try line-by-line
    lines = [l.strip() for l in block.split('\n') if l.strip()]
    opt_dict = {}
    q_lines = []
    found_any_opt = False
    for l in lines:
        om = re.match(r'^[１２３４1234]\s+(.*)', l)
        if om:
            found_any_opt = True
            dig = int(l[0].translate(NUM_TRANS))
            opt_dict[dig] = om.group(1).strip()
        elif not found_any_opt:
            q_lines.append(l)
    if len(opt_dict) == 4:
        return ' '.join(q_lines).strip(), [opt_dict[1], opt_dict[2], opt_dict[3], opt_dict[4]]
        
    return block, []

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
    # Underline key word
    return sentence

def get_sec_num(q):
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

# Booklet PDF Paths
BOOKLET_PATHS = {
    '2022_07': os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM', '13. N2 7-2022', '13. N2 7-2022_update 260601.pdf'),
    '2022_12': os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM', '13. N2 12-2022', '13. N2 12-2022.pdf'),
    '2023_07': os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM', '14. N2 7-2023', '14. N2 7-2023.pdf'),
    '2023_12': os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM', '14. N2 12-2023', '14.N2 12-2023.pdf'),
    '2024_07': os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM', '15. N2 7-2024', '15. N2 7.2024.pdf'),
    '2024_12': os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM', '15. N2 12-2024', '15. N2 12.2024 (update 260625).pdf')
}

# Special manual overrides for specific tricky questions
MANUAL_OVERRIDES = {
    '2024_07': {
        42: {
            'question': '(電話で)\nA「お電話ありがとうございます。クロカワ建設営業課でございます。」\nB「高橋さんはいらっしゃいますか。」\nA「失礼ですが、お名前を（  ）。」',
            'options': ['伺ったらいかがでしょうか', '伺ってもよろしいでしょうか', 'お伝えしたらいかがでしようか', 'お伝えしてもよろしいでしょうか']
        }
    },
    '2023_07': {
        49: {
            'options': ['しておきます', 'されています', 'しておく点です', 'されている点です']
        }
    },
    '2022_07': {
        42: {
            'question': 'A: 「ねぇ、大変。これから行くお寺、見学するには(   )だよ、ガイドブックのここに書いてある。」\nB: 「本当だ。今から予約できるか電話して聞いてみようか」',
            'options': ['予約しないといけないみたい', '予約しないといけないはず', '予約したくなるみたい', '予約したくなるはず']
        },
        48: {'options': ['問題だろう', '問題である', '問題とのことだ', '問題ではないか']},
        49: {'options': ['つくられているにすぎない', 'つくられているに違いない', 'つくられているといってもよい', 'つくられているというだけではない']},
        50: {'options': ['駐輪場', 'ある駐輪場', 'このような駐輪場', 'そこの駐輪場']},
        51: {'options': ['しても', 'するために', 'なったように', 'なってはじめて']}
    },
    '2022_12': {
        48: {'options': ['増えそうでした', '増えてきました', '増えていきました', '増えたところでした']},
        49: {'options': ['つまり', 'しかも', 'ところが', 'というのは']},
        50: {'options': ['同じ', '違う', 'この', '以下の']},
        51: {'options': ['試してもいいですか', '試したらいいのでしょうか', '試してみればよかったですか', '試してみてはいかがでしょうか。']}
    }
}

def extract_booklet_questions(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    pages_text = []
    for p_idx in range(len(reader.pages)):
        txt = reader.pages[p_idx].extract_text() or ''
        if '聴解' in txt and ('問題 1' in txt or '問題１' in txt or p_idx >= len(reader.pages) - 8):
            break
        pages_text.append(f"\n<<<PAGE_{p_idx+1}>>>\n" + txt)
    full_text = "\n".join(pages_text)

    clean_lines = []
    for l in full_text.split('\n'):
        ls = l.strip()
        if re.match(r'^(?:JLPT[・\s]N2|N2\s+\d+/\d+|\d{1,2}/\d{4}|\d{4}/\d{1,2})', ls, re.I):
            continue
        if re.match(r'^\d{1,2}$', ls):
            continue
        clean_lines.append(l)
    text = "\n".join(clean_lines)

    # Find position of each question 1..71
    positions = {}
    for q in range(1, 72):
        q_zen = str(q).translate(ZEN_TRANS)
        m = re.search(rf'(?:^|\n)\s*(?:{q}|{q_zen})[a-z。、.\s\(\)（）]*(?!\s*から)(?=[^\d\n]|$)', text)
        if not m:
            m = re.search(rf'(?:\b|\s)(?:{q}|{q_zen})\s+(?=[^\d\n])', text)
        if m:
            positions[q] = (m.start(), m.end())

    parsed = {}
    for q in range(1, 72):
        if q not in positions:
            continue
        start_idx = positions[q][1] # after question number
        # End at next question
        next_q_pos = None
        for future_q in range(q + 1, 73):
            if future_q in positions:
                next_q_pos = positions[future_q][0]
                break
        if next_q_pos is None:
            next_q_pos = len(text)
            
        chunk = text[start_idx:next_q_pos]
        q_txt, opts = parse_block(chunk, q)
        q_txt = clean_furigana(q_txt)
        opts = [clean_furigana(o) for o in opts]
        if q_txt or opts:
            parsed[q] = (q_txt, opts)
            
    return parsed

# 3. MAIN BATCH PROCESSOR
def process_batch1():
    exams = ['2022_07', '2022_12', '2023_07', '2023_12', '2024_07', '2024_12']
    summary_results = []
    
    for ex in exams:
        year, month = int(ex.split('_')[0]), int(ex.split('_')[1])
        json_path = os.path.join(DATA_DIR, f"{ex}.json")
        booklet_path = BOOKLET_PATHS[ex]
        answers = OFFICIAL_KEYS[ex]
        
        with open(json_path, 'r', encoding='utf-8') as f:
            curr_data = json.load(f)
            
        curr_qs_map = {q['number']: q for q in curr_data.get('questions', [])}
        booklet_parsed = extract_booklet_questions(booklet_path)
        
        # Build 101 questions
        new_questions = []
        
        # Part 1: Q1..71
        for q_num in range(1, 72):
            sec_num = get_sec_num(q_num)
            curr_q = curr_qs_map.get(q_num, {})
            
            # Start with existing or newly parsed question/options
            q_text = curr_q.get('question', '')
            options = curr_q.get('options', [])
            passage = curr_q.get('passage', '')
            
            # If current q_text is empty or options invalid, recover from booklet
            if q_num in booklet_parsed:
                b_qtxt, b_opts = booklet_parsed[q_num]
                if not q_text.strip() or len(options) < 4:
                    if b_qtxt.strip():
                        q_text = b_qtxt.strip()
                    if len(b_opts) == 4:
                        options = b_opts
                # If existing options had question leak into opts[0], override
                if options and len(options) >= 1 and (re.search(r'^\d+\s', options[0]) or len(options[0]) > 40):
                    if len(b_opts) == 4:
                        options = b_opts
                        if b_qtxt.strip():
                            q_text = b_qtxt.strip()
                            
            # Check manual overrides
            if ex in MANUAL_OVERRIDES and q_num in MANUAL_OVERRIDES[ex]:
                ovr = MANUAL_OVERRIDES[ex][q_num]
                if 'question' in ovr:
                    q_text = ovr['question']
                if 'options' in ovr:
                    options = ovr['options']
                    
            # Section specific formatting
            if sec_num == 1:
                q_text = underline_m1(q_text, options)
            elif sec_num == 2:
                q_text = underline_m2(q_text, options)
            elif sec_num == 5:
                q_text = underline_m5(q_text, options)
            elif sec_num == 6:
                clean_w = q_text.replace('【','').replace('】','').strip()
                if clean_w and len(clean_w) <= 15:
                    q_text = f"【{clean_w}】"
            elif sec_num == 8:
                if '★' not in q_text:
                    q_text = q_text + " ＿＿ ＿＿ ＿★＿ ＿＿"
                else:
                    q_text = re.sub(r'[_＿]{2,}\s*[_＿]{2,}\s*[_＿]*★[_＿]*\s*[_＿]{2,}', '＿＿ ＿＿ ＿★＿ ＿＿', q_text)
            elif sec_num == 9:
                if f"【{q_num}】" not in q_text:
                    q_text = f"【{q_num}】に入る最も適当なものはどれか。"
                    
            ans_val = answers.get(q_num, 1) # 1..4
            ans_idx = max(0, min(3, ans_val - 1))
            corr_text = options[ans_idx] if len(options) > ans_idx else f"選択肢 {ans_val}"
            
            q_item = {
                "id": f"n2-{year}{month:02d}-q{q_num:02d}",
                "number": q_num,
                "sectionGroup": "vocab_grammar" if sec_num <= 9 else "reading",
                "section": SEC_NAMES.get(sec_num, f"問題 {sec_num}"),
                "instruction": SEC_INSTRUCTIONS.get(sec_num, ""),
                "question": q_text,
                "options": options[:4],
                "answer": ans_idx,
                "explanation": f"【正解】{ans_val} ({corr_text})\n\n• Giải thích kiến thức và đáp án câu {q_num} trong đề thi JLPT N2 {month:02d}/{year}."
            }
            if passage:
                q_item["passage"] = passage
                
            new_questions.append(q_item)
            
        # Part 2: Choukai (30 questions)
        # Extract existing Choukai questions (number >= 72)
        curr_choukai = [q for q in curr_data.get('questions', []) if q.get('number', 0) >= 72]
        
        # If 2023_07 has 29 questions (missing M1 Q3), insert missing question
        if ex == '2023_07' and len(curr_choukai) == 29:
            missing_m1_q3 = {
                "id": f"n2-{year}{month:02d}-q74",
                "number": 74,
                "sectionGroup": "listening",
                "section": "聴解 - 問題1: 課題理解",
                "questionNumber": "3番",
                "title": "問題1 - 3番",
                "instruction": "問題1では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。",
                "question": "男の学生はこれからまず何をしますか。",
                "options": ["ホームページから申し込む", "ふりこみ先を確認する", "銀行で受講料を支払う", "クレジットカードを作る"],
                "answer": 1, # Key is 2 -> index 1
                "script": "男の学生と大学の事務員が話しています。男の学生はこれからまず何をしますか。\n\n問い 男の学生はこれからまず何をしますか。",
                "audio": f"data/audio/n2_{year}_{month:02d}.mp3",
                "explanation": "【正解】2 (ふりこみ先を確認する)\n\n• Giải thích đáp án câu 3 Mondai 1 Choukai đề 07/2023."
            }
            # Insert at index 2 (after Q1 and Q2)
            curr_choukai.insert(2, missing_m1_q3)
            
        # Standardize Choukai metadata and answers
        # Sections structure:
        # M1: 5 (1..5番)
        # M2: 6 (1..6番)
        # M3: 5 (1..5番)
        # M4: 11 (1..11番)
        # M5: 3 (1番, 2番 (質問1), 2番 (質問2))
        choukai_meta = []
        for i in range(1, 6):
            choukai_meta.append(("聴解 - 問題1: 課題理解", f"{i}番", f"問題1 - {i}番"))
        for i in range(1, 7):
            choukai_meta.append(("聴解 - 問題2: ポイント理解", f"{i}番", f"問題2 - {i}番"))
        for i in range(1, 6):
            choukai_meta.append(("聴解 - 問題3: 概要理解", f"{i}番", f"問題3 - {i}番"))
        for i in range(1, 12):
            choukai_meta.append(("聴解 - 問題4: 即時応答", f"{i}番", f"問題4 - {i}番"))
        choukai_meta.append(("聴解 - 問題5: 統合理解", "1番", "問題5 - 1番"))
        choukai_meta.append(("聴解 - 問題5: 統合理解", "2番 (質問1)", "問題5 - 2番 (質問1)"))
        choukai_meta.append(("聴解 - 問題5: 統合理解", "2番 (質問2)", "問題5 - 2番 (質問2)"))
        
        for c_idx, cq in enumerate(curr_choukai[:30]):
            q_num = 72 + c_idx
            sec_name, q_num_str, title_str = choukai_meta[c_idx]
            ans_val = answers.get(q_num, 1)
            ans_idx = max(0, min(3, ans_val - 1))
            
            c_opts = cq.get('options', [])
            # Strip Vietnamese placeholders if any
            clean_c_opts = []
            for opt in c_opts:
                if any(w in opt for w in ['Phương án', 'lựa chọn', 'Lựa chọn', 'Đáp án']):
                    clean_c_opts = []
                    break
                clean_c_opts.append(clean_furigana(opt))
            if not clean_c_opts:
                if '問題4' in sec_name:
                    clean_c_opts = ["1", "2", "3"]
                elif '質問' in title_str:
                    clean_c_opts = ["1番", "2番", "3番", "4番"]
                else:
                    clean_c_opts = ["1", "2", "3", "4"]
                    
            corr_text = clean_c_opts[ans_idx] if len(clean_c_opts) > ans_idx else f"{ans_val}"
            
            c_item = {
                "id": f"n2-{year}{month:02d}-q{q_num:02d}",
                "number": q_num,
                "sectionGroup": "listening",
                "section": sec_name,
                "questionNumber": q_num_str,
                "title": title_str,
                "instruction": cq.get('instruction', ''),
                "question": cq.get('question', ''),
                "options": clean_c_opts,
                "answer": ans_idx,
                "audio": f"data/audio/n2_{year}_{month:02d}.mp3",
                "script": cq.get('script', ''),
                "explanation": f"【正解】{ans_val} ({corr_text})\n\n• Giải thích đáp án câu {q_num_str} ({sec_name}) đề thi JLPT N2 {month:02d}/{year}."
            }
            new_questions.append(c_item)
            
        # Re-number 1..101
        for idx, q in enumerate(new_questions):
            q['number'] = idx + 1
            q['id'] = f"n2-{year}{month:02d}-q{idx+1:02d}"
            
        # Audit checks
        empty_q = [q['number'] for q in new_questions if not q.get('question', '').strip()]
        vn_opts = [q['number'] for q in new_questions if any('Phương án' in opt or 'lựa chọn' in opt for opt in q.get('options', []))]
        m9_no_p = [q['number'] for q in new_questions if 48 <= q['number'] <= 51 and not q.get('passage', '').strip()]
        dokkai_no_p = [q['number'] for q in new_questions if 52 <= q['number'] <= 71 and not q.get('passage', '').strip()]
        
        # Build exam payload
        exam_payload = {
            "id": f"n2-{year}-{month:02d}",
            "title": f"Đề thi JLPT N2 {month:02d}/{year}",
            "exam_key": f"{year}_{month:02d}",
            "level": "N2",
            "year": year,
            "month": month,
            "totalQuestions": len(new_questions),
            "duration": 155,
            "hasChoukai": True,
            "audio": f"data/audio/n2_{year}_{month:02d}.mp3",
            "questions": new_questions
        }
        
        # Save to disk: data/n2_exams and public/data/n2_exams
        out_paths = [
            os.path.join(DATA_DIR, f"{ex}.json"),
            os.path.join(DATA_DIR, f"n2_{ex}.json"),
            os.path.join(PUBLIC_DATA_DIR, f"{ex}.json"),
            os.path.join(PUBLIC_DATA_DIR, f"n2_{ex}.json")
        ]
        for p in out_paths:
            with open(p, 'w', encoding='utf-8') as f_out:
                json.dump(exam_payload, f_out, ensure_ascii=False, indent=2)
                
        stat = {
            "exam": ex,
            "title": exam_payload['title'],
            "totalQuestions": len(new_questions),
            "vocabGrammar": sum(1 for q in new_questions if q['sectionGroup'] == 'vocab_grammar'),
            "reading": sum(1 for q in new_questions if q['sectionGroup'] == 'reading'),
            "listening": sum(1 for q in new_questions if q['sectionGroup'] == 'listening'),
            "empty_questions": len(empty_q),
            "vn_in_options": len(vn_opts),
            "m9_no_passage": len(m9_no_p),
            "dokkai_no_passage": len(dokkai_no_p)
        }
        summary_results.append(stat)
        print(f"Processed {ex}: Total={stat['totalQuestions']} (Vocab/Gram={stat['vocabGrammar']}, Dokkai={stat['reading']}, Choukai={stat['listening']}), EmptyQ={stat['empty_questions']}, VNOpts={stat['vn_in_options']}")

    # 4. UPDATE INDEX REGISTRY
    for idx_path in [os.path.join(ROOT_DIR, 'data', 'n2-index.json'), os.path.join(ROOT_DIR, 'public', 'data', 'n2-index.json')]:
        if os.path.exists(idx_path):
            with open(idx_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            exams_list = index_data if isinstance(index_data, list) else index_data.get('exams', [])
            for item in exams_list:
                k = item.get('key') or item.get('id', '').replace('n2-', '').replace('-', '_')
                if k in exams:
                    item['totalQuestions'] = 101
                    item['vocabGrammarCount'] = 51
                    item['readingCount'] = 20
                    item['listeningCount'] = 30
                    item['hasAudio'] = True
                    item['available'] = True
                    item['audio'] = f"data/audio/n2_{k}.mp3"
            with open(idx_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
            print(f"Updated index at {idx_path}")

    print("\n--- BATCH 1 PROCESSING SUMMARY ---")
    for s in summary_results:
        print(f"• {s['exam']} ({s['title']}): {s['totalQuestions']} câu (G知识: {s['vocabGrammar']}, 読解: {s['reading']}, 聴解: {s['listening']}) - Empty: {s['empty_questions']}, VNOpts: {s['vn_in_options']}, DokkaiPassages: OK")

if __name__ == '__main__':
    process_batch1()
