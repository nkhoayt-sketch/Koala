import json
import os

data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'n1_dokkai')
os.makedirs(data_dir, exist_ok=True)

# ==============================================================================
# CHAPTER 3: 第3章：疑問提示・筆者の主張 (Câu hỏi gợi mở & Quan điểm của tác giả)
# ==============================================================================
ch03_data = {
  "chapterId": "ch03",
  "chapter": "第3章：疑問提示・筆者の主張",
  "title": "Chương 3: Câu hỏi gợi mở & Quan điểm của tác giả (疑問提示・筆者の主張)",
  "description": "Phương pháp Shin Kanzen Dokkai N1: Bắt trọn câu hỏi tu từ (〜だろうか・〜ではないか), nhận diện cách tác giả tự đặt vấn đề để lật ngược định kiến và chốt hạ quan điểm then chốt.",
  "totalQuestions": 4,
  "questions": [
    {
      "id": "skz_ch03_q01",
      "chapter": "第3章：疑問提示・筆者の主張",
      "title": "第3章 練習 1",
      "mondaiType": "short",
      "passage": "科学技術の進歩によって、私たちの生活はかつてないほどの利便性と効率性を手に入れた。ボタン一つで世界中の情報にアクセスでき、移動にかかる時間も劇的に短縮された。しかし、これほど便利になった現代社会において、人間は本当に幸福になり、心の豊かさを獲得したのだろうか。\n\nむしろ、効率化によって生み出されたはずの余暇は、新たな情報処理や雑務によって埋め尽くされ、私たちは常に時間に追われる感覚に苛まれている。利便性を追い求めた結果、皮肉にも自らを時間に縛り付ける生き方に陥ってしまったのではないか。真の豊かさとは、速度や利便性の追求にあるのではなく、何ものにも急かされずに目の前の瞬間に没頭できる心の静寂の中にこそ存在するのだ。",
      "question": "現代の「利便性の追求」について、筆者はどのように考えているか。",
      "options": [
        "生活の利便性が向上したことで、現代人は余暇を有効に使い心の豊かさを実現した。",
        "利便性の追求はかえって人間を時間に縛り付け、真の心の静寂を奪う結果となっている。",
        "科学技術による効率化をさらに進めることで、過密なスケジュールを解消すべきである。",
        "時間の浪費を防ぐための効率的な技術利用こそが、現代人にとって真の幸福の基盤である。"
      ],
      "answer": 2,
      "logicHighlights": {
        "counterPremise": "科学技術の進歩によって、私たちの生活はかつてないほどの利便性と効率性を手に入れた",
        "turningPoint": "しかし、これほど便利になった現代社会において、人間は本当に幸福になり、心の豊かさを獲得したのだろうか",
        "authorConclusion": "真の豊かさとは、速度や利便性の追求にあるのではなく、何ものにも急かされずに目の前の瞬間に没頭できる心の静寂の中にこそ存在するのだ"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Trái ngược lập luận): Bài đọc nêu rõ余暇 (thời gian rỗi) bị lấp đầy bởi thông tin và ta luôn bị thời gian truy đuổi, không phải đã đạt được tâm hồn phong phú.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với câu hỏi tu từ và kết luận cuối đoạn: tiện lợi trớ trêu thay lại trói buộc ta vào thời gian, đánh mất sự tĩnh lặng trong tâm hồn.",
        "opt3": "❌ BẪY TƯ DUY (Đưa giải pháp ngoài bài): Tác giả không kêu gọi tiếp tục đẩy mạnh công nghệ để giải quyết lịch trình.",
        "opt4": "❌ BẪY TƯ DUY (Ngược quan điểm tác giả): Tác giả phản đối việc chạy theo tốc độ và tiện lợi máy móc."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Nhờ sự tiến bộ của khoa học kỹ thuật, cuộc sống của chúng ta đã có được sự tiện lợi và hiệu quả chưa từng thấy. Chỉ bằng một nút bấm có thể tiếp cận thông tin toàn cầu, thời gian di chuyển cũng rút ngắn vượt bậc. Thế nhưng, trong một xã hội tiện lợi nhường này, liệu con người có thực sự trở nên hạnh phúc và đạt được sự phong phú trong tâm hồn hay không?<br><br>Trái lại, khoảng thời gian rảnh rỗi lẽ ra được sinh ra từ sự tối ưu hóa hiệu suất nay lại bị lấp kín bởi việc xử lý thông tin mới và những việc vặt vãnh, khiến chúng ta luôn bị dằn vặt bởi cảm giác bị thời gian truy đuổi. Chẳng phải việc mải miết theo đuổi tiện ích, trớ trêu thay, lại đẩy chúng ta vào lối sống tự trói buộc mình vào thời gian đó sao? Sự giàu có đích thực không nằm ở việc chạy đua tốc độ hay tiện ích, mà hiện hữu chính trong sự tĩnh lặng nội tâm, nơi ta có thể đắm mình vào khoảnh khắc trước mắt mà không bị bất cứ điều gì thúc giục.<br><br><b>【Phân tích cấu trúc 疑問提示・筆者の主張】:</b><br>1. <b>Đặt câu hỏi tu từ (疑問提示):</b> <code>〜獲得したのだろうか</code> (Liệu đã đạt được sự phong phú tâm hồn hay chưa? -> Hàm ý là chưa).<br>2. <b>Phát triển lập luận phản bác:</b> <code>〜のではないか</code> (Chẳng phải đã tự trói buộc mình vào thời gian hay sao?).<br>3. <b>Câu chốt khẳng định (筆者の主張):</b> <code>〜にこそ存在するのだ</code> (Chính trong sự tĩnh lặng nội tâm mới là sự giàu có đích thực)."
    },
    {
      "id": "skz_ch03_q02",
      "chapter": "第3章：疑問提示・筆者の主張",
      "title": "第3章 練習 2",
      "mondaiType": "short",
      "passage": "私たちは日常において、美しい絵画や雄大な自然の風景を目にしたとき、「美」が対象そのものに客観的な性質として内在していると考えがちである。だが、美とは本当に、物理的な物体の中に固定されて実在するものなのだろうか。\n\nもしそうであるなら、時代や文化、あるいは個人の境遇によって美の基準が大きく揺らぐ現象を説明することはできない。美とは、観察者の感性や記憶、そしてその瞬間の情動が対象と交錯したときに初めて立ち現れる「関係性の奇跡」にほかならない。美は事物の中にあらかじめ存在するのではなく、それを見つめる私たちの感受性の深さによって、その都度新たに創造されているのである。",
      "question": "「美」の本質について、筆者の主張と最も合致するものはどれか。",
      "options": [
        "美は絵画や自然の中に客観的・固定的に存在し、万人に共通する不変の性質である。",
        "美の基準は時代や文化に左右されず、対象物の物理的な完成度によって決まる。",
        "美は対象そのものに内在するのではなく、対象と向き合う観察者の感受性との関係において生み出される。",
        "個人の感性や記憶は不安定であるため、真の美を把握するには客観的な評価基準の確立が不可欠である。"
      ],
      "answer": 3,
      "logicHighlights": {
        "counterPremise": "「美」が対象そのものに客観的な性質として内在していると考えがちである",
        "turningPoint": "だが、美とは本当に、物理的な物体の中に固定されて実在するものなのだろうか",
        "authorConclusion": "美は事物の中にあらかじめ存在するのではなく、それを見つめる私たちの感受性の深さによって、その都度新たに創造されているのである"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đồng hóa tiền đề số đông): Đây là quan niệm thường tình ở câu đầu mà tác giả dùng câu hỏi tu từ để bác bỏ.",
        "opt2": "❌ BẪY TƯ DUY (Ngược thực tế trong bài): Tác giả chỉ ra tiêu chuẩn cái đẹp luôn biến động theo thời đại và văn hóa.",
        "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp 100% với luận điểm cốt lõi: cái đẹp là sự kỳ diệu của mối quan hệ tương tác, được sáng tạo từ chiều sâu cảm thụ của người quan sát.",
        "opt4": "❌ BẪY TƯ DUY (Suy diễn ngoài bài): Tác giả không hề yêu cầu lập tiêu chuẩn đánh giá khách quan."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Trong đời sống thường nhật, khi chiêm ngưỡng một bức tranh đẹp hay một cảnh sắc thiên nhiên hùng vĩ, ta thường dễ nghĩ rằng 'cái đẹp' vốn nội tại như một đặc tính khách quan ngay trong chính đối tượng đó. Nhưng liệu cái đẹp có thực sự tồn tại cố định bên trong các thực thể vật lý như thế hay không?<br><br>Nếu quả đúng như vậy, ta sẽ không thể lý giải được hiện tượng vì sao chuẩn mực cái đẹp lại dao động dữ dội tùy theo thời đại, văn hóa hay hoàn cảnh của mỗi cá nhân. Cái đẹp chẳng qua chính là 'phép màu của tính tương quan', chỉ bừng nở khi xúc cảm, ký ức và tâm trạng của người quan sát hòa quyện cùng đối tượng. Cái đẹp không hề tồn tại sẵn trong sự vật, mà nó được tái tạo mới trong từng khoảnh khắc nhờ vào độ sâu sắc trong năng lực cảm thụ của chúng ta.<br><br><b>【Phân tích cấu trúc 疑問提示・筆者の主張】:</b><br>1. <b>Nêu định kiến số đông:</b> <code>〜と考えがちである</code>.<br>2. <b>Cú lật bằng câu hỏi gợi mở:</b> <code>だが、〜ものなのだろうか</code>.<br>3. <b>Chốt luận điểm tác giả:</b> <code>〜ではなく、〜によって、その都度新たに創造されているのである</code>."
    },
    {
      "id": "skz_ch03_q03",
      "chapter": "第3章：疑問提示・筆者の主張",
      "title": "第3章 練習 3",
      "mondaiType": "medium",
      "passage": "現代の学校教育やビジネスの現場では、「失敗を恐れずに挑戦することの大切さ」が盛んに叫ばれている。失敗から学び、それを糧にして成長するプロセスこそが成功への近道であるという主張には、一見すると誰も反論の余地がないように思える。しかし、言葉で「失敗を恐れるな」と唱えるだけで、本当に若者や挑戦者たちの足元にある不安が払拭されるのだろうか。\n\n現実に目を向ければ、社会のシステムは一度の過ちや挫折に対して驚くほど不寛容である。入試や就職のレールから一度外れた者に向けられる冷淡な視線、組織内での減点主義の評価体系などを前にして、個人がリスクを冒すことをためらうのは極めて自然な防衛反応である。それにもかかわらず、挑戦を回避する姿勢を個人の気概や勇気の欠如に帰してしまうのは、問題のすり替えではないだろうか。\n\n挑戦する精神を社会に育みたいのであれば、個人に精神論を説く前に、失敗した人間が容易に再起できるセーフティネットと寛容な文化基盤を構築することこそが先決である。失敗のリスクを個人に背負わせたまま美辞麗句を並べるだけでは、真のイノベーションなど生まれようはずもない。",
      "question": "「失敗を恐れずに挑戦する環境」について、筆者の考えとして最も適切なものはどれか。",
      "options": [
        "若者が挑戦をためらう主な原因は精神的な気概の不足にあるため、教育現場での意識改革が急務である。",
        "社会システムは十分に寛容であるため、個人は減点主義を気にせず自らの意志で失敗を乗り越えるべきだ。",
        "個人の勇気や精神論に頼るのではなく、失敗しても再起できる寛容な社会基盤や制度を整えることが不可欠である。",
        "失敗から学ぶプロセスは美辞麗句にすぎず、最初から過ちを犯さない完璧な行動計画こそがイノベーションを生む。"
      ],
      "answer": 3,
      "logicHighlights": {
        "counterPremise": "言葉で「失敗を恐れるな」と唱えるだけで、本当に若者や挑戦者たちの足元にある不安が払拭されるのだろうか",
        "turningPoint": "それにもかかわらず、挑戦を回避する姿勢を個人の気概や勇気の欠如に帰してしまうのは、問題のすり替えではないだろうか",
        "authorConclusion": "個人に精神論を説く前に、失敗した人間が容易に再起できるセーフティネットと寛容な文化基盤を構築することこそが先決である"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đổ lỗi cho cá nhân bị tác giả phản bác): Tác giả chỉ trích việc quy kết thất bại cho sự thiếu dũng khí của cá nhân (問題のすり替え).",
        "opt2": "❌ BẪY TƯ DUY (Trái ngược thực tế nêu trong bài): Bài khẳng định hệ thống xã hội cực kỳ khắt khe (不寛容) và mang nặng tính trừ điểm.",
        "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với thông điệp then chốt: trước khi rao giảng lý thuyết suông về tinh thần, phải xây dựng mạng lưới an toàn và văn hóa dung thứ để người thất bại có thể đứng dậy làm lại.",
        "opt4": "❌ BẪY TƯ DUY (Cực đoan hóa): Tác giả không bảo phủ nhận việc học từ thất bại, mà lên án việc bắt cá nhân gánh rủi ro một mình."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Trong giáo dục nhà trường và thương trường hiện đại, người ta không ngừng ra rả khẩu hiệu 'hãy dám thách thức, đừng sợ thất bại'. Luận điểm cho rằng học hỏi từ vấp ngã rồi biến nó thành bàn đạp trưởng thành là con đường ngắn nhất đến thành công thoạt nhìn tưởng như chẳng ai có thể bắt bẻ. Thế nhưng, liệu chỉ hô hào bằng miệng 'đừng sợ thất bại' có thực sự xua tan được nỗi bất an dưới chân những người trẻ và những kẻ dấn thân hay không?<br><br>Nhìn vào thực tế, hệ thống xã hội lại khắt khe và bất khoan dung đến kinh ngạc đối với một lần lầm lỡ hay vấp ngã. Ánh nhìn lạnh nhạt hướng vào kẻ lỡ trật bánh khỏi đường ray thi cử hay xin việc, cùng chế độ đánh giá nặng tính trừ điểm trong tổ chức khiến cho việc cá nhân chùn bước trước rủi ro là một phản xạ tự vệ hết sức tự nhiên. Ấy vậy mà lại quy kết thái độ né tránh thách thức ấy cho sự thiếu hụt dũng khí hay ý chí của cá nhân, chẳng phải là hành vi đánh tráo khái niệm hay sao?<br><br>Nếu muốn nuôi dưỡng tinh thần dám dấn thân trong xã hội, thì trước khi rao giảng liệu pháp tinh thần cho cá nhân, việc cấp bách trước mắt là kiến tạo một mạng lưới an toàn và nền tảng văn hóa bao dung để kẻ thất bại có thể dễ dàng tái khởi nghiệp. Chừng nào còn bắt cá nhân trơ trọi gánh lấy rủi ro thất bại mà chỉ biết tuôn ra những lời hoa mỹ, thì đổi mới sáng tạo thực sự tuyệt đối chẳng thể nào nảy nở.<br><br><b>【Phân tích cấu trúc Trung văn (疑問提示・主張)】:</b><br>Tác giả dùng liên tiếp 2 câu hỏi tu từ: <code>〜払拭されるのだろうか</code> -> <code>〜すり替えではないだろうか</code> để lật tẩy sự đạo đức giả của các khẩu hiệu suông, từ đó chốt hạ giải pháp thể chế ở câu kết <code>〜ことこそが先決である</code>."
    },
    {
      "id": "skz_ch03_q04",
      "chapter": "第3章：疑問提示・筆者の主張",
      "title": "第3章 練習 4",
      "mondaiType": "short",
      "passage": "科学の言説は、主観や偏見を排した「絶対的な客観的真理」として社会に受け入れられる傾向が強い。数値データや実証実験によって裏付けられた結論には、疑う余地など存在しないかのように信じられている。しかし、科学者が立てる問いそのものや、データを解釈する視点までもが、本当に人間の社会的関心や時代精神から完全に独立していると言えるのだろうか。\n\n科学史を振り返れば、ある時代に絶対と信じられた理論が、パラダイムの転換によって覆された事例は枚挙にいとまがない。科学的知見とは、現時点で最も反証に耐えうる「暫定的な合意」にすぎないのである。科学を絶対視して盲信するのではなく、常に自己検証と批判的対話に開かれた仮説の体系として捉える謙虚さこそが、真の科学的精神にふさわしい。",
      "question": "「科学の客観性」について、筆者が最も伝えたいことはどれか。",
      "options": [
        "科学の結論は数値データに基づくため、時代の変化に関わらず絶対的な真理として受容されるべきだ。",
        "科学的知見は暫定的な仮説にすぎず、絶対視することなく常に批判的検証に開かれた姿勢を持つべきである。",
        "科学者の研究姿勢は主観や社会的関心から完全に独立しており、その客観性に疑いの余地はない。",
        "過去の理論が覆されてきた歴史を考慮すると、科学的知見に依拠して社会的意思決定を行うべきではない。"
      ],
      "answer": 2,
      "logicHighlights": {
        "counterPremise": "科学の言説は、主観や偏見を排した「絶対的な客観的真理」として社会に受け入れられる傾向が強い",
        "turningPoint": "しかし、科学者が立てる問いそのものや、データを解釈する視点までもが、本当に人間の社会的関心や時代精神から完全に独立していると言えるのだろうか",
        "authorConclusion": "科学を絶対視して盲信するのではなく、常に自己検証と批判的対話に開かれた仮説の体系として捉える謙虚さこそが、真の科学的精神にふさわしい"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đồng hóa tiền đề số đông): Đây là xu hướng tiếp nhận ngây thơ của xã hội mà tác giả phản bác.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp hoàn toàn với câu chốt: tri thức khoa học chỉ là sự đồng thuận tạm thời, cần giữ thái độ khiêm nhường xem nó là hệ giả thuyết luôn mở cho sự tự kiểm chứng và đối thoại phê phán.",
        "opt3": "❌ BẪY TƯ DUY (Trái ngược câu hỏi tu từ): Tác giả ngầm chỉ ra câu hỏi khoa học và cách diễn giải luôn chịu ảnh hưởng từ tinh thần thời đại.",
        "opt4": "❌ BẪY TƯ DUY (Cực đoan hóa tiêu cực): Tác giả không bảo bài xích khoa học trong quyết sách xã hội."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Diễn ngôn khoa học thường có xu hướng được xã hội tiếp nhận như một 'chân lý khách quan tuyệt đối' đã loại trừ mọi thiên kiến và chủ quan. Những kết luận được nâng đỡ bởi số liệu thực nghiệm dường như được tin tưởng tuyệt đối như thể không còn chút nghi ngờ nào. Thế nhưng, liệu ngay cả những câu hỏi do các nhà khoa học đặt ra và góc nhìn diễn giải dữ liệu có thực sự hoàn toàn độc lập khỏi mối quan tâm xã hội và tinh thần thời đại của con người hay không?<br><br>Nhìn lại lịch sử khoa học, những ví dụ về các lý thuyết từng được coi là chân lý bất di bất dịch ở một thời kỳ rồi sau đó bị đảo lộn bởi sự chuyển dịch hệ hình nhiều không đếm xuể. Tri thức khoa học thực chất chỉ là một 'sự đồng thuận tạm thời' có sức chịu đựng tốt nhất trước các phản biện ở thời điểm hiện tại. Thay vì tuyệt đối hóa và mù quáng tin theo khoa học, việc giữ thái độ khiêm nhường nhìn nhận khoa học như một hệ thống giả thuyết luôn mở ra cho sự tự kiểm chứng và đối thoại phản biện mới thực sự xứng đáng với tinh thần khoa học chân chính."
    }
  ]
}

