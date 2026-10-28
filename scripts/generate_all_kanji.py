import os, sys, re, json, pymupdf, pykakasi

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N3_PDF_PATH = r'C:\Users\default.LAPTOP-ECP2IL69\Downloads\450-cau-kanji-N3.pdf'
N1_PDF_PATH = r'C:\Users\default.LAPTOP-ECP2IL69\Downloads\n1_kanji_400.pdf'

HV_PATH = os.path.join(ROOT_DIR, 'data', 'master_hanviet.json')
with open(HV_PATH, 'r', encoding='utf-8') as f:
    hanviet_dict = json.load(f)

kks = pykakasi.kakasi()

def get_hanviet(word):
    res = []
    for c in word:
        if '\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf':
            res.append(hanviet_dict.get(c, c))
    return ' - '.join(res) if res else ''

# ==============================================================================
# PART 1: KANJI N3 DRILL (45 Sets - 450 Questions)
# ==============================================================================
print('=== [1/2] Processing Kanji N3 Drill (450 questions) ===')
n3_doc = pymupdf.open(N3_PDF_PATH)

# Answer keys
n3_ans_text = '\n'.join([n3_doc[p].get_text('text') for p in [93, 94, 95]])
n3_answers = {}
chunks = re.split(r'Set\s+(\d+)', n3_ans_text)
for i in range(1, len(chunks), 2):
    s_num = int(chunks[i])
    s_body = chunks[i+1]
    if s_num == 43:
        n3_answers[s_num] = [1, 1, 4, 1, 4, 3, 1, 4, 3, 2]
        continue
    lines = [l.strip() for l in s_body.splitlines() if l.strip() in ['1', '2', '3', '4']]
    n3_answers[s_num] = [int(x) for x in lines[:10]]

def clean_opt(text):
    text = re.sub(r'ĐÀO|DUY|LẬP|Đ|UY', '', text).strip()
    return text

def find_n3_target_word(sentence, options, ans_idx, set_type):
    correct_opt = options[ans_idx - 1] if len(options) >= ans_idx else ''
    if set_type == 'reading':
        conv = kks.convert(sentence)
        for item in conv:
            orig = item['orig']
            hira = item['hira']
            if re.search(r'[\u4e00-\u9fff]', orig):
                if hira == correct_opt or hira.startswith(correct_opt) or correct_opt.startswith(hira):
                    return orig
        for length in [4, 3, 2, 1]:
            for i in range(len(sentence) - length + 1):
                sub = sentence[i:i+length]
                if re.search(r'[\u4e00-\u9fff]', sub):
                    sub_hira = ''.join(c['hira'] for c in kks.convert(sub))
                    if sub_hira == correct_opt:
                        return sub
        kanjis = re.findall(r'[\u4e00-\u9fff]+[ぁ-ん]*', sentence)
        for k in kanjis:
            k_hira = ''.join(c['hira'] for c in kks.convert(k))
            if k_hira == correct_opt:
                return k
        return kanjis[0] if kanjis else ''
    else: # writing
        opt_hira = ''.join(c['hira'] for c in kks.convert(correct_opt))
        if opt_hira in sentence:
            return opt_hira
        for l in range(len(opt_hira), 1, -1):
            if opt_hira[:l] in sentence:
                return opt_hira[:l]
        kana_matches = re.findall(r'[ぁ-ん]{2,}', sentence)
        for km in kana_matches:
            if km in opt_hira or opt_hira in km:
                return km
        return opt_hira

n3_out_dir = os.path.join(ROOT_DIR, 'data', 'n3_kanji')
n3_pub_dir = os.path.join(ROOT_DIR, 'public', 'data', 'n3_kanji')
os.makedirs(n3_out_dir, exist_ok=True)
os.makedirs(n3_pub_dir, exist_ok=True)

n3_index = []

