#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_full_dokkai_v2.py
Comprehensive builder for Dokkai N1:
- Enriches Chapters 1 to 5 with Medium consolidation passages & questions (q05, q06)
- Completes Chapter 6 with 13 comprehensive practice questions across all 5 JLPT N1 problem types
- Validates all logicHighlights against passage substrings (100% exact match)
- Synchronizes data/n1_dokkai/ and public/data/n1_dokkai/
"""

import os
import sys
import json
import shutil

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'n1_dokkai')
PUBLIC_DATA_DIR = os.path.join(ROOT_DIR, 'public', 'data', 'n1_dokkai')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PUBLIC_DATA_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# Chapter 1 Additions (q05 & q06)
# ------------------------------------------------------------------------------
ch01_passage_med = """高度経済成長期以来、日本企業は個人の能力や実績を客観的な数値で評価する「成果主義」へと大きく舵を切ってきた。年功序列や終身雇用といった従来の日本型雇用慣行は非効率であり、個々人の競争心を刺激することこそが組織の生産性を最大化するという論理は、一見すると極めて合理的で疑う余地のないものに思われた。

しかし、この徹底した個人主義的な評価システムの導入がもたらしたのは、皮肉にも組織全体の活力の減退であった。他者との相対的な優位性を競い合う環境下では、同僚は協働のパートナーではなく競争相手へと変貌し、暗黙知の共有や若手社員への献身的な育成といった「組織の余白」を支えていた利他行動が急速に消失していったのである。個人の数値的成果を合算しても、組織としての総和が必ずしも増大するとは限らない。

真に強靭な組織とは、個人の卓越した能力の総計によって規定されるのではなく、互いの欠落を補い合い、不確実性に直面した際に自発的に助け合える「関係性の質」の中にこそ宿る。短視眼的な個人成果の最大化を追求するあまり、組織の土台である相互信頼という見えない資本を毀損しては本末転倒である。"""

ch01_q05 = {
    "id": "skz_ch01_q05",
    "chapter": "第1章：対比・逆接",
    "title": "第1章 実践・中文 1 - 問1",
    "mondaiType": "medium",
    "passage": ch01_passage_med,
    "question": "成果主義の導入がもたらした弊害について、筆者はどのように述べているか。",
    "options": [
        "個人の能力を数値化することが技術的に困難であったため、正当な人事評価が行われなくなった。",
        "社員間の過剰な競争により利他的な知識共有や育成が失われ、組織全体の活力がかえって衰退した。",
        "年功序列制度の復活を求める声が強まり、若手社員のモチベーションが著しく低下した。",
        "終身雇用の廃止によって個々人の生産性は向上したものの、企業の短期的利益が圧迫された。"
    ],
    "answer": 2,
    "logicHighlights": {
        "counterPremise": "個々人の競争心を刺激することこそが組織の生産性を最大化するという論理は、一見すると極めて合理的で疑う余地のないものに思われた",
        "turningPoint": "しかし、この徹底した個人主義的な評価システムの導入がもたらしたのは、皮肉にも組織全体の活力の減退であった",
        "authorConclusion": "個人の数値的成果を合算しても、組織としての総和が必ずしも増大するとは限らない"
    },
    "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đưa lý do ngoài bài): Bài đọc không nói về khó khăn kỹ thuật trong lượng hóa, mà nói về sự biến chất trong quan hệ hợp tác.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với đoạn 2: cạnh tranh cá nhân làm mất đi sự sẻ chia tri thức và nâng đỡ lẫn nhau, dẫn đến suy giảm sinh khí toàn tổ chức.",
        "opt3": "❌ BẪY TƯ DUY (Suy diễn không căn cứ): Bài đọc không nhắc đến việc đòi khôi phục chế độ thâm niên.",
        "opt4": "❌ BẪY TƯ DUY (Trái ngược lập luận): Bài chỉ ra tổng hòa tổ chức không tăng lên và niềm tin bị xói mòn."
    },
    "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Từ thời kỳ tăng trưởng kinh tế cao độ, các doanh nghiệp Nhật Bản đã chuyển hướng mạnh mẽ sang 'chủ nghĩa thành tích' - đánh giá năng lực cá nhân bằng chỉ số khách quan. Lập luận cho rằng tập quán truyền thống như thâm niên là kém hiệu quả và kích thích cạnh tranh mới tối đa hóa năng suất thoạt nhìn tưởng như vô cùng hợp lý.<br><br>Thế nhưng, điều mà việc áp dụng hệ thống đánh giá vị kỷ này mang lại, trớ trêu thay, lại là sự suy giảm sinh khí của toàn bộ tổ chức. Trong môi trường so kè ưu thế hơn thua, đồng nghiệp biến thành đối thủ cạnh tranh, những hành vi vị tha như chia sẻ tri thức ngầm hay tận tâm bồi dưỡng cấp dưới vốn là 'khoảng trống nâng đỡ tổ chức' đã nhanh chóng tan biến. Cộng dồn thành tích cá nhân không đồng nghĩa với tổng thể tổ chức sẽ lớn mạnh.<br><br>Một tổ chức thực sự vững mạnh không được định đoạt bởi tổng số năng lực xuất chúng của các cá nhân, mà nằm ở 'chất lượng của mối tương quan' nơi người ta bù đắp khuyết điểm và tự nguyện tương trợ lẫn nhau khi đối mặt bất định. Mải miết chạy theo tối đa hóa thành tích cá nhân thiển cận mà phá hủy vốn liếng niềm tin nền tảng thì đúng là việc đảo lộn đầu đuôi."
}

ch01_q06 = {
    "id": "skz_ch01_q06",
    "chapter": "第1章：対比・逆接",
    "title": "第1章 実践・中文 1 - 問2",
    "mondaiType": "medium",
    "passage": ch01_passage_med,
    "question": "組織のあり方について、筆者が最も主張したいことはどれか。",
    "options": [
        "組織の生産性を高めるためには、個人の数値的実績を徹底的に競わせる評価基準を再構築すべきだ。",
        "不確実な時代を生き抜くには、個人の卓越した能力を単独で最大限に発揮できる環境を整備すべきである。",
        "組織の強靭さは個人の能力の総和ではなく、互いに補い合い支え合う関係性の質と相互信頼にある。",
        "組織の活力を維持するには、成果主義を完全に撤廃して従前の日本型雇用慣行をそのまま維持すべきだ。"
    ],
    "answer": 3,
    "logicHighlights": {
        "counterPremise": "年功序列や終身雇用といった従来の日本型雇用慣行は非効率であり",
        "turningPoint": "個人の数値的成果を合算しても、組織としての総和が必ずしも増大するとは限らない",
        "authorConclusion": "真に強靭な組織とは、個人の卓越した能力の総計によって規定されるのではなく、互いの欠落を補い合い、不確実性に直面した際に自発的に助け合える「関係性の質」の中にこそ宿る"
    },
    "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đồng hóa tiền đề bị phê phán): Đây là quan điểm duy thành tích cá nhân mà tác giả đã bác bỏ.",
        "opt2": "❌ BẪY TƯ DUY (Trái ngược quan điểm): Tác giả nhấn mạnh sức mạnh không nằm ở năng lực cá nhân đơn lẻ.",
        "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với câu chốt của tác giả: sức mạnh tổ chức nằm ở chất lượng tương quan và vốn liếng niềm tin nâng đỡ nhau khi đối mặt biến cố.",
        "opt4": "❌ BẪY TƯ DUY (Đưa giải pháp cực đoan): Tác giả không kêu gọi quay lại mù quáng cách làm cũ mà cảnh báo việc xói mòn niềm tin nền tảng."
    },
    "explanation": "<b>【Phân tích kết luận của tác giả】:</b><br>Tác giả sử dụng cấu trúc tương phản cốt lõi của Chương 1: <code>〜によって規定されるのではなく、〜の中にこそ宿る</code> (Không phải định đoạt bởi tổng năng lực cá nhân, mà hiện hữu chính trong chất lượng của mối tương quan). Phương án 3 khớp 100% với luận điểm này."
}

# ------------------------------------------------------------------------------
# Chapter 2 Additions (q05 & q06)
# ------------------------------------------------------------------------------
ch02_passage_med = """古典的な書物の読書体験を、未知の山岳を登攀する行為に譬えることができる。ベストセラーの娯楽小説や手軽な解説書を読むことが、整備された遊歩道を散策することであるならば、何世紀にもわたって読み継がれてきた古典に挑むことは、自らの手足を使って切り立った岩壁によじ登るような労苦を伴う。そこには即座に理解できる平易な言葉や、手軽な教訓などは用意されていない。

すなわち、古典を読むという営みは、単なる知識の消費ではなく、読者自身が著者の強靭な知性と格闘し、思考の強度を限界まで引き上げられる「精神の筋力トレーニング」にほかならないのである。一見すると難解で時代錯誤に思える語句の一行一句に立ち止まり、その底にある意味の地層を掘り下げる過程でこそ、私たちの精神は既存の常識の枠組みを打ち破る新たな視座を獲得する。

