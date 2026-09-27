import sys, os, re, json, glob
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')

def test_exam_dokkai(folder):
    fpath = os.path.join(SOURCE_DIR, folder)
    pdfs = [f for f in os.listdir(fpath) if f.endswith('.pdf') and 'script' not in f.lower()]
    if not pdfs: return
    reader = pypdf.PdfReader(os.path.join(fpath, pdfs[0]))
    
    # Collect text up to Choukai
    dokkai_text = ""
    in_dokkai = False
    for p_idx, page in enumerate(reader.pages):
        txt = page.extract_text() or ''
        if any(h in txt for h in ['問題 10', '問題10', '問題１０', '読解']) and p_idx >= 5:
            in_dokkai = True
        if in_dokkai:
            if '聴解' in txt and ('問題 1' in txt or '問題１' in txt or p_idx >= len(reader.pages) - 8):
                break
            dokkai_text += f"\n<<<PAGE_{p_idx+1}>>>\n" + txt

    # Find section splits: 問題 10, 11, 12, 13, 14
    splits = re.split(r'(?:^|\n)\s*(?:読解\s*)?問題\s*([1-9１-９一二三四五六七八九0-9０-９]+)', dokkai_text)
    m_dict = {}
    for i in range(1, len(splits), 2):
        m_num_str = splits[i].replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5').replace('６','6').replace('７','7').replace('８','8').replace('９','9').replace('０','0')
        m_num = int(m_num_str) if m_num_str.isdigit() else 0
        m_dict[m_num] = splits[i+1]

    print(f"\n[{folder}] Found Mondai sections: {list(m_dict.keys())}")
    for m in [10, 11, 12, 13, 14]:
        if m in m_dict:
            # Count questions in this section
            q_found = re.findall(r'(?:^|\n)\s*(\d{2})\s+', m_dict[m])
            print(f"  Mondai {m}: len={len(m_dict[m])}, questions found: {q_found}")
        else:
            print(f"  Mondai {m}: NOT FOUND!")

test_exam_dokkai('15. N2 7-2024')
test_exam_dokkai('14. N2 7-2023')
test_exam_dokkai('13. N2 7-2022')
test_exam_dokkai('10. N2 7-2019')
test_exam_dokkai('1. N2 7-2010')
