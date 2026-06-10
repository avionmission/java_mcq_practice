import re, json

with open('quiz3.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by "### Question N" headers
sections = re.split(r'\n###\s+Question\s+(\d+)', text)
# sections[0] is the intro, then alternating [num, content, num, content, ...]
if not sections[0].strip().startswith('###'):
    sections = sections[1:]  # drop intro

questions = []
for i in range(0, len(sections), 2):
    qnum = int(sections[i].strip())
    block = sections[i + 1] if i + 1 < len(sections) else ''

    lines = block.split('\n')
    question = ''
    options = []
    correct_labels = []
    state = 'header'
    code_buffer = []
    in_code = False
    opt_num = 0

    # First line is usually "(Page N)" leftover from split header
    if lines and re.match(r'^\s*\(Pages?\s', lines[0]):
        lines = lines[1:]

    for line in lines:
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith('```'):
            if in_code:
                code_buffer.append('')
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_buffer.append(stripped)
            continue

        if state == 'header':
            # Skip "---" lines and blank lines
            if stripped == '' or stripped == '---':
                continue
            # "**Question:** text" or "**Question** text"
            qm = re.match(r'\*\*Question:\s*\*\*(.*)', stripped)
            if not qm:
                qm = re.match(r'\*\*Question\*\*(.*)', stripped)
            if qm:
                qt = qm.group(1).strip()
                if qt:
                    question = qt
                state = 'question'
                continue
            # Could have text before **Question:** on same line as header or after
            if stripped and not stripped.startswith('*'):
                # Skip standalone page info lines
                if re.match(r'^Pages?\s+\d+', stripped, re.IGNORECASE):
                    continue
                if question:
                    question += ' ' + stripped
                else:
                    question = stripped
                state = 'question'
            continue

        if state == 'question':
            if stripped == '':
                continue  # blank line, may transition to options
            if stripped == '---':
                continue
            # Options start with "* "
            if stripped.startswith('* '):
                state = 'in_options'
                # Process this option
                opt_text = stripped[2:].strip()
                if opt_text.startswith('**Selected Answer:**'):
                    correct_text = opt_text[21:].strip()
                    label = chr(65 + opt_num)
                    options.append({'label': label, 'text': correct_text, 'correct': True})
                    correct_labels.append(label)
                    opt_num += 1
                elif opt_text.startswith('**Selected Answer**'):
                    correct_text = opt_text[20:].strip()
                    label = chr(65 + opt_num)
                    options.append({'label': label, 'text': correct_text, 'correct': True})
                    correct_labels.append(label)
                    opt_num += 1
                else:
                    label = chr(65 + opt_num)
                    # Strip trailing "*(Note: ...)" from option text too
                    display = re.sub(r'\s*\*?\(Note:.*?\)\s*$', '', opt_text)
                    options.append({'label': label, 'text': display, 'correct': False})
                    opt_num += 1
                continue

            # Handle case where question text continues
            if stripped.startswith('**Question') or stripped.startswith('**Question:'):
                continue  # already handled

            # Accumulate question text
            if stripped and not stripped.startswith('```'):
                if question:
                    question += ' ' + stripped
                else:
                    question = stripped
            continue

        if state == 'in_options':
            if stripped == '' or stripped == '---':
                continue
            if stripped.startswith('* '):
                opt_text = stripped[2:].strip()
                if opt_text.startswith('**Selected Answer:**'):
                    correct_text = opt_text[21:].strip()
                    label = chr(65 + opt_num)
                    options.append({'label': label, 'text': correct_text, 'correct': True})
                    correct_labels.append(label)
                    opt_num += 1
                elif opt_text.startswith('**Selected Answer**'):
                    correct_text = opt_text[20:].strip()
                    label = chr(65 + opt_num)
                    options.append({'label': label, 'text': correct_text, 'correct': True})
                    correct_labels.append(label)
                    opt_num += 1
                else:
                    label = chr(65 + opt_num)
                    display = re.sub(r'\s*\*?\(Note:.*?\)\s*$', '', opt_text)
                    options.append({'label': label, 'text': display, 'correct': False})
                    opt_num += 1
                continue
            # Non-option line after options started - could be continuation of
            # a multi-line option text (like code in option)
            if options and not stripped.startswith('```'):
                # Append to last option if it was a Selected Answer continuation
                last = options[-1]
                last['text'] = last['text'] + '\n' + stripped
                if last['correct']:
                    pass  # keep tracking
            continue

    # If we have code buffer content, append it to the question
    if code_buffer:
        code_str = '\n'.join(code_buffer)
        if question:
            question += '\n' + code_str
        else:
            question = code_str

    # Determine answer_label (first correct)
    answer_label = correct_labels[0] if correct_labels else ''

    # Find answer text
    answer_text = ''
    for opt in options:
        if opt['label'] == answer_label:
            answer_text = opt['text']
            break

    if question and options and answer_label:
        # Clean up
        question = re.sub(r'\n{3,}', '\n\n', question.strip())
        question = re.sub(r'\n', '<br>', question)
        for opt in options:
            # Strip notes from option text
            opt['text'] = re.split(r'\s*\*?\s*\(Note:', opt['text'], maxsplit=1)[0]
            opt['text'] = re.sub(r'\n', '<br>', opt['text'].strip())
            del opt['correct']
        # Strip notes from answer text
        answer_text = re.split(r'\s*\*?\s*\(Note:', answer_text, maxsplit=1)[0]
        answer_text = re.sub(r'\n', '<br>', answer_text.strip())

        questions.append({
            'id': qnum,
            'question': question,
            'options': options,
            'answer': answer_text,
            'answer_label': answer_label
        })

print(json.dumps(questions, indent=2, ensure_ascii=False))
print(f'Total: {len(questions)}', file=__import__('sys').stderr)
