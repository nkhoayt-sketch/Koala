# -*- coding: utf-8 -*-
"""
Script: standardize_all_n2_data.py
Performs comprehensive data cleaning and Choukai standardization across all 31 N2 exams:
1. Strips all question body / header / page leakage from options.
2. Formats options to strictly 4 clean Japanese strings.
3. Automatically underlines target words in Mondai 1 (漢字読み), Mondai 2 (表記), and Mondai 5 (類義語).
4. Standardizes Choukai: sets section names, questionNumber ("1番", "2番"...), and image links.
5. Saves to both public/ and data/ directories.
"""

import os
import sys
import gc
import re
import json
import glob
import pykakasi

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'n2_exams')
PUB_DIR = os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams')

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

# Explicit list of target words for Mondai 5 across exams where underline is missing
M5_KEYWORDS = [
    'とりあえず', 'ゆずって', '雑談', 'かしこい', '大げさ',
    '勝手な', 'たびたび', 'ぶかぶか', '見解', 'レンタル',
    'ブーム', '慎重に', 'ちぢんで', 'ほぼ', '回復する',
    'くたくた', 'わずかに', '優秀', 'うつむいて', 'いきなり',
    'ただちに', '奇妙な', '仕上げて', '日中', 'しめっている',
    '追加', 'そうとう', 'じっと', 'あやまった', 'かさかさ',
    '済ます', 'あいまい', '思いがけない', 'みずから', 'そろいました',
    'およそ', '具体的', '依然として', '必死', 'ふもと',
    'そろえて', '買いしめた', '間際', 'たちまち', 'お勘定',
    'お詫び', '再三', 'あいにく', '張り切って', '引き受けて',
    'おおよそ', 'プラン', 'おだやかな', '急激に', 'がっかり',
    '率直', 'アイディア', '客観的', 'わずらわしい', 'あきらめた',
    '用心', '手軽に', 'わびて', 'あっさり', 'そっくり',
    'くつろいで', 'おのおの', '手をつくした', 'わいわい', 'あやうい',
    'さっぱり', 'しょっちゅう', 'わがまま', 'ユニーク', 'あわただしい',
    '合同', 'せっせと', 'わき', '妥協', 'そわそわ',
    'ぼんやり', 'すんなり', 'あらかじめ', 'おさえた', 'いきさつ',
    '重宝して', 'ぺこぺこ', 'おもむき', 'つねに', 'めきめき',
    'ばったり', 'つぶやいた', 'すっきり', 'おびただしい', 'ひたすら',
    'うろうろ', 'いらいら', 'おどおど', 'めいめい', 'みっともない',
    'あっけない', 'ものたりない', 'うっとうしい', 'しつこい', 'のんびり',
    'すたれて', 'まごまご', 'せっかち', 'たいら', 'はなはだしい',
    'おおむね', 'うすうす', 'いさぎよい', 'おのずと', 'だぶだぶ',
    '一致して', '題', 'そうぞうしい', '用心した', 'ぶかぶか'
]

