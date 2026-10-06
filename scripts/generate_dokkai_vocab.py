import os
import json
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'n1_dokkai')
PUBLIC_DATA_DIR = os.path.join(ROOT_DIR, 'public', 'data', 'n1_dokkai')

# Comprehensive N1 Dokkai Vocabulary Master Lexicon
N1_VOCAB_LEXICON = {
    # Ch01 Q01
    "美徳": {"reading": "びとく", "hanviet": "Mỹ Đức", "meaning": "Đức tính tốt đẹp, chuẩn mực đạo đức cao quý"},
    "浪費": {"reading": "ろうひ", "hanviet": "Lãng Phí", "meaning": "Sự lãng phí, tiêu tốn vô bổ"},
    "充実感": {"reading": "じゅうじつかん", "hanviet": "Sung Thực Cảm", "meaning": "Cảm giác thỏa mãn, đủ đầy ý nghĩa"},
    "思索": {"reading": "しさく", "hanviet": "Tư Tác", "meaning": "Suy ngẫm sâu sắc về bản chất vấn đề"},
    "無為": {"reading": "むい", "hanviet": "Vô Vi", "meaning": "Nhàn rỗi, không hành động gượng ép hay có mục đích"},
    "眼前": {"reading": "がんぜん", "hanviet": "Nhãn Tiền", "meaning": "Ngay trước mắt, tức thời"},
    "既存": {"reading": "きぞん", "hanviet": "Ký Tồn", "meaning": "Đã có sẵn, khuôn mẫu hiện hữu"},
    "枠組み": {"reading": "わくぐみ", "hanviet": "Khung Tổ", "meaning": "Khuôn khổ, rào cản tư duy"},
    "余白": {"reading": "よはく", "hanviet": "Dư Bạch", "meaning": "Khoảng trống dôi dư, khoảng lặng quý giá"},
    "肥沃": {"reading": "ひよく", "hanviet": "Phì Nhiêu", "meaning": "Màu mỡ, tươi tốt, giàu tiềm năng"},
    "土壌": {"reading": "どじょう", "hanviet": "Thổ Nhưỡng", "meaning": "Đất đai, môi trường màu mỡ nuôi dưỡng"},

    # Ch01 Q02
    "要約": {"reading": "ようやく", "hanviet": "Yếu Ước", "meaning": "Tóm lược, khái quát ý chính"},
    "代行": {"reading": "だいこう", "hanviet": "Đại Hành", "meaning": "Làm thay, đại diện thực hiện"},
    "膨大": {"reading": "ぼうだい", "hanviet": "Bàng Đại", "meaning": "Khổng lồ, cực kỳ đồ sộ"},
    "取って代わる": {"reading": "とってかわる", "hanviet": "Thủ Đại", "meaning": "Thay thế, đoạt chỗ"},
    "連鎖": {"reading": "れんさ", "hanviet": "Liên Tỏa", "meaning": "Chuỗi dây chuyền, mối liên hệ nối tiếp"},
    "欠落": {"reading": "けつらく", "hanviet": "Khiếm Lạc", "meaning": "Sự thiếu hụt, khiếm khuyết căn bản"},
    "揺さぶる": {"reading": "ゆさぶる", "hanviet": "Dao", "meaning": "Làm rung chuyển, lay động tâm can"},
    "背負う": {"reading": "せおう", "hanviet": "Bối Phụ", "meaning": "Gánh vác, mang trên mình sức nặng"},
    "巧み": {"reading": "たくみ", "hanviet": "Xảo", "meaning": "Khéo léo, tinh xảo, điêu luyện"},
    "紡ぎ出す": {"reading": "つむぎだす", "hanviet": "Phưởng Xuất", "meaning": "Dệt nên, sáng tạo ra áng văn"},
    "生身": {"reading": "なまみ", "hanviet": "Sinh Thân", "meaning": "Bằng xương bằng thịt, trải nghiệm sống thực"},
    "尊厳": {"reading": "そんげん", "hanviet": "Tôn Nghiêm", "meaning": "Phẩm giá, giá trị tôn nghiêm không thể xâm phạm"},

    # Ch01 Q03
    "細分化": {"reading": "さいぶんか", "hanviet": "Tế Phân Hóa", "meaning": "Phân chia nhỏ, chia thành các nhánh hẹp"},
    "特化": {"reading": "とっか", "hanviet": "Đặc Hóa", "meaning": "Chuyên môn hóa sâu vào một lĩnh vực"},
    "蛸壺": {"reading": "たこつぼ", "hanviet": "Tiêu Hồ", "meaning": "Chiếc vỏ ốc hẹp, cái hũ kín tự cô lập"},
    "閉じこもる": {"reading": "とじこもる", "hanviet": "Bế", "meaning": "Giam mình, thu mình trong phạm vi hẹp"},
    "はらむ": {"reading": "はらむ", "hanviet": "Hàm", "meaning": "Tiềm ẩn, chứa đựng nguy cơ ngầm"},
    "知見": {"reading": "ちけん", "hanviet": "Tri Kiến", "meaning": "Tri thức và hiểu biết sâu sắc tích lũy được"},
    "大所高所": {"reading": "たいしょこうしょ", "hanviet": "Đại Sở Cao Sở", "meaning": "Tầm nhìn bao quát, đại cục từ trên cao"},
    "俯瞰": {"reading": "ふかん", "hanviet": "Phủ Khám", "meaning": "Nhìn bao quát toàn cảnh từ trên cao xuống"},
    "越境": {"reading": "えっきょう", "hanviet": "Việt Cảnh", "meaning": "Vượt ranh giới, liên kết đa ngành"},

    # Ch01 Q04
    "淀みなく": {"reading": "よどみなく", "hanviet": "Định", "meaning": "Trôi chảy, lưu loát, không ngắc ngứ"},
    "間断なく": {"reading": "かんだんなく", "hanviet": "Gian Đoạn", "meaning": "Liên tục không ngừng nghỉ, không ngắt quãng"},
    "停滞": {"reading": "ていたい", "hanviet": "Đình Trệ", "meaning": "Sự ngưng trệ, bế tắc của cuộc trò chuyện"},
    "拙さ": {"reading": "つたなさ", "hanviet": "Chuyết", "meaning": "Sự vụng về, non nớt trong thể hiện"},
    "咀嚼": {"reading": "そしゃく", "hanviet": "Tổ Tước", "meaning": "Nghiền ngẫm, tiếp nhận và thẩm thấu sâu sắc"},
    "濃密": {"reading": "のうみつ", "hanviet": "Nồng Mật", "meaning": "Đậm đặc, sâu sắc, lắng đọng"},
    "余韻": {"reading": "よいん", "hanviet": "Dư Vận", "meaning": "Dư âm, dư vị lắng đọng sau lời nói"},
    "差し控える": {"reading": "さしひかえる", "hanviet": "Sai Khống", "meaning": "Chủ động kiềm chế, nhịn không nói ra"},
    "通底": {"reading": "つうてい", "hanviet": "Thông Để", "meaning": "Đồng điệu ngầm, thấu hiểu xuyên suốt mạch nguồn"},
    "雄弁": {"reading": "ゆうべん", "hanviet": "Hùng Biện", "meaning": "Nói năng trôi chảy, hùng hồn thao thao"},
    "成熟": {"reading": "せいじゅく", "hanviet": "Thành Thục", "meaning": "Sự chín muồi, trưởng thành sâu sắc"}
}

