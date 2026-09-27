import sys, os, re, json, glob
import pypdf
import pykakasi

sys.stdout.reconfigure(encoding='utf-8')

kks = pykakasi.kakasi()

# Let's write an extractor for a given year and month
def parse_single_exam(pdf_path, year, month, answers):
    reader = pypdf.PdfReader(pdf_path)
    
    # 1. Collect pages up to Choukai
    pages_text = []
    for p_idx in range(len(reader.pages)):
        txt = reader.pages[p_idx].extract_text() or ''
        if '聴解' in txt and ('問題 1' in txt or '問題１' in txt or '問題 １' in txt or p_idx >= len(reader.pages) - 8):
            break
        pages_text.append(txt)
        
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

    # 2. Extract Mondai blocks
    # Mondai 1..14
    sec_splits = re.split(r'(?:^|\n)\s*(?:読解\s*|文法\s*|文字・語彙\s*)?問題\s*([0-9０-９一二三四五六七八九]+)', text)
    mondais = {}
    for i in range(1, len(sec_splits), 2):
        s_num_str = sec_splits[i].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5').replace('６','6').replace('７','7').replace('８','8').replace('９','9').replace('０','0')
        s_num = int(s_num_str) if s_num_str.isdigit() else 0
        mondais[s_num] = sec_splits[i+1]

    # Map question numbers to section
    # Let's find which question numbers belong to which section based on answer keys
    # Standard N2:
    # M1: Q1..5 (5)
    # M2: Q6..10 (5)
    # M3: Q11..13 or 11..15 (3 or 5)
    # M4: next 7 questions
    # M5: next 5 questions
    # M6: next 5 questions
    # M7: next 12 questions
    # M8: next 5 questions
    # M9: next 4 or 5 questions
    # M10: 5 questions (短文)
    # M11: 8 or 9 questions (中文)
    # M12: 2 questions (統合理解)
    # M13: 3 questions (長文)
    # M14: 2 questions (情報検索)
    
    # We can detect question section dynamically from mondais:
    q_to_sec = {}
    for m_num, m_text in mondais.items():
        found_qs = [int(x) for x in re.findall(r'(?:^|\n)\s*(\d{1,2})\s+', m_text)]
        for q in found_qs:
            if q in answers:
                q_to_sec[q] = m_num

    print(f"Exam {year}_{month:02d}: mapped {len(q_to_sec)}/{len(answers)} questions to sections.")
    return q_to_sec, mondais

q_to_sec, mondais = parse_single_exam('N2_DE_CAC_NAM/15. N2 7-2024/15. N2 7.2024.pdf', 2024, 7, {i: 1 for i in range(1, 72)})
for m in sorted(mondais.keys()):
    qs = [q for q, s in q_to_sec.items() if s == m]
    print(f"Mondai {m:2}: questions {min(qs, default=0)}..{max(qs, default=0)} (count={len(qs)})")
