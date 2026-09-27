import glob, json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

targets = ['2024_07', '2024_12', '2023_07', '2023_12', '2022_07', '2022_12']
vn_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'

for e in targets:
    p = f'data/n2_exams/{e}.json'
    print(f"\n==================== {e} ====================")
    if not os.path.exists(p):
        print("NOT FOUND")
        continue
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    qs = d.get('questions', [])
    print(f"Total: {len(qs)}")
    
    empty_q = []
    placeholders = []
    vn_opts = []
    m9_no_passage = []
    dokkai_no_passage = []
    choukai_no_meta = []
    
    for q in qs:
        num = q.get('number')
        q_txt = q.get('question', '')
        opts = q.get('options', [])
        p_len = len(q.get('passage', ''))
        sec = q.get('section', '')
        sec_grp = q.get('sectionGroup', '')
        
        if not q_txt and sec_grp != 'choukai':
            empty_q.append(num)
        if any('Phương án' in str(opt) for opt in opts):
            placeholders.append(num)
        for opt in opts:
            if any(c in str(opt).lower() for c in vn_chars):
                vn_opts.append((num, opt))
                break
        if num in [48, 49, 50, 51] and p_len == 0:
            m9_no_passage.append(num)
        if 52 <= num <= 71 and p_len == 0:
            dokkai_no_passage.append(num)
        if num >= 72:
            if not q.get('questionNumber') or not q.get('title'):
                choukai_no_meta.append(num)
                
    print(f"Empty question text: {empty_q}")
    print(f"Placeholder options: {placeholders}")
    print(f"Vietnamese in options: {len(vn_opts)} questions")
    print(f"Mondai 9 missing passage: {m9_no_passage}")
    print(f"Dokkai missing passage: {dokkai_no_passage}")
    print(f"Choukai missing questionNumber/title: {len(choukai_no_meta)} questions")
