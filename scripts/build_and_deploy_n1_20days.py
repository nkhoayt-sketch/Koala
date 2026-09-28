# -*- coding: utf-8 -*-
"""
Master Build Script for All 20 Days of N1 '20日で合格 N1'.
Validates, writes JSON to all target paths, and updates indexes.
"""

import json
import os
import sys
import glob

# Ensure scripts dir is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_n1_day11_12 import get_day11, get_day12
from data_n1_day13_14 import get_day13, get_day14
from data_n1_day15_16 import get_day15, get_day16
from data_n1_day17_18 import get_day17, get_day18
from data_n1_day19_20 import get_day19, get_day20
from validate_and_build_pipeline import validate_n1_day

def main():
    generators = {
        11: get_day11,
        12: get_day12,
        13: get_day13,
        14: get_day14,
        15: get_day15,
        16: get_day16,
        17: get_day17,
        18: get_day18,
        19: get_day19,
        20: get_day20
    }

    print("==================================================")
    print("VALIDATING AND GENERATING DAYS 11 TO 20")
    print("==================================================")

    all_valid = True
    days_data = {}

    for d in range(11, 21):
        gen_fn = generators[d]
        data = gen_fn()
        ok, errs = validate_n1_day(data)
        if not ok:
            print(f"[FAIL] Day {d} validation errors:")
            for err in errs:
                print(f"  - {err}")
            all_valid = False
        else:
            print(f"[PASS] Day {d} validated successfully: {len(data['questions'])} questions.")
            days_data[d] = data

    if not all_valid:
        print("ERROR: One or more days failed validation. Halting build.")
        sys.exit(1)

    print("\nWriting JSON to all target directories...")
    target_dirs = [
        "public/data/n1_20days",
        "data/n1_20days",
        "public/data",
        "data"
    ]
    for d_path in target_dirs:
        os.makedirs(d_path, exist_ok=True)

    for d, data in days_data.items():
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        # 1. public/data/n1_20days/dayXX.json
        p1 = f"public/data/n1_20days/day{d:02d}.json"
        with open(p1, "w", encoding="utf-8") as f:
            f.write(json_str)

        # 2. data/n1_20days/dayXX.json
        p2 = f"data/n1_20days/day{d:02d}.json"
        with open(p2, "w", encoding="utf-8") as f:
            f.write(json_str)

        # 3. public/data/dayXX.json
        p3 = f"public/data/day{d:02d}.json"
        with open(p3, "w", encoding="utf-8") as f:
            f.write(json_str)

        # 4. data/dayXX.json
        p4 = f"data/day{d:02d}.json"
        with open(p4, "w", encoding="utf-8") as f:
            f.write(json_str)

        print(f"  Saved Day {d} to all 4 destinations.")

    print("\nUpdating days-index.json...")
    for idx_path in ["data/days-index.json", "public/data/days-index.json"]:
        if os.path.exists(idx_path):
            with open(idx_path, "r", encoding="utf-8") as f:
                index_data = json.load(f)
            
            for item in index_data:
                day_num = item.get("day")
                if 1 <= day_num <= 20:
                    item["available"] = True
                    item["questionsCount"] = 45
                    item["file"] = f"data/day{day_num:02d}.json"
            
            with open(idx_path, "w", encoding="utf-8") as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
            print(f"  Updated {idx_path}: All 20 days marked available: true.")

    print("\nVerifying all 20 days in public/data/n1_20days/...")
    all_20_pass = True
    total_qs = 0
    for d in range(1, 21):
        fpath = f"public/data/n1_20days/day{d:02d}.json"
        if not os.path.exists(fpath):
            print(f"  [MISSING] {fpath}")
            all_20_pass = False
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            c = json.load(f)
        ok, errs = validate_n1_day(c)
        if not ok:
            print(f"  [FAIL] Day {d}: {errs[:2]}")
            all_20_pass = False
        else:
            total_qs += len(c.get("questions", []))

    if all_20_pass:
        print(f"SUCCESS: ALL 20 DAYS PASSED! Total questions = {total_qs} (45 x 20 = 900).")
    else:
        print("WARNING: Some days failed.")
        sys.exit(1)

if __name__ == '__main__':
    main()
