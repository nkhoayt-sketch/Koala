import urllib.request, json, sys

sys.stdout.reconfigure(encoding='utf-8')

resp = urllib.request.urlopen('http://localhost:5500/data/n2_exams/2025_12.json')
d = json.loads(resp.read().decode('utf-8'))

vn_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
vn_found = []

for q in d['questions']:
    for idx, opt in enumerate(q.get('options', [])):
        if any(c in opt.lower() for c in vn_chars):
            vn_found.append((q['number'], idx, opt))

print("=== VIETNAMESE CHECK IN ALL OPTIONS ===")
if vn_found:
    print(f"FAILED: Found {len(vn_found)} options with Vietnamese: {vn_found}")
else:
    print("SUCCESS: 0 options contain Vietnamese characters across the entire exam!")

print("\n=== CHOUKAI FORMAT CHECK (Q72 - Q101) ===")
choukai_qs = [q for q in d['questions'] if q['number'] >= 72]
print(f"Total Choukai questions: {len(choukai_qs)}")

for q in choukai_qs[:8]:
    print(f"Q{q['number']}: sec='{q.get('section')}' | qNum='{q.get('questionNumber')}' | title='{q.get('title')}' | opts={q.get('options')}")

# Check Q73 specifically
q73 = next(q for q in d['questions'] if q['number'] == 73)
print(f"\n[Q73 Detail]")
print("Question:", q73.get('question'))
print("Options:", q73.get('options'))
print("Image:", q73.get('image'))
print("Explanation preview:", repr(q73.get('explanation')[:80]))
