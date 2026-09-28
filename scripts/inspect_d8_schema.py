import json
import os
import glob
import re

LOG_FILE = "process.log"

def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# Let's inspect data/n1_20days/day08.json structure to ensure 100% schema parity
with open('data/n1_20days/day08.json', 'r', encoding='utf-8') as f:
    d8_sample = json.load(f)

print("d8 keys:", list(d8_sample.keys()))
print("d8 sections:", [s['name'] if isinstance(s, dict) else s for s in d8_sample.get('sections', [])])
