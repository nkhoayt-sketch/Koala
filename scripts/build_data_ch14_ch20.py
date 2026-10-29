# -*- coding: utf-8 -*-
import bs4, json, sys, os

def extract_from_html(file_path, ch_id, lesson_title, theme, group):
    soup = bs4.BeautifulSoup(open(file_path, encoding='utf-8', errors='ignore'), 'html.parser')
    q_nodes = soup.find_all(lambda t: t.name == 'div' and ('question' in t.get('class', []) or 'q-card' in t.get('class', [])))
    questions = []
    
    for idx, node in enumerate(q_nodes):
        q_id = f'skz_b_{ch_id}_q{idx+1:02d}'
        ans = node.get('data-ans', '').strip().lower()
        exp = node.get('data-exp', '').strip()
        sec = node.get('data-sec', '').strip()
        
        q_text_el = node.find(class_=lambda c: c and any(k in c for k in ['text', 'japanese', 'title', 'stem', 'q-japanese', 'q-text']))
        if q_text_el:
            q_text = q_text_el.get_text().strip()
        else:
            lines = [l.strip() for l in node.get_text('\n').split('\n') if l.strip()]
            q_text = lines[0] if lines else ''
            
        labels = node.find_all('label')
        opts = []
        for l in labels:
            t = l.get_text().strip()
            # clean labels
            cleaned = t
            for p in ['a.', 'b.', 'c.', 'a', 'b', 'c']:
                if cleaned.startswith(p):
                    cleaned = cleaned[len(p):].strip()
                    break
            prefix = ['a. ', 'b. ', 'c. '][len(opts)] if len(opts) < 3 else ''
            opts.append(prefix + cleaned)
            
        gp = sec or 'Shin Kanzen Master N1'
        if not exp:
            exp = f'【Dịch & Phân tích】Đáp án đúng là ({ans}). Câu hỏi thuộc bài {lesson_title}.'
            
        rule = 'Quy tắc ngữ pháp Shin Kanzen Master N1.'
        if 'ひきかえ' in q_text:
            rule = 'N ＋ の / 普 ＋ にひきかえ: So sánh đối chiếu hai sự việc tương phản.'
        elif '至って' in q_text:
            rule = 'V-る / N ＋ に至って: Mãi cho đến khi... thì mới.'
        elif 'っぱなし' in q_text:
            rule = 'V-ます (bỏ ます) ＋ っぱなし: Giữ nguyên trạng thái xấu kéo dài.'
        elif '始末だ' in q_text:
            rule = 'V-る ＋ 始末だ: Rốt cuộc dẫn tới kết cục thảm hại.'
        elif 'たりとも' in q_text:
            rule = '1 ＋ Đơn vị đếm ＋ たりとも...ない: Dù chỉ một... cũng không.'
        elif 'すら' in q_text or 'だに' in q_text:
            rule = 'N ＋ すら / だに: Ngay cả, thậm chí.'
        elif 'てやまない' in q_text:
            rule = 'V-て ＋ やまない: Luôn hy vọng/cầu chúc không nguôi.'
        elif 'に堪えない' in q_text:
            rule = 'N ＋ に堪えない: Không kìm nén nổi cảm xúc.'
        elif 'までもない' in q_text:
            rule = 'V-る ＋ までもない: Không cần thiết phải làm.'
        elif 'に足る' in q_text:
            rule = 'V-る / N ＋ に足る: Đáng để làm gì.'
        elif 'ときたら' in q_text:
            rule = 'N ＋ ときたら: Nhắc đến... là chỉ phàn nàn chê bai.'
        elif 'ともなると' in q_text or 'ともなれば' in q_text:
            rule = 'N ＋ ともなると: Một khi đã đạt tới mức độ đó.'
            
        questions.append({
            'id': q_id,
            'lesson': lesson_title,
            'grammarPoint': gp,
            'question': q_text,
            'options': opts[:3],
            'answer': ans,
            'explanation': exp,
            'grammarRule': rule
        })
    return {
        'chapterId': ch_id,
        'lesson': lesson_title,
        'theme': theme,
        'group': group,
        'title': lesson_title,
        'description': f'Bài tập ngữ pháp chuẩn sách giáo trình Shin Kanzen Master Bunpou N1 ({lesson_title}).',
        'questions': questions
    }

