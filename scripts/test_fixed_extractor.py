import pypdf, re, sys

sys.stdout.reconfigure(encoding='utf-8')

reader = pypdf.PdfReader('N2_DE_CAC_NAM/15. N2 7-2024/15. N2 7.2024.pdf')
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

for q in [1, 10, 11, 12, 13, 21, 31, 41, 61, 71]:
    q_zen = str(q).translate(str.maketrans('0123456789', '０１２３４５６７８９'))
    # Match question header
    m = re.search(rf'(?:^|\n)\s*(?:{q}|{q_zen})[a-z。、.\s\(\)（）]*(?!\s*から)(?=[^\d\n]|$)', text)
    if m:
        start_idx = m.end()
        # Find next question or page or end
        next_q = q + 1
        next_zen = str(next_q).translate(str.maketrans('0123456789', '０１２３４５６７８９'))
        next_m = re.search(rf'(?:^|\n)\s*(?:{next_q}|{next_zen})[a-z。、.\s\(\)（）]*(?!\s*から)(?=[^\d\n]|$)', text[start_idx:])
        sub = text[start_idx:start_idx + (next_m.start() if next_m else 500)]
        # Now find options 1, 2, 3, 4
        opt_m = re.search(r'(?:^|\s|\n)[１1]\s+(.*?)(?:^|\s|\n)[２2]\s+(.*?)(?:^|\s|\n)[３3]\s+(.*?)(?:^|\s|\n)[４4]\s+([^\n<<<]+)', sub, re.DOTALL)
        if opt_m:
            q_txt = sub[:opt_m.start()].strip()
            opts = [opt_m.group(1).strip(), opt_m.group(2).strip(), opt_m.group(3).strip(), opt_m.group(4).strip()]
            print(f"Q{q}: q_txt=\"{q_txt}\", opts={opts}")
        else:
            print(f"Q{q}: NO OPT MATCH in sub: {repr(sub[:100])}")
    else:
        print(f"Q{q} NOT FOUND")
