import os, sys, re, shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'N2_DE_CAC_NAM')
DATA_AUDIO = os.path.join(ROOT_DIR, 'data', 'audio')
PUB_AUDIO = os.path.join(ROOT_DIR, 'public', 'data', 'audio')

os.makedirs(DATA_AUDIO, exist_ok=True)
os.makedirs(PUB_AUDIO, exist_ok=True)

folders = sorted([d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))])
print(f"Total folders: {len(folders)}")

linked_audio = {}

for fld in folders:
    m_ym = re.search(r'(\d{1,2})[-/.](\d{4})|(\d{4})[-/.](\d{1,2})', fld)
    if not m_ym: continue
    if m_ym.group(1) and int(m_ym.group(2)) >= 2010:
        month, year = int(m_ym.group(1)), int(m_ym.group(2))
    else:
        year, month = int(m_ym.group(3)), int(m_ym.group(4))
        
    fpath = os.path.join(SOURCE_DIR, fld)
    mp3s = [f for f in os.listdir(fpath) if f.endswith('.mp3')]
    if not mp3s:
        print(f"No mp3 in {fld}")
        continue
    
    src_mp3 = os.path.join(fpath, mp3s[0])
    target_name = f"n2_{year}_{month:02d}.mp3"
    dst1 = os.path.join(DATA_AUDIO, target_name)
    dst2 = os.path.join(PUB_AUDIO, target_name)
    
    for dst in [dst1, dst2]:
        if not os.path.exists(dst):
            try:
                os.link(src_mp3, dst)
            except Exception:
                shutil.copy2(src_mp3, dst)
                
    linked_audio[f"{year}_{month:02d}"] = f"data/audio/{target_name}"
    size_mb = os.path.getsize(src_mp3) / (1024*1024)
    print(f"[{year}_{month:02d}] Linked '{mp3s[0]}' ({size_mb:.1f} MB) -> data/audio/{target_name}")

print(f"\nSuccessfully linked audio for {len(linked_audio)}/31 exams!")
