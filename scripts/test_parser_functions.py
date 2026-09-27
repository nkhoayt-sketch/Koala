import re, sys

sys.stdout.reconfigure(encoding='utf-8')

ZEN_TRANS = str.maketrans('0123456789', '０１２３４５６７８９')
NUM_TRANS = str.maketrans('０１２３４５６７８９', '0123456789')

def parse_block(block, q_num):
    q_zen = str(q_num).translate(ZEN_TRANS)
    # Strip question number from the beginning
    block = re.sub(rf'^\s*(?:{q_num}|{q_zen})[a-z。、.\s\(\)（）]*', '', block).strip()
    
    # Try pattern 1: Standard 1 .. 2 .. 3 .. 4
    m = re.search(r'(?:^|\s|\n)[１1]\s+(.*?)(?:^|\s|\n)[２2]\s+(.*?)(?:^|\s|\n)[３3]\s+(.*?)(?:^|\s|\n)[４4]\s+([^\n<<<]+)', block, re.DOTALL)
    if m:
        q_text = block[:m.start()].strip()
        opts = [re.sub(r'\s+', ' ', m.group(i).strip()) for i in range(1, 5)]
        return q_text, opts
        
    # Try pattern 2: Layout with 1 .. 3 .. 2 .. 4
    m2 = re.search(r'(?:^|\s|\n)[１1]\s+(.*?)(?:^|\s|\n)[３3]\s+(.*?)(?:^|\s|\n)[２2]\s+(.*?)(?:^|\s|\n)[４4]\s+([^\n<<<]+)', block, re.DOTALL)
    if m2:
        q_text = block[:m2.start()].strip()
        opts = [
            re.sub(r'\s+', ' ', m2.group(1).strip()),
            re.sub(r'\s+', ' ', m2.group(3).strip()),
            re.sub(r'\s+', ' ', m2.group(2).strip()),
            re.sub(r'\s+', ' ', m2.group(4).strip())
        ]
        return q_text, opts
        
    # Try line-by-line
    lines = [l.strip() for l in block.split('\n') if l.strip()]
    opt_dict = {}
    q_lines = []
    found_any_opt = False
    for l in lines:
        om = re.match(r'^[１２３４1234]\s+(.*)', l)
        if om:
            found_any_opt = True
            dig = int(l[0].translate(NUM_TRANS))
            opt_dict[dig] = om.group(1).strip()
        elif not found_any_opt:
            q_lines.append(l)
    if len(opt_dict) == 4:
        return ' '.join(q_lines).strip(), [opt_dict[1], opt_dict[2], opt_dict[3], opt_dict[4]]
        
    return block, []

test_b = """49  １ しておきます 
 ３ しておく点です 
２ されています 
４ されている点です"""
qt, op = parse_block(test_b, 49)
print("qt:", qt)
print("op:", op)