def extract_vocab_for_passage(passage):
    found = []
    # Search for words in lexicon that appear in passage
    for word, data in N1_VOCAB_LEXICON.items():
        if word in passage:
            found.append({
                "word": word,
                "reading": data["reading"],
                "hanviet": data["hanviet"],
                "meaning": data["meaning"]
            })
    return found

def process_file(file_path):
    print(f"[VOCAB] Processing: {os.path.basename(file_path)}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data.get('questions', [])
    updated_count = 0
    for q in questions:
        passage = q.get('passage', '')
        vocab_list = extract_vocab_for_passage(passage)
        q['vocabulary'] = vocab_list
        updated_count += len(vocab_list)
        print(f"  - {q.get('id', 'q')}: Extracted {len(vocab_list)} N1 vocabulary terms.")

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return updated_count

def run():
    print("=" * 60)
    print(" KOALA JLPT HUB - N1 DOKKAI VOCABULARY GENERATOR")
    print("=" * 60)

    # Process all JSON files in data/n1_dokkai/
    for folder in [DATA_DIR, PUBLIC_DATA_DIR]:
        if not os.path.exists(folder):
            continue
        for fn in os.listdir(folder):
            if fn.startswith('shinkanzen_') and fn.endswith('.json'):
                fp = os.path.join(folder, fn)
                process_file(fp)

    print("\n[SUCCESS] Vocabulary extraction completed successfully!")

if __name__ == '__main__':
    run()
