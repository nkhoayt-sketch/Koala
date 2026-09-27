import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'N2_DE_CAC_NAM/14. N2 7-2023/14. N2 7-2023 (script).pdf'
reader = pypdf.PdfReader(pdf_path)

full_text = ""
for p in range(len(reader.pages)):
    full_text += f"\n<<<PAGE {p+1}>>>\n" + (reader.pages[p].extract_text() or '')

# Find Mondai 3 and 4
m3_idx = full_text.find('問題３')
if m3_idx == -1: m3_idx = full_text.find('問題 3')
if m3_idx == -1: m3_idx = full_text.find('問題3')

print("=== MONDAI 3 & 4 IN SCRIPT ===")
print(full_text[m3_idx:m3_idx+2500])