ch14_data = extract_from_html('D:/N1/Bưng bô/quiz14.html', 'ch14', '第14課: 話題・評価の基準', '主観を含めて説明する', 'group2')
ch15_data = extract_from_html('D:/N1/Bưng bô/15.html', 'ch15', '第15課: 比較対照', '主観を含めて説明する', 'group2')
ch16_data = extract_from_html('D:/N1/Bưng bô/16.html', 'ch16', '第16課: 結末・最終の状態', '主観を含めて説明する', 'group2')
ch17_data = extract_from_html('D:/N1/Bưng bô/17.html', 'ch17', '第17課: 評価・感想', '主観を述べる', 'group3')
ch18_data = extract_from_html('D:/N1/Bưng bô/18.html', 'ch18', '第18課: 心情・強制的思い', '主観を述べる', 'group3')
ch19_data = extract_from_html('D:/N1/Bưng bô/19.html', 'ch19', '第19課: 強調', '主観を述べる', 'group3')

# Chapter 20: 主張・断定
ch20_qs = [
    {
        'id': 'skz_b_ch20_q01',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～にほかならない',
        'question': '今回の成功は、チーム全員の弛まぬ努力の賜物（　）にほかならない。',
        'options': ['a. ', 'b. だ', 'c. な'],
        'answer': 'a',
        'explanation': '【Dịch】Thành công rực rỡ lần này chính là kết tinh từ những nỗ lực không ngừng nghỉ của toàn thể đội ngũ, không gì khác ngoài điều đó.\n【Phân tích】N ＋ にほかならない: Chính là... không gì khác hơn.',
        'grammarRule': 'N / から ＋ にほかならない: Chính là, không gì khác hơn là (khẳng định dứt khoát nguyên nhân duy nhất).'
    },
    {
        'id': 'skz_b_ch20_q02',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～にほかならない',
        'question': '親が子供を厳しく叱るのは、子供の将来を深く案じる愛情から（　）。',
        'options': ['a. にほかならない', 'b. にすぎない', 'c. ざるを得ない'],
        'answer': 'a',
        'explanation': '【Dịch】Việc cha mẹ nghiêm khắc quở trách con cái chính là xuất phát từ tình yêu thương lo lắng sâu sắc cho tương lai của con, không gì khác ngoài điều ấy.\n【Phân tích】Khẳng định nguyên nhân duy nhất xuất phát từ tình yêu thương: 愛情からにほかならない.',
        'grammarRule': 'から ＋ にほかならない: Chính là xuất phát từ lý do ấy.'
    },
    {
        'id': 'skz_b_ch20_q03',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～にすぎない',
        'question': 'いくら富や名声を得たとしても、それは人生のほんの一幕（　）にすぎない。',
        'options': ['a. ', 'b. だ', 'c. な'],
        'answer': 'a',
        'explanation': '【Dịch】Dù có đạt được bao nhiêu giàu sang và danh vọng đi nữa, điều đó cũng chỉ là một màn kịch ngắn ngủi trong cõi nhân sinh mà thôi.\n【Phân tích】N / 普通形 ＋ にすぎない: Chỉ là... không hơn không kém (đánh giá mức độ bình thường, nhỏ bé).',
        'grammarRule': 'N / 普 ＋ にすぎない: Chỉ đơn thuần là... (không có gì to tát, chỉ có thế).'
    },
    {
        'id': 'skz_b_ch20_q04',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～にすぎない',
        'question': 'わたしは単に事実をありのままに報告した（　）。',
        'options': ['a. にすぎない', 'b. にほかならない', 'c. ずにはおかない'],
        'answer': 'a',
        'explanation': '【Dịch】Tôi chẳng qua cũng chỉ thuật lại sự thật đúng như những gì đã diễn ra mà thôi.\n【Phân tích】Đơn thuần chỉ là báo cáo sự thật: 報告したにすぎない.',
        'grammarRule': 'V-た ＋ にすぎない: Chẳng qua chỉ là...'
    },
    {
        'id': 'skz_b_ch20_q05',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～ずにはおかない',
        'question': '彼の圧倒的な熱演は、観客全員に深い感動を与えずには（　）。',
        'options': ['a. おかない', 'b. いない', 'c. すまない'],
        'answer': 'a',
        'explanation': '【Dịch】Màn diễn xuất đầy lửa và thăng hoa tột bậc của anh ấy chắc chắn sẽ khiến toàn thể khán giả phải rung động sâu sắc không thể kìm nén được.\n【Phân tích】V-ない (bỏ ない) ＋ ずにはおかない (する -> せずにはおかない): Chắc chắn sẽ khiến cho / Nhất định sẽ làm cho...',
        'grammarRule': 'V-ずにはおかない: Nhất định sẽ gây ra tác động cảm xúc mạnh mẽ hoặc khiến sự việc phải xảy ra.'
    },
    {
        'id': 'skz_b_ch20_q06',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～ずにはおかない',
        'question': 'あの残虐なテロ事件は、世界中の人々に激しい怒りを抱かせ（　）。',
        'options': ['a. ずにはおかなかった', 'b. ずにはすまなかった', 'c. ざるを得なかった'],
        'answer': 'a',
        'explanation': '【Dịch】Vụ khủng bố tàn bạo kinh hoàng ấy chắc chắn đã dấy lên cơn phẫn nộ dữ dội trong lòng hàng triệu con người trên toàn thế giới.\n【Phân tích】Gây ra cơn phẫn nộ tất yếu: 抱かせずにはおかなかった.',
        'grammarRule': 'Khiến cho cảm xúc mạnh mẽ bùng nổ tất yếu.'
    },
    {
        'id': 'skz_b_ch20_q07',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～ざるを得ない',
        'question': 'これほど確固たる証拠を突きつけられては、自分の過ちを認め（　）ざるを得ない。',
        'options': ['a. ', 'b. な', 'c. の'],
        'answer': 'a',
        'explanation': '【Dịch】Bị đưa ra những bằng chứng đanh thép đến mức này rồi thì tôi đành buộc lòng phải cúi đầu thừa nhận sai sót của mình thôi.\n【Phân tích】V-ない (bỏ ない) ＋ ざるを得ない (する -> せざるを得ない): Đành phải, không thể không (dù trong lòng không muốn nhưng hoàn cảnh ép buộc).',
        'grammarRule': 'V-ない (bỏ ない) ＋ ざるを得ない: Dù không muốn nhưng tình thế buộc lòng phải làm.'
    },
    {
        'id': 'skz_b_ch20_q08',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～ざるを得ない',
        'question': '業績不振の責任を取って、社長は退任（　）。',
        'options': ['a. せざるを得なかった', 'b. せずにはおかなかった', 'c. しないではすまなかった'],
        'answer': 'a',
        'explanation': '【Dịch】Để nhận trách nhiệm cho tình hình kinh doanh bết bát suy thoái, vị giám đốc đã đành phải từ chức.\n【Phân tích】Thế cùng lực kiệt đành phải từ chức: 退任せざるを得なかった.',
        'grammarRule': 'Tình huống bất khả kháng buộc phải làm việc không mong muốn.'
    },
    {
        'id': 'skz_b_ch20_q09',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～ないではすまない',
        'question': '人様の大切な宝物を壊してしまったのだから、弁償（　）しないではすまない。',
        'options': ['a. ', 'b. だ', 'c. な'],
        'answer': 'a',
        'explanation': '【Dịch】Đã lỡ tay làm vỡ tan tành báu vật quý giá của người ta như thế thì về mặt đạo lý và lẽ thường, không đền bù bồi thường là không xong đâu.\n【Phân tích】V-ない ＋ ではすまない: Về mặt đạo đức, tình thế xã hội bắt buộc không làm việc đó là không thể yên chuyện.',
        'grammarRule': 'V-ないではすまない / ずにはすまない: Về mặt đạo lý/trách nhiệm xã hội, bắt buộc phải làm việc đó mới xong.'
    },
    {
        'id': 'skz_b_ch20_q10',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～ないではすまない',
        'question': 'あれほど迷惑をかけたのだから、直接会って一言謝罪（　）。',
        'options': ['a. せずにはすまないだろう', 'b. せずにはおかないだろう', 'c. せざるを得ないだろう'],
        'answer': 'a',
        'explanation': '【Dịch】Đã gây ra bao nhiêu rắc rối phiền toái cho người ta đến thế, nếu không trực tiếp gặp mặt nói một lời xin lỗi chân thành thì lương tâm và đạo lý không thể nào yên được.\n【Phân tích】Không tạ lỗi là không được: 謝罪せずにはすまない.',
        'grammarRule': 'Trách nhiệm đạo đức buộc phải thực hiện.'
    },
    {
        'id': 'skz_b_ch20_q11',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～を禁じ得ない',
        'question': '何の罪もない幼い子供たちが犠牲になった痛ましい事故のニュースを聞き、深い怒りと同情（　）を禁じ得ない。',
        'options': ['a. ', 'b. に', 'c. で'],
        'answer': 'a',
        'explanation': '【Dịch】Nghe bản tin về vụ tai nạn thương tâm cướp đi sinh mạng của những đứa trẻ thơ ngây vô tội, tôi không sao kìm nén nổi cơn phẫn nộ dữ dội cùng niềm xót thương khôn nguôi dâng trào trong lồng ngực.\n【Phân tích】N ＋ を禁じ得ない: Không thể kìm nén nổi cảm xúc (thường đi với 怒り, 涙, 同情, 驚き).',
        'grammarRule': 'N (cảm xúc: 涙, 怒り, 悲しみ, 同情) ＋ を禁じ得ない: Cảm xúc trào dâng mãnh liệt không tài nào kìm nén nổi.'
    },
    {
        'id': 'skz_b_ch20_q12',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '～を余儀なくされる',
        'question': '台風の直撃を受け、航空各社は全便の欠航（　）を余儀なくされた。',
        'options': ['a. ', 'b. に', 'c. で'],
        'answer': 'a',
        'explanation': '【Dịch】Hứng chịu cú đổ bộ trực diện của cơn bão dữ, các hãng hàng không đã buộc lòng phải rơi vào thế bị ép hủy toàn bộ tất cả các chuyến bay.\n【Phân tích】N ＋ を余儀なくされる (chủ ngữ bị đẩy vào tình thế bất đắc dĩ) / を余儀なくさせる (tình huống khách quan buộc người khác phải làm).',
        'grammarRule': 'N ＋ を余儀なくされる: Rơi vào tình thế bắt buộc phải làm / bị hủy hoại ngoài ý muốn do tác động ngoại cảnh.'
    },
    {
        'id': 'skz_b_ch20_q13',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '第20課 総合問題',
        'question': '彼がここまで登りつめられたのは、運ではなく不断の鍛錬（　）にほかならない。',
        'options': ['a. にほかならない', 'b. にすぎない', 'c. を禁じ得ない'],
        'answer': 'a',
        'explanation': '【Dịch】Anh ấy có thể leo lên đỉnh vinh quang như ngày hôm nay chính là nhờ quá trình rèn giũa không ngừng nghỉ chứ chẳng phải may mắn, không gì khác ngoài điều đó.\n【Phân tích】Khẳng định nguyên nhân cốt yếu: 不断の鍛錬にほかならない.',
        'grammarRule': 'N ＋ にほかならない: Chính là, không gì khác.'
    },
    {
        'id': 'skz_b_ch20_q14',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '第20課 総合問題',
        'question': '彼らの批判など、根拠のない単なる言いがかり（　）にすぎない。',
        'options': ['a. にすぎない', 'b. にほかならない', 'c. ずにはおかない'],
        'answer': 'a',
        'explanation': '【Dịch】Những lời chỉ trích của đám người đó chẳng qua chỉ là sự kiếm cớ vô căn cứ không hơn không kém mà thôi.\n【Phân tích】Coi nhẹ, đánh giá thấp: 単なる言いがかりにすぎない.',
        'grammarRule': 'N ＋ にすぎない: Chỉ là... không đáng bận tâm.'
    },
    {
        'id': 'skz_b_ch20_q15',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '第20課 総合問題',
        'question': 'この衝撃的な真実は、国民全体を揺るがさ（　）ずにはおかないだろう。',
        'options': ['a. ずにはおかない', 'b. ずにはすまない', 'c. ざるを得ない'],
        'answer': 'a',
        'explanation': '【Dịch】Sự thật gây sốc kinh hoàng này nhất định sẽ làm rung chuyển toàn bộ tâm trí của toàn thể quốc dân.\n【Phân tích】Nhất định sẽ làm rung chuyển tất yếu: 揺るがさずにはおかない.',
        'grammarRule': 'V-ずにはおかない: Nhất định sẽ tác động chấn động.'
    },
    {
        'id': 'skz_b_ch20_q16',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '第20課 総合問題',
        'question': '会社の経営が悪化した以上、人員削減を断行（　）せざるを得ない。',
        'options': ['a. せざるを得ない', 'b. せずにはおかない', 'c. しないではすまない'],
        'answer': 'a',
        'explanation': '【Dịch】Một khi tình hình kinh doanh của công ty đã rơi vào bờ vực suy thoái thì chúng ta đành phải ngậm ngùi quyết định cắt giảm nhân sự mà thôi.\n【Phân tích】Tình thế đành phải làm việc đau đớn: 断行せざるを得ない.',
        'grammarRule': 'V-ざるを得ない: Đành phải làm việc không mong muốn.'
    },
    {
        'id': 'skz_b_ch20_q17',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '第20課 総合問題',
        'question': '重大な機密を漏洩させた犯人は、厳しい法的責任を問わ（　）れないではすまない。',
        'options': ['a. れないではすまない', 'b. れずにはおかない', 'c. れざるを得ない'],
        'answer': 'a',
        'explanation': '【Dịch】Kẻ đã làm rò rỉ bí mật trọng yếu kia thì về mặt pháp luật và trật tự kỷ cương, không bị truy cứu trách nhiệm pháp lý nghiêm khắc là không xong đâu.\n【Phân tích】Không bị truy cứu là không thể xong: 問われないではすまない.',
        'grammarRule': 'V-ないではすまない: Bắt buộc phải chịu trách nhiệm.'
    },
    {
        'id': 'skz_b_ch20_q18',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '第20課 総合問題',
        'question': '戦争で荒れ果てた街の惨状を目の当たりにして、涙（　）を禁じ得なかった。',
        'options': ['a. を禁じ得なかった', 'b. にほかならなかった', 'c. にすぎなかった'],
        'answer': 'a',
        'explanation': '【Dịch】Tận mắt chứng kiến cảnh tượng hoang tàn đổ nát thê lương của thành phố sau ngọn lửa chiến tranh, tôi không tài nào cầm nổi những giọt nước mắt nghẹn ngào.\n【Phân tích】Không kìm nổi giọt lệ: 涙を禁じ得なかった.',
        'grammarRule': '涙 ＋ を禁じ得ない: Không kìm nén nổi nước mắt.'
    },
    {
        'id': 'skz_b_ch20_q19',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '第20課 総合問題',
        'question': '度重なる怪我により、彼は現役引退（　）を余儀なくされた。',
        'options': ['a. を余儀なくされた', 'b. を禁じ得なかった', 'c. にほかならなかった'],
        'answer': 'a',
        'explanation': '【Dịch】Do chấn thương liên miên tái phát quá nặng nề, anh ấy đã bị đẩy vào bước đường buộc phải giải nghệ giã từ sự nghiệp thi đấu đỉnh cao.\n【Phân tích】Bị buộc phải giải nghệ: 引退を余儀なくされた.',
        'grammarRule': 'N ＋ を余儀なくされる: Bị đẩy vào tình thế bắt buộc.'
    },
    {
        'id': 'skz_b_ch20_q20',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '第20課 総合問題',
        'question': '現代文明の繁栄は、先人たちの血と汗の結晶（　）にほかならない。',
        'options': ['a. にほかならない', 'b. にすぎない', 'c. を余儀なくされている'],
        'answer': 'a',
        'explanation': '【Dịch】Sự phồn vinh rực rỡ của nền văn minh hiện đại ngày nay chính là kết tinh từ máu và mồ hôi của bao thế hệ tiền nhân đi trước, không gì khác ngoài điều ấy.\n【Phân tích】Khẳng định chắc nịch: 結晶にほかならない.',
        'grammarRule': 'N ＋ にほかならない: Chính là kết tinh của...'
    },
    {
        'id': 'skz_b_ch20_q21',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '第20課 総合問題',
        'question': 'これほど明白な証拠がある以上、彼の有罪を疑う余地はないと結論付け（　）ざるを得ない。',
        'options': ['a. ざるを得ない', 'b. ずにはおかない', 'c. ないではすまない'],
        'answer': 'a',
        'explanation': '【Dịch】Một khi đã có những chứng cứ rành rành rõ như ban ngày thế này, chúng ta đành phải đưa ra kết luận rằng không còn một kẽ hở nào để nghi ngờ tội lỗi của hắn nữa.\n【Phân tích】Đành phải kết luận: 結論付けざるを得ない.',
        'grammarRule': 'V-ざるを得ない: Buộc lòng phải đưa ra nhận định.'
    },
    {
        'id': 'skz_b_ch20_q22',
        'lesson': '第20課: 主張・断定',
        'grammarPoint': '第20課 総合問題',
        'question': '国家の最高機密を売り渡した裏切り行為は、極刑をもって臨（　）まざるを得ない重大犯罪である。',
        'options': ['a. まざるを得ない', 'b. まずにはおかない', 'c. まないではすまない'],
        'answer': 'a',
        'explanation': '【Dịch】Hành vi phản bội bán đứng bí mật quốc gia tối mật là trọng tội cực kỳ nghiêm trọng mà pháp luật đành phải áp dụng mức án tử hình thích đáng để xử lý.\n【Phân tích】Đành phải áp dụng: 臨まざるを得ない.',
        'grammarRule': 'V-ざるを得ない: Buộc lòng phải thi hành.'
    }
]

