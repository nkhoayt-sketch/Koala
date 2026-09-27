import pypdf, re, json, sys

sys.stdout.reconfigure(encoding='utf-8')

def parse_exam_pages(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    pages = [p.extract_text() or '' for p in reader.pages]
    return pages

print("Script template ready")
