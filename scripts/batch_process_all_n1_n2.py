import pypdf
import json
import os
import re
import glob

LOG_FILE = "process.log"

def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def clean_opt(opt):
    opt = opt.strip()
    # Strip leading 1, 2, 3, 4, etc.
    opt = re.sub(r'^[1-4１-４][\s\.・]*', '', opt)
    # Strip any trailing problem header
    m = re.search(r'問題\s*[0-9１-９].*$', opt)
    if m and len(opt) > 20:
        opt = opt[:m.start()].strip()
    return opt

def main():
    log("================================================================================")
    log("STARTING KOALA DATA PIPELINE: N1 20-DAYS & N2 PAST EXAMS")
    log("================================================================================")

if __name__ == '__main__':
    main()
