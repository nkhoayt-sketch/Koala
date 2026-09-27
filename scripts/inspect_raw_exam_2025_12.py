import pypdf, sys

sys.stdout.reconfigure(encoding='utf-8')

reader = pypdf.PdfReader('N2_DE_CAC_NAM/17.N2 12-2025/17.N2 12-2025 _260603.pdf')
print("Total pages in booklet:", len(reader.pages))

# Print pages 1..10
for i in range(10):
    print(f"\n==================== Page {i+1} ====================")
    print(reader.pages[i].extract_text())
