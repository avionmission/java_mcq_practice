import re, json

with open('questionbank.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')

questions = []
current = None
state = 'idle'  # idle, question_text, options, answer
opt_count = 0
global_id = 0

def save_current():
    global current
    if current and current.get('options') and current.get('answer'):
        questions.append(current)
    current = None

for line in lines:
    stripped = line.strip()

    # Detect question header: #### **Question N**
    m = re.match(r'^#### \*\*Question (\d+)\*\*$', stripped)
    if m:
        save_current()
        global_id += 1
        current = {'id': global_id, 'question': '', 'options': [], 'answer': '', 'answer_label': ''}
        state = 'question_text'
        continue

    if current is None:
        continue

    if state == 'question_text':
        # Look for first option
        om = re.match(r'^\* ([A-D])\)\s*(.*)', stripped)
        if om:
            current['options'].append({'label': om.group(1), 'text': om.group(2)})
            state = 'options'
        else:
            if stripped:
                if current['question']:
                    current['question'] += ' ' + stripped
                else:
                    current['question'] = stripped
        continue

    if state == 'options':
        om = re.match(r'^\* ([A-D])\)\s*(.*)', stripped)
        if om:
            current['options'].append({'label': om.group(1), 'text': om.group(2)})
            continue
        # Check for answer line
        am = re.match(r'^\* \*\*Answer:\s*([A-D])\s*\)?\s*(.*)', stripped)
        if am:
            current['answer_label'] = am.group(1)
            answer_text = am.group(2)
            # Remove leading label text like "C) It is dependent..."
            answer_text = re.sub(r'^[A-D]\)\s*', '', answer_text)
            # Remove markdown bold markers and everything after (notes, etc.)
            answer_text = re.split(r'\*\*', answer_text, maxsplit=1)[0]
            # Remove any remaining (Note: ...) blocks
            answer_text = re.sub(r'\s*\(Note:.*?\)\s*', '', answer_text)
            answer_text = answer_text.strip()
            current['answer'] = answer_text
            state = 'answer'
        continue

    if state == 'answer':
        # Check if there's a continuation of the answer in parentheses (note)
        # or if we hit a new section or blank line
        if stripped == '' or stripped.startswith('---') or stripped.startswith('####'):
            save_current()
            state = 'idle'
            if stripped.startswith('####'):
                # reprocess this line
                m2 = re.match(r'^#### \*\*Question (\d+)\*\*$', stripped)
                if m2:
                    global_id += 1
                    current = {'id': global_id, 'question': '', 'options': [], 'answer': '', 'answer_label': ''}
                    state = 'question_text'
        continue

    if state == 'idle':
        continue

save_current()

# Output JSON
print(json.dumps(questions, indent=2, ensure_ascii=False))
print(f'// Total questions parsed: {len(questions)}', file=__import__('sys').stderr)
