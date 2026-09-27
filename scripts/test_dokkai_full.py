import sys, os, re, json, glob
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/exam_2024_07_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's test extracting all Dokkai questions (52..71) with their passages
def extract_dokkai_questions(full_text, q_range):
    # q_range is e.g. range(52, 72)
    # Find start position of each question
    positions = {}
    for q in q_range:
        # Match question start: newline + space + q + space + text
        # Make sure it's not part of a date or page number
        m = re.search(rf'(?:^|\n)\s*{q}\s+(?=[^\d\n])', full_text)
        if not m:
            # Fallback
            m = re.search(rf'\b{q}\s+(?=[^\d\n])', full_text)
        if m:
            positions[q] = m.start()
        else:
            print(f"Warning: Q{q} position not found!")

    questions = []
    current_passage = ""
    
    # Text before first dokkai question contains first passage (Mondai 10 (1))
    first_q = q_range[0]
    m10_idx = full_text.find('問題 10')
    if m10_idx == -1: m10_idx = full_text.find('問題10')
    if m10_idx == -1: m10_idx = full_text.find('読解')
    
    initial_passage_raw = full_text[m10_idx:positions[first_q]] if m10_idx != -1 and first_q in positions else ""
    current_passage = clean_passage(initial_passage_raw)

    for idx, q in enumerate(q_range):
        next_q = q_range[idx+1] if idx+1 < len(q_range) else None
        q_start = positions.get(q)
        q_end = positions.get(next_q) if next_q else len(full_text)
        
        chunk = full_text[q_start:q_end]
        
        # Split chunk into: (question + options) and (next passage)
        # Options are 1..4 or １..４
        # Find option 4
        opt4_m = re.search(r'(?:^|\n)\s*[４4]\s*(.*?)(?=(?:\n\s*(?:（[１-９\d]+）|\([１-９\d]+\)|問題|\bA\b|\bB\b)|\n<<<PAGE_|\Z))', chunk, re.DOTALL)
        
        if opt4_m:
            q_and_opts_text = chunk[:opt4_m.end()].strip()
            following_text = chunk[opt4_m.end():].strip()
        else:
            q_and_opts_text = chunk.strip()
            following_text = ""
            
        # Parse q_text and opts
        q_text, opts = extract_options(q_and_opts_text)
        
        # Clean q_text: remove leading question number
        q_text = re.sub(rf'^\s*{q}\s+', '', q_text).strip()
        
        # Determine section name
        if q <= 56:
            sec_name = "問題10: 短文読解"
        elif q <= 64:
            sec_name = "問題11: 中文読解"
        elif q <= 66:
            sec_name = "問題12: 統合理解"
        elif q <= 69:
            sec_name = "問題13: 長文読解"
        else:
            sec_name = "問題14: 情報検索"
            
        q_obj = {
            "number": q,
            "section": sec_name,
            "sectionGroup": "reading",
            "passage": current_passage,
            "question": q_text,
            "options": opts
        }
        questions.append(q_obj)
        
        # If following_text contains a new passage marker, update current_passage!
        # Check if following_text has substance (> 40 chars or contains （...） or A/B or 問題)
        if following_text:
            cleaned_next = clean_passage(following_text)
            if len(cleaned_next) > 30:
                current_passage = cleaned_next

    return questions

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
    # clean furigana
    lines = p.split('\n')
    non_furigana = []
    for l in lines:
        s = l.strip()
        if s and re.fullmatch(r'[\u3040-\u309F\u30A0-\u30FF]{1,6}', s) and non_furigana:
            continue
        non_furigana.append(l)
    res = '\n'.join(non_furigana)
    res = re.sub(r'([\u4e00-\u9fff])\n([\u4e00-\u9fff])', r'\1\2', res)
    res = re.sub(r'([\u4e00-\u9fff])\n([\u3040-\u309F])', r'\1\2', res)
    return res.strip()

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
    return block.strip(), []

res = extract_dokkai_questions(text, range(52, 72))
print(f"Extracted {len(res)} Dokkai questions.")
for q in res:
    p_len = len(q['passage'])
    q_len = len(q['question'])
    o_len = len(q['options'])
    print(f"Q{q['number']:2} | {q['section']:16} | Passage: {p_len:4} chars | Q: {q['question'][:30]}... | Options: {o_len}")
