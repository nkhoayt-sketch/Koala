import sys
import os
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/sample_exam_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's clean up page markers
lines = text.split('\n')
clean_lines = []
for line in lines:
    l_strip = line.strip()
    if re.match(r'^---\s*PAGE\s*\d+\s*---$', l_strip):
        continue
    if re.match(r'^JLPT[・\s]N2[・\s]\d+/\d+', l_strip):
        continue
    if re.match(r'^\d+$', l_strip): # isolated page number
        continue
    clean_lines.append(line)

content = "\n".join(clean_lines)

# Section mappings
SECTIONS = {
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

# Find all section headers: e.g. 問題 1, 問題 2, etc.
# Match lines starting with [問間題題]\s*(\d+)
sec_matches = list(re.finditer(r'(?:問題|間題|題題)\s*([0-9０-９一二三四五六七八九]+)(.*?)(?=(?:問題|間題|題題)\s*[0-9０-９一二三四五六七八九]+|\Z)', content, re.DOTALL))
print(f"Found {len(sec_matches)} sections in 7/2023 text:")
for m in sec_matches:
    raw_num = m.group(1)
    # convert kanji or zenkaku num
    tr = {'１':1, '２':2, '３':3, '４':4, '５':5, '６':6, '７':7, '８':8, '９':9,
          '一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9,
          '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, '11':11, '12':12, '13':13, '14':14}
    sec_num = tr.get(raw_num, 0)
    if not sec_num:
        try:
            sec_num = int(raw_num)
        except:
            sec_num = 0
    sec_text = m.group(0)[:60].replace('\n', ' ')
    print(f"  Sec {sec_num}: {sec_text} (length {len(m.group(0))})")
