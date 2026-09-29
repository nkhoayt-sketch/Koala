import os
import sys
import json
import glob
import re
import shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==============================================================================
# 1. EXACT REPAIR PATCHES FOR IDENTIFIED QUESTIONS
# ==============================================================================
EXAM_PATCHES = {
    # 2011_12
    ("2011_12.json", 52): {
        "question": "【52】に入る最も適当なものはどれか。",
        "options": ["思われます", "わかります", "考えられます", "調べられます"],
        "answer": 2
    },
    ("2011_12.json", 74): {
        "question": "留学生のリーさんは、友人と一緒に6 人でこの別館を見学したいと考えている。6 人1組で一緒に申し込むことはできるか。また、6 人が同じ時間に一緒に見学することは可能か。",
        "options": [
            "6 人1 組で申し込むことが可能で、同じ時間に一緒に見学することができる。",
            "6 人1 組で申し込むことはできるが、同じ時間に一緒に見学できるとは限らない。",
            "2 組に分けて申し込む必要があり、同じ時間に一緒に見学できない可能性もある。",
            "3 組に分けて申し込まなければならず、同じ時間に一緒に見学することはできない。"
        ],
        "answer": 2
    },

    # 2012_12
    ("2012_12.json", 41): {
        "question": "先輩 ｢受験する大学は決まった？」\n後輩「いえ、僕は海外の大学に行きたいんですけど、両親は僕を自宅から通える大学に（   ）」。",
        "options": [
            "行かせてほしいんです",
            "行こうとしてほしいんです",
            "行かせたがっているんです",
            "行こうとしたがっているんです"
        ],
        "answer": 2
    },
    ("2012_12.json", 68): {
        "question": "「預かりものの思想」では、ものをどのように考えているか。",
        "options": [
            "生きている間にすべて返さなければならない。",
            "生きている間だけ世の中から借りている。",
            "所有していてもいつかは消えてしまう。",
            "所有するより借りたほうがいい。"
        ],
        "answer": 1
    },

    # 2013_07
    ("2013_07.json", 74): {
        "question": "岩田さんはこの事典をなるべく安く手に入れたい。予約方法と代金の支払いはどうすればよいか。",
        "options": [
            "1 月15 日までに書店で予約し、1 月20 日までに全額を振り込む。",
            "1 月15 日までに書店で予約し、2 月1 日に書店で全額を支払う。",
            "1 月15 日までにホームページで予約し、同時にクレジットカードで全額を支払う。",
            "1 月15 日までにホームページで予約し、1 月20 日までに分割払いの初回分を振り込む。"
        ],
        "answer": 2
    },

    # 2013_12
    ("2013_12.json", 37): {
        "question": "今年の映画祭の来場者は、開幕から3 日で10 万人に達した。八日間の開催期間で最終的には昨年の20 万人を大幅に上回る（   ）。",
        "options": ["までだ", "次第だ", "勢いだ", "最中だ"],
        "answer": 2
    },
    ("2013_12.json", 41): {
        "question": "悩んでいる時は、誰かに話を（   ）気持ちが楽になる場合もある。",
        "options": [
            "聞いてあげることは",
            "聞いてもらうことで",
            "聞いてくれることに",
            "聞いてやることが"
        ],
        "answer": 1
    },

    # 2014_07
    ("2014_07.json", 56): {
        "question": "この文書によると､ 市役所は何を知るためにアンケートをしようとしているか。",
        "options": [
            "町づくり事業のホームページに対する市民の意見",
            "町づくり事業に対する市民の評価",
            "広場づくりに対する市民の意見",
            "広場づくりに対する市民の評価"
        ],
        "answer": 2
    },
    ("2014_07.json", 74): {
        "question": "商品を購入する際に、送料と手数料を払わなくてもいいのは次の4 人のうち誰か。",
        "options": ["ヘサルさん", "山田さん", "ジョンソンさん", "シンさん"],
        "answer": 2
    },

    # 2014_12
    ("2014_12.json", 41): {
        "question": "私は、いつ雨が（   ）、常に折り畳み傘を持ち歩いている。",
        "options": [
            "降ってもいいように",
            "降っているとすると",
            "降らないせいで",
            "降ることがないのに"
        ],
        "answer": 0
    },
    ("2014_12.json", 52): {
        "question": "【52】に入る最も適当なものはどれか。",
        "options": [
            "問題ないかどうかだ",
            "問題ないということだ",
            "問題ないとするだろうか",
            "問題ないのだと思っていた"
        ],
        "answer": 1
    },
    ("2014_12.json", 57): {
        "passage": "（３）\n以下は、ある調査に関する記事である。\n最近、格安航空会社に高い関心が寄せられているようだ。ある調査で、この1 年に国内の旅行や帰省で飛行機を利用した20〜60 代の男女に「今後格安航空会社を利用したいか」を聞いた。その結果、「利用したい」または「やや利用したい」と答えた人の割合は、20代男性が91％でもっとも多く、以下、40 代男性、30 代男性、20 代女性、30 代女性と続くが、いずれも約70％と高い。50 代、60 代は男女ともにやや割合が下がるが、最も低い40代女性でも半数を超えていた。",
        "question": "今後格安航空会社を「利用したい」または「やや利用したい」と答えた人の割合について、この記事からわかることはどれか。",
        "options": [
            "すべての性別・年代で50％以上である。",
            "20 代と30 代では、男女とも70％前後である。",
            "男女とも、30 代より40 代のほうが割合が高い。",
            "男女とも、年齢が低いほど割合が高い。"
        ],
        "answer": 0
    },
    ("2014_12.json", 63): {
        "question": "①“本当にやりたいこと”が見えてくるはずだとあるが、どうすれば見えてくるか。",
        "options": [
            "10 億円よりも想像しやすい金額から夢を考え始める。",
            "10 億円を使い切るには、どうすればいいかを考える。",
            "10 億円あれば実現できることを常に考える。",
            "10 億円を稼いだ自分の姿を想像し続ける。"
        ],
        "answer": 2
    },
    ("2014_12.json", 64): {
        "question": "②10 億円の夢を描けば、10 億円を手にすることは可能なのだとあるが、なぜか。",
        "options": [
            "10 億円の稼ぎ方を教えてくれる人があらわれるかもしれないから",
            "10 億円を稼ぐための具体的な行動を起こせるかもしれないから",
            "夢を実現するうえで、誰が必要かわかるようになるかもしれないから",
            "夢の実現を助けてくれる人があらわれるかもしれないから"
        ],
        "answer": 3
    },
    ("2014_12.json", 74): {
        "question": "オーリャさんと山下さんの二人は臨時スタッフになって、海岸清掃活動に参加したいと思っている。二人はどうしなければならないか。",
        "options": [
            "4 月23 日までE メールで申し込む。",
            "4 月23 日の17 時までに電話で申し込む。",
            "5 月14 日の13 時までに会場に行って、申し込む。",
            "5 月15 日の8 時までに会場に行って、申し込む。"
        ],
        "answer": 1
    },

    # 2015_07
    ("2015_07.json", 50): {
        "question": "【50】に入る最も適当なものはどれか。",
        "options": [
            "２メートルくらいだっただろうか",
            "２メートルくらいだったものなのか",
            "２メートルくらいだと言われたそうだ",
            "２メートルくらいだと思われていたことだ"
        ],
        "answer": 0
    },
    ("2015_07.json", 52): {
        "question": "【52】に入る最も適当なものはどれか。",
        "options": ["使われている", "使っていく", "使おう", "使わせる"],
        "answer": 0
    },
    ("2015_07.json", 64): {
        "question": "②ある消費者調査の結果について、この文章で述べられているのはどれか。",
        "options": [
            "金属製ボトルに対する抵抗感には男女差がある。",
            "金属製ボトルに対しては、60 歳を境に好みが分かれる。",
            "目新しい形や色のペットボトルは、性別を問わず好まれる。",
            "60 歳以上の人は、男女ともに見慣れた形や色のペットボトルを好む。"
        ],
        "answer": 1
    },
    ("2015_07.json", 74): {
        "question": "チェさんは、職場の同僚とバーベキューに行くことになった。費用を調べるように頼まれたので、日時と人数などを聞いてメモをした。費用は一人いくらかかるか。\nチェさんのメモ\n● 11 月15 日(日)10:30∼14:30   ● 参加者 25 人\n● ボリュームセット 25 人分   ● 飲み物は会社から持参",
        "options": [
            "利用料金1,000 円のみ",
            "利用料金1,200 円のみ",
            "利用料金1,000 円とバーベキューセット代2,000 円",
            "利用料金1,200 円とバーベキューセット代2,000 円"
        ],
        "answer": 2
    },
    ("2015_07.json", 75): {
        "question": "この施設を利用する際に気をつけなければならないことは、次のうちどれか。",
        "options": [
            "飲み物と調理器具は、各自が持参する。",
            "10:30 から19:00 まで利用する場合、2 回の利用料金を払う。",
            "団体で利用する場合、予約は2 か月前にしておく。",
            "予約と料金の支払いは、利用の前日までに済ませておく。"
        ],
        "answer": 1
    },

    # 2015_12
    ("2015_12.json", 51): {
        "question": "【51】に入る最も適当なものはどれか。",
        "options": [
            "2 杯分以上だ",
            "2 杯分以上でもおかしくない",
            "2 杯分以上だからだ",
            "2 杯分以上でなければいけない"
        ],
        "answer": 0
    },
    ("2015_12.json", 52): {
        "question": "【52】に入る最も適当なものはどれか。",
        "options": ["実験だといえる", "実験だとしている", "実験がある", "実験になる"],
        "answer": 2
    },
    ("2015_12.json", 56): {
        "question": "中島さんが準備すべきこととして、合っているのはどれか。",
        "options": [
            "12 月10 日に見学者の日本語レベルを確認する。",
            "12 月11 日までに会議室A を予約する。",
            "12 月17 日までに会社案内パンフレットを準備する。",
            "12 月18 日に会議室B のテーブルやいすなどを準備する。"
        ],
        "answer": 2
    },

    # 2016_07
    ("2016_07.json", 50): {
        "question": "【50】に入る最も適当なものはどれか。",
        "options": [
            "24 時間なのか",
            "24 時間ではないのか",
            "24 時間といえるか",
            "24 時間だっただろうか"
        ],
        "answer": 1
    },
    ("2016_07.json", 75): {
        "question": "ベップさんは 2017 年4 月から日本に留学し、東京の大学に入学予定である。ベップさんは 2017 年の3 月に来日する予定だ。ベップさんに可能な応募方法はどれか。",
        "options": [
            "2 月20 日の17 時までに、申請書と、合格通知書のコピーのみを持参する。",
            "2 月20 日必着で、申請書と、合格通知書コピーのみを郵送する。",
            "2 月20 日必着で、申請書と、合格通知書・パスポートの各コピーをFAX する。",
            "2 月20 日必着で、申請書と、合格通知書・パスポートの各データをE メールで送る。"
        ],
        "answer": 3
    },

    # 2016_12 (Mondai 9 Q50-54)
    ("2016_12.json", 50): {
        "question": "【50】に入る最も適当なものはどれか。",
        "options": ["ご存じなわけだ", "ご存じだろうか", "ご存じのようだ", "ご存じだからだろう"],
        "answer": 1
    },
    ("2016_12.json", 51): {
        "question": "【51】に入る最も適当なものはどれか。",
        "options": ["それに", "しかし", "または", "それどころか"],
        "answer": 1
    },
    ("2016_12.json", 52): {
        "question": "【52】に入る最も適当なものはどれか。",
        "options": ["作成者が理解したのは", "日本で考えられたのが", "ここに生み出したのは", "こうして生まれたのが"],
        "answer": 3
    },
    ("2016_12.json", 53): {
        "question": "【53】に入る最も適当なものはどれか。",
        "options": ["使用されている", "使用した点だ", "使用していける", "使用したいものだ"],
        "answer": 0
    },
    ("2016_12.json", 54): {
        "question": "【54】に入る最も適当なものはどれか。",
        "options": ["結果として表れるかもしれない", "結果のはずだった", "結果に違いない", "結果でなければならなかった"],
        "answer": 2
    },
    ("2016_12.json", 74): {
        "question": "ユンさんは、来週ミハマホテルのビュッフェに行きたいと考えている。金曜か土曜の12 時から 17 時の間で、2 時間いられるものがいい。ユンさんの希望に合うビュッフェはどれか。",
        "options": [
            "「ベルン」のランチビュッフェ",
            "「ベルン」のデザートビュッフェ",
            "「ベルン」の夕食ビュッフェ",
            "「みよし」のランチビュッフェ"
        ],
        "answer": 3
    },

    # 2017_07
    ("2017_07.json", 61): {
        "question": "筆者によると、新聞を使うといいのはなぜか。",
        "options": [
            "問題点が簡潔にまとめられていて、早く理解できるから",
            "身近な問題だけでなく、社会全体の問題も扱っているから",
            "憲法などの法の基本的なことが多く取り上げられているから",
            "今問題となっていることは、自分のこととして考えやすいから"
        ],
        "answer": 3
    },

    # 2017_12
    ("2017_12.json", 57): {
        "question": "年内に大型ごみを捨てたい寮生は、どうするように言われているか。",
        "options": [
            "12 月18 日までに清掃局の収集を申し込み、収集日を管理室に連絡する。",
            "12 月18 日までに管理室に連絡し、年内の収集が可能かどうか確認する。",
            "12 月22 日までに清掃局に収集を申し込み、収集日がいつか確認する。",
            "12 月22 日までに管理室に連絡し、清掃局への収集申し込みを依頼する。"
        ],
        "answer": 0
    },

    # 2018_12
    ("2018_12.json", 56): {
        "question": "このお知らせで伝えたいことは何か。",
        "options": [
            "インターネット販売は11 月30 日で中止し、製造体制が整うまで店での販売のみ行う。",
            "インターネット販売は11 月30 日で中止し、12 月1 日からは店での販売を始める。",
            "インターネット販売も店での販売も11 月30 日で中止するが、製造体制が整ったらともに再開する。",
            "インターネット販売も店での販売も11 月30 日で中止するが、製造体制が整ったら店での販売のみ再開する。"
        ],
        "answer": 0
    },

    # 2019_12
    ("2019_12.json", 71): {
        "question": "ポリーさんは、朝田市のダンス教室の仲間と文化祭でダンスの発表をしたいと考えている。申し込みにあたって、注意しなければならないこととして合っているのはどれか。",
        "options": [
            "10 分以内の発表時間で申し込まなければならない。",
            "事務所に直接行って申込書を提出しなければならない。",
            "1 枚の申込書に出演者全員の名前を書かなければならない。",
            "事前の舞台リハーサルに出なければならない。"
        ],
        "answer": 2
    },
    ("2019_12.json", 72): {
        "question": "ザーリンさんは文化祭に申し込みをし、写真作品を展示することになった。この後、文化祭が始まるまでに、何をしなければならないか。",
        "options": [
            "10 月4 日の説明会に行き、文化祭初日の前日の9 時から 17 時の間に作品を運び入れる。",
            "10 月4 日の説明会に行き、文化祭初日の7 時から9 時の間に作品を運び入れる。",
            "10 月4 日から6 日のどれかの説明会に行き、文化祭初日の前日の9 時から17 時の間に作品を運び入れる。",
            "10 月4 日から6 日のどれかの説明会に行き、文化祭初日の7 時から9 時の間に作品を運び入れる。"
        ],
        "answer": 1
    },

    # 2020_12
    ("2020_12.json", 72): {
        "question": "加山さんは、旅行に行くため四国地方の自宅から平山空港に荷物を送ろうと思っている。縦、横、高さの合計が90cm で重さが13kg のスーツケースを、配送会社の営業所に持っていって通常配送で送るつもりである。片道だけの利用の場合、料金はいくらになるか。",
        "options": [
            "2000 円から100 円割引された金額",
            "2000 円から200 円割引された金額",
            "2400 円から200 円割引された金額",
            "2400 円から100 円割引された金額"
        ],
        "answer": 3
    },

    # 2021_07
    ("2021_07.json", 49): {
        "question": "【49】に入る最も適当なものはどれか。",
        "options": ["なお", "たとえば", "そこで", "ところが"],
        "answer": 2
    },
    ("2021_07.json", 68): {
        "question": "①退屈する前に、時間は過ぎたとはどういうことか。",
        "options": [
            "漬物を漬ける季節はその準備がとても忙しかったので、 退屈するような暇はなかったということ。",
            "自動車や飛行機がなかった頃に比べると、今は退屈する前に目的地につくことができるということ。",
            "100 年前は何をするにも非常に長い時間が必要だったので、 人生で退屈する時間はなかったということ。",
            "かつて人々は時間のかかることをあえてしていたから、退屈するのは当たり前のことだったということ。"
        ],
        "answer": 2
    },
    ("2021_07.json", 69): {
        "question": "② 時間がむしろ負担になってくるのはなぜか。",
        "options": [
            "物事が便利になり、寿命も延びて、 使い方がわからない時間が増えるから。",
            "若いうちから30 年も40 年も先の人生の過ごし方を考えなければならないから。",
            "時間のかかることをあえてすることで、結果としてあわただしい人生になるから。",
            "ひとつのことを済ませるのに時間がかからなくなった分､ することが増えるから。"
        ],
        "answer": 0
    },
    ("2021_07.json", 72): {
        "question": "イーサさんは4 月17 日の講座に申し込んだ。キャンセル待ちになった場合、結果の連絡はいつまで待たなければならないか。",
        "options": ["4 月2 日", "4 月9 日", "4 月13 日", "4 月16 日"],
        "answer": 2
    },

    # 2021_12
    ("2021_12.json", 48): {
        "question": "【48】に入る最も適当なものはどれか。",
        "options": [
            "思えなかったまでだ",
            "思えなかったほどだ",
            "思えなかっただけだ",
            "思えなかったからだ"
        ],
        "answer": 3
    },
    ("2021_12.json", 70): {
        "question": "次の4 人は、スーパー森下で買い物を終えたところで、買った商品を自宅まで届けてほしいと考えている。この中で、店の宅配サービスを利用できるのは誰か。",
        "options": ["リーさん", "川口さん", "ハリスさん", "高橋さん"],
        "answer": 3
    },

    # 2022_07
    ("2022_07.json", 48): {
        "question": "【48】に入る最も適当なものはどれか。",
        "options": ["問題だろう", "問題である", "問題とのことだ", "問題ではないか"],
        "answer": 1
    },
    ("2022_07.json", 55): {
        "question": "このメールで問い合わせていることは何か。",
        "options": [
            "ミラ商会に、最初の予定より早く納品できるか。",
            "ミラ商会の希望する価格で、納品できるか。",
            "5 月 20 日に、ミラ商会に 80 本を納品できるか。",
            "今週中に、ミラ商会に 30 本を納品できるか。"
        ],
        "answer": 2
    },
    ("2022_07.json", 56): {
        "question": "筆者の考えに合うのはどれか。",
        "options": [
            "問題に取り組む経験を積むほど、問題に対処できるようになる。",
            "間題から逃げることも、問題の解決には必要である。",
            "人生で得をするために、難しい問題に積極的に取り組むべきだ。",
            "解決できたかどうかより、問題解決に取り組む態度が大切だ。"
        ],
        "answer": 0
    },

    # 2023_07
    ("2023_07.json", 70): {
        "question": "アニカさんは友達と3 人で一緒に、ハイキングに行くことにした。ハイキングのコースは、「お勧めコース」から選びたいと思っている。アニカさんは3 人の希望をメモに書いた。3 人の希望に最も合うコースはどれか。\nアニカさんのメモ\nテイエ...登山鉄道に乗りたい。\nサナ...「合計時間」が、2 時間までのものがいい。\nアニカ...スタートとゴールは違う場所にしたい。",
        "options": ["らくらくコース", "花を楽しむコース", "半周コース", "一周コース"],
        "answer": 1
    },
    ("2023_07.json", 71): {
        "question": "ダンさんは、10 月に会社の同僚15 人とガイドツアーを利用したいと思っている。申し込みにあたり気をつけなければならないこととして、合っているのはどれか。",
        "options": [
            "申し込みはツアーを希望する日の3 日前の午後6 時までに電話でする必要がある。",
            "ガイド料金は、どの「お勧めコース」を選ぶかによって変わる。",
            "申し込みはまとめてできるが、当日は複数のグループに分かれなければならない。",
            "出発時間は、午前8 時30 分から午前11 時までの間で指定する必要がある。"
        ],
        "answer": 2
    },

    # 2024_07
    ("2024_07.json", 38): {
        "question": "1896 年の第1 回オリンピックに参加した国と地域の数は14 だったが、2004 年には200 を超える（   ）。",
        "options": ["べきだった", "つもりだった", "ほかなかった", "までになった"],
        "answer": 3
    },
    ("2024_07.json", 53): {
        "question": "このお知らせで伝えたいことは何か。",
        "options": [
            "6 月23 日の午前2 時から4 時までは、インターネットで特急券が予約できない。",
            "6 月23 日の午前2 時から4 時までは、ホームページで時刻表や運賃表が見られない。",
            "6 月23 日の午前4 時以降インターネットで特急券が予約できるようになる。",
            "6 月23 日の午前4 時以降、ホームページで時刻表や運賃表が見られるようになる。"
        ],
        "answer": 0
    },
    ("2024_07.json", 71): {
        "question": "ローズさんは、動画コンテストに応募しようと考えている。動画は、インターネットで送りたい。ローズさんは、どうしなければならないか。",
        "options": [
            "5 月10 日までに応募情報を送信し、17 日までに動画を送信する。",
            "5 月10 日までに応募情報を送信し、24 日までに動画を送信する。",
            "5 月10 日までに応募情報と動画を送信する。",
            "5 月24 日までに応募情報と動画を送信する。"
        ],
        "answer": 1
    },

    # 2024_12
    ("2024_12.json", 48): {
        "question": "【48】に入る最も適当なものはどれか。",
        "options": ["一方", "そして", "例えば", "ただし"],
        "answer": 2
    },
    ("2024_12.json", 70): {
        "question": "カールさんは、同じ大学の友人と二人で北原ホテルに泊まりたいと考えている。ベッドがあり、お風呂がついている部屋を選ぶつもりだ。「朝食付きプラン」で日曜日に宿泊する予定だが、希望に合う部屋の一人分の料金はいくらになるか。",
        "options": [
            "7200 円",
            "7200 円に1100 円を加えた金額",
            "10500 円",
            "10500 円に1100 円を加えた金額"
        ],
        "answer": 2
    },

    # N1 Day07 & Day08 Mondai 4 用法
    ("day07.json", 20): {"question": "【センス】"},
    ("day07.json", 21): {"question": "【裁く】"},
    ("day07.json", 22): {"question": "【いきなり】"},
    ("day07.json", 23): {"question": "【幹事】"},
    ("day07.json", 24): {"question": "【タイミング】"},
    ("day07.json", 25): {"question": "【募る】"},
    ("day08.json", 20): {"question": "【がやがや】"},
    ("day08.json", 21): {"question": "【気配り】"},
    ("day08.json", 22): {"question": "【リモコン】"},
    ("day08.json", 23): {"question": "【渋る】"},
    ("day08.json", 24): {"question": "【ぎっしり】"},
    ("day08.json", 25): {"question": "【均一】"},
}

