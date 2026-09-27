import sys, pykakasi

sys.stdout.reconfigure(encoding='utf-8')

kks = pykakasi.kakasi()

test_cases = [
    ("バスの運賃を払う。", ["うんしん", "うんちん", "うんにん", "うんりん"]),
    ("風が強くて、髪が乱れてしまった。", ["くずれて", "あれて", "あばれて", "みだれて"]),
    ("前田さんは子どもたちに正しい泳ぎ方の模範を示した。", ["もうばん", "もうはん", "もばん", "もはん"]),
    ("状況を詳細に書いてください。", ["そうざい", "そうさい", "しょうざい", "しょうさい"]),
    ("分析には少し時間がかかります。", ["ぶんせき", "ぶんかい", "ぶんせつ", "ぶんかつ"]),
    ("髪の毛がくしに絡まってしまって。", ["はさまって", "からまって", "つまって", "たまって"]),
]

for sentence, options in test_cases:
    # Convert sentence with kakasi
    result = kks.convert(sentence)
    underlined = sentence
    for item in result:
        orig = item['orig']
        hira = item['hira']
        # Check if this word's reading is in options
        if hira in options:
            underlined = sentence.replace(orig, f"<u>{orig}</u>", 1)
            print(f"Matched '{orig}' -> reading '{hira}': {underlined}")
            break