# ==============================================================================
# CHAPTER 4: 第4章：指示語・機能表現 (Từ chỉ thị & Cấu trúc chức năng)
# ==============================================================================
ch04_data = {
  "chapterId": "ch04",
  "chapter": "第4章：指示語・機能表現",
  "title": "Chương 4: Từ chỉ thị & Cấu trúc chức năng (指示語・機能表現)",
  "description": "Phương pháp Shin Kanzen Dokkai N1: Lần theo dấu vết của từ chỉ thị (これ・それ・こうした・このような) và các cấu trúc chức năng mạch lạc để định vị chính xác đối tượng được đề cập.",
  "totalQuestions": 4,
  "questions": [
    {
      "id": "skz_ch04_q01",
      "chapter": "第4章：指示語・機能表現",
      "title": "第4章 練習 1",
      "mondaiType": "short",
      "passage": "他者との真のコミュニケーションにおいては、相手の言葉の表面的な意味を理解するだけでは不十分である。発話の背景にある感情の揺らぎや、言葉にされなかった沈黙の重みにまで耳を傾け、相手の内面的な世界を自己の経験に照らし合わせて追体験する感受性が求められる。\n\nこうした共感的な態度を欠いたままでは、どれほど言葉を交わそうとも、互いの主張の押し付け合いに終始してしまう。つまり、真に対話が成立するためには、自らの固定観念を一度保留し、相手の視点に立って世界を捉え直す勇気が必要なのだ。それこそが、孤立した個人と個人をつなぐ唯一の架け橋となる。",
      "question": "傍線部「それ」は何を指しているか。",
      "options": [
        "相手の発話の表面的な意味を論理的に分析し、誤りを正す行為。",
        "言葉を頻繁に交わし合い、自分の主張を相手に強く納得させる態度。",
        "自らの固定観念を保留し、相手の視点に立って世界を捉え直す勇気。",
        "過去の経験のみに頼って、他者の沈黙を自分勝手に推し量ること。"
      ],
      "answer": 3,
      "logicHighlights": {
        "counterPremise": "こうした共感的な態度を欠いたままでは、どれほど言葉を交わそうとも、互いの主張の押し付け合いに終始してしまう",
        "turningPoint": "つまり",
        "authorConclusion": "自らの固定観念を一度保留し、相手の視点に立って世界を捉え直す勇気が必要なのだ。それこそが、孤立した個人と個人をつなぐ唯一の架け橋となる"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Ngược ý đoạn 1): Chỉ phân tích bề mặt và bắt bẻ lỗi sai là thái độ thiếu thấu cảm.",
        "opt2": "❌ BẪY TƯ DUY (Đồng hóa điều bị phê phán): Ép buộc quan điểm của mình lên người khác (押し付け合い) là biểu hiện của đối thoại thất bại.",
        "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với câu văn liền trước chỉ thị từ 「それ」: lòng dũng cảm tạm gác định kiến của bản thân và đặt mình vào góc nhìn của đối phương.",
        "opt4": "❌ BẪY TƯ DUY (Suy diễn lệch lạc): Đoạn văn yêu cầu thấu cảm chân thành, không phải suy đoán áp đặt tùy tiện."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Trong giao tiếp chân thực với người khác, chỉ nắm bắt ý nghĩa bề mặt câu chữ của đối phương thôi là chưa đủ. Ta cần phải lắng nghe đến cả những rung cảm trong cảm xúc ẩn sau lời nói và sức nặng của những khoảng lặng không thốt nên lời, đòi hỏi một độ nhạy cảm để cùng trải nghiệm thế giới nội tâm của họ qua lăng kính trải nghiệm của chính mình.<br><br>Nếu thiếu đi thái độ thấu cảm như thế này, thì dù có trao đổi biết bao lời lẽ đi chăng nữa, rốt cuộc cũng chỉ dừng lại ở việc áp đặt quan điểm lẫn nhau. Nói cách khác, để cuộc đối thoại thực sự được xác lập, ta cần lòng dũng cảm tạm gác lại những định kiến bất di bất dịch của bản thân để nhìn nhận lại thế giới từ góc nhìn của đối phương. Chính điều đó mới là cây cầu duy nhất kết nối những cá nhân vốn dĩ cô lập lại với nhau.<br><br><b>【Phân tích từ chỉ thị (指示語)】:</b><br>Từ chỉ thị <code>それ</code> nằm ngay sau mệnh đề <code>自らの固定観念を一度保留し、相手の視点に立って世界を捉え直す勇気</code>. Nó quy chiếu thẳng đến hành động lùi một bước khỏi định kiến để thấu cảm."
    },
    {
      "id": "skz_ch04_q02",
      "chapter": "第4章：指示語・機能表現",
      "title": "第4章 練習 2",
      "mondaiType": "short",
      "passage": "近代社会は、自然を人間が支配し開発すべき対象として捉えることで、驚異的な物質的繁栄を築き上げてきた。原生林は農地や都市へと姿を変え、河川はダムによって制御された。しかしその一方で、地球規模の気候変動や生態系の破壊が深刻化し、人類自身の存続基盤が脅かされる事態を招いている。\n\nこのような矛盾が生じた根本的な原因は、人間が生態系という巨大な生命の網の目の一部にすぎないという事実を忘却した点にある。自然を単なる資源として客観視する傲慢さを改めない限り、真の持続可能性を達成することは不可能である。",
      "question": "傍線部「このような矛盾」が指す内容として最も適切なものはどれか。",
      "options": [
        "農地や都市を開発したにもかかわらず、人口が減少し経済が停滞していること。",
        "自然を支配して物質的繁栄を築いた一方で、環境破壊によって人類の生存基盤が脅かされていること。",
        "気候変動を防止するための技術開発が、かえって膨大なエネルギーを消費していること。",
        "原生林の保護に注力するあまり、近代都市のインフラ整備が滞ってしまったこと。"
      ],
      "answer": 2,
      "logicHighlights": {
        "counterPremise": "近代社会は、自然を人間が支配し開発すべき対象として捉えることで、驚異的な物質的繁栄を築き上げてきた",
        "turningPoint": "しかしその一方で",
        "authorConclusion": "このような矛盾が生じた根本的な原因は、人間が生態系という巨大な生命の網の目の一部にすぎないという事実を忘却した点にある"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đưa thông tin ngoài bài): Bài đọc không đề cập đến giảm dân số hay suy thoái kinh tế.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp trọn vẹn với 2 vế đối lập ở đoạn 1 được nối bởi 「しかしその一方で」: một mặt tạo phồn vinh vật chất, mặt khác phá hủy sinh thái đe dọa sự tồn vong của chính loài người.",
        "opt3": "❌ BẪY TƯ DUY (Chi tiết ngoài bài): Không nói về công nghệ chống biến đổi khí hậu tốn năng lượng.",
        "opt4": "❌ BẪY TƯ DUY (Xuyên tạc nội dung): Xã hội phát triển quá đà lấn át thiên nhiên, không phải vì lo bảo vệ rừng mà đình trệ đô thị."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Xã hội cận đại, bằng việc xem tự nhiên là đối tượng để con người thống trị và khai thác, đã kiến tạo nên một sự phồn vinh vật chất đáng kinh ngạc. Những cánh rừng nguyên sinh đã hóa thành đất nông nghiệp và đô thị, sông ngòi bị kiểm soát bởi các đập thủy điện. Thế nhưng mặt khác, sự biến đổi khí hậu toàn cầu và sự hủy hoại hệ sinh thái ngày càng trầm trọng, dẫn đến tình trạng nền tảng tồn vong của chính loài người bị đe dọa.<br><br>Nguyên nhân sâu xa làm nảy sinh mâu thuẫn như thế này bắt nguồn từ việc con người lãng quên sự thật rằng mình chỉ là một mắt xích nhỏ trong mạng lưới sự sống vĩ đại của hệ sinh thái. Chừng nào chưa sửa đổi thái độ kiêu ngạo xem tự nhiên như tài nguyên thuần túy, thì việc đạt được sự phát triển bền vững thực sự là điều bất khả thi."
    },
    {
      "id": "skz_ch04_q03",
      "chapter": "第4章：指示語・機能表現",
      "title": "第4章 練習 3",
      "mondaiType": "medium",
      "passage": "画期的なアイディアのひらめきや直感的な洞察は、しばしば論理的な思考の対極にある神秘的な能力として神秘化されがちである。天才的な芸術家や科学者が「突然神が降りてきたかのように答えが閃いた」と語るエピソードは、そうした見方を補強する根拠として好んで引用される。\n\nだが、認知科学の研究が明らかにしたように、直感とは何もない真空から突如として湧き出る超常現象ではない。それは、長年にわたって脳内に蓄積された膨大な知識や経験の断片が、意識下のレベルで高速に照合され、一つの秩序あるパターンとして再編された瞬間の知覚体験にすぎないのだ。地道な思考の試行錯誤と知識のインプットを積み重ねた者だけに、その蓄積が無意識の深層で熟成し、ひらめきという果実をもたらすのである。\n\nしたがって、日々の丹念な学習や論理的思考を怠ったまま、安易に「直感」に頼ろうとする姿勢は本末転倒と言わざるを得ない。論理の徹底的な探求の果てにこそ、真に信頼に足る直感が研ぎ澄まされるのである。",
      "question": "傍線部「そうした見方」が指す内容として最も適切なものはどれか。",
      "options": [
        "直感とは長年の知識や経験が無意識下で結びついた高度な認知プロセスであるという見方。",
        "直感やひらめきは、論理的思考とは無縁の神秘的で超常的な能力であるという見方。",
        "日々の学習を積み重ねることで、誰でも容易に天才的な閃きを得られるという見方。",
        "論理的思考を徹底的に探求しても、直感的な洞察力には敵わないという見方。"
      ],
      "answer": 2,
      "logicHighlights": {
        "counterPremise": "画期的なアイディアのひらめきや直感的な洞察は、しばしば論理的な思考の対極にある神秘的な能力として神秘化されがちである",
        "turningPoint": "だが、認知科学の研究が明らかにしたように",
        "authorConclusion": "論理の徹底的な探求の果てにこそ、真に信頼に足る直感が研ぎ澄まされるのである"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đánh tráo với quan điểm tác giả ở đoạn 2): Đây là định nghĩa khoa học đúng đắn của tác giả sau chữ 「だが」, không phải quan điểm số đông bị chỉ thị từ 「そうした見方」 quy chiếu.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với quan niệm thần bí hóa ở câu mở đầu: xem trực giác là năng lực thần bí đối lập với tư duy logic.",
        "opt3": "❌ BẪY TƯ DUY (Thông tin sai lệch): Tác giả không hề nói ai cũng dễ dàng đạt được tia sáng thiên tài.",
        "opt4": "❌ BẪY TƯ DUY (Đảo ngược tư tưởng): Tác giả đề cao việc rèn luyện tư duy logic làm nền tảng cho trực giác."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Những tia sáng ý tưởng mang tính đột phá hay sự thấu suốt mang tính trực giác thường dễ bị thần bí hóa như một thứ năng lực siêu nhiên nằm ở thái cực đối lập với tư duy logic. Những giai thoại về việc các nghệ sĩ hay nhà khoa học thiên tài kể lại rằng 'như thể bỗng nhiên có thần linh giáng xuống ban cho câu trả lời' thường rất hay được trích dẫn để củng cố cho cách nhìn nhận như thế.<br><br>Thế nhưng, như nghiên cứu khoa học nhận thức đã chỉ rõ, trực giác không phải hiện tượng siêu nhiên đột nhiên nảy nở từ chân không. Nó chẳng qua là một trải nghiệm tri giác tại khoảnh khắc mà vô số mảnh kiến thức và trải nghiệm tích lũy qua nhiều năm trong não bộ được đối chiếu với tốc độ siêu nhanh ở tầng tiềm thức và tái cấu trúc thành một trật tự hoàn chỉnh. Chỉ những ai kiên trì nạp kiến thức và trải qua quá trình thử sai suy nghĩ kỹ lưỡng, thì sự tích lũy ấy mới chín muồi trong tầng sâu vô thức để kết tinh thành trái ngọt trực giác.<br><br>Do đó, việc lơ là học hỏi cẩn trọng và tư duy logic mỗi ngày mà lại dễ dãi trông cậy vào 'trực giác' là một thái độ hoàn toàn đảo lộn đầu đuôi. Chính tại điểm tận cùng của sự truy tìm logic triệt để, trực giác thực sự đáng tin cậy mới được mài sắc."
    },
    {
      "id": "skz_ch04_q04",
      "chapter": "第4章：指示語・機能表現",
      "title": "第4章 練習 4",
      "mondaiType": "short",
      "passage": "都市化が進んだ社会において、人間はコンクリートと人工的な光に囲まれ、季節の移ろいや土の匂いといった自然の息吹から急速に切り離されつつある。空調によって一定に保たれた室内で過ごす日常は、身体が本来持っていた環境適応力や感覚の鋭敏さを次第に鈍磨させていく。\n\nこうした身体感覚の衰退は、単なる肉体的な問題にとどまらず、人間の情緒や想像力の枯渇にも深く影を落としている。生身の自然との交感が遮断されることによって、私たちは自らが生命体であるという根源的な実感を見失ってしまうのだ。",
      "question": "傍線部「こうした身体感覚の衰退」の具体例として最も適切なものはどれか。",
      "options": [
        "人工的な環境に慣れきった結果、自然の美しさに感動する情緒が完全に消滅すること。",
        "自然から切り離された生活により、身体が本来備えていた環境適応力や感覚の鋭敏さが鈍ること。",
        "都市での過密な生活ストレスによって、運動能力が低下し病気にかかりやすくなること。",
        "土の匂いや季節の移ろいに対する関心が薄れ、屋外での活動時間を極端に減らすこと。"
      ],
      "answer": 2,
      "logicHighlights": {
        "counterPremise": "空調によって一定に保たれた室内で過ごす日常は、身体が本来持っていた環境適応力や感覚の鋭敏さを次第に鈍磨させていく",
        "turningPoint": "こうした身体感覚の衰退は",
        "authorConclusion": "生身の自然との交感が遮断されることによって、私たちは自らが生命体であるという根源的な実感を見失ってしまうのだ"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đoán bừa quá mức): Bài đọc chỉ nói ảnh hưởng đến cảm xúc chứ không bảo cảm xúc 'hoàn toàn biến mất'.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với câu trước: khả năng thích ứng môi trường và độ nhạy bén của các giác quan vốn có bị cùn mòn (鈍磨させていく).",
        "opt3": "❌ BẪY TƯ DUY (Thông tin ngoài bài): Không nhắc đến stress hay bệnh tật.",
        "opt4": "❌ BẪY TƯ DUY (Nhầm lẫn giữa nguyên nhân và hệ quả suy thoái cảm giác): Việc giảm tiếp xúc tự nhiên là bối cảnh, suy thoái là việc các giác quan bị cùn lụt."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Trong xã hội đô thị hóa phát triển, con người bị bao bọc bởi bê tông và ánh sáng nhân tạo, đang nhanh chóng bị tách rời khỏi hơi thở tự nhiên như sự đổi dời của bốn mùa hay mùi hương của đất cát. Những ngày tháng sống trong phòng kín máy lạnh nhiệt độ không đổi đang dần làm cùn mòn đi khả năng thích ứng môi trường và độ nhạy bén của các giác quan vốn có của cơ thể sinh học.<br><br>Sự suy thoái cảm giác cơ thể như thế này không chỉ dừng lại ở vấn đề thể chất đơn thuần, mà còn phủ bóng đen sâu sắc lên sự cạn kiệt cảm xúc và trí tưởng tượng của con người. Việc bị cắt đứt giao cảm với tự nhiên sống động khiến chúng ta đánh mất đi cảm thức căn cốt rằng bản thân mình là một sinh mệnh sống."
    }
  ]
}