def clean_option_text(text):
    if not isinstance(text, str):
        return ""
    res = text.strip()
    for pat in HEADER_PATTERNS:
        res = re.sub(pat, '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r'^[1-4１-４][\s.、]+', '', res).strip()
    # Strip any trailing question body leaked into option
    res = re.sub(r'\s*\d+\s+[^\d].*$', '', res).strip()
    return res

def underline_m1_robust(sentence, options):
    if '<u>' in sentence or not options:
        return sentence
    # Try exact match with kanji words (with okurigana)
    kanji_words = re.findall(r'[\u4e00-\u9fff]+[\u3040-\u309f]{0,3}', sentence)
    for kw in sorted(kanji_words, key=len, reverse=True):
        conv = kks.convert(kw)
        hira = ''.join(c['hira'] for c in conv)
        if any(hira == opt for opt in options):
            return sentence.replace(kw, f"<u>{kw}</u>", 1)
            
    # Try stem match (matching without okurigana)
    for kw in sorted(re.findall(r'[\u4e00-\u9fff]+', sentence), key=len, reverse=True):
        conv = kks.convert(kw)
        hira = ''.join(c['hira'] for c in conv)
        if any(hira in opt or opt.startswith(hira) for opt in options):
            return sentence.replace(kw, f"<u>{kw}</u>", 1)
            
    # If options share an okurigana suffix (like くて, て, た, ない)
    for opt in options:
        for suffix in ['くて', 'ない', 'て', 'た', 'だ', 'る', 'い', 'しい']:
            if opt.endswith(suffix):
                # Look for a kanji word in sentence ending with same suffix
                m = re.search(r'([\u4e00-\u9fff]+' + re.escape(suffix) + r')', sentence)
                if m:
                    target = m.group(1)
                    return sentence.replace(target, f"<u>{target}</u>", 1)
    return sentence

def underline_m2_robust(sentence, options):
    if '<u>' in sentence or not options:
        return sentence
    for opt in options:
        conv = kks.convert(opt)
        h = ''.join(c['hira'] for c in conv)
        if h and h in sentence and len(h) >= 2:
            return sentence.replace(h, f"<u>{h}</u>", 1)
        # Check stem (excluding trailing kana)
        stem = re.sub(r'[てただないるい]$', '', h)
        if stem and stem in sentence and len(stem) >= 2:
            m = re.search(re.escape(stem) + r'[\u3040-\u309f]?', sentence)
            if m:
                target = m.group(0)
                return sentence.replace(target, f"<u>{target}</u>", 1)
    return sentence

def underline_m5_robust(sentence, options, explanation=""):
    if '<u>' in sentence:
        return sentence
    # Check known M5 keywords
    for kw in M5_KEYWORDS:
        if kw in sentence:
            return sentence.replace(kw, f"<u>{kw}</u>", 1)
    # Check words mentioned in explanation
    if explanation:
        for kw in re.findall(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]{2,8}', explanation):
            if kw in sentence and len(kw) >= 2 and kw not in ['正解', '問題', '選択肢', '意味', '説明', 'こと']:
                return sentence.replace(kw, f"<u>{kw}</u>", 1)
    return sentence

def standardize_exam(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    exam_id = data.get('id', '')
    exam_key = f"{data.get('year')}_{data.get('month', 0):02d}"
    questions = data.get('questions', [])

    # Group listening questions
    listening_questions = []
    non_listening_questions = []

    for q in questions:
        sec = q.get('section', '')
        if q.get('sectionGroup') == 'listening' or '聴解' in sec:
            listening_questions.append(q)
        else:
            non_listening_questions.append(q)

    # 1. CLEAN AND STANDARDIZE NON-LISTENING QUESTIONS
    for q in non_listening_questions:
        q_num = q.get('number', 0)
        sec = q.get('section', '')
        q_text = q.get('question', '').strip()
        opts = list(q.get('options', []))

        # Check if option 0 absorbed the question body
        if opts:
            opt0 = opts[0]
            m = re.search(r'^(?:[0-9０-９]+\s+)?(.*?)(?:[\s\n]+|^)[１1][\s.、]+(.+)$', opt0, re.DOTALL)
            if m:
                extracted_q = m.group(1).strip()
                real_opt0 = m.group(2).strip()
                if not q_text or len(q_text) < 4 or q_text.startswith('問題') or re.match(r'^\d+$', q_text):
                    q_text = extracted_q
                opts[0] = real_opt0
            else:
                opts[0] = re.sub(r'^[0-9０-９]+[\s.、]+', '', opt0).strip()

        # Clean all options
        cleaned_opts = [clean_option_text(o) for o in opts]
        # Pad or trim to exactly 4 options if corrupted
        if len(cleaned_opts) > 4:
            cleaned_opts = cleaned_opts[:4]
        while len(cleaned_opts) < 4:
            cleaned_opts.append(f"{len(cleaned_opts)+1}")

        # Clean question text
        q_text = re.sub(r'<<<PAGE.*?>>>', '', q_text).strip()
        q_text = re.sub(r'^\d+\s+', '', q_text).strip()

        # Apply underlines
        if '問題1' in sec and '<u>' not in q_text:
            q_text = underline_m1_robust(q_text, cleaned_opts)
        elif '問題2' in sec and '<u>' not in q_text:
            q_text = underline_m2_robust(q_text, cleaned_opts)
        elif '問題5' in sec and '<u>' not in q_text:
            q_text = underline_m5_robust(q_text, cleaned_opts, q.get('explanation', ''))

        # Star in Mondai 8
        if '問題8' in sec and '★' not in q_text:
            q_text += " ＿＿ ＿＿ ＿★＿ ＿＿"

        q['question'] = q_text
        q['options'] = cleaned_opts

    # 2. STANDARDIZE CHOUKAI (LISTENING) QUESTIONS
    # Determine listening sub-sections
    m1_list = []
    m2_list = []
    m3_list = []
    m4_list = []
    m5_list = []

    for q in listening_questions:
        sec = q.get('section', '')
        if '問題1' in sec or '課題理解' in sec:
            m1_list.append(q)
        elif '問題2' in sec or 'ポイント理解' in sec:
            m2_list.append(q)
        elif '問題3' in sec or '概要理解' in sec:
            m3_list.append(q)
        elif '問題4' in sec or '即時応答' in sec:
            m4_list.append(q)
        else:
            m5_list.append(q)

    # Standardize Mondai 1 (usually 5 questions)
    for idx, q in enumerate(m1_list, 1):
        q['sectionGroup'] = 'listening'
        q['section'] = '聴解 - 問題1: 課題理解'
        q['questionNumber'] = f"{idx}番"
        q['title'] = f"問題1 - {idx}番"

    # Standardize Mondai 2 (usually 6 questions)
    for idx, q in enumerate(m2_list, 1):
        q['sectionGroup'] = 'listening'
        q['section'] = '聴解 - 問題2: ポイント理解'
        q['questionNumber'] = f"{idx}番"
        q['title'] = f"問題2 - {idx}番"

    # Standardize Mondai 3 (usually 5 questions)
    for idx, q in enumerate(m3_list, 1):
        q['sectionGroup'] = 'listening'
        q['section'] = '聴解 - 問題3: 概要理解'
        q['questionNumber'] = f"{idx}番"
        q['title'] = f"問題3 - {idx}番"

    # Standardize Mondai 4 (usually 11 or 12 questions)
    for idx, q in enumerate(m4_list, 1):
        q['sectionGroup'] = 'listening'
        q['section'] = '聴解 - 問題4: 即時応答'
        q['questionNumber'] = f"{idx}番"
        q['title'] = f"問題4 - {idx}番"

    # Standardize Mondai 5 (usually 3 or 4 questions)
    if len(m5_list) == 3:
        m5_list[0]['sectionGroup'] = 'listening'
        m5_list[0]['section'] = '聴解 - 問題5: 統合理解'
        m5_list[0]['questionNumber'] = '1番'
        m5_list[0]['title'] = '問題5 - 1番'

        m5_list[1]['sectionGroup'] = 'listening'
        m5_list[1]['section'] = '聴解 - 問題5: 統合理解'
        m5_list[1]['questionNumber'] = '2番 (質問1)'
        m5_list[1]['title'] = '問題5 - 2番 (質問1)'

        m5_list[2]['sectionGroup'] = 'listening'
        m5_list[2]['section'] = '聴解 - 問題5: 統合理解'
        m5_list[2]['questionNumber'] = '2番 (質問2)'
        m5_list[2]['title'] = '問題5 - 2番 (質問2)'
    elif len(m5_list) == 4:
        m5_list[0]['sectionGroup'] = 'listening'
        m5_list[0]['section'] = '聴解 - 問題5: 統合理解'
        m5_list[0]['questionNumber'] = '1番'
        m5_list[0]['title'] = '問題5 - 1番'

        m5_list[1]['sectionGroup'] = 'listening'
        m5_list[1]['section'] = '聴解 - 問題5: 統合理解'
        m5_list[1]['questionNumber'] = '2番'
        m5_list[1]['title'] = '問題5 - 2番'

        m5_list[2]['sectionGroup'] = 'listening'
        m5_list[2]['section'] = '聴解 - 問題5: 統合理解'
        m5_list[2]['questionNumber'] = '3番 (質問1)'
        m5_list[2]['title'] = '問題5 - 3番 (質問1)'

        m5_list[3]['sectionGroup'] = 'listening'
        m5_list[3]['section'] = '聴解 - 問題5: 統合理解'
        m5_list[3]['questionNumber'] = '3番 (質問2)'
        m5_list[3]['title'] = '問題5 - 3番 (質問2)'
    else:
        for idx, q in enumerate(m5_list, 1):
            q['sectionGroup'] = 'listening'
            q['section'] = '聴解 - 問題5: 統合理解'
            q['questionNumber'] = f"{idx}番"
            q['title'] = f"問題5 - {idx}番"

    # Images for specific questions
    for q in listening_questions:
        # 2025_12 Q73 (Mondai 1 - 2番)
        if exam_key == '2025_12' and q.get('questionNumber') == '2番' and '問題1' in q.get('section', ''):
            q['image'] = 'data/images/n2_2025_12_q73.jpg'
        # 2023_12 Q73 (Mondai 1 - 2番)
        if exam_key == '2023_12' and q.get('questionNumber') == '2番' and '問題1' in q.get('section', ''):
            q['image'] = 'public/assets/choukai/n2_2023_12_q2.jpg'

    # Combine questions
    all_questions = non_listening_questions + listening_questions
    data['questions'] = all_questions

    # Save to file
    with open(file_path, 'w', encoding='utf-8') as out_f:
        json.dump(data, out_f, ensure_ascii=False, indent=2)

    return len(non_listening_questions), len(listening_questions)

def process_all():
    files = sorted(glob.glob(os.path.join(PUB_DIR, '20*.json')))
    print(f"Standardizing {len(files)} exams in public/data/n2_exams and data/n2_exams...")

    for idx, f in enumerate(files, 1):
        filename = os.path.basename(f)
        non_l, l = standardize_exam(f)
        
        # Also copy to root data/
        root_target = os.path.join(DATA_DIR, filename)
        alt_pub = os.path.join(PUB_DIR, f"n2_{filename}")
        alt_root = os.path.join(DATA_DIR, f"n2_{filename}")

        with open(f, 'r', encoding='utf-8') as src:
            content = src.read()
        with open(root_target, 'w', encoding='utf-8') as dst:
            dst.write(content)
        with open(alt_pub, 'w', encoding='utf-8') as dst:
            dst.write(content)
        with open(alt_root, 'w', encoding='utf-8') as dst:
            dst.write(content)

        print(f"[{idx}/{len(files)}] {filename}: {non_l} Gengo/Dokkai, {l} Choukai standardized.")
        gc.collect()

    print("\nALL EXAMS SUCCESSFULLY STANDARDIZED!")

if __name__ == '__main__':
    process_all()
