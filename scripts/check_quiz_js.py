with open('js/quiz.js', 'r', encoding='utf-8') as f:
    text = f.read()

stack = []
in_str = None
escape = False
line_num = 1

for idx, ch in enumerate(text):
    if ch == '\n':
        line_num += 1
    if escape:
        escape = False
        continue
    if ch == '\\':
        escape = True
        continue
    if in_str:
        if ch == in_str:
            in_str = None
        continue
    if ch in ('"', "'", '`'):
        in_str = ch
        continue
    if ch in '({[':
        stack.append((ch, line_num))
    elif ch in ')}]':
        if not stack:
            print(f'Unmatched {ch} at line {line_num}')
            break
        opener, o_line = stack.pop()
        if (opener == '(' and ch != ')') or (opener == '{' and ch != '}') or (opener == '[' and ch != ']'):
            print(f'Mismatched {opener} (line {o_line}) with {ch} (line {line_num})')
            break
else:
    if stack:
        print(f'Unclosed {stack[-1]}')
    else:
        print('Syntax structure check passed perfectly!')
