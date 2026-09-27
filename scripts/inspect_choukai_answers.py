import sys, os, re, pypdf

sys.stdout.reconfigure(encoding='utf-8')

ans_pdf = 'N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf'
reader = pypdf.PdfReader(ans_pdf)

for p in [1, 10, 20, 27, 30]:
    txt = reader.pages[p].extract_text()
    chokai_idx = txt.find('聴解')
    print(f"\n==================== PAGE {p} CHOUKAI ====================")
    if chokai_idx != -1:
        print(txt[chokai_idx:])
    else:
        print("NO 聴解 FOUND!")
