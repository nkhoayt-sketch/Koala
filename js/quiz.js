import { storage } from './storage.js';
import { buildMistakesReport, copyTextToClipboard, sendMistakesToAnkiConnect } from './export.js';
import { GeminiModal } from './gemini.js';

/**
 * Format fill-in-the-blank brackets: replaces empty brackets () or （） with spacious underline slot
 */
export function formatBlankSpacing(text) {
  if (!text) return '';
  // Match empty parentheses: () or （） or with internal spaces (half-width or full-width)
  const emptyBracketPattern = /[（\(][ 　\t]*[）\)]/g;
  const blankHtml = '<span class="blank-slot">（<span class="blank-slot-line">　　　</span>）</span>';
  return text.replace(emptyBracketPattern, blankHtml);
}

function buildSentenceSlotsHtml(starPosition) {
  let slots = '';
  for (let i = 1; i <= 4; i++) {
    if (i === starPosition) {
      slots += `
        <span class="slot-item is-star relative inline-flex justify-center items-end w-10 sm:w-12 h-6 border-b-2 border-slate-700 dark:border-slate-300 mx-1 sm:mx-1.5 align-bottom">
          <span class="slot-star absolute -top-1 sm:-top-1.5 left-1/2 -translate-x-1/2 text-amber-500 text-sm sm:text-base font-bold leading-none select-none">★</span>
        </span>
      `;
    } else {
      slots += `
        <span class="slot-item inline-block w-10 sm:w-12 h-6 border-b-2 border-slate-700 dark:border-slate-300 mx-1 sm:mx-1.5 align-bottom"></span>
      `;
    }
  }
  return `<span class="exam-sentence-slots inline-flex items-end mx-1 sm:mx-1.5 align-baseline whitespace-nowrap">${slots}</span>`;
}

/**
 * Format question text: specifically handles sentence arrangement (問題6/問題8 ★) with 4 distinct solid underline slots,
 * and formats empty brackets () or （） into comfortable blank slots.
 */
function formatQuestionContent(questionText, section) {
  if (!questionText) return '';

  let formatted = questionText;

  const isArrangement = (section && (section.includes('問題6') || section.includes('問題8') || section.includes('文の組み立て'))) || formatted.includes('★');
  if (isArrangement) {
    const slotToken = '[＿_]{1,10}';
    const starToken = '[＿_]*★[＿_]*';

    // 4-slot combinations
    const p1 = new RegExp(`${starToken}\\s+${slotToken}\\s+${slotToken}\\s+${slotToken}`);
    const p2 = new RegExp(`${slotToken}\\s+${starToken}\\s+${slotToken}\\s+${slotToken}`);
    const p3 = new RegExp(`${slotToken}\\s+${slotToken}\\s+${starToken}\\s+${slotToken}`);
    const p4 = new RegExp(`${slotToken}\\s+${slotToken}\\s+${slotToken}\\s+${starToken}`);

    // Truncated / short 3-slot combinations
    const p2_short = new RegExp(`${slotToken}\\s+${starToken}\\s+${slotToken}`);
    const p3_short = new RegExp(`${slotToken}\\s+${slotToken}\\s+${starToken}`);
    const p1_short = new RegExp(`${starToken}\\s+${slotToken}\\s+${slotToken}`);

    // Standalone star
    const pStandalone = /\s*★\s*/;

    if (p1.test(formatted)) {
      formatted = formatted.replace(p1, buildSentenceSlotsHtml(1));
    } else if (p2.test(formatted)) {
      formatted = formatted.replace(p2, buildSentenceSlotsHtml(2));
    } else if (p3.test(formatted)) {
      formatted = formatted.replace(p3, buildSentenceSlotsHtml(3));
    } else if (p4.test(formatted)) {
      formatted = formatted.replace(p4, buildSentenceSlotsHtml(4));
    } else if (p2_short.test(formatted)) {
      formatted = formatted.replace(p2_short, buildSentenceSlotsHtml(2));
    } else if (p3_short.test(formatted)) {
      formatted = formatted.replace(p3_short, buildSentenceSlotsHtml(3));
    } else if (p1_short.test(formatted)) {
      formatted = formatted.replace(p1_short, buildSentenceSlotsHtml(1));
    } else if (pStandalone.test(formatted)) {
      formatted = formatted.replace(pStandalone, ` ${buildSentenceSlotsHtml(3)} `);
    }
  }

  // Format fill-in-the-blank brackets
  formatted = formatBlankSpacing(formatted);

  return formatted;
}

export function formatScriptText(script) {
  if (!script) return '';
  const lines = script.split('\n');
  return lines.map(line => {
    line = line.trim();
    if (!line) return '';
    
    // Highlight speakers like 男：, 女：, 男の人：, 女の人：, 先生：, 店員：, 上司：, 職員1：, etc.
    const speakerMatch = line.match(/^([男女]|男の人|女の人|アナウンサー|先生|店員|職員\s*\d*|上司|客|社長|課長|リーダー|質問\s*\d*|問い)\s*[:：]\s*(.*)$/);
    if (speakerMatch) {
      const speaker = speakerMatch[1];
      const speech = speakerMatch[2];
      const isFemale = speaker.includes('女');
      const isMale = speaker.includes('男');
      const badgeColor = isFemale 
        ? 'bg-rose-100 text-rose-800 border-rose-200' 
        : isMale 
          ? 'bg-indigo-100 text-indigo-800 border-indigo-200' 
          : 'bg-slate-100 text-slate-800 border-slate-200';
      return `<div class="mb-2"><span class="inline-block px-2 py-0.5 rounded-md text-xs font-bold border ${badgeColor} mr-1.5 shadow-2xs">${speaker}</span><span class="text-slate-800 font-jp leading-relaxed">${speech}</span></div>`;
    }
    
    // Context / Setting line or regular line
    return `<div class="mb-2 text-slate-700 font-jp leading-relaxed">${line}</div>`;
  }).join('');
}

export class QuizEngine {
  constructor(containerElement, onProgressUpdate) {
    this.container = containerElement;
    this.onProgressUpdate = onProgressUpdate;
    this.rawDayData = null;
    this.dayData = null;
    this.scope = 'vocab_grammar'; // 'vocab_grammar' | 'full'
    this.userAnswers = {};
    this.userFlags = {};
    this.isSubmitted = false;
    this.activeFilter = 'all'; // 'all' | 'wrong' | 'correct'
    this.scoreResult = null;
    this.geminiModal = new GeminiModal();

    // Mode & Timer
    this.mode = localStorage.getItem('n1_quiz_mode') || 'practice'; // 'practice' | 'exam'
    this.examDuration = 40 * 60; // default 40 minutes = 2400 seconds
    this.examSecondsRemaining = this.getSavedExamTime() || this.examDuration;
    this.timerInterval = null;

    // Active question navigation index (always starts at Question 1 = index 0)
    this.currentQuestionIndex = 0;

    // Dokkai layout state: 'split' (Chia đôi) or 'stacked' (Bài đọc ở trên)
    this.dokkaiLayout = localStorage.getItem('koala_dokkai_layout') || 'split';
  }

  setDokkaiLayout(layout) {
    this.dokkaiLayout = layout;
    localStorage.setItem('koala_dokkai_layout', layout);
    this.render();
    this.showToast(layout === 'split' ? 'Đã chuyển sang chế độ: ◫ Chia đôi màn hình' : 'Đã chuyển sang chế độ: ☰ Bài đọc ở trên', 'info');
  }

  openImageLightbox(src) {
    let modal = document.getElementById('image-lightbox-modal');
    if (modal) modal.remove();

    modal = document.createElement('div');
    modal.id = 'image-lightbox-modal';
    modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md transition-opacity animate-toast';
    modal.innerHTML = `
      <div class="relative max-w-4xl max-h-[92vh] flex flex-col items-center">
        <button type="button" id="btn-close-lightbox" class="absolute -top-11 right-0 sm:-right-4 p-2 rounded-full bg-white/20 hover:bg-white/40 text-white transition flex items-center gap-1.5 text-xs font-semibold cursor-pointer" title="Đóng phóng to">
          <span>✕ Đóng</span>
        </button>
        <img class="max-h-[82vh] max-w-full rounded-2xl shadow-2xl object-contain border-2 border-white/20 bg-white" src="${src}" alt="Ảnh phóng to">
      </div>
    `;

    modal.addEventListener('click', (e) => {
      if (e.target.id === 'image-lightbox-modal' || e.target.closest('#btn-close-lightbox')) {
        modal.remove();
      }
    });

    const onKey = (e) => {
      if (e.key === 'Escape') {
        modal.remove();
        window.removeEventListener('keydown', onKey);
      }
    };
    window.addEventListener('keydown', onKey);

    document.body.appendChild(modal);
  }

