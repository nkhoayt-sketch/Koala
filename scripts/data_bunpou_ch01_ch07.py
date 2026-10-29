# -*- coding: utf-8 -*-
"""
Shin Kanzen Master Bunpou N1 - Nhóm I: 事柄を説明する (Chương 01 -> Chương 07)
"""

CHAPTERS_01_07 = {
    "ch01": {
        "chapterId": "ch01",
        "lesson": "第1課: 時間関係 (Quan hệ thời gian)",
        "theme": "事柄を説明する",
        "group": "group1",
        "title": "第1課: 時間関係",
        "description": "Các mẫu ngữ pháp diễn tả hành động xảy ra gần như tức thì, liên tiếp hoặc kể từ một thời điểm: ～が早いか, ～や・～や否や, ～なり, ～そばから, ～てからというもの, ～にあって.",
        "questions": [
            {
                "id": "skz_b_ch01_q01",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～が早いか",
                "question": "落書きをしていた子供たちは、わたしの顔を（　）が早いか、逃げていった。",
                "options": ["a. 見て", "b. 見る", "c. 見るの"],
                "answer": "b",
                "explanation": "【Dịch】Những đứa trẻ đang vẽ bậy vừa thoáng thấy mặt tôi một cái là bỏ chạy thục mạng ngay lập tức.\n【Phân tích】Cấu trúc ～が早いか đi với V-る (hoặc V-た). Trong các đáp án chỉ có '見る' (b) là thể từ điển phù hợp.",
                "grammarRule": "V-る / V-た ＋ が早いか: Vừa mới... thì ngay lập tức hành động kế tiếp xảy ra. Vế sau là sự việc thực tế, không dùng ý chí, mệnh lệnh."
            },
            {
                "id": "skz_b_ch01_q02",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～が早いか",
                "question": "新しい化粧品が発売されるが早いか、（　）。",
                "options": ["a. 若い女性たちが殺到した", "b. 多くの女性に買ってほしい", "c. すぐに買ってください"],
                "answer": "a",
                "explanation": "【Dịch】Mỹ phẩm mới vừa mở bán một cái là phụ nữ trẻ lập tức đổ xô chen chúc mua.\n【Phân tích】Vế sau của ～が早いか không đi với mong muốn (たい/てほしい) hay mệnh lệnh (てください), mà chỉ sự thật khách quan diễn ra.",
                "grammarRule": "Vế sau của ～が早いか không đi với câu mệnh lệnh, rủ rê hay nguyện vọng."
            },
            {
                "id": "skz_b_ch01_q03",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～が早いか",
                "question": "新幹線が走り出すが早いか、（　）。",
                "options": ["a. みんなでお弁当を食べよう", "b. みんなとても楽しそうだった", "c. 彼はビールを飲み始めた"],
                "answer": "c",
                "explanation": "【Dịch】Tàu Shinkansen vừa mới lăn bánh chạy một cái là anh ấy đã bắt đầu khui bia uống ngay.\n【Phân tích】(a) mang tính rủ rê (〜よう), (b) chỉ trạng thái tĩnh, chỉ (c) miêu tả hành động xảy ra ngay tức thì sau khi tàu chạy.",
                "grammarRule": "Vế sau biểu thị hành động diễn ra nối tiếp ngay sau vế trước."
            },
            {
                "id": "skz_b_ch01_q04",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～や・～や否や",
                "question": "本格的に絵の勉強を（　）や、彼のデッサン力はみるみる上がった。",
                "options": ["a. している", "b. 始める", "c. 続ける"],
                "answer": "b",
                "explanation": "【Dịch】Vừa mới bắt tay vào học hội họa bài bản, khả năng phác họa (dessin) của anh ấy đã tiến bộ trông thấy.\n【Phân tích】Cấu trúc ～や / ～や否や kết hợp với động từ thể từ điển (V-る).",
                "grammarRule": "V-る ＋ や / や否や: Vừa mới... thì ngay lập tức (phản ứng/biến đổi xảy ra chớp nhoáng)."
            },
            {
                "id": "skz_b_ch01_q05",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～や・～や否や",
                "question": "サイレンが鳴るや、（　）。",
                "options": ["a. すぐ飛び出そう", "b. 消防車が出動した", "c. 校庭に集合しなさい"],
                "answer": "b",
                "explanation": "【Dịch】Còi báo động vừa ré lên một cái là xe cứu hỏa lập tức xuất phát.\n【Phân tích】Vế sau không dùng mệnh lệnh (c) hay rủ rê (a), chỉ dùng sự kiện khách quan đã diễn ra.",
                "grammarRule": "Vế sau không thể hiện ý chí, mệnh lệnh, rủ rê của người nói."
            },
            {
                "id": "skz_b_ch01_q06",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～や・～や否や",
                "question": "太郎はアニメを一本見終わるや否や、（　）。",
                "options": ["a. 将来はアニメの仕事をしたいらしい", "b. 今ではアニメがとても好きだ", "c. 別のアニメを借りにレンタルショップに行った"],
                "answer": "c",
                "explanation": "【Dịch】Taro vừa xem xong một tập anime là đã phóng ngay ra tiệm thuê đĩa để mượn bộ khác.\n【Phân tích】Vế sau diễn tả hành vi tức thì nối tiếp sau hành động kết thúc tập phim.",
                "grammarRule": "Diễn tả hành vi nối tiếp tức thì của chủ thể."
            },
            {
                "id": "skz_b_ch01_q07",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～なり",
                "question": "（　）は食卓に着くなり、ものすごい勢いで食べ始めた。",
                "options": ["a. わたし", "b. わたしたち", "c. 山川さん"],
                "answer": "c",
                "explanation": "【Dịch】Anh Yamakawa vừa ngồi vào bàn ăn một cái là bắt đầu ăn lấy ăn để với tốc độ khủng khiếp.\n【Phân tích】Chủ ngữ của cấu trúc ～なり bắt buộc phải là ngôi thứ ba (山川さん), không dùng cho ngôi thứ nhất (わたし/わたしたち).",
                "grammarRule": "V-る ＋ なり: Chủ ngữ thường là ngôi thứ ba, vế trước và vế sau cùng một chủ thể thực hiện."
            },
            {
                "id": "skz_b_ch01_q08",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～なり",
                "question": "その動物を一目（　）なり、みんなその場から逃げ出した。",
                "options": ["a. 見る", "b. 見た", "c. 見て"],
                "answer": "a",
                "explanation": "【Dịch】Vừa thoáng thấy con vật ấy một cái, mọi người liền tháo chạy khỏi nơi đó.\n【Phân tích】～なり kết hợp trực tiếp với động từ thể từ điển V-る (見るなり).",
                "grammarRule": "V-る ＋ なり: Vừa mới làm... thì liền làm hành động tiếp theo."
            },
            {
                "id": "skz_b_ch01_q09",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～なり",
                "question": "ゆき子は駅に着くなり、（　）。",
                "options": ["a. 切符を買った", "b. 電車の時刻表を見た", "c. 駅員室に駆け込んだ"],
                "answer": "c",
                "explanation": "【Dịch】Yukiko vừa đến ga một cái là chạy thốc ngay vào phòng trực ga.\n【Phân tích】～なり thường dùng cho những hành vi bất ngờ, đột ngột, khác thường chứ không dùng cho các việc tuần tự bình thường như mua vé hay xem giờ.",
                "grammarRule": "Vế sau mang tính chất bất ngờ hoặc phản ứng cảm xúc bột phát của chủ thể."
            },
            {
                "id": "skz_b_ch01_q10",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～そばから",
                "question": "あの店のパンは評判が良く、焼き上がるそばから（　）売れていく。",
                "options": ["a. どんどん", "b. 次第に", "c. そのうち"],
                "answer": "a",
                "explanation": "【Dịch】Bánh mì tiệm đó rất được khen, vừa nướng xong mẻ nào là bán hết veo ngay mẻ đó.\n【Phân tích】～そばから đi với phó từ nhấn mạnh tính dồn dập, liên tục 'どんどん'.",
                "grammarRule": "V-る / V-た ＋ そばから: Vừa mới làm... thì ngay lập tức hành động đối nghịch/lặp lại diễn ra dồn dập."
            },
            {
                "id": "skz_b_ch01_q11",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～そばから",
                "question": "わたしは（　）そばから人の名前を忘れてしまう。",
                "options": ["a. わかった", "b. 聞いた", "c. 知っている"],
                "answer": "b",
                "explanation": "【Dịch】Tôi cứ vừa nghe xong tên người ta là quên bẵng đi mất ngay.\n【Phân tích】'Nghe tên' (聞いた) đi với そばから diễn tả sự lặp đi lặp lại một kết quả đáng tiếc.",
                "grammarRule": "Thường dùng với ý nghĩa phàn nàn, tiếc nuối khi một kết quả xấu liên tục lặp lại."
            },
            {
                "id": "skz_b_ch01_q12",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～そばから",
                "question": "（　）そばから新しいのが欲しくなる。",
                "options": ["a. 家を建てた", "b. 服を買った", "c. テレビが壊れた"],
                "answer": "b",
                "explanation": "【Dịch】Cứ vừa mua quần áo xong là lại thèm mua cái mới ngay.\n【Phân tích】Hành động mua sắm (服を買った) diễn ra thường xuyên nhiều lần, phù hợp tính chất tuần hoàn của そばから.",
                "grammarRule": "Hành vi được đề cập mang tính lặp đi lặp lại nhiều lần trong đời sống."
            },
            {
                "id": "skz_b_ch01_q13",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～てからというもの",
                "question": "（　）というもの、体の調子がいい。",
                "options": ["a. 朝起きてから", "b. たばこをやめてから", "c. さっき薬を飲んでから"],
                "answer": "b",
                "explanation": "【Dịch】Kể từ ngày bỏ thuốc lá đến nay, thể trạng sức khỏe của tôi rất tốt.\n【Phân tích】～てからというもの chỉ một mốc biến cố quan trọng dẫn đến trạng thái kéo dài liên tục tới hiện tại. Bỏ thuốc lá là bước ngoặt dài hạn.",
                "grammarRule": "V-て ＋ からというもの: Kể từ sau khi một sự kiện xảy ra, trạng thái đó kéo dài liên tục mãi về sau."
            },
            {
                "id": "skz_b_ch01_q14",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～てからというもの",
                "question": "あの先生の話を聞いてからというもの、（　）。",
                "options": ["a. 人生についていろいろ考えている", "b. 先生の著書を3冊買った", "c. 先生の考えに同感した"],
                "answer": "a",
                "explanation": "【Dịch】Kể từ khi nghe lời thầy dặn, tôi liên tục suy nghĩ trăn trở nhiều điều về cuộc đời.\n【Phân tích】Vế sau phải là trạng thái tiếp diễn kéo dài (〜考えている), không phải hành động kết thúc dứt điểm.",
                "grammarRule": "Vế sau luôn là trạng thái kéo dài tiếp diễn (thường ở dạng V-ている)."
            },
            {
                "id": "skz_b_ch01_q15",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～てからというもの",
                "question": "会社を辞めてからというもの、（　）。",
                "options": ["a. 新しい仕事を始めた", "b. 初めて外国旅行をした", "c. 毎日のように釣りをしている"],
                "answer": "c",
                "explanation": "【Dịch】Kể từ ngày nghỉ việc ở công ty, hầu như ngày nào tôi cũng đi câu cá thư giãn.\n【Phân tích】'毎日のように釣りをしている' là nếp sinh hoạt trạng thái kéo dài liên tục.",
                "grammarRule": "Vế sau diễn tả thói quen hoặc trạng thái duy trì đều đặn sau mốc sự kiện."
            },
            {
                "id": "skz_b_ch01_q16",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～にあって",
                "question": "木村氏は（　）にあって、日々多忙なスケジュールをこなしている。",
                "options": ["a. 一の指導者", "b. 一国の指導者という立場", "c. 二つの仕事"],
                "answer": "b",
                "explanation": "【Dịch】Ông Kimura, ở vào cương vị là một nhà lãnh đạo quốc gia, đang ngày ngày hoàn thành lịch trình vô cùng bận rộn.\n【Phân tích】～にあって đi với danh từ chỉ tình huống, vị thế, hoàn cảnh đặc biệt (一国の指導者という立場).",
                "grammarRule": "N ＋ にあって: Ở trong hoàn cảnh, tình huống, cương vị đặc biệt đó."
            },
            {
                "id": "skz_b_ch01_q17",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～にあって",
                "question": "母は（　）にあって、子供たちのことを心配している。",
                "options": ["a. 病床", "b. 仕事中", "c. 多忙な日常"],
                "answer": "a",
                "explanation": "【Dịch】Mẹ dù đang nằm trên giường bệnh (hoàn cảnh ngặt nghèo) vẫn luôn lo lắng cho các con.\n【Phân tích】'病床' (giường bệnh) là hoàn cảnh khó khăn đặc biệt, rất tiêu biểu cho cấu trúc ～にあって.",
                "grammarRule": "Thường dùng trong văn viết, thể hiện sự việc xảy ra trong hoàn cảnh đặc thù."
            },
            {
                "id": "skz_b_ch01_q18",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "～にあって",
                "question": "このような緊急時にあっても、（　）。",
                "options": ["a. 彼は驚いている", "b. わたしは彼を探した", "c. 彼は落ち着いている"],
                "answer": "c",
                "explanation": "【Dịch】Ngay cả khi đang ở trong tình huống khẩn cấp như thế này, anh ấy vẫn vô cùng điềm tĩnh.\n【Phân tích】～にあっても nhấn mạnh sự việc vế sau vẫn diễn ra dù trong hoàn cảnh ngặt nghèo.",
                "grammarRule": "N ＋ にあっても: Dù trong hoàn cảnh đặc biệt như vậy nhưng..."
            },
            {
                "id": "skz_b_ch01_q19",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "第1課 総合問題",
                "question": "彼は不正が（　）退職した。",
                "options": ["a. ばれるが早いか", "b. ばれてからというもの", "c. ばれるそばから"],
                "answer": "a",
                "explanation": "【Dịch】Vừa bị lộ hành vi gian lận một cái là anh ta lập tức từ chức ngay.\n【Phân tích】Hành động từ chức diễn ra chớp nhoáng nối tiếp sau sự việc bại lộ -> ～が早いか.",
                "grammarRule": "V-る ＋ が早いか: Vừa mới... thì ngay lập tức."
            },
            {
                "id": "skz_b_ch01_q20",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "第1課 総合問題",
                "question": "父はわたしの顔を一目（　）笑い出した。",
                "options": ["a. 見てからというもの", "b. 見るなり", "c. 見たそばから"],
                "answer": "b",
                "explanation": "【Dịch】Bố vừa thoáng nhìn thấy mặt tôi một cái là bật cười toe toét.\n【Phân tích】Vừa làm V xong là hành động kế tiếp bột phát ngay -> V-る ＋ なり.",
                "grammarRule": "V-る ＋ なり: Ngay sau khi... thì hành vi tiếp theo diễn ra."
            },
            {
                "id": "skz_b_ch01_q21",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "第1課 総合問題",
                "question": "片付ける（　）、子供たちがまた部屋を散らかす。",
                "options": ["a. が早いか", "b. そばから", "c. なり"],
                "answer": "b",
                "explanation": "【Dịch】Cứ vừa dọn dẹp xong là tụi trẻ lại bày bừa ra khắp phòng.\n【Phân tích】Sự việc lặp đi lặp lại mang tính chất bực bội, bất lực -> そばから.",
                "grammarRule": "V-る ＋ そばから: Vừa mới làm xong thì lại bị lặp lại như cũ."
            },
            {
                "id": "skz_b_ch01_q22",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "第1課 総合問題",
                "question": "サッカーのワールドカップを一度（　）、僕はサッカーに夢中になっている。",
                "options": ["a. 見るや否や", "b. 見るなり", "c. 見てからというもの"],
                "answer": "c",
                "explanation": "【Dịch】Kể từ sau lần xem World Cup bóng đá đến nay, tôi hoàn toàn mê mẩn môn thể thao này.\n【Phân tích】Đam mê kéo dài liên tục tới hiện tại -> ～てからというもの.",
                "grammarRule": "V-て ＋ からというもの: Kể từ khi... thì trạng thái kéo dài liên tục."
            },
            {
                "id": "skz_b_ch01_q23",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "第1課 総合問題",
                "question": "入場の受け付けが（　）、係の人たちは急に忙しくなった。",
                "options": ["a. 始まるや否や", "b. 始まってからというもの", "c. 始まるそばから"],
                "answer": "a",
                "explanation": "【Dịch】Vừa mới bắt đầu giờ tiếp nhận vào cửa thì các nhân viên phụ trách đã bận rộn đột ngột.\n【Phân tích】Biến đổi tình thế diễn ra tức thì ngay khi mở cửa -> ～や否や.",
                "grammarRule": "V-る ＋ や否や: Vừa mới... thì ngay lập tức."
            },
            {
                "id": "skz_b_ch01_q24",
                "lesson": "第1課: 時間関係",
                "grammarPoint": "第1課 総合問題",
                "question": "行方不明の子が見つかったという知らせが（　）、家族は泣き出した。",
                "options": ["a. 入るや", "b. 入るそばから", "c. 入ってからというもの"],
                "answer": "a",
                "explanation": "【Dịch】Vừa nhận được tin đứa trẻ mất tích đã được tìm thấy, gia đình liền òa khóc nức nở.\n【Phân tích】Phản ứng cảm xúc òa khóc xảy ra ngay lúc tin vừa đến -> V-る ＋ や.",
                "grammarRule": "V-る ＋ や: Vừa mới... là tức thì phản ứng."
            }
        ]
    },
    "ch02": {
        "chapterId": "ch02",
        "lesson": "第2課: 範囲の始まり・限度 (Khởi đầu phạm vi & Giới hạn)",
        "theme": "事柄を説明する",
        "group": "group1",
        "title": "第2課: 範囲の始まり・限度",
        "description": "Các mẫu ngữ pháp diễn tả điểm bắt đầu mở màn, giới hạn tối đa hoặc đánh giá mức độ: ～を皮切りに(して), ～に至るまで, ～を限りに, ～をもって, ～といったところだ.",
        "questions": [
            {
                "id": "skz_b_ch02_q01",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～を皮切りに(して)",
                "question": "その宇宙飛行士の講演会は（　）を皮切りに、10か所で行われた。",
                "options": ["a. 北海道", "b. 外国", "c. 全国"],
                "answer": "a",
                "explanation": "【Dịch】Buổi diễn thuyết của nhà du hành vũ trụ đó bắt đầu mở màn từ Hokkaido, sau đó được tổ chức tại 10 địa điểm tiếp theo.\n【Phân tích】～を皮切りに bắt đầu từ một địa điểm/hành động cụ thể rồi lan rộng ra các điểm khác. '北海道' là địa điểm khởi đầu cụ thể.",
                "grammarRule": "N ＋ を皮切りに(して) / を皮切りとして: Khởi đầu bằng... sau đó hàng loạt hành động tương tự liên tiếp diễn ra trên quy mô lớn."
            },
            {
                "id": "skz_b_ch02_q02",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～を皮切りに(して)",
                "question": "この選手は昨年の地区大会入賞を皮切りに、（　）。",
                "options": ["a. ますます練習に励んでいる", "b. 今年も入賞が期待される", "c. いくつもの大会で好成績を残している"],
                "answer": "c",
                "explanation": "【Dịch】Kể từ giải thưởng khu vực năm ngoái mở đầu, vận động viên này liên tiếp gặt hái thành tích tốt tại nhiều giải đấu khác.\n【Phân tích】Vế sau phải thể hiện chuỗi thành tích/hành động nở rộ tiếp nối (いくつもの大会で好成績を残している).",
                "grammarRule": "Vế sau luôn diễn tả các sự việc cùng loại liên tiếp phát triển bùng nổ theo chiều hướng tích cực."
            },
            {
                "id": "skz_b_ch02_q03",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～を皮切りに(して)",
                "question": "山田さんの発言を皮切りにして、（　）。",
                "options": ["a. 皆さんが意見を言ってください", "b. みんなが次々に意見を言った", "c. 川田さんも意見を言った"],
                "answer": "b",
                "explanation": "【Dịch】Mở màn bằng phát biểu của anh Yamada, mọi người đã lần lượt đua nhau đưa ra ý kiến.\n【Phân tích】Vế sau diễn tả chuỗi hành động của nhiều người tiếp nối nhau (次々に意見を言った).",
                "grammarRule": "Đi kèm với các hành động diễn ra liên tiếp, nối đuôi nhau."
            },
            {
                "id": "skz_b_ch02_q04",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～を皮切りに(して)",
                "question": "中川さんは10年前の個展を皮切りとして、（　）。",
                "options": ["a. いろいろなところで個展を開いている", "b. その後2度個展を開いた", "c. 1度も個展を開いていない"],
                "answer": "a",
                "explanation": "【Dịch】Lấy triển lãm cá nhân 10 năm trước làm bước khởi đầu, anh Nakagawa đã liên tục mở triển lãm ở rất nhiều nơi.\n【Phân tích】Cấu trúc biểu thị chuỗi hoạt động mở rộng liên tiếp (いろいろなところで).",
                "grammarRule": "Diễn tả chuỗi sự kiện được nhân rộng ra nhiều lần sau mốc khởi đầu."
            },
            {
                "id": "skz_b_ch02_q05",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～に至るまで",
                "question": "小林先生には卒業後の進路はもちろん、（　）に至るまで何でも相談している。",
                "options": ["a. 勉強", "b. 宿題のやり方", "c. 恋愛の悩み"],
                "answer": "c",
                "explanation": "【Dịch】Với thầy Kobayashi, không chỉ định hướng nghề nghiệp sau tốt nghiệp mà ngay cả chuyện tình cảm tôi cũng tâm sự hết với thầy.\n【Phân tích】～に至るまで nhấn mạnh phạm vi mở rộng tới mức bất ngờ, việc thầm kín cá nhân (恋愛の悩み).",
                "grammarRule": "N ＋ に至るまで: Đến tận... (nhấn mạnh phạm vi mở rộng tới cả những chi tiết vụn vặt, bất ngờ ngoài dự kiến)."
            },
            {
                "id": "skz_b_ch02_q06",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～に至るまで",
                "question": "外国で暮らすことになったので、（　）に至るまでみんなリサイクルショップに売った。",
                "options": ["a. ベッドからスプーン", "b. 皿からカップ", "c. 雑誌から本"],
                "answer": "a",
                "explanation": "【Dịch】Vì sắp sang nước ngoài sinh sống, tôi đã bán sạch mọi thứ ở tiệm đồ cũ từ cái giường lớn cho đến tận cái thìa nhỏ nhất.\n【Phân tích】Mô hình 'AからBに至るまで' với A là vật lớn/chính và B là tiểu tiết nhỏ nhặt nhất.",
                "grammarRule": "Aから Bに至るまで: Từ cái to lớn cho đến tận cái tỉ mỉ, nhỏ bé nhất."
            },
            {
                "id": "skz_b_ch02_q07",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～に至るまで",
                "question": "ゆみさんは天気はもちろん、（　）に至るまで日記に書き留めているそうだ。",
                "options": ["a. その日の自分の行動", "b. その日の朝、昼、晩の気温", "c. その日の出来事"],
                "answer": "b",
                "explanation": "【Dịch】Yumi không chỉ ghi thời tiết mà nghe nói đến tận nhiệt độ sáng, trưa, tối trong ngày cô ấy cũng ghi chép cẩn thận vào nhật ký.\n【Phân tích】'Nhiệt độ sáng trưa tối' là chi tiết cực kỳ tỉ mỉ, nhấn mạnh phạm vi sâu sát.",
                "grammarRule": "Nhấn mạnh mức độ chi tiết đến tận cùng sự việc."
            },
            {
                "id": "skz_b_ch02_q08",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～を限りに",
                "question": "この店は（　）を限りに閉店するそうだ。",
                "options": ["a. 今月", "b. 今月まで", "c. あと一月"],
                "answer": "a",
                "explanation": "【Dịch】Cửa hàng này nghe nói sẽ đóng cửa hết tháng này là chấm dứt.\n【Phân tích】～を限りに kết hợp trực tiếp với danh từ chỉ thời gian mốc (今月 / 今日 / 今回).",
                "grammarRule": "N (thời gian) ＋ を限りに: Hết... là chấm dứt (thông báo kết thúc dứt khoát một hoạt động duy trì từ trước)."
            },
            {
                "id": "skz_b_ch02_q09",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～を限りに",
                "question": "わたしは今日を限りに（　）。",
                "options": ["a. この会社の社員です", "b. この会社を辞めます", "c. 新しい会社に入社します"],
                "answer": "b",
                "explanation": "【Dịch】Tôi kể từ hết ngày hôm nay sẽ chính thức nghỉ việc ở công ty này.\n【Phân tích】Vế sau diễn tả hành động chấm dứt tình trạng hiện tại (この会社を辞めます).",
                "grammarRule": "Diễn tả tuyên bố dứt khoát dừng một việc đã làm bấy lâu."
            },
            {
                "id": "skz_b_ch02_q10",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～を限りに",
                "question": "あの高校は今年を限りに（　）ことになっている。",
                "options": ["a. 開校される", "b. 生徒数が増加する", "c. 生徒を募集しない"],
                "answer": "c",
                "explanation": "【Dịch】Trường cấp ba đó hết năm nay sẽ dừng không tuyển sinh học sinh nữa.\n【Phân tích】Dừng tuyển sinh (生徒を募集しない) là hành động kết thúc dứt điểm.",
                "grammarRule": "Chỉ thời điểm chấm dứt hiệu lực hoặc hoạt động."
            },
            {
                "id": "skz_b_ch02_q11",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～をもって",
                "question": "（　）をもちまして本日の演説会は終了いたします。",
                "options": ["a. 以上", "b. 以下", "c. 以後"],
                "answer": "a",
                "explanation": "【Dịch】Kể từ thời điểm này, tôi xin phép được kết thúc buổi diễn thuyết ngày hôm nay.\n【Phân tích】Cụm từ cố định trong thông báo trang trọng: 以上をもちまして (Xin kết thúc tại đây).",
                "grammarRule": "N ＋ をもって / をもちまして: Tại mốc thời điểm này / Bằng cách này (văn phong nghi lễ, thông báo chính thức)."
            },
            {
                "id": "skz_b_ch02_q12",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～をもって",
                "question": "3月末日をもって（　）。",
                "options": ["a. このサービスを開始いたします", "b. このサービスは停止させていただきます", "c. このサービスはございません"],
                "answer": "b",
                "explanation": "【Dịch】Kể từ ngày cuối cùng của tháng 3, chúng tôi xin phép ngừng cung cấp dịch vụ này.\n【Phân tích】Chỉ thời điểm dứt khoát kết thúc một chế độ/dịch vụ.",
                "grammarRule": "Thường dùng trong các thông báo chính thức của cơ quan, doanh nghiệp về hạn chót."
            },
            {
                "id": "skz_b_ch02_q13",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～をもって",
                "question": "これをもって本日の役員会は（　）したいと思いま す。",
                "options": ["a. 休憩", "b. 開会", "c. 閉会"],
                "answer": "c",
                "explanation": "【Dịch】Tại thời điểm này tôi xin phép bế mạc cuộc họp hội đồng quản trị hôm nay.\n【Phân tích】'これをもって...閉会いたします' là mẫu câu bế mạc hội nghị kinh điển.",
                "grammarRule": "Dùng trong các nghi lễ trang trọng để tuyên bố kết thúc hoặc chuyển tiếp."
            },
            {
                "id": "skz_b_ch02_q14",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～をもって",
                "question": "今期をもって私は（　）。",
                "options": ["a. この職に転職します", "b. この職を引退します", "c. この職を続けます"],
                "answer": "b",
                "explanation": "【Dịch】Hết nhiệm kỳ này tôi xin chính thức rút lui khỏi chức vụ này.\n【Phân tích】'この職を引退します' thể hiện mốc dừng lại chức vụ.",
                "grammarRule": "Chỉ mốc thời gian chuyển giao hoặc chấm dứt nhiệm kỳ."
            },
            {
                "id": "skz_b_ch02_q15",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～といったところだ",
                "question": "わたしの睡眠時間は（　）といったところです。",
                "options": ["a. 十分", "b. もう少し欲しい", "c. 5時間"],
                "answer": "c",
                "explanation": "【Dịch】Thời gian ngủ của tôi áng chừng cũng chỉ tầm cỡ 5 tiếng là cùng.\n【Phân tích】～といったところだ đi với con số cụ thể thể hiện ước lượng vừa phải hoặc hơi khiêm tốn (5時間).",
                "grammarRule": "N / V-る ＋ といったところだ: Đại khái cũng chỉ tầm cỡ... / Cao nhất cũng khoảng đó (ước lượng mức độ tối đa không quá cao)."
            },
            {
                "id": "skz_b_ch02_q16",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～といったところだ",
                "question": "毎日の運動といえば、近所を走るといったところなので、（　）。",
                "options": ["a. とても疲れる", "b. 40分もかかる", "c. 無理なく続けられる"],
                "answer": "c",
                "explanation": "【Dịch】Vận động hằng ngày của tôi cũng chỉ cỡ chạy quanh xóm một chút, nên có thể duy trì nhẹ nhàng mà không quá sức.\n【Phân tích】'といったところ' mang hàm ý mức độ nhẹ nhàng, vừa phải, nên kết quả là '무리なく続けられる'.",
                "grammarRule": "Hàm ý mức độ khiêm tốn, vừa phải, không có gì to tát."
            },
            {
                "id": "skz_b_ch02_q17",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "～といったところだ",
                "question": "このクラスのテストの平均点は、毎回（　）67、8点といったところです。",
                "options": ["a. せめて", "b. せいぜい", "c. 最低でも"],
                "answer": "b",
                "explanation": "【Dịch】Điểm trung bình bài kiểm tra lớp này mỗi lần cùng lắm cũng chỉ cỡ chừng 67 hay 68 điểm là căng.\n【Phân tích】'せいぜい' (cùng lắm là, tối đa là) đi kèm rất tự nhiên với といったところだ.",
                "grammarRule": "Thường đi kèm với phó từ せいぜい để nhấn mạnh mức trần khiêm tốn."
            },
            {
                "id": "skz_b_ch02_q18",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "第2課 総合問題",
                "question": "全国高校野球大会は、一昨日の第一試合（　）連日熱戦が繰り広げられている。",
                "options": ["a. を皮切りに", "b. に至るまで", "c. をもって"],
                "answer": "a",
                "explanation": "【Dịch】Giải bóng chày trung học toàn quốc bắt đầu mở màn từ trận đấu số 1 hôm kia, các trận đấu nảy lửa đang diễn ra liên tiếp từng ngày.\n【Phân tích】Trận mở màn dẫn tới chuỗi các trận liên tiếp -> ～を皮切りに.",
                "grammarRule": "N ＋ を皮切りに: Khởi đầu bằng... sau đó chuỗi sự việc tiếp nối bùng nổ."
            },
            {
                "id": "skz_b_ch02_q19",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "第2課 総合問題",
                "question": "今日（　）もう車は運転しないことにしたんです。",
                "options": ["a. を限りに", "b. をもって", "c. に至るまで"],
                "answer": "a",
                "explanation": "【Dịch】Tôi đã quyết định hết ngày hôm nay là tuyệt đối không lái xe ô tô nữa.\n【Phân tích】Quyết định dứt khoát kết thúc một việc làm thường ngày -> 今日を限りに.",
                "grammarRule": "N (thời gian) ＋ を限りに: Hết... là chấm dứt dứt khoát."
            },
            {
                "id": "skz_b_ch02_q20",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "第2課 総合問題",
                "question": "ただ今（　）チケットの販売を打ち切らせていただきます。",
                "options": ["a. を皮切りに", "b. をもって", "c. に至るまで"],
                "answer": "b",
                "explanation": "【Dịch】Kể từ đúng thời điểm này, chúng tôi xin phép dừng việc bán vé.\n【Phân tích】Thông báo thời điểm kết thúc trang trọng, lịch sự -> ただ今をもって.",
                "grammarRule": "N ＋ をもって: Tại thời điểm này (văn phong thông báo chính thức)."
            },
            {
                "id": "skz_b_ch02_q21",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "第2課 総合問題",
                "question": "日常のおかずから高級料理の食材（　）、この店にないものはない。",
                "options": ["a. をもって", "b. といったところで", "c. に至るまで"],
                "answer": "c",
                "explanation": "【Dịch】Từ món ăn kèm bình dân thường ngày cho đến tận nguyên liệu cao cấp của tiệm ăn sang trọng, quán này cái gì cũng có.\n【Phân tích】Từ A đến tận B -> AからBに至るまで.",
                "grammarRule": "Aから Bに至るまで: Từ A đến tận B (phạm vi mở rộng tối đa)."
            },
            {
                "id": "skz_b_ch02_q22",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "第2課 総合問題",
                "question": "3歳の息子がやってくれる手伝いは、洗濯物をかごに入れるとか新聞を運ぶ（　）、あまり役に立ちません。",
                "options": ["a. に至るまで", "b. といったところで", "c. をもって"],
                "answer": "b",
                "explanation": "【Dịch】Việc phụ giúp của cậu con trai 3 tuổi của tôi đại khái cũng chỉ cỡ bỏ quần áo vào giỏ hay cầm tờ báo, chứ chẳng giúp được gì nhiều.\n【Phân tích】Ước lượng mức độ nhỏ nhặt, không đáng kể -> といったところで.",
                "grammarRule": "N ＋ といったところで: Đại khái cũng chỉ tầm cỡ..."
            },
            {
                "id": "skz_b_ch02_q23",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "第2課 総合問題",
                "question": "今月20日（　）願書の受付を締め切ります。",
                "options": ["a. を皮切りに", "b. をもって", "c. といったところで"],
                "answer": "b",
                "explanation": "【Dịch】Hạn chót tiếp nhận đơn xin nhập học sẽ kết thúc vào ngày 20 tháng này.\n【Phân tích】Hạn chót chính thức trong hành chính -> ～をもって.",
                "grammarRule": "N (ngày tháng) ＋ をもって: Hạn chót chính thức."
            },
            {
                "id": "skz_b_ch02_q24",
                "lesson": "第2課: 範囲の始まり・限度",
                "grammarPoint": "第2課 総合問題",
                "question": "彼は北海道（　）沖縄に至るまで、日本全国をヒッチハイクで旅した。",
                "options": ["a. を限りに", "b. を皮切りに", "c. から"],
                "answer": "c",
                "explanation": "【Dịch】Anh ấy đã đi nhờ xe du lịch khắp nước Nhật từ Hokkaido cho đến tận Okinawa.\n【Phân tích】Đi cùng '～に至るまで' là từ chỉ xuất phát điểm '～から'.",
                "grammarRule": "N1から N2に至るまで: Từ N1 đến tận N2."
            }
        ]
    },
    "ch03": {
        "chapterId": "ch03",
        "lesson": "第3課: 限定・非限定・付加 (Giới hạn, không giới hạn & Bổ sung)",
        "theme": "事柄を説明する",
        "group": "group1",
        "title": "第3課: 限定・非限定・付加",
        "description": "Các mẫu ngữ pháp: ～をおいて, ～ならでは, ～にとどまらず, ～はおろか, ～もさることながら.",
        "questions": [
            {
                "id": "skz_b_ch03_q01",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "～をおいて",
                "question": "これほど多種多様な機能を持ったものは、わが社の（　）をおいてほかにありません。",
                "options": ["a. この製品", "b. 製品の開発", "c. 技術力"],
                "answer": "a",
                "explanation": "【Dịch】Sản phẩm sở hữu nhiều chức năng đa dạng đến mức này thì ngoài sản phẩm này của công ty chúng tôi ra, không thể có sản phẩm nào khác.\n【Phân tích】～をおいてほかにない (ngoại trừ X ra thì không có ai/cái gì khác), vế trước là đối tượng độc nhất.",
                "grammarRule": "N ＋ をおいて (ほかに...ない): Ngoại trừ N ra thì không có gì/ai khác sánh bằng."
            },
            {
                "id": "skz_b_ch03_q02",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "～をおいて",
                "question": "この大役を任せられる人は、あなた（　）をおいてほかにいません。",
                "options": ["a. の能力", "b. を", "c. のほかに"],
                "answer": "b",
                "explanation": "【Dịch】Người có thể giao phó trọng trách lớn lao này thì ngoại trừ bạn ra không có ai khác.\n【Phân tích】'あなたをおいてほかにいない'. Cấu trúc trực tiếp đi với danh từ chỉ đối tượng duy nhất.",
                "grammarRule": "N ＋ をおいて: Nhấn mạnh sự đánh giá cao nhất dành cho đối tượng duy nhất."
            },
            {
                "id": "skz_b_ch03_q03",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "～ならでは",
                "question": "こんな素晴らしい料理は、一流のシェフ（　）ならでは作れない。",
                "options": ["a. だけ", "b. だから", "c. "],
                "answer": "c",
                "explanation": "【Dịch】Món ăn tuyệt hảo đến nhường này thì chỉ có thể là đầu bếp bậc nhất mới làm nổi.\n【Phân tích】N ＋ ならでは (đặc sắc chỉ có ở N). Ở đây 'シェフならでは' kết hợp trực tiếp.",
                "grammarRule": "N ＋ ならでは (のN) / ならでは...ない: Chỉ có ở N mới có được giá trị/nét đặc sắc tuyệt vời ấy."
            },
            {
                "id": "skz_b_ch03_q04",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "～ならでは",
                "question": "地元の人たち（　）ならではの温かいもてなしを受けた。",
                "options": ["a. ", "b. に", "c. の"],
                "answer": "a",
                "explanation": "【Dịch】Chúng tôi đã nhận được sự đón tiếp nồng hậu đậm chất ấm áp chỉ có ở người dân địa phương.\n【Phân tích】N ＋ ならではの ＋ N: Nならではの温かいもてなし.",
                "grammarRule": "N ＋ ならではの ＋ N: Nét đặc trưng tuyệt vời chỉ có ở..."
            },
            {
                "id": "skz_b_ch03_q05",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "～にとどまらず",
                "question": "このアニメは日本国内（　）にとどまらず、世界中で大ヒットしている。",
                "options": ["a. ", "b. の", "c. に"],
                "answer": "a",
                "explanation": "【Dịch】Bộ anime này không chỉ dừng lại trong phạm vi nội địa Nhật Bản mà còn tạo nên cơn sốt vang dội trên toàn thế giới.\n【Phân tích】N ＋ にとどまらず: Không chỉ giới hạn trong phạm vi N mà còn lan rộng ra phạm vi lớn hơn.",
                "grammarRule": "N / V-る ＋ にとどまらず: Không chỉ dừng lại ở phạm vi đó mà còn lan rộng ra."
            },
            {
                "id": "skz_b_ch03_q06",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "～にとどまらず",
                "question": "火山噴火の影響は周辺地域にとどまらず、（　）。",
                "options": ["a. すぐに収まるだろう", "b. 被害は軽微だった", "c. 国全体に及んでいる"],
                "answer": "c",
                "explanation": "【Dịch】Ảnh hưởng của vụ phun trào núi lửa không chỉ dừng lại ở khu vực xung quanh mà còn lan rộng ra toàn bộ đất nước.\n【Phân tích】Vế sau mở rộng quy mô nghiêm trọng hơn: 国全体に及んでいる.",
                "grammarRule": "Vế sau là phạm vi rộng lớn hơn, nghiêm trọng hơn vế trước."
            },
            {
                "id": "skz_b_ch03_q07",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "～はおろか",
                "question": "彼は自分の名前（　）はおろか、住所さえ言えない状態だ。",
                "options": ["a. ", "b. を", "c. に"],
                "answer": "a",
                "explanation": "【Dịch】Anh ấy đang trong tình trạng ngay cả tên của bản thân còn chưa nói được, huống chi là địa chỉ nhà.\n【Phân tích】AはおろかBも/さえ: B (điều hiển nhiên đơn giản) còn chưa được, huống chi A (điều phức tạp hơn).",
                "grammarRule": "N ＋ はおろか: Ngay cả... cũng không được, huống chi là... (thường đi với さえ, すら, も ở vế sau mang ý tiêu cực)."
            },
            {
                "id": "skz_b_ch03_q08",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "～はおろか",
                "question": "怪我をして、走ることはおろか（　）さえできない。",
                "options": ["a. 歩くこと", "b. 泳ぐこと", "c. 立ち上がること"],
                "answer": "a",
                "explanation": "【Dịch】Bị thương nặng đến mức việc chạy nhảy đã đành một lẽ, ngay cả việc đi bộ bình thường còn chẳng thể làm được.\n【Phân tích】'Đi bộ' (歩くこと) là mức độ cơ bản hơn 'chạy' (走ること). Việc cơ bản còn không làm nổi.",
                "grammarRule": "Vế sau luôn là sự việc có mức độ đơn giản hơn, dễ thực hiện hơn vế trước."
            },
            {
                "id": "skz_b_ch03_q09",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "～もさることながら",
                "question": "このホテルは料理の美味しさ（　）もさることながら、窓からの景色の素晴らしさにも圧倒される。",
                "options": ["a. ", "b. を", "c. に"],
                "answer": "a",
                "explanation": "【Dịch】Khách sạn này món ăn ngon thì đã đành rồi, nhưng cảnh sắc nhìn từ cửa sổ cũng khiến người ta phải choáng ngợp.\n【Phân tích】N ＋ もさることながら: A thì đương nhiên rồi, nhưng B còn đáng chú ý hơn nữa.",
                "grammarRule": "N ＋ もさることながら: A đã đành / A là đương nhiên rồi, nhưng B còn hơn thế nữa."
            },
            {
                "id": "skz_b_ch03_q10",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "～もさることながら",
                "question": "若者の就職難は本人の能力もさることながら、（　）。",
                "options": ["a. 景気の悪化も大きな要因だ", "b. 本人の努力不足だ", "c. 学歴がすべてだ"],
                "answer": "a",
                "explanation": "【Dịch】Tình trạng khó xin việc của giới trẻ thì năng lực bản thân đã đành một nhẽ, nhưng suy thoái kinh tế cũng là một nguyên nhân cực kỳ lớn.\n【Phân tích】Nhấn mạnh thêm nguyên nhân ngoại cảnh vế sau: 景気の悪化も大きな要因だ.",
                "grammarRule": "Vế sau đưa ra một yếu tố khác đáng chú ý hoặc có sức nặng hơn."
            },
            {
                "id": "skz_b_ch03_q11",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "第3課 総合問題",
                "question": "彼女のバイオリン演奏の美しさは、プロ（　）ならではの深い味わいがある。",
                "options": ["a. をおいて", "b. ならでは", "c. にとどまらず"],
                "answer": "b",
                "explanation": "【Dịch】Vẻ đẹp tiếng đàn vĩ cầm của cô ấy mang một dư vị sâu sắc chỉ có ở người nghệ sĩ chuyên nghiệp đích thực.\n【Phân tích】Đặc sắc độc đáo chỉ có ở nghệ sĩ chuyên nghiệp -> プロならではの.",
                "grammarRule": "N ＋ ならではの: Nét đặc sắc chỉ có ở..."
            },
            {
                "id": "skz_b_ch03_q12",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "第3課 総合問題",
                "question": "次のリーダーは、情熱と行動力を持つ彼（　）をおいて適任者はいない。",
                "options": ["a. ならでは", "b. をおいて", "c. はおろか"],
                "answer": "b",
                "explanation": "【Dịch】Người lãnh đạo tiếp theo thì ngoại trừ anh ấy - người tràn đầy nhiệt huyết và hành động ra, chẳng còn ai thích hợp hơn.\n【Phân tích】彼をおいて適任者はいない (Ngoài anh ấy ra không ai xứng đáng).",
                "grammarRule": "N ＋ をおいて (ほかに...ない): Ngoại trừ N ra thì không có ai khác."
            },
            {
                "id": "skz_b_ch03_q13",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "第3課 総合問題",
                "question": "不況の波は中小企業（　）にとどまらず、大企業にも大きな打撃を与えている。",
                "options": ["a. にとどまらず", "b. はおろか", "c. もさることながら"],
                "answer": "a",
                "explanation": "【Dịch】Làn sóng suy thoái không chỉ dừng lại ở doanh nghiệp vừa và nhỏ mà còn giáng đòn nặng nề lên cả các tập đoàn lớn.\n【Phân tích】Không chỉ dừng lại ở phạm vi hẹp mà lan sang cả diện rộng -> ～にとどまらず.",
                "grammarRule": "N ＋ にとどまらず: Không chỉ dừng lại ở..."
            },
            {
                "id": "skz_b_ch03_q14",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "第3課 総合問題",
                "question": "入院中は固い食べ物（　）はおろか、水さえ満足に飲めなかった。",
                "options": ["a. をおいて", "b. はおろか", "c. ならでは"],
                "answer": "b",
                "explanation": "【Dịch】Trong thời gian nằm viện, thức ăn cứng thì đã đành không ăn nổi, ngay cả ngụm nước cũng chẳng thể uống trọn vẹn.\n【Phân tích】AはおろかBさえ: Thức ăn cứng đã đành, ngay cả nước cũng không uống được.",
                "grammarRule": "N ＋ はおろか...さえ: Huống chi là... ngay cả cái cơ bản cũng không xong."
            },
            {
                "id": "skz_b_ch03_q15",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "第3課 総合問題",
                "question": "新製品の性能（　）もさることながら、その洗練されたデザインにも注目が集まっている。",
                "options": ["a. もさることながら", "b. をおいて", "c. にとどまらず"],
                "answer": "a",
                "explanation": "【Dịch】Hiệu năng của sản phẩm mới thì tuyệt vời là điều đương nhiên rồi, nhưng thiết kế tinh tế của nó cũng đang thu hút sự chú ý rất lớn.\n【Phân tích】Tính năng tốt là dĩ nhiên, kiểu dáng còn ấn tượng hơn -> ～もさることながら.",
                "grammarRule": "N ＋ もさることながら: A đã đành, B cũng rất đáng kể."
            },
            {
                "id": "skz_b_ch03_q16",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "第3課 総合問題",
                "question": "京都（　）ならではの歴史を感じる街並みに感動した。",
                "options": ["a. をおいて", "b. ならでは", "c. はおろか"],
                "answer": "b",
                "explanation": "【Dịch】Tôi vô cùng xúc động trước dãy phố cổ kính mang đậm dấu ấn lịch sử chỉ có ở Kyoto.\n【Phân tích】Đặc trưng riêng biệt chỉ Kyoto mới có -> 京都ならではの.",
                "grammarRule": "N ＋ ならでは: Chỉ có ở N."
            },
            {
                "id": "skz_b_ch03_q17",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "第3課 総合問題",
                "question": "この難問を解決できるのは、鈴木博士（　）をおいてほかには考えられない。",
                "options": ["a. をおいて", "b. にとどまらず", "c. もさることながら"],
                "answer": "a",
                "explanation": "【Dịch】Người có thể giải quyết bài toán hóc búa này thì ngoài tiến sĩ Suzuki ra không thể nghĩ ra ai khác.\n【Phân tích】Đối tượng duy nhất -> ～をおいてほかに...ない.",
                "grammarRule": "N ＋ をおいて (ほかに...ない)."
            },
            {
                "id": "skz_b_ch03_q18",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "第3課 総合問題",
                "question": "彼女は英語（　）はおろか、フランス語やロシア語まで流暢に話す。",
                "options": ["a. をおいて", "b. はおろか", "c. にとどまらず"],
                "answer": "c",
                "explanation": "【Dịch】Cô ấy không chỉ dừng lại ở tiếng Anh mà ngay cả tiếng Pháp hay tiếng Nga cũng nói lưu loát.\n【Phân tích】Không chỉ tiếng Anh mà còn tiếng Pháp, tiếng Nga (ý bổ sung tích cực) -> にとどまらず. Chú ý: 'はおろか' mang sắc thái tiêu cực phủ định.",
                "grammarRule": "N ＋ にとどまらず: Không chỉ... mà còn nhiều hơn thế."
            },
            {
                "id": "skz_b_ch03_q19",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "第3課 総合問題",
                "question": "この映画は若者（　）にとどまらず、幅広い年代の人々に支持されている。",
                "options": ["a. にとどまらず", "b. はおろか", "c. をおいて"],
                "answer": "a",
                "explanation": "【Dịch】Bộ phim này không chỉ thu hút giới trẻ mà còn được đông đảo khán giả ở nhiều độ tuổi đón nhận nồng nhiệt.\n【Phân tích】Mở rộng phạm vi người xem -> ～にとどまらず.",
                "grammarRule": "N ＋ にとどまらず: Mở rộng ra phạm vi lớn hơn."
            },
            {
                "id": "skz_b_ch03_q20",
                "lesson": "第3課: 限定・非限定・付加",
                "grammarPoint": "第3課 総合問題",
                "question": "彼の誠実な人柄（　）もさることながら、その鋭いビジネスセンスにも一目置いている。",
                "options": ["a. をおいて", "b. もさることながら", "c. ならでは"],
                "answer": "b",
                "explanation": "【Dịch】Nhân cách chân thành của anh ấy đã là điều đáng nể rồi, nhưng nhạy cảm kinh doanh sắc bén của anh ấy cũng khiến người ta phải ngả mũ thán phục.\n【Phân tích】A đã đành, B còn đáng nể hơn -> ～もさることながら.",
                "grammarRule": "N ＋ もさることながら: A đã đành, B còn hơn thế."
            }
        ]
    },
    "ch04": {
        "chapterId": "ch04",
        "lesson": "第4課: 例示 (Đưa ra ví dụ)",
        "theme": "事柄を説明する",
        "group": "group1",
        "title": "第4課: 例示",
        "description": "Các mẫu ngữ pháp: ～なり・・・なり, ～であれ・・・であれ, ～といい・・・といい, ～といわず・・・といわず.",
        "questions": [
            {
                "id": "skz_b_ch04_q01",
                "lesson": "第4課: 例示",
                "grammarPoint": "～なり・・・なり",
                "question": "あの部屋はかなり寒いから、長い時間いるなら上着なり（　）なり持っていったほうがいい。",
                "options": ["a. 暖房をつける", "b. ひざ掛け", "c. 暖かい"],
                "answer": "b",
                "explanation": "【Dịch】Căn phòng đó khá lạnh đấy, nếu ở lâu thì nên mang áo khoác hay khăn đắp đùi chẳng hạn đi theo.\n【Phân tích】Danh từ kết hợp đồng dạng: 上着 (áo khoác)なり ＋ ひざ掛け (khăn trùm đùi)なり.",
                "grammarRule": "N1なり N2なり: N1 cũng được, N2 cũng được (đưa ra các phương án cùng nhóm để lựa chọn)."
            },
            {
                "id": "skz_b_ch04_q02",
                "lesson": "第4課: 例示",
                "grammarPoint": "～なり・・・なり",
                "question": "わからないことがあれば、先生に聞くなり（　）なりして、自分で調べなさい。",
                "options": ["a. 辞書を引く", "b. 辞書を引いた", "c. 辞書を引いて"],
                "answer": "a",
                "explanation": "【Dịch】Nếu có điều gì không hiểu, hãy hỏi thầy cô hoặc tra từ điển chẳng hạn, tự mình tìm hiểu đi.\n【Phân tích】Động từ đi với ～なり phải ở thể từ điển V-る: 先生に聞くなり 辞書を引くなり.",
                "grammarRule": "V1-るなり V2-るなり: Làm việc 1 hay làm việc 2 chẳng hạn."
            },
            {
                "id": "skz_b_ch04_q03",
                "lesson": "第4課: 例示",
                "grammarPoint": "～であれ・・・であれ",
                "question": "理由が（　）であれ、無断で仕事を休むことは許されない。",
                "options": ["a. 何", "b. どんな", "c. どう"],
                "answer": "a",
                "explanation": "【Dịch】Dù lý do là gì chăng nữa, việc tự tiện nghỉ làm mà không báo trước là không thể chấp nhận được.\n【Phân tích】Từ để hỏi 何 ＋ であれ: Cho dù là gì đi chăng nữa.",
                "grammarRule": "Từ để hỏi ＋ であれ / N1であれ N2であれ: Dù là... hay là... thì kết quả vẫn không đổi."
            },
            {
                "id": "skz_b_ch04_q04",
                "lesson": "第4課: 例示",
                "grammarPoint": "～であれ・・・であれ",
                "question": "大人であれ（　）であれ、法を守る義務がある。",
                "options": ["a. 子供", "b. 子供な", "c. 子供の"],
                "answer": "a",
                "explanation": "【Dịch】Dù là người lớn hay trẻ con thì đều có nghĩa vụ phải tuân thủ pháp luật.\n【Phân tích】N1であれ N2であれ: 大人であれ 子供であれ.",
                "grammarRule": "N1であれ N2であれ: Dù là đối tượng 1 hay đối tượng 2 thì đều chung một tính chất/nghĩa vụ."
            },
            {
                "id": "skz_b_ch04_q05",
                "lesson": "第4課: 例示",
                "grammarPoint": "～といい・・・といい",
                "question": "この靴はデザインといい（　）といい、申し分がない。",
                "options": ["a. 履き心地", "b. 履きやすい", "c. 履くこと"],
                "answer": "a",
                "explanation": "【Dịch】Đôi giày này từ mẫu mã thiết kế cho đến cảm giác êm ái khi xỏ chân vào đều hoàn hảo không có chỗ nào để chê.\n【Phân tích】N1といい N2といい đưa ra hai tiêu chí đánh giá cùng loại: デザインといい 履き心地といい.",
                "grammarRule": "N1といい N2といい: Xét về cả N1 lẫn N2 thì đều... (thường đi với lời khen ngợi hoặc chê bai toàn diện)."
            },
            {
                "id": "skz_b_ch04_q06",
                "lesson": "第4課: 例示",
                "grammarPoint": "～といい・・・といい",
                "question": "あのレストランは味といいサービスといい、（　）。",
                "options": ["a. 一度行ってみたい", "b. 最高水準だ", "c. 改善すべき点が多いかもしれない"],
                "answer": "b",
                "explanation": "【Dịch】Nhà hàng đó cả về hương vị lẫn cung cách phục vụ đều đạt tiêu chuẩn đỉnh cao nhất.\n【Phân tích】Vế sau của ～といい・・・といい là lời đánh giá tổng thể rõ ràng (最高水準だ).",
                "grammarRule": "Vế sau là nhận xét, đánh giá toàn diện."
            },
            {
                "id": "skz_b_ch04_q07",
                "lesson": "第4課: 例示",
                "grammarPoint": "～といわず・・・といわず",
                "question": "部屋の中は机の上といわず床（　）といわず、書類が散乱している。",
                "options": ["a. に", "b. の上", "c. で"],
                "answer": "b",
                "explanation": "【Dịch】Trong phòng từ trên mặt bàn cho đến dưới mặt sàn, chỗ nào cũng thấy giấy tờ bừa bộn khắp nơi.\n【Phân tích】N1といわず N2といわず: 机の上といわず 床の上といわず (toàn bộ khắp nơi không phân biệt).",
                "grammarRule": "N1といわず N2といわず: Bất kể là N1 hay N2 (toàn bộ mọi nơi/mọi lúc đều trong tình trạng đó, không còn ranh giới)."
            },
            {
                "id": "skz_b_ch04_q08",
                "lesson": "第4課: 例示",
                "grammarPoint": "～といわず・・・といわず",
                "question": "彼は昼といわず夜といわず、（　）。",
                "options": ["a. よく寝ている", "b. ゲームに没頭している", "c. 散歩に出かける"],
                "answer": "b",
                "explanation": "【Dịch】Anh ta bất kể ngày hay đêm, suốt ngày chìm đắm cắm đầu vào chơi game.\n【Phân tích】Diễn tả tình trạng liên tục không kể ngày đêm: ゲームに没頭している.",
                "grammarRule": "Chỉ trạng thái diễn ra liên miên không phân biệt thời gian/không gian."
            },
            {
                "id": "skz_b_ch04_q09",
                "lesson": "第4課: 例示",
                "grammarPoint": "第4課 総合問題",
                "question": "電話（　）なりメール（　）なりで、事前に連絡してください。",
                "options": ["a. と / と", "b. なり / なり", "c. であれ / であれ"],
                "answer": "b",
                "explanation": "【Dịch】Hãy liên lạc trước bằng điện thoại hoặc email chẳng hạn.\n【Phân tích】Gợi ý phương tiện lựa chọn nhẹ nhàng: 電話なりメールなり.",
                "grammarRule": "N1なり N2なり: N1 hoặc N2 chẳng hạn (đưa ra giải pháp lựa chọn)."
            },
            {
                "id": "skz_b_ch04_q10",
                "lesson": "第4課: 例示",
                "grammarPoint": "第4課 総合問題",
                "question": "晴天（　）であれ雨天（　）であれ、マラソン大会は予定通り実施されます。",
                "options": ["a. なり / なり", "b. といい / といい", "c. であれ / であれ"],
                "answer": "c",
                "explanation": "【Dịch】Dù trời nắng hay trời mưa, giải chạy marathon vẫn sẽ được tổ chức đúng như kế hoạch.\n【Phân tích】Bất kể điều kiện thời tiết nào thì sự việc vẫn tiến hành -> であれ・・・であれ.",
                "grammarRule": "N1であれ N2であれ: Dù là N1 hay N2 thì kết quả vẫn giữ nguyên."
            },
            {
                "id": "skz_b_ch04_q11",
                "lesson": "第4課: 例示",
                "grammarPoint": "第4課 総合問題",
                "question": "彼の話し方（　）といい態度（　）といい、本当に礼儀正しい青年だ。",
                "options": ["a. といい / といい", "b. といわず / といわず", "c. なり / なり"],
                "answer": "a",
                "explanation": "【Dịch】Từ cách ăn nói cho đến tác phong thái độ, cậu ấy thực sự là một chàng thanh niên vô cùng lễ phép.\n【Phân tích】Đánh giá khen ngợi đa góc độ -> といい・・・といい.",
                "grammarRule": "N1といい N2といい: Xét cả N1 lẫn N2."
            },
            {
                "id": "skz_b_ch04_q12",
                "lesson": "第4課: 例示",
                "grammarPoint": "第4課 総合問題",
                "question": "手（　）といわず足（　）といわず、泥だらけになって遊んだ。",
                "options": ["a. といい / といい", "b. といわず / といわず", "c. であれ / であれ"],
                "answer": "b",
                "explanation": "【Dịch】Từ bàn tay cho đến bàn chân, chỗ nào cũng lấm lem bùn đất khi chơi đùa.\n【Phân tích】Phủ kín toàn bộ khắp cơ thể không phân biệt chỗ nào -> といわず・・・といわず.",
                "grammarRule": "N1といわず N2といわず: Cả N1 lẫn N2 toàn bộ đều bị bao phủ/tràn ngập."
            },
            {
                "id": "skz_b_ch04_q13",
                "lesson": "第4課: 例示",
                "grammarPoint": "第4課 総合問題",
                "question": "お茶（　）なりコーヒー（　）なり、お好きなものをどうぞ。",
                "options": ["a. といい / といい", "b. なり / なり", "c. といわず / といわず"],
                "answer": "b",
                "explanation": "【Dịch】Trà hay cà phê chẳng hạn, xin mời dùng thứ bạn thích.\n【Phân tích】Mời mọc lựa chọn nhẹ nhàng -> なり・・・なり.",
                "grammarRule": "N1なり N2なり: Gợi ý các phương án lựa chọn."
            },
            {
                "id": "skz_b_ch04_q14",
                "lesson": "第4課: 例示",
                "grammarPoint": "第4課 総合問題",
                "question": "金持ち（　）であれ貧乏人（　）であれ、人の命の重さは同じだ。",
                "options": ["a. であれ / であれ", "b. なり / なり", "c. といい / といい"],
                "answer": "a",
                "explanation": "【Dịch】Dù là người giàu hay người nghèo, giá trị tính mạng con người đều nặng tựa như nhau.\n【Phân tích】Dù thuộc thành phần nào thì chân lý vẫn không đổi -> であれ・・・であれ.",
                "grammarRule": "N1であれ N2であれ: Dù là A hay B thì cũng như nhau."
            },
            {
                "id": "skz_b_ch04_q15",
                "lesson": "第4課: 例示",
                "grammarPoint": "第4課 総合問題",
                "question": "この小説はストーリー展開（　）といい登場人物の描写（　）といい、読者を飽きさせない。",
                "options": ["a. といわず / といわず", "b. といい / といい", "c. なり / なり"],
                "answer": "b",
                "explanation": "【Dịch】Cuốn tiểu thuyết này từ diễn biến cốt truyện cho đến việc khắc họa nhân vật đều khiến độc giả không hề thấy nhàm chán.\n【Phân tích】Đánh giá tác phẩm trên nhiều phương diện -> といい・・・といい.",
                "grammarRule": "N1といい N2といい: Xét cả N1 lẫn N2 đều xuất sắc."
            },
            {
                "id": "skz_b_ch04_q16",
                "lesson": "第4課: 例示",
                "grammarPoint": "第4課 総合問題",
                "question": "平日（　）といわず週末（　）といわず、あのテーマパークは観光客で溢れている。",
                "options": ["a. といわず / といわず", "b. なり / なり", "c. であれ / であれ"],
                "answer": "a",
                "explanation": "【Dịch】Bất kể ngày thường hay cuối tuần, công viên giải trí đó lúc nào cũng nườm nượp khách du lịch.\n【Phân tích】Tràn ngập khắp mọi lúc -> といわず・・・といわず.",
                "grammarRule": "N1といわず N2といわず: Cả thời gian N1 lẫn N2 đều tràn ngập."
            },
            {
                "id": "skz_b_ch04_q17",
                "lesson": "第4課: 例示",
                "grammarPoint": "第4課 総合問題",
                "question": "休みの日は散歩をする（　）本を読む（　）して、のんびり過ごしている。",
                "options": ["a. といい / といい", "b. なり / なり", "c. といわず / といわず"],
                "answer": "b",
                "explanation": "【Dịch】Vào ngày nghỉ, tôi thường đi dạo hoặc đọc sách chẳng hạn, thong thả tận hưởng thời gian.\n【Phân tích】V-るなり V-るなり: Đi dạo hay đọc sách chẳng hạn.",
                "grammarRule": "V1-るなり V2-るなり: Làm hành động 1 hay hành động 2."
            },
            {
                "id": "skz_b_ch04_q18",
                "lesson": "第4課: 例示",
                "grammarPoint": "第4課 総合問題",
                "question": "相手が誰（　）であれ、礼儀を失った態度を取ってはならない。",
                "options": ["a. に", "b. であれ", "c. なら"],
                "answer": "b",
                "explanation": "【Dịch】Dù đối phương là bất kỳ ai đi chăng nữa, bạn cũng không được có thái độ mất lịch sự.\n【Phân tích】Từ để hỏi (誰) ＋ であれ: Dù là bất kỳ ai.",
                "grammarRule": "Từ để hỏi ＋ であれ: Bất kể là ai/gì."
            }
        ]
    },
    "ch05": {
        "chapterId": "ch05",
        "lesson": "第5課: 関連・無関係 (Liên quan & Không liên quan)",
        "theme": "事柄を説明する",
        "group": "group1",
        "title": "第5課: 関連・無関係",
        "description": "Các mẫu ngữ pháp: ～いかんだ, ～いかんにかかわらず・～いかんによらず・～いかんを問わず, ～をものともせず(に), ～をよそに, ～ならいざしらず.",
        "questions": [
            {
                "id": "skz_b_ch05_q01",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "～いかんだ",
                "question": "試験に合格できるかどうかは、これからのあなたの努力（　）いかんだ。",
                "options": ["a. ", "b. の", "c. に"],
                "answer": "a",
                "explanation": "【Dịch】Việc có thi đỗ hay không phụ thuộc hoàn toàn vào nỗ lực từ nay về sau của bạn.\n【Phân tích】N ＋ いかんだ: Tùy thuộc vào N (mang tính quyết định).",
                "grammarRule": "N ＋ いかんだ / いかんによって: Tùy thuộc vào N mà kết quả sẽ được định đoạt."
            },
            {
                "id": "skz_b_ch05_q02",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "～いかんだ",
                "question": "手術が成功するかどうかは、担当医の腕（　）いかんにかかっている。",
                "options": ["a. ", "b. の", "c. を"],
                "answer": "a",
                "explanation": "【Dịch】Ca phẫu thuật có thành công hay không phụ thuộc hoàn toàn vào tay nghề của bác sĩ phụ trách.\n【Phân tích】腕いかんにかかっている: Phụ thuộc vào tay nghề.",
                "grammarRule": "N ＋ いかん: Tùy thuộc vào..."
            },
            {
                "id": "skz_b_ch05_q03",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "～いかんにかかわらず",
                "question": "理由の（　）いかんにかかわらず、遅刻した場合は試験を受けられません。",
                "options": ["a. ", "b. の", "c. に"],
                "answer": "a",
                "explanation": "【Dịch】Bất kể lý do là gì đi chăng nữa, hễ đến muộn là sẽ không được tham dự kỳ thi.\n【Phân tích】N (の) いかんにかかわらず: Bất kể lý do ra sao.",
                "grammarRule": "N (の) ＋ いかんにかかわらず / いかんによらず / いかんを問わず: Không màng tới, bất kể N thế nào."
            },
            {
                "id": "skz_b_ch05_q04",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "～いかんにかかわらず",
                "question": "国籍のいかんによらず、（　）。",
                "options": ["a. 優秀な人材を広く採用する方針だ", "b. 日本人だけを優遇する", "c. ビザが必要だ"],
                "answer": "a",
                "explanation": "【Dịch】Bất kể quốc tịch là gì, chủ trương của chúng tôi là tuyển dụng rộng rãi các nhân tài xuất chúng.\n【Phân tích】Không phân biệt quốc tịch -> Tuyển dụng rộng rãi (広く採用する).",
                "grammarRule": "Vế sau mang tính bình đẳng, không phân biệt đối xử theo điều kiện ở vế trước."
            },
            {
                "id": "skz_b_ch05_q05",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "～をものともせず(に)",
                "question": "彼は周囲の反対（　）をものともせずに、自分の信じる道を進んだ。",
                "options": ["a. ", "b. に", "c. で"],
                "answer": "a",
                "explanation": "【Dịch】Mặc kệ sự phản đối kịch liệt từ mọi người xung quanh, anh ấy vẫn kiên định bước tiếp trên con đường mình tin tưởng.\n【Phân tích】N ＋ をものともせず(に): Vượt lên trên, bất chấp trở ngại nguy hiểm to lớn.",
                "grammarRule": "N (trở ngại, bão táp, bệnh tật, phản đối) ＋ をものともせず(に): Bất chấp khó khăn hiểm nguy để dũng cảm tiến lên (khen ngợi)."
            },
            {
                "id": "skz_b_ch05_q06",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "～をものともせず(に)",
                "question": "選手たちは激しい吹雪をものともせずに、（　）。",
                "options": ["a. 試合を中止した", "b. 全力でプレーを続けた", "c. ホテルに引き返した"],
                "answer": "b",
                "explanation": "【Dịch】Các cầu thủ bất chấp trận bão tuyết dữ dội, vẫn dốc toàn lực thi đấu tiếp tục.\n【Phân tích】Vế sau là hành động kiên cường tiếp tục (全力でプレーを続けた).",
                "grammarRule": "Vế sau luôn thể hiện sự dũng cảm, nỗ lực phi thường."
            },
            {
                "id": "skz_b_ch05_q07",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "～をよそに",
                "question": "親の心配（　）をよそに、息子は毎晩遅くまで遊び歩いている。",
                "options": ["a. ", "b. に", "c. で"],
                "answer": "a",
                "explanation": "【Dịch】Phớt lờ nỗi lo lắng thấp thỏm của cha mẹ, đứa con trai cứ đàn đúm chơi bời đến tận khuya mỗi đêm.\n【Phân tích】N ＋ をよそに: Phớt lờ, mặc kệ sự lo lắng/kỳ vọng của người khác (mang sắc thái phê phán).",
                "grammarRule": "N (lo lắng, can ngăn, kỳ vọng) ＋ をよそに: Bỏ ngoài tai, phớt lờ điều đáng lẽ phải bận tâm (thường mang ý chê trách)."
            },
            {
                "id": "skz_b_ch05_q08",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "～をよそに",
                "question": "住民の強い抗議の声をよそに、（　）。",
                "options": ["a. 工事は中止された", "b. 開発工事が強行された", "c. 説明会が開かれた"],
                "answer": "b",
                "explanation": "【Dịch】Phớt lờ những tiếng la ó phản đối gay gắt của người dân, công trình xây dựng phát triển vẫn ngang nhiên bị ép thi công.\n【Phân tích】Hành động bất chấp tiếng phản đối để cưỡng chế làm -> 工事が強行された.",
                "grammarRule": "Diễn tả hành vi phớt lờ dư luận hoặc sự ngăn cản."
            },
            {
                "id": "skz_b_ch05_q09",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "～ならいざしらず",
                "question": "小学生（　）ならいざしらず、大学生にもなってそんな基本的な漢字が書けないとは信じられない。",
                "options": ["a. ", "b. だ", "c. の"],
                "answer": "a",
                "explanation": "【Dịch】Học sinh tiểu học thì không nói làm gì, chứ đã lên đại học rồi mà không viết nổi chữ Hán cơ bản như thế thì thật không thể tin nổi.\n【Phân tích】Aならいざしらず B: A thì còn châm chước được, chứ B thì tuyệt đối không thể chấp nhận.",
                "grammarRule": "N / 普通形 ＋ ならいざしらず: Nếu là trường hợp A thì còn tạm bỏ qua được, nhưng trường hợp này thì không thể chấp nhận nổi."
            },
            {
                "id": "skz_b_ch05_q10",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "～ならいざしらず",
                "question": "昔ならいざしらず、現代において（　）。",
                "options": ["a. 女性の社会進出は当たり前だ", "b. インターネットがない時代だった", "c. 身分制度が残っている"],
                "answer": "a",
                "explanation": "【Dịch】Thời xưa thì còn tạm nói, chứ trong thời đại ngày nay thì việc phụ nữ tham gia phát triển xã hội là điều đương nhiên.\n【Phân tích】Thời nay thì khác hẳn thời xưa: 当たり前だ.",
                "grammarRule": "So sánh giữa trường hợp đặc biệt chấp nhận được với thực tế không thể chấp nhận."
            },
            {
                "id": "skz_b_ch05_q11",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "第5課 総合問題",
                "question": "成果の（　）いかんによって、来期のボーナスの支給額が決まる。",
                "options": ["a. ", "b. の", "c. に"],
                "answer": "a",
                "explanation": "【Dịch】Tùy thuộc vào thành quả công việc mà số tiền thưởng của kỳ tới sẽ được định đoạt.\n【Phân tích】成果いかんによって: Tùy theo thành quả.",
                "grammarRule": "N ＋ いかんによって: Tùy thuộc vào..."
            },
            {
                "id": "skz_b_ch05_q12",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "第5課 総合問題",
                "question": "天候のいかんを問わず、明日のチャリティーイベントは（　）。",
                "options": ["a. 雨なら中止です", "b. 予定通り開催されます", "c. 延期される可能性があります"],
                "answer": "b",
                "explanation": "【Dịch】Bất kể thời tiết thế nào, sự kiện từ thiện ngày mai vẫn sẽ được tổ chức đúng như lịch trình.\n【Phân tích】いかんを問わず = không màng thời tiết ra sao -> vẫn diễn ra theo lịch.",
                "grammarRule": "いかんを問わず: Không màng tới điều kiện vế trước."
            },
            {
                "id": "skz_b_ch05_q13",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "第5課 総合問題",
                "question": "高齢（　）をものともせず、彼女はエベレスト登頂に見事成功した。",
                "options": ["a. ", "b. に", "c. で"],
                "answer": "a",
                "explanation": "【Dịch】Bất chấp tuổi tác đã cao, bà ấy đã chinh phục thành công đỉnh Everest một cách ngoạn mục.\n【Phân tích】Tuổi cao là trở ngại khó khăn, bất chấp tuổi tác -> 高齢をものともせず.",
                "grammarRule": "N ＋ をものともせず: Vượt qua rào cản bất lợi."
            },
            {
                "id": "skz_b_ch05_q14",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "第5課 総合問題",
                "question": "医師の忠告（　）をよそに、彼は退院後すぐに大酒を飲んだ。",
                "options": ["a. ", "b. に", "c. を"],
                "answer": "a",
                "explanation": "【Dịch】Bỏ ngoài tai lời khuyên can của bác sĩ, anh ta vừa xuất viện xong là lập tức nốc rượu đẫy đà.\n【Phân tích】Phớt lờ lời khuyên can tốt đẹp -> 忠告をよそに.",
                "grammarRule": "N ＋ をよそに: Phớt lờ sự khuyên can, lo lắng."
            },
            {
                "id": "skz_b_ch05_q15",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "第5課 総合問題",
                "question": "初心者（　）ならいざしらず、ベテランの君がこんな凡ミスをするとは情けない。",
                "options": ["a. ", "b. だ", "c. な"],
                "answer": "a",
                "explanation": "【Dịch】Người mới vào nghề thì còn thông cảm được, chứ người dày dạn kinh nghiệm như cậu mà lại mắc lỗi ngớ ngẩn thế này thì thật đáng thất vọng.\n【Phân tích】Người mới thì bỏ qua, chứ thâm niên thì không thể -> ならいざしらず.",
                "grammarRule": "N ＋ ならいざしらず: Trường hợp A thì còn châm chước được."
            },
            {
                "id": "skz_b_ch05_q16",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "第5課 総合問題",
                "question": "本人のやる気（　）いかんで、語学の習得スピードは大きく変わる。",
                "options": ["a. ", "b. の", "c. に"],
                "answer": "a",
                "explanation": "【Dịch】Tùy thuộc vào tinh thần quyết tâm của chính bản thân mà tốc độ tiếp thu ngoại ngữ sẽ thay đổi đáng kể.\n【Phân tích】N ＋ いかんで: Tùy vào quyết tâm.",
                "grammarRule": "N ＋ いかんで: Do yếu tố N quyết định."
            },
            {
                "id": "skz_b_ch05_q17",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "第5課 総合問題",
                "question": "年齢や性別の（　）にかかわらず、どなたでも自由に応募できます。",
                "options": ["a. いかん", "b. ものともせず", "c. よそに"],
                "answer": "a",
                "explanation": "【Dịch】Bất kể tuổi tác hay giới tính thế nào, bất kỳ ai cũng có thể tự do nộp đơn ứng tuyển.\n【Phân tích】Cụm từ tiêu chuẩn: 性別のいかんにかかわらず.",
                "grammarRule": "N ＋ のいかんにかかわらず: Bất kể thế nào."
            },
            {
                "id": "skz_b_ch05_q18",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "第5課 総合問題",
                "question": "体のハンディキャップ（　）をものともせずに、世界的なパラリンピック選手として活躍している。",
                "options": ["a. をよそに", "b. をものともせずに", "c. ならいざしらず"],
                "answer": "b",
                "explanation": "【Dịch】Bất chấp những khiếm khuyết khiếm thị của cơ thể, anh ấy vẫn hoạt động xuất sắc như một vận động viên Paralympic tầm cỡ thế giới.\n【Phân tích】Vượt lên trở ngại nghịch cảnh -> をものともせずに.",
                "grammarRule": "N ＋ をものともせず: Vượt qua nghịch cảnh cơ thể/môi trường."
            },
            {
                "id": "skz_b_ch05_q19",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "第5課 総合問題",
                "question": "周りの迷惑（　）をよそに、電車の中で大声で通話している乗客がいる。",
                "options": ["a. をものともせず", "b. をよそに", "c. いかんによらず"],
                "answer": "b",
                "explanation": "【Dịch】Phớt lờ sự phiền toái gây ra cho người xung quanh, có hành khách cứ lớn tiếng buôn điện thoại trên tàu điện.\n【Phân tích】Hành vi thiếu ý thức, mặc kệ người khác -> をよそに.",
                "grammarRule": "N ＋ をよそに: Phớt lờ sự khó chịu/phiền hà của người khác."
            },
            {
                "id": "skz_b_ch05_q20",
                "lesson": "第5課: 関連・無関係",
                "grammarPoint": "第5課 総合問題",
                "question": "数千円（　）ならいざしらず、何百万円もの借金を肩代わりすることなど到底できない。",
                "options": ["a. ならいざしらず", "b. をものともせず", "c. いかんにかかわらず"],
                "answer": "a",
                "explanation": "【Dịch】Vài nghìn yên thì còn nói làm gì, chứ gánh hộ món nợ tới hàng triệu yên thì tuyệt đối không thể nào kham nổi.\n【Phân tích】Vài nghìn yên thì đỡ được, hàng triệu yên thì không -> ならいざしらず.",
                "grammarRule": "N ＋ ならいざしらず: Trường hợp nhỏ thì còn được, trường hợp lớn thì không."
            }
        ]
    },
    "ch06": {
        "chapterId": "ch06",
        "lesson": "第6課: 様子 (Dáng vẻ, trạng thái)",
        "theme": "事柄を説明する",
        "group": "group1",
        "title": "第6課: 様子",
        "description": "Các mẫu ngữ pháp: ～んばかりだ, ～とばかり(に), ～ともなく・～ともなしに, ～ながらに(して), ～きらいがある.",
        "questions": [
            {
                "id": "skz_b_ch06_q01",
                "lesson": "第6課: 様子",
                "grammarPoint": "～んばかりだ",
                "question": "彼女は今にも泣き出さ（　）んばかりの表情で立ち尽くしていた。",
                "options": ["a. ", "b. し", "c. せ"],
                "answer": "a",
                "explanation": "【Dịch】Cô ấy đứng chết lặng với nét mặt ngỡ như chực khóc òa ra ngay đến nơi.\n【Phân tích】V-ない (bỏ ない) ＋ んばかり: 泣き出さない -> 泣き出さんばかり.",
                "grammarRule": "V-ない (bỏ ない) ＋ んばかりだ (riêng する -> せんばかり): Cứ như thể sắp sửa... đến nơi rồi."
            },
            {
                "id": "skz_b_ch06_q02",
                "lesson": "第6課: 様子",
                "grammarPoint": "～んばかりだ",
                "question": "割れ（　）んばかりの拍手が会場全体に鳴り響いた。",
                "options": ["a. ん", "b. ", "c. る"],
                "answer": "b",
                "explanation": "【Dịch】Tiếng vỗ tay vang dội như muốn làm nổ tung cả khán phòng.\n【Phân tích】割れない -> 割れんばかりの拍手 (tiếng vỗ tay tưởng chừng vỡ tung).",
                "grammarRule": "V-ない (bỏ ない) ＋ んばかりのN: N như muốn... đến nơi."
            },
            {
                "id": "skz_b_ch06_q03",
                "lesson": "第6課: 様子",
                "grammarPoint": "～とばかり(に)",
                "question": "彼は「早く帰れ」（　）とばかりに、時計をチラチラ見ている。",
                "options": ["a. ", "b. だ", "c. な"],
                "answer": "a",
                "explanation": "【Dịch】Anh ta cứ liếc nhìn đồng hồ liên tục như thể muốn ra hiệu bằng lời 'Về nhanh đi cho rảnh'.\n【Phân tích】Câu văn / từ ngữ ＋ とばかりに: Như thể muốn nói rằng...",
                "grammarRule": "Câu trích dẫn / Dáng vẻ ＋ とばかり(に): Ra điệu như muốn nói rằng... (hành động không nói thành lời nhưng thái độ lộ rõ)."
            },
            {
                "id": "skz_b_ch06_q04",
                "lesson": "第6課: 様子",
                "grammarPoint": "～とばかり(に)",
                "question": "チャンスが到来したとばかりに、（　）。",
                "options": ["a. 彼は慎重に行動した", "b. 一気に攻勢に出た", "c. あきらめて帰った"],
                "answer": "b",
                "explanation": "【Dịch】Như thể thấy thời cơ ngàn năm có một đã tới, anh ấy lập tức mở đợt tổng tấn công ồ ạt.\n【Phân tích】Chớp thời cơ ra đòn quyết định: 一気に攻勢に出た.",
                "grammarRule": "Hành vi chớp lấy dáng vẻ/thời điểm tức thì."
            },
            {
                "id": "skz_b_ch06_q05",
                "lesson": "第6課: 様子",
                "grammarPoint": "～ともなく・～ともなしに",
                "question": "ラジオを聴く（　）ともなしに聴いていたら、懐かしい曲が流れてきた。",
                "options": ["a. ", "b. の", "c. こと"],
                "answer": "a",
                "explanation": "【Dịch】Tôi đang để radio phát vu vơ không chủ đích thì bỗng nhiên một bài hát xưa cũ ùa về bên tai.\n【Phân tích】V-る ＋ ともなく / ともなしに: Làm hành động một cách vô thức, không chú định.",
                "grammarRule": "V-る ＋ ともなく / ともなしに: Làm việc gì đó vu vơ, vô định, không hề có chủ đích trước."
            },
            {
                "id": "skz_b_ch06_q06",
                "lesson": "第6課: 様子",
                "grammarPoint": "～ともなく・～ともなしに",
                "question": "窓の外を見るともなくぼんやり眺めていたら、（　）。",
                "options": ["a. 鳥が巣を作っているのに気づいた", "b. 一生懸命鳥を探した", "c. 宿題を始めた"],
                "answer": "a",
                "explanation": "【Dịch】Đang lúc lơ đãng nhìn vu vơ ra ngoài cửa sổ, tôi bỗng phát hiện ra một chú chim đang cặm cụi làm tổ.\n【Phân tích】Bắt gặp ngẫu nhiên khi đang vô định ngắm nhìn: 鳥が巣を作っているのに気づいた.",
                "grammarRule": "Thường đi kèm các động từ giác quan (nhìn, nghe, nghĩ) diễn tả sự tình cờ nhận ra."
            },
            {
                "id": "skz_b_ch06_q07",
                "lesson": "第6課: 様子",
                "grammarPoint": "～ながらに(して)",
                "question": "彼女は生まれ（　）ながらにして、並外れた音楽の才能を持っていた。",
                "options": ["a. ", "b. に", "c. の"],
                "answer": "a",
                "explanation": "【Dịch】Ngay từ khi mới sinh ra đời, cô ấy đã sở hữu tài năng âm nhạc phi phàm xuất chúng.\n【Phân tích】Cụm từ cố định: 生まれながらにして (bẩm sinh từ lúc chào đời).",
                "grammarRule": "N / V-ます (bỏ ます) ＋ ながらに(して): Giữ nguyên trong trạng thái vốn có từ đầu (thường đi với 生まれ, 涙, 昔)."
            },
            {
                "id": "skz_b_ch06_q08",
                "lesson": "第6課: 様子",
                "grammarPoint": "～ながらに(して)",
                "question": "インターネットのおかげで、家に（　）ながらにして世界中の情報が手に入る。",
                "options": ["a. いて", "b. いる", "c. い"],
                "answer": "c",
                "explanation": "【Dịch】Nhờ có Internet, chỉ cần ngồi yên tại nhà mà ta vẫn có thể nắm trọn mọi thông tin trên toàn thế giới trong tay.\n【Phân tích】居る -> 居ながらにして (ở yên một chỗ tại nhà).",
                "grammarRule": "V-ます (bỏ ます) ＋ ながらに: Ở nguyên trong tình trạng đó."
            },
            {
                "id": "skz_b_ch06_q09",
                "lesson": "第6課: 様子",
                "grammarPoint": "～きらいがある",
                "question": "彼は物事を少し大げさに言う（　）きらいがある。",
                "options": ["a. ", "b. な", "c. の"],
                "answer": "a",
                "explanation": "【Dịch】Anh ấy có tật hay nói quá, phóng đại mọi chuyện lên một chút.\n【Phân tích】V-る ＋ きらいがある: Có thói/có tật hay làm điều không tốt.",
                "grammarRule": "V-る / Nの ＋ きらいがある: Có khuynh hướng, tật xấu tiêu cực lặp đi lặp lại."
            },
            {
                "id": "skz_b_ch06_q10",
                "lesson": "第6課: 様子",
                "grammarPoint": "～きらいがある",
                "question": "最近の若者は、失敗を恐れて新しい挑戦を避ける（　）。",
                "options": ["a. きらいがある", "b. んばかりだ", "c. ながらにして"],
                "answer": "a",
                "explanation": "【Dịch】Giới trẻ ngày nay có khuynh hướng sợ thất bại nên hay né tránh những thử thách mới.\n【Phân tích】Nhận xét khuynh hướng tiêu cực -> きらいがある.",
                "grammarRule": "Phê phán một xu hướng, nếp nghĩ tiêu cực."
            },
            {
                "id": "skz_b_ch06_q11",
                "lesson": "第6課: 様子",
                "grammarPoint": "第6課 総合問題",
                "question": "怒り（　）んばかりの剣幕で、彼は部屋を飛び出していった。",
                "options": ["a. せ", "b. ", "c. し"],
                "answer": "b",
                "explanation": "【Dịch】Với khí thế đằng đằng như muốn nổ tung cơn thịnh nộ, anh ta lao vút ra khỏi phòng.\n【Phân tích】怒る -> 怒らんばかり (bỏ ない thêm んばかり).",
                "grammarRule": "V-ない (bỏ ない) ＋ んばかり: Như sắp bùng nổ."
            },
            {
                "id": "skz_b_ch06_q12",
                "lesson": "第6課: 様子",
                "grammarPoint": "第6課 総合問題",
                "question": "「任せておけ」（　）とばかりに、彼は胸をドンと叩いた。",
                "options": ["a. とばかりに", "b. んばかりに", "c. ながらに"],
                "answer": "a",
                "explanation": "【Dịch】Như muốn nói ra điệu 'Cứ để đấy cho tôi', anh ấy vỗ ngực cái bộp đầy tự tin.\n【Phân tích】Hành động ra vẻ 'cứ giao cho tôi' -> とばかりに.",
                "grammarRule": "Câu thoại ngầm ＋ とばかりに: Ra dáng, ra điệu."
            },
            {
                "id": "skz_b_ch06_q13",
                "lesson": "第6課: 様子",
                "grammarPoint": "第6課 総合問題",
                "question": "どこから（　）ともなく、美しい笛の音が聞こえてきた。",
                "options": ["a. ともなく", "b. ながらに", "c. んばかりに"],
                "answer": "a",
                "explanation": "【Dịch】Không biết tự nơi nào văng vẳng đưa lại, một tiếng sáo du dương êm ái vọng tới.\n【Phân tích】どこからともなく: Chẳng biết từ đâu đưa lại (vô định).",
                "grammarRule": "Từ nghi vấn ＋ ともなく: Không rõ là từ đâu/bao giờ."
            },
            {
                "id": "skz_b_ch06_q14",
                "lesson": "第6課: 様子",
                "grammarPoint": "第6課 総合問題",
                "question": "祖母は昔の思い出を、涙（　）ながらに語ってくれた。",
                "options": ["a. ", "b. に", "c. の"],
                "answer": "a",
                "explanation": "【Dịch】Bà vừa rưng rưng nước mắt nghẹn ngào vừa kể lại cho tôi nghe những kỷ niệm xưa cũ.\n【Phân tích】涙ながらに: Trong làn nước mắt nghẹn ngào (cụm từ cố định).",
                "grammarRule": "涙ながらに: Trong dòng nước mắt."
            },
            {
                "id": "skz_b_ch06_q15",
                "lesson": "第6課: 様子",
                "grammarPoint": "第6課 総合問題",
                "question": "彼女は自分に都合の悪い話を（　）きらいがある。",
                "options": ["a. 聞き流す", "b. 聞き流した", "c. 聞き流して"],
                "answer": "a",
                "explanation": "【Dịch】Cô ấy có cái tật hay bỏ ngoài tai những câu chuyện bất lợi cho bản thân mình.\n【Phân tích】V-る ＋ きらいがある: 聞き流すきらいがある.",
                "grammarRule": "V-る ＋ きらいがある: Có thói quen xấu."
            },
            {
                "id": "skz_b_ch06_q16",
                "lesson": "第6課: 様子",
                "grammarPoint": "第6課 総合問題",
                "question": "土下座（　）せんばかりに頭を下げて謝罪した。",
                "options": ["a. ", "b. し", "c. に"],
                "answer": "a",
                "explanation": "【Dịch】Anh ấy cúi rạp đầu xin lỗi như thể muốn quỳ mọp xuống đất đến nơi.\n【Phân tích】Động từ する -> せんばかりに (quy tắc biến đổi đặc biệt của する).",
                "grammarRule": "する -> せんばかりだ: Cứ như muốn làm đến nơi."
            },
            {
                "id": "skz_b_ch06_q17",
                "lesson": "第6課: 様子",
                "grammarPoint": "第6課 総合問題",
                "question": "「私には関係ない」（　）とばかりの態度で知らん顔をしている。",
                "options": ["a. とばかりの", "b. んばかりの", "c. ながらの"],
                "answer": "a",
                "explanation": "【Dịch】Anh ta làm bộ mặt ngơ ngác phớt lờ với thái độ như muốn bảo 'Chuyện đó chẳng liên quan gì tới tôi cả'.\n【Phân tích】Thái độ tỏ vẻ -> とばかりの態度.",
                "grammarRule": "Câu văn ＋ とばかりのN: N như muốn nói rằng..."
            },
            {
                "id": "skz_b_ch06_q18",
                "lesson": "第6課: 様子",
                "grammarPoint": "第6課 総合問題",
                "question": "この村には、昔（　）ながらの素朴な生活習慣が今も息づいている。",
                "options": ["a. ", "b. に", "c. の"],
                "answer": "a",
                "explanation": "【Dịch】Ngôi làng này cho đến tận bây giờ vẫn còn lưu giữ nguyên vẹn nếp sống mộc mạc từ thuở ngàn xưa.\n【Phân tích】昔ながらの: Vốn có giữ nguyên từ xa xưa.",
                "grammarRule": "昔ながらのN: Giữ nguyên từ ngày xưa."
            }
        ]
    },
    "ch07": {
        "chapterId": "ch07",
        "lesson": "第7課: 付随行動 (Hành động đi kèm)",
        "theme": "事柄を説明する",
        "group": "group1",
        "title": "第7課: 付随行動",
        "description": "Các mẫu ngữ pháp: ～がてら, ～かたがた, ～かたわら.",
        "questions": [
            {
                "id": "skz_b_ch07_q01",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "～がてら",
                "question": "散歩（　）がてら、近くのポストまで手紙を出しに行ってくるよ。",
                "options": ["a. ", "b. に", "c. の"],
                "answer": "a",
                "explanation": "【Dịch】Tiện thể đi dạo bộ thì tôi chạy ra hòm thư gần đây bỏ thư gửi luôn nhé.\n【Phân tích】N / V-ます (bỏ ます) ＋ がてら: Nhân tiện làm việc A thì kết hợp làm thêm việc B.",
                "grammarRule": "N / V-ます (bỏ ます) ＋ がてら: Tiện thể làm việc chính thì làm luôn việc phụ (thường là việc đi lại, sinh hoạt thường nhật)."
            },
            {
                "id": "skz_b_ch07_q02",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "～がてら",
                "question": "買い物がてら、（　）。",
                "options": ["a. 近所のカフェでお茶を飲もう", "b. 家の掃除をした", "c. 宿題を終わらせた"],
                "answer": "a",
                "explanation": "【Dịch】Tiện thể đi mua sắm thì ghé vào quán cà phê gần nhà làm tách trà luôn đi.\n【Phân tích】Hành động di chuyển đi ra ngoài tiện thể ghé quán uống trà -> お茶を飲もう.",
                "grammarRule": "Vế sau là hành vi di chuyển kết hợp cùng lộ trình."
            },
            {
                "id": "skz_b_ch07_q03",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "～かたがた",
                "question": "ご挨拶（　）かたがた、新居のお祝いにお伺いいたしました。",
                "options": ["a. ", "b. に", "c. の"],
                "answer": "a",
                "explanation": "【Dịch】Nhân tiện đi chào hỏi thăm hỏi, tôi xin phép ghé qua chúc mừng tân gia nhà mới của anh chị.\n【Phân tích】N (lịch sự, trang trọng) ＋ かたがた: Tiện thể kết hợp hai mục đích trang trọng (chào hỏi, cảm ơn, tạ lỗi).",
                "grammarRule": "N ＋ かたがた: Tiện thể (dùng trong bối cảnh giao tiếp xã hội lịch sự, trang trọng)."
            },
            {
                "id": "skz_b_ch07_q04",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "～かたがた",
                "question": "お礼かたがた、（　）。",
                "options": ["a. 近況をご報告申し上げます", "b. 買い物をした", "c. 遊びに行こう"],
                "answer": "a",
                "explanation": "【Dịch】Nhân tiện gửi lời cảm ơn sâu sắc, tôi cũng xin phép được kính báo tình hình gần đây của bản thân.\n【Phân tích】Văn phong trang trọng: ご報告申し上げます.",
                "grammarRule": "Vế sau sử dụng kính ngữ hoặc lối diễn đạt trang trọng."
            },
            {
                "id": "skz_b_ch07_q05",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "～かたわら",
                "question": "彼は会社に勤務する（　）かたわら、夜間大学で法律を学んでいる。",
                "options": ["a. ", "b. の", "c. に"],
                "answer": "a",
                "explanation": "【Dịch】Bên cạnh công việc chính là làm việc tại công ty, anh ấy còn theo học ngành luật tại trường đại học ban đêm.\n【Phân tích】V-る / Nの ＋ かたわら: Bên cạnh công việc chính thì đồng thời đảm nhiệm một công việc/hoạt động xã hội khác trong thời gian dài.",
                "grammarRule": "V-る / Nの ＋ かたわら: Bên cạnh công việc/nghề nghiệp chính yếu, đồng thời làm thêm hoạt động khác (kéo dài trong thời gian dài)."
            },
            {
                "id": "skz_b_ch07_q06",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "～かたわら",
                "question": "母は家業を手伝うかたわら、（　）。",
                "options": ["a. ボランティア活動に励んでいる", "b. ご飯を食べた", "c. テレビを見た"],
                "answer": "a",
                "explanation": "【Dịch】Mẹ tôi bên cạnh việc phụ giúp kinh doanh gia đình, còn tích cực tham gia các hoạt động tình nguyện xã hội.\n【Phân tích】Hoạt động xã hội có tính bền vững: ボランティア活動に励んでいる.",
                "grammarRule": "Hai công việc được duy trì song song, mang tính chất nghề nghiệp hoặc hoạt động xã hội."
            },
            {
                "id": "skz_b_ch07_q07",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "第7課 総合問題",
                "question": "夕涼み（　）がてら、川辺のホタルを見に行きませんか。",
                "options": ["a. がてら", "b. かたがた", "c. かたわら"],
                "answer": "a",
                "explanation": "【Dịch】Tiện thể đi hóng mát buổi chiều tối, chúng mình cùng ra bờ sông ngắm đom đóm đi không?\n【Phân tích】Hành động sinh hoạt đời thường kết hợp đi lại -> 夕涼みがてら.",
                "grammarRule": "N ＋ がてら: Tiện thể làm gì đó trong đời sống thường nhật."
            },
            {
                "id": "skz_b_ch07_q08",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "第7課 総合問題",
                "question": "出張（　）かたがた、恩師の墓参りをしてまいりました。",
                "options": ["a. がてら", "b. かたがた", "c. かたわら"],
                "answer": "b",
                "explanation": "【Dịch】Nhân chuyến công tác, tôi đã kết hợp đi viếng mộ người thầy kính yêu của mình.\n【Phân tích】Chuyến đi có mục đích nghi lễ, trang trọng -> 出張かたがた.",
                "grammarRule": "N ＋ かたがた: Tiện thể làm việc trang trọng."
            },
            {
                "id": "skz_b_ch07_q09",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "第7課 総合問題",
                "question": "彼女は小説を書く（　）かたわら、大学で文学の教鞭を執っている。",
                "options": ["a. がてら", "b. かたがた", "c. かたわら"],
                "answer": "c",
                "explanation": "【Dịch】Bên cạnh công việc chính là sáng tác tiểu thuyết, cô ấy còn tham gia giảng dạy bộ môn văn học tại trường đại học.\n【Phân tích】Hai nghề nghiệp song hành dài hạn -> ～かたわら.",
                "grammarRule": "V-る ＋ かたわら: Bên cạnh nghề chính, làm thêm việc phụ dài hạn."
            },
            {
                "id": "skz_b_ch07_q10",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "第7課 総合問題",
                "question": "花見（　）がてら、近くの神社へお参りに行こう。",
                "options": ["a. がてら", "b. かたがた", "c. かたわら"],
                "answer": "a",
                "explanation": "【Dịch】Tiện thể đi ngắm hoa anh đào, chúng mình cùng vào ngôi đền gần đó cầu nguyện luôn nhé.\n【Phân tích】Tiện thể trên đường đi ngắm hoa -> 花見がてら.",
                "grammarRule": "N ＋ がてら: Tiện thể."
            },
            {
                "id": "skz_b_ch07_q11",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "第7課 総合問題",
                "question": "無事退院のご報告（　）かたがた、主治医の先生へのお礼の手紙を書いた。",
                "options": ["a. がてら", "b. かたがた", "c. かたわら"],
                "answer": "b",
                "explanation": "【Dịch】Nhân tiện báo tin xuất viện an toàn, tôi đã viết lá thư cảm ơn gửi tới bác sĩ điều trị chính của mình.\n【Phân tích】Báo tin và cảm ơn trang trọng -> ご報告かたがた.",
                "grammarRule": "N ＋ かたがた: Báo cáo, cảm ơn trang trọng."
            },
            {
                "id": "skz_b_ch07_q12",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "第7課 総合問題",
                "question": "彼は医師として働く（　）かたわら、週末は地域のアマチュア楽団で指揮棒を振っている。",
                "options": ["a. がてら", "b. かたがた", "c. かたわら"],
                "answer": "c",
                "explanation": "【Dịch】Bên cạnh việc làm bác sĩ, vào cuối tuần anh ấy còn làm nhạc trưởng chỉ huy dàn nhạc nghiệp dư của địa phương.\n【Phân tích】Hai vai trò xã hội song song -> 働くかたわら.",
                "grammarRule": "V-る ＋ かたわら: Đảm nhiệm hai vai trò song song."
            },
            {
                "id": "skz_b_ch07_q13",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "第7課 総合問題",
                "question": "ドライブ（　）がてら、評判の道の駅に立ち寄ってみた。",
                "options": ["a. がてら", "b. かたがた", "c. かたわら"],
                "answer": "a",
                "explanation": "【Dịch】Tiện chuyến lái xe ngắm cảnh, tôi đã ghé vào trạm dừng chân nổi tiếng ven đường xem sao.\n【Phân tích】Đi dạo lái xe tiện thể ghé thăm -> ドライブがてら.",
                "grammarRule": "N ＋ がてら: Tiện thể trên đường di chuyển."
            },
            {
                "id": "skz_b_ch07_q14",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "第7課 総合問題",
                "question": "就職のご報告（　）かたがた、お世話になった先輩にお礼のお食事をごちそうした。",
                "options": ["a. がてら", "b. かたがた", "c. かたわら"],
                "answer": "b",
                "explanation": "【Dịch】Nhân tiện báo tin đã tìm được việc làm, tôi đã mời người tiền bối từng hết lòng giúp đỡ mình một bữa cơm cảm ơn.\n【Phân tích】Báo tin mừng và cảm ơn tiền bối -> ご報告かたがた.",
                "grammarRule": "N ＋ かたがた: Báo tin kết hợp cảm ơn."
            },
            {
                "id": "skz_b_ch07_q15",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "第7課 総合問題",
                "question": "農業を営む（　）かたわら、特産品を活かしたジャムの加工販売も手掛けている。",
                "options": ["a. がてら", "b. かたがた", "c. かたわら"],
                "answer": "c",
                "explanation": "【Dịch】Bên cạnh việc làm nông nghiệp, anh ấy còn kiêm luôn việc chế biến và bán mứt tận dụng nông sản đặc sản địa phương.\n【Phân tích】Hai hoạt động kinh doanh bền vững song song -> 営むかたわら.",
                "grammarRule": "V-る ＋ かたわら: Vừa làm nghề A vừa làm việc B."
            },
            {
                "id": "skz_b_ch07_q16",
                "lesson": "第7課: 付随行動",
                "grammarPoint": "第7課 総合問題",
                "question": "犬の散歩（　）がてら、コンビニで明日の朝食用のパンを買ってきた。",
                "options": ["a. がてら", "b. かたがた", "c. かたわら"],
                "answer": "a",
                "explanation": "【Dịch】Tiện thể dắt chó đi dạo, tôi đã ghé cửa hàng tiện lợi mua bánh mì cho bữa sáng mai.\n【Phân tích】Đi dạo tiện ghé mua bánh -> 散歩がてら.",
                "grammarRule": "N ＋ がてら: Tiện thể làm việc vặt thường nhật."
            }
        ]
    }
}
