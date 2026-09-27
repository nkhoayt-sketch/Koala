# -*- coding: utf-8 -*-
import json
import os

DAY06 = {
    "day": 6,
    "title": "第6日: 類義語・用法特訓 2",
    "proverb": "表の裏は六（おもてのうらはろく）: There are two sides to everything",
    "description": "Trọn bộ 45 câu hỏi thực tế trong sách '20日で合格 N1 文字・語彙・文法' (Trang 46 đến Trang 53) với đầy đủ 問題 1 đến 問題 7.",
    "totalQuestions": 45,
    "questions": [
        # 問題1：漢字読み
        {
            "id": "d06-q01", "number": 1, "section": "問題1: 漢字読み",
            "instruction": "_____の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "渡辺さんは事業に成功して、巨万の富を<u>築いた</u>。",
            "targetWord": "築いた", "options": ["うずいた", "つまずいた", "きずいた", "かしずいた"], "answer": 2,
            "explanation": "【正解】3 (きずいた)\n\n• 築く（きずく）：Xây dựng, gây dựng của cải/thành trì.\n• 躓く (つまずく - vấp ngã), 傅く (かしずく - cung phụng/hầu hạ).\n\n【Dịch nghĩa】\nÔng Watanabe đã thành công trong kinh doanh và gây dựng khối tài sản kếch xù."
        },
        {
            "id": "d06-q02", "number": 2, "section": "問題1: 漢字読み",
            "instruction": "_____の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "清水君の立場を<u>察すると</u>、同情せずにはいられない。",
            "targetWord": "察すると", "options": ["せっする", "さっする", "ほっする", "きっする"], "answer": 1,
            "explanation": "【正解】2 (さっする)\n\n• 察する（さっする）：Thấu hiểu, cảm thông nỗi niềm của người khác.\n• 接する (せっする - tiếp xúc), 欲する (ほっする - mong muốn/thèm khát).\n\n【Dịch nghĩa】\nThấu hiểu hoàn cảnh của Shimizu, tôi không thể không đồng cảm với cậu ấy."
        },
        {
            "id": "d06-q03", "number": 3, "section": "問題1: 漢字読み",
            "instruction": "_____の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "雪景色が朝日に<u>映えて</u>、本当に美しかった。",
            "targetWord": "映えて", "options": ["はえて", "ひえて", "ふえて", "ほえて"], "answer": 0,
            "explanation": "【正解】1 (はえて)\n\n• 映える（はえる）：Ánh lên, rực sáng lên, nổi bật vẻ đẹp dưới ánh sáng.\n• 冷える (ひえる - lạnh đi), 増える (ふえる - tăng lên), 吠える (ほえる - sủa).\n\n【Dịch nghĩa】\nCảnh tuyết ánh lên dưới nắng sớm ban mai thực sự vô cùng tuyệt đẹp."
        },
        {
            "id": "d06-q04", "number": 4, "section": "問題1: 漢字読み",
            "instruction": "_____の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "ビール会社の<u>合併</u>の話はうまくいかなかった。",
            "targetWord": "合併", "options": ["ごうべん", "ごうへい", "がつへい", "がっぺい"], "answer": 3,
            "explanation": "【正解】4 (がっぺい)\n\n• 合併（がっぺい）：Sáp nhập doanh nghiệp/công ty. Biến âm xúc âm 「がっぺい」.\n\n【Dịch nghĩa】\nChuyện bàn thảo sáp nhập giữa hai công ty bia đã không diễn ra suôn sẻ."
        },
        {
            "id": "d06-q05", "number": 5, "section": "問題1: 漢字読み",
            "instruction": "_____の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "裏で<u>細工</u>をするような人間を信用してはいけない。",
            "targetWord": "細工", "options": ["ほそく", "ほそこう", "さいく", "さいこう"], "answer": 2,
            "explanation": "【正解】3 (さいく)\n\n• 細工（さいく）：Giở trò thủ đoạn mánh khóe ngầm / chế tác tinh xảo.\n\n【Dịch nghĩa】\nKhông được tin tưởng những kẻ giở trò thủ đoạn mánh khóe sau lưng."
        },
        {
            "id": "d06-q06", "number": 6, "section": "問題1: 漢字読み",
            "instruction": "_____の言葉の読み方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "隊員は厳しい規則に<u>束縛</u>され、ほとんど自由がなかった。",
            "targetWord": "束縛", "options": ["そくはく", "そくばく", "ぞくはく", "ぞくばく"], "answer": 1,
            "explanation": "【正解】2 (そくばく)\n\n• 束縛（そくばく）：Trói buộc, giam hãm tự do. 縛 đọc âm đục là 「ばく」.\n\n【Dịch nghĩa】\nCác đội viên bị trói buộc bởi những quy định nghiêm ngặt, hầu như chẳng có chút tự do nào."
        },

        # 問題2：文脈規定
        {
            "id": "d06-q07", "number": 7, "section": "問題2: 文脈規定",
            "instruction": "（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "漢字の必要性を痛感し、彼は（　）もふらず覚え続けた。",
            "options": ["わき見", "わき目", "よそ見", "よそ目"], "answer": 1,
            "explanation": "【正解】2 (わき目)\n\n• わき目もふらず（脇目も振らず）：Tập trung cao độ không hề xao nhãng sang hai bên.\n• よそ見 (ngó nghiêng chỗ khác) nhưng quán ngữ chuẩn là 「わき目もふらず」."
        },
        {
            "id": "d06-q08", "number": 8, "section": "問題2: 文脈規定",
            "instruction": "（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "フランス映画の新作が（　）されたが、客足が伸びていない。",
            "options": ["配布", "分配", "配給", "配分"], "answer": 2,
            "explanation": "【正解】3 (配給)\n\n• 配給（はいきゅう）：Phát hành/phân phối phim ảnh chiếu rạp (映画の配給).\n• 配布 (phát tờ rơi), 分配 (phân chia lợi nhuận), 配分 (phân bổ ngân sách)."
        },
        {
            "id": "d06-q09", "number": 9, "section": "問題2: 文脈規定",
            "instruction": "（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "開発を断念するのも、（　）な選択と言えるのではないだろうか。",
            "options": ["賢明", "発明", "利発", "知的"], "answer": 0,
            "explanation": "【正解】1 (賢明)\n\n• 賢明（けんめい）：Sáng suốt, khôn ngoan (賢明な選択: lựa chọn sáng suốt).\n• 利発 (thông minh lanh lợi - dùng cho trẻ con), 知的 (mang tính trí tuệ)."
        },
        {
            "id": "d06-q10", "number": 10, "section": "問題2: 文脈規定",
            "instruction": "（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "A社の会長はうちの社長と同（　）だそうだ。",
            "options": ["老年", "年寄り", "年配", "老人"], "answer": 2,
            "explanation": "【正解】3 (年配)\n\n• 同年配（どうねんぱい）：Cùng trang lứa, trạc tuổi nhau."
        },
        {
            "id": "d06-q11", "number": 11, "section": "問題2: 文脈規定",
            "instruction": "（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "王さんは専門学校に進学して、（　）師の免許を取るつもりだ。",
            "options": ["料亭", "調理", "炊事", "調味"], "answer": 1,
            "explanation": "【正解】2 (調理)\n\n• 調理師（ちょうりし）：Đầu bếp có chứng chỉ/bằng cấp chuyên môn."
        },
        {
            "id": "d06-q12", "number": 12, "section": "問題2: 文脈規定",
            "instruction": "（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "夫婦と未婚の子どもだけで構成される家族を（　）家族と言う。",
            "options": ["単", "核", "真", "純"], "answer": 1,
            "explanation": "【正解】2 (核)\n\n• 核家族（かくかぞく）：Gia đình hạt nhân (chỉ gồm vợ chồng và con cái chưa kết hôn)."
        },
        {
            "id": "d06-q13", "number": 13, "section": "問題2: 文脈規定",
            "instruction": "（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "世間（　）を気にし過ぎると、思い切ったことができない時もある。",
            "options": ["面", "風", "性", "体"], "answer": 3,
            "explanation": "【正解】4 (体)\n\n• 世間体（せけんてい）：Miệng lưỡi thế gian, thể diện/sĩ diện trước xã hội."
        },

        # 問題3：言い換え類義
        {
            "id": "d06-q14", "number": 14, "section": "問題3: 言い換え類義",
            "instruction": "_____の言葉に意味が最も近いものを、1・2・3・4から一つ選びなさい。",
            "question": "風邪を軽く見ないほうがいい。腹痛を伴うなら<u>なおさら</u>気をつけるべきだ。",
            "options": ["とにかく", "さらに", "かならず", "いよいよ"], "answer": 1,
            "explanation": "【正解】2 (さらに)\n\n• なおさら（尚更）：Càng, hơn nữa (= さらに, いっそう)."
        },
        {
            "id": "d06-q15", "number": 15, "section": "問題3: 言い換え類義",
            "instruction": "_____の言葉に意味が最も近いものを、1・2・3・4から一つ選びなさい。",
            "question": "奈良県の吉野は桜で<u>名高い</u>ところだ。",
            "options": ["偉大な", "豊かな", "立派な", "有名な"], "answer": 3,
            "explanation": "【正解】4 (有名な)\n\n• 名高い（なだかい）：Nổi tiếng, lừng danh (= 有名な)."
        },
        {
            "id": "d06-q16", "number": 16, "section": "問題3: 言い換え類義",
            "instruction": "_____の言葉に意味が最も近いものを、1・2・3・4から一つ選びなさい。",
            "question": "彼は子どもの頃から化石集めに<u>凝って</u>、今や一大コレクションになった。",
            "options": ["ふけって", "ほどこして", "よって", "つくって"], "answer": 0,
            "explanation": "【正解】1 (ふけって)\n\n• 凝る（こる）：Say mê, đắm chìm vào sở thích (= ふける / 熱中する)."
        },
        {
            "id": "d06-q17", "number": 17, "section": "問題3: 言い換え類義",
            "instruction": "_____の言葉に意味が最も近いものを、1・2・3・4から一つ選びなさい。",
            "question": "人気商品の品切れが続き、需要と供給の<u>均衡</u>が崩れている。",
            "options": ["ステップ", "メソッド", "セット", "バランス"], "answer": 3,
            "explanation": "【正解】4 (バランス)\n\n• 均衡（きんこう）：Cân bằng (= バランス, 釣り合い)."
        },
        {
            "id": "d06-q18", "number": 18, "section": "問題3: 言い換え類義",
            "instruction": "_____の言葉に意味が最も近いものを、1・2・3・4から一つ選びなさい。",
            "question": "難病の少女を救うため、多額の<u>寄付</u>が集まった。",
            "options": ["寄与", "貸与", "授与", "贈与"], "answer": 3,
            "explanation": "【正解】4 (贈与)\n\n• 寄付（きふ）：Quyên góp, tặng cho (= 贈与: tặng/cho tài sản)."
        },
        {
            "id": "d06-q19", "number": 19, "section": "問題3: 言い換え類義",
            "instruction": "_____の言葉に意味が最も近いものを、1・2・3・4から一つ選びなさい。",
            "question": "彼は借りた金が返せず、友人に<u>気兼ねしている</u>。",
            "options": ["気を遣って遠慮している", "気持ちを隠している", "気分を害している", "正直に話している"], "answer": 0,
            "explanation": "【正解】1 (気を遣って遠慮している)\n\n• 気兼ねする（きがねする）：E dè, giữ kẽ, ngại ngùng vì sợ làm phiền người khác."
        },

        # 問題4：用法
        {
            "id": "d06-q20", "number": 20, "section": "問題4: 用法",
            "instruction": "次の言葉の使い方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "<b>ひっそり</b>",
            "options": [
                "恋人を驚かそうと思って、バラの花束をひっそり渡した。",
                "帰省していた子どもたちが東京へ戻り、家は再びひっそりしていた。",
                "ボーナスをもらったので、冬用のコートをひっそり買ってきた。",
                "一カ月の登山を無事に終え、下山してひげを剃ったらひっそりした。"
            ],
            "answer": 1,
            "explanation": "【正解】2\n\n• ひっそり：Yên ắng, tĩnh mịch (dùng cho không gian, căn nhà vắng vẻ tĩnh lặng)."
        },
        {
            "id": "d06-q21", "number": 21, "section": "問題4: 用法",
            "instruction": "次の言葉の使い方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "<b>解約</b>",
            "options": [
                "生命保険会社の積立貯蓄は、中途解約するとかなり損になる。",
                "彼女との婚約は解約することにしたが、今でも未練が残る。",
                "遺跡発掘チームは一応の成果をあげ、解約することになった。",
                "自動車の解約業者による不法投棄が社会問題になった。"
            ],
            "answer": 0,
            "explanation": "【正解】1\n\n• 解約（かいやく）：Hủy bỏ hợp đồng giao dịch/tiết kiệm tích lũy (中途解約: hủy hợp đồng giữa chừng)."
        },
        {
            "id": "d06-q22", "number": 22, "section": "問題4: 用法",
            "instruction": "次の言葉の使い方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "<b>ファスナー</b>",
            "options": [
                "缶コーヒーのファスナーが開かなくて、全然飲めない。",
                "彼の携帯に付いているファスナーはなかなか便利なようだ。",
                "旅行カバンのファスナーが壊れ、カメラが出せなくなった。",
                "リモコンのファスナーを操作して、ドラマの録画予約をした。"
            ],
            "answer": 2,
            "explanation": "【正解】3\n\n• ファスナー（fastener）：Khóa kéo (khóa kéo túi xách/áo quần)."
        },
        {
            "id": "d06-q23", "number": 23, "section": "問題4: 用法",
            "instruction": "次の言葉の使い方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "<b>さく</b>",
            "options": [
                "先生が進学相談のためにわざわざ時間をさいてくださった。",
                "会社が便宜をさいてくれ、住宅を探さなくてよくなった。",
                "キャベツをさいて皿に盛り、その上にトンカツをのせた。",
                "カレンダーをさいて時間を作ったが、急用ではなかった。"
            ],
            "answer": 0,
            "explanation": "【正解】1\n\n• 割く（さく）：Dành (thời gian, tiền bạc) cho mục đích nào đó (時間を割く)."
        },
        {
            "id": "d06-q24", "number": 24, "section": "問題4: 用法",
            "instruction": "次の言葉の使い方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "<b>まんざら</b>",
            "options": [
                "あの若者は働きもせずにまんざらな生活を送っている。",
                "70歳を過ぎた母は、ウォーキングで足腰をまんざら鍛えている。",
                "祭りのはやしが聞こえてきても、まんざら気分が高まってこない。",
                "監督が若手俳優を起用するという噂はまんざら嘘でもないらしい。"
            ],
            "answer": 3,
            "explanation": "【正解】4\n\n• まんざら～ない：Không hẳn là... hoàn toàn (まんざら嘘でもない: không hẳn là hoàn toàn bịa đặt vô căn cứ)."
        },
        {
            "id": "d06-q25", "number": 25, "section": "問題4: 用法",
            "instruction": "次の言葉の使い方として最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "<b>形見</b>",
            "options": [
                "母の形見である着物は、さすがに袖を通すことはできない。",
                "本の形見を見せてもらったが、色が気に入らなかった。",
                "このスポーツカーは1970年代の形見で、今は製造されていない。",
                "博物館に昭和の古いテレビの形見があったが、実際に映るらしい。"
            ],
            "answer": 0,
            "explanation": "【正解】1\n\n• 形見（かたみ）：Kỷ vật/di vật người đã mất để lại (母の形見)."
        },

        # 問題5：文法形式
        {
            "id": "d06-q26", "number": 26, "section": "問題5: 文法形式",
            "instruction": "次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "たとえ一国の首相（　）、賄賂を受け取れば逮捕される。",
            "options": ["をよそに", "ならでは", "ともなると", "であれ"], "answer": 3,
            "explanation": "【正解】4 (であれ)\n\n• たとえ～であれ：Dù có là... đi chăng nữa thì."
        },
        {
            "id": "d06-q27", "number": 27, "section": "問題5: 文法形式",
            "instruction": "次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "中東の原油輸出がストップした（　）、日本経済は大混乱に陥る。",
            "options": ["だけに", "あまり", "ものの", "が最後"], "answer": 3,
            "explanation": "【正解】4 (が最後)\n\n• ～たが最後：Một khi đã... thì (chắc chắn sẽ dẫn tới thảm họa/hậu quả tồi tệ)."
        },
        {
            "id": "d06-q28", "number": 28, "section": "問題5: 文法形式",
            "instruction": "次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "軍事基地を分析するには、衛星画像を利用（　）だろう。",
            "options": ["したものだ", "したてだ", "したらいい", "したところだ"], "answer": 2,
            "explanation": "【正解】3 (したらいい)\n\n• ～たらいいだろう：Nên làm... thì tốt hơn hết (đưa ra giải pháp/gợi ý thích hợp)."
        },
        {
            "id": "d06-q29", "number": 29, "section": "問題5: 文法形式",
            "instruction": "次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "1853年浦賀に来航したペリーは、歴史的使命（　）開国を迫った。",
            "options": ["といえば", "とばかりに", "ときたら", "ともなく"], "answer": 1,
            "explanation": "【正解】2 (とばかりに)\n\n• ～とばかりに：Như thể muốn nói rằng/coi như là (thể hiện thái độ rõ ràng qua hành động)."
        },
        {
            "id": "d06-q30", "number": 30, "section": "問題5: 文法形式",
            "instruction": "次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "鬼才芥川龍之介でも、もはや生き（　）ほど心身は傷ついていた。",
            "options": ["ていられない", "ずにはおかない", "かねない", "たところ"], "answer": 0,
            "explanation": "【正解】1 (ていられない)\n\n• ～ていられない：Không thể nào tiếp tục... nổi (生きていられないほど: kiệt quệ đến mức không thể sống nổi)."
        },
        {
            "id": "d06-q31", "number": 31, "section": "問題5: 文法形式",
            "instruction": "次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "まだ入団したばかりの新人の（　）、台詞を間違えるのは仕方がない。",
            "options": ["わりに", "のみならず", "ものとして", "こととて"], "answer": 3,
            "explanation": "【正解】4 (こととて)\n\n• ～こととて：Vì lý do là... nên mong thông cảm (văn phong trang trọng)."
        },
        {
            "id": "d06-q32", "number": 32, "section": "問題5: 文法形式",
            "instruction": "次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "有名な絵を真似するなど、画家としてある（　）行為だ。",
            "options": ["べき", "ごとき", "まじき", "かぎり"], "answer": 2,
            "explanation": "【正解】3 (まじき)\n\n• あるまじき：Không thể chấp nhận đối với tư cách một... (画家としてあるまじき行為)."
        },
        {
            "id": "d06-q33", "number": 33, "section": "問題5: 文法形式",
            "instruction": "次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "(店頭で)\nA「店内が混雑した場合は（　）ありますので、ご了承ください。」\nB「わかったから、早く開けたらどうだ。」",
            "options": [
                "お待ちしていただくことが",
                "お待ちされていただくことが",
                "お待ち申していただくことが",
                "お待ちいただくことが"
            ],
            "answer": 3,
            "explanation": "【正解】4 (お待ちいただくことが)\n\n• お待ちいただく：Kính ngữ lịch sự chuẩn xác đối với khách hàng (mong quý khách thông cảm việc phải chờ đợi)."
        },
        {
            "id": "d06-q34", "number": 34, "section": "問題5: 文法形式",
            "instruction": "次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "文芸映画の上映が始まる（　）、隣席の男は居眠りし出した。",
            "options": ["ばかりに", "なり", "ときたら", "どころか"], "answer": 1,
            "explanation": "【正解】2 (なり)\n\n• ～なり：Vừa mới... xong là ngay lập tức làm hành động khác."
        },
        {
            "id": "d06-q35", "number": 35, "section": "問題5: 文法形式",
            "instruction": "次の文の（　）に入れるのに最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "(駅の改札で)\nA「おい、（　）じゃないぞ。走らんと次の電車に間に合わん。」\nB「大丈夫だって。地震でダイヤが乱れてるから。」",
            "options": [
                "のんびりしているくらい",
                "のんびりしているばあい",
                "のんびりしているほど",
                "のんびりしているわけ"
            ],
            "answer": 1,
            "explanation": "【正解】2 (のんびりしているばあい)\n\n• ～ている場合じゃない：Đây không phải là lúc thong thả nhởn nhơ đâu."
        },

        # 問題6：文の組み立て
        {
            "id": "d06-q36", "number": 36, "section": "問題6: 文の組み立て",
            "instruction": "次の文の ★ に入る最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "彼は複数の ＿＿ ＿＿ ★ ＿＿ に熱中している。",
            "options": ["オンラインゲーム", "ユーザーが", "行う", "参加して"], "answer": 2,
            "explanation": "【正解】3 (行う)\n\n• Thứ tự ghép câu: ユーザーが(2) 参加して(4) ★行う(3) オンラインゲーム(1)\n• Câu hoàn chỉnh: 彼は複数の「ユーザーが参加して行うオンラインゲーム」に熱中している。"
        },
        {
            "id": "d06-q37", "number": 37, "section": "問題6: 文の組み立て",
            "instruction": "次の文の ★ に入る最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "探査機・ボイジャー ＿＿ ＿＿ ＿＿ ★ が相次いだ。",
            "options": ["惑星", "によって", "貴重な発見", "に関する"], "answer": 2,
            "explanation": "【正解】3 (貴重な発見)\n\n• Thứ tự ghép câu: 探査機・ボイジャーによって(2) 惑星(1) に関する(4) ★貴重な発見(3) が相次いだ。"
        },
        {
            "id": "d06-q38", "number": 38, "section": "問題6: 文の組み立て",
            "instruction": "次の文の ★ に入る最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "人体が ＿＿ ＿＿ ★ ＿＿ が起きる。",
            "options": ["染色体などに", "浴びると", "様々な障害", "放射線を"], "answer": 0,
            "explanation": "【正解】1 (染色体などに)\n\n• Thứ tự ghép câu: 人体が放射線を(4) 浴びると(2) ★染色体などに(1) 様々な障害(3) が起きる。"
        },
        {
            "id": "d06-q39", "number": 39, "section": "問題6: 文の組み立て",
            "instruction": "次の文の ★ に入る最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "遠く離れた自分の巣に ＿＿ ＿＿ ★ ＿＿ は不思議だ。",
            "options": ["戻ってくる", "能力", "正しく", "動物の"], "answer": 3,
            "explanation": "【正解】4 (動物の)\n\n• Thứ tự ghép câu: 遠く離れた自分の巣に正しく(3) 戻ってくる(1) ★動物の(4) 能力(2) は不思議だ。"
        },
        {
            "id": "d06-q40", "number": 40, "section": "問題6: 文の組み立て",
            "instruction": "次の文の ★ に入る最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "アンドロイドは ＿＿ ★ ＿＿ ＿＿ している。",
            "options": ["人間そっくりの", "万博にも", "外観をもち", "出展されたり"], "answer": 1,
            "explanation": "【正解】2 (万博にも)\n\n• Thứ tự ghép câu: アンドロイドは人間そっくりの(1) ★外観をもち(3) / 万博にも(2) 出展されたり(4) している。"
        },

        # 問題7：文章の文法
        {
            "id": "d06-q41", "number": 41, "section": "問題7: 文章の文法",
            "instruction": "次の文章を読んで、文章全体の趣旨を踏まえて、41から45の中に入る最もよいものを、1・2・3・4から一つ選びなさい。",
            "passage": "インドネシアとフィリピンから来日した介護福祉士の研修生36人がこの春、国家試験に初めて合格し、各地で新たなスタートを切った。人手不足の介護施設で、どんな役割を果たせるのか。外国人の受け入れを【 41 】ための課題は――。\n\n岐阜市の特別養護老人ホーム「サンライフ彦坂」。この春介護福祉士になったアスリ・フジアンティ・サエランさん(26)は、体が不自由な杉本はつえさん(82)を手際よくベッドから車いすに移し、食堂へ連れて行った。「手の力、ついてきたやろ」。アスリさんの手をぎゅっと握る杉本さん。アスリさんもなめらかな日本語で応じた。「ほんまやね。私の指、痛いくらい。がんばってリハビリしましょうね」\n\n現場では「外国人」に戸惑う利用者への接し方に悩む【 42 】。体を触ろうとすると顔を【 43-a 】、方言を何度も聞き直して【 43-b 】。粘り強く相手の趣味などを調べて話題にし、方言をノートに書いて覚え、今では冗談を言い合う仲だ。アスリさんが担当した認知症女性の夫、井上永一さん(80)は「初めは岐阜弁が通じるか不安やったが、食事やトイレの介助は日本人と大差なく、安心して【 44 】。高齢者が増えて日本人だけではやっていけないご時世ですから」と話す。\n\n一人前になるにはこれからが正念場だ。合格後は見習いではなくなり、責任も重くなる。6月に始めた夜勤では、呼吸や顔色などにきめ細かく目配りし、緊急事態にも対応できる幅広い専門的な判断が求められる。「申し送り用の介護記録【 45-a 】、口頭で報告【 45-b 】ことが必要」(介護副主任)という。",
            "question": "【 41 】に入る最もよいものを選びなさい。",
            "options": ["定着できる", "定着される", "定着させる", "定着させられる"], "answer": 2,
            "explanation": "【正解】3 (定着させる)\n\n• 外国人の受け入れを定着させる: làm cho việc tiếp nhận lao động nước ngoài đi vào ổn định/bền vững (tha động từ sai khiến 「定着させる」)."
        },
        {
            "id": "d06-q42", "number": 42, "section": "問題7: 文章の文法",
            "instruction": "次の文章を読んで、文章全体の趣旨を踏まえて、41から45の中に入る最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "【 42 】に入る最もよいものを選びなさい。",
            "options": ["ことにした", "ことであった", "こともあった", "ことにしていた"], "answer": 2,
            "explanation": "【正解】3 (こともあった)\n\n• 悩むこともあった: cũng từng có những lúc phiền lòng, bối rối trong quá khứ."
        },
        {
            "id": "d06-q43", "number": 43, "section": "問題7: 文章の文法",
            "instruction": "次の文章を読んで、文章全体の趣旨を踏まえて、41から45の中に入る最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "【 43 】の a と b に入る組み合わせとして最もよいものを選びなさい。",
            "options": [
                "a: そむいたり / b: 怒ったり",
                "a: そむかせたり / b: 怒られたり",
                "a: そむけたり / b: 怒ったり",
                "a: そむけられたり / b: 怒られたり"
            ],
            "answer": 3,
            "explanation": "【正解】4 (a: そむけられたり / b: 怒られたり)\n\n• Bị bệnh nhân ngoảnh mặt đi (顔をそむけられたり) và bị mắng vì nghe không kịp tiếng địa phương (怒られたり)."
        },
        {
            "id": "d06-q44", "number": 44, "section": "問題7: 文章の文法",
            "instruction": "次の文章を読んで、文章全体の趣旨を踏まえて、41から45の中に入る最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "【 44 】に入る最もよいものを選びなさい。",
            "options": [
                "世話してもらえる",
                "世話してあげられる",
                "世話になってくれる",
                "世話になってもらう"
            ],
            "answer": 0,
            "explanation": "【正解】1 (世話してもらえる)\n\n• 安心して世話してもらえる: yên tâm để cho bạn ấy chăm sóc, giúp đỡ người thân của mình."
        },
        {
            "id": "d06-q45", "number": 45, "section": "問題7: 文章の文法",
            "instruction": "次の文章を読んで、文章全体の趣旨を踏まえて、41から45の中に入る最もよいものを、1・2・3・4から一つ選びなさい。",
            "question": "【 45 】の a と b に入る組み合わせとして最もよいものを選びなさい。",
            "options": [
                "a: につけ / b: できるようにする",
                "a: をつけ / b: できるようになる",
                "a: につけ / b: できるようにみる",
                "a: をつけ / b: できるようにとる"
            ],
            "answer": 1,
            "explanation": "【正解】2 (a: をつけ / b: できるようになる)\n\n• 申し送り用の介護記録をつけ (ghi chép nhật ký bàn giao ca chăm sóc)、口頭で報告できるようになる (có thể báo cáo trực tiếp bằng lời nói)."
        }
    ]
}

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    n1_dir = os.path.join(data_dir, 'n1_20days')

    os.makedirs(n1_dir, exist_ok=True)

    # 1. Write Day 6
    day06_json = json.dumps(DAY06, ensure_ascii=False, indent=2)
    with open(os.path.join(data_dir, 'day06.json'), 'w', encoding='utf-8') as f:
        f.write(day06_json)
    with open(os.path.join(n1_dir, 'day06.json'), 'w', encoding='utf-8') as f:
        f.write(day06_json)
    print("Day 6 successfully written (45 questions).")

    # 2. Standardize Day 7
    day07_path = os.path.join(data_dir, 'day07.json')
    if os.path.exists(day07_path):
        with open(day07_path, 'r', encoding='utf-8-sig') as f:
            d7_raw = json.load(f)
        
        # Flatten sections into questions array if not present
        if 'questions' not in d7_raw or len(d7_raw['questions']) == 0:
            flat_qs = []
            num = 1
            for sec in d7_raw.get('sections', []):
                sec_name = sec.get('sectionName', '')
                sec_inst = sec.get('instruction', '')
                for q in sec.get('questions', []):
                    # convert answer from 1-based (1..4) to 0-based (0..3) if needed
                    ans = q.get('answer', 1)
                    if isinstance(ans, int) and ans >= 1 and ans <= 4:
                        ans_idx = ans - 1
                    else:
                        ans_idx = ans
                    
                    flat_qs.append({
                        "id": q.get('id', f'd07-q{str(num).zfill(2)}'),
                        "number": num,
                        "section": sec_name,
                        "instruction": sec_inst,
                        "passage": q.get('passage', sec.get('passage', '')),
                        "question": q.get('question', ''),
                        "targetWord": q.get('targetWord', ''),
                        "options": q.get('options', []),
                        "answer": ans_idx,
                        "explanation": q.get('explanation', f"【正解】{ans} ({q.get('options', [''])[ans_idx] if ans_idx < len(q.get('options', [])) else ''})")
                    })
                    num += 1
            d7_raw['questions'] = flat_qs
        
        d7_raw['proverb'] = d7_raw.get('proverb', '七不思議（ななふしぎ）: Seven wonders')
        d7_raw['totalQuestions'] = len(d7_raw['questions'])
        day07_json = json.dumps(d7_raw, ensure_ascii=False, indent=2)
        with open(day07_path, 'w', encoding='utf-8') as f:
            f.write(day07_json)
        with open(os.path.join(n1_dir, 'day07.json'), 'w', encoding='utf-8') as f:
            f.write(day07_json)
        print(f"Day 7 successfully standardized ({len(d7_raw['questions'])} questions).")

    # 3. Standardize Day 8
    day08_path = os.path.join(data_dir, 'day08.json')
    if os.path.exists(day08_path):
        with open(day08_path, 'r', encoding='utf-8-sig') as f:
            d8_raw = json.load(f)
        
        if 'questions' not in d8_raw or len(d8_raw['questions']) == 0:
            flat_qs = []
            num = 1
            for sec in d8_raw.get('sections', []):
                sec_name = sec.get('sectionName', '')
                sec_inst = sec.get('instruction', '')
                for q in sec.get('questions', []):
                    ans = q.get('answer', 1)
                    if isinstance(ans, int) and ans >= 1 and ans <= 4:
                        ans_idx = ans - 1
                    else:
                        ans_idx = ans
                    
                    flat_qs.append({
                        "id": q.get('id', f'd08-q{str(num).zfill(2)}'),
                        "number": num,
                        "section": sec_name,
                        "instruction": sec_inst,
                        "passage": q.get('passage', sec.get('passage', '')),
                        "question": q.get('question', ''),
                        "targetWord": q.get('targetWord', ''),
                        "options": q.get('options', []),
                        "answer": ans_idx,
                        "explanation": q.get('explanation', f"【正解】{ans} ({q.get('options', [''])[ans_idx] if ans_idx < len(q.get('options', [])) else ''})")
                    })
                    num += 1
            d8_raw['questions'] = flat_qs
        
        d8_raw['proverb'] = d8_raw.get('proverb', '八面六臂（はちめんろっぴ）: superhuman versatility')
        d8_raw['totalQuestions'] = len(d8_raw['questions'])
        day08_json = json.dumps(d8_raw, ensure_ascii=False, indent=2)
        with open(day08_path, 'w', encoding='utf-8') as f:
            f.write(day08_json)
        with open(os.path.join(n1_dir, 'day08.json'), 'w', encoding='utf-8') as f:
            f.write(day08_json)
        print(f"Day 8 successfully standardized ({len(d8_raw['questions'])} questions).")

    # 4. Update days-index.json
    days_index_path = os.path.join(data_dir, 'days-index.json')
    if os.path.exists(days_index_path):
        with open(days_index_path, 'r', encoding='utf-8-sig') as f:
            index_list = json.load(f)
        
        for item in index_list:
            if item.get('day') == 6:
                item['available'] = True
                item['questionsCount'] = 45
                item['file'] = 'data/day06.json'
                item['title'] = '第6日'
                item['theme'] = '類義語・用法特訓 2'
            elif item.get('day') == 7:
                item['available'] = True
                item['questionsCount'] = 45
                item['file'] = 'data/day07.json'
                item['title'] = '第7日'
                item['theme'] = '第1週 総復習テスト'
            elif item.get('day') == 8:
                item['available'] = True
                item['questionsCount'] = 45
                item['file'] = 'data/day08.json'
                item['title'] = '第8日'
        
        with open(days_index_path, 'w', encoding='utf-8') as f:
            json.dump(index_list, f, ensure_ascii=False, indent=2)
        print("days-index.json successfully updated.")

if __name__ == '__main__':
    main()
