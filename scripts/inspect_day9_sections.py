with open('scratch/day09_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pages = text.split('=== PAGE ')
for p in pages:
    if not p.strip(): continue
    lines = p.split('\n')
    header = lines[0]
    print(f"PAGE {header}")
    for l in lines[1:8]:
        if l.strip():
            print("  ", l.strip())
