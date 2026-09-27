import sys, os, re, json, glob
import pypdf
import pykakasi

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'n2_exams')
PUBLIC_DATA_DIR = os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PUBLIC_DATA_DIR, exist_ok=True)

kks = pykakasi.kakasi()

# 1. Parse official answers for all 31 exams
ans_pdf = os.path.join(SOURCE_DIR, 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader_ans = pypdf.PdfReader(ans_pdf)

def parse_answer_page(p_idx):
    text = reader_ans.pages[p_idx].extract_text()
    chokai_idx = text.find('聴解')
    if chokai_idx != -1:
        text = text[:chokai_idx]
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    cleaned = []
    for l in lines:
        if any(h in l for h in ['JLPT', '文字・語彙', '文法', '読解', 'ĐÁP ÁN']) or re.match(r'^\d{1,2}$', l):
            continue
        cleaned.append(l)

    q_to_ans = {}
    pending_qs = []
    for l in cleaned:
        clean_l = re.sub(r'問題\s*[0-9０-９一二三四五六七八九１-９]*', ' ', l)
        nums = [int(x) for x in re.findall(r'\b\d+\b', clean_l)]
        if not nums:
            continue
        next_expected = len(q_to_ans) + len(pending_qs) + 1
        is_q = False
        if any(n > 4 for n in nums):
            is_q = True
        elif nums[0] == next_expected:
            if not pending_qs:
                is_q = True
        if is_q:
            pending_qs.extend(nums)
        else:
            for a in nums:
                if pending_qs:
                    q = pending_qs.pop(0)
                    q_to_ans[q] = a
    return q_to_ans

answer_db = {}
for p in range(1, len(reader_ans.pages)):
    text = reader_ans.pages[p].extract_text()
    m_ym = re.search(r'(\d{1,2})[/.-](\d{4})|(\d{4})[/.-](\d{1,2})', text)
    if m_ym:
        if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
            month, year = int(m_ym.group(1)), int(m_ym.group(2))
        else:
            year, month = int(m_ym.group(3)), int(m_ym.group(4))
        key = f"{year}_{month:02d}"
        answer_db[key] = parse_answer_page(p)

print(f"Loaded answers for {len(answer_db)} exams.")

# 2. Text cleanups
def clean_furigana(text):
    if not text:
        return ""
    lines = text.split('\n')
    cleaned = []
    for l in lines:
        s = l.strip()
        # Drop standalone short kana lines (furigana artifacts)
        if s and re.fullmatch(r'[\u3040-\u309F\u30A0-\u30FF]{1,6}', s) and cleaned:
            continue
        cleaned.append(l)
    res = '\n'.join(cleaned)
    # Join broken kanji across newlines
    res = re.sub(r'([\u4e00-\u9fff])\n([\u4e00-\u9fff])', r'\1\2', res)
    res = re.sub(r'([\u4e00-\u9fff])\n([\u3040-\u309F])', r'\1\2', res)
    return res

def clean_passage_text(text):
    if not text:
        return ""
    text = re.sub(r'<<<PAGE_\d+>>>', '', text)
    lines = text.split('\n')
    cleaned = []
    for l in lines:
        s = l.strip()
        if any(h in s for h in ['問題 10', '問題 11', '問題 12', '問題 13', '問題 14', '問題10', '問題11', '問題12', '問題13', '問題14', '読解', '次の(1)から', '次の（１）から', '次の A と B', '次の文章を読んで', '後の問いに対する答えとして']):
            continue
        cleaned.append(l)
    res = '\n'.join(cleaned).strip()
    return clean_furigana(res)

def extract_options(block):
    # Try finding 1..4 or １..４
    opt_m = re.search(r'[１1]\s*(.*?)[２2]\s*(.*?)[３3]\s*(.*?)[４4]\s*(.*)', block, re.DOTALL)
    if opt_m:
        q_text = block[:opt_m.start()].strip()
        opts = [
            re.sub(r'\s+', ' ', opt_m.group(1).strip()),
            re.sub(r'\s+', ' ', opt_m.group(2).strip()),
            re.sub(r'\s+', ' ', opt_m.group(3).strip()),
            re.sub(r'\s+', ' ', opt_m.group(4).strip())
        ]
        return q_text, opts
    # Try lines starting with numbers
    lines = block.split('\n')
    opt_lines = [l.strip() for l in lines if re.match(r'^[1234１２３４]\s+', l.strip())]
    if len(opt_lines) >= 4:
        # q_text is before the first option line
        first_opt_idx = next(i for i, l in enumerate(lines) if re.match(r'^[1234１２３４]\s+', l.strip()))
        q_text = '\n'.join(lines[:first_opt_idx]).strip()
        opts = [re.sub(r'^[1234１２３４]\s+', '', l).strip() for l in opt_lines[:4]]
        return q_text, opts
    return block.strip(), []

def underline_m1(sentence, options):
    """Underline kanji in Mondai 1 using pykakasi matching"""
    if '<u>' in sentence or not options:
        return sentence
    conv = kks.convert(sentence)
    for item in conv:
        orig = item['orig']
        hira = item['hira']
        # If this word is kanji and its reading is among the options
        if re.search(r'[\u4e00-\u9fff]', orig):
            if any(hira == opt or hira in opt or opt in hira for opt in options):
                return sentence.replace(orig, f"<u>{orig}</u>", 1)
    return sentence

def underline_m2(sentence, options):
    """Underline hiragana in Mondai 2 using options reading"""
    if '<u>' in sentence or not options:
        return sentence
    # Convert options to reading
    opt_readings = []
    for opt in options:
        conv = kks.convert(opt)
        h = ''.join(c['hira'] for c in conv)
        if h:
            opt_readings.append(h)
    for hira in opt_readings:
        if hira in sentence:
            return sentence.replace(hira, f"<u>{hira}</u>", 1)
    return sentence

def underline_m5(sentence, options):
    """Underline target word in Mondai 5"""
    if '<u>' in sentence or not options:
        return sentence
    # Often the target word in the sentence has similar meaning or length
    # Check if any option word is a stem or has kanji synonym
    conv = kks.convert(sentence)
    for item in conv:
        orig = item['orig']
        if len(orig) >= 2 and orig in sentence:
            # If word is surrounded by particles or adverbs
            pass
    return sentence