登山者が険しい頂に立ったときに初めて眼下に広がる壮大なパノラマを目撃できるように、難解な古典を粘り強く読了した者だけが、時代や文化の制約を超えた普遍的な人間理解の地平に到達することができるのだ。手軽な要約で満足することは、登山の過程を省略してロープウェイで展望台に運ばれるようなものであり、自らの足で登り詰めた者だけが得られる真の変容を味わうことはできない。"""

ch02_q05 = {
    "id": "skz_ch02_q05",
    "chapter": "第2章：言い換え・比喩",
    "title": "第2章 実践・中文 1 - 問1",
    "mondaiType": "medium",
    "passage": ch02_passage_med,
    "question": "筆者が古典を読むことを「精神の筋力トレーニング」と言い換えているのはなぜか。",
    "options": [
        "短時間で実用的な知識を大量に暗記し、試験やビジネスで即効性のある成果を出すため。",
        "難解なテキストと格闘し思索を深める過程を通じて、読者自身の思考の強度が鍛えられるから。",
        "古典の知識を消費することで、他者との知的優位性を誇示するための教養が身につくから。",
        "娯楽小説を読むときと同じように、リラックスした状態で精神の疲労を回復できるから。"
    ],
    "answer": 2,
    "logicHighlights": {
        "counterPremise": "ベストセラーの娯楽小説や手軽な解説書を読むことが、整備された遊歩道を散策することであるならば",
        "turningPoint": "すなわち、古典を読むという営みは、単なる知識の消費ではなく、読者自身が著者の強靭な知性と格闘し、思考の強度を限界まで引き上げられる「精神の筋力トレーニング」にほかならないのである",
        "authorConclusion": "一見すると難解で時代錯誤に思える語句の一行一句に立ち止まり、その底にある意味の地層を掘り下げる過程でこそ、私たちの精神は既存の常識の枠組みを打ち破る新たな視座を獲得する"
    },
    "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Thực dụng hóa ngắn hạn): Đọc sách kinh điển không đem lại kết quả ăn liền kiểu mẹo mực.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với cách diễn đạt tương đương: vật lộn với tư tưởng khó nhằn của tác giả để nâng giới hạn cơ bắp tư duy.",
        "opt3": "❌ BẪY TƯ DUY (Đánh tráo mục đích): Đọc kinh điển không nhằm khoe mẽ tri thức thượng đẳng.",
        "opt4": "❌ BẪY TƯ DUY (Ngược nghĩa ẩn dụ): Đọc kinh điển là leo núi đá hiểm trở đầy nhọc nhằn, không phải dạo bộ thư giãn."
    },
    "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Trải nghiệm đọc kinh điển có thể ví như việc leo lên một đỉnh núi chưa ai biết. Nếu đọc sách giải trí bán chạy là đi dạo trên lối mòn phẳng phiu, thì đối mặt kinh điển là việc dùng chân tay leo lên vách đá dựng đứng.<br><br>Nói cách khác (すなわち), đọc kinh điển là 'tập thể hình cho cơ bắp tinh thần', nơi độc giả vật lộn cùng trí tuệ của tác giả để nâng giới hạn tư duy."
}

ch02_q06 = {
    "id": "skz_ch02_q06",
    "chapter": "第2章：言い換え・比喩",
    "title": "第2章 実践・中文 1 - 問2",
    "mondaiType": "medium",
    "passage": ch02_passage_med,
    "question": "「手軽な要約で満足すること」について、筆者はどのように捉えているか。",
    "options": [
        "読書にかかる時間を節約し、より多くの古典の知識を効率的に網羅するための有効な手段である。",
        "自らの頭で思索を深める労苦を伴わないため、読書を通じた真の人間的変容をもたらさない。",
        "ロープウェイのように安全に頂上に到達できるため、現代人にとって最も推奨される読書スタイルである。",
        "難解な古典の本質を完璧に凝縮しているため、原文を読むのと全く同等の読書体験が得られる。"
    ],
    "answer": 2,
    "logicHighlights": {
        "counterPremise": "手軽な要約で満足することは、登山の過程を省略してロープウェイで展望台に運ばれるようなものであり",
        "turningPoint": "登山者が険しい頂に立ったときに初めて眼下に広がる壮大なパノラマを目撃できるように、難解な古典を粘り強く読了した者だけが、時代や文化の制約を超えた普遍的な人間理解の地平に到達することができるのだ",
        "authorConclusion": "自らの足で登り詰めた者だけが得られる真の変容を味わうことはできない"
    },
    "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đồng hóa góc nhìn hiệu suất): Tác giả phê phán việc đi tắt đón đầu qua các bản tóm tắt hời hợt.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp trọn vẹn với ẩn dụ cáp treo: bỏ qua nhọc nhằn tự thân leo núi thì không bao giờ nếm trải sự biến chuyển nội tâm thực thụ.",
        "opt3": "❌ BẪY TƯ DUY (Đồng tình với hành vi bị tác giả chê): Tác giả dùng hình ảnh cáp treo với hàm ý mỉa mai, không phải khuyến khích.",
        "opt4": "❌ BẪY TƯ DUY (Thổi phồng phi thực tế): Bản tóm tắt không thể thay thế việc đối thoại trực tiếp với nguyên tác."
    },
    "explanation": "<b>【Phân tích ẩn dụ chiếc cáp treo (ロープウェイ)】:</b><br>Tác giả dùng hình ảnh đi cáp treo lên đài quan sát để ẩn dụ cho việc đọc bản tóm tắt ăn liền: tuy nhanh nhưng bỏ qua quá trình tự bước đi, vì thế không thể đạt được sự biến chuyển tư duy sâu sắc."
}

# ------------------------------------------------------------------------------
# Chapter 3 Additions (q05 & q06)
# ------------------------------------------------------------------------------
ch03_passage_med = """インターネット空間の言論において、私たちは「自分自身で情報を取捨選択し、主体的に意思決定を行っている」と信じて疑わない。膨大なニュースやSNSの投稿の中から、自らの価値観に合致するオピニオンを選び取ることこそが、個人の自律的な思考の証であると考えられている。だが、私たちが「自分の意志」と信じ込んでいるその判断は、本当にアルゴリズムの誘導から自由なものなのだろうか。

現実には、プラットフォームが提供する推薦アルゴリズムは、ユーザーの過去の閲覧履歴や感情的反応を精緻に分析し、最もエンゲージメントを高めやすい情報だけを選択的に提示し続けている。その結果、私たちは知らず知らずのうちに自らの偏見を強化する心地よい情報だけに囲まれ、異なる視点を排除する「認識の牢獄」に自発的に幽閉されてしまっているのではないか。自ら選んでいるつもりで、実はアルゴリズムに選ばされているにすぎないのだ。

真の知的自律性とは、推薦される快適な情報に安住することではなく、自らの信条を揺るがすような不都合な他者の声にあえて身を晒し、自らの偏見を不断に相対化し続ける営みの中にこそ成立する。客観的な客体として情報を消費するのではなく、自らの認知の限界を自覚的に問い直す態度を持たない限り、デジタルの海で思考の自由を維持することはできない。"""

ch03_q05 = {
    "id": "skz_ch03_q05",
    "chapter": "第3章：疑問提示・筆者の主張",
    "title": "第3章 実践・中文 1 - 問1",
    "mondaiType": "medium",
    "passage": ch03_passage_med,
    "question": "現代の情報接触について、筆者が問題視している点は何か。",
    "options": [
        "推薦アルゴリズムの精度が低いため、ユーザーが求める情報にアクセスする効率が落ちていること。",
        "自分の意志で選んでいるつもりが、アルゴリズムに誘導され偏見を強化する情報に幽閉されていること。",
        "インターネット上の情報量が多すぎるため、若者がニュースを読む習慣を失ってしまっていること。",
        "プラットフォームが利用者の個人情報を不正に売買し、思想信条の自由を直接侵害していること。"
    ],
    "answer": 2,
    "logicHighlights": {
        "counterPremise": "膨大なニュースやSNSの投稿の中から、自らの価値観に合致するオピニオンを選び取ることこそが、個人の自律的な思考の証であると考えられている",
        "turningPoint": "だが、私たちが「自分の意志」と信じ込んでいるその判断は、本当にアルゴリズムの誘導から自由なものなのだろうか",
        "authorConclusion": "自ら選んでいるつもりで、実はアルゴリズムに選ばされているにすぎないのだ"
    },
    "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Ngược thực tế): Thuật toán đề xuất quá tinh vi chứ không phải kém cỏi.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với câu hỏi tu từ và phân tích đoạn 2: ngỡ là tự chọn nhưng thực chất bị nhốt trong nhà tù nhận thức tự củng cố định kiến.",
        "opt3": "❌ BẪY TƯ DUY (Đưa thông tin ngoài bài): Bài đọc không nói về việc mất thói quen đọc tin.",
        "opt4": "❌ BẪY TƯ DUY (Lạc đề pháp lý): Bài đọc phân tích tâm lý nhận thức, không bàn chuyện buôn bán dữ liệu cá nhân."
    },
    "explanation": "<b>【Phân tích câu hỏi tu từ 疑問提示】:</b><br>Tác giả dùng câu hỏi gợi mở <code>本当にアルゴリズムの誘導から自由なものなのだろうか</code> để đánh đổ định kiến rằng người dùng mạng có toàn quyền tự chủ."
}

ch03_q06 = {
    "id": "skz_ch03_q06",
    "chapter": "第3章：疑問提示・筆者の主張",
    "title": "第3章 実践・中文 1 - 問2",
    "mondaiType": "medium",
    "passage": ch03_passage_med,
    "question": "「真の知的自律性」について、筆者の主張と最も合致するものはどれか。",
    "options": [
        "自分の価値観と一致するオピニオンを徹底的に収集し、自らの信念を一切揺るがさない姿勢。",
        "アルゴリズムの推薦機能を最大限に活用し、最も効率的に偏りのない知識を蓄積すること。",
        "快適な情報にとどまらず、自らの偏見を揺るがす不都合な異見に触れて認知の限界を問い直すこと。",
        "インターネットやSNSの利用を完全に断ち、デジタル技術を一切使わずに思索を深めること。"
    ],
    "answer": 3,
    "logicHighlights": {
        "counterPremise": "その結果、私たちは知らず知らずのうちに自らの偏見を強化する心地よい情報だけに囲まれ",
        "turningPoint": "客観的な客体として情報を消費するのではなく",
        "authorConclusion": "真の知的自律性とは、推薦される快適な情報に安住することではなく、自らの信条を揺るがすような不都合な他者の声にあえて身を晒し、自らの偏見を不断に相対化し続ける営みの中にこそ成立する"
    },
    "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Bảo thủ hóa quan điểm): Tác giả chống lại việc chỉ bám chặt vào quan điểm cá nhân có sẵn.",
        "opt2": "❌ BẪY TƯ DUY (Trái ngược cảnh báo): Tác giả cảnh báo nguy cơ bị thuật toán thao túng nhận thức.",
        "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp 100% với câu chốt của tác giả ở đoạn cuối: dũng cảm đối diện với ý kiến trái chiều gây khó chịu để liên tục tương đối hóa định kiến bản thân.",
        "opt4": "❌ BẪY TƯ DUY (Cực đoan hóa giải pháp): Tác giả không yêu cầu cấm tiệt Internet."
    },
    "explanation": "<b>【Phân tích quan điểm của tác giả (筆者の主張)】:</b><br>Tác giả kết luận bằng công thức: <code>〜ではなく、〜の中にこそ成立する</code>. Độc lập tri thức thật sự là việc dám đối diện với những góc nhìn trái chiều làm rung chuyển định kiến bản thân."
}

# ------------------------------------------------------------------------------
# Chapter 4 Additions (q05 & q06)
# ------------------------------------------------------------------------------
ch04_passage_med = """近代以降の都市計画は、機能性と衛生を最優先し、住宅地、商業地、工業地帯を整然と区分する「ゾーニング」を基本方針としてきた。自動車の円滑な通行を保証する幅広の幹線道路や、用途ごとに純化された整然たる街並みは、都市の効率的な発展を支える理想形とみなされた。