# ==============================================================================
# 2. CLEANING UTILITIES
# ==============================================================================
PAGE_NUM_PAT = re.compile(r'(?:(?<=\n)|^)\s*-\s*\d{1,3}\s*-\s*(?=(?:\n|$))')
STANDALONE_PAGE_LINE = re.compile(r'(?:(?<=\n)|^)\s*\d{1,3}\s*ページ(?:目)?\s*(?=(?:\n|$))')

def clean_watermarks_and_pages(text):
    if not isinstance(text, str) or not text:
        return text
    # Remove standalone page lines: "- 12 -" or "12 ページ"
    text = PAGE_NUM_PAT.sub('', text)
    text = STANDALONE_PAGE_LINE.sub('', text)
    # Remove standalone JLPT headers that might appear on their own line in passages
    text = re.sub(r'(?:(?<=\n)|^)\s*JLPT[・\s]*N[12][・\s]*\d{1,2}/\d{2,4}\s*(?=(?:\n|$))', '', text, flags=re.I)
    # Remove trailing/leading excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def clean_option(opt):
    if not isinstance(opt, str):
        return opt
    # Specific known leaked fragments in options
    if '店に自転車を取りに行く 田中さんへ' in opt:
        return '店に自転車を取りに行く'
    if '広場づくりに対する市民の評価' in opt and '（３）' in opt:
        return '広場づくりに対する市民の評価'
    if '花を買う 新幹線' in opt:
        return '花を買う'
    
    # Strip JLPT watermarks with dates
    opt = re.sub(r'\s*(?:\d+\s+)?JLPT[・\s]*N[12][・\s]*\d{1,2}/\d{2,4}(?:\s+\d+)?\s*$', '', opt, flags=re.I)
    # Strip N2 date watermarks like "N2 12/2020 31" or "N2 12/2022 29"
    opt = re.sub(r'\s*\bN2\s*\d{2,4}[/-]\d{1,2}(?:\s+\d+)?\s*$', '', opt, flags=re.I)
    # Strip trailing numbers leaked from page footers (e.g. "あさっての夜 22" -> "あさっての夜")
    opt = re.sub(r'\s+\d{1,2}\s*$', '', opt)
    
    return opt.strip()

