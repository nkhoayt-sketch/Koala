# 20日で合格 N1 文字・語彙・文法 (Web Quiz App - MVP)

Ứng dụng Web luyện thi JLPT N1 theo giáo trình **"20日で合格 N1 文字・語彙・文法"** với giao diện hiện đại (Clean UI), kiến trúc tách rời dữ liệu 100%, hỗ trợ chấm điểm tức thì và xuất báo cáo câu sai sang Anki.

---

## 📁 Cấu trúc thư mục

```text
N1_Quizz/
├── index.html            # Giao diện chính (Tailwind CSS + Google Fonts Noto Sans JP)
├── css/
│   └── style.css         # Typography tiếng Nhật, thanh cuộn tùy biến, hiệu ứng chuyển động
├── js/
│   ├── app.js            # Điều phối ứng dụng, nạp ngày, xử lý thanh tiến độ & menu
│   ├── quiz.js           # Engine render câu hỏi, kiểm tra đáp án, chấm điểm, bộ lọc
│   ├── storage.js        # Quản lý lưu trữ trạng thái làm bài (LocalStorage)
│   └── export.js         # Xuất báo cáo câu làm sai vào Clipboard / Anki
├── data/
│   ├── days-index.json   # Danh mục quản lý 20 ngày luyện thi
│   ├── day01.json        # Dữ liệu Ngày 1 (đầy đủ 14 câu chuẩn JLPT N1: 問題 1 - 7)
│   └── day02.json        # Template mẫu cho Ngày 2
├── server.ps1            # Web server nội bộ chạy bằng PowerShell (không cần cài thêm phần mềm)
├── start-server.bat      # File nhấp đúp chuột để chạy server nhanh trên Windows
└── README.md             # Tài liệu hướng dẫn sử dụng & phát triển
```

---

## 🚀 Cách chạy ứng dụng

### Cách 1: Nhấp đúp chuột (Khuyên dùng)
- Nhấp đúp vào file `start-server.bat`.
- Mở trình duyệt và truy cập: **`http://localhost:5500`**

### Cách 2: Chạy lệnh PowerShell
Mở PowerShell tại thư mục dự án và chạy:
```powershell
powershell -ExecutionPolicy Bypass -File .\server.ps1
```

---

## ✨ Tính năng nổi bật trong bản MVP

1. **Tách rời dữ liệu tuyệt đối**:
   - Mã nguồn không chứa câu hỏi cứng. Toàn bộ câu hỏi được tải động từ thư mục `data/`.
2. **Đầy đủ 7 dạng bài thi JLPT N1**:
   - **問題1: 漢字読み** (Cách đọc Kanji)
   - **問題2: 文脈規定** (Điền từ vựng theo ngữ cảnh)
   - **問題3: 言い換え類義** (Từ đồng nghĩa, cách diễn đạt tương đương)
   - **問題4: 用法** (Cách dùng từ chính xác trong câu)
   - **問題5: 文法形式の判断** (Phán đoán cấu trúc ngữ pháp)
   - **問題6: 文の組み立て** (Sắp xếp trật tự câu có dấu sao `★`)
   - **問題7: 文章の文法** (Ngữ pháp trong ngữ cảnh đoạn văn đọc hiểu)
3. **UI / UX hiện đại, tối ưu cho tiếng Nhật**:
   - Sử dụng font chữ chuẩn **Noto Sans JP** sắc nét.
   - Thẻ câu hỏi bo tròn mềm mại, hiệu ứng chọn mượt mà.
   - Thanh tiến độ (Progress Bar) cập nhật trực tiếp theo từng câu chọn.
4. **Chấm điểm & Phân tích thông minh**:
   - Nút **Nộp bài & Chấm điểm**: Tự động tính điểm, tỷ lệ % và xếp loại Đạt (合格)/Chưa đạt.
   - Tô màu trực quan: Đáp án đúng đổi màu xanh lá, đáp án người dùng chọn sai đổi màu đỏ.
   - Hộp **Giải thích chi tiết & Dịch nghĩa** tự động bung mở dưới mỗi câu.
   - Bộ lọc tiện lợi: Xem tất cả, chỉ xem câu sai, hoặc chỉ xem câu đúng.
5. **Xuất báo cáo câu sai sang Anki**:
   - Bấm nút **"Sao chép câu sai (Anki)"** để copy toàn bộ câu làm sai, đáp án đúng và lời giải thích vào Clipboard.
6. **Lưu trạng thái LocalStorage**:
   - Tự động lưu tiến độ làm bài, khi F5 trình duyệt không bị mất dữ liệu. Có nút **"Làm lại từ đầu"** để xóa tiến độ và thi lại.

---

## 📝 Cách bổ sung câu hỏi cho Ngày 2 đến Ngày 20

1. Tạo file mới `data/day02.json` (hoặc copy từ `day01.json`).
2. Điền các câu hỏi theo cấu trúc JSON:
   ```json
   {
     "id": "d02-q01",
     "number": 1,
     "section": "問題1: 漢字読み",
     "instruction": "＿＿の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。",
     "question": "Câu hỏi tiếng Nhật...",
     "options": ["Lựa chọn 1", "Lựa chọn 2", "Lựa chọn 3", "Lựa chọn 4"],
     "answer": 0,
     "explanation": "Giải thích chi tiết và dịch nghĩa..."
   }
   ```
   *(Lưu ý: `answer` là chỉ số index từ `0` đến `3` tương ứng với vị trí lựa chọn đúng).*
3. Mở `data/days-index.json`, đổi thuộc tính `"available": true` cho Ngày 2. Khi đó Sidebar sẽ tự động kích hoạt Ngày 2!
