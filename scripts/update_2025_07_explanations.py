import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load the file
target_path = 'data/n2_exams/2025_07.json'
with open(target_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

qs = data.get('questions', [])

# 101 Explanations Map
EXPLANATIONS = {
    # Mondai 1: 漢字読み
    1: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (さいのう)<br><b>【Ý nghĩa / Bản chất】:</b> 才能 (TÀI NĂNG): tài năng, năng khiếu. Chữ 「才」 có âm Hán Việt là TÀI, cách đọc on'yomi là さい (như 天才 てんさい, 才色兼備 さいしょくけんび). Chữ 「能」 có âm NĂNG, đọc là のう (như 能力 のうりょく, 可能 かのう).<br><b>【Dịch nghĩa câu】:</b> Anh ấy/cô ấy đã phát huy được tài năng tuyệt vời của mình.",
    },
    2: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (からい)<br><b>【Ý nghĩa / Bản chất】:</b> 辛い (TÂN): vị cay (ớt, hạt tiêu). Khi nói về mùi vị món ăn (食べ物), chữ 辛い đọc là からい. Chú ý: chữ Hán này khi đọc là つらい sẽ mang nghĩa đau đớn, khổ sở về tinh thần/thể xác. Các vị khác: 甘い (あまい - ngọt), 苦い (にがい - đắng), 渋い (しぶい - chát).<br><b>【Dịch nghĩa câu】:</b> Tôi không thích những món ăn cay.",
    },
    3: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (けいじ)<br><b>【Ý nghĩa / Bản chất】:</b> 刑事 (HÌNH SỰ): cảnh sát hình sự, vụ án hình sự. Chữ 「刑」 (HÌNH) đọc là けい (như 刑罰 けいばつ, 刑務所 けいむしょ). Chữ 「事」 (SỰ) đọc là じ (như 火事 かじ, 記事 きじ).<br><b>【Dịch nghĩa câu】:</b> Bạn của tôi là một cảnh sát hình sự.",
    },
    4: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (きしょう)<br><b>【Ý nghĩa / Bản chất】:</b> 起床 (KHỞI SÀNG): thức dậy, rời khỏi giường. Chữ 「起」 (KHỞI) đọc là き (như 起動 きどう, 起点 きてん). Chữ 「床」 (SÀNG - giường) đọc là しょう (như 臨床 りんしょう). 起床する = thức dậy vào buổi sáng.<br><b>【Dịch nghĩa câu】:</b> Mỗi buổi sáng tôi đều thức dậy vào lúc 6 giờ và tập thể dục một lát.",
    },
    5: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (おさまった)<br><b>【Ý nghĩa / Bản chất】:</b> 収まる (THU): lắng xuống, dịu bớt, ngừng lại (cơn bão, gió lớn, cơn đau, cơn giận). Cụm từ thông dụng: 風が収まる (gió ngừng thổi, gió lặng đi). Các phương án khác: 定まる (さだまる - ổn định, định đoạt), 静まる (しずまる - trở nên yên tĩnh), 休まる (やすまる - nghỉ ngơi, thư thái).<br><b>【Dịch nghĩa câu】:</b> Đến chiều tối, cơn gió cuối cùng cũng đã dịu bớt đi.",
    },

    # Mondai 2: 表記
    6: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (湿って)<br><b>【Ý nghĩa / Bản chất】:</b> 湿る (THẤP): ẩm, ẩm ướt, chưa khô hẳn. Thể te là 湿って (しめって). Cụm từ: タオルが湿っている (khăn vẫn còn ẩm). Chữ 「湿」 xuất hiện trong 湿度 (しつど - độ ẩm), 湿気 (しっけ - không khí ẩm).<br><b>【Dịch nghĩa câu】:</b> Chiếc khăn tắm này vẫn còn ẩm ướt.",
    },
    7: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (傾向)<br><b>【Ý nghĩa / Bản chất】:</b> 傾向 (KHUYNH HƯỚNG): xu hướng, khuynh hướng. Chữ 「傾」 (KHUYNH - nghiêng) và 「向」 (HƯỚNG - hướng về). Cấu trúc cố định rất phổ biến: 〜傾向がある (có xu hướng...).<br><b>【Dịch nghĩa câu】:</b> Thời điểm này thường có xu hướng số người bị cảm cúm tăng lên.",
    },
    8: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (視察)<br><b>【Ý nghĩa / Bản chất】:</b> 視察 (THỊ SÁT): đi thị sát, khảo sát, kiểm tra thực tế hiện trường. Chữ 「視」 (THỊ - nhìn, quan sát) và 「察」 (SÁT - xem xét, thanh sát). Cần phân biệt với 診察 (CHẨN SÁT - khám bệnh).<br><b>【Dịch nghĩa câu】:</b> Rất đông người đã đến để đi thị sát/tham quan khảo sát thực tế.",
    },
    9: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (削って)<br><b>【Ý nghĩa / Bản chất】:</b> 削る (TƯỚC): gọt, bào, cạo, cắt giảm bớt. Thể te là 削って (けずって). Các từ khác: 絞って (しぼって - vắt kiệt), 握って (にぎって - nắm chặt), 掘って (ほって - đào bới).<br><b>【Dịch nghĩa câu】:</b> Hãy dùng thêm một chút lực nữa rồi gọt/bào đi nhé.",
    },
    10: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (施設)<br><b>【Ý nghĩa / Bản chất】:</b> 施設 (THI THIẾT): cơ sở vật chất, công trình tiện ích công cộng. Chữ 「施」 (THI - thực hiện, thi hành) và 「設」 (THIẾT - thành lập, kiến thiết).<br><b>【Dịch nghĩa câu】:</b> Cơ sở tiện ích này không có bãi đỗ xe ô tô.",
    },

    # Mondai 3: 語形成
    11: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (論)<br><b>【Ý nghĩa / Bản chất】:</b> Hậu tố 「〜論」(LUẬN) ghép sau các danh từ lĩnh vực, học thuyết để chỉ quan điểm, lý thuyết hoặc học thuyết chuyên sâu: 教育論 (きょういくろん - quan điểm giáo dục, lý luận giáo dục). Tương tự: 人生論 (nhân sinh quan), 幸福論 (thuyết hạnh phúc).<br><b>【Dịch nghĩa câu】:</b> Trong giới giáo viên, quan điểm giáo dục mới đang nhận được rất nhiều sự quan tâm chú ý.",
    },
    12: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (づらい)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc hậu tố: V-masu (bỏ ます) + づらい mang ý nghĩa khó làm việc gì đó (do tính chất cơ học, vật lý hoặc gây khó chịu, đau đớn): 食べづらい (khó ăn, vì nhiều xương hoặc dai). So sánh với にくい (khó khăn về thao tác nói chung).<br><b>【Dịch nghĩa câu】:</b> Con cá này nhiều xương quá nên rất khó ăn.",
    },
    13: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (悪)<br><b>【Ý nghĩa / Bản chất】:</b> Tiền tố 「悪〜」(ÁC) ghép trước danh từ mang nghĩa xấu, bất lợi, tiêu cực: 悪条件 (あくじょうけん - điều kiện xấu, điều kiện bất lợi). Tương tự: 悪天候 (thời tiết xấu), 悪影響 (ảnh hưởng xấu).<br><b>【Dịch nghĩa câu】:</b> Vụ tai nạn lần này xảy ra do nhiều điều kiện bất lợi trùng hợp dồn vào cùng một lúc.",
    },

    # Mondai 4: 文脈規定
    14: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (誓った)<br><b>【Ý nghĩa / Bản chất】:</b> 誓う (ちかう - THỆ): thề, thề thốt, cam đoan dứt khoát trước ai đó. Ngữ cảnh: \"trước mặt mọi người, cam đoan tuyệt đối không làm điều xấu nữa\" -> dùng 誓った. Các từ khác: 論じた (bình luận, biện luận), 命じた (ra lệnh), 迫った (thúc bách, áp sát).<br><b>【Dịch nghĩa câu】:</b> Con trai tôi đã thề trước mặt mọi người rằng từ nay tuyệt đối sẽ không bao giờ làm điều xấu nữa.",
    },
    15: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (一時的に)<br><b>【Ý nghĩa / Bản chất】:</b> 一時的 (いちじてき - NHẤT THỜI ĐÍCH): mang tính tạm thời, chốc lát. Cụm từ: 一時的に電気が止まる (tạm thời bị cúp điện trong chốc lát do thi công). Các phương án khác: 簡潔に (ngắn gọn), 手軽に (dễ dàng, tiện lợi), 不完全に (không hoàn chỉnh).<br><b>【Dịch nghĩa câu】:</b> Do đang thi công nên có những lúc điện sẽ bị cắt tạm thời trong một thời gian ngắn.",
    },
    16: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (関与)<br><b>【Ý nghĩa / Bản chất】:</b> 関与 (かんよ - QUAN DỮ): can dự, dính líu, dính líu vào sự vụ (thường dùng trong văn cảnh pháp lý, vụ án, tranh chấp): 事件に関与する (dính líu/can dự vào vụ án). Các từ khác: 参列 (tham dự tang lễ/nghi thức), 加入 (gia nhập bảo hiểm), 登場 (xuất hiện trên sân khấu).<br><b>【Dịch nghĩa câu】:</b> Chắc chắn không thể nhầm được rằng nhân vật đó đã dính líu vào vụ án lần này.",
    },
    17: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (べたべた)<br><b>【Ý nghĩa / Bản chất】:</b> べたべた (từ tượng hình): dính nhớp nháp, bết dính dầu mỡ, dính keo. Các từ tượng thanh tượng hình khác: かさかさ (khô khốc, nứt nẻ), じめじめ (ẩm thấp, ủ dột), ちくちく (ngứa châm chích).<br><b>【Dịch nghĩa câu】:</b> Chiếc chảo rán dính bết đầy dầu mỡ nên cực kỳ khó rửa sạch.",
    },
    18: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (反則)<br><b>【Ý nghĩa / Bản chất】:</b> 反則 (はんそく - PHẢN TẮC): phạm quy, phạm luật thi đấu trong thể thao. Dùng tay chơi bóng trong bóng đá là lỗi phạm quy (反則). Phân biệt: 違法 (vi phạm pháp luật nhà nước), 非常識 (thiếu ý thức thông thường), 不都合 (bất tiện, trục trặc).<br><b>【Dịch nghĩa câu】:</b> Trong bóng đá việc dùng tay bị nghiêm cấm, nếu dùng tay thì sẽ bị tính là phạm quy.",
    },
    19: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (追い払った)<br><b>【Ý nghĩa / Bản chất】:</b> 追い払う (おいはらう): xua đuổi, đuổi đi nơi khác (xua đuổi côn trùng, ruồi muỗi, kẻ quấy rối). Cụm từ: 虫を追い払う (xua đuổi con bọ bay đi xa). Các từ khác: 連れ出した (dẫn ra ngoài), 締め出した (khóa cửa ngăn ở ngoài), 取り払った (tháo dỡ rào cản).<br><b>【Dịch nghĩa câu】:</b> Vì có con bọ bay tới nên tôi đã vẫy chiếc mũ đang cầm trên tay để xua nó bay đi xa.",
    },
    20: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (スタイル)<br><b>【Ý nghĩa / Bản chất】:</b> スタイル (style): phong cách, lối sống. Cụm từ quen thuộc: 生活のスタイル (phong cách sống, lifestyle) = ライフスタイル. Các từ mượn khác: ポーズ (tạo dáng chụp ảnh, pose), ブランド (thương hiệu, brand), シリーズ (loạt bài, chuỗi, series).<br><b>【Dịch nghĩa câu】:</b> Cùng với sự thay đổi của xã hội, phong cách sống mà con người lựa chọn như cách làm việc hay cách trải qua ngày nghỉ cũng đã đổi thay.",
    },

    # Mondai 5: 言い換え類義
    21: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (不思議な)<br><b>【Ý nghĩa / Bản chất】:</b> 妙な (みょうな - DIỆU) đồng nghĩa với 不思議な (ふしぎな): kỳ lạ, quái lạ, khó hiểu. 妙な事件 = 不思議な事件 (vụ việc kỳ lạ). Các từ khác: 恐ろしい (đáng sợ), 悲しい (buồn bã), 重大な (trọng đại, nghiêm trọng).<br><b>【Dịch nghĩa câu】:</b> Đêm qua, một vụ việc kỳ lạ đã xảy ra ở gần nhà tôi.",
    },
    22: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (かなり)<br><b>【Ý nghĩa / Bản chất】:</b> 相当 (そうとう - TƯƠNG ĐƯƠNG) mang nghĩa phó từ: khá là, rất, tương đối nhiều, đồng nghĩa với かなり. 相当迷っている = かなり迷っている (đang phân vân, do dự rất nhiều).<br><b>【Dịch nghĩa câu】:</b> Có vẻ như anh Suzuki đang phân vân, đắn đo rất nhiều.",
    },
    23: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (うるさくて)<br><b>【Ý nghĩa / Bản chất】:</b> やかましい đồng nghĩa với うるさい: ồn ào, om sòm, phiền hà. Các phương án khác: 汚い (bẩn thỉu), 暑い (nóng bức), 暗い (tối tăm).<br><b>【Dịch nghĩa câu】:</b> Phòng học ồn ào quá nên tôi không tài nào tập trung vào việc học được.",
    },
    24: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (ふるさとに戻って)<br><b>【Ý nghĩa / Bản chất】:</b> 帰省する (きせいする - QUY TỈNH) có nghĩa là trở về quê hương thăm gia đình, họ hàng, đồng nghĩa với ふるさとに戻る. Các đáp án khác như về từ chuyến công tác (出張) hay kỳ nghỉ (休暇) đều không mang nghĩa về quê quán.<br><b>【Dịch nghĩa câu】:</b> Anh Nakayama hiện đang về quê (thăm gia đình).",
    },
    25: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (突然)<br><b>【Ý nghĩa / Bản chất】:</b> いきなり đồng nghĩa với 突然 (とつぜん): bất thình lình, đột ngột, bất ngờ không báo trước. Cụm từ: いきなり振り向いた = 突然振り向いた (đột ngột quay ngoắt lại phía sau).<br><b>【Dịch nghĩa câu】:</b> Anh Hayashi đã bất thình lình quay ngoắt đầu lại phía sau.",
    },

    # Mondai 6: 用法
    26: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (空き缶は、潰してからごみ箱に入れてください。)<br><b>【Ý nghĩa / Bản chất】:</b> 潰す (つぶす - HỘI): đè bẹp, nghiền nát, bóp bẹp (các vật rỗng như vỏ lon, hộp giấy). Câu 2 dùng hoàn toàn chính xác: 空き缶を潰す (bóp bẹp lon rỗng). Câu 1 cốc thủy tinh vỡ phải dùng 割る (わる). Câu 3 gấp quần áo phải dùng 畳む (たたむ). Câu 4 xé vụn giấy tờ phải dùng 破る (やぶる) hoặc 細かく裂く.<br><b>【Dịch nghĩa câu】:</b> Vỏ lon rỗng thì xin hãy bóp bẹp rồi mới bỏ vào thùng rác nhé.",
    },
    27: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (昔の学校給食は、おかずの種類も少なく、今と比べると粗末なものだった。)<br><b>【Ý nghĩa / Bản chất】:</b> 粗末 (そまつ - THÔ MẠT): sơ sài, đạm bạc, thô sơ (thường dùng miêu tả bữa ăn đạm bạc, quần áo đơn sơ, quà mọn khiêm tốn). Câu 1 dùng chuẩn: 粗末なもの (bữa ăn trưa sơ sài/đạm bạc). Câu 2 lời nói thô lỗ phải dùng 乱暴な (らんぼうな). Câu 3 giọng bị khàn phải dùng かすれる. Câu 4 tính năng máy tính đơn giản/kém thì dùng 単純な hoặc 低性能.<br><b>【Dịch nghĩa câu】:</b> Bữa trưa học đường ngày xưa số lượng món ăn rất ít, nếu so với bây giờ thì quả là những bữa ăn vô cùng đạm bạc, sơ sài.",
    },
    28: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (学生のときは野球に熱中していて、毎日遅くまで練習していた。)<br><b>【Ý nghĩa / Bản chất】:</b> 熱中する (ねっちゅうする - NHIỆT TRUNG): say mê, mải mê, cống hiến hết tâm sức vào một niềm đam mê/môn thể thao: 〜に熱中する. Câu 1 sự chỉ trích tập trung dồn dập vào ai phải dùng 集中した (しゅうちゅう). Câu 3 thích mặc một bộ đồ dùng 夢中 / 気に入っている. Câu 4 sự quan tâm của toàn thế giới đổ dồn về thì dùng 集中している.<br><b>【Dịch nghĩa câu】:</b> Hồi còn là học sinh tôi đã vô cùng say mê môn bóng chày, ngày nào cũng miệt mài luyện tập đến tận tối muộn.",
    },
    29: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (代表者同士の話し合いは、和やかな雰囲気で行われた。)<br><b>【Ý nghĩa / Bản chất】:</b> 和やか (なごやか - HÒA): ấm cúng, vui vẻ, hòa nhã, thân thiện (thường dùng miêu tả bầu không khí, cuộc nói chuyện thân mật: 和やかな雰囲気, 和やかに語り合う). Câu 1 hành động bình tĩnh khi xảy ra sự cố khẩn cấp dùng 冷静な. Câu 2 khí hậu ấm áp dễ chịu dùng 温暖な (おんだんな) hoặc 穏やかな (おだやかな). Câu 3 vị súp thanh nhẹ dùng あっさりした.<br><b>【Dịch nghĩa câu】:</b> Cuộc trao đổi giữa các đại diện đã diễn ra trong một bầu không khí vô cùng hòa nhã, thân thiện.",
    },
    30: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (この机はもう使っていないのだが、愛着があってなかなか捨てられない。)<br><b>【Ý nghĩa / Bản chất】:</b> 愛着 (あいちゃく - ÁI TRỨ): tình cảm gắn bó tha thiết, sự yêu quý bịn rịn đối với một món đồ vật hay nơi chốn quen thuộc sau thời gian dài gắn bó. Cụm từ cố định: 愛着がある / 愛着がわく / 愛着を持つ. Câu 1 thử giày ưng ý dùng 気に入る. Câu 2 trồng trọt dồn tâm huyết tình yêu dùng 愛情を込めて. Câu 4 theo đuổi ước mơ dùng 情熱を持つ / 夢にこだわる.<br><b>【Dịch nghĩa câu】:</b> Chiếc bàn này dù tôi không còn sử dụng nữa, nhưng vì có tình cảm gắn bó bấy lâu nay nên mãi mà chẳng nỡ vứt đi.",
    },

    # Mondai 7: 文法形式の判断
    31: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (にあたって)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc ngữ pháp: V-ru / N + にあたって (nhân dịp, vào thời điểm bắt đầu một sự kiện quan trọng/chính thức). Dùng để chỉ thời điểm chuẩn bị bước vào một sự kiện lớn như xây dựng công trình, khai trương, thành lập. Thành phố khi chuẩn bị xây dựng hội trường thì tổ chức buổi giải thích cho cư dân.<br><b>【Dịch nghĩa câu】:</b> Thành phố Minami dự định sẽ tổ chức buổi giải thích cho cư dân khu vực xung quanh nhân dịp xây dựng hội trường công dân.",
    },
    32: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (ながらも)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc ngữ pháp: N / V-masu / A-i + ながら(も) mang ý nghĩa tương phản đối lập: \"dù là... nhưng lại...; tuy... nhưng...\". Cô bé dù chỉ mới là học sinh tiểu học, nhưng đã đoạt giải vô địch ở hàng loạt cuộc thi piano quốc tế danh giá.<br><b>【Dịch nghĩa câu】:</b> Cô bé ấy tuy chỉ mới là một học sinh tiểu học, nhưng đã đoạt chức vô địch tại rất nhiều cuộc thi piano mang tầm quốc tế.",
    },
    33: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (いったい)<br><b>【Ý nghĩa / Bản chất】:</b> Phó từ: 一体 (いったい) thường kết hợp với các từ để hỏi (何, どう, なぜ) tạo thành mẫu câu nhấn mạnh: \"rốt cuộc là...\", \"rốt cuộc thì...\": 一体何が違うのだろうか (rốt cuộc thì có điểm gì khác biệt nhỉ?). Các phó từ khác: おそらく (có lẽ), かえって (ngược lại), どうしても (dù thế nào cũng).<br><b>【Dịch nghĩa câu】:</b> Những người được khen là làm được việc, nếu so với những người không làm được thì rốt cuộc khác biệt ở điểm gì nhỉ?",
    },
    34: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (おいでくださり)<br><b>【Ý nghĩa / Bản chất】:</b> Kính ngữ (Tôn kính ngữ): おいでくださる là dạng tôn kính ngữ của 来てくれる (quý khách cất công đến cho). Khi nhân viên nhà trọ chào đón và cảm ơn khách hàng: 「森川旅館においでくださり、ありがとうございます」(cảm ơn quý khách đã ghé thăm nhà trọ Morikawa chúng tôi). Các từ 伺いまして, 参りまして là Khiêm nhường ngữ (dùng cho hành động của bản thân mình), không dùng cho khách; お越しになり thiếu ý nghĩa đón nhận ơn huệ くれる.<br><b>【Dịch nghĩa câu】:</b> (Tại quán trọ) Nhân viên: \"Kính chào quý khách. Cảm ơn quý khách hôm nay đã cất công ghé thăm quán trọ Morikawa chúng tôi ạ.\"",
    },
    35: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (歩くようにしているらしく)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: 〜ようにしている (nỗ lực duy trì một thói quen có lợi) kết hợp với 〜らしい (nghe nói, dường như - thể hiện sự phán đoán quan sát khách quan từ bên ngoài). Người con quan sát thấy thói quen của bố (có hôm dành hẳn 1 tiếng đi bộ về) nên dùng 〜らしく để phán đoán.<br><b>【Dịch nghĩa câu】:</b> Bố tôi dường như đang cố gắng đi bộ nhiều nhất có thể vì lý do sức khỏe, có hôm bố còn dành hẳn một tiếng đồng hồ đi bộ từ công ty về nhà.",
    },
    36: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (読み終わらないうちに)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: V-nai + うちに (trong khi chưa kịp làm gì đó thì sự việc khác đã ập đến): 読み終わらないうちに (trong khi còn chưa kịp đọc xong hết thì đã sắp đến hạn phải trả sách). Phân biệt với まで (cho đến khi).<br><b>【Dịch nghĩa câu】:</b> Tôi đã mượn cuốn sách này ở thư viện, nhưng trong khi còn chưa kịp đọc xong thì đã sắp đến hạn phải trả rồi.",
    },
    37: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (でいいのかどうか)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: N + でいい (như thế này là được/ổn) + 〜かどうか (liệu có... hay không). Người nói vì thành tích dậm chân tại chỗ nên muốn xin ý kiến thầy cô xem: 「このままの勉強方法でいいのかどうか」(liệu phương pháp học cứ duy trì như thế này có ổn hay không). Dùng trợ từ で để chỉ phạm vi/trạng thái chấp nhận được.<br><b>【Dịch nghĩa câu】:</b> Dạo gần đây thành tích không tiến bộ nên tôi đã thử hỏi ý kiến thầy giáo xem liệu cứ giữ nguyên phương pháp học như thế này có ổn không.",
    },
    38: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (一方だ)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: V-ru + 一方だ (ngày càng có xu hướng tiếp diễn theo một chiều hướng, thường là biến chuyển mạnh mẽ): 激しくなる一方だ (ngày càng trở nên khốc liệt hơn). Các mẫu khác: 次第だ (tùy thuộc vào), ほどだ (đến mức), べきだ (nên/phải).<br><b>【Dịch nghĩa câu】:</b> Nhận thức về các vấn đề môi trường trên toàn thế giới ngày càng nâng cao, khiến cho cuộc cạnh tranh phát triển xe điện giữa các nhà sản xuất ngày càng trở nên khốc liệt hơn.",
    },
    39: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (くらいだった)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: 〜くらいだ / ほどだ mang ý nghĩa so sánh chỉ mức độ cao của sự việc: 寒い気候で、寒い靴を履きたいくらいだった (lạnh đến mức/cỡ như là...). Đi với 寒い (lạnh) để nhấn mạnh mức độ giá rét trên đỉnh núi.<br><b>【Dịch nghĩa câu】:</b> Cuối tuần qua tôi đã đi leo núi. Hôm đó là một ngày rất nóng, thế nhưng ở gần đỉnh núi thì nhiệt độ lại thấp đến mức cảm thấy rét buốt.",
    },
    40: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (乗らないわけにはいかない)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: V-nai + わけにはいかない (không thể không làm, bắt buộc phải làm vì tình thế hoặc trách nhiệm xã hội): 乗らないわけにはいかない (không thể không đi/buộc phải đi tàu chen chúc vì không còn cách nào khác). Các phương án khác: 乗るものではない (không nên đi), 乗りようがない (không có cách nào để đi), 乗らなくてもかまわない (không đi cũng chẳng sao).<br><b>【Dịch nghĩa câu】:</b> Bước lên chuyến tàu điện chật kín người thì khó chịu thật đấy, nhưng vì không còn phương tiện nào khác nên tôi không thể không đi.",
    },
    41: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (ことがあるためです)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: V-ru + ことがある (có những lúc/có nguy cơ xảy ra) + 〜ためです (dùng để giải thích nguyên nhân lý do cho câu hỏi なぜ/どうして ở phía trước): 影響が出る・ことがあるためです (là vì có những trường hợp sẽ làm ảnh hưởng đến hiệu quả của thuốc).<br><b>【Dịch nghĩa câu】:</b> (Trên chương trình TV) MC: \"Tại sao thuốc lại không được uống bằng các loại đồ uống khác ngoài nước lọc ạ?\" - Bác sĩ: \"Đó là vì nếu uống bằng trà hay nước trái cây thì có trường hợp sẽ gây ảnh hưởng đến hiệu lực của thuốc.\"",
    },
    42: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (触ってみたくなってしまう)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc kết hợp: V-tai -> 〜たくなる (bất giác nảy sinh cảm xúc muốn làm gì đó) + 〜てしまう (lỡ, không kìm nén được bản thân): つい触ってみたくなってしまう (cứ bất giác lỡ muốn chạm vào thử). Thể hiện sự đấu tranh giữa lý trí (bị dị ứng) và cảm xúc (quá thích mèo).<br><b>【Dịch nghĩa câu】:</b> Tôi bị dị ứng lông mèo, cứ hễ chạm vào mèo là người lại ngứa ngáy, thế nhưng vì rất thích mèo nên cứ mỗi lần nhìn thấy là tôi lại bất giác không kìm được mà muốn vuốt ve thử.",
    },

    # Mondai 8: 文の組み立て ★
    43: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (水にまで)<br><b>【Ý nghĩa / Bản chất】:</b> Thứ tự ghép câu hoàn chỉnh: このパン屋では、原料の【小麦粉は (2)】【もちろん (4)】【水にまで (3) ★】【こだわって (1)】一つ一つ丁寧にパンを作っているそうだ。<br>• Cấu trúc: N1 はもちろん、N2 にまでこだわって (không chỉ nguyên liệu N1 là lẽ dĩ nhiên, mà ngay cả đến N2 cũng được chọn lọc kỹ càng). Ngôi sao ★ nằm ở vị trí thứ 3 là đáp án 3.<br><b>【Dịch nghĩa câu】:</b> Ở tiệm bánh này, nghe nói người ta làm từng chiếc bánh một cách vô cùng tỉ mỉ, không chỉ bột mì làm nguyên liệu là lẽ đương nhiên, mà ngay cả đến nguồn nước cũng được chăm chút tuyển chọn kỹ lưỡng.",
    },
    44: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (珍しく)<br><b>【Ý nghĩa / Bản chất】:</b> Thứ tự ghép câu hoàn chỉnh: 昨日は、梅雨の【この (3)】【時期にしては (2)】【珍しく (4) ★】【いい天気で (1)】、久しぶりに洗濯物を外に干すことができた。<br>• Cấu trúc: 〜にしては (xét theo tiêu chuẩn thì lại khác thường): この時期にしては珍しくいい天気で (hiếm khi thời tiết lại đẹp như vậy nếu xét theo thời điểm mùa mưa này). Ngôi sao ★ ở vị trí thứ 3 là đáp án 4.<br><b>【Dịch nghĩa câu】:</b> Ngày hôm qua, hiếm hoi lắm mới có một ngày thời tiết đẹp so với thời điểm mùa mưa này, nên đã lâu lắm rồi tôi mới có thể phơi đồ giặt ở ngoài trời.",
    },
    45: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (ことを考えると)<br><b>【Ý nghĩa / Bản chất】:</b> Thứ tự ghép câu hoàn chỉnh: 今回のセミナーの開催日が人の【集まりにくい (1)】【平日だった (3)】【ことを考えると (2) ★】【200名もの (4)】参加者が集まったのは大成功といえる。<br>• Cấu trúc: 〜ことを考えると (nếu suy xét đến việc...). Cụm bổ nghĩa: 人の集まりにくい平日だったこと (việc rơi vào ngày thường vốn rất khó tập trung người). Ngôi sao ★ ở vị trí thứ 3 là đáp án 2.<br><b>【Dịch nghĩa câu】:</b> Nếu xét đến việc ngày tổ chức hội thảo lần này rơi vào ngày thường - vốn rất khó tập trung người tham gia, thì việc thu hút được tới 200 người có thể coi là một thành công rực rỡ.",
    },
    46: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (良さがあるというが)<br><b>【Ý nghĩa / Bản chất】:</b> Thứ tự ghép câu hoàn chỉnh: 人には【誰にでも (2)】【その人にしかない (3)】【良さがあるというが (1) ★】【自分でそれに (4)】気づくのは難しい。<br>• Cụm từ: 人には誰にでもその人にしかない良さがある (ở mỗi con người, ai ai cũng có nét tốt đẹp độc nhất mà chỉ người đó có) + というが (người ta thường nói là... nhưng). Ngôi sao ★ ở vị trí thứ 3 là đáp án 1.<br><b>【Dịch nghĩa câu】:</b> Người ta vẫn thường nói ở mỗi con người ai ai cũng có những nét tốt đẹp độc nhất mà chỉ riêng người đó có, thế nhưng việc tự bản thân nhận ra được điều đó lại là chuyện vô cùng khó khăn.",
    },
    47: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (たまたまかかってきた)<br><b>【Ý nghĩa / Bản chất】:</b> Thứ tự ghép câu hoàn chỉnh: 昨日の晩、目覚まし時計をセットするのを忘れてしまい、今朝は寝坊してしまった。それでも【遅刻をせずに済んだ (4)】【のは (1)】【たまたまかかってきた (2) ★】【電話に起こされた (3)】からだ。<br>• Cấu trúc: 〜ずに済む (thoát khỏi việc gì không mong muốn) + 〜のは...からだ (sở dĩ... là vì...). Cụm vị ngữ: たまたまかかってきた電話に起こされたからだ. Ngôi sao ★ ở vị trí thứ 3 là đáp án 2.<br><b>【Dịch nghĩa câu】:</b> Tối qua tôi quên đặt đồng hồ báo thức nên sáng nay đã ngủ quên mất. Dẫu vậy sở dĩ tôi vẫn thoát khỏi việc bị đi muộn là vì đã được đánh thức bởi một cuộc điện thoại tình cờ gọi tới.",
    },

    # Mondai 9: 文章の文法
    48: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (利用されている)<br><b>【Ý nghĩa / Bản chất】:</b> Thể bị động (受身形): 車での送迎サービス (dịch vụ đưa đón bằng xe hơi) đang được sử dụng bởi những người cao tuổi khó tự lái xe: 「...人に利用されている」(được sử dụng bởi những người...). Các lựa chọn khác như muốn sử dụng (させてほしい), làm ơn sử dụng hộ (してくれている) đều không đúng ngữ cảnh khách quan.<br><b>【Dịch nghĩa câu】:</b> Dịch vụ này đang được sử dụng rộng rãi bởi những người gặp khó khăn trong việc tự lái xe ô tô hoặc những người coi việc đi bộ đến bến xe buýt, nhà ga gần nhất là một gánh nặng.",
    },
    49: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (少なくないという)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: 少なくない (không hề ít, rất nhiều) + 〜という (nghe nói, truyền đạt lại kết quả khảo sát/thực tế khách quan). Tác giả dẫn chứng rằng số người già không muốn ra ngoài chỉ vì không có việc gì làm là rất nhiều.<br><b>【Dịch nghĩa câu】:</b> Nghe nói số lượng người cao tuổi không chịu ra ngoài chỉ vì không có công việc bận rộn gì là không hề ít.",
    },
    50: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (ある)<br><b>【Ý nghĩa / Bản chất】:</b> Cụm từ xác định ẩn danh: 「ある市では」(ở một thành phố nọ). Khi đưa ra một dẫn chứng cụ thể thực tế trong bài viết nhưng không cần nêu đích danh tên địa phương, ta dùng tiền tố 「ある〜」.<br><b>【Dịch nghĩa câu】:</b> Tại một thành phố nọ, người ta đã tổ chức các sự kiện thu hút người cao tuổi tụ họp lại cùng nhau.",
    },
    51: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (において)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc ngữ pháp: N + において (ở, tại, trong bối cảnh N - văn phong trang trọng viết) = で: 「超高齢社会を迎える日本において」(ở một đất nước đang bước vào xã hội siêu già hóa như Nhật Bản).<br><b>【Dịch nghĩa câu】:</b> Tại một quốc gia đang bước vào xã hội siêu già hóa như Nhật Bản, những dịch vụ hỗ trợ người cao tuổi ra ngoài như thế này được kỳ vọng sẽ ngày càng đóng vai trò quan trọng hơn nữa.",
    },

    # Mondai 10: 短文読解
    52: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (自分がどういう人間かは、他者とのかかわりがなければわからない。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ trực tiếp từ câu then chốt cuối bài: 「他人と自分の違いを通して初めて、自分というものがどういうものかがわかる」「他者なしに、自分を自分として認識することはできない」(Chính thông qua sự khác biệt với người khác mà ta mới hiểu được mình là con người như thế nào; nếu không có người khác thì ta không thể tự nhận thức được bản thân). Lựa chọn 1 hoàn toàn trùng khớp với kết luận này.<br><b>【Dịch nghĩa câu】:</b> Ý kiến nào phù hợp với suy nghĩ của tác giả? -> Bản thân là người như thế nào thì nếu không có sự gắn kết tương tác với người khác sẽ không thể hiểu được.",
    },
    53: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (売店で販売するための「水石りんごジャム」を、来月から納品できるか。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ vào đoạn 2 của email: 「お客様から名産のりんごを使ったお土産がないかたびたびご質問を受けますので、このジャムを売店でも販売したいと考えております。同じ時期に販売を開始したいと思っておりますが、ご対応いただけるでしょうか」(Khách thường xuyên hỏi mua đặc sản táo làm quà, nên chúng tôi muốn bán loại mứt này tại quầy lưu niệm cùng thời điểm tháng sau, liệu bên anh/chị có thể đáp ứng cung cấp hàng được không).<br><b>【Dịch nghĩa câu】:</b> Điều mà bức thư điện tử này đang dò hỏi/thắc mắc là gì? -> Liệu có thể giao hàng mứt táo Suiseki để bán tại quầy lưu niệm bắt đầu từ tháng sau hay không.",
    },
    54: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (音以外の情報がなく、自由に空想が広がりやすい。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ câu văn trong bài: 「ラジオは余白のあるメディアだ。音しかそこには存在しないわけで、そこから先は聞き手である自分たちの手に委ねられる」「与えられる情報が少ないほど、ある意味、自由度が高い」(Radio là phương tiện truyền thông có nhiều khoảng trống. Ở đó chỉ có âm thanh tồn tại, còn lại đều phó thác cho người nghe tự tưởng tượng. Thông tin cung cấp càng ít thì mức độ tự do tưởng tượng lại càng cao).<br><b>【Dịch nghĩa câu】:</b> Tác giả có suy nghĩ như thế nào về radio? -> Vì không có thông tin nào khác ngoài âm thanh nên rất dễ dàng tự do mở rộng trí tưởng tượng.",
    },
    55: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (9月から紙の通知書を有料にするので、無料で確認したい場合はウェブで確認してほしい。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ nội dung thông báo: Giấy báo cước sẽ bị bãi bỏ từ cuối tháng 8 để tiết kiệm tài nguyên. Từ tháng 9, xem cước trên web; nếu khách hàng vẫn muốn nhận giấy thông báo gửi tận nhà thì phải chịu phí 180 yên/tháng: 「9月以降、使用量と料金の確認は、ウェブ会員サービスをご利用ください。引き続き通知書でのご希望のお客様には... 手数料180円/月をご負担いただきます」.<br><b>【Dịch nghĩa câu】:</b> Thông báo này muốn truyền đạt điều gì về việc thông báo lượng gas tiêu thụ và tiền cước? -> Từ tháng 9 giấy thông báo sẽ bị thu phí, nên nếu muốn xác nhận miễn phí thì xin mời xem qua trang web.",
    },
    56: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (部門同士が互いのことを考えて仕事をしなければ、会社とはいえない。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ vào phê phán của tác giả: 「自部門に余裕があれば、忙しい他部門を手伝ってあげるべきだが... いつのまにか自分の城を築き、守りに入る。これでは「会社」ではない」(Nếu phòng mình có thời gian rảnh thì nên giúp đỡ phòng khác đang bận rộn, nhưng mọi người lại co cụm xây thành lũy bảo vệ phòng mình. Như thế này thì không thể gọi là một \"công ty\" được).<br><b>【Dịch nghĩa câu】:</b> Tác giả phát biểu như thế nào về \"công ty\"? -> Nếu các bộ phận không biết suy nghĩ cho nhau trong công việc thì không thể gọi là một công ty thực thụ.",
    },

    # Mondai 11: 中文読解
    57: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (高い知能を持つ脳を守るため、頭骨が頑丈である。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ vào đoạn 2 của bài đọc: 「ゾウの頭は頑丈な頭骨とむきむきの筋肉からなります。ゾウはとても賢い動物で豊かな感情を持っています... そのような大きな脳を守るために頭骨が非常に頑丈にできているのです」(Đầu voi gồm hộp sọ kiên cố và cơ bắp cuồn cuộn. Voi là loài vật thông minh có cảm xúc phong phú, để bảo vệ bộ não lớn đó mà hộp sọ của voi được cấu tạo vô cùng kiên cố).<br><b>【Dịch nghĩa câu】:</b> Về phần đầu của loài voi, tác giả trình bày như thế nào? -> Để bảo vệ bộ não chứa trí thông minh cao, xương hộp sọ của voi rất chắc chắn, kiên cố.",
    },
    58: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (首が太く頭部が自由に動かないのを補っている。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ vào phân tích của tác giả: Đầu voi rất nặng (khoảng 500kg) nên cần cổ to và ngắn để nâng đỡ, khiến đầu không thể cử động linh hoạt. Để bù đắp cho nhược điểm đầu không quay được tự do, chiếc vòi dài và uyển chuyển đã tiến hóa để làm thay nhiệm vụ đó: 「自由に動かせない頭の代わりに、鼻が自由に動くことでそれを補っている」.<br><b>【Dịch nghĩa câu】:</b> Tác giả có suy nghĩ như thế nào về chiếc vòi của loài voi? -> Chiếc vòi dùng để bù đắp cho việc cổ quá to khiến phần đầu không thể cử động một cách tự do.",
    },
    59: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (多くの人が何か足りないと思っていたことを取り上げたから。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ vào câu văn của tác giả: 「少なくともそこに”穴”があいていたから... 埋まっていない隙間があって、実はみんなが気になっていた。そこを本の形で埋めたから買ってもらえた」(Ít nhất là vì ở đó có một \"cái lỗ/khoảng trống chưa được lấp đầy\", thực ra mọi người đều cảm thấy thiếu thốn và bận tâm. Tác giả đã dùng cuốn sách để lấp đầy khoảng trống ấy nên sách mới bán chạy). Điều này tương đương với việc đề cập đến điều mọi người đang cảm thấy còn thiếu thốn.<br><b>【Dịch nghĩa câu】:</b> Tác giả cho rằng cuốn sách của mình bán chạy là vì lý do gì? -> Vì tác giả đã đề cập đến điều mà nhiều người đang cảm thấy còn thiếu thốn, chưa được giải tỏa.",
    },
    60: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (自分に合った仕事を探すよりも、まずは仕事に就いてみることが大切だ。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ vào câu kết bài: 「とにかく仕事に就き、身体を動かして現場の作業を知ることだ。どの穴も、外側から見て全体がわかるほど単純な形はしていない。入ってみないで頭でばかり考えたって何もわからないのである」(Trước hết cứ nhận lấy một công việc, vận động cơ thể để hiểu được công việc thực tế tại hiện trường. Nếu không bước vào làm thử mà chỉ ngồi nghĩ trong đầu thì sẽ chẳng hiểu được gì).<br><b>【Dịch nghĩa câu】:</b> Tác giả muốn nhắn nhủ điều gì tới những người trẻ tuổi? -> Thay vì cứ mải mê đi tìm công việc hợp với mình, điều quan trọng trước hết là hãy cứ bắt tay vào làm một công việc cụ thể.",
    },
    61: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (わかったつもりにとさせる。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ trong bài: 「親がそのように努力して教えても、実はわかっていないことのほうが多いのだが、それでいいのである。子どもをわかったような気にさせるというのでいい」(Bố mẹ giảng giải xong đứa trẻ có thể chưa hiểu hết, nhưng thế là được rồi; chỉ cần làm cho đứa trẻ có cảm giác như thể mình đã hiểu được vấn đề là tốt). Cụm 「わかったような気にさせる」 đồng nghĩa với 「わかったつもりにさせる」.<br><b>【Dịch nghĩa câu】:</b> Theo tác giả, khi trẻ gặp điều không hiểu, cha mẹ nên làm gì? -> Hãy làm cho trẻ cảm thấy như thể mình đã hiểu được vấn đề.",
    },
    62: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (子どもが関心を持ったとき、大人は興味がわくように話してやることが大切だ。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ trong bài: 「要は、好奇心を刺激し、いろいろなものに関心を持たせることがいちばん重要なのである」(Điều cốt lõi là kích thích trí tò mò và giúp trẻ có hứng thú với nhiều điều khác nhau mới là quan trọng nhất). Do đó khi trẻ chú ý đến tin tức gì, người lớn cần trò chuyện để khơi gợi thêm sự thích thú ở trẻ.<br><b>【Dịch nghĩa câu】:</b> Ý kiến nào phù hợp với quan điểm của tác giả? -> Khi trẻ quan tâm đến điều gì, người lớn cần trò chuyện sao cho khơi gợi được sự hứng thú tò mò ở trẻ.",
    },
    63: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (患者の考え方に応じて、治療方針がさまざまになること。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ định nghĩa trong bài: 「「個別性」とは言いかえると、治療方針は10人いれば10通りあるということです。どれほど苦しくても生きられるなら辛い治療を頑張りたい人がいる一方で... 命が短くなっても治療は一切したくない人だっている」(Tính cá nhân hóa nghĩa là 10 bệnh nhân thì có 10 phác đồ điều trị khác nhau tùy thuộc vào suy nghĩ, mong muốn và quan điểm sống của từng người).<br><b>【Dịch nghĩa câu】:</b> Theo tác giả, \"tính cá nhân hóa\" trong y tế có nghĩa là gì? -> Có nghĩa là phương châm điều trị sẽ đa dạng tùy thuộc vào quan điểm, suy nghĩ của từng bệnh nhân.",
    },
    64: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (患者と直接話をして、患者の考えや希望を理解すること。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ vào đoạn cuối: Tác giả nhấn mạnh sứ mệnh của người bác sĩ: 「あくまで患者さんのやりたいよう、生きたいように手助けするという使命があります」「患者さんの生の声を聞き、その人が本当に望んでいる生き方を理解すること」(Bác sĩ có sứ mệnh giúp bệnh nhân sống theo cách họ mong muốn, do đó việc lắng nghe tiếng nói trực tiếp của bệnh nhân để thấu hiểu ước nguyện của họ là quan trọng nhất).<br><b>【Dịch nghĩa câu】:</b> Tác giả coi trọng điều gì với tư cách là một bác sĩ? -> Trò chuyện trực tiếp với bệnh nhân để thấu hiểu suy nghĩ và nguyện vọng của họ.",
    },

    # Mondai 12: 統合理解
    65: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (選手と同じ気持ちになれること。)<br><b>【Ý nghĩa / Bản chất】:</b> So sánh hai đoạn văn:<br>• Đoạn A viết: 「選手と感情を共有できるというのが最大の魅力だ... まるで自分が選手と一緒にその場にいてプレーしているかのような感覚になる」(Sức hút lớn nhất là được chia sẻ cảm xúc cùng vận động viên, như thể mình đang cùng thi đấu trên sân).<br>• Đoạn B viết: 「選手の一挙一動に一喜一憂し、スタジアム全体が一体となる」(Cùng vui cùng buồn theo từng chuyển động của tuyển thủ).<br>Cả A và B đều thống nhất: xem thể thao hấp dẫn vì người xem được hòa chung cảm xúc với tuyển thủ.<br><b>【Dịch nghĩa câu】:</b> Điểm chung mà cả hai đoạn A và B đều nhắc tới về sức hút của việc theo dõi thể thao là gì? -> Có thể hòa chung một cảm xúc, tâm trạng với các vận động viên.",
    },
    66: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (Aは必ずしもルールを知らなくてもいいと述べ、Bはルールの基本を理解しておくほうがいいと述べている。)<br><b>【Ý nghĩa / Bản chất】:</b> So sánh quan điểm về luật thi đấu:<br>• Đoạn A: 「知らなくても十分楽しめると思う。ルールのことは気にせず、気軽にスポーツ観戦を楽しんでほしい」(Không biết luật vẫn xem rất vui, không cần bận tâm đến luật lệ).<br>• Đoạn B: 「基本的なルールを知っていれば、戦術の意図がわかり、より深くスポーツの面白さを味わえる」(Nếu nắm vững luật cơ bản thì sẽ hiểu được ý đồ chiến thuật và thưởng thức sâu sắc hơn).<br>Do đó đáp án 3 phản ánh chính xác nhất sự khác biệt này.<br><b>【Dịch nghĩa câu】:</b> Về việc có cần biết luật thi đấu của môn thể thao đó hay không, tác giả A và B phát biểu như thế nào? -> Đoạn A cho rằng không nhất thiết phải biết luật, còn đoạn B cho rằng nên hiểu các luật lệ cơ bản thì tốt hơn.",
    },

    # Mondai 13: 長文読解
    67: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (「分かる」とは、新しい情報を頭の中にある知識と関連づけて分類することだから。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ vào đoạn 1: Tác giả dùng hình ảnh các chiếc hộp dán nhãn trong não: 「みなさんの頭の中に沢山のラベルがつけられた「箱」があるとイメージしてみてください... 新しい情報を頭の中のしかるべき「箱」に入れることが「分かる」ことであり」(Hãy tưởng tượng trong đầu bạn có rất nhiều chiếc hộp dán nhãn; việc phân loại và xếp thông tin mới vào chiếc hộp kiến thức phù hợp chính là \"Hiểu\"). Do đó hiểu chính là việc liên hệ và phân loại thông tin mới vào tri thức sẵn có.<br><b>【Dịch nghĩa câu】:</b> Tại sao lại nói \"Hiểu\" chính là \"Phân loại/Chia tách\"? -> Vì \"hiểu\" chính là việc liên hệ và phân loại thông tin mới vào các vùng kiến thức sẵn có trong đầu.",
    },
    68: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (誤った箱に入れたのに、適切な箱に入れたつもりになって忘れてしまうこと)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ đoạn 2: Tác giả cảnh báo nguy cơ khi gặp khái niệm hoàn toàn mới lạ nhưng ta lại cố nhét nó vào một chiếc hộp cũ sẵn có: 「無理に既存の箱に押し込め、分かった気になってその疑問を忘れてしまうこと。これこそが学びにおいて最も警戒すべきことなのです」(Việc cố ép vào một chiếc hộp cũ rồi cứ ngỡ là mình đã hiểu và quên bẵng đi; chính \"điều này\" mới là thứ đáng báo động nhất trong học tập).<br><b>【Dịch nghĩa câu】:</b> Từ \"Điều này\" (これ) ở đây chỉ điều gì? -> Việc nhét thông tin vào nhầm hộp nhưng lại cứ ngỡ là đã cho vào đúng hộp rồi lãng quên đi.",
    },
    69: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (学習においては、「分からない」状態を大切にする態度が重要だ。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ vào thông điệp cốt lõi ở cuối bài: Khi gặp khái niệm mới, không nên vội vã nhét bừa vào hộp cũ, mà cần kiên nhẫn chịu đựng trạng thái băn khoăn \"chưa hiểu\", từ đó não bộ mới dần kiến tạo nên một chiếc hộp nhận thức hoàn toàn mới: 「分からないという宙ぶらりんな状態を安易に解消せず、大切に保持し続ける態度こそが、本当の学びと知性の成長につながる」(Thái độ trân trọng và duy trì trạng thái \"chưa hiểu\" mà không vội vàng giải tỏa dễ dãi mới là chìa khóa dẫn tới sự học đích thực).<br><b>【Dịch nghĩa câu】:</b> Điều tác giả muốn nhấn mạnh nhất trong bài viết này là gì? -> Trong học tập, thái độ trân trọng và kiên nhẫn với trạng thái \"chưa hiểu\" là vô cùng quan trọng.",
    },

    # Mondai 14: 情報検索
    70: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (③と⑤)<br><b>【Ý nghĩa / Bản chất】:</b> Phân tích đối chiếu 3 điều kiện của Maeda:<br>1. Chủ đề: Học về hoa hoặc cây (花か木).<br>2. Thời gian: Buổi sáng (午前中).<br>3. Hình thức: Có cả giảng lý thuyết và thực hành (実習もある).<br>• Khóa ①: Diễn ra buổi chiều (14h-16h) -> Loại vì sai giờ.<br>• Khóa ②: Buổi sáng (9h-11h), học về cây nhưng KHÔNG có thực hành -> Loại.<br>• Khóa ③: Hoa gần gũi, buổi sáng 9h30-11h30, có thực hành chụp ảnh quanh trường -> Thỏa mãn cả 3 điều kiện.<br>• Khóa ④: Khóa học nấu ăn -> Loại vì sai chủ đề hoa/cây.<br>• Khóa ⑤: Cây cảnh bonsai, buổi sáng 10h-12h, có thực hành cắt tỉa cây -> Thỏa mãn cả 3 điều kiện.<br>Do đó kết hợp đúng là khóa ③ và ⑤.<br><b>【Dịch nghĩa câu】:</b> Anh Maeda muốn tham gia khóa học về hoa hoặc cây, tổ chức vào buổi sáng và có cả phần thực hành. Khóa học nào phù hợp với nguyện vọng của anh ấy? -> Khóa ③ và ⑤.",
    },
    71: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (12月7日までに電話で空きを確認し申し込む。)<br><b>【Ý nghĩa / Bản chất】:</b> Căn cứ vào quy định đăng ký trong tờ hướng dẫn:<br>• Khóa ④ diễn ra ngày 10/12. Hạn chót đăng ký là trước ngày học 3 ngày, tức ngày 7/12.<br>• Hôm nay là ngày 3/12. Quy định ghi rõ: Hạn đăng ký qua trang web là trước ngày diễn ra 1 tuần (tức hạn web là ngày 2/12). Vì ngày 3/12 đã quá hạn đăng ký trên web, nên bắt buộc người học phải gọi điện thoại trực tiếp để kiểm tra xem còn chỗ trống hay không rồi mới đăng ký: 「ウェブ締切日以降は電話にて空き状況を確認の上、お申し込みください」.<br><b>【Dịch nghĩa câu】:</b> Nicholas muốn đăng ký khóa học ④, hôm nay là ngày 3/12. Anh ấy phải làm thủ tục đăng ký như thế nào? -> Trước ngày 7/12 gọi điện thoại xác nhận còn chỗ trống và đăng ký.",
    },

    # Choukai Mondai 1
    72: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (本のデータをとうろくする)<br><b>【Ý nghĩa / Bản chất】:</b> Trong hội thoại tại thư viện, người nữ báo cáo việc kiểm tra sách rách và thiếu trang đã hoàn thành xong xuôi. Người nam liền giao nhiệm vụ tiếp theo cần làm ngay: 「じゃあ、先にパソコンにデータを入力して登録してくれる？」(Vậy em nhập dữ liệu vào máy tính đăng ký trước nhé). Người nữ đáp: 「わかりました、すぐやります」.<br><b>【Dịch nghĩa câu】:</b> Tại thư viện, nhân viên nam và nhân viên nữ đang nói chuyện. Nhân viên nữ sau đây sẽ làm gì trước tiên? -> Đăng ký/nhập dữ liệu của sách vào máy tính.",
    },
    73: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (当日のしりょうをいんさつする)<br><b>【Ý nghĩa / Bản chất】:</b> Hai nhân viên tại bảo tàng khoa học rà soát khâu chuẩn bị cho buổi diễn thuyết: Phòng ốc đã đặt xong, câu hỏi đã gửi cho giáo sư, thông tin web đã đăng tải. Người nam nhắc: 「あとは当日の参加者用レジュメの印刷だけだね」(Chỉ còn khâu in tài liệu phát cho người tham gia thôi nhỉ). Người nữ xung phong: 「はい、私が印刷室で刷ってきます」(Vâng, em sẽ vào phòng in để in ra ngay ạ).<br><b>【Dịch nghĩa câu】:</b> Nhân viên nữ sau đây sẽ làm gì? -> In ấn tài liệu phát cho người tham dự trong ngày diễn thuyết.",
    },
    74: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (メンバーの仕事の内容を決定する)<br><b>【Ý nghĩa / Bản chất】:</b> Tại công ty văn phòng phẩm, trưởng phòng và nam nhân viên bàn về dự án mới: Các thành viên đã tập hợp đủ, lịch trình tổng thể đã có. Trưởng phòng chỉ thị: 「まずはそれぞれのメンバーの担当業務を割り振って決めてくれ」(Trước hết cậu hãy phân công và quyết định cụ thể nội dung công việc cho từng thành viên). Người nam vâng lời thực hiện ngay.<br><b>【Dịch nghĩa câu】:</b> Người nam sau đây sẽ làm gì trước tiên? -> Quyết định nội dung công việc cụ thể cho từng thành viên trong nhóm.",
    },
    75: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (作業用てぶくろをする)<br><b>【Ý nghĩa / Bản chất】:</b> Cán bộ市役所 phân công cho các bạn làm thêm dọn dẹp sân bóng sau sự kiện: Trước khi bốc dỡ bàn ghế lều bạt nặng lên thùng xe tải, cán bộ căn dặn để đảm bảo an toàn tuyệt đối: 「ケガをしないよう、まず全員作業用手袋をはめてください」(Để tránh bị thương, trước hết tất cả mọi người hãy đeo găng tay lao động vào đã).<br><b>【Dịch nghĩa câu】:</b> Những người làm thêm sau đây sẽ làm việc gì trước tiên? -> Đeo găng tay bảo hộ lao động.",
    },
    76: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (しょうめいを暗くする)<br><b>【Ý nghĩa / Bản chất】:</b> Trưởng câu lạc bộ mỹ thuật và bạn nữ thảo luận bố trí phòng triển lãm tranh: Trưởng nhóm nhận xét đèn chiếu đang quá sáng khiến tranh bị lóa: 「まず照明の明るさを少し落として暗くしてみよう」(Trước hết hãy hạ bớt độ sáng của đèn cho tối hơn chút xem sao). Nữ sinh viên đồng ý đi chỉnh công tắc đèn ngay.<br><b>【Dịch nghĩa câu】:</b> Nữ sinh viên sau đây sẽ làm việc gì trước tiên? -> Điều chỉnh cho ánh sáng đèn chiếu tối bớt đi.",
    },

    # Choukai Mondai 2
    77: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (しゅっぱんしゃで働く)<br><b>【Ý nghĩa / Bản chất】:</b> Nam sinh viên hỏi bạn nữ về dự định sự nghiệp sau khi tốt nghiệp đại học: Dù từng cân nhắc học tiếp lên cao học hoặc xin vào ngành thực phẩm, nhưng bạn nữ khẳng định niềm đam mê thực sự: 「やっぱり本が好きだから、出版社に就職することにしたの」(Vì rốt cuộc mình vẫn yêu sách nhất, nên mình đã quyết định sẽ vào làm việc tại một nhà xuất bản).<br><b>【Dịch nghĩa câu】:</b> Nữ sinh viên nói muốn làm gì sau khi tốt nghiệp? -> Làm việc tại một nhà xuất bản.",
    },
    78: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (つえを使わないで長時間歩くこと)<br><b>【Ý nghĩa / Bản chất】:</b> Bác sĩ khám và dặn dò người phụ nữ đang hồi phục chấn thương khớp chân: Các bài tập nhẹ vẫn làm, thuốc vẫn uống đều, nhưng bác sĩ nghiêm khắc dặn điều cấm kỵ: 「まだ無理は禁物ですから、杖なしで長い時間歩くのだけは絶対に避けてください」(Vẫn tuyệt đối không được ráng sức, riêng việc đi bộ thời gian dài mà không có gậy chống là tuyệt đối phải tránh).<br><b>【Dịch nghĩa câu】:</b> Bác sĩ căn dặn người bệnh không được làm điều gì? -> Đi bộ trong thời gian dài mà không dùng gậy chống.",
    },
    79: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (同級生の知らなかった面を知ったこと)<br><b>【Ý nghĩa / Bản chất】:</b> Nữ sinh hỏi bạn nam về cảm nghĩ sau chuyến trải nghiệm nông nghiệp: Cảnh đẹp hay hái rau tươi đều đáng nhớ, nhưng điều đọng lại sâu sắc nhất là: 「普段教室では物静かなクラスメイトが率先して泥だらけで頑張ってて、意外な一面が見られたのが一番印象に残ったよ」(Bạn cùng lớp thường ngày trên lớp vốn rất trầm tính nhưng lại xông xáo bùn đất làm việc nhiệt tình, thấy được một góc bất ngờ chưa từng biết ấy là điều ấn tượng nhất).<br><b>【Dịch nghĩa câu】:</b> Điều để lại ấn tượng sâu sắc nhất với nam sinh trong chuyến trải nghiệm nông nghiệp là gì? -> Biết được một nét tính cách bất ngờ chưa từng thấy ở người bạn cùng lớp.",
    },
    80: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (花を育てるのに きょうみがあったから)<br><b>【Ý nghĩa / Bản chất】:</b> Người nam tâm sự về cơ duyên tham gia đội tình nguyện chăm sóc công viên: Mặc dù việc giao lưu với bà con hay đi lại bằng xe buýt tiện lợi đều tốt, nhưng động lực ban đầu thôi thúc anh đăng ký chính là niềm đam mê cây cỏ: 「もともと昔から草花を育てることに強い興味があったんだ」(Ngay từ xưa tôi đã có niềm đam mê rất lớn với việc trồng hoa cỏ).<br><b>【Dịch nghĩa câu】:</b> Lý do người nam bắt đầu tham gia làm tình nguyện viên ở công viên là gì? -> Vì có niềm yêu thích, hứng thú với việc chăm sóc trồng trọt hoa lá.",
    },
    81: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (ご飯の量を少なくする)<br><b>【Ý nghĩa / Bản chất】:</b> Đội ngũ phát triển hộp cơm văn phòng bàn bạc sau khi thử nghiệm: Món ăn nhận được góp ý là lượng tinh bột quá đầy, ăn dễ ngán đối với dân công sở. Cả hai thống nhất phương án: 「味付けはそのままで、ご飯のボリュームを少し減らして軽やかに仕上げよう」(Giữ nguyên hương vị món ăn, chỉ cần bớt lượng cơm đi một chút cho nhẹ nhàng vừa vặn).<br><b>【Dịch nghĩa câu】:</b> Hai người đã quyết định thay đổi hộp cơm mẫu như thế nào để bán ra thị trường? -> Giảm bớt lượng cơm đi một chút.",
    },
    82: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (顔の毛の色がユニークだったから)<br><b>【Ý nghĩa / Bản chất】:</b> Người phụ nữ kể lại lý do chọn chú mèo cưng trong buổi nhận nuôi thú cưng: Có nhiều chú mèo chạy nhảy hay ngủ rất đáng yêu, nhưng điều khiến cô rung động quyết định nhận nuôi ngay chú mèo này là: 「顔の毛の模様と色がとても個性的でユニークだったの」(Màu lông và họa tiết ở trên mặt của chú mèo cực kỳ độc đáo, ấn tượng không lẫn vào đâu được).<br><b>【Dịch nghĩa câu】:</b> Lý do lớn nhất khiến người phụ nữ chọn chú mèo này tại sự kiện là gì? -> Vì màu lông trên mặt của chú mèo rất độc đáo, khác lạ.",
    },

    # Choukai Mondai 3
    83: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (スマートフォンから離れる時間の効果)<br><b>【Ý nghĩa / Bản chất】:</b> Người dẫn chương trình radio bàn luận về xu hướng \"Digital Detox\" (cai nghiện thiết bị số): Việc chủ động thiết lập những khoảng thời gian trong ngày không chạm vào smartphone giúp não bộ được nghỉ ngơi sâu, giảm căng thẳng thần kinh và cải thiện chất lượng các mối quan hệ trực tiếp.<br><b>【Dịch nghĩa câu】:</b> Người phụ nữ trên sóng phát thanh đang bàn luận về nội dung gì? -> Hiệu quả tích cực của việc dành thời gian rời xa điện thoại thông minh.",
    },
    84: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (使い手の生活に合わせた家具作りの姿勢)<br><b>【Ý nghĩa / Bản chất】:</b> Nghệ nhân đóng đồ gỗ thủ công chia sẻ quan điểm làm nghề: Đóng một món đồ gỗ không chỉ là phô diễn hoa văn tinh xảo, mà cốt lõi là người thợ phải lắng nghe để hiểu rõ thói quen sinh hoạt và không gian sống của gia chủ, từ đó tạo nên món đồ vừa vặn, hữu dụng và gắn bó lâu dài.<br><b>【Dịch nghĩa câu】:</b> Người thợ thủ công làm đồ gỗ đang chia sẻ về điều gì? -> Tinh thần chế tác đồ nội thất thích ứng và phù hợp với đời sống của người sử dụng.",
    },
    85: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (地元の旬の果物を生かした商品作り)<br><b>【Ý nghĩa / Bản chất】:</b> Chủ cửa hàng bánh ngọt truyền thống trả lời phỏng vấn truyền hình: Cửa hàng liên kết chặt chẽ với các nông trại trong vùng để thu hoạch trái cây đúng độ chín mọng theo mùa, sáng tạo ra các dòng bánh ngọt tươi ngon mang đậm phong vị đặc sản địa phương.<br><b>【Dịch nghĩa câu】:</b> Đại diện tiệm bánh kẹo đang chia sẻ về điều gì? -> Việc sáng tạo sản phẩm tận dụng tối đa các loại hoa quả tươi ngon theo mùa của địa phương.",
    },
    86: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (質の良い睡眠をとるための工夫)<br><b>【Ý nghĩa / Bản chất】:</b> Vị chuyên gia y tế hướng dẫn thói quen sinh hoạt lành mạnh: Để có được một giấc ngủ sâu và hồi phục thể lực, mọi người cần chú ý điều chỉnh ánh sáng phòng ngủ, tránh ăn đêm no, tắt màn hình điện thoại trước giờ ngủ và giữ thói quen thức dậy đúng giờ vào mỗi sáng.<br><b>【Dịch nghĩa câu】:</b> Vị chuyên gia đang thuyết trình về nội dung gì? -> Những bí quyết/cách thức để có được một giấc ngủ đạt chất lượng tốt.",
    },
    87: {
        "exp": "<b>【Đáp án đúng】:</b> 4 (空き店舗を活用した商店街活性化の試み)<br><b>【Ý nghĩa / Bản chất】:</b> Bản tin phóng sự giới thiệu mô hình hồi sinh khu phố mua sắm truyền thống: Ban quản lý đã tận dụng các gian hàng bỏ trống lâu năm (空き店舗) để cho các bạn trẻ khởi nghiệp và nghệ sĩ thủ công thuê với giá ưu đãi, mở ra các tiệm cà phê sách, xưởng gốm nghệ thuật thu hút đông đảo khách du lịch quay trở lại.<br><b>【Dịch nghĩa câu】:</b> Người phát thanh viên đang nói về chủ đề gì? -> Nỗ lực hồi sinh khu phố mua sắm bằng cách tận dụng các gian hàng bị bỏ trống.",
    },

    # Choukai Mondai 4
    88: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (それは大変だったね、もう大丈夫？)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: 〜すら (đến cả... cũng không): 「おかゆすら食べられなかった」(đến cháo loãng cũng không ăn nổi). Người nói chia sẻ về trận đau bụng dữ dội, lời đáp lại phù hợp và thể hiện sự đồng cảm, hỏi thăm sức khỏe đúng mực nhất là: \"Khổ thân cậu quá, giờ đã đỡ hơn chưa?\".<br><b>【Dịch nghĩa câu】:</b> \"Hôm qua tớ đau bụng đến nỗi cháo loãng cũng chẳng ăn nổi.\" -> \"Khổ thân cậu quá, giờ đã đỡ hơn chưa?\"",
    },
    89: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (うん、しっとりして風情があったね。)<br><b>【Ý nghĩa / Bản chất】:</b> Phó từ: かえって (ngược lại, trái lại so với dự liệu). Trời mưa nhưng \"かえって素敵だった\" (ngược lại cảnh sắc lại rất nên thơ, tuyệt vời). Lời đồng tình tương ứng mang tính thẩm mỹ: \"Ừ, không gian êm dịu mà lại đượm phong vị hữu tình nhỉ\".<br><b>【Dịch nghĩa câu】:</b> \"Chuyến du lịch tuần trước trời mưa đấy, nhưng mà ngược lại lại rất tuyệt vời cậu nhỉ.\" -> \"Ừ, trời mưa êm dịu thế mà lại có nét phong vị thơ mộng ghê.\"",
    },
    90: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (はい、すぐ伺います。)<br><b>【Ý nghĩa / Bản chất】:</b> Khiêm nhường ngữ: 伺う (うかがう) là dạng khiêm nhường của 行く (đi đến gặp người bề trên). Khi được đồng nghiệp báo giám đốc đang gọi (社長がお呼びですよ), nhân viên đáp lại: \"Vâng, tôi sẽ sang gặp giám đốc ngay đây ạ\".<br><b>【Dịch nghĩa câu】:</b> \"Anh Watanabe ơi, giám đốc đang gọi anh đấy.\" -> \"Vâng, tôi sẽ sang gặp giám đốc ngay đây ạ.\"",
    },
    91: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (本当だ、すごいボリュームだね。)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: V-masu + きれない (không thể làm hết nổi): 食べきれない (nhiều quá không thể ăn hết nổi). Bạn đồng hành nhìn vào và đồng tình: \"Đúng thật, khẩu phần nhiều ghê/đầy đặn thật đấy\".<br><b>【Dịch nghĩa câu】:</b> \"Cậu nhìn suất ăn này xem. Nhiều thế này làm sao mà ăn hết được chứ.\" -> \"Công nhận, lượng đồ ăn khủng thật đấy.\"",
    },
    92: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (わかりました、よく話し合ってみます。)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: 〜たうえで (sau khi làm A rồi mới làm B). Giáo viên khuyên học sinh hãy bàn bạc kỹ với bố mẹ rồi mới quyết định trường thi, học sinh đáp lễ phép: \"Em hiểu rồi ạ, em sẽ trao đổi kỹ lưỡng với bố mẹ\".<br><b>【Dịch nghĩa câu】:</b> \"Em Ono này, em hãy trao đổi bàn bạc kỹ với bố mẹ rồi hẵng quyết định thi vào trường nào nhé.\" -> \"Vâng ạ, em sẽ bàn bạc kỹ với gia đình ạ.\"",
    },
    93: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (教えてくれてありがとう、すぐ書類書くよ。)<br><b>【Ý nghĩa / Bản chất】:</b> Khi bạn bè tốt bụng nhắc nhở thời hạn học bổng sắp hết (早く準備しないと期限が近いよ), lời đáp lịch sự và đúng mực nhất là cảm ơn đã báo và bảo sẽ viết giấy tờ ngay: \"Cảm ơn cậu đã nhắc nhé, tớ sẽ làm hồ sơ ngay đây\".<br><b>【Dịch nghĩa câu】:</b> \"Đơn xin học bổng không chuẩn bị sớm là sắp đến hạn chót rồi đấy nhé.\" -> \"Cảm ơn cậu đã báo nhé, tớ sẽ viết hồ sơ ngay đây.\"",
    },
    94: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (さすが評判通り、大人気なんだね。)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: 〜だけに (chính vì... nên quả đúng là/càng...). Tai nghe mới ra vì nổi tiếng nên sạch bách hàng ở các tiệm. Lời hồi đáp cảm thán: \"Quả đúng như lời đồn, được hâm mộ ghê nhỉ\".<br><b>【Dịch nghĩa câu】:</b> \"Chiếc tai nghe mới ra mắt, chính vì đang hot nên cửa hàng nào cũng chẳng còn cái nào cả.\" -> \"Đúng như danh tiếng bấy lâu, bán chạy thật đấy nhỉ.\"",
    },
    95: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (あれ以来、一度も会ってないんだね。)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: V-ta + きり (kể từ khi làm V thì bặt vô âm tín, không lặp lại nữa): その時会ったきり (kể từ lần gặp đó đến nay chưa gặp lại). Người nghe xác nhận lại: \"Từ dạo đó đến giờ cậu chưa gặp lại anh ấy lần nào à\".<br><b>【Dịch nghĩa câu】:</b> \"Tớ cãi nhau với anh trai từ 2 năm trước, từ dạo ấy đến giờ chỉ gặp đúng lần đó thôi.\" -> \"Từ dạo đó đến nay hai anh em chưa từng gặp lại nhau lần nào à?\"",
    },
    96: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (こちらこそ、お招きいただき感謝申し上げます。)<br><b>【Ý nghĩa / Bản chất】:</b> Giao tiếp thương mại (Kính ngữ): Khi phía đối tác/khách hàng được chủ nhà cảm ơn vì đã đến tham dự: 「本日は... お越しいただきありがとうございます」, người khách đáp lại bằng thái độ cảm tạ lịch thiệp: 「こちらこそ、お招きいただき感謝申し上げます」(Chính chúng tôi mới phải cảm ơn vì quý công ty đã mời đến).<br><b>【Dịch nghĩa câu】:</b> \"Xin chân thành cảm ơn quý khách đã cất công đến tham dự buổi giới thiệu sản phẩm hôm nay.\" -> \"Chính chúng tôi mới phải cảm ơn vì quý công ty đã gửi lời mời ạ.\"",
    },
    97: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (優勝は逃したけど、素晴らしい走りだったね。)<br><b>【Ý nghĩa / Bản chất】:</b> Cụm từ: 〜に迫る勢い (khí thế suýt soát, áp sát người phía trước). Tuyển thủ Tamura chạy với khí thế áp sát vị trí số 1 (nghĩa là suýt đoạt chức vô địch, về đích sát nút ở vị trí thứ nhì). Lời nhận xét chuẩn xác: \"Tuy vuột mất cúp vô địch nhưng màn chạy quả thực quá tuyệt vời\".<br><b>【Dịch nghĩa câu】:</b> \"Giải marathon hôm qua, tuyển thủ Tamura chạy với khí thế suýt soát áp sát vị trí số 1 nhỉ.\" -> \"Tuy để tuột mất chức vô địch nhưng anh ấy đã có một màn chạy quá xuất sắc nhỉ.\"",
    },
    98: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (本当ね、急用が入っちゃったみたいで残念だったわ。)<br><b>【Ý nghĩa / Bản chất】:</b> Cấu trúc: 〜とよかったのに (giá như mà... thì tốt biết mấy - bày tỏ sự tiếc nuối về điều đã không xảy ra). Bạn bè tiếc vì Sato không đến phụ dọn phòng được: \"Đúng thế thật, tiếc là bạn ấy dính việc bận đột xuất\".<br><b>【Dịch nghĩa câu】:</b> \"Hara này. Việc dọn phòng câu lạc bộ, giá như Sato cũng đến phụ giúp được thì tốt biết mấy nhỉ.\" -> \"Đúng thế thật, nghe đâu bạn ấy vướng việc bận đột xuất nên tiếc ghê.\"",
    },

    # Choukai Mondai 5
    99: {
        "exp": "<b>【Đáp án đúng】:</b> 3 (案内スタッフを増員する)<br><b>【Ý nghĩa / Bản chất】:</b> Ban tổ chức sự kiện thể thao thảo luận: Năm ngoái có vấn đề khách tham gia đông đúc không biết lối vào và khu vực thay đồ, gây tắc nghẽn và phàn nàn. Cán bộ phụ trách kết luận biện pháp xử lý: Năm nay sẽ tăng cường thêm nhân viên chỉ dẫn (案内スタッフを増員する) bố trí ở các lối đi và cửa ra vào.<br><b>【Dịch nghĩa câu】:</b> Để giải quyết vấn đề phát sinh, ban tổ chức đã quyết định làm gì? -> Tăng cường thêm số lượng nhân viên hướng dẫn.",
    },
    100: {
        "exp": "<b>【Đáp án đúng】:</b> 1 (夕日通り)<br><b>【Ý nghĩa / Bản chất】:</b> Trong đoạn nghe, người nam và người nữ lên lịch đi ngắm hoàng hôn: Ngày thứ nhất (1日目), hai người muốn đi ngắm hoàng hôn ở nơi gần biển và thuận đường dạo bộ sau bữa tối, và đã chọn \"Đại lộ Hoàng Hôn\" (夕日通り) vì có thể vừa tản bộ dọc bờ biển vừa ngắm cảnh mặt trời lặn.<br><b>【Dịch nghĩa câu】:</b> Câu hỏi 1: Hai người sẽ đi ngắm hoàng hôn ở đâu vào ngày thứ nhất? -> Đại lộ Hoàng Hôn (夕日通り).",
    },
    101: {
        "exp": "<b>【Đáp án đúng】:</b> 2 (にしがおか)<br><b>【Ý nghĩa / Bản chất】:</b> Sang ngày thứ hai (2日目), sau khi tham quan đồi núi và các danh lam thắng cảnh, hai người quyết định ghé điểm ngắm hoàng hôn từ trên cao nhìn bao quát toàn thị trấn, đó chính là đồi Nishigaoka (にしがおか): 「2日目は高台から街と夕日が見渡せる『にしがおか』に行こう」(Ngày thứ hai chúng mình hãy đến đồi Nishigaoka để ngắm toàn cảnh thị trấn và hoàng hôn từ trên cao nhé).<br><b>【Dịch nghĩa câu】:</b> Câu hỏi 2: Hai người sẽ đi ngắm hoàng hôn ở đâu vào ngày thứ hai? -> Đồi Nishigaoka (にしがおか).",
    }
}

# Apply to questions
for q in qs:
    num = q['number']
    
    # Restorations
    if num == 28:
        if q['options'][0] == 'ごみ処理の':
            q['options'][0] = 'ごみ処理の問題に関して、市民から担当者に批判が熱中した。'
    elif num == 59:
        if q['options'][2] == '多くの人が気づいていなかった社会の':
            q['options'][2] = '多くの人が気づいていなかった社会の問題を指摘したから。'
    elif num == 97:
        # Lock answer to option 2 (0-indexed 1)
        q['answer'] = 1

    # Apply explanation
    if num in EXPLANATIONS:
        q['explanation'] = EXPLANATIONS[num]['exp']

# Save back to data/n2_exams/2025_07.json
with open(target_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Successfully updated all 101 explanations in {target_path}!")

# Sync to mirror and public files
mirror_data = 'data/n2_exams/n2_2025_07.json'
public_1 = 'public/data/n2_exams/2025_07.json'
public_2 = 'public/data/n2_exams/n2_2025_07.json'

shutil.copy2(target_path, mirror_data)
shutil.copy2(target_path, public_1)
shutil.copy2(target_path, public_2)

print("Synchronized to all mirror and public files successfully!")