# ==============================================================================
# 3. REPAIR & SYNC PIPELINE
# ==============================================================================
def repair_exam_file(file_path):
    fname = os.path.basename(file_path)
    base_name = fname.replace('n2_', '') # e.g. 2011_12.json
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    qs = data if isinstance(data, list) else data.get('questions', [])
    if not qs and isinstance(data, dict) and 'sections' in data:
        for s in data['sections']:
            qs.extend(s.get('questions', []))
            
    modified = False
    
    # 2025_12 Q69 passage fix (copy from Q67/Q68)
    if '2025_12' in fname:
        p_q67 = None
        for q in qs:
            if q.get('number') == 67:
                p_q67 = q.get('passage')
                break
        if p_q67:
            for q in qs:
                if q.get('number') == 69 and len(q.get('passage', '')) < 100:
                    q['passage'] = p_q67
                    modified = True

    for q in qs:
        num = q.get('number')
        
        # Check specific patches
        patch = EXAM_PATCHES.get((base_name, num))
        if patch:
            for k, v in patch.items():
                if q.get(k) != v:
                    q[k] = v
                    modified = True
                    
        # Clean question text
        old_q = q.get('question', '')
        if isinstance(old_q, str):
            clean_q = clean_watermarks_and_pages(old_q)
            if old_q != clean_q:
                q['question'] = clean_q
                modified = True
                
        # Clean passage text
        old_p = q.get('passage', '')
        if isinstance(old_p, str):
            clean_p = clean_watermarks_and_pages(old_p)
            if old_p != clean_p:
                q['passage'] = clean_p
                modified = True
                
        # Clean options
        opts = q.get('options', [])
        if isinstance(opts, list):
            new_opts = []
            for o in opts:
                c_o = clean_option(o)
                new_opts.append(c_o)
            if opts != new_opts:
                q['options'] = new_opts
                modified = True
                
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    return modified

