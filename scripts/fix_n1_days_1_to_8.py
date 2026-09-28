import json
import os
import glob
import re

def fix_existing_n1_days():
    # Make sure target directories exist
    os.makedirs('public/data/n1_20days', exist_ok=True)
    os.makedirs('data/n1_20days', exist_ok=True)
    os.makedirs('public/data', exist_ok=True)
    
    files = sorted(glob.glob('data/n1_20days/day*.json'))
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            
        qs = data.get('questions', [])
        
        # 1. Propagate passage for Mondai 7 questions
        m7_passage = ""
        for q in qs:
            sec = q.get('section', '')
            if '問題7' in sec:
                p = q.get('passage', '')
                if p and len(p.strip()) > 10:
                    m7_passage = p
                    break
        
        if m7_passage:
            for q in qs:
                sec = q.get('section', '')
                if '問題7' in sec:
                    q['passage'] = m7_passage
                    
        # 2. Clean options in all questions
        for q in qs:
            for idx, opt in enumerate(q.get('options', [])):
                # Strip out any dangling '問題X' trailing headers
                m = re.search(r'問題\s*[0-9１-９].*$', opt)
                if m and len(opt) > 30:
                    q['options'][idx] = opt[:m.start()].strip()
                    
        # Save to both data/n1_20days, public/data/n1_20days, data/dayXX.json, public/data/dayXX.json
        day_num = data.get('day')
        day_str = f"day{day_num:02d}.json"
        
        paths = [
            f"data/n1_20days/{day_str}",
            f"public/data/n1_20days/{day_str}",
            f"data/{day_str}",
            f"public/data/{day_str}"
        ]
        
        for p in paths:
            with open(p, 'w', encoding='utf-8') as fp:
                json.dump(data, fp, ensure_ascii=False, indent=2)
                
        print(f"Fixed & synced {day_str} ({len(qs)} Qs)")

if __name__ == '__main__':
    fix_existing_n1_days()