ch20_data = {
    'chapterId': 'ch20',
    'lesson': '第20課: 主張・断定 (Khẳng định & Chủ trương)',
    'theme': '主観を述べる',
    'group': 'group3',
    'title': '第20課: 主張・断定',
    'description': 'Các mẫu ngữ pháp khẳng định dứt khoát hoặc bắt buộc về tâm lý, đạo đức: ～にほかならない, ～にすぎない, ～ずにはおかない, ～ざるを得ない, ～ないではすまない, ～を禁じ得ない, ～を余儀なくされる.',
    'questions': ch20_qs
}

all_14_20 = {
    'ch14': ch14_data,
    'ch15': ch15_data,
    'ch16': ch16_data,
    'ch17': ch17_data,
    'ch18': ch18_data,
    'ch19': ch19_data,
    'ch20': ch20_data
}

# Write to scripts/data_bunpou_ch14_ch20.py
with open('scripts/data_bunpou_ch14_ch20.py', 'w', encoding='utf-8') as f:
    f.write('# -*- coding: utf-8 -*-\n')
    f.write('"""Shin Kanzen Master Bunpou N1 - Nhóm II and III: Chương 14 -> Chương 20"""\n\n')
    f.write('CHAPTERS_14_20 = ' + json.dumps(all_14_20, ensure_ascii=False, indent=2) + '\n')

print('Successfully created scripts/data_bunpou_ch14_ch20.py')
