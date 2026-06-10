import re, json

with open('quiz2.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split into sections by "N. Title" pattern at start of line
section_splits = re.split(r'\n(?=\d+\.\s+)', text)

# Remove header intro
if section_splits and not re.match(r'^\d+\.\s+', section_splits[0].strip()):
    section_splits = section_splits[1:]

# Remove trailing junk
if section_splits and 'Correct Answer' not in section_splits[-1] and 'Correct Answers' not in section_splits[-1]:
    section_splits = section_splits[:-1]

questions = []
for idx, block in enumerate(section_splits):
    lines = block.strip().split('\n')
    question = ''
    options = []
    correct_label = ''
    option_num = 0
    state = 'header'  # header -> question -> options_start -> options -> done
    current_opt_text = []
    current_opt_correct = False

    for line in lines:
        stripped = line.strip()

        if state == 'header':
            # Skip the "N. Title (Page X)" line
            if re.match(r'^\d+\.\s+', stripped):
                state = 'question'
                continue

        if state in ('header', 'question'):
            # Look for "Question #N:" or "Questions #N:"
            qm = re.match(r'^Question[s]?\s*#?\s*\d+[.:]?\s*(.*)', stripped, re.IGNORECASE)
            if qm:
                qt = qm.group(1).strip()
                if qt:
                    question = question + '\n' + qt if question else qt
                state = 'question'
                continue

            if stripped.lower().startswith('options'):
                state = 'options_start'
                continue

            # Check for option start
            om = re.match(r'^\[([ x])\]\s*(.*)', stripped)
            if om:
                state = 'options'
                current_opt_correct = (om.group(1) == 'x')
                current_opt_text = [om.group(2)]
                continue

            if stripped and not stripped.startswith('Correct '):
                question = question + '\n' + stripped if question else stripped

        elif state == 'options_start':
            om = re.match(r'^\[([ x])\]\s*(.*)', stripped)
            if om:
                state = 'options'
                current_opt_correct = (om.group(1) == 'x')
                current_opt_text = [om.group(2)]
                continue
            # else skip blank lines

        elif state == 'options':
            om = re.match(r'^\[([ x])\]\s*(.*)', stripped)
            if om:
                # Save previous option
                opt_text_full = '\n'.join(current_opt_text).strip()
                display = re.sub(r'\s*\(Note:.*?\)\s*$', '', opt_text_full)
                label = chr(65 + len(options))
                options.append({'label': label, 'text': display, 'correct': current_opt_correct})
                if current_opt_correct and not correct_label:
                    correct_label = label
                # Start new option
                current_opt_correct = (om.group(1) == 'x')
                current_opt_text = [om.group(2)]
            elif stripped.lower().startswith('correct answer') or stripped.startswith('---'):
                # Save current option
                if current_opt_text:
                    opt_text_full = '\n'.join(current_opt_text).strip()
                    display = re.sub(r'\s*\(Note:.*?\)\s*$', '', opt_text_full)
                    label = chr(65 + len(options))
                    options.append({'label': label, 'text': display, 'correct': current_opt_correct})
                    if current_opt_correct and not correct_label:
                        correct_label = label
                state = 'done'
            elif stripped:
                # Continuation of current option
                current_opt_text.append(stripped)

        elif state == 'done':
            pass

    # Save last option if still pending
    if state == 'options' and current_opt_text:
        opt_text_full = '\n'.join(current_opt_text).strip()
        display = re.sub(r'\s*\(Note:.*?\)\s*$', '', opt_text_full)
        label = chr(65 + len(options))
        options.append({'label': label, 'text': display, 'correct': current_opt_correct})
        if current_opt_correct and not correct_label:
            correct_label = label

    answer_text = ''
    for opt in options:
        if opt['label'] == correct_label:
            answer_text = opt['text']
            break

    if question and options and correct_label:
        # Clean up question
        question = re.sub(r'\n{3,}', '\n\n', question.strip())
        question = re.sub(r'\n', '<br>', question)
        # Clean up option texts
        for opt in options:
            opt['text'] = re.sub(r'\n', '<br>', opt['text'].strip())
            del opt['correct']
        answer_text = re.sub(r'\n', '<br>', answer_text.strip())

        questions.append({
            'id': idx + 1,
            'question': question,
            'options': options,
            'answer': answer_text,
            'answer_label': correct_label
        })

print(json.dumps(questions, indent=2, ensure_ascii=False))
print(f'Total: {len(questions)}', file=__import__('sys').stderr)
