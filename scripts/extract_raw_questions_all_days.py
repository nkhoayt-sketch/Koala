import pypdf
import json
import os

r = pypdf.PdfReader('20NgayN1.pdf')

day_pages = {
    9: [69, 70, 71, 72, 73, 74, 75, 76],
    10: [77, 78, 79, 80],
    11: [81, 82, 83, 84, 85, 86],
    12: [87, 88, 89, 90, 91, 92, 93, 94],
    13: [95, 96, 97, 98, 99, 100, 101, 102],
    14: [103, 104, 105, 106, 107, 108, 109, 110],
    15: [111, 112, 113, 114, 115, 116],
    16: [117, 118, 119, 120, 121, 122],
    17: [123, 124, 125, 126, 127, 128, 129, 130],
    18: [131, 132, 133, 134, 135, 136, 137, 138],
    19: [139, 140, 141, 142, 143, 144, 145, 146]
}

os.makedirs('scratch', exist_ok=True)

for day, pages in day_pages.items():
    combined = ""
    for p in pages:
        combined += f"\n=== PAGE {p} ===\n" + (r.pages[p-1].extract_text() or "")
    with open(f"scratch/day{day:02d}_raw.txt", "w", encoding="utf-8") as f:
        f.write(combined)
    print(f"Dumped Day {day} ({len(pages)} pages, {len(combined)} chars)")
