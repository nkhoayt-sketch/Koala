import sys
import os
import re
import json
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

ans_pdf = os.path.join('N2_DE_CAC_NAM', 'ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')
reader = pypdf.PdfReader(ans_pdf)

def parse_answer_page(text):
    # Stop before Chokai (listening)
    chokai_idx = text.find('聴解')
    if chokai_idx != -1:
        text = text[:chokai_idx]
    
    # We want pairs of numbers: question numbers (1..56) and their choices (1..4)
    # Let's clean up line by line
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Let's find sections or blocks
    # Often lines look like:
    # 1 2 3 4 5
    # 2 3 1 4 2
    # or combined with "問題 1"
    q_to_ans = {}
    
    # Strategy: Scan for sequences of consecutive question numbers
    # A line like "1 2 3 4 5" followed by "2 3 1 4 2"
    # Or "31 32 33 34 35 36 37 38 39 40 41 42" followed by "4 4 3 1 2 1 1 2 3 3 2 4"
    for i in range(len(lines) - 1):
        l1 = lines[i]
        l2 = lines[i+1]
        
        nums1 = [int(x) for x in re.findall(r'\b\d+\b', l1)]
        nums2 = [int(x) for x in re.findall(r'\b\d+\b', l2)]
        
        # Check if nums1 is a sequence of questions, e.g. 1, 2, 3.. or 31, 32..
        # and nums2 are valid choices (1..4) of the same length
        if len(nums1) >= 2 and len(nums1) == len(nums2):
            is_seq = all(nums1[j+1] == nums1[j] + 1 for j in range(len(nums1)-1))
            is_ans = all(1 <= a <= 4 for a in nums2)
            if is_seq and is_ans and 1 <= nums1[0] <= 70:
                for q, a in zip(nums1, nums2):
                    q_to_ans[q] = a
                    
    return q_to_ans

# Test on 2023_12 (Page 28), 2022_12 (Page 26), 2019_12 (Page 21), 2018_07 (Page 18)
for p_idx in [17, 20, 25, 27]:
    txt = reader.pages[p_idx].extract_text()
    ans = parse_answer_page(txt)
    print(f"Page {p_idx+1}: Extracted {len(ans)} answers. Range: {min(ans.keys(), default=0)} to {max(ans.keys(), default=0)}")
    # Print sample
    sorted_q = sorted(ans.keys())
    print(f"Sample 1-10: {[ans.get(q) for q in sorted_q[:10]]}")
    print(f"Sample 31-40: {[ans.get(q) for q in range(31, 41) if q in ans]}")
