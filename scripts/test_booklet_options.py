import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')

def extract_booklet_choukai_options(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    # Find pages containing Choukai
    choukai_text = ""
    for p_idx in range(len(reader.pages)-8, len(reader.pages)):
        if p_idx < 0: continue
        txt = reader.pages[p_idx].extract_text() or ''
        if '聴解' in txt or '問題 1' in txt or '問題１' in txt:
            choukai_text += f"\n" + txt
            
    # Clean furigana
    lines = choukai_text.split('\n')
    clean = []
    for l in lines:
        s = l.strip()
        if re.match(r'^(?:N2\s+\d+/\d+|JLPT[・\s]N2|\d{1,2}$)', s):
            continue
        clean.append(l)
    text = '\n'.join(clean)
    
    # Split by 問題 1, 2, 5
    m_splits = re.split(r'(?:^|\n)\s*問題\s*([1-5１-５])', text)
    mondais = {}
    for i in range(1, len(m_splits), 2):
        m_num = int(m_splits[i].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5'))
        mondais[m_num] = m_splits[i+1]
        
    options_by_mondai = {}
    for m in [1, 2, 5]:
        if m not in mondais: continue
        m_txt = mondais[m]
        # Split by 1番, 2番, etc.
        q_splits = re.split(r'(?:^|\n)\s*([0-9０-９１-９]+)\s*番', m_txt)
        q_opts = {}
        for j in range(1, len(q_splits), 2):
            q_num = int(q_splits[j].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5').replace('６','6'))
            chunk = q_splits[j+1]
            # Extract 4 options
            # Options in booklet: 1 ..., 2 ..., 3 ..., 4 ...
            opt_lines = [l.strip() for l in chunk.split('\n') if re.match(r'^[1234１２３４]\s+', l.strip())]
            if len(opt_lines) >= 4:
                opts = [re.sub(r'^[1234１２３４]\s+', '', l).strip() for l in opt_lines[:4]]
            else:
                opt_m = re.search(r'[１1]\s*(.*?)[２2]\s*(.*?)[３3]\s*(.*?)[４4]\s*(.*)', chunk, re.DOTALL)
                if opt_m:
                    opts = [opt_m.group(k).strip() for k in range(1, 5)]
                else:
                    opts = []
            q_opts[q_num] = opts
        options_by_mondai[m] = q_opts
    return options_by_mondai

for folder in ['15. N2 7-2024', '14. N2 7-2023', '10. N2 7-2019', '1. N2 7-2010']:
    fpath = os.path.join(SOURCE_DIR, folder)
    pdfs = [f for f in os.listdir(fpath) if f.endswith('.pdf') and 'script' not in f.lower()]
    opts = extract_booklet_choukai_options(os.path.join(fpath, pdfs[0]))
    print(f"\n[{folder}] Booklet options:")
    for m, qs in opts.items():
        print(f"  Mondai {m}: {len(qs)} questions with options. Sample Q1: {qs.get(1)}")
