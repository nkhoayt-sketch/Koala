import pypdf, re, sys, json

sys.stdout.reconfigure(encoding='utf-8')

reader = pypdf.PdfReader('N2_DE_CAC_NAM/ĐÁP ÁN JLPT N2 (update 10.4.2026).pdf')

pages = {
    '2022_07': 25,
    '2022_12': 26,
    '2023_07': 27,
    '2023_12': 28,
    '2024_07': 29,
    '2024_12': 30
}

def parse_answer_page(p_num):
    text = reader.pages[p_num - 1].extract_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return text

for exam, p in pages.items():
    print(f"\n==================== {exam} (Page {p}) ====================")
    txt = parse_answer_page(p)
    print(txt[:400])
