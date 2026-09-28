import pypdf
import re
import json

r = pypdf.PdfReader('20NgayN1.pdf')

def extract_answers_from_text(txt):
    # Regex to find boxes followed by digit or ] (which is 1)
    # Characters used as answer markers: □, 回, 国, 匝, 巨, 匡, 睡, 睦, 腱, 贖, 鵬, 醒, 厘, 匹, 國, 囲, 図, etc.
    # Note: ] or ￢ or l or ‐ 1 often OCR'd as 1
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    
    # We want to identify blocks of Mondai
    # Let's inspect sections
    return lines

# Let's write an extractor that splits each answer page into its two days
for p in range(150, 160):
    txt = r.pages[p].extract_text()
    day_a = (p - 150) * 2 + 1
    day_b = day_a + 1
    print(f"Page {p+1} -> Day {day_a} and Day {day_b}")
