import sys, os, re, json, glob
import pypdf
import pykakasi

sys.stdout.reconfigure(encoding='utf-8')

kks = pykakasi.kakasi()

with open('scripts/exam_2024_07_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect Mondai 9 passage in 2024_07
m9_idx = text.find('問題 9')
m10_idx = text.find('問題 10')
m9_chunk = text[m9_idx:m10_idx]

# In m9_chunk, find where questions start (e.g. "48")
q48_m = re.search(r'(?:^|\n)\s*48\s+', m9_chunk)
if q48_m:
    m9_passage_raw = m9_chunk[:q48_m.start()]
    # Clean passage
    lines = m9_passage_raw.split('\n')
    cleaned_m9 = []
    for l in lines:
        s = l.strip()
        if any(h in s for h in ['問題 9', '次の文章を読んで', '文章全体の内容を考えて', '48 から 51', '1・2・3・4 から一つ選びなさい']):
            continue
        cleaned_m9.append(l)
    m9_passage = '\n'.join(cleaned_m9).strip()
    print("=== MONDAI 9 PASSAGE ===")
    print(m9_passage[:200] + "...")
