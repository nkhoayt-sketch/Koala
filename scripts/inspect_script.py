# -*- coding: utf-8 -*-
import re

with open('choukai_script_2025_07.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pages = text.split('=== SCRIPT PAGE ')
print('Total script pages:', len(pages)-1)
for p in pages[1:]:
    p_num = p.split(' ===')[0]
    p_content = p.split(' ===\n')[1] if ' ===\n' in p else p
    first_lines = [l.strip() for l in p_content.split('\n') if l.strip()][:3]
    print(f'Page {p_num}: {" | ".join(first_lines)}')
