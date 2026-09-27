# -*- coding: utf-8 -*-
with open('choukai_script_2025_07.txt', 'r', encoding='utf-8') as f:
    script_text = f.read()

with open('choukai_booklet_2025_07.txt', 'r', encoding='utf-8') as f:
    booklet_text = f.read()

# Let's write out the full script text to inspect cleanly
with open('full_script_clean.txt', 'w', encoding='utf-8') as out:
    for line in script_text.split('\n'):
        if 'JLPT・N2' in line:
            continue
        out.write(line + '\n')

print('Cleaned script written to full_script_clean.txt')
