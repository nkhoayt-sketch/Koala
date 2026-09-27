import sys
import os
import re
import json
import glob
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'n2_exams')
PUBLIC_DATA_DIR = os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams')

# Standard Instructions
INSTRUCTIONS = {
    1: "問題1では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。",
    2: "問題2では、まず質問を聞いてください。そのあと、問題用紙を見てください。読む時間があります。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。",
    3: "問題3では、問題用紙に何も印刷されていません。この問題は、全体としてどんな内容かを聞く問題です。話の前に質問はありません。まず話を聞いてください。それから、質問と選択肢を聞いて、1から4の中から、最もよいものを一つ選んでください。",
    4: "問題4では、問題用紙に何も印刷されていません。まず文を聞いてください。それから、それに対する返事を聞いて、1から3の中から、最もよいものを一つ選んでください。",
    5: "問題5では、長めの話を聞きます。この問題には練習はありません。メモをとってもかまいません。"
}

SEC_NAMES = {
    1: "聴解 問題1: 課題理解",
    2: "聴解 問題2: ポイント理解",
    3: "聴解 問題3: 概要理解",
    4: "聴解 問題4: 即時応答",
    5: "聴解 問題5: 統合理解"
}

def extract_choukai_from_folder(folder_path, start_num, exam_key):
    files = os.listdir(folder_path)
    script_candidates = [f for f in files if 'script' in f.lower() and f.endswith('.pdf')]
    exam_candidates = [f for f in files if f.endswith('.pdf') and 'script' not in f.lower()]
    
    if not script_candidates:
        return []
        
    script_path = os.path.join(folder_path, script_candidates[0])
    reader_script = pypdf.PdfReader(script_path)
    
    # 1. Read script full text
    full_script = ""
    for p in range(len(reader_script.pages)):
        full_script += f"\n<<<PAGE_{p+1}>>>\n" + (reader_script.pages[p].extract_text() or '')
        
    clean_lines = []
    for l in full_script.split('\n'):
        s = l.strip()
        if re.match(r'^(?:N2\s+\d+/\d+|JLPT[・\s]N2|\d{1,2}$)', s):
            continue
        clean_lines.append(l)
    script_text = '\n'.join(clean_lines)

    # 2. Extract options from booklet PDF for M1, M2, M5 if available
    booklet_options = {}
    if exam_candidates:
        try:
            reader_booklet = pypdf.PdfReader(os.path.join(folder_path, exam_candidates[0]))
            booklet_text = ""
            for p_idx in range(max(0, len(reader_booklet.pages)-9), len(reader_booklet.pages)):
                booklet_text += f"\n" + (reader_booklet.pages[p_idx].extract_text() or '')
            
            # Split booklet by Mondai 1..5
            b_m_splits = re.split(r'(?:^|\n)\s*問題\s*([1-5１-５])', booklet_text)
            for i in range(1, len(b_m_splits), 2):
                m_num = int(b_m_splits[i].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5'))
                m_chunk = b_m_splits[i+1]
                q_splits = re.split(r'(?:^|\n)\s*([0-9０-９１-９]+)\s*番', m_chunk)
                q_opts = {}
                for j in range(1, len(q_splits), 2):
                    qn = int(q_splits[j].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5').replace('６','6'))
                    q_block = q_splits[j+1]
                    opt_lines = [ol.strip() for ol in q_block.split('\n') if re.match(r'^[1234１２３４]\s+', ol.strip())]
                    if len(opt_lines) >= 4:
                        opts = [re.sub(r'^[1234１２３４]\s+', '', ol).strip() for ol in opt_lines[:4]]
                    else:
                        opt_m = re.search(r'[１1]\s*(.*?)[２2]\s*(.*?)[３3]\s*(.*?)[４4]\s*(.*)', q_block, re.DOTALL)
                        if opt_m:
                            opts = [re.sub(r'\s+', ' ', opt_m.group(k).strip()) for k in range(1, 5)]
                        else:
                            opts = []
                    if opts and len(opts) == 4 and all(opts):
                        q_opts[qn] = opts
                booklet_options[m_num] = q_opts
        except Exception as e:
            pass

    # 3. Parse Mondais from Script
    m_splits = re.split(r'(?:^|\n)\s*問題\s*([1-5１-５一二三四五]+)', script_text)
    mondais = {}
    for i in range(1, len(m_splits), 2):
        m_num = int(m_splits[i].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5'))
        mondais[m_num] = m_splits[i+1]

    questions = []
    curr_num = start_num

    for m_num in range(1, 6):
        if m_num not in mondais:
            continue
        m_txt = mondais[m_num]
        q_splits = re.split(r'(?:^|\n)\s*([0-9０-９１-９]+)\s*番', m_txt)
        
        for j in range(1, len(q_splits), 2):
            q_in_m = int(q_splits[j].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5').replace('６','6').replace('７','7').replace('８','8').replace('９','9').replace('０','0'))
            chunk = q_splits[j+1].strip()
            chunk_clean = re.sub(r'<<<PAGE_\d+>>>', '', chunk).strip()
            
            # Special handling for Mondai 5 with 質問1 and 質問2
            if m_num == 5 and ('質問２' in chunk_clean or '質問 2' in chunk_clean or '質問2' in chunk_clean):
                sub_parts = re.split(r'(?:^|\n)\s*(?:質問\s*[１-２1-2]|質問[１-２1-2])', chunk_clean)
                main_dialogue = sub_parts[0].strip()
                for sub_idx, sub_chunk in enumerate(sub_parts[1:], 1):
                    ans_m = re.search(r'[（\(]\s*正解\s*[:：]\s*([1-4１-４])\s*[）\)]', sub_chunk)
                    ans_val = int(ans_m.group(1).replace('１','1').replace('２','2').replace('３','3').replace('４','4')) if ans_m else 1
                    
                    first_l = sub_chunk.split('\n')[0].strip()
                    first_l = re.sub(r'[（\(]\s*正解.*', '', first_l).strip()
                    q_prompt = f"質問{sub_idx}：{first_l}"
                    
                    opt_lines = [ol.strip() for ol in sub_chunk.split('\n') if re.match(r'^[1234１２３４]\s+', ol.strip())]
                    if len(opt_lines) >= 4:
                        opts = [re.sub(r'^[1234１２３４]\s+', '', ol).strip() for ol in opt_lines[:4]]
                    else:
                        opt_m = re.search(r'[１1]\s*(.*?)[２2]\s*(.*?)[３3]\s*(.*?)[４4]\s*(.*)', sub_chunk, re.DOTALL)
                        if opt_m:
                            opts = [re.sub(r'\s+', ' ', opt_m.group(k).strip()) for k in range(1, 5)]
                        else:
                            opts = ["1", "2", "3", "4"]
                            
                    ans_idx = max(0, min(len(opts)-1, ans_val - 1))
                    corr_text = opts[ans_idx] if len(opts) > ans_idx else f"Phương án {ans_val}"
                    
                    q_item = {
                        "id": f"n2-{exam_key.replace('_','')}-q{curr_num:02d}",
                        "number": curr_num,
                        "sectionGroup": "listening",
                        "section": SEC_NAMES[m_num],
                        "instruction": INSTRUCTIONS[m_num],
                        "question": q_prompt,
                        "options": opts,
                        "answer": ans_idx,
                        "script": f"{main_dialogue}\n\n{q_prompt}",
                        "explanation": f"【正解】{ans_val} ({corr_text})\n\n• Giải thích nội dung bài nghe câu {curr_num} (聴解 問題5) trong đề thi JLPT N2."
                    }
                    questions.append(q_item)
                    curr_num += 1
                continue

            # Standard question extraction
            ans_m = re.search(r'[（\(]\s*正解\s*[:：]\s*([1-4１-４])\s*[）\)]', chunk_clean)
            ans_val = int(ans_m.group(1).replace('１','1').replace('２','2').replace('３','3').replace('４','4')) if ans_m else 1
            
            prompt_m = re.search(r'(?:問い|質問)\s*[:：]?\s*(.*?)(?=\n|（正解|\Z)', chunk_clean)
            if prompt_m:
                q_prompt = prompt_m.group(1).strip()
            else:
                first_line = chunk_clean.split('\n')[0].strip()
                q_prompt = re.sub(r'[（\(]\s*正解.*', '', first_line).strip()

            opts = []
            if m_num in booklet_options and q_in_m in booklet_options[m_num]:
                opts = booklet_options[m_num][q_in_m]
                
            if not opts:
                if m_num == 4:
                    opt_lines = [ol.strip() for ol in chunk_clean.split('\n') if re.match(r'^[123１２３]\s+', ol.strip())]
                    if len(opt_lines) >= 3:
                        opts = [re.sub(r'^[123１２３]\s+', '', ol).strip() for ol in opt_lines[:3]]
                    else:
                        opt_m = re.search(r'[１1]\s*(.*?)[２2]\s*(.*?)[３3]\s*(.*)', chunk_clean, re.DOTALL)
                        if opt_m:
                            opts = [re.sub(r'\s+', ' ', opt_m.group(k).strip()) for k in range(1, 4)]
                        else:
                            opts = ["1", "2", "3"]
                else:
                    opt_lines = [ol.strip() for ol in chunk_clean.split('\n') if re.match(r'^[1234１２３４]\s+', ol.strip())]
                    if len(opt_lines) >= 4:
                        opts = [re.sub(r'^[1234１２３４]\s+', '', ol).strip() for ol in opt_lines[:4]]
                    else:
                        opt_m = re.search(r'[１1]\s*(.*?)[２2]\s*(.*?)[３3]\s*(.*?)[４4]\s*(.*)', chunk_clean, re.DOTALL)
                        if opt_m:
                            opts = [re.sub(r'\s+', ' ', opt_m.group(k).strip()) for k in range(1, 5)]
                        else:
                            opts = ["1", "2", "3", "4"]

            ans_idx = max(0, min(len(opts)-1, ans_val - 1))
            corr_text = opts[ans_idx] if len(opts) > ans_idx else f"Phương án {ans_val}"
            
            q_item = {
                "id": f"n2-{exam_key.replace('_','')}-q{curr_num:02d}",
                "number": curr_num,
                "sectionGroup": "listening",
                "section": SEC_NAMES[m_num],
                "instruction": INSTRUCTIONS[m_num],
                "question": q_prompt,
                "options": opts,
                "answer": ans_idx,
                "script": chunk_clean,
                "explanation": f"【正解】{ans_val} ({corr_text})\n\n• Giải thích nội dung bài nghe câu {curr_num} ({SEC_NAMES[m_num]}) trong đề thi JLPT N2."
            }
            questions.append(q_item)
            curr_num += 1

    return questions

# 4. RUN CHOUKAI INTEGRATION FOR ALL 31 EXAMS
GOLDEN_TEMPLATES = {"2023_12", "2025_07"}
folders = sorted([d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))])
print(f"Processing Choukai integration for {len(folders)} folders...")

all_exams_meta = []

for folder in folders:
    m_ym = re.search(r'(\d{1,2})[-/.](\d{4})|(\d{4})[-/.](\d{1,2})', folder)
    if not m_ym: continue
    if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
        month, year = int(m_ym.group(1)), int(m_ym.group(2))
    else:
        year, month = int(m_ym.group(3)), int(m_ym.group(4))

    key = f"{year}_{month:02d}"
    out_name = f"{year}_{month:02d}.json"
    legacy_name = f"n2_{year}_{month:02d}.json"
    json_path = os.path.join(DATA_DIR, out_name)

    # 4.1 If Golden template, keep and ensure audio & public sync
    if key in GOLDEN_TEMPLATES:
        with open(json_path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        data['audio'] = f"data/audio/n2_{year}_{month:02d}.mp3"
        data['hasAudio'] = True
        
        # Save back
        for p in [json_path, os.path.join(DATA_DIR, legacy_name), os.path.join(PUBLIC_DATA_DIR, out_name), os.path.join(PUBLIC_DATA_DIR, legacy_name)]:
            with open(p, 'w', encoding='utf-8') as f_out:
                json.dump(data, f_out, ensure_ascii=False, indent=2)
                
        all_exams_meta.append({
            "id": data.get("id", f"n2-{year}-{month:02d}"),
            "level": "N2",
            "year": year,
            "month": month,
            "title": data.get("title", f"JLPT N2 - {month:02d}/{year}"),
            "theme": data.get("theme", f"Đề thi chính thức {month:02d}/{year}"),
            "description": data.get("description", f"Đề thi chính thức kỳ thi JLPT N2 tháng {month:02d}/{year}."),
            "file": f"data/n2_exams/{out_name}",
            "available": True,
            "totalQuestions": data["totalQuestions"],
            "vocabGrammarCount": data.get("vocabGrammarCount", 51),
            "readingCount": data.get("readingCount", 20),
            "listeningCount": data.get("listeningCount", 30),
            "hasAudio": True,
            "audio": f"data/audio/n2_{year}_{month:02d}.mp3",
            "durations": data.get("durations", {"vocab_grammar": 35, "reading": 70, "listening": 50, "full": 155})
        })
        print(f"[GOLDEN] {key}: Preserved {len(data['questions'])} questions.")
        continue

    # 4.2 For other 29 exams
    if not os.path.exists(json_path):
        print(f"Warning: {json_path} does not exist!")
        continue

    with open(json_path, 'r', encoding='utf-8') as fp:
        exam_data = json.load(fp)

    # Filter out any existing listening questions to prevent duplication
    existing_qs = [q for q in exam_data.get('questions', []) if q.get('sectionGroup') != 'listening']
    start_num = len(existing_qs) + 1

    folder_path = os.path.join(SOURCE_DIR, folder)
    choukai_qs = extract_choukai_from_folder(folder_path, start_num, key)
    print(f"-> {key}: Added {len(choukai_qs)} Choukai questions (Q{start_num}..Q{start_num + len(choukai_qs) - 1})")

    all_qs = existing_qs + choukai_qs
    exam_data['questions'] = all_qs
    exam_data['totalQuestions'] = len(all_qs)
    exam_data['listeningCount'] = len(choukai_qs)
    exam_data['hasAudio'] = True
    exam_data['audio'] = f"data/audio/n2_{year}_{month:02d}.mp3"
    exam_data['durations'] = {
        "vocab_grammar": 35,
        "reading": 70,
        "listening": 50,
        "full": 155
    }

    # Save to all target paths
    for p in [json_path, os.path.join(DATA_DIR, legacy_name), os.path.join(PUBLIC_DATA_DIR, out_name), os.path.join(PUBLIC_DATA_DIR, legacy_name)]:
        with open(p, 'w', encoding='utf-8') as f_out:
            json.dump(exam_data, f_out, ensure_ascii=False, indent=2)

    all_exams_meta.append({
        "id": f"n2-{year}-{month:02d}",
        "level": "N2",
        "year": year,
        "month": month,
        "title": f"JLPT N2 - {month:02d}/{year}",
        "theme": f"Đề thi chính thức {month:02d}/{year}",
        "description": f"Đề thi chính thức kỳ thi JLPT N2 tháng {month:02d}/{year} (Trọn bộ Từ vựng, Ngữ pháp, Đọc hiểu và Nghe hiểu).",
        "file": f"data/n2_exams/{out_name}",
        "available": True,
        "totalQuestions": len(all_qs),
        "vocabGrammarCount": exam_data.get("vocabGrammarCount", 51),
        "readingCount": exam_data.get("readingCount", 20),
        "listeningCount": len(choukai_qs),
        "hasAudio": True,
        "audio": f"data/audio/n2_{year}_{month:02d}.mp3",
        "durations": exam_data['durations']
    })

# Sort meta by year desc, month desc
all_exams_meta.sort(key=lambda x: (x['year'], x['month']), reverse=True)

# 5. UPDATE N2-INDEX.JSON IN ALL LOCATIONS
target_index_paths = [
    os.path.join(ROOT_DIR, 'data', 'n2-index.json'),
    os.path.join(DATA_DIR, 'n2-index.json'),
    os.path.join(ROOT_DIR, 'public', 'data', 'n2-index.json'),
    os.path.join(PUBLIC_DATA_DIR, 'n2-index.json'),
]

for idx_path in target_index_paths:
    with open(idx_path, 'w', encoding='utf-8') as f_idx:
        json.dump(all_exams_meta, f_idx, ensure_ascii=False, indent=2)

print("\n=======================================================")
print(f"CHOUKAI INTEGRATION COMPLETE FOR ALL {len(all_exams_meta)} EXAMS!")
print("=======================================================")
