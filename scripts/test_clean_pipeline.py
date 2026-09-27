import glob, json, re, os
import pykakasi

kks = pykakasi.kakasi()

HEADER_PATTERNS = [
    r'<<<PAGE.*?>>>',
    r'\s*(?:問題|間題|題題)\s*[0-9０-９一二三四五六七八九１-９]*.*$',
    r'____の言葉.*$',
    r'最もよいものを.*$',
    r'選びなさい.*$',
    r'（\s*）に入る.*$',
    r'次の(?:文章|文|言葉|AとB|ページ).*$',
    r'^\d+\s*$'
]

def clean_option_text(text):
    if not isinstance(text, str): return ""
    res = text.strip()
    for pat in HEADER_PATTERNS:
        res = re.sub(pat, '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r'^[1-4１-４][\s.、]+', '', res).strip()
    return res

def clean_question_item(q):
    opts = list(q.get('options', []))
    q_text = q.get('question', '').strip()
    sec = q.get('section', '')
    sec_group = q.get('sectionGroup', '')

    # 1. Check if opt[0] has question body leaked in
    if opts:
        opt0 = opts[0]
        # Match pattern where question body and 1 are in opt0
        m = re.search(r'^(?:[0-9０-９]+\s+)?(.*?)(?:[\s\n]+|^)[１1][\s.、]+(.+)$', opt0, re.DOTALL)
        if m:
            extracted_q = m.group(1).strip()
            real_opt0 = m.group(2).strip()
            if not q_text or len(q_text) < 4 or q_text.startswith('問題') or re.match(r'^\d+$', q_text):
                q_text = extracted_q
            opts[0] = real_opt0
        else:
            opts[0] = re.sub(r'^[0-9０-９]+[\s.、]+', '', opt0).strip()

    # 2. Clean all options
    cleaned_opts = [clean_option_text(o) for o in opts]
    q['options'] = cleaned_opts

    # 3. Clean q_text if it has trailing numbers or artifacts
    q_text = re.sub(r'<<<PAGE.*?>>>', '', q_text).strip()
    q_text = re.sub(r'^\d+\s+', '', q_text).strip()
    
    # 4. Underline logic for Mondai 1 & Mondai 2
    if sec_group == 'vocab_grammar':
        if '問題1' in sec and '<u>' not in q_text and cleaned_opts:
            q_text = underline_m1_robust(q_text, cleaned_opts)
        elif '問題2' in sec and '<u>' not in q_text and cleaned_opts:
            q_text = underline_m2_robust(q_text, cleaned_opts)

    q['question'] = q_text
    return q

def underline_m1_robust(sentence, options):
    if '<u>' in sentence or not options: return sentence
    # Match kanji word whose reading matches one of the options
    kanji_words = re.findall(r'[\u4e00-\u9fff]+[\u3040-\u309f]{0,3}', sentence)
    for kw in sorted(kanji_words, key=len, reverse=True):
        conv = kks.convert(kw)
        hira = ''.join(c['hira'] for c in conv)
        if any(hira == opt for opt in options):
            return sentence.replace(kw, f"<u>{kw}</u>", 1)
    # Match kanji without okurigana
    for kw in sorted(re.findall(r'[\u4e00-\u9fff]+', sentence), key=len, reverse=True):
        conv = kks.convert(kw)
        hira = ''.join(c['hira'] for c in conv)
        if any(hira in opt or opt in hira for opt in options):
            return sentence.replace(kw, f"<u>{kw}</u>", 1)
    return sentence

def underline_m2_robust(sentence, options):
    if '<u>' in sentence or not options: return sentence
    for opt in options:
        conv = kks.convert(opt)
        h = ''.join(c['hira'] for c in conv)
        if h and h in sentence and len(h) >= 2:
            return sentence.replace(h, f"<u>{h}</u>", 1)
    return sentence

# Test on 2010_07
d = json.load(open('public/data/n2_exams/2010_07.json', encoding='utf-8'))
for q in d['questions'][:25]:
    cleaned_q = clean_question_item(q)
    print(f"Q{cleaned_q['number']}: q='{cleaned_q['question']}'")
    print(f"   opts={cleaned_q['options']}")
