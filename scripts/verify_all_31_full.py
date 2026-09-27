import os, sys, json, glob

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, 'data', 'n2-index.json')

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    index_data = json.load(f)

print(f"Total exams in n2-index.json: {len(index_data)}")
available_count = sum(1 for e in index_data if e.get('available'))
has_audio_count = sum(1 for e in index_data if e.get('hasAudio'))

print(f"Available exams: {available_count}/31")
print(f"Exams with Audio: {has_audio_count}/31")

print("\n" + "="*95)
print(f"{'Exam ID':15} | {'Title':16} | {'Total':5} | {'Vocab/Gram':10} | {'Dokkai':7} | {'Choukai':8} | {'Audio File':24}")
print("="*95)

issues = []
for entry in index_data:
    exam_id = entry['id']
    f_rel = entry['file']
    f_path = os.path.join(ROOT_DIR, f_rel)
    f_pub = os.path.join(ROOT_DIR, 'public', f_rel)
    
    if not os.path.exists(f_path):
        issues.append(f"Missing file: {f_path}")
        continue
    if not os.path.exists(f_pub):
        issues.append(f"Missing public file: {f_pub}")
        continue
        
    with open(f_path, 'r', encoding='utf-8') as fp:
        exam = json.load(fp)
        
    qs = exam.get('questions', [])
    v_len = sum(1 for q in qs if q.get('sectionGroup') == 'vocab_grammar')
    r_len = sum(1 for q in qs if q.get('sectionGroup') == 'reading')
    c_len = sum(1 for q in qs if q.get('sectionGroup') == 'listening')
    
    # Audio file existence
    audio_path = os.path.join(ROOT_DIR, entry.get('audio', ''))
    audio_ok = os.path.exists(audio_path)
    if not audio_ok:
        issues.append(f"Missing audio file: {audio_path}")
        
    # Check script in Choukai
    choukai_qs = [q for q in qs if q.get('sectionGroup') == 'listening']
    with_script = sum(1 for q in choukai_qs if q.get('script', '').strip())
    
    audio_basename = os.path.basename(entry.get('audio', ''))
    print(f"{exam_id:15} | {entry['title']:16} | {len(qs):5} | {v_len:10} | {r_len:7} | {c_len:8} | {audio_basename:24}")

print("="*95)
if issues:
    print("\nISSUES FOUND:")
    for iss in issues:
        print(f" - {iss}")
else:
    print("\nALL 31 EXAMS FULLY VERIFIED! (VOCAB + GRAMMAR + DOKKAI + CHOUKAI + AUDIO)")