# ==============================================================================
# CHAPTER 5: 第5章：理由・因果関係 (Mối quan hệ nhân quả & Lý do)
# ==============================================================================
ch05_data = {
  "chapterId": "ch05",
  "chapter": "第5章：理由・因果関係",
  "title": "Chương 5: Mối quan hệ nhân quả & Lý do (理由・因果関係)",
  "description": "Phương pháp Shin Kanzen Dokkai N1: Lần theo cấu trúc giải thích nguyên nhân (なぜなら・〜からだ・〜に起因する) để trả lời chính xác câu hỏi 'Vì sao tác giả lập luận như vậy?'.",
  "totalQuestions": 4,
  "questions": [
    {
      "id": "skz_ch05_q01",
      "chapter": "第5章：理由・因果関係",
      "title": "第5章 練習 1",
      "mondaiType": "short",
      "passage": "現代人はしばしば「孤独」を寂しさや孤立として恐れ、常にSNSなどを通じて誰かとつながっていないと不安を覚える。しかし、思索を深め自己を確立するためには、意識的に一人になる「積極的な孤独の時間」が不可欠である。\n\nなぜなら、他者の視線や社会的評価から完全に解放された静寂の中でしか、人間は自らの内面にある本音と向き合い、自立した価値判断を鍛え上げることができないからだ。常に他者と接続された状態では、自分自身の思考すらも世間の声に同調して希釈されてしまう。精神的な成熟とは、他者との調和と同時に、孤独に耐えうる強さを培うことによって初めて成し遂げられるのである。",
      "question": "筆者が「積極的な孤独の時間」を不可欠と考える理由は何か。",
      "options": [
        "他者とのつながりを断つことで、社会的な責任や義務から逃避できるから。",
        "他者の視線から離れた静寂の中でこそ、自己の内面と向き合い自立した価値判断を養えるから。",
        "SNSでの交流は時間の浪費であり、人間関係のトラブルを未然に防ぐ唯一の手段だから。",
        "孤独に耐える訓練を積むことで、他者との一切の妥協を排した強い自己主張ができるようになるから。"
      ],
      "answer": 2,
      "logicHighlights": {
        "counterPremise": "現代人はしばしば「孤独」を寂しさや孤立として恐れ、常にSNSなどを通じて誰かとつながっていないと不安を覚える",
        "turningPoint": "なぜなら",
        "authorConclusion": "精神的な成熟とは、他者との調和と同時に、孤独に耐えうる強さを培うことによって初めて成し遂げられるのである"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Bóp méo thành trốn tránh trách nhiệm): Tác giả bảo cô độc tích cực để trưởng thành, không phải để trốn tránh trách nhiệm xã hội.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với lý do sau chữ 「なぜなら」: chỉ trong tĩnh lặng thoát khỏi ánh nhìn tha nhân mới đối diện được với lòng mình và rèn giũa phán đoán độc lập.",
        "opt3": "❌ BẪY TƯ DUY (Thêm thắt thông tin tiêu cực): Bài viết không nói SNS là nguồn cơn rắc rối hay lãng phí thời gian.",
        "opt4": "❌ BẪY TƯ DUY (Cực đoan hóa): Trưởng thành tinh thần đòi hỏi hòa hợp với người khác chứ không phải bài trừ thỏa hiệp để tự cao tự đại."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Người hiện đại thường lo sợ 'sự cô độc' như một nỗi buồn bã hay sự cô lập, và luôn cảm thấy bất an nếu không liên tục kết nối với ai đó qua mạng xã hội. Thế nhưng, để đào sâu suy tưởng và xác lập bản ngã, khoảng thời gian 'cô độc chủ động' - tức là có ý thức ở một mình - là điều không thể thiếu.<br><br>Lý do là vì chỉ trong sự tĩnh lặng khi hoàn toàn được giải phóng khỏi ánh mắt và sự phán xét xã hội của người khác, con người mới có thể đối diện với tiếng lòng chân thực bên trong mình và tôi luyện khả năng phán đoán giá trị độc lập. Trong trạng thái luôn kết nối với người khác, ngay cả suy nghĩ của chính mình cũng bị hòa tan và pha loãng theo thanh âm số đông. Sự trưởng thành về mặt tinh thần chỉ có thể đạt được khi ta vừa biết hòa hợp với người khác, đồng thời vừa bồi đắp được sức mạnh đủ để chịu đựng sự cô độc.<br><br><b>【Phân tích quan hệ nhân quả (因果関係)】:</b><br>Câu hỏi hỏi 'Vì sao?'. Đáp án nằm trọn vẹn ở câu nối bằng <code>なぜなら、〜からだ</code>."
    },
    {
      "id": "skz_ch05_q02",
      "chapter": "第5章：理由・因果関係",
      "title": "第5章 練習 2",
      "mondaiType": "short",
      "passage": "世界各地の大都市を訪れると、どこに行っても同じような高層ビルが立ち並び、似通ったチェーン店が軒を連ねている光景に遭遇する。都市のグローバル化と機能性の追求は、地域固有の歴史的風情や独自の文化的多様性を急速に均質化させてしまった。\n\nこうした都市空間の画一化がもたらされた主因は、経済的な効率性と短期的な収益性の極大化ばかりが都市開発の至上命題とされてきたことにある。地域に固有の古い街並みや職人文化を維持するコストは「非効率」として切り捨てられ、規格化された商業施設へと建て替えられていった。その結果、都市はその土地ならではの魂を失い、どこにも代わりのきく無機質な空間へと成り下がってしまったのである。",
      "question": "都市空間が「均質化・画一化」してしまった主な原因について、筆者はどう説明しているか。",
      "options": [
        "歴史的建造物の老朽化が進み、災害防止のために建て替えを余儀なくされたから。",
        "経済的な効率性と短期的な利益ばかりを最優先して都市開発が進められてきたから。",
        "観光客を誘致するために、世界基準の便利なチェーン店を増やす必要があったから。",
        "地域の住民が伝統的な職人文化に誇りを持たなくなり、近代的な利便性を求めたから。"
      ],
      "answer": 2,
      "logicHighlights": {
        "counterPremise": "都市のグローバル化と機能性の追求は、地域固有の歴史的風情や独自の文化的多様性を急速に均質化させてしまった",
        "turningPoint": "こうした都市空間の画一化がもたらされた主因は",
        "authorConclusion": "その結果、都市はその土地ならではの魂を失い、どこにも代わりのきく無機質な空間へと成り下がってしまったのである"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Lý do ngoài bài): Không hề nhắc đến nhà cửa xuống cấp hay phòng chống thiên tai.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp nguyên văn với cụm từ chỉ nguyên nhân then chốt: 「主因は、経済的な効率性と短期的な収益性の極大化ばかりが都市開発の至上命題とされてきたことにある」.",
        "opt3": "❌ BẪY TƯ DUY (Đoán bừa): Bài viết không nói mở chuỗi cửa hàng vì thu hút khách du lịch.",
        "opt4": "❌ BẪY TƯ DUY (Đổ lỗi cho dân cư): Tác giả phê phán triết lý phát triển kinh tế của quy hoạch đô thị chứ không đổ lỗi cho người dân."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Khi ghé thăm các đô thị lớn khắp thế giới, ta thường bắt gặp cảnh tượng ở đâu cũng san sát những tòa nhà chọc trời giống hệt nhau và các chuỗi cửa hàng tương tự nhau xếp hàng dài. Quá trình toàn cầu hóa đô thị và sự theo đuổi công năng thuần túy đã nhanh chóng đồng nhất hóa phong vị lịch sử và tính đa dạng văn hóa độc đáo vốn có của từng vùng miền.<br><br>Nguyên nhân chính dẫn đến sự rập khuôn của không gian đô thị như thế này nằm ở chỗ: hiệu quả kinh tế và việc tối đa hóa lợi nhuận ngắn hạn đã bị coi là mệnh lệnh tối thượng của phát triển đô thị. Chi phí bảo tồn phố cổ và văn hóa thủ công truyền thống bị gạt bỏ với danh nghĩa 'kém hiệu quả', nhường chỗ cho các tổ hợp thương mại quy chuẩn hóa. Hệ quả là các đô thị đã đánh mất linh hồn bản địa, biến thành những không gian vô hồn có thể thay thế ở bất kỳ đâu."
    },
    {
      "id": "skz_ch05_q03",
      "chapter": "第5章：理由・因果関係",
      "title": "第5章 練習 3",
      "mondaiType": "medium",
      "passage": "インターネットとソーシャルメディアの普及は、誰もが瞬時に膨大な情報へアクセスできる情報民主化の時代をもたらした。知りたいことがあれば即座に検索し、世界中の専門知識やニュースを手に入れることができる。しかし、皮肉なことに、流通する情報量が爆発的に増大したにもかかわらず、人々の主体的な思考力や的確な判断力はむしろ低下しているのではないかという懸念が強まっている。\n\nこの問題が生じる理由は、過剰な情報刺激の洪水が、人間が深く思索するために不可欠な「認知的余白」を奪い去っているからである。次々と流れてくるセンセーショナルな見出しや断片的な情報を受動的にスクロールし続けることで、脳は情報の真偽を吟味したり論理的な整合性を検討したりする前に、過負荷に陥ってしまうのだ。自ら問いを立て、粘り強く考え抜くプロセスを省き、アルゴリズムが提示する手軽な要約や他人の意見をそのまま自己の意見と錯覚してしまう現象は、まさにこの知的怠惰に起因している。\n\n真に知識を血肉とし、独自の知性を磨くためには、意識的に情報摂取の量を絞り込み、得た情報を自らの頭の中で反芻する「遅い思考」の時間を取り戻さなければならない。",
      "question": "情報が氾濫する現代において、人々の主体的思考力が低下してしまう原因は何か。",
      "options": [
        "専門知識の難易度が高すぎて、一般の利用者が内容を正しく理解できないから。",
        "インターネット上の情報の大半が虚偽であり、正しい知識を得る手段が制限されているから。",
        "過剰な情報刺激により思考の余白が奪われ、真偽や論理を吟味せず受動的に受け入れてしまうから。",
        "検索エンジンのアルゴリズムが未熟なため、質の高い情報が検索結果に表示されないから。"
      ],
      "answer": 3,
      "logicHighlights": {
        "counterPremise": "流通する情報量が爆発的に増大したにもかかわらず、人々の主体的な思考力や的確な判断力はむしろ低下しているのではないか",
        "turningPoint": "この問題が生じる理由は",
        "authorConclusion": "意識的に情報摂取の量を絞り込み、得た情報を自らの頭の中で反芻する「遅い思考」の時間を取り戻さなければならない"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Lệch hướng): Bài viết không nói do chuyên môn quá khó hiểu.",
        "opt2": "❌ BẪY TƯ DUY (Nói quá đà): Tác giả không bảo phần lớn thông tin mạng là tin giả.",
        "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp hoàn toàn với lý giải của tác giả: lượng kích thích thông tin quá tải cướp đi khoảng trống nhận thức (認知的余白), khiến não bộ bị quá tải trước khi kịp thẩm định tính logic và chân ngụy.",
        "opt4": "❌ BẪY TƯ DUY (Đổ lỗi cho thuật toán kỹ thuật): Vấn đề nằm ở thói quen tiếp nhận thụ động của con người, không phải thuật toán chưa đủ hoàn thiện."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Sự phổ biến của Internet và mạng xã hội đã mở ra kỷ nguyên dân chủ hóa thông tin, nơi bất kỳ ai cũng có thể tức thời tiếp cận lượng thông tin khổng lồ. Hễ có điều gì muốn biết là có thể lập tức tra cứu. Thế nhưng, trớ trêu thay, bất chấp việc lượng thông tin lưu hành bùng nổ, mối lo ngại về việc năng lực tư duy chủ động và phán đoán chuẩn xác của con người đang suy giảm lại ngày càng dâng cao.<br><br>Lý do nảy sinh vấn đề này là vì cơn lũ kích thích thông tin thái quá đang cướp đoạt đi 'khoảng trống nhận thức' vốn dĩ thiết yếu để con người suy ngẫm sâu sắc. Bằng việc cứ tiếp tục cuộn chuột thụ động xem qua những tiêu đề giật gân và mẩu tin vụn vặt trôi dạt liên hồi, não bộ sẽ rơi vào tình trạng quá tải trước khi kịp cân nhắc tính chân ngụy hay thẩm tra tính nhất quán logic. Hiện tượng lược bỏ quy trình tự đặt câu hỏi và kiên trì suy nghĩ đến cùng, rồi ngộ nhận những bản tóm tắt tiện lợi của thuật toán hay ý kiến người khác thành ý kiến của mình, bắt nguồn chính từ sự lười biếng trí tuệ này.<br><br>Để thực sự biến tri thức thành máu thịt và mài giũa trí tuệ độc lập, ta phải có ý thức chắt lọc lượng thông tin nạp vào, lấy lại khoảng thời gian 'tư duy chậm' để nhai đi nhai lại thông tin trong chính bộ não của mình."
    },
    {
      "id": "skz_ch05_q04",
      "chapter": "第5章：理由・因果関係",
      "title": "第5章 練習 4",
      "mondaiType": "short",
      "passage": "対面でのコミュニケーションにおいて、私たちは言葉そのものよりも、相手の視線や声のトーン、微細な表情の変化といった非言語的な合図から、より多くの情報を直感的に読み取っている。心理学の実験でも、言語情報と非言語情報が矛盾した場合、聞き手は圧倒的に非言語情報を信頼することが示されている。\n\nこれは、言語が理性の産物であり意識的に嘘をつくことが容易であるのに対し、身体的な反応や無意識の仕草は感情の動きに直結しており、偽ることが極めて困難だからである。つまり、信頼関係の構築において非言語コミュニケーションが決定的役割を果たすのは、身体が言葉よりもはるかに嘘をつかない誠実な語り手だからなのだ。",
      "question": "非言語情報が言語情報よりも強く信頼されるのはなぜか。",
      "options": [
        "非言語情報は理性的な分析に基づく客観的な事実を表しているから。",
        "言語は意識的に偽ることができるが、身体反応は感情に直結し偽ることが困難だから。",
        "対面での会話では、言葉の意味を理解するよりも表情を観察するほうが簡単だから。",
        "現代社会では言葉によるコミュニケーション能力が全般的に低下しているから。"
      ],
      "answer": 2,
      "logicHighlights": {
        "counterPremise": "聞き手は圧倒的に非言語情報を信頼することが示されている",
        "turningPoint": "これは、〜からである",
        "authorConclusion": "信頼関係の構築において非言語コミュニケーションが決定的役割を果たすのは、身体が言葉よりもはるかに嘘をつかない誠実な語り手だからなのだ"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đảo ngược tính chất): Ngôn ngữ mới là sản phẩm lý tính (理性の産物), còn phi ngôn ngữ gắn với cảm xúc tự nhiên.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với cấu trúc giải thích: 「言語が理性の産物であり意識的に嘘をつくことが容易であるのに対し、身体的な反応や無意識の仕草は感情の動きに直結しており、偽ることが極めて困難だからである」.",
        "opt3": "❌ BẪY TƯ DUY (Lý do chủ quan ngớ ngẩn): Không phải vì nhìn mặt dễ hơn hiểu chữ.",
        "opt4": "❌ BẪY TƯ DUY (Suy diễn không liên quan): Bài không bàn về sự suy giảm năng lực ngôn ngữ của xã hội."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Trong giao tiếp trực diện, con người trực giác đọc được nhiều thông tin hơn từ những tín hiệu phi ngôn ngữ như ánh mắt, tông giọng, hay biến đổi vi mô trên nét mặt của đối phương hơn là câu chữ đơn thuần. Trong các thí nghiệm tâm lý học, khi thông tin ngôn ngữ và phi ngôn ngữ mâu thuẫn nhau, người nghe áp đảo chọn tin vào thông tin phi ngôn ngữ.<br><br>Điều này là bởi vì trong khi ngôn từ là sản phẩm của lý tính và rất dễ để cố ý nói dối, thì phản ứng thân thể và cử chỉ vô thức lại gắn liền trực tiếp với chuyển động cảm xúc, cực kỳ khó để giả tạo. Nói cách khác, giao tiếp phi ngôn ngữ đóng vai trò quyết định trong việc xây dựng lòng tin chính là vì thân thể là một người kể chuyện thành thật, ít biết nói dối hơn nhiều so với ngôn từ."
    }
  ]
}

