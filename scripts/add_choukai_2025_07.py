# -*- coding: utf-8 -*-
import json
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_file = os.path.join(base_dir, 'data', 'n2_exams', '2025_07.json')
    alt_file = os.path.join(base_dir, 'data', 'n2_exams', 'n2_2025_07.json')
    index_file = os.path.join(base_dir, 'data', 'n2-index.json')
    alt_index_file = os.path.join(base_dir, 'data', 'n2_exams', 'n2-index.json')

    with open(target_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Filter to only keep questions up to 71 first
    data['questions'] = [q for q in data['questions'] if q['number'] <= 71]

    # Audio setting
    data['audio'] = 'data/audio/n2_2025_07.mp3'

    m1_instruction = "問題1では、まず質問を聞いてください。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。"
    m2_instruction = "問題2では、まず質問を聞いてください。そのあと、問題用紙を見てください。読む時間があります。それから話を聞いて、問題用紙の1から4の中から、最もよいものを一つ選んでください。"
    m3_instruction = "問題3では、問題用紙に何も印刷されていません。この問題は、全体としてどんな内容かを聞く問題です。話の前に質問はありません。まず話を聞いてください。それから、質問と選択肢を聞いて、1から4の中から、最もよいものを一つ選んでください。"
    m4_instruction = "問題4では、問題用紙に何も印刷されていません。まず文を聞いてください。それから、それに対する返事を聞いて、1から3の中から、最もよいものを一つ選んでください。"
    m5_instruction = "問題5では、長めの話を聞きます。この問題には練習はありません。メモをとってもかまいません。"

    choukai_questions = [
        # ==================== MONDAI 1 ====================
        {
            "id": "n2-202507-q72", "number": 72, "sectionGroup": "listening", "section": "聴解 問題1: 課題理解",
            "instruction": m1_instruction,
            "question": "図書館で男の職員と女の職員が話しています。女の職員はこの後まず、何をしますか。",
            "options": [
                "ページがぬけていないか かくにんする",
                "本のデータをとうろくする",
                "本にカバーをつける",
                "イベントで使う本を選ぶ"
            ],
            "answer": 1,
            "script": "図書館で男の職員と女の職員が話しています。女の職員はこの後まず、何をしますか。\n\n男：新しく入った本の登録作業、お願いできる？\n女：はい、本のデータを登録する作業ですね。カバーをつけたり、ページが抜けていないか確認したりする作業はもう済んでいますか。\n男：うん、それは終わってるよ。登録が終わったら、来月のイベントで使う本を何冊か選んでほしいんだけど、まずはデータの入力からよろしく。\n女：わかりました。すぐ始めます。\n\n問い：女の職員はこの後まず何をしますか。",
            "explanation": "【Đáp án đúng: 2 (本のデータをとうろくする)】\n• Nam nhân viên nhờ nữ nhân viên: 「まずはデータの入力からよろしく」 (trước tiên nhờ cô nhập dữ liệu sách mới vào máy).\n• Các việc bọc bìa, kiểm tra trang đã xong trước đó. Việc chọn sách cho sự kiện sẽ làm sau đó."
        },
        {
            "id": "n2-202507-q73", "number": 73, "sectionGroup": "listening", "section": "聴解 問題1: 課題理解",
            "instruction": m1_instruction,
            "question": "科学館で男の職員と女の職員が講演会について話しています。女の職員はこの後何をしますか。",
            "options": [
                "部屋をさがす",
                "質問をまとめて先生に送る",
                "当日のしりょうをいんさつする",
                "ホームページの情報を新しくする"
            ],
            "answer": 2,
            "script": "科学館で男の職員と女の職員が講演会について話しています。女の職員はこの後何をしますか。\n\n男：来週の講演会の準備、進んでる？\n女：はい。参加者からの事前質問をまとめて先生に送る作業と、ホームページの更新は終わりました。\n男：部屋の確保もできてるよね。\n女：はい、第1会議室を押さえてあります。\n男：じゃあ、先生から届いた当日配布用の資料の印刷をお願いできるかな。部数が多いから早めにやっておいてほしいんだ。\n女：わかりました。すぐに印刷室に行って刷ってきます。\n\n問い：女の職員はこの後何をしますか。",
            "explanation": "【Đáp án đúng: 3 (当日のしりょうをいんさつする)】\n• Các việc tổng hợp câu hỏi, cập nhật website, đặt phòng đều đã hoàn tất.\n• Nam nhân viên nhờ: 「当日配布用の資料の印刷をお願いできるかな...早めにやっておいてほしい」, nữ nhân viên đồng ý đi in ngay."
        },
        {
            "id": "n2-202507-q74", "number": 74, "sectionGroup": "listening", "section": "聴解 問題1: 課題理解",
            "instruction": m1_instruction,
            "question": "文房具の会社で課長と男の人が話しています。男の人はこの後まず何をしますか。",
            "options": [
                "チームのメンバーを選ぶ",
                "会議でチームをしょうかいする",
                "メンバーの仕事の内容を決定する",
                "開発スケジュールを作る"
            ],
            "answer": 2,
            "script": "文房具の会社で課長と男の人が話しています。男の人はこの後まず何をしますか。\n\n課長：新商品の開発プロジェクト、メンバーの選定は終わったようね。\n男：はい、各部署から4名選出しました。\n課長：そう。来週の全体会議でチームの紹介をするから、その前にそれぞれのメンバーがどの分野を担当するか、業務内容をきっちり決めておいてちょうだい。全体のスケジュール作成はその役割分担が決まってからね。\n男：承知しました。早速、担当業務の割り振りを詰めます。\n\n問い：男の人はこの後まず何をしますか。",
            "explanation": "【Đáp án đúng: 3 (メンバーの仕事の内容を決定する)】\n• Trưởng phòng chỉ thị: Trước cuộc họp tuần sau, phải xác định rõ nội dung công việc/phân chia vai trò cụ thể cho từng thành viên (業務内容をきっちり決めておいて), sau đó mới làm tiến độ."
        },
        {
            "id": "n2-202507-q75", "number": 75, "sectionGroup": "listening", "section": "聴解 問題1: 課題理解",
            "instruction": m1_instruction,
            "question": "野球場で市役所の職員がアルバイトの人たちに話しています。アルバイトの人たちはこの後まず何をしますか。",
            "options": [
                "アンケートをかいしゅうする",
                "テントをかたづける",
                "作業用てぶくろをする",
                "机といすをトラックにのせる"
            ],
            "answer": 2,
            "script": "野球場で市役所の職員がアルバイトの人たちに話しています。アルバイトの人たちはこの後まず何をしますか。\n\n職員：皆さん、本日のイベントの運営お疲れ様でした。これから会場の撤収作業に入ります。机や椅子の片付けやテントの解体など力仕事になりますので、怪我防止のために、まずは配った作業用手袋を全員はめてください。机や椅子をトラックに積み込むのはその後で指示を出します。アンケートの回収は別のスタッフが対応済みです。\n\n問い：アルバイトの人たちはこの後まず何をしますか。",
            "explanation": "【Đáp án đúng: 3 (作業用てぶくろをする)】\n• Nhân viên nhắc nhở: 「怪我防止のために、まずは配った作業用手袋を全員はめてください」 (Để phòng tránh chấn thương, trước hết tất cả mọi người hãy đeo găng tay lao động vào)."
        },
        {
            "id": "n2-202507-q76", "number": 76, "sectionGroup": "listening", "section": "聴解 問題1: 課題理解",
            "instruction": m1_instruction,
            "question": "大学で美術サークルの男の部長と女の学生が話しています。女の学生はこの後まず何をしますか。",
            "options": [
                "入り口の絵をほかの絵に替える",
                "しょうめいを暗くする",
                "教室に花をかざる",
                "絵と絵のかんかくを広くする"
            ],
            "answer": 1,
            "script": "大学で美術サークルの男の部長と女の学生が話しています。女の学生はこの後まず何をしますか。\n\n男：展示の準備、だいたいできたね。絵の間隔もちょうどいいし、入り口の絵も目を引いていい感じだ。\n女：はい。あ、教室の隅に花を飾るって言ってませんでしたっけ？\n男：それは花が届いてからでいいよ。それより、この照明、ちょっと明るすぎて絵に光が反射しちゃってるんだよね。少し暗めに調整してくれる？\n女：わかりました。スイッチを操作して照明を落としますね。\n\n問い：女の学生はこの後まず何をしますか。",
            "explanation": "【Đáp án đúng: 2 (しょうめいを暗くする)】\n• Trưởng nhóm nhờ: 「この照明、ちょっと明るすぎて絵に光が反射しちゃってるんだよね。少し暗めに調整してくれる？」. Nữ sinh đồng ý làm ngay."
        },

        # ==================== MONDAI 2 ====================
        {
            "id": "n2-202507-q77", "number": 77, "sectionGroup": "listening", "section": "聴解 問題2: ポイント理解",
            "instruction": m2_instruction,
            "question": "大学で女の学生と男の学生が話しています。女の学生は卒業したら何をしたいと言っていますか。",
            "options": [
                "食品かんれんの仕事をする",
                "大学院に進む",
                "研究の仕事をする",
                "しゅっぱんしゃで働く"
            ],
            "answer": 3,
            "script": "大学で女の学生と男の学生が話しています。女の学生は卒業したら何をしたいと言っていますか。\n\n男：もうすぐ就職活動だけど、進路は決めた？大学院に進んで食品の研究を続けると思ってたけど。\n女：最初は研究職を目指して食品メーカーも考えたんだけど、最近は食の魅力を文章や本で伝える仕事がしたいって思うようになったの。だから出版関係の会社に就職したいんだ。\n男：へえ、本を作る仕事か、いいね！\n\n問い：女の学生は卒業したら何をしたいと言っていますか。",
            "explanation": "【Đáp án đúng: 4 (しゅっぱんしゃで働く)】\n• Nữ sinh nói muốn làm công việc truyền tải sự hấp dẫn của ẩm thực qua sách báo nên chọn xin việc vào nhà xuất bản (出版関係の会社に就職したい)."
        },
        {
            "id": "n2-202507-q78", "number": 78, "sectionGroup": "listening", "section": "聴解 問題2: ポイント理解",
            "instruction": m2_instruction,
            "question": "病院で女の人と医者が話しています。医者は何をしてはいけないと言っていますか。",
            "options": [
                "つえを使わないで長時間歩くこと",
                "薬をやめること",
                "自転車で会社に通うこと",
                "足首のトレーニングをすること"
            ],
            "answer": 0,
            "script": "病院で女の人と医者が話しています。医者は何をしてはいけないと言っていますか。\n\n女：先生、足首の痛みはだいぶ良くなりました。もう自転車に乗っても大丈夫でしょうか。\n医者：通勤で乗るくらいなら問題ありませんよ。足首の軽いリハビリ運動も続けてください。薬も痛みが出なければ減らしていって構いません。ただ、杖なしで長い時間歩くのだけはまだ骨に負担がかかるので絶対に避けてください。\n女：わかりました。気をつけます。\n\n問い：医者は何をしてはいけないと言っていますか。",
            "explanation": "【Đáp án đúng: 1 (つえを使わないで長時間歩くこと)】\n• Bác sĩ cảnh báo điều tuyệt đối không được làm: 「ただ、杖なしで長い時間歩くのだけはまだ骨に負担がかかるので絶対に避けてください」."
        },
        {
            "id": "n2-202507-q79", "number": 79, "sectionGroup": "listening", "section": "聴解 問題2: ポイント理解",
            "instruction": m2_instruction,
            "question": "女の高校生と男の高校生が話しています。男の高校生が農業体験で1番印象に残っていることは何ですか。",
            "options": [
                "自然のゆたかな所へ行けたこと",
                "野菜をとる経験をしたこと",
                "同級生の知らなかった面を知ったこと",
                "のうぎょうの面白さを実感したこと"
            ],
            "answer": 2,
            "script": "女の高校生と男の高校生が話しています。男の高校生が農業体験で1番印象に残っていることは何ですか。\n\n女：先週の農業体験合宿、どうだった？自然豊かで野菜の収穫も楽しかったでしょ。\n男：うん、農業の面白さも実感できたけど、それ以上に普段おとなしいクラスメイトが誰よりも率先して畑仕事をしてたり、リーダーシップを発揮してて驚いたんだ。友達の意外な一面を発見できたことが一番心に残ってるよ。\n女：へえ、そういう発見って合宿ならではだよね。\n\n問い：男の高校生が農業体験で1番印象に残っていることは何ですか。",
            "explanation": "【Đáp án đúng: 3 (同級生の知らなかった面を知ったこと)】\n• Nam sinh chia sẻ: 「友達の意外な一面を発見できたことが一番心に残ってるよ」 (Điều đọng lại sâu sắc nhất là phát hiện ra những góc tính cách bất ngờ của bạn bè)."
        },
        {
            "id": "n2-202507-q80", "number": 80, "sectionGroup": "listening", "section": "聴解 問題2: ポイント理解",
            "instruction": m2_instruction,
            "question": "女の人と男の人が公園ボランティアを始めた理由は何ですか。男の人が公園ボランティアを始めた理由です。",
            "options": [
                "花を育てるのに きょうみがあったから",
                "町の人がよろこんでくれるから",
                "いろいろな人と交流したいから",
                "バスで通いやすいから"
            ],
            "answer": 0,
            "script": "女の人と男の人が公園ボランティアについて話しています。男の人が公園ボランティアを始めた理由は何ですか。\n\n女：佐藤さん、最近休日に公園の花壇の手入れボランティアを始めたんだって？\n男：そうなんだ。もともと家でもガーデニングが好きで、花を育てることに興味があったんだよね。広い公園で色んな花を育てられるのが魅力的で始めたんだ。\n女：へえ、地域の人との交流や町の人に喜んでもらえるのもやりがいになりそうだね。\n男：うん、やってみるとそういう楽しさもあるけど、きっかけはやっぱり花が好きだったからなんだ。\n\n問い：男の人が公園ボランティアを始めた理由は何ですか。",
            "explanation": "【Đáp án đúng: 1 (花を育てるのに きょうみがあったから)】\n• Người nam khẳng định lý do bắt đầu: 「もともと家でもガーデニングが好きで、花を育てることに興味があったんだよね」."
        },
        {
            "id": "n2-202507-q81", "number": 81, "sectionGroup": "listening", "section": "聴解 問題2: ポイント理解",
            "instruction": m2_instruction,
            "question": "弁当屋の開発部で女の人と男の人が話しています。2人は試作の弁当をどのように変えて売ることにしましたか。",
            "options": [
                "おかずの味をこくする",
                "ご飯の量を少なくする",
                "サラダの量を増やす",
                "おかずの種類を多くする"
            ],
            "answer": 1,
            "script": "弁当屋の開発部で女の人と男の人が話しています。2人は試作の弁当をどのように変えて売ることにしましたか。\n\n女：健康志向の新作弁当の試作品、アンケートの結果が出ました。おかずの種類が多くて味付けも上品だと好評です。\n男：ただ、女性客からは少しボリュームが多すぎるという意見も出ているね。サラダを増やすか、ご飯の量を減らすか...\n女：サラダを増やすとコストが上がってしまいます。健康を意識する方向けなので、ご飯を少し軽めの小盛りに調整するのが良いのではないでしょうか。\n男：そうだね、それでいこう。\n\n問い：2人は試作の弁当をどのように変えて売ることにしましたか。",
            "explanation": "【Đáp án đúng: 2 (ご飯の量を少なくする)】\n• Cả hai thống nhất giảm lượng cơm để vừa nhẹ bụng, vừa giữ được mức chi phí phù hợp (ご飯を少し軽めの小盛りに調整する)."
        },
        {
            "id": "n2-202507-q82", "number": 82, "sectionGroup": "listening", "section": "聴解 問題2: ポイント理解",
            "instruction": m2_instruction,
            "question": "ラジオで女の人が自分の家で飼っている猫について話しています。女の人がイベントでこの猫を選んだ1番の理由は何ですか。",
            "options": [
                "元気に飛び回っていたから",
                "寝ているすがたが かわいかったから",
                "しっぽの形が気に入ったから",
                "顔の毛の色がユニークだったから"
            ],
            "answer": 3,
            "script": "ラジオで女の人が自分の家で飼っている猫について話しています。女の人がイベントでこの猫を選んだ1番の理由は何ですか。\n\n女：うちの猫は保護猫の譲渡イベントで出会いました。会場には元気に走り回る子や、丸くなって気持ちよさそうに眠っている子などたくさんの猫がいました。その中で、目の周りだけ黒くてまるでマスクをつけているような、顔の模様がとてもユニークな子に一目惚れしたんです。かぎ状の尻尾も可愛かったんですが、決め手となったのはやはりその独特な顔の毛色でした。\n\n問い：女の人がイベントでこの猫を選んだ1番の理由は何ですか。",
            "explanation": "【Đáp án đúng: 4 (顔の毛の色がユニークだったから)】\n• Người phụ nữ nói: 「決め手となったのはやはりその独特な顔の毛色でした」 (Yếu tố quyết định là màu lông trên mặt vô cùng độc đáo)."
        },

        # ==================== MONDAI 3 ====================
        {
            "id": "n2-202507-q83", "number": 83, "sectionGroup": "listening", "section": "聴解 問題3: 概要理解",
            "instruction": m3_instruction,
            "question": "ラジオで女の人が話しています。女の人は何について話していますか。",
            "options": [
                "スマートフォンの最新機能",
                "スマートフォンの便利な活用法",
                "スマートフォンの適切な充電方法",
                "スマートフォンから離れる時間の効果"
            ],
            "answer": 3,
            "script": "ラジオで女の人が話しています。\n\n女：現代人は常にスマホを手放せず、常に情報に追われています。私も以前は少し時間が空くとすぐにスマホを見ていました。しかし、週末の数時間だけでもスマホの電源を切り、通知を気にしない時間を作るようにしたところ、頭がすっきりして読書や散歩を心から楽しめるようになりました。常に誰かとつながっている状態から意識的に離れることは、心の休養にとって本当に大切なことだと実感しています。\n\n問い：女の人は何について話していますか。",
            "explanation": "【Đáp án đúng: 4 (スマートフォンから離れる時間の効果)】\n• Diễn giả nói về trải nghiệm tắt điện thoại vào cuối tuần, nhấn mạnh lợi ích và hiệu quả của việc tạm rời xa smartphone đối với việc nghỉ ngơi tinh thần."
        },
        {
            "id": "n2-202507-q84", "number": 84, "sectionGroup": "listening", "section": "聴解 問題3: 概要理解",
            "instruction": m3_instruction,
            "question": "講演会で家具を作る職人が話しています。家具を作る職人は何について話していますか。",
            "options": [
                "伝統的な家具の歴史",
                "オーダーメイド家具の注文手順",
                "使い手の生活に合わせた家具作りの姿勢",
                "家具の耐久性を高める塗料の種類"
            ],
            "answer": 2,
            "script": "講演会で家具を作る職人が話しています。\n\n職人：家具作りにおいて私が最も大切にしているのは、技術の誇示ではなく、その家具を使う人の日常生活にいかに馴染むかということです。例えば椅子の高さを決めるときも、単に標準的な寸法で作るのではなく、家族がどんな姿勢で食事をし、どんな風にくつろぐのかを丁寧に聞き取ってから設計します。使う人の日々の暮らしに寄り添い、何十年も心地よく使ってもらえることこそが、家具職人の使命だと考えています。\n\n問い：家具を作る職人は何について話していますか。",
            "explanation": "【Đáp án đúng: 3 (使い手の生活に合わせた家具作りの姿勢)】\n• Nghệ nhân nhấn mạnh thái độ làm mộc: lắng nghe và thấu hiểu lối sống của người sử dụng để làm ra món đồ nội thất đồng hành lâu dài cùng gia đình."
        },
        {
            "id": "n2-202507-q85", "number": 85, "sectionGroup": "listening", "section": "聴解 問題3: 概要理解",
            "instruction": m3_instruction,
            "question": "テレビでアナウンサーの男の人がお菓子屋の人にインタビューしています。お菓子屋の人は何について話していますか。",
            "options": [
                "地元の旬の果物を生かした商品作り",
                "伝統的な製法を守り続ける難しさ",
                "若い世代に向けた店舗の内装デザイン",
                "海外への販路拡大の計画"
            ],
            "answer": 0,
            "script": "テレビでアナウンサーの男の人がお菓子屋の人にインタビューしています。\n\nアナウンサー：こちらの老舗のお菓子屋さんですが、最近新作のケーキが大人気だそうですね。\n店主：はい。この地域で採れる新鮮な旬の果物を農家から直接仕入れて、そのみずみずしさをそのまま生かしたスイーツ作りにこだわっています。地元の良質な素材のおいしさをそのまま味わっていただきたいという思いで開発しました。季節ごとに変わる地域の味をお客様に楽しんでいただいています。\n\n問い：お菓子屋の人は何について話していますか。",
            "explanation": "【Đáp án đúng: 1 (地元の旬の果物を生かした商品作り)】\n• Chủ tiệm bánh chia sẻ về sự chú trọng khai thác nguồn hoa quả tươi theo mùa thu hoạch trực tiếp tại địa phương để làm nên sản phẩm đặc trưng."
        },
        {
            "id": "n2-202507-q86", "number": 86, "sectionGroup": "listening", "section": "聴解 問題3: 概要理解",
            "instruction": m3_instruction,
            "question": "市民講座で専門家が話しています。専門家は何について話していますか。",
            "options": [
                "質の良い睡眠をとるための工夫",
                "朝食をしっかり食べることのメリット",
                "夜遅い運動が体に与える影響",
                "睡眠不足による生活習慣病のリスク"
            ],
            "answer": 0,
            "script": "市民講座で専門家が話しています。\n\n専門家：朝すっきりと目覚めるためには、単に睡眠時間を長く取るだけでなく、睡眠の質を高めることが重要です。就寝前の1時間は部屋の照明を少し落とし、スマホやパソコンの強い光を避けること。そしてぬるめのお湯にゆっくり浸かって体を温めておくと、自然な体温低下とともに深い眠りに入りやすくなります。毎日のちょっとした工夫で、睡眠の質は大きく改善します。\n\n問い：専門家は何について話していますか。",
            "explanation": "【Đáp án đúng: 1 (質の良い睡眠をとるための工夫)】\n• Chuyên gia hướng dẫn những mẹo và thói quen sinh hoạt trước khi ngủ nhằm nâng cao chất lượng giấc ngủ."
        },
        {
            "id": "n2-202507-q87", "number": 87, "sectionGroup": "listening", "section": "聴解 問題3: 概要理解",
            "instruction": m3_instruction,
            "question": "テレビでアナウンサーが話しています。アナウンサーは何について話していますか。",
            "options": [
                "商店街の店舗減少の歴史",
                "高齢化による商業施設の利用変化",
                "大型スーパーと地元商店街の競争",
                "空き店舗を活用した商店街活性化の試み"
            ],
            "answer": 3,
            "script": "テレビでアナウンサーが話しています。\n\nアナウンサー：後継者不足などでシャッターが閉まったままの店舗が目立っていたこちらの商店街ですが、最近新しい動きが始まっています。使われなくなった空き店舗をリノベーションし、若手クリエイターの工房や地域のコミュニティカフェとして貸し出すプロジェクトです。これにより若い世代の来訪者が増え、商店街全体にかつての賑わいが戻りつつあります。\n\n問い：アナウンサーは何について話していますか。",
            "explanation": "【Đáp án đúng: 4 (空き店舗を活用した商店街活性化の試み)】\n• Bản tin tường thuật nỗ lực hồi sinh khu phố thương mại thông qua việc tận dụng các cửa hàng bỏ trống làm xưởng nghệ thuật và quán cà phê cộng đồng."
        },

        # ==================== MONDAI 4 ====================
        {
            "id": "n2-202507-q88", "number": 88, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "昨日は腹痛でおかゆすら食べられなかったんだ。",
            "options": [
                "おかゆがおいしかったんだね。",
                "それは大変だったね、もう大丈夫？",
                "おかゆだけは食べられたんだね。"
            ],
            "answer": 1,
            "script": "男：昨日は腹痛でおかゆすら食べられなかったんだ。\n1 おかゆがおいしかったんだね。\n2 それは大変だったね、もう大丈夫？\n3 おかゆだけは食べられたんだね。",
            "explanation": "【Đáp án đúng: 2】\n• ～すら: ngay cả... cũng không. \"Hôm qua đau bụng đến mức ngay cả cháo cũng không nuốt nổi\". Phản hồi đồng cảm phù hợp nhất: \"Khổ thân bạn, đã đỡ hơn chưa?\""
        },
        {
            "id": "n2-202507-q89", "number": 89, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "先週の旅行、雨だったけど、かえって素敵だったよね。",
            "options": [
                "雨で散々な目に遭ったね。",
                "晴れて本当に良かったよね。",
                "うん、しっとりして風情があったね。"
            ],
            "answer": 2,
            "script": "女：先週の旅行、雨だったけど、かえって素敵だったよね。\n1 雨で散々な目に遭ったね。\n2 晴れて本当に良かったよね。\n3 うん、しっとりして風情があったね。",
            "explanation": "【Đáp án đúng: 3】\n• かえって: ngược lại (mang ý nghĩa tích cực ngoài dự tính). Người kia khen trời mưa lại tạo cảm giác tuyệt vời, đáp lại đồng tình: \"Ừ, phong cảnh tĩnh lặng rất nên thơ\"."
        },
        {
            "id": "n2-202507-q90", "number": 90, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "渡辺さん、社長がお呼びですよ。",
            "options": [
                "はい、すぐ伺います。",
                "社長をお呼びしましょうか。",
                "社長はどちらへ行かれますか。"
            ],
            "answer": 0,
            "script": "女：渡辺さん、社長がお呼びですよ。\n1 はい、すぐ伺います。\n2 社長をお呼びしましょうか。\n3 社長はどちらへ行かれますか。",
            "explanation": "【Đáp án đúng: 1】\n• \"Watanabe ơi, giám đốc gọi anh đấy\". Khiêm nhường ngữ đáp lại khi được cấp trên gọi: 「はい、すぐ伺います」 (Vâng, tôi sang gặp ngay đây)."
        },
        {
            "id": "n2-202507-q91", "number": 91, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "見てこの定食。この量は食べきれないよ。",
            "options": [
                "本当だ、すごいボリュームだね。",
                "全部食べちゃったんだね。",
                "もう少し大盛りにしてもらおうか。"
            ],
            "answer": 0,
            "script": "男：見てこの定食。この量は食べきれないよ。\n1 本当だ、すごいボリュームだね。\n2 全部食べちゃったんだね。\n3 もう少し大盛りにしてもらおうか。",
            "explanation": "【Đáp án đúng: 1】\n• ～きれない: không thể nào hết. \"Nhìn suất ăn này đi, nhiều thế này ăn sao hết\". Đáp lại: \"Đúng thật, khẩu phần nhiều ghê\"."
        },
        {
            "id": "n2-202507-q92", "number": 92, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "小野さん、ご両親と相談したうえでどの学校を受験するか決めてくださいね。",
            "options": [
                "はい、一人で勝手に決めます。",
                "わかりました、よく話し合ってみます。",
                "両親には知らせなくていいんですね。"
            ],
            "answer": 1,
            "script": "先生：小野さん、ご両親と相談したうえでどの学校を受験するか決めてくださいね。\n1 はい、一人で勝手に決めます。\n2 わかりました、よく話し合ってみます。\n3 両親には知らせなくていいんですね。",
            "explanation": "【Đáp án đúng: 2】\n• ～たうえで: sau khi... Giáo viên dặn hãy thảo luận với bố mẹ rồi mới quyết định trường dự thi, đáp lại: \"Vâng, em sẽ bàn bạc kỹ với gia đình ạ\"."
        },
        {
            "id": "n2-202507-q93", "number": 93, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "奨学金の申請、早く準備しないと期限が近いよ。",
            "options": [
                "締め切りはまだずっと先だよ。",
                "教えてくれてありがとう、すぐ書類書くよ。",
                "申請しなくてもいいんだね。"
            ],
            "answer": 1,
            "script": "女：奨学金の申請、早く準備しないと期限が近いよ。\n1 締め切りはまだずっと先だよ。\n2 教えてくれてありがとう、すぐ書類書くよ。\n3 申請しなくてもいいんだね。",
            "explanation": "【Đáp án đúng: 2】\n• \"Hạn nộp học bổng sắp đến rồi đấy, không chuẩn bị nhanh là muộn mất\". Phản hồi: \"Cảm ơn bạn đã nhắc, mình sẽ viết giấy tờ ngay\"."
        },
        {
            "id": "n2-202507-q94", "number": 94, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "新しく出たイヤホン、人気があるだけにどの店にも残ってなかったよ。",
            "options": [
                "どのお店でも簡単に手に入ったんだね。",
                "人気がないから売り切れたんだね。",
                "さすが評判通り、大人気なんだね。"
            ],
            "answer": 2,
            "script": "男：新しく出たイヤホン、人気があるだけにどの店にも残ってなかったよ。\n1 どのお店でも簡単に手に入ったんだね。\n2 人気がないから売り切れたんだね。\n3 さすが評判通り、大人気なんだね。",
            "explanation": "【Đáp án đúng: 3】\n• ～だけに: chính vì... \"Chính vì được yêu thích nên mẫu tai nghe mới chẳng còn chiếc nào ở tiệm\". Đáp: \"Quả đúng như lời đồn, hot thật sự\"."
        },
        {
            "id": "n2-202507-q95", "number": 95, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "兄と 2 年前に言い合いしちゃって、その時会ったきりなんだ。",
            "options": [
                "あれ以来、一度も会ってないんだね。",
                "2年ぶりに会えてよかったね。",
                "喧嘩のあとすぐ仲直りしたんだね。"
            ],
            "answer": 0,
            "script": "女：兄と 2 年前に言い合いしちゃって、その時会ったきりなんだ。\n1 あれ以来、一度も会ってないんだね。\n2 2年ぶりに会えてよかったね。\n3 喧嘩のあとすぐ仲直りしたんだね。",
            "explanation": "【Đáp án đúng: 1】\n• ～たきり: kể từ lần đó suốt cho tới nay chưa từng lặp lại. \"Cãi nhau với anh 2 năm trước và từ đó tới giờ chưa gặp lại\". Đáp: \"Kể từ dạo đó đến giờ chưa gặp lại lần nào à\"."
        },
        {
            "id": "n2-202507-q96", "number": 96, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "本日は商品説明会へお越しいただきありがとうございます。",
            "options": [
                "いいえ、お越しいただき光栄です。",
                "こちらこそ、お招きいただき感謝申し上げます。",
                "どういたしまして、すぐ失礼します。"
            ],
            "answer": 1,
            "script": "司会：本日は商品説明会へお越しいただきありがとうございます。\n1 いいえ、お越しいただき光栄です。\n2 こちらこそ、お招きいただき感謝申し上げます。\n3 どういたしまして、すぐ失礼します。",
            "explanation": "【Đáp án đúng: 2】\n• Lời chào mở đầu trong hội thảo thương mại: \"Cảm ơn quý vị đã dành thời gian đến dự buổi giới thiệu sản phẩm hôm nay\". Khách đáp: \"Chính chúng tôi mới phải cảm ơn vì lời mời\"."
        },
        {
            "id": "n2-202507-q97", "number": 97, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "昨日のマラソン大会、田村選手 1 位に迫る勢いだったね。",
            "options": [
                "トップには全然届かなかったね。",
                "優勝は逃したけど、素晴らしい走りだったね。",
                "本当に1位でゴールできて良かったね。"
            ],
            "answer": 1,
            "script": "男：昨日のマラソン大会、田村選手 1 位に迫る勢いだったね。\n1 トップには全然届かなかったね。\n2 優勝は逃したけど、素晴らしい走りだったね。\n3 本当に1位でゴールできて良かったね。",
            "explanation": "【Đáp án đúng: 2】\n• ～に迫る勢い: khí thế áp sát/bám đuổi sít sao vị trí thứ 1. Đáp: \"Dù bỏ lỡ chức vô địch nhưng màn trình diễn bám đuổi quả thực tuyệt vời\"."
        },
        {
            "id": "n2-202507-q98", "number": 98, "sectionGroup": "listening", "section": "聴解 問題4: 即時応答",
            "instruction": m4_instruction,
            "question": "原さん。サークルの部屋の掃除、佐藤さんも手伝ってくれるとよかったのにね。",
            "options": [
                "佐藤さんが手伝ってくれて助かったよ。",
                "本当ね、急用が入っちゃったみたいで残念だったわ。",
                "佐藤さんには頼まない方がいいよ。"
            ],
            "answer": 1,
            "script": "女：原さん。サークルの部屋の掃除、佐藤さんも手伝ってくれるとよかったのにね。\n1 佐藤さんが手伝ってくれて助かったよ。\n2 本当ね、急用が入っちゃったみたいで残念だったわ。\n3 佐藤さんには頼まない方がいいよ。",
            "explanation": "【Đáp án đúng: 2】\n• ～とよかったのに: giá mà... thì tốt biết bao (tiếc nuối vì thực tế không xảy ra). Đáp: \"Đúng vậy, tiếc là bạn ấy có việc bận đột xuất không phụ giúp được\"."
        },

        # ==================== MONDAI 5 ====================
        {
            "id": "n2-202507-q99", "number": 99, "sectionGroup": "listening", "section": "聴解 問題5: 統合理解",
            "instruction": m5_instruction,
            "question": "市のスポーツセンターで職員がイベントについて話しています。問題に対応するために、何をすることにしましたか。",
            "options": [
                "参加人数を制限する",
                "開催時間を変更する",
                "案内スタッフを増員する",
                "会場の部屋を広げる"
            ],
            "answer": 2,
            "script": "市のスポーツセンターで職員がイベントについて話しています。問題に対応するために、何をすることにしましたか。\n\n男：来月の健康スポーツフェスティバルの準備状況ですが、前回の開催時に受付周辺で参加者が迷って混雑が発生したという課題がありました。\n女：会場の広さ自体は十分でしたので部屋を変える必要はありませんが、受付から各競技コーナーへの動線で戸惑う方が多かったですね。\n男：参加人数を制限したり時間を短縮するよりは、当日の誘導をスムーズにする必要がありますね。\n女：はい。各通路や曲がり角に案内スタッフを配置して誘導を強化すれば、混雑は防げると思います。\n男：よし、ボランティアとスタッフのシフトを調整して案内係を増員しよう。\n\n問い：問題に対応するために、何をすることにしましたか。",
            "explanation": "【Đáp án đúng: 3 (案内スタッフを増員する)】\n• Hai nhân viên thống nhất giải pháp xử lý ùn tắc là tăng cường nhân viên hướng dẫn tại các ngã rẽ và lối đi (案内スタッフを増員する)."
        },
        {
            "id": "n2-202507-q100", "number": 100, "sectionGroup": "listening", "section": "聴解 問題5: 統合理解",
            "instruction": m5_instruction,
            "question": "ラジオを聞いて男の人と女の人が話しています。質問1：２人は 1 日目、どこに夕日を見に行きますか。",
            "options": [
                "夕日通り",
                "にしがおか",
                "さくら公園",
                "東山"
            ],
            "answer": 0,
            "script": "ラジオを聞いて男の人と女の人が話しています。\n\nラジオ：秋の夕暮れ、美しい夕日を楽しめる市内のおすすめスポットをご紹介します。1つ目は海沿いの『夕日通り』。水平線に沈む太陽が圧巻で、遊歩道を歩きながら楽しめます。2つ目は高台にある『にしがおか』。街の夜景と夕焼けのコントラストが素晴らしく、静かに過ごせます。3つ目は『さくら公園』、水辺に映る夕日が絵画のようです。4つ目は山頂の『東山』、遠くの山並みまで一望できます。\n\n男：今度の週末のドライブ、夕日を見に行こうよ。1日目は海沿いのドライブだから、海に沈む夕日が見たいな。\n女：いいね！海沿いなら1番の夕日通りね。夕日通りを散歩しながら見よう。\n\n質問1：２人は 1 日目、どこに夕日を見に行きますか。",
            "explanation": "【Đáp án đúng: 1 (夕日通り)】\n• Ngày 1 đi dọc bờ biển nên cả hai chọn điểm số 1: con đường ngắm hoàng hôn ven biển (夕日通り)."
        },
        {
            "id": "n2-202507-q101", "number": 101, "sectionGroup": "listening", "section": "聴解 問題5: 統合理解",
            "instruction": m5_instruction,
            "question": "ラジオを聞いて男の人と女の人が話しています。質問2：２人は 2 日目、どこに夕日を見に行きますか。",
            "options": [
                "夕日通り",
                "にしがおか",
                "さくら公園",
                "東山"
            ],
            "answer": 1,
            "script": "男：2日目はどうする？山の東山か、高台のにしがおかもいいね。\n女：山登りは疲れるから、車で気軽に行けて街の明かりと夕焼けが両方楽しめる高台の場所がいいな。\n男：それなら2番のにしがおかだね。そこに決まり！\n\n質問2：２人は 2 日目、どこに夕日を見に行きますか。",
            "explanation": "【Đáp án đúng: 2 (にしがおか)】\n• Ngày thứ 2 nữ thích nơi đồi cao ngắm cảnh thành phố không phải leo núi, nên hai người chọn điểm số 2: ngọn đồi Nishigaoka (にしがおか)."
        }
    ]

    data['questions'].extend(choukai_questions)
    data['totalQuestions'] = len(data['questions'])
    data['vocabGrammarCount'] = 51
    data['readingCount'] = 20
    data['listeningCount'] = len(choukai_questions)
    data['durations'] = {
        "vocab_grammar": 35,
        "reading": 70,
        "listening": 50,
        "full": 155
    }

    print(f"Total questions with Choukai: {data['totalQuestions']}")
    print(f"  Vocab/Grammar: {data['vocabGrammarCount']}")
    print(f"  Reading: {data['readingCount']}")
    print(f"  Listening: {data['listeningCount']}")

    out_json = json.dumps(data, ensure_ascii=False, indent=2)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(out_json)
    print(f"Saved: {target_file}")

    if os.path.exists(alt_file):
        with open(alt_file, 'w', encoding='utf-8') as f:
            f.write(out_json)
        print(f"Saved: {alt_file}")

    def update_index(idx_path):
        if not os.path.exists(idx_path):
            return
        with open(idx_path, 'r', encoding='utf-8-sig') as f:
            exams = json.load(f)
        for e in exams:
            if e.get('id') == 'n2-2025-07' or (e.get('year') == 2025 and e.get('month') == 7):
                e['totalQuestions'] = 101
                e['vocabGrammarCount'] = 51
                e['readingCount'] = 20
                e['listeningCount'] = 30
                e['available'] = True
                e['hasAudio'] = True
                e['audio'] = 'data/audio/n2_2025_07.mp3'
                e['durations'] = {
                    "vocab_grammar": 35,
                    "reading": 70,
                    "listening": 50,
                    "full": 155
                }
        with open(idx_path, 'w', encoding='utf-8') as f:
            json.dump(exams, f, ensure_ascii=False, indent=2)
        print(f"Updated index: {idx_path}")

    update_index(index_file)
    update_index(alt_index_file)

if __name__ == '__main__':
    main()