  isN2(data = this.rawDayData) {
    if (!data) return false;
    return data.level === 'N2' || (typeof data.id === 'string' && data.id.startsWith('n2'));
  }

  getExamId() {
    if (!this.dayData) return 'default';
    if (this.dayData.id) return this.dayData.id;
    if (this.dayData.day !== undefined) return `n1_day${String(this.dayData.day).padStart(2, '0')}`;
    return 'default';
  }

  getStorageKey() {
    if (!this.dayData) return 'default';
    const base = this.dayData.id || `day_${this.dayData.day}`;
    return this.scope ? `${base}_${this.scope}` : `${base}`;
  }

  getSavedExamTime() {
    try {
      const key = this.getStorageKey();
      const saved = localStorage.getItem(`n1_quiz_exam_seconds_${key}`);
      return saved ? parseInt(saved, 10) : null;
    } catch {
      return null;
    }
  }

  setMode(newMode) {
    this.mode = newMode;
    localStorage.setItem('n1_quiz_mode', newMode);

    if (newMode === 'exam') {
      if (!this.isSubmitted) {
        this.startTimer();
      }
      const durationMins = Math.round(this.examDuration / 60);
      this.showToast(`Đã bật Chế độ Thi thử! Thời gian làm bài ${durationMins} phút.`, 'info');
    } else {
      this.pauseTimer();
      this.showToast('Đã chuyển sang Chế độ Luyện tập tự do.', 'info');
    }

    this.render();
    this.renderPalette();
  }

  startTimer() {
    this.pauseTimer();
    this.updateTimerDisplay();

    this.timerInterval = setInterval(() => {
      if (this.examSecondsRemaining > 0) {
        this.examSecondsRemaining--;
        const key = this.getStorageKey();
        localStorage.setItem(`n1_quiz_exam_seconds_${key}`, this.examSecondsRemaining);
        this.updateTimerDisplay();

        if (this.examSecondsRemaining === 5 * 60) {
          this.showToast('⚠️ Còn 5 phút cuối cùng! Hãy kiểm tra lại bài làm.', 'error');
        }

        if (this.examSecondsRemaining <= 0) {
          this.pauseTimer();
          this.submitQuiz(true); // Auto submit on timeout
        }
      }
    }, 1000);
  }

  pauseTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }

  updateTimerDisplay() {
    const timerEl = document.getElementById('exam-timer-display');
    const timerBadge = document.getElementById('exam-timer-badge');
    if (!timerEl) return;

    const mins = Math.floor(this.examSecondsRemaining / 60);
    const secs = this.examSecondsRemaining % 60;
    const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    timerEl.textContent = formatted;

    if (timerBadge) {
      if (this.mode === 'exam' && !this.isSubmitted) {
        timerBadge.classList.remove('hidden');
        if (this.examSecondsRemaining < 300) {
          timerBadge.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-bold bg-rose-50 text-rose-600 border border-rose-200 timer-warning';
        } else {
          timerBadge.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200';
        }
      } else {
        timerBadge.classList.add('hidden');
      }
    }
  }

  /**
   * Load and render a day or exam quiz
   */
  loadDay(rawDayData, options = {}) {
    this.rawDayData = rawDayData;
    this.currentQuestionIndex = 0; // Reset question index to 0 (Question 1) whenever switching exam/day
    const isN2Exam = this.isN2(rawDayData);

    // Support scopes object { vocab_grammar, reading, listening } or legacy scope string
    let scopes = options.scopes;
    if (!scopes) {
      const scopeStr = options.scope || (isN2Exam ? 'vocab_grammar' : 'full');
      scopes = {
        vocab_grammar: scopeStr !== 'reading' && scopeStr !== 'listening',
        reading: scopeStr === 'reading' || scopeStr === 'full',
        listening: scopeStr === 'listening'
      };
    }
    this.scopes = scopes;

    let questions = rawDayData.questions || [];
    if (questions.length === 0 && Array.isArray(rawDayData.sections)) {
      let num = 1;
      questions = [];
      for (const sec of rawDayData.sections) {
        for (const q of (sec.questions || [])) {
          let ans = q.answer;
          if (typeof ans === 'number' && ans >= 1 && ans <= (q.options ? q.options.length : 4)) {
            ans = ans - 1;
          }
          questions.push({
            id: q.id || `q_${num}`,
            number: q.number || num,
            section: q.section || sec.sectionName || '',
            instruction: q.instruction || sec.instruction || '',
            passage: q.passage || sec.passage || '',
            question: q.question || '',
            targetWord: q.targetWord || '',
            options: q.options || [],
            answer: typeof ans === 'number' ? ans : 0,
            explanation: q.explanation || ''
          });
          num++;
        }
      }
    }
    if (isN2Exam) {
      questions = questions.filter(q => {
        const isVocab = q.sectionGroup === 'vocab_grammar' || (!q.sectionGroup && !q.section.includes('読解') && !q.section.includes('聴解'));
        const isReading = q.sectionGroup === 'reading' || q.section.includes('読解');
        const isListening = q.sectionGroup === 'listening' || q.section.includes('聴解');

        if (scopes.vocab_grammar && isVocab) return true;
        if (scopes.reading && isReading) return true;
        if (scopes.listening && isListening) return true;
        return false;
      });
    }

    this.dayData = {
      ...rawDayData,
      questions: questions
    };

    if (options.mode) {
      this.mode = options.mode;
      localStorage.setItem('n1_quiz_mode', options.mode);
    }

    // Set duration based on exam level and selected scopes
    if (isN2Exam) {
      let durationMinutes = 35;
      if (scopes.vocab_grammar && scopes.reading && scopes.listening) {
        durationMinutes = 155;
      } else if (scopes.vocab_grammar && scopes.reading) {
        durationMinutes = 105;
      } else if (scopes.vocab_grammar && scopes.listening) {
        durationMinutes = 85;
      } else if (scopes.reading && scopes.listening) {
        durationMinutes = 120;
      } else if (scopes.vocab_grammar) {
        durationMinutes = rawDayData.durations?.vocab_grammar || 35;
      } else if (scopes.reading) {
        durationMinutes = 70;
      } else if (scopes.listening) {
        durationMinutes = 50;
      }
      this.examDuration = durationMinutes * 60;
    } else {
      this.examDuration = 40 * 60;
    }

    const storageKey = this.getStorageKey();
    this.userAnswers = storage.getAnswers(storageKey) || {};
    this.userFlags = storage.getFlags(storageKey) || {};
    const savedSubmission = storage.getSubmission(storageKey);
    this.isSubmitted = !!savedSubmission;
    this.scoreResult = savedSubmission ? savedSubmission.scoreResult : null;
    this.activeFilter = 'all';

    const examId = this.getExamId();
    const history = options.historyRecord || storage.getExamHistoryRecord(examId);

    if (options.reviewMode || (this.isSubmitted && Object.keys(this.userAnswers).length === 0)) {
      if (history) {
        this.isSubmitted = true;
        if (history.userAnswers && Object.keys(history.userAnswers).length > 0) {
          this.userAnswers = { ...this.userAnswers, ...history.userAnswers };
        }
        if (history.flaggedQuestions && Array.isArray(history.flaggedQuestions)) {
          history.flaggedQuestions.forEach(qid => { this.userFlags[qid] = true; });
        }
        if (!this.scoreResult) {
          this.scoreResult = {
            total: history.totalQuestions || this.dayData.questions.length,
            correct: history.lastScore || 0,
            percentage: history.percentage || 0,
            isPassed: (history.percentage || 0) >= 60
          };
        }
      }
    }

    const savedExamTime = this.getSavedExamTime();
    this.examSecondsRemaining = savedExamTime !== null ? savedExamTime : this.examDuration;

    if (this.mode === 'exam' && !this.isSubmitted) {
      this.startTimer();
    } else {
      this.pauseTimer();
      this.updateTimerDisplay();
    }

    this.render();
    this.renderPalette();
    this.updateProgress();
  }

  /**
   * Main render function
   */
  render() {
    if (!this.dayData || !this.dayData.questions || this.dayData.questions.length === 0) {
      if (this.scopes?.listening && this.dayData?.audio) {
        this.container.innerHTML = `
          <div class="max-w-3xl mx-auto py-10 space-y-6">
            <div class="p-6 rounded-3xl bg-gradient-to-r from-amber-950 via-slate-900 to-indigo-950 text-white shadow-xl border border-amber-500/30 animate-toast">
              <div class="flex items-center gap-4 mb-4">
                <div class="w-12 h-12 rounded-2xl bg-amber-500 text-white flex items-center justify-center font-bold text-2xl shadow-md">
                  🎧
                </div>
                <div>
                  <h3 class="text-lg font-bold text-white">聴解 (Nghe hiểu) - ${this.dayData.title}</h3>
                  <p class="text-xs text-amber-200 mt-0.5">Phần nghe hiểu đề thi chính thức JLPT N2</p>
                </div>
              </div>
              <p class="text-xs text-slate-300 mb-4 leading-relaxed">
                Bấm nút Play để nghe toàn bộ file âm thanh đề thi thật. Bạn có thể tạm dừng, tua thời gian hoặc điều chỉnh âm lượng tùy ý.
              </p>
              <audio id="exam-audio-player" controls preload="auto" class="w-full h-11 rounded-xl bg-white/10" src="${this.dayData.audio}">
                Trình duyệt của bạn không hỗ trợ phát âm thanh.
              </audio>
            </div>
          </div>
        `;
        return;
      }

      this.container.innerHTML = `
        <div class="text-center py-20 px-4">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-amber-50 text-amber-500 mb-4">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-slate-800 mb-2">Chưa có dữ liệu câu hỏi</h3>
          <p class="text-slate-500 max-w-md mx-auto">Vui lòng chọn Ngày 1 để bắt đầu luyện tập.</p>
        </div>
      `;
      return;
    }

    const { questions } = this.dayData;

    // Group questions by section
    const sections = [];
    const sectionMap = new Map();
    questions.forEach(q => {
      if (!sectionMap.has(q.section)) {
        sectionMap.set(q.section, []);
        sections.push(q.section);
      }
      sectionMap.get(q.section).push(q);
    });

    let html = `
      <div class="space-y-8 max-w-5xl mx-auto pb-28">
        <!-- Results Banner if submitted -->
        <div id="result-banner-container">
          ${this.isSubmitted && this.scoreResult ? this.renderResultBanner() : ''}
        </div>
    `;

    // Separate sections into non-listening (Vocab, Grammar, Reading) and listening (Choukai)
    const nonListeningSections = [];
    const listeningSections = [];

    sections.forEach(sectionName => {
      const sectionQuestions = sectionMap.get(sectionName);
      const firstQ = sectionQuestions[0];
      const isListening = firstQ?.sectionGroup === 'listening' || sectionName.includes('聴解');
      if (isListening) {
        listeningSections.push(sectionName);
      } else {
        nonListeningSections.push(sectionName);
      }
    });

    // 1. Render all Language Knowledge & Reading Sections (Mondai 1 ~ 14)
    nonListeningSections.forEach(sectionName => {
      html += this.renderSectionBlock(sectionName, sectionMap.get(sectionName));
    });

    // 2. Render Choukai Section (Listening) with Header Divider and Audio Player (Mondai 1 - 5)
    // Audio Player is placed INSIDE this container so it ONLY sticks while scrolling Choukai questions
    if (listeningSections.length > 0) {
      html += `
        <!-- Bounded Choukai Container: Audio Player only sticks while within this container -->
        <div id="choukai-exam-container" class="space-y-8 pt-8 mt-12 border-t-2 border-dashed border-amber-300/80 relative">
          <!-- Big Section Header Divider for Choukai -->
          <div id="choukai-section-header" class="rounded-2xl p-5 sm:p-6 bg-gradient-to-r from-amber-600 via-amber-700 to-indigo-900 text-white shadow-md flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div class="flex items-center gap-3.5">
              <div class="w-12 h-12 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-2xl shadow-inner shrink-0">
                🎧
              </div>
              <div>
                <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-400/25 text-amber-100 text-xs font-bold uppercase tracking-wider mb-1">
                  Phần thi Nghe hiểu • Choukai
                </div>
                <h2 class="text-xl sm:text-2xl font-black text-white tracking-tight">
                  PHẦN THI NGHE HIỂU (聴解)
                </h2>
                <p class="text-xs sm:text-sm text-amber-100/90 mt-0.5">
                  Lắng nghe file âm thanh chính thức và trả lời các câu hỏi từ Mondai 1 đến Mondai 5
                </p>
              </div>
            </div>
          </div>

          <!-- Audio Player Banner (Sticky ONLY while scrolling within Choukai) -->
          ${this.dayData.audio ? `
            <div id="quiz-audio-player-banner" class="sticky top-16 z-20 p-4 rounded-2xl bg-gradient-to-r from-amber-950 via-slate-900 to-indigo-950 text-white shadow-xl border border-amber-500/40 backdrop-blur-md flex flex-col sm:flex-row items-center justify-between gap-4 transition-all duration-300">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold text-lg shadow-xs shrink-0">
                  🎧
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-bold text-amber-300">聴解 (Nghe hiểu)</span>
                    <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-200 border border-amber-500/30">Official Audio</span>
                  </div>
                  <div class="text-xs text-slate-300 font-medium mt-0.5">${this.dayData.title} • File nghe đề thi chính thức</div>
                </div>
              </div>
              <audio id="exam-audio-player" controls preload="auto" class="w-full sm:w-80 h-10 rounded-xl bg-white/10" src="${this.dayData.audio}">
                Trình duyệt không hỗ trợ phát âm thanh.
              </audio>
            </div>
          ` : ''}

          <!-- Choukai Sub-sections (Mondai 1 ~ 5) -->
          <div class="space-y-8">
            ${listeningSections.map(sectionName => this.renderSectionBlock(sectionName, sectionMap.get(sectionName))).join('')}
          </div>
        </div>
      `;
    }

    // Render Bottom Action Bar
    html += `
        <!-- Floating / Sticky Action Bar -->
        <div class="fixed bottom-0 left-0 right-0 z-30 bg-white/95 backdrop-blur-md border-t border-slate-200/90 py-3.5 px-4 shadow-lg lg:pl-72 transition-all" id="quiz-bottom-bar">
          <div class="max-w-5xl mx-auto flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <div class="text-sm">
                <span class="text-slate-500">Đã trả lời:</span>
                <span class="font-bold text-slate-800" id="bottom-answered-count">${Object.keys(this.userAnswers).length}</span>
                <span class="text-slate-400">/ ${questions.length}</span>
              </div>
              <div class="hidden sm:flex items-center gap-1.5 text-xs text-amber-700 bg-amber-50 px-2.5 py-1 rounded-lg border border-amber-200">
                <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"/></svg>
                <span>Khó: <strong id="bottom-flagged-count">${Object.keys(this.userFlags).length}</strong></span>
              </div>
            </div>

            <div class="flex items-center gap-2.5">
              ${this.isSubmitted ? `
                <!-- AnkiConnect Direct Sync Button -->
                <button id="btn-anki-connect-sync" class="inline-flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl text-xs sm:text-sm font-semibold bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 transition active:scale-95 shadow-sm" title="Bắn toàn bộ câu làm sai vào ứng dụng Anki qua AnkiConnect (localhost:8765)">
                  <span>⚡</span>
                  <span>Bắn vào AnkiConnect</span>
                </button>
                <button id="btn-copy-mistakes" class="inline-flex items-center gap-2 px-3.5 py-2.5 rounded-xl text-xs sm:text-sm font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 transition active:scale-95 shadow-sm">
                  <svg class="w-4 h-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
                  </svg>
                  <span>Sao chép câu sai</span>
                </button>
                <button id="btn-retry" class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 hover:bg-slate-900 text-white transition active:scale-95 shadow-sm">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                  </svg>
                  <span>Làm lại từ đầu</span>
                </button>
              ` : `
                <button id="btn-reset-current" class="px-3.5 py-2.5 rounded-xl text-sm font-medium text-slate-600 hover:text-slate-800 hover:bg-slate-100 transition">
                  Đặt lại
                </button>
                <button id="btn-submit" class="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-semibold bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white shadow-md shadow-indigo-200 transition active:scale-95">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <span>Nộp bài & Chấm điểm</span>
                </button>
              `}
            </div>
          </div>
        </div>
      </div>
    `;

    this.container.innerHTML = html;
    this.bindEvents();
    this.applyActiveFilter();
    this.updateTimerDisplay();
  }

  /**
   * Render a complete section group including Section Header and either Split-View or standard cards
   */
  renderSectionBlock(sectionName, sectionQuestions) {
    if (!sectionQuestions || sectionQuestions.length === 0) return '';
    const firstQ = sectionQuestions[0];

    let html = `
      <div class="section-group space-y-5" data-section="${sectionName}">
        <!-- Section Header -->
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl p-5 shadow-sm border border-slate-800">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                ${this.dayData.level ? 'JLPT ' + this.dayData.level : 'JLPT N1'}
              </span>
              <h3 class="text-lg font-bold tracking-tight text-white">${sectionName}</h3>
            </div>
            <span class="text-xs font-medium text-slate-400 bg-slate-800/80 px-2.5 py-1 rounded-lg">
              ${sectionQuestions.length} câu hỏi
            </span>
          </div>
          ${firstQ.instruction ? `
            <p class="mt-2.5 text-sm text-slate-300 font-jp leading-relaxed border-t border-slate-800/60 pt-2.5">
              ${formatBlankSpacing(firstQ.instruction)}
            </p>
          ` : ''}
        </div>
    `;

    // Universal Dokkai Block Grouping:
    // Group consecutive questions that share identical non-empty passage into Split-View blocks.
    // Non-passage questions are rendered as standard vertical cards.
    const passageBlocks = [];
    let currentBlock = null;

    sectionQuestions.forEach(q => {
      const pText = (q.passage || '').trim();
      if (pText) {
        if (currentBlock && currentBlock.isPassage && currentBlock.passage === pText) {
          currentBlock.questions.push(q);
        } else {
          currentBlock = { isPassage: true, passage: pText, questions: [q] };
          passageBlocks.push(currentBlock);
        }
      } else {
        if (currentBlock && !currentBlock.isPassage) {
          currentBlock.questions.push(q);
        } else {
          currentBlock = { isPassage: false, questions: [q] };
          passageBlocks.push(currentBlock);
        }
      }
    });

    // Render each block
    passageBlocks.forEach(block => {
      if (block.isPassage) {
        const qStart = block.questions[0]?.number || '';
        const qEnd = block.questions[block.questions.length - 1]?.number || '';
        const rangeLabel = block.questions.length > 1 ? `Câu ${qStart} 〜 ${qEnd}` : `Câu ${qStart}`;
        const isSplit = this.dokkaiLayout !== 'stacked';
        const isGrammarPassage = block.questions[0]?.sectionGroup === 'vocab_grammar' || (block.questions[0]?.section && block.questions[0].section.includes('問題9'));
        const passageBadgeLabel = isGrammarPassage ? `Đoạn văn điền từ (${rangeLabel})` : `Đoạn văn đọc hiểu (${rangeLabel})`;

        const toolbarHeader = `
          <div class="flex flex-wrap items-center justify-between pb-3 mb-4 border-b border-slate-100 gap-2">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-indigo-600"></span>
              <span class="text-xs font-bold text-slate-800 uppercase tracking-wider">
                ${passageBadgeLabel}
              </span>
            </div>
            <div class="flex items-center gap-2">
              ${isSplit ? `<span class="text-[11px] text-slate-400 font-medium hidden sm:inline">Cuộn độc lập ↕</span>` : ''}
              <!-- Layout Toggle Switch -->
              <div class="inline-flex items-center p-0.5 rounded-xl bg-slate-100 border border-slate-200 text-xs font-semibold">
                <button type="button" 
                        class="btn-dokkai-toggle-split px-2.5 py-1 rounded-lg transition flex items-center gap-1.5 cursor-pointer ${isSplit ? 'bg-white text-indigo-700 shadow-2xs font-bold' : 'text-slate-500 hover:text-slate-800'}"
                        title="Chia đôi màn hình (Cột trái bài đọc, cột phải câu hỏi)">
                  <span>◫</span>
                  <span class="hidden sm:inline">Chia đôi màn hình</span>
                </button>
                <button type="button" 
                        class="btn-dokkai-toggle-stacked px-2.5 py-1 rounded-lg transition flex items-center gap-1.5 cursor-pointer ${!isSplit ? 'bg-white text-indigo-700 shadow-2xs font-bold' : 'text-slate-500 hover:text-slate-800'}"
                        title="Bài đọc ở trên (Bài đọc trải rộng full-width, câu hỏi bên dưới)">
                  <span>☰</span>
                  <span class="hidden sm:inline">Bài đọc ở trên</span>
                </button>
              </div>
            </div>
          </div>
        `;

        if (isSplit) {
          html += `
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              <!-- Left: Sticky Passage (Renders ONCE for all sub-questions) -->
              <div class="lg:col-span-6 xl:col-span-7 lg:sticky lg:top-20">
                <div class="bg-white rounded-2xl border border-slate-200/90 p-5 sm:p-6 shadow-sm max-h-[calc(100vh-6.5rem)] overflow-y-auto">
                  ${toolbarHeader}
                  <div class="question-text font-jp text-slate-900 text-sm sm:text-base leading-loose whitespace-pre-line">
                    ${formatBlankSpacing(block.passage)}
                  </div>
                </div>
              </div>

              <!-- Right: Sub-questions without repeating passage in card -->
              <div class="lg:col-span-6 xl:col-span-5 space-y-5">
                ${block.questions.map(q => this.renderQuestionCard(q, true)).join('')}
              </div>
            </div>
          `;
        } else {
          // Mode 2: Standard View / Bài đọc ở trên (trải rộng full-width)
          html += `
            <div class="space-y-6">
              <!-- Top: Full-width Passage -->
              <div class="w-full">
                <div class="bg-white rounded-2xl border border-slate-200/90 p-6 sm:p-8 shadow-sm">
                  ${toolbarHeader}
                  <div class="question-text font-jp text-slate-900 text-base sm:text-lg leading-loose whitespace-pre-line">
                    ${formatBlankSpacing(block.passage)}
                  </div>
                </div>
              </div>

              <!-- Bottom: Sub-questions full-width -->
              <div class="w-full space-y-5">
                ${block.questions.map(q => this.renderQuestionCard(q, true)).join('')}
              </div>
            </div>
          `;
        }
      } else {
        // Standard vertical cards for questions without passage
        block.questions.forEach(q => {
          html += this.renderQuestionCard(q, false);
        });
      }
    });

    html += `</div>`;
    return html;
  }

  /**
   * Render single question card
   * @param {Object} q Question object
   * @param {Boolean} hidePassageInCard If true (in Split View), do not duplicate the passage inside the card
   */
  renderQuestionCard(q, hidePassageInCard = false) {
    const userChoice = this.userAnswers[q.id];
    const isAnswered = userChoice !== undefined;
    const isCorrect = isAnswered && userChoice === q.answer;
    const isFlagged = !!this.userFlags[q.id];
    const canShowScript = (this.mode === 'practice' || this.isSubmitted) && !!q.script;

    // Card border / highlight based on post-submit state
    let cardStatusClass = 'border-slate-200/80 bg-white';
    if (this.isSubmitted) {
      cardStatusClass = isCorrect ? 'card-correct border-emerald-300 bg-white' : 'card-wrong border-rose-300 bg-white';
    }

    const formattedQuestion = formatQuestionContent(q.question, q.section);

    return `
      <div class="question-card rounded-2xl border ${cardStatusClass} p-5 sm:p-6 shadow-sm transition-card relative" 
           id="question-${q.id}"
           data-question-id="${q.id}" 
           data-status="${this.isSubmitted ? (isCorrect ? 'correct' : 'wrong') : 'pending'}">
        
        <!-- Question Header & Badges -->
        <div class="flex items-center justify-between gap-3 mb-4">
          <div class="flex flex-wrap items-center gap-2">
            <span class="inline-flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm shrink-0 shadow-xs ${
              this.isSubmitted
                ? (isCorrect ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700')
                : (isAnswered ? 'bg-indigo-100 text-indigo-700' : 'bg-slate-100 text-slate-700')
            }">
              ${q.number || ''}
            </span>

            ${q.questionNumber ? `
              <span class="inline-flex items-center px-2.5 py-1 rounded-xl text-xs font-bold bg-amber-500 text-white shadow-xs tracking-wide">
                ${q.questionNumber}
              </span>
            ` : ''}

            ${q.title ? `
              <span class="text-xs font-bold text-amber-900 bg-amber-100/90 border border-amber-300/80 px-2.5 py-1 rounded-xl hidden sm:inline-flex items-center gap-1">
                <span>🎧</span>
                <span>${q.title}</span>
              </span>
            ` : ''}

            <!-- Flag Button to mark as hard -->
            <button type="button" 
                    class="btn-toggle-flag inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium border transition ${
                      isFlagged 
                        ? 'bg-amber-100 border-amber-300 text-amber-800 shadow-xs' 
                        : 'bg-slate-50 border-slate-200 text-slate-400 hover:text-amber-600 hover:bg-amber-50/50'
                    }"
                    data-question-id="${q.id}"
                    title="${isFlagged ? 'Bỏ đánh dấu câu khó' : 'Đánh dấu câu khó để xem lại'}">
              <svg class="w-3.5 h-3.5 ${isFlagged ? 'fill-current text-amber-500' : 'fill-none'}" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"/>
              </svg>
              <span class="text-[11px]">${isFlagged ? 'Khó' : 'Đánh dấu'}</span>
            </button>
          </div>

          <div class="flex items-center gap-2">
            ${this.isSubmitted ? `
              <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${
                isCorrect 
                  ? 'bg-emerald-100/90 text-emerald-800 border border-emerald-200' 
                  : 'bg-rose-100/90 text-rose-800 border border-rose-200'
              }">
                ${isCorrect ? `
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                  Chính xác
                ` : `
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                  Chưa đúng
                `}
              </span>
            ` : `
              <span class="text-xs px-2.5 py-1 rounded-md ${isAnswered ? 'bg-indigo-50 text-indigo-600 font-medium' : 'text-slate-400'}">
                ${isAnswered ? 'Đã chọn' : 'Chưa làm'}
              </span>
            `}
          </div>
        </div>

        <!-- Optional Passage (shown only if not in Split View) -->
        ${!hidePassageInCard && q.passage ? `
          <div class="mb-5 p-4 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 font-jp leading-loose text-sm sm:text-base whitespace-pre-line">
            <div class="text-xs font-bold text-slate-500 uppercase mb-2 flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
              Đoạn văn đọc hiểu
            </div>
            ${formatBlankSpacing(q.passage)}
          </div>
        ` : ''}

        <!-- Choukai Sub-Header: Mondai & Audio Track Info -->
        ${q.sectionGroup === 'listening' ? `
          <div class="flex flex-wrap items-center gap-2 mb-3.5 px-3 py-1.5 rounded-xl bg-amber-50/90 border border-amber-200/80 text-xs font-semibold text-amber-900 w-fit">
            <span>🎧</span>
            <span>${q.section || '聴解'}</span>
            ${q.questionNumber ? `<span class="text-amber-400">•</span><span class="font-bold text-amber-700 bg-amber-200/70 px-1.5 py-0.5 rounded-md">${q.questionNumber}</span>` : ''}
          </div>
        ` : ''}

        <!-- Question Text (With enhanced authentic JLPT slots for Problem 6) -->
        <div class="question-text text-base sm:text-lg text-slate-900 mb-5 font-jp">
          ${formattedQuestion}
        </div>

        <!-- Optional Image (Illustration for Choukai / Diagram) -->
        ${q.image ? `
          <div class="choukai-image-container mb-5 text-center">
            <div class="inline-block relative group">
              <img src="${q.image}" 
                   alt="Hình minh họa đề thi" 
                   class="question-illustration-img max-h-72 sm:max-h-96 w-auto max-w-full rounded-2xl border border-slate-200/90 shadow-2xs mx-auto cursor-zoom-in hover:brightness-95 transition active:scale-99" 
                   data-zoom-src="${q.image}">
              <div class="mt-2 text-xs text-slate-500 flex items-center justify-center gap-1.5 font-medium">
                <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"/></svg>
                <span>Bấm vào hình để phóng to xem chi tiết</span>
              </div>
            </div>
          </div>
        ` : ''}

        <!-- Options List: 100% Vertical Stack (Mỗi đáp án 1 hàng dọc độc lập) -->
        <div class="options-container flex flex-col space-y-2.5 w-full mb-4">
          ${q.options.map((optText, optIdx) => {
            const isSelected = userChoice === optIdx;
            const isThisCorrect = q.answer === optIdx;

            let optionStyle = 'border-slate-200 hover:border-indigo-300 hover:bg-slate-50/80 text-slate-700';
            let indicatorStyle = 'border-slate-300 text-slate-500 bg-white';

            if (!this.isSubmitted) {
              if (isSelected) {
                optionStyle = 'border-indigo-600 bg-indigo-50/60 text-indigo-950 ring-2 ring-indigo-500/20 font-medium';
                indicatorStyle = 'border-indigo-600 bg-indigo-600 text-white font-bold';
              }
            } else {
              // Post submission state
              if (isThisCorrect) {
                optionStyle = 'border-emerald-500 bg-emerald-50 text-emerald-950 ring-2 ring-emerald-400/30 font-semibold';
                indicatorStyle = 'border-emerald-600 bg-emerald-600 text-white font-bold';
              } else if (isSelected && !isThisCorrect) {
                optionStyle = 'border-rose-400 bg-rose-50 text-rose-950 ring-2 ring-rose-400/30 font-medium';
                indicatorStyle = 'border-rose-500 bg-rose-500 text-white font-bold';
              } else {
                optionStyle = 'border-slate-200 text-slate-400 opacity-70';
                indicatorStyle = 'border-slate-200 text-slate-400 bg-slate-50';
              }
            }

            return `
              <button type="button" 
                      class="option-item ${this.isSubmitted ? 'locked cursor-default' : 'cursor-pointer'} w-full text-left p-3.5 sm:p-4 rounded-xl border ${optionStyle} flex items-start gap-3 transition-card"
                      data-question-id="${q.id}"
                      data-option-index="${optIdx}"
                      ${this.isSubmitted ? 'disabled' : ''}>
                <span class="inline-flex items-center justify-center w-6 h-6 rounded-lg text-xs font-semibold border ${indicatorStyle} shrink-0 mt-0.5">
                  ${optIdx + 1}
                </span>
                <span class="font-jp text-sm sm:text-base leading-relaxed flex-1 break-words">
                  ${optText}
                </span>
                ${this.isSubmitted && isThisCorrect ? `
                  <svg class="w-5 h-5 text-emerald-600 shrink-0 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                ` : ''}
                ${this.isSubmitted && isSelected && !isThisCorrect ? `
                  <svg class="w-5 h-5 text-rose-500 shrink-0 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                ` : ''}
              </button>
            `;
          }).join('')}
        </div>

        <!-- Explanation & Script Accordion -->
        ${canShowScript ? `
          <!-- Choukai Audio Script Accordion -->
          <div class="mt-4 pt-3.5 border-t border-slate-100">
            <div class="choukai-script-container">
              <button type="button" 
                      class="btn-toggle-script w-full flex items-center justify-between p-3 rounded-xl bg-slate-50 hover:bg-indigo-50/70 border border-slate-200 hover:border-indigo-200 transition group cursor-pointer text-left" 
                      data-target="script-${q.id}">
                <div class="flex items-center gap-2">
                  <span class="text-base">📜</span>
                  <span class="text-xs sm:text-sm font-bold text-slate-700 group-hover:text-indigo-700 transition">
                    Xem Script lời thoại bài nghe
                  </span>
                  <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100">
                    Audio Transcript
                  </span>
                </div>
                <svg class="script-chevron w-4 h-4 text-slate-400 group-hover:text-indigo-600 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>

              <!-- Collapsible Script Content -->
              <div id="script-${q.id}" class="script-content hidden mt-3 p-4 sm:p-5 rounded-2xl bg-gradient-to-b from-slate-50 to-indigo-50/20 border border-indigo-100 text-slate-800 text-sm animate-fade-in space-y-3">
                <div class="flex items-center justify-between pb-2 border-b border-indigo-100/80">
                  <span class="text-xs font-bold text-indigo-950 uppercase tracking-wider flex items-center gap-1.5">
                    <span>🎙️</span> Lời thoại bài nghe (Transcript)
                  </span>
                  <span class="text-[11px] text-slate-400 font-medium">Tiếng Nhật có phân vai</span>
                </div>

                <!-- Dialogue text with speaker formatting -->
                <div class="font-jp text-slate-900 text-sm sm:text-base leading-relaxed script-text">
                  ${formatScriptText(q.script)}
                </div>

                <!-- Explanation & Correct Answer Conclusion below script -->
                ${q.explanation ? `
                  <div class="mt-3 pt-3 border-t border-indigo-100 bg-white/80 p-3.5 rounded-xl border border-indigo-100/80">
                    <div class="flex items-center justify-between gap-2 mb-1.5">
                      <div class="flex items-center gap-1.5 text-xs font-bold text-emerald-800">
                        <svg class="w-4 h-4 text-emerald-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        <span>Giải thích & Chốt đáp án đúng</span>
                      </div>
                      <button type="button" 
                              class="btn-gemini-explain inline-flex items-center justify-center w-7 h-7 rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white shadow-xs transition active:scale-95 btn-gemini-sparkle"
                              data-question-id="${q.id}"
                              title="✨ Hỏi Gemini phân tích sâu câu này">
                        <span class="text-sm">✨</span>
                      </button>
                    </div>
                    <div class="text-xs sm:text-sm text-slate-700 leading-relaxed font-jp whitespace-pre-line pl-5">
                      ${q.explanation}
                    </div>
                  </div>
                ` : ''}
              </div>
            </div>
          </div>
        ` : (this.isSubmitted && q.explanation ? `
          <div class="mt-4 pt-4 border-t border-slate-100">
            <div class="rounded-xl bg-amber-50/80 border border-amber-200/80 p-4 text-slate-800 text-sm">
              <div class="flex items-center justify-between gap-2 mb-2">
                <div class="flex items-center gap-2 font-bold text-amber-900">
                  <svg class="w-4 h-4 text-amber-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <span>Giải thích chi tiết</span>
                </div>

                <!-- Minimalist Single-icon Sparkle Gemini Button -->
                <button type="button" 
                        class="btn-gemini-explain inline-flex items-center justify-center w-7 h-7 rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white shadow-xs transition active:scale-95 btn-gemini-sparkle"
                        data-question-id="${q.id}"
                        title="✨ Hỏi Gemini phân tích sâu câu này">
                  <span class="text-sm">✨</span>
                </button>
              </div>

              <div class="font-jp text-slate-800 whitespace-pre-line leading-relaxed pl-6">
                ${q.explanation}
              </div>
            </div>
          </div>
        ` : '')}

      </div>
    `;
  }

  /**
   * Render Result Banner shown upon submission
   */
  renderResultBanner() {
    const { total, correct, percentage, isPassed } = this.scoreResult;
    const wrongCount = total - correct;

    return `
      <div class="bg-gradient-to-br from-indigo-900 via-slate-900 to-indigo-950 text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-indigo-500/20 mb-8 animate-toast">
        <div class="flex flex-col md:flex-row items-center justify-between gap-6">
          <div class="text-center md:text-left space-y-2">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold ${
              isPassed ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
            }">
              <span>${isPassed ? `合格 • ĐẠT CHUẨN ${this.dayData.level || 'N1'}` : '不合格 • CẦN CỐ GẮNG'}</span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight">
              ${isPassed ? 'Chúc mừng! Bạn đã hoàn thành rất tốt!' : 'Hoàn thành bài luyện tập!'}
            </h2>
            <p class="text-slate-300 text-sm max-w-md">
              ${isPassed 
                ? 'Kiến thức từ vựng và ngữ pháp của ngày này đã nắm chắc. Hãy xem lại các câu chưa đúng nếu có.' 
                : 'Đừng nản lòng! Hãy bấm nút "Bắn vào AnkiConnect" hoặc "Sao chép câu sai" bên dưới để ôn tập lại nhé.'}
            </p>
          </div>

          <!-- Score circle / metric -->
          <div class="flex items-center gap-4 bg-white/5 backdrop-blur-sm px-6 py-4 rounded-2xl border border-white/10 shrink-0">
            <div class="text-center">
              <div class="text-3xl sm:text-4xl font-black text-indigo-300">${correct}<span class="text-lg font-normal text-slate-400">/${total}</span></div>
              <div class="text-xs text-slate-400 font-medium">Số câu đúng</div>
            </div>
            <div class="h-10 w-px bg-white/10"></div>
            <div class="text-center">
              <div class="text-3xl sm:text-4xl font-black ${isPassed ? 'text-emerald-400' : 'text-amber-400'}">${percentage}%</div>
              <div class="text-xs text-slate-400 font-medium">Tỷ lệ chính xác</div>
            </div>
          </div>
        </div>

        <!-- Filter tabs for quick review & Anki Actions -->
        <div class="mt-6 pt-6 border-t border-white/10 flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <span class="text-xs text-slate-400 mr-1">Bộ lọc:</span>
            <button type="button" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              this.activeFilter === 'all' ? 'bg-white text-slate-900 shadow-sm' : 'bg-white/10 text-slate-300 hover:bg-white/20'
            }" data-filter="all">
              Tất cả (${total})
            </button>
            <button type="button" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              this.activeFilter === 'wrong' ? 'bg-rose-500 text-white shadow-sm' : 'bg-white/10 text-slate-300 hover:bg-white/20'
            }" data-filter="wrong">
              Câu sai (${wrongCount})
            </button>
            <button type="button" class="filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              this.activeFilter === 'correct' ? 'bg-emerald-500 text-white shadow-sm' : 'bg-white/10 text-slate-300 hover:bg-white/20'
            }" data-filter="correct">
              Câu đúng (${correct})
            </button>
          </div>

          <div class="flex items-center gap-2">
            <button id="btn-anki-connect-banner" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500/30 hover:bg-emerald-500/40 text-emerald-200 border border-emerald-400/30 transition">
              <span>⚡</span>
              <span>Bắn vào AnkiConnect</span>
            </button>
            <button id="btn-copy-mistakes-banner" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-500/30 hover:bg-indigo-500/40 text-indigo-200 border border-indigo-400/30 transition">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
              <span>Sao chép câu sai</span>
            </button>
            <button id="btn-retry-banner" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-rose-500/30 hover:bg-rose-500/40 text-rose-200 border border-rose-400/30 transition">
              <span>🔄</span>
              <span>Làm lại từ đầu</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Question Palette (Matrix) rendering
   */
  renderPalette() {
    const paletteContainer = document.getElementById('question-palette-grid');
    if (!paletteContainer || !this.dayData || !this.dayData.questions) return;

    const questions = this.dayData.questions;

    paletteContainer.innerHTML = questions.map((q, idx) => {
      const isAnswered = this.userAnswers[q.id] !== undefined;
      const isFlagged = !!this.userFlags[q.id];
      const isCurrent = idx === this.currentQuestionIndex;

      // Determine CSS class based on priority: Flagged (Yellow) > Answered (Blue) > Unanswered (Transparent/gray border)
      let statusClass = 'status-unanswered';
      if (isFlagged) {
        statusClass = 'status-flagged';
      } else if (isAnswered) {
        statusClass = 'status-answered';
      }

      return `
        <button type="button" 
                class="palette-btn w-9 h-9 rounded-xl text-xs font-semibold flex items-center justify-center relative transition-all ${statusClass} ${isCurrent ? 'ring-2 ring-indigo-500 ring-offset-1 font-bold' : ''}"
                data-palette-qid="${q.id}"
                data-palette-index="${idx}"
                data-q-num="${q.number}"
                title="Câu ${q.number} (${q.section})">
          ${q.number}
          ${isFlagged ? `
            <span class="absolute -top-1 -right-1 w-2.5 h-2.5 bg-amber-500 rounded-full border border-white"></span>
          ` : ''}
        </button>
      `;
    }).join('');

    // Update Palette Stats Summary
    this.updatePaletteStats();

    // Bind clicks on palette buttons to jump smoothly to question
    const paletteBtns = paletteContainer.querySelectorAll('.palette-btn');
    paletteBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const qid = btn.getAttribute('data-palette-qid');
        const idx = parseInt(btn.getAttribute('data-palette-index'), 10);
        this.currentQuestionIndex = isNaN(idx) ? 0 : idx;
        this.updateActivePaletteTile();
        this.scrollToQuestion(qid);
      });
    });
  }

  updateActivePaletteTile() {
    const allBtns = document.querySelectorAll('.palette-btn');
    allBtns.forEach((btn, idx) => {
      if (idx === this.currentQuestionIndex) {
        btn.classList.add('ring-2', 'ring-indigo-500', 'ring-offset-1', 'font-bold');
      } else {
        btn.classList.remove('ring-2', 'ring-indigo-500', 'ring-offset-1', 'font-bold');
      }
    });
  }

  updatePaletteTile(questionId) {
    const paletteBtn = document.querySelector(`.palette-btn[data-palette-qid="${questionId}"]`);
    if (!paletteBtn) return;

    const isAnswered = this.userAnswers[questionId] !== undefined;
    const isFlagged = !!this.userFlags[questionId];
    const qNum = paletteBtn.getAttribute('data-q-num');
    const idx = parseInt(paletteBtn.getAttribute('data-palette-index'), 10);
    const isCurrent = idx === this.currentQuestionIndex;

    let statusClass = 'status-unanswered';
    if (isFlagged) {
      statusClass = 'status-flagged';
    } else if (isAnswered) {
      statusClass = 'status-answered';
    }

    paletteBtn.className = `palette-btn w-9 h-9 rounded-xl text-xs font-semibold flex items-center justify-center relative transition-all ${statusClass} ${isCurrent ? 'ring-2 ring-indigo-500 ring-offset-1 font-bold' : ''}`;
    paletteBtn.innerHTML = `
      ${qNum}
      ${isFlagged ? `<span class="absolute -top-1 -right-1 w-2.5 h-2.5 bg-amber-500 rounded-full border border-white"></span>` : ''}
    `;

    this.updatePaletteStats();
  }

  updatePaletteStats() {
    if (!this.dayData || !this.dayData.questions) return;
    const total = this.dayData.questions.length;
    const answered = Object.keys(this.userAnswers).length;
    const flagged = Object.keys(this.userFlags).length;
    const unanswered = Math.max(0, total - answered);

    const statAnswered = document.getElementById('palette-stat-answered');
    const statFlagged = document.getElementById('palette-stat-flagged');
    const statUnanswered = document.getElementById('palette-stat-unanswered');
    const bottomFlagged = document.getElementById('bottom-flagged-count');

    if (statAnswered) statAnswered.textContent = answered;
    if (statFlagged) statFlagged.textContent = flagged;
    if (statUnanswered) statUnanswered.textContent = unanswered;
    if (bottomFlagged) bottomFlagged.textContent = flagged;
  }

  scrollToQuestion(questionId) {
    if (this.dayData && this.dayData.questions) {
      const idx = this.dayData.questions.findIndex(q => q.id === questionId);
      if (idx !== -1) {
        this.currentQuestionIndex = idx;
        this.updateActivePaletteTile();
      }
    }

    const card = document.getElementById(`question-${questionId}`);
    if (card) {
      card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      // Temporary pulse highlight ring
      card.classList.add('ring-4', 'ring-indigo-400/50');
      setTimeout(() => {
        card.classList.remove('ring-4', 'ring-indigo-400/50');
      }, 1500);
    }
  }

  /**
   * Bind DOM event listeners
   */
  bindEvents() {
    // Option click
    const optionButtons = this.container.querySelectorAll('.option-item:not(.locked)');
    optionButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const questionId = btn.getAttribute('data-question-id');
        const optionIndex = parseInt(btn.getAttribute('data-option-index'), 10);
        this.selectOption(questionId, optionIndex);
      });
    });

    // Toggle Flag (Hard Question) click
    const flagButtons = this.container.querySelectorAll('.btn-toggle-flag');
    flagButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const questionId = btn.getAttribute('data-question-id');
        this.toggleFlag(questionId);
      });
    });

    // Gemini Deep-dive Explain buttons (Compact ✨)
    const geminiButtons = this.container.querySelectorAll('.btn-gemini-explain');
    geminiButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const questionId = btn.getAttribute('data-question-id');
        const question = this.dayData.questions.find(q => q.id === questionId);
        if (question) {
          this.geminiModal.open(question);
        }
      });
    });

    // Submit button
    const submitBtn = this.container.querySelector('#btn-submit');
    if (submitBtn) {
      submitBtn.addEventListener('click', () => this.submitQuiz());
    }

    // Reset current answers (before submit)
    const resetCurrentBtn = this.container.querySelector('#btn-reset-current');
    if (resetCurrentBtn) {
      resetCurrentBtn.addEventListener('click', () => {
        if (confirm('Bạn có chắc muốn xóa tất cả lựa chọn hiện tại để làm lại không?')) {
          this.userAnswers = {};
          this.userFlags = {};
          storage.resetDay(this.getStorageKey());
          this.render();
          this.renderPalette();
          this.updateProgress();
        }
      });
    }

    // Retry button (after submit: sticky bar & top banner)
    const retryBtns = [
      this.container.querySelector('#btn-retry'),
      this.container.querySelector('#btn-retry-banner')
    ].filter(Boolean);

    retryBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        if (confirm('Làm lại từ đầu cho đề/ngày này? Kết quả và các lựa chọn sẽ được thiết lập lại.')) {
          const key = this.getStorageKey();
          const examId = this.getExamId();
          storage.resetDay(key);
          storage.resetDay(examId);
          storage.removeExamHistoryRecord(examId);
          window.dispatchEvent(new CustomEvent('koala:exam-reset', { detail: { examId } }));

          this.userAnswers = {};
          this.userFlags = {};
          this.isSubmitted = false;
          this.scoreResult = null;
          this.activeFilter = 'all';
          this.examSecondsRemaining = this.examDuration;
          localStorage.removeItem(`n1_quiz_exam_seconds_${key}`);
          localStorage.removeItem(`n1_quiz_exam_seconds_${examId}`);

          if (this.mode === 'exam') {
            this.startTimer();
          }

          this.render();
          this.renderPalette();
          this.updateProgress();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      });
    });

    // Copy mistakes button (in sticky bar and banner)
    const copyBtns = [
      this.container.querySelector('#btn-copy-mistakes'),
      this.container.querySelector('#btn-copy-mistakes-banner')
    ].filter(Boolean);

    copyBtns.forEach(btn => {
      btn.addEventListener('click', () => this.handleCopyMistakes());
    });

    // AnkiConnect direct sync buttons
    const ankiSyncBtns = [
      this.container.querySelector('#btn-anki-connect-sync'),
      this.container.querySelector('#btn-anki-connect-banner')
    ].filter(Boolean);

    ankiSyncBtns.forEach(btn => {
      btn.addEventListener('click', () => this.handleAnkiConnectSync());
    });

    // Filter buttons
    const filterBtns = this.container.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const filter = btn.getAttribute('data-filter');
        this.activeFilter = filter;
        this.render();
      });
    });

    // Dokkai layout toggles (Split-View vs Stacked/Top)
    const splitBtns = this.container.querySelectorAll('.btn-dokkai-toggle-split');
    splitBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.setDokkaiLayout('split');
      });
    });

    const stackedBtns = this.container.querySelectorAll('.btn-dokkai-toggle-stacked');
    stackedBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.setDokkaiLayout('stacked');
      });
    });

    // Image Zoom / Lightbox for Choukai illustrations & diagrams
    const illustrationImgs = this.container.querySelectorAll('.question-illustration-img');
    illustrationImgs.forEach(img => {
      img.addEventListener('click', (e) => {
        e.stopPropagation();
        const src = img.getAttribute('data-zoom-src') || img.src;
        this.openImageLightbox(src);
      });
    });

    // Choukai Audio Script Accordion Toggle
    const scriptToggleBtns = this.container.querySelectorAll('.btn-toggle-script');
    scriptToggleBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const targetId = btn.getAttribute('data-target');
        const content = document.getElementById(targetId);
        const chevron = btn.querySelector('.script-chevron');
        if (!content) return;

        const isHidden = content.classList.contains('hidden');
        if (isHidden) {
          content.classList.remove('hidden');
          if (chevron) chevron.classList.add('rotate-180');
        } else {
          content.classList.add('hidden');
          if (chevron) chevron.classList.remove('rotate-180');
        }
      });
    });
  }

  /**
   * Option selection logic
   */
  selectOption(questionId, optionIndex) {
    if (this.isSubmitted) return;

    this.userAnswers[questionId] = optionIndex;
    storage.saveAnswer(this.getStorageKey(), questionId, optionIndex);

    // Update UI directly for speed without full re-render
    const card = this.container.querySelector(`.question-card[data-question-id="${questionId}"]`);
    if (card) {
      const allOptions = card.querySelectorAll('.option-item');
      allOptions.forEach((btn) => {
        const idx = parseInt(btn.getAttribute('data-option-index'), 10);
        const badge = btn.querySelector('span:first-child');
        if (idx === optionIndex) {
          btn.className = 'option-item cursor-pointer w-full text-left p-3.5 rounded-xl border border-indigo-600 bg-indigo-50/60 text-indigo-950 ring-2 ring-indigo-500/20 font-medium flex items-start gap-3 transition-card';
          badge.className = 'inline-flex items-center justify-center w-6 h-6 rounded-lg text-xs font-semibold border border-indigo-600 bg-indigo-600 text-white font-bold shrink-0 mt-0.5';
        } else {
          btn.className = 'option-item cursor-pointer w-full text-left p-3.5 rounded-xl border border-slate-200 hover:border-indigo-300 hover:bg-slate-50/80 text-slate-700 flex items-start gap-3 transition-card';
          badge.className = 'inline-flex items-center justify-center w-6 h-6 rounded-lg text-xs font-semibold border border-slate-300 text-slate-500 bg-white shrink-0 mt-0.5';
        }
      });

      const statusBadge = card.querySelector('div.flex.items-center.gap-2 span');
      if (statusBadge) {
        statusBadge.className = 'text-xs px-2.5 py-1 rounded-md bg-indigo-50 text-indigo-600 font-medium';
        statusBadge.textContent = 'Đã chọn';
      }
    }

    // Update Question Palette tile
    this.updatePaletteTile(questionId);
    this.updateProgress();
  }

  /**
   * Toggle question flagged state (hard question)
   */
  toggleFlag(questionId) {
    const isNowFlagged = storage.toggleFlag(this.getStorageKey(), questionId);
    if (isNowFlagged) {
      this.userFlags[questionId] = true;
    } else {
      delete this.userFlags[questionId];
    }

    // Update Flag button on card
    const card = this.container.querySelector(`.question-card[data-question-id="${questionId}"]`);
    if (card) {
      const flagBtn = card.querySelector('.btn-toggle-flag');
      if (flagBtn) {
        flagBtn.className = `btn-toggle-flag inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium border transition ${
          isNowFlagged 
            ? 'bg-amber-100 border-amber-300 text-amber-800 shadow-xs' 
            : 'bg-slate-50 border-slate-200 text-slate-400 hover:text-amber-600 hover:bg-amber-50/50'
        }`;
        flagBtn.innerHTML = `
          <svg class="w-3.5 h-3.5 ${isNowFlagged ? 'fill-current text-amber-500' : 'fill-none'}" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"/>
          </svg>
          <span class="text-[11px]">${isNowFlagged ? 'Khó' : 'Đánh dấu'}</span>
        `;
        flagBtn.title = isNowFlagged ? 'Bỏ đánh dấu câu khó' : 'Đánh dấu câu khó để xem lại';
      }
    }

    // Update Question Palette tile
    this.updatePaletteTile(questionId);

    const question = this.dayData.questions.find(q => q.id === questionId);
    const qNum = question ? question.number : '';
    if (isNowFlagged) {
      this.showToast(`Đã đánh dấu câu ${qNum} là câu khó.`, 'info');
    } else {
      this.showToast(`Đã bỏ đánh dấu câu ${qNum}.`, 'info');
    }
  }

  /**
   * Submit and calculate score
   */
  submitQuiz(isTimeout = false) {
    const total = this.dayData.questions.length;
    const answeredCount = Object.keys(this.userAnswers).length;

    if (!isTimeout && answeredCount < total) {
      const remaining = total - answeredCount;
      const proceed = confirm(`Bạn còn ${remaining} câu chưa trả lời. Bạn có chắc chắn muốn nộp bài ngay bây giờ không?`);
      if (!proceed) return;
    }

    let correct = 0;
    this.dayData.questions.forEach(q => {
      if (this.userAnswers[q.id] === q.answer) {
        correct++;
      }
    });

    const percentage = Math.round((correct / total) * 100);
    const isPassed = percentage >= 60; // 60% standard pass line

    this.scoreResult = {
      total,
      correct,
      percentage,
      isPassed
    };

    this.isSubmitted = true;
    this.pauseTimer();

    const now = new Date();
    const pad = (n) => String(n).padStart(2, '0');
    const completedAt = `${pad(now.getDate())}/${pad(now.getMonth() + 1)}/${now.getFullYear()} ${pad(now.getHours())}:${pad(now.getMinutes())}`;
    const examId = this.getExamId();

    const historyRecord = {
      examId: examId,
      lastScore: correct,
      totalQuestions: total,
      percentage: percentage,
      completedAt: completedAt,
      userAnswers: { ...this.userAnswers },
      flaggedQuestions: Object.keys(this.userFlags)
    };

    // Save to official koala_exam_history storage
    storage.saveExamHistoryRecord(examId, historyRecord);

    // Save session submission status for in-quiz results view
    storage.saveSubmission(this.getStorageKey(), {
      scoreResult: this.scoreResult,
      submittedAt: now.toISOString()
    });

    // Notify app to update score badges on Home dashboard and sidebar
    window.dispatchEvent(new CustomEvent('koala:exam-submitted', { detail: historyRecord }));

    this.render();
    this.renderPalette();
    window.scrollTo({ top: 0, behavior: 'smooth' });

    if (isTimeout) {
      this.showToast(`⏰ Hết giờ làm bài! Hệ thống đã nộp bài: bạn đạt ${correct}/${total} câu (${percentage}%).`, 'error');
    } else {
      this.showToast(`Đã chấm điểm! Bạn đạt ${correct}/${total} câu (${percentage}%).`, 'info');
    }
  }

  /**
   * Filter card visibility
   */
  applyActiveFilter() {
    if (!this.isSubmitted || this.activeFilter === 'all') return;

    const cards = this.container.querySelectorAll('.question-card');
    cards.forEach(card => {
      const status = card.getAttribute('data-status');
      if (this.activeFilter === 'wrong' && status !== 'wrong') {
        card.classList.add('hidden');
      } else if (this.activeFilter === 'correct' && status !== 'correct') {
        card.classList.add('hidden');
      } else {
        card.classList.remove('hidden');
      }
    });

    // Hide empty section groups if all questions in section are filtered out
    const sections = this.container.querySelectorAll('.section-group');
    sections.forEach(sec => {
      const visibleCards = sec.querySelectorAll('.question-card:not(.hidden)');
      if (visibleCards.length === 0) {
        sec.classList.add('hidden');
      } else {
        sec.classList.remove('hidden');
      }
    });
  }

  /**
   * Handle copy wrong answers to clipboard
   */
  async handleCopyMistakes() {
    const report = buildMistakesReport(this.dayData.title, this.dayData.questions, this.userAnswers);
    if (!report) {
      this.showToast('Tuyệt vời! Bạn không làm sai câu nào để xuất báo cáo.', 'success');
      return;
    }

    const success = await copyTextToClipboard(report);
    if (success) {
      this.showToast('Đã sao chép danh sách câu sai vào Clipboard!', 'success');
    } else {
      this.showToast('Không thể sao chép tự động. Vui lòng cấp quyền Clipboard.', 'error');
    }
  }

  /**
   * Direct sync to AnkiConnect API
   */
  async handleAnkiConnectSync() {
    this.showToast('Đang kết nối AnkiConnect (localhost:8765)...', 'info');
    const result = await sendMistakesToAnkiConnect(this.dayData.title, this.dayData.questions, this.userAnswers);

    if (result.success) {
      if (result.message === 'no_mistakes') {
        this.showToast('🎉 Bạn không làm sai câu nào nên không cần thêm vào Anki!', 'success');
      } else {
        this.showToast(`⚡ Đã bắn thành công ${result.count} câu sai vào Deck "${result.deckName}" trong Anki!`, 'success');
      }
    } else {
      this.showToast('⚠️ Không thể kết nối AnkiConnect (localhost:8765). Hãy mở app Anki & cài AnkiConnect!', 'error');
    }
  }

  /**
   * Update Progress bar in header and bottom bar
   */
  updateProgress() {
    if (!this.dayData || !this.dayData.questions) return;
    const total = this.dayData.questions.length;
    const answered = Object.keys(this.userAnswers).length;
    const percent = total > 0 ? Math.round((answered / total) * 100) : 0;

    const bottomCount = this.container.querySelector('#bottom-answered-count');
    if (bottomCount) {
      bottomCount.textContent = answered;
    }

    if (typeof this.onProgressUpdate === 'function') {
      this.onProgressUpdate({ answered, total, percent, isSubmitted: this.isSubmitted });
    }
  }

  showToast(message, type = 'info') {
    window.dispatchEvent(new CustomEvent('app:toast', { detail: { message, type } }));
  }
}