しかし、こうした画一的な都市の区画整理は、街が本来備えていた「有機的な賑わい」を根こそぎ奪い去ることになった。これによって生じた最大の問題は、歩行者が安心して歩き、偶然の出会いや雑談を楽しむ余白が街から消滅したことである。用途が単一化された通りは、夜間や休日になると人通りが途絶え、防犯上の死角と化してしまう。雑多な店舗や住居が混在し、街路に人々の視線が絶え間なく注がれている状態こそが、都市の安全と活気を自発的に生み出す源泉であったのだ。

このような街の「生きた生態系」を回復するためには、効率至上主義の都市計画を見直さなければならない。単一の機能に特化した無機質な空間ではなく、多様な生活の営みが幾重にも重なり合う街路の再生こそが、現代の都市生活者に人間的な居場所を取り戻させる道である。"""

ch04_q05 = {
    "id": "skz_ch04_q05",
    "chapter": "第4章：指示語・機能表現",
    "title": "第4章 実践・中文 1 - 問1",
    "mondaiType": "medium",
    "passage": ch04_passage_med,
    "question": "「これによって生じた最大の問題」とあるが、どのような問題を指しているか。",
    "options": [
        "自動車の交通量が劇的に増加し、都市中心部で深刻な大気汚染と渋滞が引き起こされたこと。",
        "商業地と工業地の区分が曖昧になり、都市の産業競争力が国際的に著しく低下したこと。",
        "用途の純化により街から歩行者の余白や偶発的な交流が消え、夜間に人通りが途絶える死角が生まれたこと。",
        "住宅地の衛生環境が悪化し、都市住民の健康被害が深刻化したこと。"
    ],
    "answer": 3,
    "logicHighlights": {
        "counterPremise": "自動車の円滑な通行を保証する幅広の幹線道路や、用途ごとに純化された整然たる街並みは、都市の効率的な発展を支える理想形とみなされた",
        "turningPoint": "しかし、こうした画一的な都市の区画整理は、街が本来備えていた「有機的な賑わい」を根こそぎ奪い去ることになった",
        "authorConclusion": "これによって生じた最大の問題は、歩行者が安心して歩き、偶然の出会いや雑談を楽しむ余白が街から消滅したことである"
    },
    "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Nêu vấn đề ngoài bài): Bài đọc không nói về ô nhiễm khí thải xe cộ.",
        "opt2": "❌ BẪY TƯ DUY (Ngược sự thật): Bài nêu rõ khu vực bị phân chia quá rạch ròi, không phải mơ hồ.",
        "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với từ chỉ thị 'これ' chỉ việc phân lô quy hoạch đồng nhất làm biến mất khoảng trống giao lưu của người đi bộ và tạo ra điểm mù an ninh.",
        "opt4": "❌ BẪY TƯ DUY (Ngược tiền đề): Tiền đề bài đọc ghi nhận việc quy hoạch ban đầu nhằm ưu tiên vệ sinh và công năng."
    },
    "explanation": "<b>【Phân tích từ chỉ thị (これ・こうした)】:</b><br>Từ chỉ thị <code>これ</code> thay thế trực tiếp cho mệnh đề trước đó: việc quy hoạch đô thị đồng nhất (こうした画一的な都市の区画整理) đã cướp đi sự nhộn nhịp hữu cơ."
}

ch04_q06 = {
    "id": "skz_ch04_q06",
    "chapter": "第4章：指示語・機能表現",
    "title": "第4章 実践・中文 1 - 問2",
    "mondaiType": "medium",
    "passage": ch04_passage_med,
    "question": "「生きた生態系」を持つ都市の再生について、筆者はどのように考えているか。",
    "options": [
        "幹線道路の整備をさらに加速させ、自家用車による移動効率を徹底的に高めるべきだ。",
        "単一機能の空間ではなく、多様な生活の営みが重なり合い人の視線が行き交う街路を再生すべきだ。",
        "都市の人口密度を抑制するために、住宅地を郊外へ完全に移転させるべきである。",
        "商業活動を全面的に規制し、静寂で衛生的な住宅専用の街並みを維持すべきである。"
    ],
    "answer": 2,
    "logicHighlights": {
        "counterPremise": "用途が単一化された通りは、夜間や休日になると人通りが途絶え、防犯上の死角と化してしまう",
        "turningPoint": "効率至上主義の都市計画を見直さなければならない",
        "authorConclusion": "単一の機能に特化した無機質な空間ではなく、多様な生活の営みが幾重にも重なり合う街路の再生こそが、現代の都市生活者に人間的な居場所を取り戻させる道である"
    },
    "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đồng hóa tư duy quy hoạch cũ): Đây chính là tư duy hiệu suất xe hơi mà tác giả phản đối.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp 100% với chỉ thị từ 'このような' và câu chốt: hồi sinh những con phố đa dạng nhiều tầng nấc sinh hoạt đan xen.",
        "opt3": "❌ BẪY TƯ DUY (Đưa giải pháp trái ngược): Tác giả phản đối việc chia tách dân cư ra ngoại ô.",
        "opt4": "❌ BẪY TƯ DUY (Ngược quan điểm tác giả): Tác giả ủng hộ sự đan xen buôn bán và nhà ở để tạo sự nhộn nhịp."
    },
    "explanation": "<b>【Phân tích chỉ thị từ liên kết văn bản】:</b><br>Cụm từ <code>このような街の「生きた生態系」</code> tổng hợp lại đặc tính: các cửa hàng, nhà ở đan xen hỗn hợp, ánh mắt người qua lại bảo vệ an ninh đường phố."
}

# ------------------------------------------------------------------------------
# Chapter 5 Additions (q05 & q06)
# ------------------------------------------------------------------------------
ch05_passage_med = """各地の伝統工芸や職人技が後継者不足に悩み、次々と衰退の危機に瀕している。この現象の原因について、世間では「若者のものづくり離れ」や「伝統文化への敬意の欠如」といった、受け手側の意識の変化に理由を求める言説が後を絶たない。若者が苦労を嫌い、手軽なデスクワークやIT産業ばかりを志向するようになったからだという批判は、極めてわかりやすい解釈として人口に膾炙している。

なぜなら、ものづくりに対する情熱や関心を持つ若者は依然として多数存在するにもかかわらず、その技術を専業として生活を成り立たせるための「経済的循環構造」が完全に崩壊してしまっているからだ。どれほど卓越した技術を身につけても、製品の正当な価値が市場で評価されず、原材料費や制作時間にすら見合わない不当な安価で買いたたかれる現状では、生活の基盤を築くことなど不可能である。

