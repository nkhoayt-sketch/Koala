import sys, os, re, json, glob
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')

def test_extract_script(folder):
    fpath = os.path.join(SOURCE_DIR, folder)
    scripts = [f for f in os.listdir(fpath) if 'script' in f.lower() and f.endswith('.pdf')]
    if not scripts: return
    reader = pypdf.PdfReader(os.path.join(fpath, scripts[0]))
    
    full_text = ""
    for p in range(len(reader.pages)):
        full_text += f"\n<<<PAGE_{p+1}>>>\n" + (reader.pages[p].extract_text() or '')
        
    # Clean header noise
    clean_lines = []
    for l in full_text.split('\n'):
        ls = l.strip()
        if re.match(r'^(?:JLPT[・\s]N2|N2\s+\d+/\d+|\d{1,2}/\d{4}|\d{4}/\d{1,2})', ls, re.I):
            continue
        if re.match(r'^\d{1,2}$', ls):
            continue
        clean_lines.append(l)
    text = "\n".join(clean_lines)

    # Split by Mondai 1..5
    m_splits = re.split(r'(?:^|\n)\s*問題\s*([1-5１-５])', text)
    mondais = {}
    for i in range(1, len(m_splits), 2):
        m_num = int(m_splits[i].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5'))
        mondais[m_num] = m_splits[i+1]
        
    print(f"\n[{folder}] Script has Mondais: {list(mondais.keys())}")
    for m in range(1, 6):
        if m in mondais:
            m_txt = mondais[m]
            # Find all questions in this mondai: e.g. "1番", "２番", "1 番", etc.
            q_splits = re.split(r'(?:^|\n)\s*([0-9０-９１-９]+)\s*番', m_txt)
            q_count = (len(q_splits) - 1) // 2
            print(f"  Mondai {m}: {q_count} questions found.")
            if q_count > 0:
                first_q_txt = q_splits[2][:100].replace('\n', ' ')
                print(f"    Sample Q1: {first_q_txt}...")

test_extract_script('15. N2 7-2024')
test_extract_script('14. N2 7-2023')
test_extract_script('10. N2 7-2019')
test_extract_script('1. N2 7-2010')
