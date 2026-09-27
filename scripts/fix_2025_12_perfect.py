# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILE = os.path.join(ROOT_DIR, 'data', 'n2_exams', '2025_12.json')
ALT_FILE = os.path.join(ROOT_DIR, 'data', 'n2_exams', 'n2_2025_12.json')
PUB_TARGET_FILE = os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams', '2025_12.json')
PUB_ALT_FILE = os.path.join(ROOT_DIR, 'public', 'data', 'n2_exams', 'n2_2025_12.json')

with open(TARGET_FILE, 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

# 1. Precise fixes for Vocab & Grammar (Q1 - Q47)
vocab_grammar_fixes = {
    1: {
        "question": "この家の<u>柱</u>はしっかりしている。",
        "options": ["はしら", "ゆか", "かべ", "たな"],
        "answer": 0,
        "explanation": "【正解】1 (はしら)\n\n• 柱（はしら）：Cột, trụ nhà.\n• 床（ゆか）：Sàn nhà.\n• 壁（かべ）：Bức tường.\n• 棚（たな）：Cái kệ, giá sách."
    },
    2: {
        "question": "なかなか<u>討論</u>が終わらない。",
        "options": ["どうろん", "ぎろん", "とうろん", "きろん"],
        "answer": 2,
        "explanation": "【正解】3 (とうろん)\n\n• 討論（とうろん）：Thảo luận, tranh luận.\n• 議論（ぎろん）：Nghị luận."
    },
    3: {
        "question": "家具の色は白で<u>統一</u>した。",
        "options": ["とういつ", "とういち", "どういつ", "どういち"],
        "answer": 0,
        "explanation": "【正解】1 (とういつ)\n\n• 統一（とういつ）：Thống nhất, đồng bộ."
    },
    4: {
        "question": "彼はいつも誰かと<u>争って</u>いる。",
        "options": ["たたかって", "あらそって", "きそって", "ぶつかって"],
        "answer": 1,
        "explanation": "【正解】2 (あらそって)\n\n• 争う（あらそう）：Tranh chấp, cãi cọ, tranh giành.\n• 戦う（たたかう）：Chiến đấu.\n• 競う（きそう）：Cạnh tranh ganh đua."
    },
    5: {
        "question": "この野菜はビタミンが<u>豊富</u>です。",
        "options": ["ほんふう", "ほんふ", "ほうふう", "ほうふ"],
        "answer": 3,
        "explanation": "【正解】4 (ほうふ)\n\n• 豊富（ほうふ）：Phong phú, dồi dào."
    },
    6: {
        "question": "「デジタルカメラ」を<u>りゃくして</u>「デジカメ」という。",
        "options": ["縮して", "省して", "略して", "簡して"],
        "answer": 2,
        "explanation": "【正解】3 (略して)\n\n• 略する（りゃくする）：Viết tắt, lược bỏ."
    },
    7: {
        "question": "暑いので、日陰で<u>すずんだ</u>。",
        "options": ["快んだ", "冷んだ", "清んだ", "涼んだ"],
        "answer": 3,
        "explanation": "【正解】4 (涼んだ)\n\n• 涼む（すずむ）：Hóng mát."
    },
    8: {
        "question": "来年からサービスを<u>かくじゅう</u>することになった。",
        "options": ["拡張", "拡充", "各充", "各張"],
        "answer": 1,
        "explanation": "【正解】2 (拡充)\n\n• 拡充（かくじゅう）：Mở rộng và tăng cường (quy mô, dịch vụ, trang thiết bị)."
    },
    9: {
        "question": "私はあの人たちに<u>すくわれました</u>。",
        "options": ["嫌われました", "敬われました", "疑われました", "救われました"],
        "answer": 3,
        "explanation": "【正解】4 (救われました)\n\n• 救う（すくう）：Cứu giúp, giải cứu."
    },
    10: {
        "question": "犯人はすでに国外に逃亡した可能性が<u>のうこう</u>だ。",
        "options": ["濃厚", "農厚", "濃高", "農高"],
        "answer": 0,
        "explanation": "【正解】1 (濃厚)\n\n• 濃厚（のうこう）：Đậm đặc; (khả năng) rất cao, rõ rệt."
    },
    11: {
        "question": "9時（   ）の新幹線に乗るために、8時に家を出た。",
        "options": ["行", "発", "進", "始"],
        "answer": 1,
        "explanation": "【正解】2 (発)\n\n• 9時発（くじはつ）：Khởi hành lúc 9 giờ."
    },
    12: {
        "question": "コンサートのチケットは、先着（   ）で買うことができます。",
        "options": ["列", "番", "序", "順"],
        "answer": 3,
        "explanation": "【正解】4 (順)\n\n• 先着順（せんちゃくじゅん）：Thứ tự ai đến trước được phục vụ trước (First-come, first-served)."
    },
    13: {
        "question": "（   ）予約の場合は、キャンセル料がかかりません。",
        "options": ["単", "副", "仮", "中"],
        "answer": 2,
        "explanation": "【正解】3 (仮)\n\n• 仮予約（かりよやく）：Đặt chỗ tạm thời."
    },
    14: {
        "question": "風邪の（   ）のために、栄養と睡眠を十分に取りましょう。",
        "options": ["自衛", "予備", "予防", "守衛"],
        "answer": 2,
        "explanation": "【正解】3 (予防)\n\n• 風邪の予防（よぼう）：Phòng ngừa cảm cúm."
    },
    15: {
        "question": "昨日のコンサートでは（   ）に近い席に座れたので、演奏者の様子が良く見えた。",
        "options": ["ホール", "ステージ", "スペース", "マーケット"],
        "answer": 1,
        "explanation": "【正解】2 (ステージ)\n\n• ステージ（Stage）：Sân khấu."
    },
    16: {
        "question": "来週の発表内容を（   ）して、大事なところだけ短くまとめて話してください。",
        "options": ["要約", "節約", "減量", "縮小"],
        "answer": 0,
        "explanation": "【正解】1 (要約)\n\n• 要約（ようやく）：Tóm tắt, cô đọng nội dung chính."
    },
    17: {
        "question": "フライパンの油が回りに（   ）、キッチンが汚れた。",
        "options": ["飛び散って", "飛び立って", "飛び越えて", "飛び上がって"],
        "answer": 0,
        "explanation": "【正解】1 (飛び散って)\n\n• 飛び散る（とびちる）：Bắn tung tóe, văng ra xung quanh."
    },
    18: {
        "question": "私の娘は音に（   ）で、小さな音でも目を覚ましてしまう。",
        "options": ["詳細", "器用", "敏感", "短気"],
        "answer": 2,
        "explanation": "【正解】3 (敏感)\n\n• 敏感（びんかん）：Nhạy cảm (音に敏感: nhạy cảm với âm thanh)."
    },
    19: {
        "question": "ユーキ教授の主張が正しいことを（   ）貴重な資料が見つかった。",
        "options": ["近づける", "取り上げる", "持ち上げる", "裏づける"],
        "answer": 3,
        "explanation": "【正解】4 (裏づける)\n\n• 裏づける（うらづける）：Chứng minh, xác thực, làm cơ sở chứng minh."
    },
    20: {
        "question": "今日は仕事で一日中歩き回ったので、（   ）疲れた。",
        "options": ["かさかさに", "くたくたに", "ぶくぶくに", "ふさふさに"],
        "answer": 1,
        "explanation": "【正解】2 (くたくたに)\n\n• くたくた：Mệt lử, kiệt sức."
    },
    21: {
        "question": "二人の意見は<u>一致して</u>いた。",
        "options": ["正しかった", "同じだった", "はっきりしていた", "似ていた"],
        "answer": 1,
        "explanation": "【正解】2 (同じだった)\n\n• 一致する（いっちする）＝ 同じ（おなじ）：Trùng khớp, giống nhau."
    },
    22: {
        "question": "この作品の<u>題</u>はとても印象的だ。",
        "options": ["デザイン", "アイデア", "ストーリー", "タイトル"],
        "answer": 3,
        "explanation": "【正解】4 (タイトル)\n\n• 題（だい）＝ タイトル（Title）：Nhan đề, tiêu đề tác phẩm."
    },
    23: {
        "question": "この辺りはいつも<u>そうぞうしい</u>。",
        "options": ["暗い", "静かだ", "明るい", "うるさい"],
        "answer": 3,
        "explanation": "【正解】4 (うるさい)\n\n• 騒々しい（そうぞうしい）＝ うるさい：Ồn ào, huyên náo."
    },
    24: {
        "question": "私はいつもより<u>用心した</u>。",
        "options": ["注意", "努力", "準備", "集中"],
        "answer": 0,
        "explanation": "【正解】1 (注意)\n\n• 用心する（ようじんする）＝ 注意する（ちゅういする）：Cẩn trọng, đề phòng, chú ý."
    },
    25: {
        "question": "このシャツは私には<u>ぶかぶか</u>だ。",
        "options": ["派手すぎる", "小さすぎる", "大きすぎる", "地味すぎる"],
        "answer": 2,
        "explanation": "【正解】3 (大きすぎる)\n\n• ぶかぶか ＝ 大きすぎる：Rộng thùng thình (quần áo, giày dép)."
    },
    26: {
        "question": "【休憩】",
        "options": [
            "仕事の途中だったが、少し疲れたので休憩を取った。",
            "今週は日曜日に仕事がありますが、月曜日は休憩です。",
            "夏の休憩を使って、家族と海外旅行に行きました。",
            "手術のため、病院で 1 週間、休憩をすることになった。"
        ],
        "answer": 0,
        "explanation": "【正解】1 (仕事の途中だったが、少し疲れたので休憩を取った。)\n\n• 休憩（きゅうけい）：Nghỉ ngơi ngắn giữa giờ làm việc/học tập.\n• Câu 2 dùng 休み, câu 3 dùng 休暇/休み, câu 4 dùng 入院/療養."
    },
    27: {
        "question": "【進める】",
        "options": [
            "一度試合に勝って自信を進めれば、チームの成績は必ずよくなるだろう。",
            "朝にトレーニングを行うことで、运动の効果を進めることができるそうです。",
            "市では現在、防災対策として、道路整備の検討を進めています。",
            "ユーキさんが仕事で同じ失敗を繰り返すのは、その失敗の反省を進めていないからだ。"
        ],
        "answer": 2,
        "explanation": "【正解】3 (市では現在、防災対策として、道路整備の検討を進めています。)\n\n• 進める（すすめる）：Tiến hành, xúc tiến (検討・計画を進める: xúc tiến xem xét/kế hoạch).\n• Câu 1 dùng 深める/つければ, câu 2 dùng 高める, câu 4 dùng して."
    },
    28: {
        "question": "【貢献】",
        "options": [
            "高校時代の先生の一言が、私の人生に大きく貢献した。",
            "この薬は、痛みを抑えるのに大きく貢献するのでよく売れるらしい。",
            "鈴木氏が長い間行ってきた活動は、地域の安全に大きく貢献した。",
            "海外での経験が就職に大きく貢献し、希望の会社に入社できた。"
        ],
        "answer": 2,
        "explanation": "【正解】3 (鈴木氏が長い間行ってきた活動は、地域の安全に大きく貢献した。)\n\n• 貢献（こうけん）：Cống hiến, đóng góp to lớn cho xã hội, cộng đồng, lĩnh vực chung (地域の安全に貢献する).\n• Câu 1 dùng 影響を与えた, câu 2 dùng 効果的, câu 4 dùng 役立って."
    },
    29: {
        "question": "【早急】",
        "options": [
            "原さんは素質があるので、早急に強くなって、試合にも勝てるだろう。",
            "薬がよく効いたようで、痛みは早急に治まった。",
            "二つの液体を混ぜると、早急に反応して気体が発生する。",
            "この問題については早急に対策を検討する必要がある。"
        ],
        "answer": 3,
        "explanation": "【正解】4 (この問題については早急に対策を検討する必要がある。)\n\n• 早急（さっきゅう／そうきゅう）：Khẩn cấp, ngay lập tức (早急に対応・検討する: cần khẩn cấp xử lý/xem xét).\n• Câu 1 dùng 早く, câu 2 dùng すぐに, câu 3 dùng 急激に."
    },
    30: {
        "question": "【区切り】",
        "options": [
            "雨が降っている間、区切りがついていた試合が、やっと再開された。",
            "この仕事は今日中には終わりそうもないので、区切りをつけて帰ります。",
            "今が成功か失敗かの区切りなので、諦めずに頑張りましょう。",
            "次のバスまで区切りが 2 時間あるので、食事をしながら待つことにした。"
        ],
        "answer": 1,
        "explanation": "【正解】2 (この仕事は今日中には終わりそうもないので、区切りをつけて帰ります。)\n\n• 区切りをつける（くぎりをつける）：Tạm dừng ở một mốc/giai đoạn hợp lý để chuyển việc khác.\n• Câu 1 dùng 中断, câu 3 dùng 分かれ目/境目, câu 4 dùng 間隔/待ち時間."
    },
    31: {
        "question": "今朝は寝坊をしてしまい、（   ）抜きで大学に来た。",
        "options": ["朝食が", "朝食の", "朝食に", "朝食"],
        "answer": 3,
        "explanation": "【正解】4 (朝食)\n\n• N 抜きで（ぬきで）：Bỏ qua N, không có N (朝食抜きで: bỏ bữa sáng)."
    },
    32: {
        "question": "新しいコーヒーカップを使い始めて（   ）たたないうちに、床に落として割ってしまった。",
        "options": ["まだ", "まもなく", "いくらも", "いつのまにか"],
        "answer": 2,
        "explanation": "【正解】3 (いくらも)\n\n• いくらも〜ない：Chẳng được bao lâu, chẳng bao nhiêu (使い始めていくらもたたないうちに: dùng chưa được bao lâu thì...)."
    },
    33: {
        "question": "（鉄道会社のホームページで）\n「一日乗車券」は、ご購入いただいた当日（   ）、何度でも自由に乗り降りができる乗車券です。",
        "options": ["につれ", "に際し", "にわたり", "に限り"],
        "answer": 3,
        "explanation": "【正解】4 (に限り)\n\n• 〜に限り（にかぎり）：Chỉ giới hạn riêng trong... (当日限りに: chỉ riêng trong ngày mua)."
    },
    34: {
        "question": "苦手な同僚と同じチームで仕事をすることになってしまったが、決まった（   ）、うまく付き合っていこうと思う。",
        "options": ["からには", "わりには", "ばかりか", "どころか"],
        "answer": 0,
        "explanation": "【正解】1 (からには)\n\n• 〜からには：Một khi đã... thì phải (決まったからには: một khi đã quyết định phân công thì cố gắng hợp tác tốt)."
    },
    35: {
        "question": "A 社のおもちゃは、赤ちゃんが口に（   ）、米や小麦を原料にして作られているそうだ。",
        "options": ["入れてもよければ", "入れてもいいように", "入れることがあれば", "入れることがあるように"],
        "answer": 1,
        "explanation": "【正解】2 (入れてもいいように)\n\n• 〜てもいいように：Để phòng khi / cho dù có làm gì thì vẫn an toàn, không sao (bé dù có cho vào miệng cũng không sao)."
    },
    36: {
        "question": "私は音楽大学でバイオリンを専攻しているが、卒業後は演奏家（   ）、子供たちに教えるという形でバイオリンに関わっていきたいと思っている。",
        "options": ["としてだったら", "にとってだったら", "としてではなく", "にとってではなく"],
        "answer": 2,
        "explanation": "【正解】3 (としてではなく)\n\n• 〜としてではなく：Không phải với tư cách là... mà là... (không phải dưới danh nghĩa nghệ sĩ biểu diễn mà dưới dạng dạy cho trẻ em)."
    },
    37: {
        "question": "（卓球教室で）\nA「私、卓球初めてなんです。」\nB「私も、友達と遊びで少し（   ）、習うのははじめてです。」",
        "options": ["やったことがあるだけで", "やったことがあることで", "やっていなかったことで", "やっていなかっただけで"],
        "answer": 0,
        "explanation": "【正解】1 (やったことがあるだけで)\n\n• 〜だけで：Chỉ mới... thôi (tôi cũng chỉ mới chơi vui một chút với bạn thôi, chứ học bài bản thì đây là lần đầu)."
    },
    38: {
        "question": "後輩の田中さんは仕事熱心だが、少しまじめすぎる（   ）。",
        "options": ["ことになっている", "ところがある", "がちだ", "ものだ"],
        "answer": 1,
        "explanation": "【正解】2 (ところがある)\n\n• 〜ところがある：Có điểm, có phần... (tính cách có điểm hơi quá nghiêm túc)."
    },
    39: {
        "question": "駅前のラーメン屋はいつも込んでいて、けっこう待たされるのに、今日はそんなに（   ）。",
        "options": ["待たずに済んだ", "待ったおかげだ", "待ちきれなかった", "待たなければよかった"],
        "answer": 0,
        "explanation": "【正解】1 (待たずに済んだ)\n\n• 〜ずに済んだ：Không phải... cũng xong (hôm nay không phải đợi nhiều mà vẫn được ăn ngay)."
    },
    40: {
        "question": "私は彼と結婚したいと思っているが、彼はきっとまだ結婚は（   ）。",
        "options": ["考えなくなってもしかたない", "考えなくなるに違いない", "考えていなくてもしかたない", "考えていないに違いない"],
        "answer": 3,
        "explanation": "【正解】4 (考えていないに違いない)\n\n• 〜に違いない：Chắc chắn là... (chắc chắn anh ấy vẫn chưa tính tới chuyện kết hôn)."
    },
    41: {
        "question": "（会議で）\n社長「新商品のコマーシャルについては、どうなっていますか。」\n課長「はい。それについては、担当の私からご報告（   ）。」",
        "options": ["なさいます", "おっしゃいます", "申し上げます", "伺います"],
        "answer": 2,
        "explanation": "【正解】3 (申し上げます)\n\n• ご報告申し上げます：Khiêm nhường ngữ (Kenjougo) kính cẩn khi báo cáo cấp trên."
    },
    42: {
        "question": "ピアノの発表会の前に、間違えそうで怖いと先生に言ったら、「ちょっとぐらい（   ）よ。大事なのは楽しんで弾くことだよ。」と言ってくれた。",
        "options": ["間違えちゃいけないんだ", "間違えたっていいんだ", "間違えなきゃいいんだ", "間違えたいんじゃないんだ"],
        "answer": 1,
        "explanation": "【正解】2 (間違えたっていいんだ)\n\n• 〜たっていい：Dù có... một chút thì cũng không sao cả."
    },
    43: {
        "question": "ちょっと ＿＿ ＿＿ ＿★＿ ＿＿ 好みの T シャツを見つけてしまい、つい買ってしまった。",
        "options": ["だけの", "つもりで", "服屋に入ったら", "見る"],
        "answer": 1,
        "explanation": "【正解】2 (つもりで)\n\n• Thứ tự đúng: 4 - 1 - 2 - 3 (見る だけの つもりで 服屋に入ったら)\n• Ý nghĩa: Chỉ định vào xem một lát thôi nhưng lại thấy chiếc áo đúng gu nên lỡ mua mất."
    },
    44: {
        "question": "兄は最近ずっと「歯が痛くて眠れない」と言っているけれど、歯医者には行こうとしない。そんなに ＿＿ ＿＿ ＿★＿ ＿＿ 。",
        "options": ["痛い", "早く行けばいい", "のに", "んだったら"],
        "answer": 1,
        "explanation": "【正解】2 (早く行けばいい)\n\n• Thứ tự đúng: 1 - 4 - 2 - 3 (痛い んだったら 早く行けばいい のに)\n• Ý nghĩa: Đau đến thế thì đi khám sớm đi cho rồi, vậy mà..."
    },
    45: {
        "question": "「ABC チーズ」はチーズ料理の専門店で、私のような ＿＿ ＿＿ ＿★＿ ＿＿ 店だ。",
        "options": ["人に", "好きでたまらないという", "チーズが", "ぜひおすすめしたい"],
        "answer": 0,
        "explanation": "【正解】1 (人に)\n\n• Thứ tự đúng: 3 - 2 - 1 - 4 (チーズが 好きでたまらないという 人に ぜひおすすめしたい)\n• Ý nghĩa: Đây là quán tôi muốn giới thiệu đến những người mê mẩn phô mai như tôi."
    },
    46: {
        "question": "親友の花子に初めて会ったとき、初対面とは思えない ＿＿ ＿＿ ＿★＿ ＿＿ 。",
        "options": ["よく覚えている", "ぐらい", "のを", "話が盛り上がった"],
        "answer": 2,
        "explanation": "【正解】3 (のを)\n\n• Thứ tự đúng: 2 - 4 - 3 - 1 (ぐらい 話が盛り上がった のを よく覚えている)\n• Ý nghĩa: Tôi vẫn nhớ như in chuyện hai đứa đã nói chuyện hào hứng đến mức không tưởng tượng nổi là mới gặp lần đầu."
    },
    47: {
        "question": "学生のころ、様々な国を旅行して、自分の ＿＿ ＿＿ ＿★＿ ＿＿ 、世界には多様な考え方があることを知った。",
        "options": ["出会えない", "交流したことで", "国にいては", "様々な文化や価値観を持つ人と"],
        "answer": 3,
        "explanation": "【正解】4 (様々な文化や価値観を持つ人と)\n\n• Thứ tự đúng: 3 - 1 - 4 - 2 (国にいては 出会えない 様々な文化や価値観を持つ人と 交流したことで)\n• Ý nghĩa: Nhờ giao lưu với những người mang nền văn hoá và giá trị quan đa dạng mà nếu chỉ ở nước mình thì không thể gặp gỡ..."
    }
}

# 2. Perfect Passage & Options for Mondai 9 (Q48 - Q51)
m9_passage = """以下は、雑話のコラムである。

目で味わう
　「目で味わう」という言葉があります。もちろん、目で食べ物を食べるという意味ではありません。食べる前に目で見て料理の見た目を楽しむという意味です。しかし、「味わう」という言葉は普通、舌で料理の味を楽しむことを指します。目でも味を感じることはできるのでしょうか。
　色使いや盛り方など、料理の見た目がきれいだと食事の楽しみが増すという人も（ 48 ）。料理人たちも、塩や酢などを使って野菜の色を鮮やかに保ったり、料理に合う色や形の器を選んだりと、見た目を大切にしています。同じ料理でも、見た目がより良いもののほうがおいしそうに感じられます。
　では、単に料理を見ておいしそうだと思うことを「味わう」と表現しているのでしょうか。（ 49 ）近年、料理の見た目が影響するのは食べる前だけではないことがわかってきました。ある研究で、食べ物の味は変えずに、色や器の種類などを変えて提供し、それぞれどんな味か評価させる実験が行われました。すると、全く同じ味のものを食べたにもかかわらず、味が異なると評価した人が多かったそうです。目から入る情報は、食べた時の味の感じ方（ 50 ）影響していたのです。このように科学的にも、実際に目で味わっているということが証明されつつあります。
　味を感じる仕組みは複雑で、見た目も大切な要素の一つです。それが感覚的に理解されていたからこそ、「目で味わう」と表現されるように（ 51 ）。"""

m9_questions = {
    48: {
        "question": "【48】に入る最も適当なものはどれか。",
        "options": ["多いとします", "多かったとします", "多いでしょう", "多かったでしょう"],
        "answer": 2,
        "explanation": "【正解】3 (多いでしょう)\n\n• Suy đoán hiện tại: Việc thức ăn bày biện đẹp mắt làm tăng hứng thú ăn uống thì ắt hẳn có nhiều người nghĩ vậy (「増すという人も多いでしょう」). 『〜でしょう』 thể hiện phỏng đoán xác đáng của tác giả."
    },
    49: {
        "question": "【49】に入る最も適当なものはどれか。",
        "options": ["実は", "確かに", "しかも", "ところが"],
        "answer": 0,
        "explanation": "【正解】1 (実は)\n\n• Liên từ 『実は』 (thực ra thì...): Tác giả đặt câu hỏi tu từ, sau đó tiết lộ một sự thật nghiên cứu mới bất ngờ: 「実は近年、料理の見た目が影響するのは食べる前だけではないことがわかってきました」."
    },
    50: {
        "question": "【50】に入る最も適当なものはどれか。",
        "options": ["にのみ", "にまで", "に限らず", "に比べて"],
        "answer": 1,
        "explanation": "【正解】2 (にまで)\n\n• Trợ từ 『にまで』 (ảnh hưởng đến tận/ngay cả...): 「目から入る情報は、食べた時の味の感じ方にまで影響していたのです」 (Thông tin mắt tiếp nhận ảnh hưởng đến tận cảm nhận vị giác lúc ăn)."
    },
    51: {
        "question": "【51】に入る最も適当なものはどれか。",
        "options": ["なったにすぎません", "なったはずがありません", "なったとはいえません", "なったのかもしれません"],
        "answer": 3,
        "explanation": "【正解】4 (なったのかもしれません)\n\n• Kết luận nhẹ nhàng: Có lẽ chính vì trực giác người xưa đã hiểu điều đó nên mới có cách diễn đạt như vậy (「『目で味わう』と表現されるようになったのかもしれません」)."
    }
}

# 3. Clean Dokkai questions (Q61, Q64, Q71)
dokkai_fixes = {
    61: {
        "question": "共通することとして筆者が述べているのはどれか。",
        "options": [
            "自分にも相手にも原因があると感じられること。",
            "自分では解決できそうにないと感じられること。",
            "相手に原因があっても、自分が悪いと感じられること。",
            "相手が変わっても解決しないと感じられること。"
        ],
        "answer": 1,
        "explanation": "【正解】2 (自分では解決できそうにないと感じられること。)\n\n• Đoạn văn nêu rõ điểm chung của những nỗi trăn trở (悩み): dường như ta không thể tự mình giải quyết được."
    },
    64: {
        "question": "150人という数について、筆者はどのように考えているか。",
        "options": [
            "共有した経験によって記憶に残り、信頼関係が築ける人の数である。",
            "人間がよりよく生きるために必要な人の数である。",
            "都市での生活で誰もが知り合うことのできる人の数である。",
            "言葉や文字を使えば記憶でき、信頼してつき合える人の数である。"
        ],
        "answer": 0,
        "explanation": "【正解】1 (共有した経験によって記憶に残り、信頼関係が築ける人の数である。)\n\n• Con số 150 người được tác giả khẳng định là số người tối đa mà con người có thể duy trì mối quan hệ tin cậy và ghi nhớ qua trải nghiệm cùng nhau."
    },
    71: {
        "question": "ユーキさんは、10 月 22 日（月）に赤木港を出発する船で、岩根島に行こうと思っている。予約のしかたとして合っているのはどれか。",
        "options": [
            "10 月 20 日（土）の 17 時 30 分までに、丸山汽船本社に電話する。",
            "10 月 20 日（土）の 17 時 30 分までに、赤木港発着所に電話する。",
            "10 月 21 日（日）の 17 時までに、丸山汽船本社に電話する。",
            "10 月 21 日（日）の 17 時までに、赤木港発着所に電話する。"
        ],
        "answer": 3,
        "explanation": "【正解】4 (10 月 21 日（日）の 17 時までに、赤木港発着所に電話する。)\n\n• Thông báo quy định: Đặt chỗ cho chuyến tàu xuất phát từ cảng Akagi cần gọi trước 17:00 ngày hôm trước (21/10) đến điểm đón trả khách cảng Akagi."
    }
}

# 4. Clean Choukai Questions (Q72 - Q101)
choukai_fixes = {
    72: {
        "question": "女の人はこの後、まず何をしますか。",
        "options": ["同意書にサインする", "エプロンを着ける", "ガラスの色を選ぶ", "かびんの送料を払う"],
        "answer": 1,
        "explanation": "【正解】2 (エプロンを着ける)\n\n• Người phụ nữ hỏi: Trước hết tôi cần làm gì? Nhân viên tiếp tân bảo: Đồng ý thư thì chị đã ký rồi, bây giờ chị hãy đeo tạp dề vào trước rồi sang bàn làm việc chọn màu thủy tinh."
    },
    73: {
        "question": "男の店員はこれからまず、何をしなければなりませんか。",
        "options": [
            "1. テーブルを拭く (Lau/dọn bàn ăn)",
            "2. サラダの準備をする (Chuẩn bị rau/salad trong bếp)",
            "3. お客さんを席に案内する (Dẫn khách vào bàn)",
            "4. 待っているお客さんにメニューを配る (Phát menu cho khách chờ)"
        ],
        "answer": 1,
        "explanation": "【正解】2 (サラダの準備をする)\n\n• Quản lý dặn nhân viên nam: Bàn ghế đã lau sạch rồi, khách bên ngoài đang đợi nhưng trước khi mở cửa đón khách thì hãy vào bếp chuẩn bị sẵn món salad chia vào từng đĩa nhỏ trước."
    },
    74: {
        "question": "女の学生はパンフレットを作るために何をしますか。",
        "options": [
            "練習中の写真をとる",
            "曲の紹介文を書く",
            "先輩に原稿をたのむ",
            "表紙のデザイン案を作る"
        ],
        "answer": 2,
        "explanation": "【正解】3 (先輩に原稿をたのむ)\n\n• Trưởng nhóm giao việc: Phần giới thiệu bản nhạc và ảnh chụp đã có người phụ trách rồi, bạn hãy nhờ các anh chị tiền bối viết bài chia sẻ cảm nghĩ để đưa vào tờ gấp."
    },
    75: {
        "question": "スタッフはまず何をしますか。",
        "options": [
            "料理の道具を運ぶ",
            "ゲームで使う道具を運ぶ",
            "ゴミ箱を運ぶ",
            "机を運ぶ"
        ],
        "answer": 0,
        "explanation": "【正解】1 (料理の道具を運ぶ)\n\n• Cán bộ trung tâm cộng đồng hướng dẫn: Bàn ghế hội trường đã xếp xong, việc đầu tiên cần làm ngay là chuyển các dụng cụ nấu nướng vào phòng bếp để chuẩn bị."
    },
    76: {
        "question": "男の人はこの後、まず何をしますか。",
        "options": [
            "資料を訂正する",
            "参加者名簿に名前を加える",
            "名札を作成する",
            "交流会をする店に連絡する"
        ],
        "answer": 0,
        "explanation": "【正解】1 (資料を訂正する)\n\n• Nam nhân viên phát hiện có thông tin nhầm lẫn trên tài liệu phát cho hội thảo, nữ đồng nghiệp bảo: Danh sách và thẻ tên tôi sẽ làm nốt, anh hãy sửa lại chỗ sai trên tài liệu trước đi."
    },
    77: {
        "question": "男の人が新しい先生に１番必要だと考えている条件は何ですか。",
        "options": [
            "長い間働けること",
            "美術大学を卒業したこと",
            "先生として教えた経験があること",
            "子どもと接するのが好きなこと"
        ],
        "answer": 2,
        "explanation": "【正解】3 (先生として教えた経験があること)\n\n• Người quản lý nhấn mạnh: Dù việc yêu quý trẻ em hay làm việc lâu dài cũng quan trọng, nhưng để lớp học hoạt động tốt ngay thì điều cốt yếu nhất là người đã có kinh nghiệm giảng dạy."
    },
    78: {
        "question": "社長は家の庭で野菜を作るようになってよかったことは何だと言っていますか。",
        "options": [
            "季節感を味わえるようになったこと",
            "子どもと過ごす時間が増えたこと",
            "スーパーで野菜を買う必要がなくなったこと",
            "体力がついたこと"
        ],
        "answer": 1,
        "explanation": "【正解】2 (子どもと過ごす時間が増えたこと)\n\n• Giám đốc chia sẻ: Từ khi cùng trồng rau ở vườn nhà, điều tuyệt vời nhất là có thêm nhiều thời gian gần gũi và trò chuyện cùng con cái."
    },
    79: {
        "question": "この選手は引退を決めた理由は何だと言っていますか。",
        "options": [
            "指導者になる機会をもらったため",
            "大学院に合格したため",
            "国際大会で満足できる成績を出せたため",
            "体力が落ちてきたため"
        ],
        "answer": 0,
        "explanation": "【正解】1 (指導者になる機会をもらったため)\n\n• Vận động viên giải thích: Không phải do thể lực suy giảm, mà vì nhận được lời mời làm huấn luyện viên chỉ đạo thế hệ trẻ nên đã quyết định giải nghệ để bước sang vai trò mới."
    },
    80: {
        "question": "女の先輩はどんな点から今の会社を選んだと言っていますか。",
        "options": [
            "給料がいいかどうか",
            "自宅での勤務が可能かどうか",
            "海外で働くチャンスがあるかどうか",
            "休みが取りやすいかどうか"
        ],
        "answer": 1,
        "explanation": "【正解】2 (自宅での勤務が可能かどうか)\n\n• Nữ tiền bối chia sẻ: Điều quyết định khi chọn công ty hiện tại là chế độ làm việc từ xa tại nhà (Telework / 在宅勤務) rất linh hoạt."
    },
    81: {
        "question": "社長はどうやって、パイナップルピザの売り上げを伸ばしたと言っていますか。",
        "options": [
            "無料のドリンクをつけたこと",
            "強い印象をあたえる広告を出したこと",
            "人気アイドルを広告に使ったこと",
            "商品の価格を一時的に下げたこと"
        ],
        "answer": 1,
        "explanation": "【正解】2 (強い印象をあたえる広告を出したこと)\n\n• Giám đốc chuỗi pizza giải thích: Bằng cách tạo chiến dịch quảng cáo gây ấn tượng mạnh mẽ, độc đáo khiến mọi người tò mò dùng thử, doanh số món pizza dứa đã tăng vọt."
    },
    82: {
        "question": "男の人は自分にとって、映画の一番の魅力は何だと言っていますか。",
        "options": [
            "共通の話題が持てること",
            "自分の気持ちを切り替えられること",
            "他人の人生を体験した気持ちになれること",
            "いろいろな知識が身につけられること"
        ],
        "answer": 3,
        "explanation": "【正解】4 (いろいろな知識が身につけられること)\n\n• Người đàn ông bày tỏ: Sức hút lớn nhất của phim ảnh đối với bản thân anh chính là học hỏi được vô số kiến thức mới về thế giới, lịch sử và văn hóa."
    },
    83: {
        "question": "男の人は何について話していますか。",
        "options": ["1", "2", "3", "4"],
        "answer": 2,
        "explanation": "【正解】3\n\n• Mondai 3 Q1: Ý chính bài nói về trải nghiệm của nhân vật."
    },
    84: {
        "question": "男の人は自分が受けた研修についてどう言っていますか。",
        "options": ["1", "2", "3", "4"],
        "answer": 3,
        "explanation": "【正解】4\n\n• Mondai 3 Q2: Đánh giá khóa đào tạo."
    },
    85: {
        "question": "ラジオで女の人が話しています。女の人は何について話していますか。",
        "options": ["1", "2", "3", "4"],
        "answer": 3,
        "explanation": "【正解】4\n\n• Mondai 3 Q3: Chương trình phát thanh giới thiệu nội dung."
    },
    86: {
        "question": "農家の男の人は何について話していますか。",
        "options": ["1", "2", "3", "4"],
        "answer": 2,
        "explanation": "【正解】3\n\n• Mondai 3 Q4: Người nông dân chia sẻ phương pháp canh tác."
    },
    87: {
        "question": "ラジオで女の人が話しています。女の人は何について話していますか。",
        "options": ["1", "2", "3", "4"],
        "answer": 1,
        "explanation": "【正解】2\n\n• Mondai 3 Q5: Nữ phát thanh viên chia sẻ mẹo vặt."
    },
    88: {
        "question": "ねえ、今日の帰り、本屋行くついでにご飯でも食べない？",
        "options": ["1", "2", "3"],
        "answer": 2,
        "explanation": "【正解】3\n\n• Mondai 4 Q1: Đáp lại lời rủ đi ăn."
    },
    89: {
        "question": "課長。こちら、春の新商品の企画書なんですが、ご覧いただけますか？",
        "options": ["1", "2", "3"],
        "answer": 2,
        "explanation": "【正解】3\n\n• Mondai 4 Q2: Kính ngữ khi trình bản kế hoạch cho trưởng phòng."
    },
    90: {
        "question": "昨日のテニスの試合、負けちゃったけど自分の力を出し切ったよ。",
        "options": ["1", "2", "3"],
        "answer": 1,
        "explanation": "【正解】2\n\n• Mondai 4 Q3: Động viên bạn sau trận đấu nỗ lực hết mình."
    },
    91: {
        "question": "木村さん、新しい企画のことで相談に乗っていただけるとありがたいんですが。",
        "options": ["1", "2", "3"],
        "answer": 1,
        "explanation": "【正解】2\n\n• Mondai 4 Q4: Nhận lời giúp đỡ thảo luận kế hoạch mới."
    },
    92: {
        "question": "週末の旅行、バスが遅れて帰りの飛行機に乗り遅れるところでしたよ。",
        "options": ["1", "2", "3"],
        "answer": 0,
        "explanation": "【正解】1\n\n• Mondai 4 Q5: Đồng cảm với sự cố suýt lỡ chuyến bay「大変でしたね」."
    },
    93: {
        "question": "林さん、担当しているゲームの開発、スケジュール通り進んでいますか？",
        "options": ["1", "2", "3"],
        "answer": 1,
        "explanation": "【正解】2\n\n• Mondai 4 Q6: Báo cáo tiến độ dự án game."
    },
    94: {
        "question": "小野さん。小野さんの卒業論文の締め切り、来週って言ってたよね。何とかなりそう？",
        "options": ["1", "2", "3"],
        "answer": 0,
        "explanation": "【正解】1\n\n• Mondai 4 Q7: Trả lời về hạn nộp luận văn tốt nghiệp."
    },
    95: {
        "question": "青木さん。新商品発表の件、午後、私は本社から戻り次第打ち合わせをしましょう。",
        "options": ["1", "2", "3"],
        "answer": 2,
        "explanation": "【正解】3\n\n• Mondai 4 Q8: Nhận lệnh họp từ cấp trên「承知しました。お待ちしております」."
    },
    96: {
        "question": "今度の市民マラソン大会、年齢を問わず参加できるそうですね。",
        "options": ["1", "2", "3"],
        "answer": 1,
        "explanation": "【正解】2\n\n• Mondai 4 Q9: Hưởng ứng thông tin giải chạy không giới hạn độ tuổi."
    },
    97: {
        "question": "会社の前にできた定食屋、値段が安いわりになかなかの味だったよ。",
        "options": ["1", "2", "3"],
        "answer": 0,
        "explanation": "【正解】1\n\n• Mondai 4 Q10: Đáp lại nhận xét về quán cơm bình dân."
    },
    98: {
        "question": "10 代がターゲットの新発売のゲーム、予想に反して各年代に受けていますね。",
        "options": ["1", "2", "3"],
        "answer": 0,
        "explanation": "【正解】1\n\n• Mondai 4 Q11: Nhận xét sự thành công ngoài mong đợi của tựa game."
    },
    99: {
        "question": "この店では何を変えることにしましたか。",
        "options": ["1", "2", "3", "4"],
        "answer": 1,
        "explanation": "【正解】2\n\n• Mondai 5 Q1: Quyết định thay đổi phương án kinh doanh của tiệm bánh mì."
    },
    100: {
        "question": "質問 1 女の人はどの自転車を買いますか。",
        "options": ["1 番の自転車", "2 番の自転車", "3 番の自転車", "4 番の自転車"],
        "answer": 2,
        "explanation": "【正解】3 (3 番の自転車)\n\n• Mondai 5 Q2-1: Người phụ nữ quyết định mua xe đạp số 3."
    },
    101: {
        "question": "質問 2 男の人はどの自転車を買いますか。",
        "options": ["1 番の自転車", "2 番の自転車", "3 番の自転車", "4 番の自転車"],
        "answer": 1,
        "explanation": "【正解】2 (2 番の自転車)\n\n• Mondai 5 Q2-2: Người đàn ông quyết định mua xe đạp số 2."
    }
}

# Apply all updates to questions
for q in exam_data['questions']:
    num = q['number']
    
    # 1. Vocab & Grammar
    if num in vocab_grammar_fixes:
        fix = vocab_grammar_fixes[num]
        q['question'] = fix['question']
        q['options'] = fix['options']
        q['answer'] = fix['answer']
        q['explanation'] = fix['explanation']
        q['passage'] = ""
        
    # 2. Mondai 9
    elif num in m9_questions:
        fix = m9_questions[num]
        q['sectionGroup'] = 'vocab_grammar'
        q['section'] = '問題9: 文章の文法'
        q['instruction'] = '次の文章を読んで、文章全体の内容を考えて、（   ）に入る最もよいものを、1・2・3・4から一つ選びなさい。'
        q['passage'] = m9_passage
        q['question'] = fix['question']
        q['options'] = fix['options']
        q['answer'] = fix['answer']
        q['explanation'] = fix['explanation']
        
    # 3. Dokkai
    elif num in dokkai_fixes:
        fix = dokkai_fixes[num]
        q['question'] = fix['question']
        q['options'] = fix['options']
        q['answer'] = fix['answer']
        q['explanation'] = fix['explanation']
        
    # 4. Choukai
    elif num in choukai_fixes:
        fix = choukai_fixes[num]
        q['question'] = fix['question']
        q['options'] = fix['options']
        q['answer'] = fix['answer']
        q['explanation'] = fix['explanation']
        q['audio'] = "data/audio/n2_2025_12.mp3"
        if num == 73:
            q['image'] = "data/images/n2_2025_12_q73.jpg"

# Re-calculate counts
v_count = sum(1 for q in exam_data['questions'] if q['sectionGroup'] == 'vocab_grammar')
r_count = sum(1 for q in exam_data['questions'] if q['sectionGroup'] == 'reading')
c_count = sum(1 for q in exam_data['questions'] if q['sectionGroup'] == 'choukai')

exam_data['totalQuestions'] = len(exam_data['questions'])
exam_data['vocabGrammarCount'] = v_count
exam_data['readingCount'] = r_count
exam_data['choukaiCount'] = c_count

print(f"Processed 2025_12: Total={exam_data['totalQuestions']}, Vocab={v_count}, Reading={r_count}, Choukai={c_count}")

# Save to all target locations
for path in [TARGET_FILE, ALT_FILE, PUB_TARGET_FILE, PUB_ALT_FILE]:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(exam_data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {path}")

print("All 2025_12 files updated successfully!")