# ==============================================================================
# CHAPTER 6: 第6章：実践演習・総合理解 (Luyện thực chiến: Đoản, Trung, Trường, So sánh, Tìm tin)
# ==============================================================================
ch06_data = {
  "chapterId": "ch06",
  "chapter": "第6章：実践演習・総合理解",
  "title": "Chương 6: Luyện thực chiến & Đọc hiểu tổng hợp (実践演習・総合理解)",
  "description": "Tổng hợp trọn bộ các dạng thức đề thi JLPT N1 Dokkai thực chiến: Đoản văn (短文), Trung văn (中文), Trường văn (長文), So sánh văn bản tích hợp (統合理解 A-B) và Tìm kiếm thông tin (情報検索).",
  "totalQuestions": 4,
  "questions": [
    {
      "id": "skz_ch06_q01",
      "chapter": "第6章：実践演習・総合理解",
      "title": "第6章 練習 1（中文）",
      "mondaiType": "medium",
      "passage": "私たちは時計という人工的な機械によって測定される「均質な時間」を自明のものとして生きている。一日は24時間、一時間は60分として厳密に等分され、すべての行動はその目盛りに従って秩序づけられる。この近代的な時間規律のおかげで、社会の組織的協調や産業活動は驚異的な同期と効率化を達成することができた。\n\nしかし、この時計の時間が絶対化した代償として、人間は内面的な「生の主観的リズム」を切り捨ててしまった。自然界に目を向ければ、春の訪れとともに芽吹き、冬の寒さの中で眠りにつく生命のサイクルは、決して機械的な均等さでは測れない。人間自身の心や身体もまた、情熱に駆られて没頭するときには時間は瞬く間に過ぎ去り、苦痛や思索に沈むときには一刻が永遠のように引き伸ばされる独自の「質的な時間」を生きているはずなのだ。\n\n均等に細切れにされたスケジュールに心身を無理に適合させ続ける現代人は、自らの生命が発する固有のテンポを見失った「時間の難民」と言えるかもしれない。今求められているのは、時計の支配から自律を取り戻し、自分自身の内なる時間に耳を澄ませる勇気である。",
      "question": "近代的な「時計の時間」と人間の関係について、筆者の主張として最も適切なものはどれか。",
      "options": [
        "時計の時間がもたらした効率性は人間の幸福そのものであり、主観的な時間感覚は克服されるべき非合理である。",
        "社会秩序を維持するためには個人の内面的なリズムを優先すべきではなく、厳密な時間管理を徹底すべきである。",
        "均質な時計の時間に過度に適合した結果、人間は心身の固有な質的リズムを見失っており、内なる時間を取り戻す必要がある。",
        "自然界のサイクルと機械の時間は完全に一致しており、時計の目盛りに従うことこそが自然な生き方である。"
      ],
      "answer": 3,
      "logicHighlights": {
        "counterPremise": "この近代的な時間規律のおかげで、社会の組織的協調や産業活動は驚異的な同期と効率化を達成することができた",
        "turningPoint": "しかし、この時計の時間が絶対化した代償として",
        "authorConclusion": "今求められているのは、時計の支配から自律を取り戻し、自分自身の内なる時間に耳を澄ませる勇気である"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đồng hóa tiền đề đã bị phê phán): Tác giả chỉ trích việc biến thời gian đồng hồ thành tuyệt đối.",
        "opt2": "❌ BẪY TƯ DUY (Trái ngược lập luận): Tác giả cảnh báo con người đang trở thành 'người tị nạn của thời gian' do quá kỷ luật máy móc.",
        "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với thông điệp: con người đang đánh mất nhịp điệu sinh mệnh chất lượng riêng do quá gượng ép tuân theo thời gian đồng hồ cơ học, cần phải lấy lại quyền tự chủ thời gian nội tại.",
        "opt4": "❌ BẪY TƯ DUY (Xuyên tạc sự thật trong bài): Bài nêu rõ nhịp điệu thiên nhiên không thể đo bằng sự đều đặn máy móc."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Chúng ta đang sống và coi 'thời gian đồng nhất' được đo lường bằng cỗ máy nhân tạo mang tên đồng hồ là điều hiển nhiên. Một ngày được chia đều tăm tắp thành 24 giờ, một giờ là 60 phút, và mọi hành vi được trật tự hóa theo từng vạch chia ấy. Nhờ kỷ luật thời gian cận đại này, sự phối hợp tổ chức và hoạt động sản xuất công nghiệp của xã hội mới đạt được sự đồng bộ và tối ưu hóa phi thường.<br><br>Thế nhưng, như một cái giá phải trả cho sự tuyệt đối hóa thời gian đồng hồ, con người đã vứt bỏ 'nhịp điệu sinh mệnh chủ quan' trong nội tâm. Hướng mắt ra thế giới tự nhiên, chu kỳ của sự sống đâm chồi vào mùa xuân và chìm vào giấc ngủ giữa đông buốt giá tuyệt nhiên không thể đo đếm bằng sự chia đều máy móc. Bản thân tâm trí và thân thể con người vốn dĩ cũng sống trong một 'thời gian định tính' độc đáo: khi say mê đắm chìm thì thời gian vút qua trong chớp mắt, khi đớn đau hay trầm tư thì một khoảnh khắc dài tựa thiên thu.<br><br>Những người hiện đại cứ ép uổng thân tâm mình phải thích nghi với những lịch trình bị băm nhỏ đều đặn có lẽ chính là những 'người tị nạn thời gian' đã đánh mất tiết tấu nội tại của sinh mệnh. Điều cần kíp lúc này là lòng dũng cảm lấy lại quyền tự chủ khỏi sự thống trị của đồng hồ, để lắng nghe thời gian nội tâm của chính mình."
    },
    {
      "id": "skz_ch06_q02",
      "chapter": "第6章：実践演習・総合理解",
      "title": "第6章 練習 2（長文）",
      "mondaiType": "long",
      "passage": "インターネットの普及とデジタルテクノロジーの進化は、人間の「共同体」のあり方を根底から変容させた。地理的な制約に縛られることなく、地球の裏側にいる他者と共通の趣味や関心で瞬時につながり合えるバーチャルなコミュニティは、個人の自由をかつてないほど拡張したかに見えた。\n\nしかし、物理的な空間を共有しないデジタルなつながりには、決定的な要素が欠落している。それは、「偶発的な出会い」と「厄介さの引き受け」である。オンライン空間では、アルゴリズムによって最適化された同質的な意見ばかりが反響し合う「エコーチェンバー」に陥りやすく、自分が不快と感じる異質な他者はワンクリックで遮断することができる。そこには、他者の存在の手触りや、意見の衝突を粘り強くすり合わせる中で生まれる生の摩擦が存在しない。\n\n古来、人間が育んできた真の「居場所」とは、単に自分にとって心地よい賛同者ばかりが集まるサロンではなかったはずだ。そこには、時に意見が合わず、煩わしく思える他者もまた同じ空間に実在し、そうした厄介さを引き受け合いながら互いの存在を認め合う重層的な関係性の網の目があったのだ。\n\n身体を伴った物理的な空間での他者との交わりを軽視し、都合の良いデジタルな関係性だけに逃避し続けるならば、私たちの社会は個別に分断され、他者への寛容さを失った不毛な孤立の集合体へと退行してしまうだろう。今こそ、面倒で思い通りにならない「生身の他者」と共に生きる場所の尊厳を問い直さなければならない。",
      "question": "物理的な空間における「居場所」の意義について、筆者の見解として最も適切なものはどれか。",
      "options": [
        "デジタル空間と完全に一致しており、同質な関心を持つ仲間と効率的に交流するための快適な環境である。",
        "煩わしい人間関係を排除し、個人の自由とプライバシーを完全に保障する安全なサロンである。",
        "意見の不一致や厄介さも含めて生身の他者と身体を共有し、摩擦を通じて相互承認を育む場である。",
        "地理的な制約を完全に克服し、全世界のあらゆる人々と衝突なしに調和するための架け橋である。"
      ],
      "answer": 3,
      "logicHighlights": {
        "counterPremise": "地理的な制約に縛られることなく、地球の裏側にいる他者と共通の趣味や関心で瞬時につながり合えるバーチャルなコミュニティは、個人の自由をかつてないほど拡張したかに見えた",
        "turningPoint": "しかし、物理的な空間を共有しないデジタルなつながりには、決定的な要素が欠落している",
        "authorConclusion": "今こそ、面倒で思い通りにならない「生身の他者」と共に生きる場所の尊厳を問い直さなければならない"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đánh tráo với không gian ảo): Đây là đặc điểm của cộng đồng mạng đồng nhất mà tác giả chỉ trích.",
        "opt2": "❌ BẪY TƯ DUY (Trái ngược bản chất): Tác giả khẳng định chốn dung thân chân thực không phải là cái salon êm ấm trốn tránh phiền hà.",
        "opt3": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với tư tưởng trường văn: chốn thuộc về vật lý là nơi cùng chia sẻ thân xác với tha nhân bằng xương bằng thịt, chấp nhận cả sự bất đồng và phiền toái, qua đó tôi luyện sự thừa nhận lẫn nhau.",
        "opt4": "❌ BẪY TƯ DUY (Lý tưởng hóa hão huyền): Bài đọc nhấn mạnh sự va chạm đời thực đầy phiền toái, không phải sự hài hòa không xung đột."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc】:</b><br>Sự phổ biến của Internet và công nghệ số đã làm biến đổi tận gốc rễ phương thức tồn tại của 'cộng đồng' loài người. Các cộng đồng ảo nơi con người có thể kết nối tức thời qua sở thích chung mà không bị trói buộc bởi rào cản địa lý thoạt nhìn như mở rộng tự do cá nhân hơn bao giờ hết.<br><br>Thế nhưng, những kết nối số không cùng chia sẻ không gian vật lý lại thiếu vắng những yếu tố mang tính quyết định: đó là 'sự hội ngộ ngẫu nhiên' và 'việc chấp nhận những phiền toái'. Trong không gian mạng, người ta rất dễ rơi vào 'phòng dội âm' nơi thuật toán chỉ phản hồi những quan điểm đồng điệu, còn những tha nhân dị biệt khiến ta khó chịu thì có thể chặn đứng chỉ bằng một cú nhấp chuột. Ở đó không có cảm giác chân thực về sự hiện diện của người khác, cũng chẳng có sự ma sát sống động vốn được sinh ra từ quá trình kiên trì dàn xếp xung đột.<br><br>Tự cổ chí kim, một 'chốn thuộc về' thực sự mà con người vun đắp đâu phải chỉ là một phòng khách êm ái quy tụ toàn những kẻ tán đồng mình. Ở đó, ngay cả những người đôi khi bất đồng ý kiến, những kẻ ta thấy phiền toái cũng cùng tồn tại trong một không gian thực, tạo nên mạng lưới quan hệ đa tầng nơi người ta cùng gánh vác sự phiền phức để công nhận sự hiện diện của nhau.<br><br>Nếu cứ tiếp tục coi nhẹ việc giao tiếp có cơ thể trong không gian vật lý mà trốn tránh vào những mối quan hệ số thuận tiện, xã hội chúng ta sẽ bị phân mảnh thành tập hợp những kẻ cô lập cằn cỗi đánh mất lòng khoan dung. Đã đến lúc phải nhìn nhận lại phẩm giá của chốn cùng chung sống với những 'tha nhân bằng xương bằng thịt' - những con người phiền phức và không bao giờ chiều theo ý mình."
    },
    {
      "id": "skz_ch06_q03",
      "chapter": "第6章：実践演習・総合理解",
      "title": "第6章 練習 3（統合理解 A-B）",
      "mondaiType": "compare",
      "passage": "【A】\nテレワークの普及は、通勤ラッシュの疲労から労働者を解放し、ワークライフバランスの改善に大きく寄与した。場所を選ばずに業務を遂行できる柔軟性は、育児や介護とキャリアの両立を容易にし、個人の自律的な時間管理を促している。デジタルツールを活用した業務効率化が進む現代において、オフィスという一箇所に全員が集まることを強制する従来の働き方はもはや過去の遺物であり、完全なリモートワークへの移行こそが未来の標準となるべきである。\n\n【B】\n確かにリモートワークは定型的な業務処理においては高い効率を発揮する。しかし、革新的なアイディアの創出や強固な組織の信頼関係は、画面越しの計画的な会議だけでは育まれない。廊下ですれ違った際の一言の雑談や、同じ空間で共に汗を流す中で共有される暗黙の空気感こそが、創造的な協働の起爆剤となるのだ。オフィスは単なる作業場ではなく、偶発的な対話を生み出す社会的な触媒であり、その価値を過小評価して完全なオンライン化を進めることには慎重であるべきだ。",
      "question": "リモートワークとオフィスの存在意義について、AとBの主張を比較したものとして最も適切なものはどれか。",
      "options": [
        "AもBも、業務の効率化と社員のワークライフバランスを最優先し、オフィスを完全に撤廃すべきだという点で一致している。",
        "Aはリモートワークこそが未来の標準だと全面肯定しているのに対し、Bは雑談や偶発的対話を生む場としてオフィスの独自の価値を主張している。",
        "Aはオフィスの対面コミュニケーションの重要性を強調し、Bは通勤の負担を軽減するために完全な在宅勤務を推奨している。",
        "AもBも、オンライン会議ではアイディアの創出が不可能であるため、全従業員がオフィスに出社すべきだと主張している。"
      ],
      "answer": 2,
      "logicHighlights": {
        "counterPremise": "【A】オフィスという一箇所に全員が集まることを強制する従来の働き方はもはや過去の遺物であり、完全なリモートワークへの移行こそが未来の標準となるべきである",
        "turningPoint": "【B】確かにリモートワークは定型的な業務処理においては高い効率を発揮する。しかし",
        "authorConclusion": "【B】オフィスは単なる作業場ではなく、偶発的な対話を生み出す社会的な触媒であり、その価値を過小評価して完全なオンライン化を進めることには慎重であるべきだ"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Đồng nhất hóa sai lệch): B không hề muốn xóa bỏ văn phòng mà bảo vệ giá trị của văn phòng.",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với so sánh 2 văn bản: A ủng hộ hoàn toàn làm từ xa xem văn phòng là tàn tích, trong khi B chỉ ra văn phòng có vai trò xúc tác xã hội tạo ra đối thoại ngẫu nhiên và sáng tạo mà online không thay thế được.",
        "opt3": "❌ BẪY TƯ DUY (Đảo ngược lập trường giữa A và B): A là người ủng hộ từ xa, B mới là người bảo vệ văn phòng.",
        "opt4": "❌ BẪY TƯ DUY (Sai lệch cả hai): A nhiệt liệt ủng hộ online chứ không bắt mọi người lên công ty."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc So sánh A-B】:</b><br><b>【Văn bản A】:</b> Việc phổ biến làm việc từ xa (telework) đã giải phóng người lao động khỏi nỗi ám ảnh kẹt xe tàu điện giờ cao điểm, đóng góp lớn vào cân bằng công việc - cuộc sống. Sự linh hoạt trong địa điểm làm việc giúp việc vừa chăm con hay chăm sóc người thân vừa thăng tiến sự nghiệp trở nên dễ dàng. Cách làm việc truyền thống bắt ép toàn bộ nhân viên tụ về một chỗ tại văn phòng nay đã là tàn tích của quá khứ, và việc chuyển dịch hoàn toàn sang làm việc từ xa nên trở thành tiêu chuẩn tương lai.<br><br><b>【Văn bản B】:</b> Quả thật làm việc từ xa phát huy hiệu suất cao trong các tác vụ xử lý theo quy trình cố định. Tuy nhiên, việc sản sinh các ý tưởng đổi mới sáng tạo và gây dựng lòng tin tổ chức vững chắc lại không thể nuôi dưỡng chỉ bằng những cuộc họp lên lịch sẵn qua màn hình. Những câu tán gẫu ngẫu nhiên khi lướt qua nhau ở hành lang hay bầu không khí ngầm hiểu khi cùng chung một phòng làm việc mới chính là ngòi nổ cho sự cộng tác sáng tạo. Văn phòng không chỉ là nơi làm việc đơn thuần, nó là chất xúc tác xã hội tạo ra đối thoại ngẫu nhiên, và ta cần hết sức thận trọng trước việc coi nhẹ giá trị ấy để thúc đẩy số hóa toàn bộ."
    },
    {
      "id": "skz_ch06_q04",
      "chapter": "第6章：実践演習・総合理解",
      "title": "第6章 練習 4（情報検索）",
      "mondaiType": "search",
      "passage": "【国際文化交流財団・海外研究助成プログラム 募集要項（抜粋）】\n\n1. 助成対象者：\n・日本国内の大学院に在籍する大学院生（修士課程または博士課程）、または大学等で研究に従事する35歳未満の若手研究者。\n・過去に本財団の助成を受けたことがない者。\n\n2. 助成金額及び期間：\n・上限150万円（渡航費、現地滞在費、研究資料収集費を含む）。\n・現地滞在期間は3ヶ月以上1年以内とする。\n\n3. 申請手続きと締切：\n・申請期間：2026年4月1日〜5月15日（消印有効）。\n・提出書類：申請書、指導教員の推薦書（1通）、研究計画書（書式自由、A4で3枚以内）。\n※大学院生は在学証明書の添付が必須。\n\n4. 注意事項：\n・他機関からの助成金と本プログラムの重複受給は不可（併願は可能だが採択時に辞退手続きが必要）。\n・助成期間終了後、2ヶ月以内に研究成果報告書及び会計報告書を提出すること。",
      "question": "本助成プログラムの申請条件および手続きについて、適切なものはどれか。",
      "options": [
        "過去に本財団の助成を受けたことがある者でも、研究テーマが異なれば再度の申請が可能である。",
        "他機関の助成金と併願して申請することは認められているが、採択された場合は重複して受け取ることはできない。",
        "大学院生の場合、指導教員の推薦書は不要であり、在学証明書と研究計画書のみを提出すればよい。",
        "現地滞在期間は最短で1ヶ月から申請可能であり、助成金の上限は200万円である。"
      ],
      "answer": 2,
      "logicHighlights": {
        "counterPremise": "他機関からの助成金と本プログラムの重複受給は不可",
        "turningPoint": "（併願は可能だが採択時に辞退手続きが必要）",
        "authorConclusion": "他機関の助成金と併願して申請することは認められているが、採択された場合は重複して受け取ることはできない"
      },
      "trapBreakdown": {
        "opt1": "❌ BẪY TƯ DUY (Trái ngược điều kiện 1): Mục 1 ghi rõ: 「過去に本財団の助成を受けたことがない者」 (Người chưa từng nhận trợ cấp của quỹ).",
        "opt2": "✓ ĐÁP ÁN ĐÚNG: Khớp chính xác với mục 4: 「他機関からの助成金と本プログラムの重複受給は不可（併願は可能だが採択時に辞退手続きが必要）」 (Được nộp cùng lúc nhiều nơi nhưng khi đỗ không được nhận song song).",
        "opt3": "❌ BẪY TƯ DUY (Trái ngược mục 3): Thư giới thiệu của giáo viên hướng dẫn (推薦書) là bắt buộc cho tất cả người nộp.",
        "opt4": "❌ BẪY TƯ DUY (Sai số liệu mục 2): Thời gian ở thực địa tối thiểu là 3 tháng (không phải 1 tháng) và trần kinh phí là 150 vạn yên (không phải 200 vạn)."
      },
      "explanation": "<b>【Dịch nghĩa bài đọc Tìm kiếm thông tin (情報検索)】:</b><br><b>【Quy chế chương trình Trợ cấp Nghiên cứu Nước ngoài (Trích yếu)】:</b><br>1. <b>Đối tượng:</b> Học viên cao học (Thạc sĩ hoặc Tiến sĩ) tại các trường đại học Nhật Bản, hoặc nhà nghiên cứu trẻ dưới 35 tuổi. Chưa từng nhận trợ cấp của quỹ trong quá khứ.<br>2. <b>Mức trợ cấp & thời hạn:</b> Tối đa 1.500.000 yên. Thời gian lưu trú từ 3 tháng đến 1 năm.<br>3. <b>Thủ tục & hạn nộp:</b> Từ 1/4/2026 đến 15/5/2026. Hồ sơ gồm đơn đăng ký, 1 thư giới thiệu của giảng viên hướng dẫn, đề cương nghiên cứu (A4 tối đa 3 trang). Học viên cao học bắt buộc đính kèm giấy chứng nhận đang theo học.<br>4. <b>Lưu ý:</b> Không được nhận trùng lặp với học bổng/trợ cấp của cơ quan khác (cho phép nộp song song nhiều nơi, nhưng khi được chọn phải làm thủ tục từ chối nơi kia). Phải nộp báo cáo nghiên cứu và quyết toán trong vòng 2 tháng sau khi kết thúc đợt lưu trú."
    }
  ]
}