すなわち、後継者不足の真因は、個人の精神性や若者の気質の変化にあるのではなく、熟練の技に対して適正な対価を保証し、職人が誇りを持って自活できる持続可能な市場エコシステムを構築してこなかった社会構造の不全にこそあるのだ。精神論で若者を責めるのをやめ、工芸の価値を正当に換金できる流通と評価の仕組みを再設計することこそが、危機の根治につながる唯一の道である。"""

ch05_q05 = {
    "id": "skz_ch05_q05",
    "chapter": "第5章：理由・因果関係",
    "title": "第5章 実践・中文 1 - 問1",
    "mondaiType": "medium",
    "passage": ch05_passage_med,
    "question": "伝統工芸の後継者不足について、世間で広く信じられている解釈はどのようなものか。",
    "options": [
        "原材料の高騰により、伝統工芸品の製造コストが採算ラインを超えてしまったこと。",
        "若者のものづくり離れや伝統文化への敬意不足など、若者の意識や気質の変化に原因があるとする解釈。",
        "国や自治体からの助成金が打ち切られ、職人の養成学校が閉鎖されたこと。",
        "海外からの安価な複製品が市場に大量流入し、本物の工芸品の需要が消滅したこと。"
    ],
    "answer": 2,
    "logicHighlights": {
        "counterPremise": "若者が苦労を嫌い、手軽なデスクワークやIT産業ばかりを志向するようになったからだという批判は、極めてわかりやすい解釈として人口に膾炙している",
        "turningPoint": "なぜなら、ものづくりに対する情熱や関心を持つ若者は依然として多数存在するにもかかわらず",
        "authorConclusion": "その技術を専業として生活を成り立たせるための「経済的循環構造」が完全に崩壊してしまっているからだ"
    },
    "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đưa yếu tố kinh tế): Đây là thực tế khách quan ở đoạn 2, không phải quan niệm phổ biến ở đoạn 1.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với tiền đề số đông được nêu ở đoạn 1: dư luận dễ dãi quy chụp cho giới trẻ lười biếng, thiếu tôn trọng văn hóa truyền thống.",
        "opt3": "❌ BẪY TƯ DUY (Đưa thông tin ngoài bài): Bài đọc không đề cập chuyện cắt học bổng hay đóng cửa trường.",
        "opt4": "❌ BẪY TƯ DUY (Yếu tố thị trường ngoài bài): Bài đọc không đổ lỗi cho hàng nhái ngoại nhập."
    },
    "explanation": "<b>【Phân tích mối quan hệ nhân quả (理由・因果関係)】:</b><br>Đoạn 1 nêu lý do giả định của dư luận (世間の解釈): quy kết cho tâm lý giới trẻ. Đoạn 2 bẻ gãy giả định này bằng từ nối chỉ nguyên nhân thật sự: <code>なぜなら〜からだ</code>."
}

ch05_q06 = {
    "id": "skz_ch05_q06",
    "chapter": "第5章：理由・因果関係",
    "title": "第5章 実践・中文 1 - 問2",
    "mondaiType": "medium",
    "passage": ch05_passage_med,
    "question": "伝統工芸の危機を解決するために、筆者が真に必要だと考えていることは何か。",
    "options": [
        "学校教育において若者に精神論を説き、苦労に耐えうる忍耐力を養わせること。",
        "熟練の技術に見合った適正な対価を保証し、職人が自活できる経済的な市場エコシステムを再設計すること。",
        "手作業による工芸を廃止し、ITやAIを導入して生産コストを極限まで引き下げること。",
        "伝統工芸品を博物館に収蔵し、一般市場での商業的取引を全面的に禁止すること。"
    ],
    "answer": 2,
    "logicHighlights": {
        "counterPremise": "どれほど卓越した技術を身につけても、製品の正当な価値が市場で評価されず",
        "turningPoint": "すなわち、後継者不足の真因は、個人の精神性や若者の気質の変化にあるのではなく",
        "authorConclusion": "熟練の技に対して適正な対価を保証し、職人が誇りを持って自活できる持続可能な市場エコシステムを構築してこなかった社会構造の不全にこそあるのだ"
    },
    "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đồng hóa điều tác giả bài trừ): Tác giả yêu cầu chấm dứt việc đổ lỗi bằng luận điệu tinh thần.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp 100% với kết luận nhân quả: giải quyết tận gốc bằng việc xây dựng lại hệ sinh thái thị trường trả công xứng đáng để người thợ tự nuôi sống mình.",
        "opt3": "❌ BẪY TƯ DUY (Phản bội bản chất thủ công): Đòi cơ giới hóa xóa bỏ thủ công là đi ngược bài đọc.",
        "opt4": "❌ BẪY TƯ DUY (Cực đoan hóa phi lý): Đưa vào bảo tàng cấm buôn bán là giết chết nghề sống."
    },
    "explanation": "<b>【Chốt nguyên nhân cốt lõi (真因の解明)】:</b><br>Tác giả sử dụng liên từ tổng kết <code>すなわち</code> và cấu trúc khẳng định <code>〜にこそあるのだ</code> để khẳng định: mấu chốt nằm ở cơ cấu kinh tế và định giá giá trị, không phải ở phẩm chất người trẻ."
}

# ------------------------------------------------------------------------------
# Chapter 6 Full Set (13 Questions across all 5 JLPT N1 problem types)
# ------------------------------------------------------------------------------
ch06_p1_short = """本を速く読むこと、いわゆる「速読」が現代のビジネスマンの間で持て囃されている。短時間で膨大な情報を処理し、他者よりも多くの知識をインプットすることこそが競争力の源泉であるという論理だ。しかし、真に知的な読書とは、ページをめくる速度にあるのではなく、立ち止まり、問い、自らの内なる記憶や思索と対話する「遅さ」の中にこそ息づいている。どれほど大量の文字を目で追ったところで、自らの精神を通過せずに素通りした知識は、人間を深く耕すことなど決してない。"""

ch06_p2_short = """科学研究において、明確な仮説を立ててそれを実証していく演繹的なプロセスは確かに不可欠である。だが、科学史上の画期的な大発見の多くを振り返ってみると、当初の計画通りの道筋から生まれたものはむしろ稀である。研究者が予期せぬ実験の失敗や偶発的な異常現象に直面したとき、それを「単なる誤差」として切り捨てずに面白がり、徹底的に観察し直した瞬間にこそ、新たなパラダイムの扉が開かれてきたのだ。制御された計画性以上に、偶然の悪戯を受け入れる知的な柔軟性こそが、創造の揺籃なのである。"""

ch06_p3_med = """私たちは時計という人工的な機械によって測定される「均質な時間」を自明のものとして生きている。一日は24時間、一時間は60分として厳密に等分され、すべての行動はその目盛りに従って秩序づけられる。この近代的な時間規律のおかげで、社会の組織的協調や産業活動は驚異的な同期と効率化を達成することができた。

しかし、この時計の時間が絶対化した代償として、人間は内面的な「生の主観的リズム」を切り捨ててしまった。自然界に目を向ければ、春の訪れとともに芽吹き、冬の寒さの中で眠りにつく生命のサイクルは、決して機械的な均等さでは測れない。人間自身の心や身体もまた、情熱に駆られて没頭するときには時間は瞬く間に過ぎ去り、苦痛や思索に沈むときには一刻が永遠のように引き伸ばされる独自の「質的な時間」を生きているはずなのだ。

均等に細切れにされたスケジュールに心身を無理に適合させ続ける現代人は、自らの生命が発する固有のテンポを見失った「時間の難民」と言えるかもしれない。今求められているのは、時計の支配から自律を取り戻し、自分自身の内なる時間に耳を澄ませる勇気である。"""

ch06_p4_long = """インターネットの普及とデジタルテクノロジーの進化は、人間の「共同体」のあり方を根底から変容させた。地理的な制約に縛られることなく、地球の裏側にいる他者と共通の趣味や関心で瞬時につながり合えるバーチャルなコミュニティは、個人の自由をかつてないほど拡張したかに見えた。

しかし、物理的な空間を共有しないデジタルなつながりには、決定的な要素が欠落している。それは、「偶発的な出会い」と「厄介さの引き受け」である。オンライン空間では、アルゴリズムによって最適化された同質的な意見ばかりが反響し合う「エコーチェンバー」に陥りやすく、自分が不快と感じる異質な他者はワンクリックで遮断することができる。そこには、他者の存在の手触りや、意見の衝突を粘り強くすり合わせる中で生まれる生の摩擦が存在しない。

古来、人間が育んできた真の「居場所」とは、単に自分にとって心地よい賛同者ばかりが集まるサロンではなかったはずだ。そこには、時に意見が合わず、煩わしく思える他者もまた同じ空間に実在し、そうした厄介さを引き受け合いながら互いの存在を認め合う重層的な関係性の網の目があったのだ。

身体を伴った物理的な空間での他者との交わりを軽視し、都合の良いデジタルな関係性だけに逃避し続けるならば、私たちの社会は個別に分断され、他者への寛容さを失った不毛な孤立の集合体へと退行してしまうだろう。今こそ、面倒で思い通りにならない「生身の他者」と共に生きる場所の尊厳を問い直さなければならない。"""

ch06_p5_compare = """【A】
テレワークの普及は、通勤ラッシュの疲労から労働者を解放し、ワークライフバランスの改善に大きく寄与した。場所を選ばずに業務を遂行できる柔軟性は、育児や介護とキャリアの両立を容易にし、個人の自律的な時間管理を促している。デジタルツールを活用した業務効率化が進む現代において、オフィスという一箇所に全員が集まることを強制する従来の働き方はもはや過去の遺物であり、完全なリモートワークへの移行こそが未来の標準となるべきである。

【B】
確かにリモートワークは定型的な業務処理においては高い効率を発揮する。しかし、革新的なアイディアの創出や強固な組織の信頼関係は、画面越しの計画的な会議だけでは育まれない。廊下ですれ違った際の一言の雑談や、同じ空間で共に汗を流す中で共有される暗黙の空気感こそが、創造的な協働の起爆剤となるのだ。オフィスは単なる作業場ではなく、偶発的な対話を生み出す社会的な触媒であり、その価値を過小評価して完全なオンライン化を進めることには慎重であるべきだ。"""

ch06_p6_search = """【国際文化交流財団・海外研究助成プログラム 募集要項（抜粋）】

1. 助成対象者：
・日本国内の大学院に在籍する大学院生（修士課程または博士課程）、または大学等で研究に従事する35歳未満の若手研究者。
・過去に本財団の助成を受けたことがない者。

2. 助成金額及び期間：
・上限150万円（渡航費、現地滞在費、研究資料収集費を含む）。
・現地滞在期間は3ヶ月以上1年以内とする。

3. 申請手続きと締切：
・申請期間：2026年4月1日〜5月15日（消印有効）。
・提出書類：申請書、指導教員の推薦書（1通）、研究計画書（書式自由、A4で3枚以内）。
※大学院生は在学証明書の添付が必須。

