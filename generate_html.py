import json

with open('questions.json') as f:
    questions = json.load(f)

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Java MCQ Quiz</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f0f2f5; min-height: 100vh; display: flex; justify-content: center;
    padding: 20px; color: #1a1a2e;
  }
  .container { width: 100%; max-width: 720px; }
  .header {
    background: #1a1a2e; color: white; padding: 20px 24px; border-radius: 12px 12px 0 0;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
  }
  .header h1 { font-size: 20px; font-weight: 600; }
  .score { font-size: 16px; background: #16213e; padding: 6px 14px; border-radius: 20px; }
  .progress-wrap { background: #e9ecef; height: 6px; }
  .progress-bar { height: 100%; background: #0f3460; transition: width 0.3s ease; width: 0%; }
  .card {
    background: white; border-radius: 0 0 12px 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    padding: 28px 24px 24px;
  }
  .q-num { font-size: 13px; color: #6c757d; margin-bottom: 10px; font-weight: 500; }
  .q-text {
    font-size: 17px; line-height: 1.6; margin-bottom: 24px; font-weight: 500;
  }
  .q-text code, .answer-text code { background: #f0f2f5; padding: 1px 5px; border-radius: 4px; font-size: 0.9em; }
  .options { display: flex; flex-direction: column; gap: 10px; }
  .option-btn {
    display: flex; align-items: flex-start; gap: 12px; padding: 14px 16px;
    border: 2px solid #dee2e6; border-radius: 10px; background: white;
    font-size: 15px; cursor: pointer; transition: all 0.15s ease; text-align: left;
    line-height: 1.5; width: 100%;
  }
  .option-btn:hover:not(.disabled) { border-color: #0f3460; background: #f8f9ff; }
  .option-btn .label {
    flex-shrink: 0; width: 28px; height: 28px; border-radius: 50%;
    background: #e9ecef; display: flex; align-items: center; justify-content: center;
    font-weight: 600; font-size: 14px; transition: all 0.15s ease;
  }
  .option-btn.selected { border-color: #0f3460; background: #eef1ff; }
  .option-btn.correct { border-color: #28a745; background: #d4edda; }
  .option-btn.correct .label { background: #28a745; color: white; }
  .option-btn.wrong { border-color: #dc3545; background: #f8d7da; }
  .option-btn.wrong .label { background: #dc3545; color: white; }
  .option-btn.disabled { cursor: default; opacity: 0.85; }
  .option-btn.show-correct { border-color: #28a745; background: #d4edda; }
  .option-btn.show-correct .label { background: #28a745; color: white; }
  .feedback {
    margin-top: 20px; padding: 14px 18px; border-radius: 10px;
    font-size: 15px; line-height: 1.5; display: none;
  }
  .feedback.show { display: block; }
  .feedback.correct { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
  .feedback.wrong { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
  .feedback .answer-text { margin-top: 5px; }
  .feedback .answer-text code { background: rgba(0,0,0,0.06); }
  .next-btn {
    margin-top: 20px; padding: 12px 32px; border: none; border-radius: 8px;
    background: #0f3460; color: white; font-size: 16px; font-weight: 500;
    cursor: pointer; transition: background 0.15s ease; display: none;
  }
  .next-btn:hover { background: #1a1a2e; }
  .next-btn.show { display: inline-block; }
  .results {
    display: none; text-align: center; padding: 20px 0;
  }
  .results.show { display: block; }
  .results h2 { font-size: 28px; margin-bottom: 8px; }
  .results .score-big { font-size: 56px; font-weight: 700; color: #0f3460; margin: 16px 0; }
  .results .score-big .total { font-size: 28px; color: #6c757d; }
  .results .pct { font-size: 18px; color: #6c757d; margin-bottom: 24px; }
  .results .summary { text-align: left; margin-top: 16px; }
  .results .summary-item {
    padding: 10px 14px; border-bottom: 1px solid #eee; font-size: 14px;
  }
  .results .summary-item:last-child { border-bottom: none; }
  .results .summary-item .sq-num { font-weight: 600; color: #0f3460; }
  .results .summary-item .sq-status { display: inline-block; margin-right: 6px; }
  .restart-btn {
    margin-top: 20px; padding: 12px 32px; border: 2px solid #0f3460;
    border-radius: 8px; background: white; color: #0f3460;
    font-size: 16px; font-weight: 500; cursor: pointer;
  }
  .restart-btn:hover { background: #f0f2f5; }
  .quiz-content { display: block; }
  .quiz-content.hidden { display: none; }
  @media (max-width: 500px) {
    body { padding: 10px; }
    .header { padding: 14px 16px; }
    .header h1 { font-size: 17px; }
    .card { padding: 20px 16px; }
    .q-text { font-size: 15px; }
    .option-btn { padding: 12px 14px; font-size: 14px; }
  }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>Java MCQ Quiz</h1>
    <div class="score">Score: <span id="score">0</span> / <span id="total">''' + str(len(questions)) + '''</span></div>
  </div>
  <div class="progress-wrap"><div class="progress-bar" id="progressBar"></div></div>
  <div class="card">
    <div id="quizContent" class="quiz-content">
      <div class="q-num" id="qNum">Question 1 of ''' + str(len(questions)) + '''</div>
      <div class="q-text" id="qText"></div>
      <div class="options" id="options"></div>
      <div class="feedback" id="feedback">
        <div id="feedbackMsg"></div>
        <div class="answer-text" id="feedbackAnswer"></div>
      </div>
      <button class="next-btn" id="nextBtn">Next</button>
    </div>
    <div class="results" id="results">
      <h2>Quiz Complete!</h2>
      <div class="score-big"><span id="finalScore">0</span><span class="total"> / ''' + str(len(questions)) + '''</span></div>
      <div class="pct" id="finalPct">0%</div>
      <div class="summary" id="summary"></div>
      <button class="restart-btn" id="restartBtn">Restart Quiz</button>
    </div>
  </div>
</div>
<script>
const QUESTIONS = ''' + json.dumps(questions, ensure_ascii=False) + ''';

let currentIdx = 0;
let score = 0;
let answered = [];
let quizDone = false;

const qNum = document.getElementById('qNum');
const qText = document.getElementById('qText');
const options = document.getElementById('options');
const feedback = document.getElementById('feedback');
const feedbackMsg = document.getElementById('feedbackMsg');
const feedbackAnswer = document.getElementById('feedbackAnswer');
const nextBtn = document.getElementById('nextBtn');
const progressBar = document.getElementById('progressBar');
const scoreEl = document.getElementById('score');
const totalEl = document.getElementById('total');
const quizContent = document.getElementById('quizContent');
const results = document.getElementById('results');
const finalScore = document.getElementById('finalScore');
const finalPct = document.getElementById('finalPct');
const summary = document.getElementById('summary');
const restartBtn = document.getElementById('restartBtn');

function escapeHtml(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

function renderQuestion() {
  if (quizDone) return;
  const q = QUESTIONS[currentIdx];
  qNum.textContent = 'Question ' + (currentIdx + 1) + ' of ' + QUESTIONS.length;
  qText.innerHTML = escapeHtml(q.question).replace(/`([^`]+)`/g, '<code>$1</code>');

  options.innerHTML = '';
  q.options.forEach((opt, i) => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.innerHTML = '<span class="label">' + opt.label + '</span><span>' + escapeHtml(opt.text).replace(/`([^`]+)`/g, '<code>$1</code>') + '</span>';
    btn.dataset.label = opt.label;
    btn.addEventListener('click', () => selectOption(i));
    options.appendChild(btn);
  });

  feedback.classList.remove('show', 'correct', 'wrong');
  nextBtn.classList.remove('show');
  progressBar.style.width = ((currentIdx) / QUESTIONS.length * 100) + '%';

  if (answered[currentIdx] !== undefined) {
    applyAnswerState();
  }
}

function applyAnswerState() {
  const state = answered[currentIdx];
  if (state === undefined) return;
  const q = QUESTIONS[currentIdx];
  const btns = options.querySelectorAll('.option-btn');
  btns.forEach((btn, i) => {
    btn.classList.add('disabled');
    const label = q.options[i].label;
    if (label === q.answer_label) {
      btns[i].classList.add('correct');
    }
  });
  if (state.selectedLabel === q.answer_label) {
    btns[state.selectedIdx].classList.add('correct');
  } else {
    btns[state.selectedIdx].classList.add('wrong');
  }
  showFeedback(state.selectedLabel === q.answer_label);
  nextBtn.classList.add('show');
  if (currentIdx === QUESTIONS.length - 1) {
    nextBtn.textContent = 'Show Results';
  }
}

function selectOption(idx) {
  if (answered[currentIdx] !== undefined) return;
  const q = QUESTIONS[currentIdx];
  const btns = options.querySelectorAll('.option-btn');
  const selectedLabel = q.options[idx].label;
  const isCorrect = selectedLabel === q.answer_label;

  btns.forEach((btn, i) => {
    btn.classList.add('disabled');
    if (q.options[i].label === q.answer_label) {
      btn.classList.add('correct');
    }
  });
  if (isCorrect) {
    btns[idx].classList.add('correct');
    score++;
    scoreEl.textContent = score;
  } else {
    btns[idx].classList.add('wrong');
  }

  answered[currentIdx] = { selectedLabel, selectedIdx: idx, correct: isCorrect };
  showFeedback(isCorrect);
  nextBtn.classList.add('show');
  if (currentIdx === QUESTIONS.length - 1) {
    nextBtn.textContent = 'Show Results';
  }
}

function showFeedback(isCorrect) {
  const q = QUESTIONS[currentIdx];
  feedback.className = 'feedback show ' + (isCorrect ? 'correct' : 'wrong');
  feedbackMsg.textContent = isCorrect ? 'Correct!' : 'Wrong!';
  const answerHtml = escapeHtml(q.answer).replace(/`([^`]+)`/g, '<code>$1</code>');
  feedbackAnswer.innerHTML = '<strong>Answer: ' + q.answer_label + ') </strong>' + answerHtml;
}

nextBtn.addEventListener('click', () => {
  if (currentIdx < QUESTIONS.length - 1) {
    currentIdx++;
    renderQuestion();
  } else {
    showResults();
  }
});

function showResults() {
  quizDone = true;
  quizContent.classList.add('hidden');
  results.classList.add('show');
  progressBar.style.width = '100%';
  finalScore.textContent = score;
  const pct = Math.round(score / QUESTIONS.length * 100);
  finalPct.textContent = pct + '%';

  let html = '<h3 style="margin-bottom:12px">Review Answers</h3>';
  QUESTIONS.forEach((q, i) => {
    const a = answered[i];
    const status = a && a.correct ? '\u2705' : '\u274C';
    const label = a ? a.selectedLabel : '-';
    html += '<div class="summary-item"><span class="sq-status">' + status + '</span><span class="sq-num">Q' + (i+1) + ':</span> ' + escapeHtml(q.question.slice(0, 80)) + (q.question.length > 80 ? '...' : '') + ' <em>(Your answer: ' + label + ', Correct: ' + q.answer_label + ')</em></div>';
  });
  summary.innerHTML = html;
}

restartBtn.addEventListener('click', () => {
  currentIdx = 0;
  score = 0;
  answered = [];
  quizDone = false;
  scoreEl.textContent = '0';
  results.classList.remove('show');
  quizContent.classList.remove('hidden');
  if (nextBtn.textContent === 'Show Results') nextBtn.textContent = 'Next';
  renderQuestion();
});

renderQuestion();
</script>
</body>
</html>'''

with open('index.html', 'w') as f:
    f.write(html)

print('index.html generated successfully')