for set_num in range(1, 46):
    set_str = f"Set {set_num:02d}"
    if (1 <= set_num <= 15) or (27 <= set_num <= 37):
        set_type = 'reading'
        set_type_label = '問題1　読み方クイズ'
    else:
        set_type = 'writing'
        set_type_label = '問題2　書き方クイズ'

    ans_list = n3_answers[set_num]
    p1 = n3_doc[(set_num - 1) * 2 + 2]
    p2 = n3_doc[(set_num - 1) * 2 + 3]
    
    set_questions = []

    for page, q_start in [(p1, 1), (p2, 6)]:
        cards = []
        for d in page.get_drawings():
            fill = d.get('fill')
            rect = pymupdf.Rect(d['rect'])
            if fill and abs(fill[0] - 1.0) < 0.02 and abs(fill[1] - 1.0) < 0.02 and abs(fill[2] - 1.0) < 0.02:
                if rect.width > 400 and rect.height > 60:
                    cards.append(rect)
        cards = sorted(cards, key=lambda r: r.y0)
        
        for idx, card in enumerate(cards):
            q_num = q_start + idx
            ans = ans_list[q_num - 1]
            words = page.get_text('words', clip=card)
            
            # Sentence words
            sent_words = [
                w for w in words
                if 15 <= (w[1] - card.y0) <= 35
                and (w[3] - w[1]) >= 8.5
                and w[4] not in ['ĐÀO', 'DUY', 'LẬP', 'Đ', 'UY']
            ]
            sent_words = sorted(sent_words, key=lambda w: w[0])
            sentence = ''.join([w[4] for w in sent_words]).strip()
            
            # Options words
            opt1_w = [w[4] for w in words if 40 <= (w[1] - card.y0) <= 62 and 95 < w[0] < 300]
            opt2_w = [w[4] for w in words if 40 <= (w[1] - card.y0) <= 62 and w[0] > 320]
            opt3_w = [w[4] for w in words if 68 <= (w[1] - card.y0) <= 95 and 95 < w[0] < 300]
            opt4_w = [w[4] for w in words if 68 <= (w[1] - card.y0) <= 95 and w[0] > 320]
            
            options = [clean_opt(''.join(w)) for w in [opt1_w, opt2_w, opt3_w, opt4_w]]
            if set_num == 43 and q_num == 10 and not options[3]:
                options[3] = '(sách gốc in trống)'
            
            target_word = find_n3_target_word(sentence, options, ans, set_type)
            # clean target word
            target_word = re.sub(r'^[A-ZĐUY]+\s*', '', target_word).strip('。、！？ ')
            
            # format question with <u>
            if target_word and target_word in sentence:
                q_formatted = sentence.replace(target_word, f"<u>{target_word}</u>", 1)
            else:
                q_formatted = f"<u>{sentence}</u>"
                
            correct_opt = options[ans - 1] if len(options) >= ans else ''
            hv_word = target_word if set_type == 'reading' else correct_opt
            han_viet = get_hanviet(hv_word)
            
            if set_type == 'reading':
                expl = (
                    f"【正解】{ans} ({correct_opt})\n\n"
                    f"• Từ vựng kiểm tra: {target_word} [{correct_opt}]\n"
                    f"• Âm Hán Việt: {han_viet}\n"
                    f"• Cách đọc chính xác của 「{target_word}」 trong câu là 「{correct_opt}」."
                )
            else:
                expl = (
                    f"【正解】{ans} ({correct_opt})\n\n"
                    f"• Từ vựng kiểm tra: {correct_opt} ({target_word})\n"
                    f"• Âm Hán Việt: {han_viet}\n"
                    f"• Chữ Hán chính xác ứng với cách đọc 「{target_word}」 là 「{correct_opt}」."
                )

            q_obj = {
                "id": f"n3_k_s{set_num:02d}_q{q_num:02d}",
                "number": q_num,
                "level": "N3",
                "set": f"Set {set_num:02d}",
                "type": set_type,
                "question": q_formatted,
                "targetWord": target_word or (correct_opt if set_type == 'writing' else ''),
                "options": options,
                "answer": ans,
                "hanViet": han_viet,
                "explanation": expl
            }
            set_questions.append(q_obj)

    set_filename = f"n3_kanji_set{set_num:02d}.json"
    set_data = {
        "id": f"n3_k_set{set_num:02d}",
        "set": f"Set {set_num:02d}",
        "title": f"Kanji N3 • Set {set_num:02d} ({set_type_label})",
        "level": "N3",
        "type": set_type,
        "totalQuestions": len(set_questions),
        "questions": set_questions
    }
    
    for d_path in [n3_out_dir, n3_pub_dir]:
        with open(os.path.join(d_path, set_filename), 'w', encoding='utf-8') as f:
            json.dump(set_data, f, ensure_ascii=False, indent=2)

    n3_index.append({
        "id": f"n3_k_set{set_num:02d}",
        "set": f"Set {set_num:02d}",
        "setNumber": set_num,
        "title": f"Set {set_num:02d} • {set_type_label.split('・')[0].strip()}",
        "type": set_type,
        "filename": set_filename,
        "totalQuestions": len(set_questions)
    })

for d_path in [n3_out_dir, n3_pub_dir]:
    with open(os.path.join(d_path, "n3_kanji_index.json"), 'w', encoding='utf-8') as f:
        json.dump(n3_index, f, ensure_ascii=False, indent=2)

print('Done Kanji N3 (45 sets saved)!')