def sync_data_directories():
    """Keep data/ and public/data/ 100% identical."""
    src_dirs = ['data/n1_20days', 'data/n2_exams']
    for s_dir in src_dirs:
        p_dir = os.path.join('public', s_dir)
        os.makedirs(p_dir, exist_ok=True)
        for f in glob.glob(f'{s_dir}/*.json'):
            target = os.path.join(p_dir, os.path.basename(f))
            shutil.copy2(f, target)

    # In data/n2_exams and public/data/n2_exams, sync duplicate named files:
    # 2011_12.json <-> n2_2011_12.json
    for base_dir in ['data/n2_exams', 'public/data/n2_exams']:
        for f in glob.glob(f'{base_dir}/20*.json'):
            fname = os.path.basename(f)
            mirror = os.path.join(base_dir, f'n2_{fname}')
            shutil.copy2(f, mirror)

# ==============================================================================
# 4. COMPREHENSIVE LINTER / AUDIT GATE
# ==============================================================================
WATERMARK_AUDIT_PATS = [
    re.compile(r'-\s*\d+\s*-'),                  # Page numbers like - 12 -
    re.compile(r'\bN2\s*\d{2,4}[/-]\d{1,2}\b', re.I), # N2 07/2025
    re.compile(r'JLPT[・\s]*N[12][・\s]*\d{1,2}/\d{2,4}', re.I), # JLPT・N2・12/2025
]

