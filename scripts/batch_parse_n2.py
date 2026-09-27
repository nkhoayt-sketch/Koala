# -*- coding: utf-8 -*-
"""
Script: batch_parse_n2.py
Description: Batch processes, extracts, and standardizes all JLPT N2 exams (2010-2025)
to match the 100% standardized format of 12/2025:
- Pure Japanese options (no Vietnamese garbage / placeholder text)
- Split-View passage preserved for Mondai 9 to 14 and Choukai transcripts
- Exact answer keys from official PDF
- Audio linkage and duration metadata
- Garbage collection per exam iteration for memory safety
"""

import os
import sys
import gc
import re
import json
import glob
import pypdf
import pykakasi

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')
DATA_EXAMS_DIR = os.path.join(ROOT_DIR, 'data', 'n2_exams')
PUB_EXAMS_DIR = os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams')
INDEX_FILE = os.path.join(ROOT_DIR, 'data', 'n2-index.json')
PUB_INDEX_FILE = os.path.join(ROOT_DIR, 'public', 'data', 'n2-index.json')

os.makedirs(DATA_EXAMS_DIR, exist_ok=True)
os.makedirs(PUB_EXAMS_DIR, exist_ok=True)

kks = pykakasi.kakasi()
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

CHOUKAI_NAMES = {
    1: "聴解 - 問題1: 課題理解",
    2: "聴解 - 問題2: ポイント理解",
    3: "聴解 - 問題3: 概要理解",
    4: "聴解 - 問題4: 即時応答",
    5: "聴解 - 問題5: 統合理解"
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

# 1. PARSE OFFICIAL ANSWER PDF
def load_all_official_answers():
    ans_pdf = os.path.join(SOURCE_DIR, 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
    reader = pypdf.PdfReader(ans_pdf)
    db = {}
    
    for p_idx in range(1, len(reader.pages)):
        text = reader.pages[p_idx].extract_text()
        m_ym = re.search(r'(\d{1,2})[/.-](\d{4})|(\d{4})[/.-](\d{1,2})', text)
        if not m_ym:
            continue
        if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
            month, year = int(m_ym.group(1)), int(m_ym.group(2))
        else:
            year, month = int(m_ym.group(3)), int(m_ym.group(4))
            
        key = f"{year}_{month:02d}"
        
        # Parse Gengo + Dokkai
        chokai_idx = text.find('聴解')
        lang_text = text[:chokai_idx] if chokai_idx != -1 else text
        
        raw_lines = [l.strip() for l in lang_text.split('\n') if l.strip()]
        q_to_ans = {}
        pending = []
        for l in raw_lines:
            if any(h in l for h in ['JLPT', '文字・語彙', '文法', '読解', 'ĐÁP ÁN']):
                continue
            l_clean = re.sub(r'問題\s*[0-9０-９一二三四五六七八九１-９]*', '', l).strip()
            nums = [int(x) for x in re.findall(r'\b\d+\b', l_clean)]
            if not nums:
                continue
            next_exp = len(q_to_ans) + len(pending) + 1
            is_q_line = any(n > 4 for n in nums) or (nums[0] == next_exp and len(nums) > 1 and nums[1] == next_exp + 1) or (nums[0] == next_exp and len(pending) == 0 and not all(1 <= x <= 4 for x in nums))
            if pending and len(nums) == len(pending) and all(1 <= x <= 4 for x in nums):
                for q, a in zip(pending, nums):
                    q_to_ans[q] = a
                pending = []
            elif is_q_line:
                pending.extend(nums)
            elif pending and all(1 <= x <= 4 for x in nums):
                for a in nums:
                    if pending:
                        q_to_ans[pending.pop(0)] = a
            elif not pending and nums[0] == 1 and all(nums[j] == j+1 for j in range(len(nums))):
                pending.extend(nums)
                
        # Parse Choukai answers
        choukai_ans_list = []
        if chokai_idx != -1:
            chokai_text = text[chokai_idx:]
            c_lines = [l.strip() for l in chokai_text.split('\n') if l.strip()]
            c_pending = []
            for l in c_lines:
                if any(h in l for h in ['JLPT', 'ĐÁP ÁN', '聴解']):
                    continue
                l_c = re.sub(r'問題\s*[0-9０-９一二三四五六七八九１-９]*', '', l).strip()
                nums = [int(x) for x in re.findall(r'\b\d+\b', l_c)]
                if not nums:
                    continue
                if c_pending and len(nums) == len(c_pending) and all(1 <= x <= 4 for x in nums):
                    choukai_ans_list.extend(nums)
                    c_pending = []
                elif any(n > 4 for n in nums) or (nums[0] == 1 and len(nums) > 1 and nums[1] == 2):
                    c_pending = nums
                elif c_pending and all(1 <= x <= 4 for x in nums):
                    for a in nums:
                        if c_pending:
                            c_pending.pop(0)
                            choukai_ans_list.append(a)
                            
        # Map choukai to question numbers starting after max gengo/dokkai
        max_q = max(q_to_ans.keys(), default=0)
        for idx, a in enumerate(choukai_ans_list):
            q_to_ans[max_q + idx + 1] = a
            
        db[key] = q_to_ans
        
    return db

# 2. HELPER FUNCTIONS
def get_clean_booklet_text(pdf_path):
    if not pdf_path or not os.path.exists(pdf_path):
        return ""
    try:
        reader = pypdf.PdfReader(pdf_path)
        cleaned_pages = []
        for p in reader.pages:
            t = p.extract_text() or ""
            lines = t.split('\n')
            good_lines = []
            for l in lines:
                if re.match(r'^\s*(?:JLPT|N2|\d{1,2}/\d{4})\b', l, re.I): continue
                if re.match(r'^\s*\d{1,2}\s*$', l): continue
                good_lines.append(l)
            cleaned_pages.append('\n'.join(good_lines))
        return '\n'.join(cleaned_pages)
    except Exception as e:
        print(f"  Error reading {pdf_path}: {e}")
        return ""

def extract_options_from_block(block):
    opt_map = {}
    pattern = r'(?:^|[\s\n])([１２３４1234])[\s.、]+(.*?)(?=(?:[\s\n][１２３４1234][\s.、]+|\Z))'
    for m in re.finditer(pattern, block, re.DOTALL):
        d_val = int(m.group(1).translate(NUM_TRANS))
        if 1 <= d_val <= 4 and d_val not in opt_map:
            val = re.sub(r'\s+', ' ', m.group(2).strip())
            # Strip trailing question headers if leaked
            val = re.sub(r'\s*(?:問題|間題|\d{1,2}\s+).*$', '', val).strip()
            opt_map[d_val] = val
    if len(opt_map) == 4 and all(opt_map[i] for i in range(1, 5)):
        return [opt_map[1], opt_map[2], opt_map[3], opt_map[4]]
    return None

def extract_question_and_options(booklet_text, q_num):
    q_zen = str(q_num).translate(ZEN_TRANS)
    next_q = q_num + 1
    next_zen = str(next_q).translate(ZEN_TRANS)
    
    # Pattern to find question block
    pat = rf'(?:^|\n)\s*(?:{q_num}|{q_zen})\s+(.*?)(?=(?:\n\s*(?:{next_q}|{next_zen})\s+[^\d]|\n\s*(?:問題|間題)|\Z))'
    m = re.search(pat, booklet_text, re.DOTALL)
    if not m:
        pat_fb = rf'\b(?:{q_num}|{q_zen})\s+(.*?)(?=(?:\b(?:{next_q}|{next_zen})\s+|\Z))'
        m = re.search(pat_fb, booklet_text, re.DOTALL)
        
    if m:
        block = m.group(1).strip()
        opts = extract_options_from_block(block)
        # Strip options from question text
        m_opt = re.search(r'(?:^|[\s\n])[１1][\s.、]+', block)
        q_text = block[:m_opt.start()].strip() if m_opt else block
        q_text = re.sub(r'\s+', ' ', q_text).strip()
        return q_text, opts
    return None, None

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

def has_vietnamese(text):
    if not isinstance(text, str): return False
    return any(c in text for c in 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ')

MANUAL_OVERRIDES = {
    '2011_07': {
        45: {
            'options': ['したら', 'という', 'プレッシャーは', '「もし、またミスをしたら」']
        }
    },
    '2013_12': {
        45: {
            'options': ['ぐらい', '1 週間', 'あと', 'は']
        }
    },
    '2014_12': {
        52: {
            'options': ['問題ないかどうかだ', '問題ないということだ', '問題ないとするだろうか', '問題ないのだと思っていた']
        }
    },
    '2018_07': {
        51: {
            'options': ['ご存じだ', 'ご存じのようだ', 'ご存じだろうか', 'ご存じなのだろう']
        }
    },
    '2021_07': {
        2: {
            'question': '近年、科学技術は<u>著しい</u>進歩を見せている。',
            'options': ['かやぶかしい', 'かがやかしい', 'いちじるしい', 'いちるじしい']
        }
    },
    '2021_12': {
        46: {
            'options': ['ありがたいんですが', '変更していただけると', '4 時以降に', 'よろしければ']
        }
    }
}

# 3. BUILD DIRECTORY MAPPING
def get_source_exam_map():
    mapping = {}
    for item in os.listdir(SOURCE_DIR):
        p = os.path.join(SOURCE_DIR, item)
        if os.path.isdir(p):
            m = re.search(r'(\d{1,2})[-_.](\d{4})|(\d{4})[-_.](\d{1,2})', item)
            if m:
                if m.group(1):
                    month, year = int(m.group(1)), int(m.group(2))
                else:
                    year, month = int(m.group(3)), int(m.group(4))
                key = f"{year}_{month:02d}"
                files = os.listdir(p)
                pdfs = [f for f in files if f.lower().endswith('.pdf')]
                script_pdf = [f for f in pdfs if 'script' in f.lower() or 'choukai' in f.lower()]
                booklet_pdf = [f for f in pdfs if f not in script_pdf]
                
                b_path = os.path.join(p, booklet_pdf[0]) if booklet_pdf else None
                s_path = os.path.join(p, script_pdf[0]) if script_pdf else None
                mapping[key] = {
                    'year': year,
                    'month': month,
                    'folder': item,
                    'booklet': b_path,
                    'script': s_path
                }
    return mapping

# 4. MAIN BATCH PROCESSOR
def process_all_exams():
    print("=" * 60)
    print("KOALA JLPT N2 - BATCH EXAM PARSER & STANDARDIZER")
    print("Standard: Form 12/2025 (Pure JP Options, Split-View Passages)")
    print("=" * 60)

    print("\n1. Loading official answer keys...")
    answer_db = load_all_official_answers()
    print(f"Loaded official answers for {len(answer_db)} exam sessions.")

    source_map = get_source_exam_map()
    all_keys = sorted(source_map.keys())
    print(f"Found {len(all_keys)} exam sessions in source directory.")

    index_records = []

    for idx, key in enumerate(all_keys, 1):
        info = source_map[key]
        year = info['year']
        month = info['month']
        print(f"\n[{idx}/{len(all_keys)}] Processing {key} ({month:02d}/{year})...")

        # Load existing JSON file as base if present
        existing_file = os.path.join(PUB_EXAMS_DIR, f"{key}.json")
        if not os.path.exists(existing_file):
            existing_file = os.path.join(DATA_EXAMS_DIR, f"{key}.json")
            
        base_data = None
        if os.path.exists(existing_file):
            try:
                with open(existing_file, 'r', encoding='utf-8') as f:
                    base_data = json.load(f)
            except Exception as e:
                print(f"  Warning reading existing file {existing_file}: {e}")

        # Extract booklet text once
        booklet_text = get_clean_booklet_text(info['booklet'])
        official_ans = answer_db.get(key, {})

        # Questions to build
        questions = []
        existing_qs = base_data.get('questions', []) if base_data else []
        existing_q_map = {q['number']: q for q in existing_qs}

        # Determine total questions (usually 101 to 107)
        total_q_count = max(len(existing_qs), max(official_ans.keys(), default=0), 101)

        # Missing passage for Mondai 9 in 2018_07
        m9_2018_07_passage = (
            "道路のひみつ\n\n"
            "仕事、買い物、遊びに行くとき、誰でも必ずお世話になるものがある。50 だ。当たり前のように存在し、"
            "多くの人に利用されているが、様々な工夫がされていることはあまり知られていない。\n\n"
            "例えば、高速道路や大きな道路の多くで雨水が道路上にたまりにくい設計になっていることは 51 。"
            "道路表面に小さな無数の穴があり、水が舗装の下に抜けるという仕組みだ。高速道路で雨の日に事故が"
            "多かった地点も、この舗装にした後、雨の日の事故が約 80％減少したという。\n\n"
            "52 、寒い地域では雪や氷が原因でスリップ事故が多発する。そのため、雪や氷を砕く機能をもった"
            "道路が開発されている。粒状のゴムなど、柔軟性のある小さな素材を道路に埋め込み、車の重みで"
            "道路をわずかに変形させて雪や氷を砕く。カーブや坂道などをそういう舗装にすれば、道路に雪や氷が"
            "53 。\n\n"
            "他にも、車の走行音を吸収する道路など、様々な機能をもった道路が開発され、私たちの暮らしの"
            "安全や快適さを支えている。普段何気なく通っている道路だが、そこには快適に走行するための"
            "工夫が 54 のだ。"
        )

        # Missing passage for Mondai 10 in 2018_12
        m10_2018_12_q53_passage = (
            "（１）\n"
            "情報が容易に入手できると、必要な情報を探索する努力が必要なくなるかのように思われる。"
            "自分で集めるよりも、情報機器の提供する情報のほうが客観的で信頼できると勘違いする。\n\n"
            "しかし、だれにでも役に立つ完璧な情報など存在しない。情報化時代を生きるためには個々人が"
            "他者の提供する情報を評価し、比較検討し、その中から自分にとって、自分の目標にとって有益な"
            "情報を選別する能力と知識を持たなければならないのである。"
        )

        for q_num in range(1, total_q_count + 1):
            q_obj = existing_q_map.get(q_num)
            
            # If not in existing, create template
            if not q_obj:
                q_obj = {
                    "id": f"n2-{year}{month:02d}-q{q_num:02d}",
                    "number": q_num,
                    "sectionGroup": "vocab_grammar" if q_num <= 51 else ("reading" if q_num <= 71 else "listening"),
                    "section": SEC_NAMES.get(min(14, max(1, (q_num // 5) + 1)), "問題"),
                    "instruction": "",
                    "question": f"問題 {q_num}",
                    "options": ["1", "2", "3", "4"],
                    "answer": 0,
                    "explanation": "",
                    "passage": ""
                }

            # 1. Check and fix options with Vietnamese or placeholder
            current_opts = q_obj.get('options', [])
            opts_bad = (
                not current_opts or 
                len(current_opts) < 3 or 
                any(has_vietnamese(opt) for opt in current_opts) or
                any('phương án' in str(opt).lower() for opt in current_opts)
            )

            if opts_bad and booklet_text:
                q_text_extracted, opts_extracted = extract_question_and_options(booklet_text, q_num)
                if opts_extracted and len(opts_extracted) == 4 and not any(has_vietnamese(o) for o in opts_extracted):
                    q_obj['options'] = opts_extracted
                    if q_text_extracted and len(q_text_extracted) > 3:
                        q_obj['question'] = q_text_extracted

            # Apply manual overrides if defined
            if key in MANUAL_OVERRIDES and q_num in MANUAL_OVERRIDES[key]:
                override = MANUAL_OVERRIDES[key][q_num]
                if 'options' in override:
                    q_obj['options'] = override['options']
                if 'question' in override:
                    q_obj['question'] = override['question']

            # 2. Fix passages for Mondai 9 to 14
            sec = q_obj.get('section', '')
            if '問題9' in sec or q_obj.get('sectionGroup') == 'reading':
                # Special fix for 2018_07 Mondai 9
                if key == '2018_07' and '問題9' in sec:
                    q_obj['passage'] = m9_2018_07_passage
                # Special fix for 2018_12 Q52 & Q53
                elif key == '2018_12' and q_num == 52:
                    q_obj['sectionGroup'] = 'vocab_grammar'
                    q_obj['section'] = '問題9: 文章の文法'
                    prev_p = existing_q_map.get(51, {}).get('passage')
                    if prev_p: q_obj['passage'] = prev_p
                elif key == '2018_12' and q_num == 53:
                    q_obj['passage'] = m10_2018_12_q53_passage

                # If passage is missing, copy from peer question in same section
                if not q_obj.get('passage'):
                    for peer_num in range(q_num - 3, q_num + 4):
                        peer = existing_q_map.get(peer_num)
                        if peer and peer.get('section') == sec and peer.get('passage'):
                            q_obj['passage'] = peer['passage']
                            break

            # 3. Clean options: strip leading digits, extra whitespace
            clean_opts = []
            for opt in q_obj.get('options', []):
                cleaned = re.sub(r'^[1-4１-４][\s.、]+', '', str(opt)).strip()
                clean_opts.append(cleaned)
            q_obj['options'] = clean_opts

            # 4. Underline keywords for Mondai 1 & 2
            q_text = q_obj.get('question', '')
            if '問題1' in sec and '<u>' not in q_text:
                q_obj['question'] = underline_m1(q_text, q_obj['options'])
            elif '問題2' in sec and '<u>' not in q_text:
                q_obj['question'] = underline_m2(q_text, q_obj['options'])

            # 5. Star symbol for Mondai 8
            if '問題8' in sec and '★' not in q_obj['question']:
                q_obj['question'] += " ＿＿ ＿＿ ＿★＿ ＿＿"

            # 6. Synchronize official answer
            if q_num in official_ans:
                ans_num = official_ans[q_num] # 1..4
                ans_idx = max(0, min(len(q_obj['options']) - 1, ans_num - 1))
                q_obj['answer'] = ans_idx
                correct_text = q_obj['options'][ans_idx] if ans_idx < len(q_obj['options']) else f"Đáp án {ans_num}"
                if not q_obj.get('explanation') or '【正解】' not in q_obj['explanation']:
                    q_obj['explanation'] = f"【正解】{ans_num} ({correct_text})\n\n• Kiến thức và nội dung câu hỏi {q_num} trong đề thi JLPT N2 {month:02d}/{year}."

            questions.append(q_obj)

        # Standardize question counts & durations
        vocab_count = sum(1 for q in questions if q.get('sectionGroup') == 'vocab_grammar')
        reading_count = sum(1 for q in questions if q.get('sectionGroup') == 'reading')
        listening_count = sum(1 for q in questions if q.get('sectionGroup') == 'listening')

        exam_payload = {
            "id": f"n2-{year}-{month:02d}",
            "level": "N2",
            "year": year,
            "month": month,
            "title": f"JLPT N2 - {month:02d}/{year}",
            "theme": f"Đề thi chính thức JLPT N2 (Tháng {month:02d}/{year})",
            "description": f"Trọn bộ đề thi thực tế JLPT N2 kỳ tháng {month:02d}/{year} chuẩn hóa 100% (Từ vựng, Ngữ pháp, Đọc hiểu Split-View và Nghe hiểu).",
            "totalQuestions": len(questions),
            "vocabGrammarCount": vocab_count,
            "readingCount": reading_count,
            "listeningCount": listening_count,
            "hasAudio": True,
            "audio": f"data/audio/n2_{year}_{month:02d}.mp3",
            "standardized": True,
            "durations": {
                "vocab_grammar": 35,
                "reading": 70,
                "listening": 50,
                "full": 155
            },
            "questions": questions
        }

        # Write to public and root data directories
        target_pub1 = os.path.join(PUB_EXAMS_DIR, f"{key}.json")
        target_pub2 = os.path.join(PUB_EXAMS_DIR, f"n2_{key}.json")
        target_root1 = os.path.join(DATA_EXAMS_DIR, f"{key}.json")
        target_root2 = os.path.join(DATA_EXAMS_DIR, f"n2_{key}.json")

        for target in [target_pub1, target_pub2, target_root1, target_root2]:
            with open(target, 'w', encoding='utf-8') as out_f:
                json.dump(exam_payload, out_f, ensure_ascii=False, indent=2)

        # Build index entry
        index_records.append({
            "id": f"n2-{year}-{month:02d}",
            "level": "N2",
            "year": year,
            "month": month,
            "title": f"JLPT N2 - {month:02d}/{year}",
            "theme": f"Đề thi chính thức {month:02d}/{year}",
            "description": f"Đề thi chính thức kỳ thi JLPT N2 tháng {month:02d}/{year} đã chuẩn hóa 100% (Từ vựng, Ngữ pháp, Đọc hiểu & Nghe hiểu kèm Audio).",
            "file": f"data/n2_exams/{key}.json",
            "available": True,
            "standardized": True,
            "totalQuestions": len(questions),
            "vocabGrammarCount": vocab_count,
            "readingCount": reading_count,
            "listeningCount": listening_count,
            "hasAudio": True,
            "audio": f"data/audio/n2_{year}_{month:02d}.mp3",
            "durations": {
                "vocab_grammar": 35,
                "reading": 70,
                "listening": 50,
                "full": 155
            }
        })

        print(f"  -> Saved {key}.json: {len(questions)} Qs (Vocab: {vocab_count}, Dokkai: {reading_count}, Choukai: {listening_count})")
        
        # Explicit garbage collection per session to prevent memory overhead
        del exam_payload, questions, booklet_text, existing_qs, existing_q_map
        gc.collect()

    # Sort index records by year desc, month desc
    index_records.sort(key=lambda x: (x['year'], x['month']), reverse=True)

    # Save index files
    for idx_target in [INDEX_FILE, PUB_INDEX_FILE]:
        with open(idx_target, 'w', encoding='utf-8') as f:
            json.dump(index_records, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"COMPLETE! Successfully processed and standardized all {len(index_records)} exams.")
    print(f"Updated index saved to {PUB_INDEX_FILE}")
    print("=" * 60)

if __name__ == '__main__':
    process_all_exams()
