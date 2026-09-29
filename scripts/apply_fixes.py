import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FIXES = {
    "2025_07.json": {
        45: {
            "question": "今回のセミナーの開催日が人の ＿＿ ＿＿ ＿★＿ ＿＿ 参加者が集まったのは大成功といえる。",
            "options": ["集まりにくい", "ことを考えると", "平日だった", "200名もの"],
            "answer": 1,
            "explanation": "Thứ tự đúng: 1 - 3 - ★2 - 4\nCâu hoàn chỉnh: 今回のセミナーの開催日が人の集まりにくい平日だったことを考えると、200名もの参加者が集まったのは大成功といえる。\n(Xét việc ngày tổ chức hội thảo rơi vào ngày thường vốn khó tập trung người, thì việc thu hút tới 200 người tham gia có thể coi là đại thành công.)\nVị trí ngôi sao ★ là phương án 2 (ことを考えると)."
        },
        55: {
            "options": [
                "7月中にウェブ会員サービスの申し込みを始めるので、登録してほしい。",
                "8月末で使用量と料金の通知を終了するので、知りたい場合は連絡してほしい。",
                "9月から新しい形式の通知書を郵送するので、手数料を負担してほしい。",
                "9月から紙の通知書を有料にするので、無料で確認したい場合はウェブで確認してほしい。"
            ],
            "answer": 3
        },
        71: {
            "options": [
                "12月5日までにホームページか電話で空きを確認し申し込む。",
                "12月5日までに電話で空きを確認し申し込む。",
                "12月7日までにホームページか電話で空きを確認し申し込む。",
                "12月7日までに電話で空きを確認し申し込む。"
            ],
            "answer": 3
        }
    },
    "2025_12.json": {
        63: {
            "options": [
                "700万年前から大きくなりはじめ、200万年前にゴリラの脳より大きくなった。",
                "200万年前から大きくなりはじめ、7万年前に現代人の脳と同じ大きさになった。",
                "言葉を話しはじめる前に、現代人の脳と同じ大きさになった。",
                "言葉を話しはじめたころ、ゴリラの脳より大きくなった。"
            ],
            "answer": 2
        },
        71: {
            "options": [
                "10月20日（土）の17時30分までに、丸山汽船本社に電話する。",
                "10月20日（土）の17時30分までに、赤木港発着所に電話する。",
                "10月21日（日）の17時までに、丸山汽船本社に電話する。",
                "10月21日（日）の17時までに、赤木港発着所に電話する。"
            ],
            "answer": 3
        }
    },
    "2014_12.json": {
        46: {
            "question": "姉の ＿＿ ＿＿ ＿★＿ ＿＿ 私にはとてもできない。",
            "options": ["欠かさず", "ように", "10年以上一日も", "日記を書くなんて"],
            "answer": 0,
            "explanation": "Thứ tự đúng: 2 - 3 - ★1 - 4\nCâu hoàn chỉnh: 姉のように10年以上一日も欠かさず日記を書くなんて、私にはとてもできない。\n(Như chị gái tôi ngày nào cũng viết nhật ký không bỏ sót một ngày nào suốt hơn 10 năm trời thì tôi hoàn toàn không làm được.)\nVị trí ngôi sao ★ là phương án 1 (欠かさず)."
        }
    },
    "2018_07.json": {
        49: {
            "question": "私は、中学生になったころから ＿＿ ＿＿ ＿★＿ ＿＿ 医者になろうと決めていた。",
            "options": ["将来", "医学に興味を持ち始め", "高校に入ったころには", "次第に"],
            "answer": 2,
            "explanation": "Thứ tự đúng: 4 - 2 - ★3 - 1\nCâu hoàn chỉnh: 私は、中学生になったころから次第に医学に興味を持ち始め、高校に入ったころには将来医者になろうと決めていた。\n(Từ hồi học cấp hai tôi đã dần dần có hứng thú với y học, và đến khi vào cấp ba thì đã quyết định tương lai sẽ trở thành bác sĩ.)\nVị trí ngôi sao ★ là phương án 3 (高校に入ったころには)."
        }
    },
    "2020_12.json": {
        44: {
            "question": "「10倍がゆ」とは ＿＿ ＿＿ ＿★＿ ＿＿ おかゆのことです。",
            "options": ["作った", "水で", "10倍の", "米1に対して"],
            "answer": 1,
            "explanation": "Thứ tự đúng: 4 - 3 - ★2 - 1\nCâu hoàn chỉnh: 「10倍がゆ」とは米1に対して10倍の水で作ったおかゆのことです。\n(\"Cháo gấp 10 lần\" là loại cháo được nấu với lượng nước gấp 10 lần so với 1 phần gạo.)\nVị trí ngôi sao ★ là phương án 2 (水で)."
        }
    },
    "2021_07.json": {
        46: {
            "question": "参考書を読んで完璧に ＿＿ ＿＿ ＿★＿ ＿＿ ということがよくある。",
            "options": ["理解した", "問題を解いてみると", "できない", "つもりでも"],
            "answer": 1,
            "explanation": "Thứ tự đúng: 1 - 4 - ★2 - 3\nCâu hoàn chỉnh: 参考書を読んで完璧に理解したつもりでも、問題を解いてみるとできないということがよくある。\n(Dù cứ ngỡ là đã hiểu hoàn toàn khi đọc sách tham khảo, nhưng hễ bắt tay vào giải bài tập thì thường lại không làm được.)\nVị trí ngôi sao ★ là phương án 2 (問題を解いてみると)."
        },
        47: {
            "question": "この池に ＿＿ ＿＿ ＿★＿ ＿＿ そうだ。",
            "options": ["ものもいる", "すむ", "魚の中には", "100年以上生きる"],
            "answer": 3,
            "explanation": "Thứ tự đúng: 2 - 3 - ★4 - 1\nCâu hoàn chỉnh: この池にすむ魚の中には、100年以上生きるものもいるそうだ。\n(Nghe nói trong số những loài cá sống ở ao này, có con sống thọ hơn 100 năm.)\nVị trí ngôi sao ★ là phương án 4 (100年以上生きる)."
        }
    },
    "2013_07.json": {
        32: {
            "question": "【隔てる】",
            "options": [
                "この二つの問題は隔てて考えるべきだ。",
                "大きな川が二つの市を隔てている。",
                "5分ほど休憩を隔てて、11時から再開します。",
                "試験のときは、隣の人と隔てて座ってください。"
            ],
            "answer": 1,
            "explanation": "Đáp án đúng là 2: 「大きな川が二つの市を隔てている。」(Con sông lớn ngăn cách hai thành phố).\nCác câu còn lại dùng từ chưa tự nhiên:\n- Câu 1: nên dùng 別にして / 分けて\n- Câu 3: nên dùng 挟んで (5分ほど休憩を挟んで)\n- Câu 4: nên dùng 離れて / 間隔をあけて"
        }
    },
    "2018_12.json": {
        28: {
            "question": "【日課】",
            "options": [
                "停留所でバスの時刻表を見ると、次の発車時刻は20分後だった。",
                "今日は売り上げが10万円以上あったので、目標が達成できた。",
                "朝9時までに出社することが会社の規則で決まっている。",
                "健康のため、毎朝30分体操することを日課にしている。"
            ],
            "answer": 3,
            "explanation": "Đáp án đúng là 4: 「健康のため、毎朝30分体操することを日課にしている。」(Vì sức khỏe, tôi biến việc tập thể dục 30 phút mỗi sáng thành thói quen hàng ngày).\nCác câu còn lại dùng sai từ:\n- Câu 1: nên dùng 時刻表 (bảng giờ xe)\n- Câu 2: nên dùng 目標 / ノルマ (chỉ tiêu)\n- Câu 3: nên dùng 規則 / ルール (quy tắc)"
        }
    },
    "2022_07.json": {
        28: {
            "question": "【世代】",
            "options": [
                "野口さんはまだ20代なので、年をとっているとはいえない。",
                "先日のパーティーでは私と同じ世代の人がたくさんいて、話が盛り上がった。",
                "青山さんは今は日本語の先生をしているが、実は英語の先生の期間の方が長い。",
                "仕事を頑張るだけでなく、趣味も楽しんで、充実した生活を送りたい。"
            ],
            "answer": 1,
            "explanation": "Đáp án đúng là 2: 「先日のパーティーでは私と同じ世代の人がたくさんいて、話が盛り上がった。」(Bữa tiệc hôm trước có rất nhiều người cùng thế hệ/lứa tuổi với tôi nên trò chuyện rất rôm rả).\nCác câu còn lại dùng sai từ:\n- Câu 1: nên dùng 年をとっている\n- Câu 3: nên dùng 期間 / 年月\n- Câu 4: nên dùng 生活 / 人生"
        }
    }
}

def apply_fixes():
    fixed_count = 0
    for filename, q_fixes in FIXES.items():
        alt_filename = f"n2_{filename}"
        
        target_paths = [
            os.path.join(ROOT_DIR, "data", "n2_exams", filename),
            os.path.join(ROOT_DIR, "public", "data", "n2_exams", filename),
            os.path.join(ROOT_DIR, "data", "n2_exams", alt_filename),
            os.path.join(ROOT_DIR, "public", "data", "n2_exams", alt_filename),
        ]
        
        for path in target_paths:
            if not os.path.exists(path):
                continue
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            qs = data if isinstance(data, list) else data.get("questions", [])
            for q in qs:
                num = q.get("number")
                if num in q_fixes:
                    patch = q_fixes[num]
                    for k, v in patch.items():
                        q[k] = v
                    fixed_count += 1
            
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Applied fixes to {path}")

if __name__ == "__main__":
    apply_fixes()
    print("Done applying fixes!")