# Write files
files_to_write = [
  ('shinkanzen_ch03.json', ch03_data),
  ('shinkanzen_ch04.json', ch04_data),
  ('shinkanzen_ch05.json', ch05_data),
  ('shinkanzen_ch06.json', ch06_data)
]

for filename, content in files_to_write:
  file_path = os.path.join(data_dir, filename)
  with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(content, f, ensure_ascii=False, indent=2)
  print(f"[CREATED] {file_path}")

# Update dokkai-index.json
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
    "totalQuestions": 4,
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
    "totalQuestions": 4,
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
    "totalQuestions": 4,
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
    "totalQuestions": 4,
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
    "totalQuestions": 4,
    "types": ["short", "medium"]
  },
  {
    "id": "skz_ch06",
    "chapterNumber": 6,
    "chapter": "第6章：実践演習・総合理解",
    "title": "Luyện thực chiến & Đọc hiểu tổng hợp (実践演習・総合理解)",
    "theme": "Trọn bộ định dạng thi N1: Đoản văn, Trung văn, Trường văn, So sánh A-B, Tìm thông tin",
    "description": "Luyện tập tổng hợp với các dạng bài thi thực chiến của Shin Kanzen Master Dokkai N1 dưới áp lực phòng thi thật.",
    "file": "data/n1_dokkai/shinkanzen_ch06.json",
    "available": True,
    "totalQuestions": 4,
    "types": ["short", "medium", "long", "compare", "search"]
  }
]

index_path = os.path.join(data_dir, 'dokkai-index.json')
with open(index_path, 'w', encoding='utf-8') as f:
  json.dump(index_data, f, ensure_ascii=False, indent=2)
print(f"[UPDATED] {index_path}")