# ==============================================================================
# PART 2: SHIN KANZEN MASTER KANJI N1 DRILL (10 Chapters - 400 Questions)
# ==============================================================================
print('\n=== [2/2] Processing Shin Kanzen Master Kanji N1 Drill (400 questions) ===')
n1_doc = pymupdf.open(N1_PDF_PATH)

def decode_text(val):
    if val.startswith('<') and val.endswith('>'):
        hex_str = val[1:-1]
        try:
            raw = bytes.fromhex(hex_str)
            if raw.startswith(b'\xfe\xff'):
                return raw[2:].decode('utf-16-be', errors='ignore')
            return raw.decode('utf-8', errors='ignore')
        except Exception:
            return ''
    elif val.startswith('(') and val.endswith(')'):
        return val[1:-1]
    return val

page_xref_map = {page.xref: i for i, page in enumerate(n1_doc)}
page_texts = {i: [] for i in range(len(n1_doc))}

for xref in range(1, n1_doc.xref_length()):
    try:
        obj = n1_doc.xref_object(xref)
    except Exception:
        continue
    if '/ActualText' in obj:
        m_pg = re.search(r'/Pg\s+(\d+)\s+0\s+R', obj)
        m_txt = re.search(r'/ActualText\s+(\([^\)]*\)|<[^>]*>)', obj)
        if m_txt and m_pg:
            pg_xref = int(m_pg.group(1))
            pg_num = page_xref_map.get(pg_xref)
            if pg_num is not None:
                page_texts[pg_num].append(decode_text(m_txt.group(1)))

# Parse N1 answers
n1_answers = {}
for ch in range(1, 11):
    ans_page_idx = ch * 5 - 1
    raw_str = ''.join(page_texts[ans_page_idx]).translate(str.maketrans('０１２３４５６７８９', '0123456789'))
    ch_ans = {}
    parts = re.split(r'問題\s*([1-4１-４])', raw_str)
    for p_idx in range(1, len(parts), 2):
        sec_num = int(parts[p_idx])
        sec_body = parts[p_idx+1]
        pairs = re.findall(r'(\d+)\s+([1-4])', sec_body)
        ch_ans[sec_num] = [int(p[1]) for p in pairs[:10]]
    n1_answers[ch] = ch_ans

def normalize_digits(s):
    s = s.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
    s = re.sub(r'([0-9])([^\d\s\.\,\)）＝×])', r'\1 \2', s)
    s = re.sub(r'([^\d\s\(\（＝×])([0-9])', r'\1 \2', s)
    return s

def parse_n1_page(page_idx):
    raw = normalize_digits(''.join(page_texts[page_idx]))
    m_head = re.search(r'（\s*1\s*×\s*10\s*＝\s*10点\s*）', raw)
    if m_head:
        body = raw[m_head.end():]
    else:
        m_head = re.search(r'選[び|べ]なさい。', raw)
        if m_head:
            body = raw[m_head.end():]
        else:
            body = raw

    parts = re.split(r'(?<=\s)(10|[1-9])\s+(?=[^\d\s])', ' ' + body.strip())
    items = []
    i = 1
    current_q_num = 1
    while i < len(parts):
        num_str = parts[i]
        content = parts[i+1].strip()
        num = int(num_str)
        if num == current_q_num:
            q_text = content
            options = []
            for opt_idx in [1, 2, 3, 4]:
                if i + 2 < len(parts) and int(parts[i+2]) == opt_idx:
                    options.append(parts[i+3].strip())
                    i += 2
                else:
                    break
            items.append({
                'num': num,
                'question': q_text,
                'options': options
            })
            current_q_num += 1
            i += 2
        else:
            i += 2
    return items

def find_n1_target_word(sentence, options, ans, q_type):
    correct_opt = options[ans - 1] if len(options) >= ans else ''
    if q_type == 'reading':
        conv = kks.convert(sentence)
        for c in conv:
            if re.search(r'[\u4e00-\u9fff]', c['orig']):
                if c['hira'] == correct_opt or c['hira'].startswith(correct_opt) or correct_opt.startswith(c['hira']):
                    return c['orig']
        for l in range(min(5, len(sentence)), 0, -1):
            for i in range(len(sentence) - l + 1):
                sub = sentence[i:i+l]
                if re.search(r'[\u4e00-\u9fff]', sub):
                    if ''.join(c['hira'] for c in kks.convert(sub)) == correct_opt:
                        return sub
        return sentence
    else: # writing
        opt_hira = ''.join(c['hira'] for c in kks.convert(correct_opt))
        if opt_hira in sentence:
            return opt_hira
        for l in range(len(opt_hira), 1, -1):
            if opt_hira[:l] in sentence:
                return opt_hira[:l]
        kana_blocks = re.findall(r'[ぁ-んァ-ン]{2,}', sentence)
        for kb in kana_blocks:
            if kb in opt_hira or opt_hira in kb or len(set(kb).intersection(set(opt_hira))) >= 2:
                return kb
        return correct_opt

