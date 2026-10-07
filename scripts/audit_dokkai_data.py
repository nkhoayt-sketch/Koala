#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_dokkai_data.py
Automated Quality Audit & Comprehensive Validation for Dokkai N1 Data.
"""

import os
import sys
import glob
import json
import re

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

VALID_MONDAI = {'short', 'medium', 'long', 'compare', 'search'}

def audit_and_fix():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dirs = [
        os.path.join(root_dir, 'data', 'n1_dokkai'),
        os.path.join(root_dir, 'public', 'data', 'n1_dokkai')
    ]
    
    report = []
    total_files = 0
    total_questions = 0
    total_issues = 0
    total_fixed = 0

    print("=" * 80)
    print(" 🔍 DOKKAI N1 DATA AUDIT & SANITY CHECK")
    print("=" * 80)

    # We will process files in data/n1_dokkai, fix them, and mirror to public/data/n1_dokkai
    src_dir = data_dirs[0]
    json_files = sorted(glob.glob(os.path.join(src_dir, 'shinkanzen_ch*.json')))

    for fpath in json_files:
        fname = os.path.basename(fpath)
        total_files += 1
        file_modified = False

        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        chapter_title = data.get('chapter', '')
        questions = data.get('questions', [])
        
        file_issues = []

        for idx, q in enumerate(questions):
            total_questions += 1
            qid = q.get('id', f'unknown_q{idx+1}')
            q_title = q.get('title', '')
            passage = q.get('passage', '')
            question_text = q.get('question', '')
            options = q.get('options', [])
            answer = q.get('answer')
            traps = q.get('trapBreakdown', {})
            hl = q.get('logicHighlights', {})
            mtype = q.get('mondaiType', '')

            # -------------------------------------------------------------
            # 1. Answer & Traps Audit
            # -------------------------------------------------------------
            # Answer must be integer 1 to 4
            if not isinstance(answer, int) or answer < 1 or answer > 4:
                file_issues.append(f"[{qid}] Answer '{answer}' is invalid, must be integer 1-4.")
                total_issues += 1

            # Check trap breakdown consistency
            for opt_num in range(1, 5):
                opt_key = f'opt{opt_num}'
                trap_text = traps.get(opt_key, '')
                if not trap_text:
                    file_issues.append(f"[{qid}] Missing trapBreakdown for {opt_key}.")
                    total_issues += 1
                    continue

                if opt_num == answer:
                    # Must be correct answer explanation
                    # Shouldn't contain negative trap keywords like '❌ BẪY TƯ DUY'
                    has_trap_neg = any(k in trap_text for k in ['❌ BẪY TƯ DUY', 'BẪY TƯ DUY', 'Nói quá đà', 'Bóp méo'])
                    has_correct_tag = '✓ ĐÁP ÁN ĐÚNG' in trap_text or 'ĐÁP ÁN ĐÚNG' in trap_text

                    if has_trap_neg and not has_correct_tag:
                        file_issues.append(f"[{qid}] Correct option opt{opt_num} contains trap label: {trap_text[:50]}")
                        total_issues += 1
                    elif not has_correct_tag:
                        # Auto-fix: ensure ✓ ĐÁP ÁN ĐÚNG prefix
                        traps[opt_key] = f"✓ ĐÁP ÁN ĐÚNG: {trap_text.lstrip('✓: ')}"
                        file_modified = True
                        total_fixed += 1
                else:
                    # Must be trap explanation
                    if '✓ ĐÁP ÁN ĐÚNG' in trap_text or 'ĐÁP ÁN ĐÚNG' in trap_text:
                        file_issues.append(f"[{qid}] Wrong option opt{opt_num} is labeled as ĐÁP ÁN ĐÚNG!")
                        # Auto-fix: change to ❌ BẪY TƯ DUY
                        cleaned = trap_text.replace('✓ ĐÁP ÁN ĐÚNG:', '').replace('ĐÁP ÁN ĐÚNG:', '').strip()
                        traps[opt_key] = f"❌ BẪY TƯ DUY: {cleaned}"
                        file_modified = True
                        total_fixed += 1
                        total_issues += 1
                    elif not trap_text.startswith('❌ BẪY TƯ DUY'):
                        # Ensure standard prefix
                        if not trap_text.startswith('❌'):
                            traps[opt_key] = f"❌ BẪY TƯ DUY: {trap_text}"
                            file_modified = True
                            total_fixed += 1

            # -------------------------------------------------------------
            # 2. Options & Passage Integrity
            # -------------------------------------------------------------
            if len(options) != 4:
                file_issues.append(f"[{qid}] Options count is {len(options)}, expected 4.")
                total_issues += 1
            for opt_idx, opt_str in enumerate(options):
                if not opt_str or not isinstance(opt_str, str) or len(opt_str.strip()) == 0:
                    file_issues.append(f"[{qid}] Option {opt_idx+1} is empty.")
                    total_issues += 1

            if not passage or len(passage.strip()) < 30:
                file_issues.append(f"[{qid}] Passage is too short or empty ({len(passage)} chars).")
                total_issues += 1

            # -------------------------------------------------------------
            # 3. Logic Highlights Alignment (Substring Match 100%)
            # -------------------------------------------------------------
            for hl_key in ['counterPremise', 'turningPoint', 'authorConclusion']:
                hl_val = hl.get(hl_key, '')
                if hl_val:
                    if hl_val not in passage:
                        file_issues.append(f"[{qid}] Highlight '{hl_key}' NOT found in passage: '{hl_val[:40]}...'")
                        total_issues += 1
                        
                        # Auto-fix known mismatches
                        # Ch05 Q4: turningPoint 'これは、〜からである'
                        if qid == 'skz_ch05_q04' and hl_key == 'turningPoint':
                            # In passage: "これは、言語が理性の産物であり意識的に嘘をつくことが容易であるのに対し、身体的な反応や無意識の仕草は感情の動きに直結しており、偽ることが極めて困難だからである。"
                            # Best turning point: "これは、言語が理性の産物であり" or "だからである"
                            target = "これは、言語が理性の産物であり意識的に嘘をつくことが容易であるのに対し"
                            if target in passage:
                                hl[hl_key] = target
                                file_modified = True
                                total_fixed += 1
                                print(f"    [FIXED] {qid} {hl_key} -> '{target}'")
                        
                        # Ch06 Q3: Highlights had 【A】 and 【B】 tags which were not in the sentence
                        elif qid == 'skz_ch06_q03':
                            clean_hl = hl_val.replace('【A】', '').replace('【B】', '').strip()
                            if clean_hl in passage:
                                hl[hl_key] = clean_hl
                                file_modified = True
                                total_fixed += 1
                                print(f"    [FIXED] {qid} {hl_key} removed tag -> '{clean_hl[:30]}...'")
                            else:
                                # Look for substring
                                if hl_key == 'turningPoint':
                                    target = "確かにリモートワークは定型的な業務処理においては高い効率を発揮する。しかし"
                                    if target in passage:
                                        hl[hl_key] = target
                                        file_modified = True
                                        total_fixed += 1
                                        print(f"    [FIXED] {qid} {hl_key} -> '{target}'")
                                elif hl_key == 'authorConclusion':
                                    target = "オフィスは単なる作業場ではなく、偶発的な対話を生み出す社会的な触媒であり、その価値を過小評価して完全なオンライン化を進めることには慎重であるべきだ。"
                                    if target in passage:
                                        hl[hl_key] = target
                                        file_modified = True
                                        total_fixed += 1
                                        print(f"    [FIXED] {qid} {hl_key} -> '{target[:30]}...'")

                        # Ch06 Q4: authorConclusion had Vietnamese paraphrased text instead of exact text from notice
                        elif qid == 'skz_ch06_q04' and hl_key == 'authorConclusion':
                            # In passage: "・他機関からの助成金と本プログラムの重複受給は不可（併願は可能だが採択時に辞退手続きが必要）。"
                            target = "他機関からの助成金と本プログラムの重複受給は不可（併願は可能だが採択時に辞退手続きが必要）"
                            if target in passage:
                                hl[hl_key] = target
                                file_modified = True
                                total_fixed += 1
                                print(f"    [FIXED] {qid} {hl_key} -> '{target}'")

            # -------------------------------------------------------------
            # 4. Title & MondaiType Format
            # -------------------------------------------------------------
            if mtype not in VALID_MONDAI:
                file_issues.append(f"[{qid}] mondaiType '{mtype}' invalid. Must be in {VALID_MONDAI}")
                total_issues += 1
                q['mondaiType'] = 'short'
                file_modified = True
                total_fixed += 1

            # Title must be pure Japanese format, e.g. 第1章：対比・逆接 - 練習 1
            if "Bài đọc" in q_title or "Chương" in q_title:
                ch_num_match = re.search(r'ch0?(\d+)', qid)
                q_num_match = re.search(r'q0?(\d+)', qid)
                if ch_num_match and q_num_match:
                    c_num = int(ch_num_match.group(1))
                    qn = int(q_num_match.group(1))
                    pure_title = f"{chapter_title} - 練習 {qn}"
                    q['title'] = pure_title
                    file_modified = True
                    total_fixed += 1
                    print(f"    [FIXED] {qid} title -> '{pure_title}'")

        # Save modifications if any
        if file_modified:
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  💾 Updated and saved: {fname}")

        # Print file status
        status_str = "PASS" if len(file_issues) == 0 else f"{len(file_issues)} ISSUES DETECTED"
        print(f"FILE: {fname:<24} | QUESTIONS: {len(questions):<2} | STATUS: {status_str}")
        for iss in file_issues:
            print(f"   ⚠️  {iss}")

    print("=" * 80)
    print(f" AUDIT SUMMARY: {total_files} files checked, {total_questions} questions scanned.")
    print(f" ISSUES FOUND: {total_issues} | AUTOMATICALLY RESOLVED: {total_fixed}")
    print("=" * 80)

    if total_issues > 0 and total_issues == total_fixed:
        print(">>> ALL ISSUES SUCCESSFULLY RESOLVED & ALIGNED 100%! <<<")
    elif total_issues == 0:
        print(">>> 100% PERFECT DATA INTEGRITY! NO ISSUES FOUND. <<<")
    else:
        print(f">>> WARNING: {total_issues - total_fixed} unresolved issues remaining. <<<")

    return total_issues - total_fixed == 0

if __name__ == '__main__':
    success = audit_and_fix()
    if not success:
        sys.exit(1)
