import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

sample_text = """新緑の時期に森を歩くと、地面に小さなロールキャベツ（注 1）状の物体が落ちている
のを見かけます。しばしばーか所に大量に落ちていて、とてもよく目立ちます。これは 
オトシブミという小さな 甲虫
こうちゅう
（注 2）の仲間が、自分の 幼虫
ようちゅう
のためにつくったもの        
です。この虫のメスは、数分の間に産んだ卵を木の葉で丁寧
ていねい
に包んでから地面に落とす
習性（注３）をもちます。中で孵
かえ
った（注４）幼
よう
虫
ちゅう
は、内側からこの巻いた葉を食べて
成長します。幼虫にとっては、この葉巻きは隠れ家であるとともに食料なわけです。"""

def clean_furigana_advanced(text):
    # Pattern 1: Kanji followed by newline and hiragana furigana:
    # e.g. 幼\nよう\n虫\nちゅう -> 幼虫
    # e.g. 甲虫\nこうちゅう -> 甲虫
    # e.g. 丁寧\nていねい\nに -> 丁寧に
    # Let's replace Kanji + \n + Hiragana with Kanji
    lines = text.split('\n')
    cleaned_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # If this line is only 1-4 hiragana and previous line ended with kanji:
        if stripped and re.fullmatch(r'[\u3040-\u309F]{1,5}', stripped) and cleaned_lines:
            prev = cleaned_lines[-1]
            # It's furigana! Drop it.
            # But wait, what if prev line ended with a single kanji of a compound?
            # e.g. "幼" and next is "よう" and next is "虫"?
            i += 1
            continue
        cleaned_lines.append(line)
        i += 1
        
    result = '\n'.join(cleaned_lines)
    # Fix single kanji broken by newlines like "幼\n虫" -> "幼虫"
    result = re.sub(r'([\u4e00-\u9fff])\n([\u4e00-\u9fff])', r'\1\2', result)
    result = re.sub(r'([\u4e00-\u9fff])\n([\u3040-\u309F])', r'\1\2', result)
    result = re.sub(r'([\u3040-\u309F])\n([\u3040-\u309F])', r'\1\2', result)
    return result

cleaned = clean_furigana_advanced(sample_text)
print("CLEANED TEXT:")
print(cleaned)