def audit_file(file_path):
    fname = os.path.basename(file_path)
    is_n1 = 'n1' in file_path.lower()
    is_n2 = 'n2' in file_path.lower()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    qs = data if isinstance(data, list) else data.get('questions', [])
    if not qs and isinstance(data, dict) and 'sections' in data:
        for s in data['sections']:
            qs.extend(s.get('questions', []))

    issues = []
    
    # 5. [LỖI SỐ LƯỢNG CÂU]
    if is_n1 and len(qs) != 45:
        issues.append({
            'code': 'LỖI SỐ LƯỢNG CÂU',
            'q_num': 0,
            'desc': f'N1 yêu cầu 45 câu/ngày nhưng file có {len(qs)} câu.'
        })
    elif is_n2 and len(qs) < 100:
        issues.append({
            'code': 'LỖI SỐ LƯỢNG CÂU',
            'q_num': 0,
            'desc': f'N2 thiếu câu: tổng chỉ có {len(qs)} câu (< 100 câu).'
        })

    for idx, q in enumerate(qs):
        q_num = q.get('number', idx + 1)
        q_text = str(q.get('question', '') or '').strip()
        passage = str(q.get('passage', '') or '').strip()
        opts = q.get('options', [])
        ans = q.get('answer')
        section = q.get('section', '')
        group = q.get('sectionGroup', '')

        # 1. [LỖI CÂU HỎI]
        # Allow vocabulary usage words (Mondai 6 / 用法) e.g. 【初期】, 遺跡, etc.
        is_vocab_usage = '用法' in section or '問題6' in section or (is_n1 and '問題4' in section) or (q_text.startswith('【') and q_text.endswith('】'))
        is_listening = 'listening' in group or '聴解' in section

        if not q_text:
            if not is_listening:
                issues.append({
                    'code': 'LỖI CÂU HỎI',
                    'q_num': q_num,
                    'desc': 'Trường question rỗng hoặc null.'
                })
        elif len(q_text) < 5 and not is_vocab_usage and not is_listening:
            issues.append({
                'code': 'LỖI CÂU HỎI',
                'q_num': q_num,
                'desc': f'Trường question quá ngắn ({len(q_text)} ký tự): "{q_text}"'
            })
        elif 'Câu hỏi ' in q_text and not is_listening:
            issues.append({
                'code': 'LỖI CÂU HỎI',
                'q_num': q_num,
                'desc': f'Trường question chứa placeholder chưa được bóc tách: "{q_text}"'
            })

        # 2. [LỖI ĐỌC HIỂU]
        is_dokkai_n2 = any(f'問題{m}' in section for m in [9, 10, 11, 12, 13, 14]) or '読解' in section or group == 'reading'
        is_dokkai_n1 = is_n1 and ('問題7' in section or '読解' in section)
        if (is_dokkai_n2 or is_dokkai_n1) and not is_listening:
            if not passage or len(passage) < 50:
                issues.append({
                    'code': 'LỖI ĐỌC HIỂU',
                    'q_num': q_num,
                    'desc': f'Phần đọc hiểu thiếu passage hoặc passage quá ngắn ({len(passage)} ký tự).'
                })

        # 3. [LỖI OPTIONS]
        is_choukai_m4 = '問題4' in section and is_listening
        expected_len = 3 if is_choukai_m4 else 4
        
        if not isinstance(opts, list) or len(opts) != expected_len:
            issues.append({
                'code': 'LỖI OPTIONS',
                'q_num': q_num,
                'desc': f'Số lượng options = {len(opts) if isinstance(opts, list) else 0}, yêu cầu {expected_len}.'
            })
        else:
            for o_idx, opt in enumerate(opts):
                opt_str = str(opt if opt is not None else '').strip()
                if not opt_str:
                    issues.append({
                        'code': 'LỖI OPTIONS',
                        'q_num': q_num,
                        'desc': f'Option #{o_idx + 1} bị rỗng hoặc null.'
                    })
                elif len(opt_str) > 150:
                    issues.append({
                        'code': 'LỖI OPTIONS',
                        'q_num': q_num,
                        'desc': f'Option #{o_idx + 1} dài bất thường ({len(opt_str)} ký tự): "{opt_str[:50]}..."'
                    })

        # 4. [LỖI ĐÁP ÁN]
        if ans is None or not isinstance(ans, int) or ans < 0 or (isinstance(opts, list) and ans >= len(opts)):
            issues.append({
                'code': 'LỖI ĐÁP ÁN',
                'q_num': q_num,
                'desc': f'Giá trị answer không hợp lệ: {ans} (options: {len(opts) if isinstance(opts, list) else 0})'
            })

        # 6. [LỖI RÁC VĂN BẢN]
        for pat in WATERMARK_AUDIT_PATS:
            # Check question
            if pat.search(q_text):
                issues.append({
                    'code': 'LỖI RÁC VĂN BẢN',
                    'q_num': q_num,
                    'desc': f'Question chứa rác ({pat.pattern}): "{q_text[:60]}"'
                })
            # Check passage (exclude phone numbers like 01-4321-5577)
            if pat.pattern == r'-\s*\d+\s*-':
                # Check with genuine page num pattern
                if PAGE_NUM_PAT.search(passage):
                    issues.append({
                        'code': 'LỖI RÁC VĂN BẢN',
                        'q_num': q_num,
                        'desc': f'Passage chứa số trang: "{passage[:60]}..."'
                    })
            else:
                if pat.search(passage):
                    issues.append({
                        'code': 'LỖI RÁC VĂN BẢN',
                        'q_num': q_num,
                        'desc': f'Passage chứa rác ({pat.pattern}): "{passage[:60]}..."'
                    })
            # Check options
            for o_idx, opt in enumerate(opts if isinstance(opts, list) else []):
                opt_str = str(opt if opt is not None else '')
                if pat.search(opt_str):
                    issues.append({
                        'code': 'LỖI RÁC VĂN BẢN',
                        'q_num': q_num,
                        'desc': f'Option #{o_idx + 1} chứa rác ({pat.pattern}): "{opt_str}"'
                    })

    return issues

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    print("=" * 80)
    print(" KOALA JLPT HUB - COMPREHENSIVE DATA LINTER & REPAIR GATE")
    print("=" * 80)
    
    # 1. Run repairs on all files in data/
    target_files = sorted(glob.glob('data/n1_20days/*.json')) + sorted(glob.glob('data/n2_exams/*.json'))
    
    repaired_count = 0
    for f in target_files:
        if 'index' in f or os.path.basename(f) == 'n2_exams.json':
            continue
        if repair_exam_file(f):
            repaired_count += 1
            
    print(f"[REPAIR] Successfully checked and repaired {repaired_count} files in data/.")
    
    # 2. Sync to public/data and mirror files
    sync_data_directories()
    print("[SYNC] Successfully synchronized data/ -> public/data/ and all mirror files.")
    
    # 3. Run audit on all files
    audit_files = sorted(glob.glob('data/n1_20days/*.json')) + [f for f in sorted(glob.glob('data/n2_exams/*.json')) if 'index' not in f and not os.path.basename(f).startswith('n2_')]
    
    print("\n" + "=" * 80)
    print(f" AUDIT SCAN REPORT ({len(audit_files)} Core Files)")
    print("=" * 80)
    print(f"{'FILE NAME':<25} | {'QUESTIONS':<10} | {'STATUS':<10} | {'ISSUES'}")
    print("-" * 80)
    
    total_issues = 0
    passed_files = 0
    
    for f in audit_files:
        fname = os.path.basename(f)
        with open(f, 'r', encoding='utf-8') as jf:
            d = json.load(jf)
        qs = d if isinstance(d, list) else d.get('questions', [])
        issues = audit_file(f)
        
        if not issues:
            passed_files += 1
            print(f"{fname:<25} | {len(qs):<10} | \033[92mPASS\033[0m       | 0 issues")
        else:
            total_issues += len(issues)
            print(f"{fname:<25} | {len(qs):<10} | \033[91mFAIL\033[0m       | {len(issues)} issues")
            for iss in issues[:3]:
                print(f"   -> [{iss['code']}] Q#{iss['q_num']}: {iss['desc']}")
            if len(issues) > 3:
                print(f"   ... and {len(issues) - 3} more issues")
                
    print("-" * 80)
    print(f"SUMMARY: {passed_files}/{len(audit_files)} files passed. Total issues: {total_issues}")
    
    if total_issues == 0:
        print("\n\033[92m>>> 100% DATA AUDIT PASSED! ALL CHECKS CLEAR. <<<\033[0m\n")
    else:
        print(f"\n\033[91m>>> AUDIT FAILED WITH {total_issues} REMAINING ISSUES. <<<\033[0m\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