n1_out_dir = os.path.join(ROOT_DIR, 'data', 'n1_kanji')
n1_pub_dir = os.path.join(ROOT_DIR, 'public', 'data', 'n1_kanji')
os.makedirs(n1_out_dir, exist_ok=True)
os.makedirs(n1_pub_dir, exist_ok=True)

ch_ranges = {
    1: '漢字 001～078',
    2: '漢字 079～156',
    3: '漢字 157～234',
    4: '漢字 235～306',
    5: '漢字 307～378',
    6: '漢字 379～450',
    7: '漢字 451～522',
    8: '漢字 523～594',
    9: '漢字 595～660',
    10: '漢字 661～800'
}

n1_index = []

for ch in range(1, 11):
    ch_questions = []
    global_q_num = 1
    
    for p_offset in range(4):
        sec_num = p_offset + 1
        sec_type = 'reading' if sec_num in [1, 3] else 'writing'
        sec_label = f"問題{sec_num}"
        
        p_idx = (ch - 1) * 5 + p_offset
        page_qs = parse_n1_page(p_idx)
        ans_list = n1_answers[ch].get(sec_num, [])
        
        for q_item in page_qs:
            q_num = q_item['num']
            sentence = q_item['question']
            options = q_item['options']
            ans = ans_list[q_num - 1] if len(ans_list) >= q_num else 1
            
            target_word = find_n1_target_word(sentence, options, ans, sec_type)
            target_word = target_word.strip('。、！？ ')
            
            # wrap in <u>
            if target_word and target_word in sentence:
                q_formatted = sentence.replace(target_word, f"<u>{target_word}</u>", 1)
            else:
                q_formatted = f"<u>{sentence}</u>"
                
            correct_opt = options[ans - 1] if len(options) >= ans else ''
            hv_word = target_word if sec_type == 'reading' else correct_opt
            han_viet = get_hanviet(hv_word)
            
            if sec_type == 'reading':
                expl = (
                    f"【正解】{ans} ({correct_opt})\n\n"
                    f"• Từ vựng kiểm tra: {target_word} [{correct_opt}]\n"
                    f"• Âm Hán Việt: {han_viet}\n"
                    f"• Cách đọc chính xác của 「{target_word}」 là 「{correct_opt}」."
                )
            else:
                expl = (
                    f"【正解】{ans} ({correct_opt})\n\n"
                    f"• Từ vựng kiểm tra: {correct_opt} ({target_word})\n"
                    f"• Âm Hán Việt: {han_viet}\n"
                    f"• Chữ Hán chính xác ứng với cách đọc 「{target_word}」 là 「{correct_opt}」."
                )

            q_obj = {
                "id": f"n1_skz_k_ch{ch:02d}_q{global_q_num:02d}",
                "number": global_q_num,
                "sectionNumber": sec_num,
                "section": sec_label,
                "level": "N1",
                "chapter": f"Chapter {ch} ドリル",
                "type": sec_type,
                "question": q_formatted,
                "targetWord": target_word or (correct_opt if sec_type == 'writing' else ''),
                "options": options,
                "answer": ans,
                "hanViet": han_viet,
                "explanation": expl
            }
            ch_questions.append(q_obj)
            global_q_num += 1

    ch_filename = f"shinkanzen_k_ch{ch:02d}.json"
    ch_data = {
        "id": f"n1_skz_k_ch{ch:02d}",
        "chapter": f"Chapter {ch} ドリル",
        "title": f"Chapter {ch} {ch_ranges[ch]} ドリル",
        "level": "N1",
        "totalQuestions": len(ch_questions),
        "questions": ch_questions
    }

    for d_path in [n1_out_dir, n1_pub_dir]:
        with open(os.path.join(d_path, ch_filename), 'w', encoding='utf-8') as f:
            json.dump(ch_data, f, ensure_ascii=False, indent=2)

    n1_index.append({
        "id": f"n1_skz_k_ch{ch:02d}",
        "chapter": f"Chapter {ch} ドリル",
        "chapterNumber": ch,
        "title": f"Chapter {ch} • {ch_ranges[ch]} ドリル",
        "range": ch_ranges[ch],
        "filename": ch_filename,
        "totalQuestions": len(ch_questions)
    })

for d_path in [n1_out_dir, n1_pub_dir]:
    with open(os.path.join(d_path, "n1_kanji_index.json"), 'w', encoding='utf-8') as f:
        json.dump(n1_index, f, ensure_ascii=False, indent=2)

print('Done Kanji N1 (10 chapters saved)!')
print('\nAll Kanji data generated successfully in both data/ and public/data/!')
