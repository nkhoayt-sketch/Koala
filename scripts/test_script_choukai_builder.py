import sys, os, re, json, pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')

def build_choukai_from_script(folder):
    fpath = os.path.join(SOURCE_DIR, folder)
    scripts = [f for f in os.listdir(fpath) if 'script' in f.lower() and f.endswith('.pdf')]
    if not scripts: return []
    reader = pypdf.PdfReader(os.path.join(fpath, scripts[0]))
    
    full_text = ""
    for p in range(len(reader.pages)):
        full_text += f"\n<<<PAGE_{p+1}>>>\n" + (reader.pages[p].extract_text() or '')
        
    lines = full_text.split('\n')
    clean = []
    for l in lines:
        s = l.strip()
        if re.match(r'^(?:N2\s+\d+/\d+|JLPT[・\s]N2|\d{1,2}$)', s):
            continue
        clean.append(l)
    text = '\n'.join(clean)
    
    # Split by 問題 1..5
    m_splits = re.split(r'(?:^|\n)\s*問題\s*([1-5１-５一二三四五]+)', text)
    mondais = {}
    for i in range(1, len(m_splits), 2):
        m_num = int(m_splits[i].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5'))
        mondais[m_num] = m_splits[i+1]
        
    questions = []
    
    # Instructions
    instructions = {
        1: "問題1では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。",
        2: "問題2では、まず質問を聞いてください。そのあと、問題用紙を見てください。読む時間があります。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。",
        3: "問題3では、問題用紙に何も印刷されていません。この問題は、全体としてどんな内容かを聞く問題です。話の前に質問はありません。まず話を聞いてください。それから、質問と選択肢を聞いて、1から4の中から、最もよいものを一つ選んでください。",
        4: "問題4では、問題用紙に何も印刷されていません。まず文を聞いてください。それから、それに対する返事を聞いて、1から3の中から、最もよいものを一つ選んでください。",
        5: "問題5では、長めの話を聞きます。この問題には練習はありません。メモをとってもかまいません。"
    }
    
    sec_names = {
        1: "聴解 問題1: 課題理解",
        2: "聴解 問題2: ポイント理解",
        3: "聴解 問題3: 概要理解",
        4: "聴解 問題4: 即時応答",
        5: "聴解 問題5: 統合理解"
    }

    for m_num in range(1, 6):
        if m_num not in mondais: continue
        m_txt = mondais[m_num]
        q_splits = re.split(r'(?:^|\n)\s*([0-9０-９１-９]+)\s*番', m_txt)
        for j in range(1, len(q_splits), 2):
            q_in_m = int(q_splits[j].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5').replace('６','6').replace('７','7').replace('８','8').replace('９','9').replace('０','0'))
            chunk = q_splits[j+1].strip()
            
            # Clean chunk from page markers
            chunk_clean = re.sub(r'<<<PAGE_\d+>>>', '', chunk).strip()
            
            # Find correct answer if printed like (正解: 4)
            ans_m = re.search(r'[（\(]\s*正解\s*[:：]\s*([1-4１-４])\s*[）\)]', chunk_clean)
            detected_ans = int(ans_m.group(1).replace('１','1').replace('２','2').replace('３','3').replace('４','4')) if ans_m else None
            
            # Extract question prompt
            # Usually starts with: "問い ..." or the first sentence
            prompt_m = re.search(r'(?:問い|質問[１-２1-2]?)\s*[:：]?\s*(.*?)(?=\n|（正解|\Z)', chunk_clean)
            if prompt_m:
                q_prompt = prompt_m.group(1).strip()
            else:
                first_line = chunk_clean.split('\n')[0].strip()
                q_prompt = first_line
                
            # If Mondai 4: options are 1, 2, 3
            if m_num == 4:
                opt_lines = [l.strip() for l in chunk_clean.split('\n') if re.match(r'^[123１２３]\s+', l.strip())]
                if len(opt_lines) >= 3:
                    opts = [re.sub(r'^[123１２３]\s+', '', l).strip() for l in opt_lines[:3]]
                else:
                    opt_m = re.search(r'[１1]\s*(.*?)[２2]\s*(.*?)[３3]\s*(.*)', chunk_clean, re.DOTALL)
                    if opt_m:
                        opts = [opt_m.group(k).strip() for k in range(1, 4)]
                    else:
                        opts = ["1", "2", "3"]
            else:
                # 4 options
                opt_lines = [l.strip() for l in chunk_clean.split('\n') if re.match(r'^[1234１２３４]\s+', l.strip())]
                if len(opt_lines) >= 4:
                    opts = [re.sub(r'^[1234１２３４]\s+', '', l).strip() for l in opt_lines[:4]]
                else:
                    opt_m = re.search(r'[１1]\s*(.*?)[２2]\s*(.*?)[３3]\s*(.*?)[４4]\s*(.*)', chunk_clean, re.DOTALL)
                    if opt_m:
                        opts = [opt_m.group(k).strip() for k in range(1, 5)]
                    else:
                        opts = ["1", "2", "3", "4"]

            questions.append({
                "mondai": m_num,
                "q_in_mondai": q_in_m,
                "section": sec_names[m_num],
                "instruction": instructions[m_num],
                "question": q_prompt,
                "options": opts,
                "detected_answer": detected_ans,
                "script": chunk_clean
            })
            
    return questions

q_2024 = build_choukai_from_script('15. N2 7-2024')
print(f"2024_07 extracted {len(q_2024)} questions from script!")
for q in q_2024[:8]:
    print(f"  M{q['mondai']} Q{q['q_in_mondai']}: prompt='{q['question'][:40]}...' | opts={len(q['options'])} | ans={q['detected_answer']}")