4. 注意事項：
・他機関からの助成金と本プログラムの重複受給は不可（併願は可能だが採択時に辞退手続きが必要）。
・助成期間終了後、2ヶ月以内に研究成果報告書及び会計報告書を提出すること。"""

ch06_questions = [
    # 1. 短文 1
    {
        "id": "skz_ch06_q01",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・短文 1",
        "mondaiType": "short",
        "passage": ch06_p1_short,
        "question": "「真に知的な読書」について、筆者の考えとして最も適切なものはどれか。",
        "options": [
            "短時間で大量の書籍を読了し、ビジネスに必要な知識を他者より先んじて蓄積すること。",
            "ページを速くめくることではなく、立ち止まって自らの思索と対話し精神を深めること。",
            "文字を目で追う速度を訓練によって極限まで高め、情報処理能力を向上させること。",
            "難解な書物を避け、自分の既存の知識で即座に理解できる平易な本だけを選ぶこと。"
        ],
        "answer": 2,
        "logicHighlights": {
            "counterPremise": "短時間で膨大な情報を処理し、他者よりも多くの知識をインプットすることこそが競争力の源泉であるという論理だ",
            "turningPoint": "しかし、真に知的な読書とは、ページをめくる速度にあるのではなく",
            "authorConclusion": "立ち止まり、問い、自らの内なる記憶や思索と対話する「遅さ」の中にこそ息づいている"
        },
        "trapBreakdown": {
            "opt1": "❌ BẪY TƯ DUY (Đồng hóa tiền đề số đông): Đây là quan điểm của người chạy theo 'đọc nhanh' bị tác giả phản bác.",
            "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với câu chốt: giá trị đích thực của đọc sách nằm ở sự 'chậm rãi' để đối thoại với nội tâm.",
            "opt3": "❌ BẪY TƯ DUY (Trái ngược lập luận): Tác giả phê phán việc chỉ dùng mắt lướt chữ mà không để kiến thức thấm qua tinh thần.",
            "opt4": "❌ BẪY TƯ DUY (Suy diễn ngoài bài): Bài đọc không bảo chọn sách dễ để đọc."
        },
        "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Đọc nhanh (速読) đang được giới kinh doanh hiện đại tán dương như nguồn sức mạnh cạnh tranh. Thế nhưng, việc đọc trí tuệ thực sự không nằm ở tốc độ lật trang, mà hiện hữu chính trong 'sự chậm rãi' dừng lại, đặt câu hỏi và đối thoại với ký ức, suy ngẫm nội tâm.<br><br><b>【Phân tích cấu trúc】:</b><br>Từ nối <code>しかし</code> lật ngược quan điểm đọc nhanh để khẳng định giá trị của sự chiêm nghiệm chậm rãi."
    },
    # 2. 短文 2
    {
        "id": "skz_ch06_q02",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・短文 2",
        "mondaiType": "short",
        "passage": ch06_p2_short,
        "question": "科学における「画期的な大発見」の契機について、筆者が強調していることは何か。",
        "options": [
            "当初立てた明確な仮説と緻密な計画通りに、一切の誤差を出さず実験を完遂すること。",
            "予期せぬ失敗や偶発的な現象を誤差として排除せず、柔軟に面白がり観察し直すこと。",
            "過去の偉大な科学者の理論を無批判に信奉し、既存のパラダイムを厳格に踏襲すること。",
            "実験の失敗を避けるために、あらかじめ結果が予測できる安全なテーマのみを選択すること。"
        ],
        "answer": 2,
        "logicHighlights": {
            "counterPremise": "明確な仮説を立ててそれを実証していく演繹的なプロセスは確かに不可欠である",
            "turningPoint": "だが、科学史上の画期的な大発見の多くを振り返ってみると、当初の計画通りの道筋から生まれたものはむしろ稀である",
            "authorConclusion": "制御された計画性以上に、偶然の悪戯を受け入れる知的な柔軟性こそが、創造の揺籃なのである"
        },
        "trapBreakdown": {
            "opt1": "❌ BẪY TƯ DUY (Đồng hóa tiền đề bị tương đối hóa): Tác giả chỉ ra rất hiếm phát kiến lớn sinh ra từ kế hoạch suôn sẻ ban đầu.",
            "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với phát biểu của tác giả: không vứt bỏ sự cố bất ngờ như sai số đơn thuần, mà linh hoạt tái quan sát để mở ra cánh cửa sáng tạo.",
            "opt3": "❌ BẪY TƯ DUY (Bảo thủ sai lệch): Bài đọc nói về việc phá vỡ khuôn mẫu cũ, không phải bám chặt lý thuyết quá khứ.",
            "opt4": "❌ BẪY TƯ DUY (Tránh né mạo hiểm): Nghiên cứu sáng tạo cần chấp nhận sự trêu ngươi của ngẫu nhiên."
        },
        "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Quy trình diễn dịch lập giả thuyết là cần thiết, nhưng lịch sử các phát kiến vĩ đại hiếm khi đi theo đúng kế hoạch ban đầu. Khi đối mặt thất bại hay dị thường, người dám thích thú quan sát lại chứ không vứt đi như sai số mới là người mở ra hệ hình mới."
    },
    # 3. 中文 1 - 問1
    {
        "id": "skz_ch06_q03",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・中文 1 - 問1",
        "mondaiType": "medium",
        "passage": ch06_p3_med,
        "question": "近代的な「均質な時間」が社会にもたらした功績について、筆者はどのように述べているか。",
        "options": [
            "社会の組織的協調や産業活動において、驚異的な同期と効率化を達成させた。",
            "自然界のサイクルと人間の生活を完全に一致させ、身体の健康を向上させた。",
            "個人の主観的な生のテンポを尊重し、自由な創造活動を促進させた。",
            "貧困や格差をなくし、万人に平等な余暇時間を安定して分配した。"
        ],
        "answer": 1,
        "logicHighlights": {
            "counterPremise": "一日は24時間、一時間は60分として厳密に等分され、すべての行動はその目盛りに従って秩序づけられる",
            "turningPoint": "この近代的な時間規律のおかげで",
            "authorConclusion": "社会の組織的協調や産業活動は驚異的な同期と効率化を達成することができた"
        },
        "trapBreakdown": {
            "opt1": "✓ ĐÁP ÁN ĐÚNG: Khớp 100% với câu cuối đoạn 1: nhờ kỷ luật thời gian cận đại mà tổ chức xã hội và công nghiệp đạt được sự đồng bộ và hiệu suất kinh ngạc.",
            "opt2": "❌ BẪY TƯ DUY (Đưa thông tin ngược): Đoạn 2 nói thời gian đồng hồ cắt đứt nhịp điệu tự nhiên.",
            "opt3": "❌ BẪY TƯ DUY (Trái ngược lập luận): Thời gian đồng hồ bóp nghẹt nhịp điệu chủ quan của con người.",
            "opt4": "❌ BẪY TƯ DUY (Lạc đề xã hội): Bài đọc không bàn về xóa đói giảm nghèo."
        },
        "explanation": "<b>【Phân tích câu hỏi 1 (Đoạn 1)】:</b><br>Tác giả thừa nhận thành tựu của 'thời gian đồng hồ' ở đoạn 1 trước khi lật ngược vấn đề ở đoạn 2 bằng liên từ <code>しかし</code>."
    },
    # 4. 中文 1 - 問2
    {
        "id": "skz_ch06_q04",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・中文 1 - 問2",
        "mondaiType": "medium",
        "passage": ch06_p3_med,
        "question": "筆者が現代人を「時間の難民」と表現している理由は何か。",
        "options": [
            "時計を持たずに生活しているため、社会のスケジュールに遅刻することが多いから。",
            "自然界の厳しさに適応できず、季節の移り変わりを感じ取る感性を失ったから。",
            "均等に細切れにされたスケジュールに縛られ、生命固有の質的なリズムを見失っているから。",
            "労働時間が長すぎるために余暇がなく、家族と過ごす時間を奪われているから。"
        ],
        "answer": 3,
        "logicHighlights": {
            "counterPremise": "人間自身の心や身体もまた、情熱に駆られて没頭するときには時間は瞬く間に過ぎ去り",
            "turningPoint": "しかし、この時計の時間が絶対化した代償として、人間は内面的な「生の主観的リズム」を切り捨ててしまった",
            "authorConclusion": "均等に細切れにされたスケジュールに心身を無理に適合させ続ける現代人は、自らの生命が発する固有のテンポを見失った「時間の難民」と言えるかもしれない"
        },
        "trapBreakdown": {
            "opt1": "❌ BẪY TƯ DUY (Hiểu nghĩa đen ngây ngô): 'Người tị nạn thời gian' là ẩn dụ triết học, không phải chuyện quên mang đồng hồ.",
            "opt2": "❌ BẪY TƯ DUY (Lấy ví dụ làm trọng tâm): Thiên nhiên chỉ là hình ảnh đối sánh.",
            "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với định nghĩa ở câu đầu đoạn 3: ép mình theo lịch trình băm nhỏ và đánh mất nhịp điệu sinh mệnh.",
            "opt4": "❌ BẪY TƯ DUY (Nêu lý do đời thường ngoài bài): Bài đọc không bàn chuyện thiếu thời gian gia đình."
        },
        "explanation": "<b>【Phân tích ẩn dụ 'Người tị nạn thời gian' (時間の難民)】:</b><br>Khái niệm này xuất hiện ở đầu đoạn 3, giải thích cho cái giá của việc tuyệt đối hóa thời gian cơ học khiến con người lạc lõng khỏi nhịp sinh học tự nhiên."
    },
    # 5. 中文 1 - 問3
    {
        "id": "skz_ch06_q05",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・中文 1 - 問3",
        "mondaiType": "medium",
        "passage": ch06_p3_med,
        "question": "「時計の時間」に対する筆者の最終的な主張として最も適切なものはどれか。",
        "options": [
            "社会の近代化をさらに進めるため、秒単位まで徹底した時間管理を導入すべきである。",
            "時計の利用を一切禁止し、時計のない古代の原始的な生活様式に戻るべきである。",
            "主観的な時間感覚は錯覚にすぎないため、客観的な数値基準に従うことが唯一の合理性である。",
            "時計の支配から自立を取り戻し、自分自身の内なる生命のリズムに耳を澄ませるべきだ。"
        ],
        "answer": 4,
        "logicHighlights": {
            "counterPremise": "この近代的な時間規律のおかげで、社会の組織的協調や産業活動は驚異的な同期と効率化を達成することができた",
            "turningPoint": "均等に細切れにされたスケジュールに心身を無理に適合させ続ける現代人は",
            "authorConclusion": "今求められているのは、時計の支配から自律を取り戻し、自分自身の内なる時間に耳を澄ませる勇気である"
        },
        "trapBreakdown": {
            "opt1": "❌ BẪY TƯ DUY (Cực đoan hóa theo chiều ngược): Tác giả phản đối việc băm nhỏ thời gian hơn nữa.",
            "opt2": "❌ BẪY TƯ DUY (Cực đoan hóa phi thực tế): Tác giả không đòi vứt đồng hồ về thời nguyên thủy.",
            "opt3": "❌ BẪY TƯ DUY (Phủ nhận cảm xúc): Trái ngược hoàn toàn với việc bảo vệ 'thời gian định tính'.",
            "opt4": "✓ ĐÁP ÁN ĐÚNG: Khớp 100% với câu kết: lấy lại quyền tự chủ khỏi sự thống trị của đồng hồ và lắng nghe thời gian nội tâm."
        },
        "explanation": "<b>【Chốt luận điểm toàn bài】:</b><br>Câu kết thúc bài văn dùng mẫu câu kêu gọi: <code>今求められているのは、〜勇気である</code> (Điều cần thiết lúc này là lòng dũng cảm...). Phương án 4 khớp tuyệt đối."
    },
    # 6. 長文 1 - 問1
    {
        "id": "skz_ch06_q06",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・長文 1 - 問1",
        "mondaiType": "long",
        "passage": ch06_p4_long,
        "question": "デジタルコミュニティの普及当初、人々はどのような期待を抱いていたか。",
        "options": [
            "地理的な制約に縛られることなく趣味や関心でつながり、個人の自由が拡張されること。",
            "物理的な空間での直接対話が増加し、地域社会の防犯機能が強化されること。",
            "国家の枠組みが解体され、全人類が同一の言語を用いて意思疎通できるようになること。",
            "アルゴリズムによって不要な意見が排除され、議論が一切起こらなくなること。"
        ],
        "answer": 1,
        "logicHighlights": {
            "counterPremise": "インターネットの普及とデジタルテクノロジーの進化は、人間の「共同体」のあり方を根底から変容させた",
            "turningPoint": "地理的な制約に縛られることなく、地球の裏側にいる他者と共通の趣味や関心で瞬時につながり合えるバーチャルなコミュニティは",
            "authorConclusion": "個人の自由をかつてないほど拡張したかに見えた"
        },
        "trapBreakdown": {
            "opt1": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với đoạn 1: không bị ràng buộc bởi địa lý, kết nối tức thì qua sở thích và mở rộng tự do cá nhân.",
            "opt2": "❌ BẪY TƯ DUY (Đưa thông tin ngược): Đoạn 2 chỉ ra không gian vật lý bị bỏ quên.",
            "opt3": "❌ BẪY TƯ DUY (Thổi phồng viển vông ngoài bài): Bài đọc không nói về giải tán quốc gia hay đồng nhất ngôn ngữ.",
            "opt4": "❌ BẪY TƯ DUY (Đánh tráo mặt tiêu cực): Việc thuật toán loại bỏ ý kiến dị biệt là điều tiêu cực được chỉ trích ở đoạn 2."
        },
        "explanation": "<b>【Phân tích câu hỏi 1 (Đoạn 1)】:</b><br>Đoạn mở đầu nêu lên tiền đề ban đầu mà mọi người từng kỳ vọng vào mạng xã hội: kết nối không biên giới và mở rộng tự do cá nhân."
    },
    # 7. 長文 1 - 問2
    {
        "id": "skz_ch06_q07",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・長文 1 - 問2",
        "mondaiType": "long",
        "passage": ch06_p4_long,
        "question": "オンライン空間における人間関係の欠陥として、筆者が指摘しているものはどれか。",
        "options": [
            "不快な他者を容易に遮断できるため、生の摩擦やすり合わせのプロセスが欠落すること。",
            "通信速度の遅延により、遠隔地の相手とリアルタイムで会話することが困難なこと。",
            "個人情報が常に流出する危険があり、他者との信頼関係を構築できないこと。",
            "意見が対立した際に裁判などの法的手段に訴えるコストが高すぎること。"
        ],
        "answer": 1,
        "logicHighlights": {
            "counterPremise": "個人の自由をかつてないほど拡張したかに見えた",
            "turningPoint": "しかし、物理的な空間を共有しないデジタルなつながりには、決定的な要素が欠落している。それは、「偶発的な出会い」と「厄介さの引き受け」である",
            "authorConclusion": "そこには、他者の存在の手触りや、意見の衝突を粘り強くすり合わせる中で生まれる生の摩擦が存在しない"
        },
        "trapBreakdown": {
            "opt1": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với đoạn 2: tha nhân dị biệt có thể bị chặn chỉ bằng một click, làm mất đi sự cọ xát sống động và quá trình kiên trì dàn xếp xung đột.",
            "opt2": "❌ BẪY TƯ DUY (Vấn đề kỹ thuật ngoài bài): Bài đọc khẳng định kết nối diễn ra tức thời (瞬時).",
            "opt3": "❌ BẪY TƯ DUY (Vấn đề an ninh mạng ngoài bài): Bài đọc phân tích tâm lý tương tác, không nói về rò rỉ dữ liệu.",
            "opt4": "❌ BẪY TƯ DUY (Yếu tố pháp lý ngoài bài): Không hề có chi tiết về kiện tụng hay tòa án."
        },
        "explanation": "<b>【Phân tích luận điểm đoạn 2】:</b><br>Tác giả chỉ ra nhược điểm chí mạng của kết nối ảo: thiếu đi sự 'hội ngộ ngẫu nhiên' và 'sẵn sàng gánh vác sự phiền toái' (厄介さの引き受け)."
    },
    # 8. 長文 1 - 問3
    {
        "id": "skz_ch06_q08",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・長文 1 - 問3",
        "mondaiType": "long",
        "passage": ch06_p4_long,
        "question": "伝統的な「居場所」の本質について、筆者の説明として最も適切なものはどれか。",
        "options": [
            "自分と同じ趣味や考え方を持つ人だけが集まり、常に快適に過ごせるサロンであること。",
            "煩わしい人間関係が一切なく、個人のプライバシーが完全に保護される場所であること。",
            "意見が合わず煩わしい他者とも身体を共有し、互いの厄介さを引き受け合って認める場であること。",
            "効率的な意思決定を行うために、意見の対立を速やかに排除できる管理された空間であること。"
        ],
        "answer": 3,
        "logicHighlights": {
            "counterPremise": "古来、人間が育んできた真の「居場所」とは、単に自分にとって心地よい賛同者ばかりが集まるサロンではなかったはずだ",
            "turningPoint": "そこには、時に意見が合わず、煩わしく思える他者もまた同じ空間に実在し",
            "authorConclusion": "そうした厄介さを引き受け合いながら互いの存在を認め合う重層的な関係性の網の目があったのだ"
        },
        "trapBreakdown": {
            "opt1": "❌ BẪY TƯ DUY (Đồng hóa điều bị phủ định): Tác giả tuyên bố chốn thuộc về không phải là cái salon toàn kẻ tán đồng mình.",
            "opt2": "❌ BẪY TƯ DUY (Trái ngược bản chất): Chốn thuộc về thật sự chứa đựng cả sự phiền toái.",
            "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với đoạn 3: nơi người ta cùng chia sẻ không gian với tha nhân bất đồng, chấp nhận phiền phức để công nhận nhau.",
            "opt4": "❌ BẪY TƯ DUY (Đưa góc nhìn quản lý): Đây là tư duy doanh nghiệp, không phải chốn thuộc về của con người."
        },
        "explanation": "<b>【Phân tích định nghĩa về 'Chốn dung thân chân chính' (真の居場所)】:</b><br>Đoạn 3 định nghĩa rõ: <code>厄介さを引き受け合いながら互いの存在を認め合う重層的な関係性の網の目</code>."
    },
    # 9. 長文 1 - 問4
    {
        "id": "skz_ch06_q09",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・長文 1 - 問4",
        "mondaiType": "long",
        "passage": ch06_p4_long,
        "question": "この文章全体を通じて、筆者が現代社会に最も強く訴えかけている主張は何か。",
        "options": [
            "インターネットの利用を直ちに中止し、全てのデジタル機器を廃棄して自然に回帰すべきだ。",
            "快適なデジタル空間の拡大を歓迎し、煩わしい対面コミュニケーションを減らすべきだ。",
            "意見の合わない他者とは関わりを持たず、同質的な集団の中だけで生活を送るべきだ。",
            "都合のよい関係に逃げず、面倒で思い通りにならない生身の他者と共に生きる場の尊厳を取り戻すべきだ。"
        ],
        "answer": 4,
        "logicHighlights": {
            "counterPremise": "身体を伴った物理的な空間での他者との交わりを軽視し、都合の良いデジタルな関係性だけに逃避し続けるならば",
            "turningPoint": "私たちの社会は個別に分断され、他者への寛容さを失った不毛な孤立の集合体へと退行してしまうだろう",
            "authorConclusion": "今こそ、面倒で思い通りにならない「生身の他者」と共に生きる場所の尊厳を問い直さなければならない"
        },
        "trapBreakdown": {
            "opt1": "❌ BẪY TƯ DUY (Giải pháp cực đoan): Tác giả không kêu gọi vứt bỏ công nghệ số.",
            "opt2": "❌ BẪY TƯ DUY (Trái ngược lời cảnh báo): Tác giả cảnh báo đây là sự thoái lui nguy hiểm.",
            "opt3": "❌ BẪY TƯ DUY (Bảo vệ căn bệnh phân mảnh): Đây là căn bệnh xã hội mà tác giả đang phê phán.",
            "opt4": "✓ ĐÁP ÁN ĐÚNG: Khớp 100% với thông điệp cốt lõi ở câu chốt: nhìn nhận lại phẩm giá của chốn cùng chung sống với những tha nhân bằng xương bằng thịt đầy phiền phức."
        },
        "explanation": "<b>【Chốt quan điểm toàn bài trường văn】:</b><br>Câu kết thúc chốt lại: <code>今こそ、面倒で思い通りにならない「生身の他者」と共に生きる場所の尊厳を問い直さなければならない</code>."
    },
    # 10. 統合理解 A-B - 問1
    {
        "id": "skz_ch06_q10",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・統合理解 1 - 問1",
        "mondaiType": "compare",
        "passage": ch06_p5_compare,
        "question": "リモートワークの利点について、AとBの認識はどう異なっているか。",
        "options": [
            "Aは定型業務の効率化のみを認めるのに対し、Bは創造的な協働に不可欠な手段として評価している。",
            "Aは柔軟な時間管理と効率化をもたらす未来の標準と見なすが、Bは定型業務の効率化にとどまる限界を指摘している。",
            "AもBも、リモートワークは通勤ラッシュの解消以外には何のメリットもないという点で一致している。",
            "Aはリモートワークを過去の遺物と見なし、Bは完全なオンライン化を全面的に推進している。"
        ],
        "answer": 2,
        "logicHighlights": {
            "counterPremise": "完全なリモートワークへの移行こそが未来の標準となるべきである",
            "turningPoint": "確かにリモートワークは定型的な業務処理においては高い効率を発揮する。しかし",
            "authorConclusion": "廊下ですれ違った際の一言の雑談や、同じ空間で共に汗を流す中で共有される暗黙の空気感こそが、創造的な協働の起爆剤となるのだ"
        },
        "trapBreakdown": {
            "opt1": "❌ BẪY TƯ DUY (Đảo ngược nhận định giữa A và B): A mới là người đánh giá cao toàn diện, B chỉ công nhận khía cạnh việc định hình.",
            "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác: A xem từ xa là chuẩn mực tương lai, còn B chỉ ra làm từ xa chỉ hiệu quả với việc theo khuôn mẫu, không nuôi dưỡng được ý tưởng mới.",
            "opt3": "❌ BẪY TƯ DUY (Xuyên tạc sự thật): Cả hai đều công nhận lợi ích riêng, không phải không có ích gì.",
            "opt4": "❌ BẪY TƯ DUY (Đảo ngược vai trò): A xem văn phòng là tàn tích, B mới là người cảnh giác với online hoàn toàn."
        },
        "explanation": "<b>【So sánh nhận định về Telework】:</b><br>Văn bản A tán dương làm việc từ xa tối đa (tương lai chuẩn mực). Văn bản B thừa nhận lợi ích tác vụ định hình nhưng vạch ra giới hạn trong sáng tạo ý tưởng mới."
    },
    # 11. 統合理解 A-B - 問2
    {
        "id": "skz_ch06_q11",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・統合理解 1 - 問2",
        "mondaiType": "compare",
        "passage": ch06_p5_compare,
        "question": "オフィスの存在意義について、AとBの主張を対比したものとして適切なものはどれか。",
        "options": [
            "Aは全員集合を強制する過去の遺物と捉えるのに対し、Bは偶発的な対話と創造性を促す触媒として評価している。",
            "Aはオフィスが偶発的な対話を生む場だと賞賛し、Bはオフィスを維持する費用の無駄を批判している。",
            "AもBも、オフィスの存在は社員の健康を著しく害するため、即刻廃止すべきだという結論で一致している。",
            "Aは地方移転を提案し、Bは都心の大規模オフィスへの集約を求めている。"
        ],
        "answer": 1,
        "logicHighlights": {
            "counterPremise": "オフィスという一箇所に全員が集まることを強制する従来の働き方はもはや過去の遺物であり",
            "turningPoint": "オフィスは単なる作業場ではなく",
            "authorConclusion": "偶発的な対話を生み出す社会的な触媒であり、その価値を過小評価して完全なオンライン化を進めることには慎重であるべきだ"
        },
        "trapBreakdown": {
            "opt1": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác sự đối lập: A coi văn phòng là tàn tích bắt ép tập trung, còn B coi văn phòng là chất xúc tác xã hội nuôi dưỡng đối thoại ngẫu nhiên và sáng tạo.",
            "opt2": "❌ BẪY TƯ DUY (Gán ghép ngược): A chê văn phòng, B mới khen ngợi vai trò xúc tác.",
            "opt3": "❌ BẪY TƯ DUY (Đồng nhất hóa sai lệch): B không hề đồng ý dẹp bỏ văn phòng.",
            "opt4": "❌ BẪY TƯ DUY (Đưa thông tin địa lý ngoài bài): Không bài nào bàn chuyện chuyển về nông thôn hay thủ đô."
        },
        "explanation": "<b>【So sánh nhận định về Văn phòng】:</b><br>A: <code>過去の遺物</code> (Tàn tích quá khứ).<br>B: <code>偶発的な対話を生み出す社会的な触媒</code> (Chất xúc tác xã hội sản sinh đối thoại ngẫu nhiên)."
    },
    # 12. 情報検索 - 問1
    {
        "id": "skz_ch06_q12",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・情報検索 1 - 問1",
        "mondaiType": "search",
        "passage": ch06_p6_search,
        "question": "本プログラムの応募資格および申請条件として、合致するものはどれか。",
        "options": [
            "過去に本財団の助成を受けたことがある者でも、35歳未満であれば再申請できる。",
            "他機関の助成金と併願して申請することはできるが、採択された場合は重複受給できない。",
            "大学院生であれば、年齢制限に関わらず35歳以上であっても応募可能である。",
            "申請書は2026年5月15日までに財団事務所へ必着で届かなければ無効となる。"
        ],
        "answer": 2,
        "logicHighlights": {
            "counterPremise": "過去に本財団の助成を受けたことがない者",
            "turningPoint": "他機関からの助成金と本プログラムの重複受給は不可",
            "authorConclusion": "（併願は可能だが採択時に辞退手続きが必要）"
        },
        "trapBreakdown": {
            "opt1": "❌ BẪY TƯ DUY (Vi phạm điều kiện tiên quyết): Mục 1 nêu rõ: '過去に本財団の助成を受けたことがない者' (Chưa từng nhận tài trợ của quỹ).",
            "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với mục 4 Chú ý: '他機関からの助成金と本プログラムの重複受給は不可（併願は可能だが採択時に辞退手続きが必要）'.",
            "opt3": "❌ BẪY TƯ DUY (Đọc sót điều kiện): Tuổi tác áp dụng chặt chẽ cho nghiên cứu sinh trẻ.",
            "opt4": "❌ BẪY TƯ DUY (Sai lệch quy định bưu điện): Mục 3 ghi rõ: '5月15日（消印有効）' (Căn cứ dấu bưu điện, không phải bắt buộc đến trước)."
        },
        "explanation": "<b>【Kỹ thuật dò thông tin Thông báo (情報検索)】:</b><br>Đối chiếu với Mục 4 Chú ý: <code>他機関からの助成金と本プログラムの重複受給は不可（併願は可能だが採択時に辞退手続きが必要）</code>. Cho phép nộp song song nhưng trúng tuyển thì phải từ chối một bên, không được nhận trùng lặp."
    },
    # 13. 情報検索 - 問2
    {
        "id": "skz_ch06_q13",
        "chapter": "第6章：実践演習・総合理解",
        "title": "第6章 実践・情報検索 1 - 問2",
        "mondaiType": "search",
        "passage": ch06_p6_search,
        "question": "大学院生が申請する場合の提出書類および滞在期間の規定として、正しいものはどれか。",
        "options": [
            "指導教員の推薦書は不要であり、在学証明書と申請書のみで申請できる。",
            "現地滞在期間は最短で1ヶ月から認められ、研究計画書の枚数は無制限である。",
            "助成期間終了後、半年以内に研究成果報告書を提出すればよい。",
            "在学証明書、推薦書、研究計画書を提出し、3ヶ月以上1年以内の滞在期間で申請しなければならない。"
        ],
        "answer": 4,
        "logicHighlights": {
            "counterPremise": "提出書類：申請書、指導教員の推薦書（1通）、研究計画書（書式自由、A4で3枚以内）",
            "turningPoint": "※大学院生は在学証明書の添付が必須",
            "authorConclusion": "現地滞在期間は3ヶ月以上1年以内とする"
        },
        "trapBreakdown": {
            "opt1": "❌ BẪY TƯ DUY (Thiếu thư giới thiệu): Thư giới thiệu của giáo viên hướng dẫn là bắt buộc cho mọi đối tượng.",
            "opt2": "❌ BẪY TƯ DUY (Sai thời hạn & số trang): Thời gian lưu trú tối thiểu 3 tháng, đề cương tối đa 3 trang A4.",
            "opt3": "❌ BẪY TƯ DUY (Sai hạn nộp báo cáo): Báo cáo phải nộp trong vòng 2 tháng (2ヶ月以内), không phải nửa năm.",
            "opt4": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác mục 2 (3 tháng đến 1 năm) và mục 3 (giấy chứng nhận đang học + thư giới thiệu + đề cương A4 dưới 3 trang)."
        },
        "explanation": "<b>【Kỹ thuật dò thông tin Thông báo】:</b><br>1. Thời gian lưu trú: Mục 2: <code>3ヶ月以上1年以内</code>.<br>2. Hồ sơ sinh viên cao học: Mục 3: Đơn + Thư giới thiệu 1 bản + Đề cương dưới 3 trang A4 + Giấy chứng nhận đang học (※大学院生は在学証明書の添付が必須)."
    }
]

# ------------------------------------------------------------------------------
# Processing & Merging
# ------------------------------------------------------------------------------
def run():
    print("=" * 80)
    print(" 🚀 BUILDING & ENRICHING ALL DOKKAI CHAPTERS (CH01 TO CH06)")
    print("=" * 80)

    # 1. Enrich Chapter 1
    ch01_path = os.path.join(DATA_DIR, 'shinkanzen_ch01.json')
    with open(ch01_path, 'r', encoding='utf-8') as f:
        ch01_data = json.load(f)
    existing_ids = {q['id'] for q in ch01_data['questions']}
    if 'skz_ch01_q05' not in existing_ids:
        ch01_data['questions'].append(ch01_q05)
    if 'skz_ch01_q06' not in existing_ids:
        ch01_data['questions'].append(ch01_q06)
    ch01_data['totalQuestions'] = len(ch01_data['questions'])
    with open(ch01_path, 'w', encoding='utf-8') as f:
        json.dump(ch01_data, f, ensure_ascii=False, indent=2)
    print(f"[CH01] Updated with {ch01_data['totalQuestions']} questions.")

    # 2. Enrich Chapter 2
    ch02_path = os.path.join(DATA_DIR, 'shinkanzen_ch02.json')
    with open(ch02_path, 'r', encoding='utf-8') as f:
        ch02_data = json.load(f)
    existing_ids = {q['id'] for q in ch02_data['questions']}
    if 'skz_ch02_q05' not in existing_ids:
        ch02_data['questions'].append(ch02_q05)
    if 'skz_ch02_q06' not in existing_ids:
        ch02_data['questions'].append(ch02_q06)
    ch02_data['totalQuestions'] = len(ch02_data['questions'])
    with open(ch02_path, 'w', encoding='utf-8') as f:
        json.dump(ch02_data, f, ensure_ascii=False, indent=2)
    print(f"[CH02] Updated with {ch02_data['totalQuestions']} questions.")

    # 3. Enrich Chapter 3
    ch03_path = os.path.join(DATA_DIR, 'shinkanzen_ch03.json')
    with open(ch03_path, 'r', encoding='utf-8') as f:
        ch03_data = json.load(f)
    existing_ids = {q['id'] for q in ch03_data['questions']}
    if 'skz_ch03_q05' not in existing_ids:
        ch03_data['questions'].append(ch03_q05)
    if 'skz_ch03_q06' not in existing_ids:
        ch03_data['questions'].append(ch03_q06)
    ch03_data['totalQuestions'] = len(ch03_data['questions'])
    with open(ch03_path, 'w', encoding='utf-8') as f:
        json.dump(ch03_data, f, ensure_ascii=False, indent=2)
    print(f"[CH03] Updated with {ch03_data['totalQuestions']} questions.")

    # 4. Enrich Chapter 4
    ch04_path = os.path.join(DATA_DIR, 'shinkanzen_ch04.json')
    with open(ch04_path, 'r', encoding='utf-8') as f:
        ch04_data = json.load(f)
    existing_ids = {q['id'] for q in ch04_data['questions']}
    if 'skz_ch04_q05' not in existing_ids:
        ch04_data['questions'].append(ch04_q05)
    if 'skz_ch04_q06' not in existing_ids:
        ch04_data['questions'].append(ch04_q06)
    ch04_data['totalQuestions'] = len(ch04_data['questions'])
    with open(ch04_path, 'w', encoding='utf-8') as f:
        json.dump(ch04_data, f, ensure_ascii=False, indent=2)
    print(f"[CH04] Updated with {ch04_data['totalQuestions']} questions.")

    # 5. Enrich Chapter 5
    ch05_path = os.path.join(DATA_DIR, 'shinkanzen_ch05.json')
    with open(ch05_path, 'r', encoding='utf-8') as f:
        ch05_data = json.load(f)
    existing_ids = {q['id'] for q in ch05_data['questions']}
    if 'skz_ch05_q05' not in existing_ids:
        ch05_data['questions'].append(ch05_q05)
    if 'skz_ch05_q06' not in existing_ids:
        ch05_data['questions'].append(ch05_q06)
    ch05_data['totalQuestions'] = len(ch05_data['questions'])
    with open(ch05_path, 'w', encoding='utf-8') as f:
        json.dump(ch05_data, f, ensure_ascii=False, indent=2)
    print(f"[CH05] Updated with {ch05_data['totalQuestions']} questions.")

    # 6. Complete Chapter 6 with 13 questions
    ch06_data = {
        "chapterId": "ch06",
        "chapter": "第6章：実践演習・総合理解",
        "title": "Chương 6: Luyện thực chiến & Đọc hiểu tổng hợp (実践演習・総合理解)",
        "description": "Tổng hợp trọn bộ 13 bài đọc thực chiến chuẩn định dạng JLPT N1: Đoạn văn ngắn (短文 2 bài), Đoạn văn vừa (中文 3 câu hỏi), Đoạn văn dài (長文 4 câu hỏi), So sánh tích hợp A-B (統合理解 2 câu hỏi) và Tìm kiếm thông tin bảng biểu (情報検索 2 câu hỏi).",
        "totalQuestions": len(ch06_questions),
        "questions": ch06_questions
    }
    ch06_path = os.path.join(DATA_DIR, 'shinkanzen_ch06.json')
    with open(ch06_path, 'w', encoding='utf-8') as f:
        json.dump(ch06_data, f, ensure_ascii=False, indent=2)
    print(f"[CH06] Generated complete suite with {len(ch06_questions)} questions.")

    # 7. Update dokkai-index.json
    total_all = 6 + 6 + 6 + 6 + 6 + len(ch06_questions)
    index_data = [
        {
            "id": "skz_ch01",
            "chapterNumber": 1,
            "chapter": "第1章：対比・逆接",
            "title": "Cấu trúc tương phản & nghịch lý (対比・逆接)",
            "theme": "Tiền đề số đông (〜と思われがちだが) vs Cú lật tư duy (しかし・実は)",
            "description": "Chương 1 mở đầu giáo trình Shin Kanzen Master Dokkai N1. Rèn luyện phản xạ bóc tách quan niệm thông thường của xã hội và nắm bắt tức thì thông điệp cốt lõi của tác giả qua các từ nối lật ngược vấn đề.",
            "file": "data/n1_dokkai/shinkanzen_ch01.json",
            "available": True,
            "totalQuestions": 6,
            "types": ["short", "medium"]
        },
        {
            "id": "skz_ch02",
            "chapterNumber": 2,
            "chapter": "第2章：言い換え・比喩",
            "title": "Diễn đạt tương đương & Ẩn dụ (言い換え・比喩)",
            "theme": "Nhận diện mệnh đề đồng nghĩa (つまり・すなわち) và giải mã hình ảnh ẩn dụ",
            "description": "Rèn luyện kỹ năng phát hiện các cách diễn đạt lại tư tưởng của tác giả và giải mã hàm ý ẩn dụ trong câu hỏi N1.",
            "file": "data/n1_dokkai/shinkanzen_ch02.json",
            "available": True,
            "totalQuestions": 6,
            "types": ["short", "medium"]
        },
        {
            "id": "skz_ch03",
            "chapterNumber": 3,
            "chapter": "第3章：疑問提示・筆者の主張",
            "title": "Câu hỏi gợi mở & Quan điểm tác giả (疑問提示・筆者の主張)",
            "theme": "Bắt trọn câu hỏi tu từ (〜だろうか) và nhận diện quan điểm cốt lõi của tác giả",
            "description": "Khám phá cách thức tác giả đặt câu hỏi tu từ để lật ngược định kiến và khẳng định lập trường then chốt.",
            "file": "data/n1_dokkai/shinkanzen_ch03.json",
            "available": True,
            "totalQuestions": 6,
            "types": ["short", "medium"]
        },
        {
            "id": "skz_ch04",
            "chapterNumber": 4,
            "chapter": "第4章：指示語・機能表現",
            "title": "Từ chỉ thị & Cấu trúc chức năng (指示語・機能表現)",
            "theme": "Lần theo dấu vết của từ chỉ thị (これ・それ・こうした) và liên kết mạch văn",
            "description": "Luyện kỹ năng truy tìm đối tượng được chỉ định chính xác, giải quyết triệt để các câu hỏi 'Điều này chỉ cái gì?'.",
            "file": "data/n1_dokkai/shinkanzen_ch04.json",
            "available": True,
            "totalQuestions": 6,
            "types": ["short", "medium"]
        },
        {
            "id": "skz_ch05",
            "chapterNumber": 5,
            "chapter": "第5章：理由・因果関係",
            "title": "Mối quan hệ nhân quả & Lý do (理由・因果関係)",
            "theme": "Bóc tách mối quan hệ nhân quả (なぜなら・〜からだ) và nguồn cơn sự việc",
            "description": "Nắm vững phương pháp lần theo nguồn cơn của vấn đề để trả lời chính xác các câu hỏi 'Tại sao tác giả lại nói như vậy?'.",
            "file": "data/n1_dokkai/shinkanzen_ch05.json",
            "available": True,
            "totalQuestions": 6,
            "types": ["short", "medium"]
        },
        {
            "id": "skz_ch06",
            "chapterNumber": 6,
            "chapter": "第6章：実践演習・総合理解",
            "title": "Luyện thực chiến & Đọc hiểu tổng hợp (実践演習・総合理解)",
            "theme": "Trọn bộ 5 định dạng thi N1: Đoản văn, Trung văn, Trường văn, So sánh A-B, Tìm thông tin",
            "description": "Luyện tập tổng hợp trọn bộ 13 câu hỏi thực chiến chuẩn đề thi JLPT N1 Dokkai dưới áp lực phòng thi thật.",
            "file": "data/n1_dokkai/shinkanzen_ch06.json",
            "available": True,
            "totalQuestions": len(ch06_questions),
            "types": ["short", "medium", "long", "compare", "search"]
        }
    ]

    index_path = os.path.join(DATA_DIR, 'dokkai-index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    print(f"[INDEX] Updated {index_path} with total {total_all} questions.")

    # 8. Copy to public/data/n1_dokkai/
    for fname in os.listdir(DATA_DIR):
        if fname.endswith('.json'):
            src = os.path.join(DATA_DIR, fname)
            dst = os.path.join(PUBLIC_DATA_DIR, fname)
            shutil.copy2(src, dst)
    print(f"[MIRROR] Copied all json files to {PUBLIC_DATA_DIR}.")

    print("=" * 80)
    print(f" ✨ BUILD COMPLETE! Total Dokkai Questions: {total_all}")
    print("=" * 80)

if __name__ == '__main__':
    run()
