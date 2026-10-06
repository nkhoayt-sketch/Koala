/**
 * Koala JLPT Hub - Shin Kanzen Master Dokkai N1 Engine
 * 2-Column Responsive Workspace with Sticky Timer Dock, Pre-start Blur Lock,
 * Single-Correct Logic Mastery, and Universal N1 Vocab Tooltip & Anki Harvest Engine
 */

import { downloadAnkiTxtFile } from './export.js';

export const TIMER_CONFIGS = {
  short: {
    name: 'Đoản văn (Short)',
    standard: { seconds: 180, label: '3 phút', badge: '🟢 Chuẩn thi (3 phút)' },
    hardcore: { seconds: 120, label: '2 phút', badge: '🔥 Hardcore (2 phút)' },
    unlimited: { seconds: 0, label: 'Không giới hạn', badge: '☕ Không giới hạn' }
  },
  medium: {
    name: 'Trung văn (Medium)',
    standard: { seconds: 450, label: '7.5 phút', badge: '🟢 Chuẩn thi (7.5 phút)' },
    hardcore: { seconds: 330, label: '5.5 phút', badge: '🔥 Hardcore (5.5 phút)' },
    unlimited: { seconds: 0, label: 'Không giới hạn', badge: '☕ Không giới hạn' }
  },
  long: {
    name: 'Trường văn (Long)',
    standard: { seconds: 660, label: '11 phút', badge: '🟢 Chuẩn thi (11 phút)' },
    hardcore: { seconds: 480, label: '8 phút', badge: '🔥 Hardcore (8 phút)' },
    unlimited: { seconds: 0, label: 'Không giới hạn', badge: '☕ Không giới hạn' }
  },
  compare: {
    name: 'So sánh (Compare)',
    standard: { seconds: 540, label: '9 phút', badge: '🟢 Chuẩn thi (9 phút)' },
    hardcore: { seconds: 420, label: '7 phút', badge: '🔥 Hardcore (7 phút)' },
    unlimited: { seconds: 0, label: 'Không giới hạn', badge: '☕ Không giới hạn' }
  },
  search: {
    name: 'Tìm thông tin (Search)',
    standard: { seconds: 240, label: '4 phút', badge: '🟢 Chuẩn thi (4 phút)' },
    hardcore: { seconds: 150, label: '2.5 phút', badge: '🔥 Hardcore (2.5 phút)' },
    unlimited: { seconds: 0, label: 'Không giới hạn', badge: '☕ Không giới hạn' }
  }
};

export class DokkaiEngine {
  constructor(containerEl, appInstance) {
    this.containerEl = containerEl;
    this.app = appInstance;

    this.chapterData = null;
    this.questions = [];
    this.currentIndex = 0;

    // State per question
    this.step = 1; // 1: Reading & Timer, 2: Logic Highlights, Trap Breakdown & Vocab Tooltips
    this.isStarted = false; // Blur/Lock overlay before user clicks Start
    this.selectedOption = null; // 0, 1, 2, 3
    this.userAnswersHistory = {}; // { questionId: { selectedOption, isCorrect, timeSpent } }

    // Anki Harvest State: Map of word -> { word, reading, hanviet, meaning, context }
    this.savedVocab = new Map();

    // Timer State
    this.timerMode = 'standard'; // 'standard' | 'hardcore' | 'unlimited'
    this.totalTimerSeconds = 180;
    this.remainingSeconds = 180;
    this.elapsedSeconds = 0;
    this.timerInterval = null;
    this.isTimerRunning = false;
    this.isTimeUp = false;

    // Active tooltip element state
    this.activeTooltipEl = null;
  }

  /**
   * Load chapter data and initialize first reading
   */
  loadChapter(chapterData, initialIndex = 0) {
    this.chapterData = chapterData;
    this.questions = chapterData.questions || [];
    this.currentIndex = Math.max(0, Math.min(initialIndex, this.questions.length - 1));
    this.resetQuestionState();
    this.render();
  }

  resetQuestionState() {
    this.stopTimer();
    this.step = 1;
    this.isStarted = false;
    this.selectedOption = null;
    this.isTimerRunning = false;
    this.isTimeUp = false;
    this.elapsedSeconds = 0;

    const currentQ = this.getCurrentQuestion();
    const qType = (currentQ && currentQ.mondaiType) || 'short';
    const cfg = TIMER_CONFIGS[qType] || TIMER_CONFIGS.short;
    const defaultTimer = cfg[this.timerMode] || cfg.standard;
    this.totalTimerSeconds = defaultTimer.seconds;
    this.remainingSeconds = defaultTimer.seconds;
  }

  getCurrentQuestion() {
    return this.questions[this.currentIndex] || null;
  }

  // ==============================================================
  // TIMER CONTROLS
  // ==============================================================

  setTimerMode(mode) {
    if (this.isTimerRunning) return; // Prevent change mid-reading
    this.timerMode = mode;
    const currentQ = this.getCurrentQuestion();
    const qType = (currentQ && currentQ.mondaiType) || 'short';
    const cfg = TIMER_CONFIGS[qType] || TIMER_CONFIGS.short;
    const target = cfg[mode] || cfg.standard;
    this.totalTimerSeconds = target.seconds;
    this.remainingSeconds = target.seconds;
    this.render();
  }

  startReading() {
    this.isStarted = true;
    this.startTimer();
    this.render();
  }

  startTimer() {
    if (this.isTimerRunning) return;
    this.isTimerRunning = true;
    this.isTimeUp = false;

    if (this.timerInterval) clearInterval(this.timerInterval);

    this.timerInterval = setInterval(() => {
      this.elapsedSeconds++;

      if (this.totalTimerSeconds > 0) {
        // Countdown mode
        this.remainingSeconds--;
        if (this.remainingSeconds <= 0) {
          this.remainingSeconds = 0;
          this.handleTimeUp();
        }
      }
      this.updateTimerDisplay();
    }, 1000);

    this.updateTimerDisplay();
  }

  stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
    this.isTimerRunning = false;
  }

  handleTimeUp() {
    this.stopTimer();
    this.isTimeUp = true;

    const cardEl = document.getElementById('dokkai-reading-card');
    if (cardEl) {
      cardEl.classList.add('animate-shake');
      setTimeout(() => cardEl.classList.remove('animate-shake'), 700);
    }

    if (this.app && typeof this.app.showToast === 'function') {
      this.app.showToast('⚠️ Đã hết thời gian đọc tiêu chuẩn! Vui lòng chốt ngay đáp án.', 'warning');
    }

    this.updateTimerDisplay();
  }

  formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }

  updateTimerDisplay() {
    const timerDisplayEl = document.getElementById('dokkai-timer-display');
    const timerProgressEl = document.getElementById('dokkai-timer-progress');
    const dockStatusBadgeEl = document.getElementById('dokkai-dock-status-badge');

    if (timerDisplayEl) {
      if (this.totalTimerSeconds > 0) {
        timerDisplayEl.textContent = this.formatTime(this.remainingSeconds);

        if (this.remainingSeconds <= 30 && !this.isTimeUp && this.isTimerRunning) {
          timerDisplayEl.className = 'font-mono text-3xl sm:text-4xl font-black tracking-wider py-2.5 rounded-2xl transition-all text-rose-600 bg-rose-50 border-2 border-rose-300 animate-pulse';
        } else if (this.isTimeUp) {
          timerDisplayEl.className = 'font-mono text-3xl sm:text-4xl font-black tracking-wider py-2.5 rounded-2xl transition-all text-rose-600 bg-rose-50 border-2 border-rose-300';
        } else {
          timerDisplayEl.className = 'font-mono text-3xl sm:text-4xl font-black tracking-wider py-2.5 rounded-2xl transition-all text-slate-900 bg-slate-50 border border-slate-200/80';
        }

        if (timerProgressEl) {
          const pct = Math.max(0, Math.min(100, (this.remainingSeconds / this.totalTimerSeconds) * 100));
          timerProgressEl.style.width = `${pct}%`;
          if (this.remainingSeconds <= 30) {
            timerProgressEl.className = 'h-full transition-all duration-300 rounded-full bg-rose-500';
          } else {
            timerProgressEl.className = 'h-full transition-all duration-300 rounded-full bg-gradient-to-r from-emerald-500 to-indigo-600';
          }
        }
      } else {
        // Unlimited
        timerDisplayEl.textContent = `☕ ${this.formatTime(this.elapsedSeconds)}`;
        timerDisplayEl.className = 'font-mono text-3xl sm:text-4xl font-black tracking-wider py-2.5 rounded-2xl transition-all text-amber-700 bg-amber-50/80 border border-amber-200';
        if (timerProgressEl) {
          timerProgressEl.style.width = '100%';
          timerProgressEl.className = 'h-full transition-all duration-300 rounded-full bg-amber-500';
        }
      }
    }

    if (dockStatusBadgeEl) {
      if (!this.isStarted) {
        dockStatusBadgeEl.textContent = '⏸️ Chưa bắt đầu';
        dockStatusBadgeEl.className = 'text-[10px] font-bold px-2 py-0.5 rounded-full border bg-slate-100 text-slate-500 border-slate-200';
      } else if (this.step === 2) {
        dockStatusBadgeEl.textContent = '✓ Đã hoàn thành';
        dockStatusBadgeEl.className = 'text-[10px] font-bold px-2 py-0.5 rounded-full border bg-emerald-50 text-emerald-700 border-emerald-200';
      } else if (this.isTimeUp) {
        dockStatusBadgeEl.textContent = '⚠️ Hết giờ';
        dockStatusBadgeEl.className = 'text-[10px] font-bold px-2 py-0.5 rounded-full border bg-rose-50 text-rose-700 border-rose-200 animate-pulse';
      } else if (this.isTimerRunning) {
        dockStatusBadgeEl.textContent = '⚡ Đang đếm giờ';
        dockStatusBadgeEl.className = 'text-[10px] font-bold px-2 py-0.5 rounded-full border bg-emerald-50 text-emerald-700 border-emerald-200';
      } else {
        dockStatusBadgeEl.textContent = '⏸️ Tạm dừng';
        dockStatusBadgeEl.className = 'text-[10px] font-bold px-2 py-0.5 rounded-full border bg-slate-100 text-slate-600 border-slate-200';
      }
    }
  }

  // ==============================================================
  // STEP 2: LOGIC HIGHLIGHTING & N1 VOCABULARY TOOLTIPS PROCESSOR
  // ==============================================================

  escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /**
   * Safely replaces target word outside HTML tags to avoid corrupting attributes
   */
  replaceWordOutsideTags(html, word, replacementHtml) {
    if (!html || !word) return html;
    const parts = html.split(/(<[^>]+>)/g);
    for (let i = 0; i < parts.length; i++) {
      if (i % 2 === 0) {
        // Text outside tags
        parts[i] = parts[i].split(word).join(replacementHtml);
      }
    }
    return parts.join('');
  }

  buildHighlightedPassage(passage, logicHighlights = {}, vocabulary = []) {
    if (!passage) return '';
    if (this.step !== 2) {
      // Step 1: Clean, unhighlighted text (pure reading practice)
      return passage
        .split('\n\n')
        .map(para => `<p class="mb-5 last:mb-0">${this.escapeHtml(para)}</p>`)
        .join('');
    }

    // Step 2: Full logic highlights + N1 Vocabulary tooltips
    let text = passage;
    const { counterPremise, turningPoint, authorConclusion } = logicHighlights;

    const tokenBlue = '___DOKKAI_HL_BLUE___';
    const tokenYellow = '___DOKKAI_HL_YELLOW___';
    const tokenRed = '___DOKKAI_HL_RED___';

    let replacedBlue = '';
    let replacedYellow = '';
    let replacedRed = '';

    if (counterPremise && text.includes(counterPremise)) {
      replacedBlue = `
        <mark class="dokkai-hl-blue" title="Tiền đề / Quan niệm số đông (一般論・前提)">
          <span class="dokkai-tag bg-blue-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded mr-1.5 select-none shadow-2xs">🔵 Tiền đề số đông</span>${this.escapeHtml(counterPremise)}
        </mark>
      `;
      text = text.replace(counterPremise, tokenBlue);
    }

    if (turningPoint && text.includes(turningPoint)) {
      replacedYellow = `
        <mark class="dokkai-hl-yellow" title="Từ nối lật ngược vấn đề (逆接の転換)">
          <span class="dokkai-tag bg-amber-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded mr-1.5 select-none shadow-2xs">🟡 Cú lật tư duy</span>${this.escapeHtml(turningPoint)}
        </mark>
      `;
      text = text.replace(turningPoint, tokenYellow);
    }

    if (authorConclusion && text.includes(authorConclusion)) {
      replacedRed = `
        <mark class="dokkai-hl-red" title="Quan điểm cốt lõi của tác giả (筆者の主張・結論)">
          <span class="dokkai-tag bg-rose-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded mr-1.5 select-none shadow-2xs">🔴 Câu chốt tác giả</span>${this.escapeHtml(authorConclusion)}
        </mark>
      `;
      text = text.replace(authorConclusion, tokenRed);
    }

    let paragraphs = text.split('\n\n').map(p => this.escapeHtml(p));
    let combined = paragraphs.map(para => `<p class="mb-5 last:mb-0">${para}</p>`).join('');

    if (replacedBlue) combined = combined.replace(tokenBlue, replacedBlue);
    if (replacedYellow) combined = combined.replace(tokenYellow, replacedYellow);
    if (replacedRed) combined = combined.replace(tokenRed, replacedRed);

    // Inject Vocabulary Tooltip Spans (Sorted by length descending)
    if (Array.isArray(vocabulary) && vocabulary.length > 0) {
      const sortedVocab = [...vocabulary].sort((a, b) => (b.word?.length || 0) - (a.word?.length || 0));
      for (const item of sortedVocab) {
        if (!item.word) continue;
        const isSaved = this.savedVocab.has(item.word);
        const vocabSpan = `<span class="dokkai-vocab-word cursor-pointer border-b-2 border-dashed border-indigo-400 hover:border-indigo-600 hover:bg-indigo-50/80 transition-colors font-medium rounded-xs px-0.5 ${isSaved ? 'bg-amber-50 border-amber-400 font-bold' : ''}" data-word="${this.escapeHtml(item.word)}" data-reading="${this.escapeHtml(item.reading || '')}" data-hanviet="${this.escapeHtml(item.hanviet || '')}" data-meaning="${this.escapeHtml(item.meaning || '')}" title="Nhấn để xem chú thích & lưu Anki">${this.escapeHtml(item.word)}</span>`;
        combined = this.replaceWordOutsideTags(combined, item.word, vocabSpan);
      }
    }

    return combined;
  }

  // ==============================================================
  // ACCURATE ANSWER EVALUATION (FIX 1-BASED INDEX BUG)
  // ==============================================================

  getCorrectAnswerNumber(q) {
    if (!q) return 1;
    if (typeof q.answer === 'number' && q.answer >= 1 && q.answer <= 4) {
      return q.answer;
    }
    const parsed = parseInt(q.answer, 10);
    if (!isNaN(parsed) && parsed >= 1 && parsed <= 4) {
      return parsed;
    }
    if (q.trapBreakdown) {
      for (let i = 1; i <= 4; i++) {
        const text = q.trapBreakdown[`opt${i}`] || '';
        if (text.includes('ĐÁP ÁN ĐÚNG') || text.includes('Đáp án đúng')) {
          return i;
        }
      }
    }
    return 1;
  }

  isAnswerCorrect(userChoiceIdx, q) {
    if (userChoiceIdx === null || userChoiceIdx === undefined) return false;
    const correctNum = this.getCorrectAnswerNumber(q);
    return (userChoiceIdx + 1) === correctNum;
  }

  // ==============================================================
  // USER ACTIONS
  // ==============================================================

  selectOption(optIdx) {
    if (this.step === 2) return;
    if (!this.isStarted) {
      this.startReading();
    }
    this.selectedOption = optIdx;
    this.render();
  }

  submitAnswer() {
    if (this.selectedOption === null) {
      if (this.app && typeof this.app.showToast === 'function') {
        this.app.showToast('Vui lòng chọn 1 phương án trước khi chốt đáp án!', 'info');
      }
      return;
    }

    this.stopTimer();
    this.step = 2;

    const q = this.getCurrentQuestion();
    const isCorrect = this.isAnswerCorrect(this.selectedOption, q);

    this.userAnswersHistory[q.id] = {
      selectedOption: this.selectedOption,
      isCorrect,
      timeSpent: this.elapsedSeconds
    };

    this.render();

    // Scroll smoothly to the trap breakdown analysis
    setTimeout(() => {
      const breakdownEl = document.getElementById('dokkai-breakdown-section');
      if (breakdownEl) {
        breakdownEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  }

  goToQuestion(index) {
    if (index < 0 || index >= this.questions.length) return;
    this.currentIndex = index;
    const q = this.getCurrentQuestion();
    if (q && this.userAnswersHistory[q.id]) {
      const hist = this.userAnswersHistory[q.id];
      this.step = 2;
      this.isStarted = true;
      this.selectedOption = hist.selectedOption;
      this.elapsedSeconds = hist.timeSpent || 0;
      this.stopTimer();
    } else {
      this.resetQuestionState();
    }
    this.render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  retakeCurrentQuestion() {
    this.resetQuestionState();
    this.render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ==============================================================
  // ANKI VOCABULARY HARVEST ENGINE
  // ==============================================================

  toggleSaveVocab(item) {
    if (!item || !item.word) return;
    if (this.savedVocab.has(item.word)) {
      this.savedVocab.delete(item.word);
      if (this.app && typeof this.app.showToast === 'function') {
        this.app.showToast(`Đã bỏ lưu từ "${item.word}" khỏi danh sách Anki.`, 'info');
      }
    } else {
      this.savedVocab.set(item.word, item);
      if (this.app && typeof this.app.showToast === 'function') {
        this.app.showToast(`✨ Đã thêm "${item.word}" (${item.reading}) vào danh sách thẻ Anki!`, 'success');
      }
    }
    this.updateVocabHarvestCount();
    this.render();
  }

  updateVocabHarvestCount() {
    const badgeEl = document.getElementById('dokkai-vocab-harvest-badge');
    if (badgeEl) {
      badgeEl.textContent = `${this.savedVocab.size} từ`;
    }
  }

  saveSelectedTextToAnki(selectedText) {
    if (!selectedText || !selectedText.trim()) return;
    const cleanWord = selectedText.trim();
    const q = this.getCurrentQuestion();
    const item = {
      word: cleanWord,
      reading: '',
      hanviet: 'Tự do bôi đen',
      meaning: `Trích từ bài đọc: ${q ? q.title : ''}`
    };
    this.savedVocab.set(cleanWord, item);
    if (this.app && typeof this.app.showToast === 'function') {
      this.app.showToast(`✨ Đã lưu cụm từ "${cleanWord}" vào danh sách thẻ Anki!`, 'success');
    }
    this.updateVocabHarvestCount();
    this.render();
  }

  exportVocabToAnki() {
    if (this.savedVocab.size === 0) {
      // If none saved manually, offer to export all vocabulary of this chapter
      const q = this.getCurrentQuestion();
      if (q && Array.isArray(q.vocabulary) && q.vocabulary.length > 0) {
        q.vocabulary.forEach(v => this.savedVocab.set(v.word, v));
        if (this.app && typeof this.app.showToast === 'function') {
          this.app.showToast(`Đã tự động gom ${q.vocabulary.length} từ vựng N1 của bài đọc vào file xuất!`, 'info');
        }
      } else {
        if (this.app && typeof this.app.showToast === 'function') {
          this.app.showToast('Chưa có từ vựng nào được lưu. Hãy rê chuột vào các từ có gạch chân để lưu!', 'warning');
        }
        return;
      }
    }

    const q = this.getCurrentQuestion();
    let tsvRows = [];

    this.savedVocab.forEach((item) => {
      const front = `<b>【Từ vựng N1 Dokkai】</b><br><span style="font-size:26px; color:#4338ca; font-weight:bold;">${item.word}</span> ${item.reading ? `【${item.reading}】` : ''}`;
      const back = `<b>【Âm Hán Việt】:</b> ${item.hanviet || '--'}<br><b>【Ý nghĩa ngữ cảnh】:</b> ${item.meaning || '--'}<br><br><b>【Bài đọc trích đoạn】:</b> ${q ? q.title : 'Shin Kanzen Master N1'}`;
      const tags = `Koala_Dokkai_Vocab_N1 ${q ? q.chapter.replace(/[:：]/g, '_') : 'Ch01'}`;
      tsvRows.push(`${front}\t${back}\t${tags}`);
    });

    const tsvContent = tsvRows.join('\n') + '\n';
    const blob = new Blob([tsvContent], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Koala_Dokkai_Vocab_${(q && q.id) || 'Ch01'}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    if (this.app && typeof this.app.showToast === 'function') {
      this.app.showToast(`🎉 Đã xuất thành công file thẻ Anki (.txt) với ${tsvRows.length} từ vựng N1!`, 'success');
    }
  }

  // ==============================================================
  // RENDER MAIN 2-COLUMN WORKSPACE
  // ==============================================================

  render() {
    if (!this.containerEl) return;
    const q = this.getCurrentQuestion();
    if (!q) {
      this.containerEl.innerHTML = `
        <div class="py-16 text-center text-slate-500">
          <p class="font-bold text-base">Không tìm thấy bài đọc trong chương này.</p>
        </div>
      `;
      return;
    }

    const qType = q.mondaiType || 'short';
    const cfg = TIMER_CONFIGS[qType] || TIMER_CONFIGS.short;
    const typeLabel = cfg.name;
    const isAnswered = this.step === 2;
    const correctNum = this.getCorrectAnswerNumber(q);
    const isCorrect = isAnswered && this.isAnswerCorrect(this.selectedOption, q);

    this.containerEl.innerHTML = `
      <div class="dokkai-workspace max-w-7xl mx-auto px-3 sm:px-6 py-6 space-y-6 animate-fade-in font-sans">
        
        <!-- Chapter & Breadcrumb Header -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-200/80">
          <div>
            <div class="flex flex-wrap items-center gap-2 mb-1.5">
              <button type="button" id="btn-dokkai-back-home" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-xl text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 border border-slate-200/80 shadow-2xs hover:shadow-xs transition active:scale-95 cursor-pointer" title="Quay lại Trang Chủ">
                <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
                <span>Trang Chủ</span>
              </button>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-extrabold bg-indigo-50 text-indigo-700 border border-indigo-200">
                📖 Shin Kanzen Dokkai N1
              </span>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-50 text-amber-800 border border-amber-200">
                ${q.chapter || '第1章：対比・逆接'}
              </span>
              <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-slate-100 text-slate-600">
                ${typeLabel}
              </span>
            </div>
            <h1 class="text-lg sm:text-xl font-black text-slate-900 tracking-tight">
              ${q.title || `Bài đọc ${this.currentIndex + 1}`}
            </h1>
          </div>

          <!-- Pagination Bar -->
          <div class="flex items-center gap-1.5 self-start sm:self-center">
            <button type="button" id="btn-dokkai-prev" class="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer" ${this.currentIndex === 0 ? 'disabled' : ''} title="Bài trước">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
            </button>
            <div class="flex items-center gap-1">
              ${this.questions.map((item, idx) => `
                <button type="button" class="btn-dokkai-page w-7 h-7 rounded-xl text-xs font-bold transition flex items-center justify-center cursor-pointer ${
                  idx === this.currentIndex
                    ? 'bg-indigo-600 text-white shadow-xs'
                    : this.userAnswersHistory[item.id]
                      ? this.userAnswersHistory[item.id].isCorrect
                        ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                        : 'bg-rose-100 text-rose-800 border border-rose-300'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }" data-index="${idx}">
                  ${idx + 1}
                </button>
              `).join('')}
            </div>
            <button type="button" id="btn-dokkai-next" class="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer" ${this.currentIndex === this.questions.length - 1 ? 'disabled' : ''} title="Bài tiếp">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </button>
          </div>
        </div>

        <!-- 2-COLUMN WORKSPACE: LEFT (75%) & RIGHT STICKY DOCK (25%) -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

          <!-- LEFT COLUMN: Main Reading, Questions, and Step 2 Analysis (~75%) -->
          <div class="lg:col-span-8 xl:col-span-9 space-y-6">

            <!-- Result Banner in Step 2 -->
            ${isAnswered ? `
              <div class="rounded-2xl p-4 sm:p-5 border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-xs ${
                isCorrect ? 'bg-emerald-50/90 border-emerald-200 text-emerald-950' : 'bg-rose-50/90 border-rose-200 text-rose-950'
              }">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-2xl text-white font-black text-lg flex items-center justify-center shrink-0 shadow-xs ${
                    isCorrect ? 'bg-emerald-600' : 'bg-rose-600'
                  }">
                    ${isCorrect ? '✓' : '✗'}
                  </div>
                  <div>
                    <div class="text-sm font-black flex items-center gap-2">
                      <span>${isCorrect ? 'CHÍNH XÁC! TƯ DUY RẤT TỐT' : 'CHƯA CHÍNH XÁC (ĐÃ DÍNH BẪY TƯ DUY)'}</span>
                      <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full ${isCorrect ? 'bg-emerald-200 text-emerald-900' : 'bg-rose-200 text-rose-900'}">
                        ⏱️ Hoàn thành: ${this.formatTime(this.elapsedSeconds)}
                      </span>
                    </div>
                    <p class="text-xs mt-0.5 ${isCorrect ? 'text-emerald-800' : 'text-rose-800'}">
                      ${isCorrect 
                        ? 'Bạn đã bắt đúng câu chốt của tác giả và không bị quan niệm số đông đánh lừa.' 
                        : 'Hãy xem văn bản bên dưới đã bật 3 màu điểm nhìn để mổ xẻ nguyên nhân sai.'}
                    </p>
                  </div>
                </div>

                <div class="flex items-center gap-2 shrink-0">
                  <button type="button" id="btn-dokkai-retake-top" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 transition flex items-center gap-1.5 shadow-2xs cursor-pointer active:scale-95">
                    <span>🔄 Làm lại</span>
                  </button>
                  ${this.currentIndex < this.questions.length - 1 ? `
                    <button type="button" id="btn-dokkai-next-top" class="px-4 py-1.5 rounded-xl text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white transition flex items-center gap-1.5 shadow-xs cursor-pointer active:scale-95">
                      <span>Bài tiếp theo ➡</span>
                    </button>
                  ` : ''}
                </div>
              </div>
            ` : ''}

            <!-- PASSAGE & QUESTIONS WRAPPER WITH PRE-START BLUR LOCK -->
            <div class="dokkai-reading-and-question-wrapper relative rounded-3xl ${!this.isStarted && this.step === 1 ? 'max-h-[500px] overflow-hidden' : ''}">
              
              <!-- PRE-START BLUR OVERLAY MODAL -->
              ${!this.isStarted && this.step === 1 ? `
                <div class="absolute inset-0 z-30 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-md rounded-3xl">
                  <div class="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 max-w-md w-full text-center shadow-2xl space-y-4 animate-scale-up">
                    <div class="w-13 h-13 mx-auto rounded-2xl bg-gradient-to-tr from-amber-500 via-amber-600 to-indigo-600 text-white flex items-center justify-center text-2xl shadow-lg shadow-amber-400/25">
                      🔒
                    </div>
                    <div>
                      <h3 class="text-base sm:text-lg font-black text-slate-900 tracking-tight">
                        BÀI ĐỌC ĐANG ĐƯỢC KHÓA (CHỐNG LỘ ĐỀ)
                      </h3>
                      <p class="text-xs text-slate-500 mt-1 leading-relaxed">
                        Để đảm bảo phản xạ và áp lực phòng thi thật, nội dung bài đọc và câu hỏi sẽ mở ngay khi bạn bấm Bắt đầu.
                      </p>
                    </div>

                    <!-- Mode selection inside pre-start card -->
                    <div class="bg-slate-50 rounded-2xl p-2.5 border border-slate-200 text-left space-y-1.5">
                      <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Thời gian làm bài:</div>
                      <div class="grid grid-cols-3 gap-1">
                        <button type="button" class="btn-dokkai-modal-mode p-1.5 rounded-xl text-xs font-bold transition flex flex-col items-center justify-center cursor-pointer ${this.timerMode === 'standard' ? 'bg-emerald-600 text-white shadow-xs' : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200'}" data-mode="standard">
                          <span>🟢 Chuẩn</span>
                          <span class="text-[9px] font-normal opacity-90">${cfg.standard.label}</span>
                        </button>
                        <button type="button" class="btn-dokkai-modal-mode p-1.5 rounded-xl text-xs font-bold transition flex flex-col items-center justify-center cursor-pointer ${this.timerMode === 'hardcore' ? 'bg-rose-600 text-white shadow-xs' : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200'}" data-mode="hardcore">
                          <span>🔥 Gắt</span>
                          <span class="text-[9px] font-normal opacity-90">${cfg.hardcore.label}</span>
                        </button>
                        <button type="button" class="btn-dokkai-modal-mode p-1.5 rounded-xl text-xs font-bold transition flex flex-col items-center justify-center cursor-pointer ${this.timerMode === 'unlimited' ? 'bg-amber-600 text-white shadow-xs' : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200'}" data-mode="unlimited">
                          <span>☕ Tự do</span>
                          <span class="text-[9px] font-normal opacity-90">Vô hạn</span>
                        </button>
                      </div>
                    </div>

                    <!-- Big Start Button -->
                    <button type="button" id="btn-dokkai-start-reading-modal" class="w-full py-3.5 px-6 rounded-2xl bg-gradient-to-r from-amber-500 via-amber-600 to-indigo-600 hover:from-amber-600 hover:to-indigo-700 active:scale-98 text-white font-black text-sm shadow-xl shadow-amber-300/40 transition flex items-center justify-center gap-2 cursor-pointer">
                      <span>🚀 BẮT ĐẦU ĐỌC & BẤM GIỜ</span>
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                    </button>
                  </div>
                </div>
              ` : ''}

              <!-- BLURRED INNER CONTENT (Locked when !isStarted) -->
              <div class="space-y-6 ${!this.isStarted && this.step === 1 ? 'filter blur-md select-none pointer-events-none opacity-25' : ''}">
                
                <!-- Reading Passage Card -->
                <div id="dokkai-reading-card" class="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-9 shadow-sm transition-card relative">
                  
                  <!-- Card Header: Cleaned Meta Info (Requirement 4: No redundant font text) -->
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 mb-5 border-b border-slate-100">
                    <div class="flex items-center gap-2">
                      <span class="w-8 h-8 rounded-xl bg-slate-100 text-slate-700 flex items-center justify-center font-bold text-xs">
                        📄
                      </span>
                      <div>
                        <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Văn bản bài đọc gốc</h2>
                      </div>
                    </div>

                    <!-- Legend & Vocab Hint (Step 2 Only) -->
                    ${this.step === 2 ? `
                      <div class="flex flex-wrap items-center gap-1.5 text-[11px] font-bold">
                        <span class="px-2 py-0.5 rounded-md bg-blue-50 text-blue-800 border border-blue-200">
                          🔵 Tiền đề số đông
                        </span>
                        <span class="px-2 py-0.5 rounded-md bg-amber-50 text-amber-800 border border-amber-200">
                          🟡 Cú lật tư duy
                        </span>
                        <span class="px-2 py-0.5 rounded-md bg-rose-50 text-rose-800 border border-rose-200">
                          🔴 Câu chốt tác giả
                        </span>
                        <span class="px-2 py-0.5 rounded-md bg-indigo-50 text-indigo-700 border border-indigo-200 flex items-center gap-1">
                          <span class="w-1.5 h-1.5 rounded-full bg-indigo-500"></span>
                          <span>Gạch chân nét đứt: Chú thích N1</span>
                        </span>
                      </div>
                    ` : `
                      <div class="text-[11px] font-semibold text-slate-400 flex items-center gap-1">
                        <span>${this.isStarted ? '⚡ Bước 1: Đọc tự lực & tư duy độc lập' : '🛡️ Bài đọc được che mờ chống lộ đề'}</span>
                      </div>
                    `}
                  </div>

                  <!-- Passage Content (with N1 Vocab Tooltips in Step 2) -->
                  <div id="dokkai-passage-container" class="dokkai-passage-text font-jp text-slate-800 text-base sm:text-[17px] leading-[2.3] tracking-wide select-text relative">
                    ${this.buildHighlightedPassage(q.passage, q.logicHighlights, q.vocabulary)}
                  </div>

                  <!-- Step 2 Floating Selection Toolbar -->
                  ${this.step === 2 ? `
                    <div id="dokkai-selection-toolbar" class="hidden mt-3 p-2.5 rounded-xl bg-indigo-900/90 text-white text-xs flex items-center justify-between gap-2 shadow-lg animate-fade-in">
                      <div class="flex items-center gap-2 truncate">
                        <span>✂️</span>
                        <span class="truncate">Đã bôi đen: <b id="dokkai-selection-text" class="text-amber-300"></b></span>
                      </div>
                      <button type="button" id="btn-save-selected-to-anki" class="px-3 py-1 rounded-lg bg-amber-500 hover:bg-amber-600 text-slate-900 font-bold text-xs shrink-0 cursor-pointer shadow-xs active:scale-95">
                        ⚡ Thêm vào Anki
                      </button>
                    </div>
                  ` : ''}

                </div>

                <!-- Question & 4 Options Card -->
                <div id="dokkai-question-card" class="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm space-y-6">
                  
                  <!-- Question Title -->
                  <div class="space-y-1">
                    <div class="text-xs font-bold text-indigo-700 uppercase tracking-wider flex items-center gap-1.5">
                      <span>❓ CÂU HỎI ĐỌC HIỂU</span>
                    </div>
                    <h3 class="font-jp text-base sm:text-lg font-bold text-slate-900 leading-snug">
                      ${this.escapeHtml(q.question)}
                    </h3>
                  </div>

                  <!-- Options Stack -->
                  <div class="options-stack space-y-3">
                    ${(q.options || []).map((opt, optIdx) => {
                      const isSelected = this.selectedOption === optIdx;
                      // FIX REQUIREMENT 3: Only exact match (optIdx + 1) === correctNum gets isThisCorrect = true
                      const isThisCorrect = isAnswered && ((optIdx + 1) === correctNum);
                      const isSelectedAndWrong = isAnswered && isSelected && !isThisCorrect;

                      let optionStyle = 'border-slate-200 bg-white hover:border-indigo-300 hover:bg-slate-50/70 text-slate-800 cursor-pointer';
                      let badgeStyle = 'bg-slate-100 text-slate-600 border-slate-200';

                      if (this.step === 1) {
                        if (isSelected) {
                          optionStyle = 'border-indigo-600 bg-indigo-50/70 text-indigo-950 ring-2 ring-indigo-500/20 shadow-xs font-semibold cursor-pointer';
                          badgeStyle = 'bg-indigo-600 text-white border-indigo-600 shadow-xs';
                        }
                      } else {
                        // Step 2
                        if (isThisCorrect) {
                          optionStyle = 'border-emerald-500 bg-emerald-50/80 text-emerald-950 font-bold ring-2 ring-emerald-500/20';
                          badgeStyle = 'bg-emerald-600 text-white border-emerald-600';
                        } else if (isSelectedAndWrong) {
                          optionStyle = 'border-rose-400 bg-rose-50/70 text-rose-950 ring-2 ring-rose-400/20';
                          badgeStyle = 'bg-rose-600 text-white border-rose-600';
                        } else {
                          optionStyle = 'border-slate-200 bg-slate-50/40 text-slate-500 opacity-80';
                          badgeStyle = 'bg-slate-100 text-slate-400 border-slate-200';
                        }
                      }

                      return `
                        <button type="button" class="btn-dokkai-option w-full text-left p-4 sm:p-5 rounded-2xl border-2 transition-all flex items-start gap-3.5 group ${optionStyle}" data-opt-idx="${optIdx}" ${this.step === 2 ? 'disabled' : ''}>
                          <div class="w-7 h-7 rounded-xl font-black text-xs flex items-center justify-center shrink-0 border mt-0.5 transition ${badgeStyle}">
                            ${optIdx + 1}
                          </div>
                          <div class="flex-1 font-jp text-sm sm:text-base leading-relaxed">
                            ${this.escapeHtml(opt)}
                          </div>
                          ${isSelected ? `
                            <div class="shrink-0 text-xs font-bold px-2 py-0.5 rounded-full ${
                              this.step === 1 ? 'bg-indigo-600 text-white' : isThisCorrect ? 'bg-emerald-600 text-white' : 'bg-rose-600 text-white'
                            }">
                              ${this.step === 1 ? 'Đã chọn' : isThisCorrect ? '✓ Bạn chọn' : '✗ Bạn chọn'}
                            </div>
                          ` : isThisCorrect ? `
                            <div class="shrink-0 text-xs font-bold px-2 py-0.5 rounded-full bg-emerald-600 text-white">
                              ✓ Đáp án đúng
                            </div>
                          ` : ''}
                        </button>
                      `;
                    }).join('')}
                  </div>

                  <!-- Step 1 Bottom Action Bar -->
                  ${this.step === 1 ? `
                    <div class="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3">
                      <div class="text-xs text-slate-500">
                        ${this.selectedOption !== null 
                          ? `<span class="font-bold text-indigo-700">Đã chọn lựa chọn ${this.selectedOption + 1}.</span> Nhấn nút bên cạnh hoặc ở khung bên phải để chốt đáp án & mở khóa mổ xẻ.`
                          : 'Hãy đọc kỹ văn bản, chọn 1 phương án để mở khóa phân tích.'}
                      </div>

                      <button type="button" id="btn-dokkai-submit" class="w-full sm:w-auto px-7 py-3.5 rounded-xl font-bold text-xs shadow-md transition flex items-center justify-center gap-2 ${
                        this.selectedOption !== null
                          ? 'bg-gradient-to-r from-indigo-600 to-indigo-800 hover:from-indigo-700 hover:to-indigo-900 text-white shadow-indigo-200 cursor-pointer active:scale-95'
                          : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                      }" ${this.selectedOption === null ? 'disabled' : ''}>
                        <span>🎯 Chốt đáp án & Xem phân tích logic</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                      </button>
                    </div>
                  ` : ''}

                </div>

              </div>
            </div>

            <!-- STEP 2: TRAP BREAKDOWN & EXPLANATION (Mổ xẻ logic & Bắt bẫy) -->
            ${this.step === 2 ? `
              <div id="dokkai-breakdown-section" class="space-y-6 animate-fade-in">
                
                <!-- Trap Breakdown Container -->
                <div class="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm space-y-4">
                  <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                    <div class="flex items-center gap-2">
                      <span class="w-8 h-8 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold text-xs shadow-xs">
                        ⚡
                      </span>
                      <div>
                        <h3 class="text-sm font-black text-slate-900">Bắt Bẫy Tư Duy (Trap Breakdown)</h3>
                        <p class="text-[11px] text-slate-500 font-medium">Phân tích chi tiết từng phương án theo phương pháp Shin Kanzen</p>
                      </div>
                    </div>
                    <span class="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700">
                      Chương 1: 対比・逆接
                    </span>
                  </div>

                  <div class="grid grid-cols-1 gap-3.5 pt-2">
                    ${[1, 2, 3, 4].map(num => {
                      const optKey = `opt${num}`;
                      const trapText = (q.trapBreakdown && q.trapBreakdown[optKey]) || '';
                      // FIX REQUIREMENT 3: Strictly single correct answer badge
                      const isThisCorrect = (num === correctNum);
                      const isUserPick = (this.selectedOption === (num - 1));

                      return `
                        <div class="p-4 rounded-2xl border-2 transition ${
                          isThisCorrect
                            ? 'border-emerald-300 bg-emerald-50/40 text-emerald-950'
                            : isUserPick
                              ? 'border-rose-300 bg-rose-50/50 text-rose-950'
                              : 'border-slate-200 bg-slate-50/60 text-slate-700'
                        }">
                          <div class="flex flex-wrap items-center justify-between gap-2 mb-1.5">
                            <div class="flex items-center gap-2">
                              <span class="w-6 h-6 rounded-lg font-black text-xs flex items-center justify-center ${
                                isThisCorrect ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-700'
                              }">
                                ${num}
                              </span>
                              <span class="text-xs font-bold ${isThisCorrect ? 'text-emerald-900' : 'text-slate-800'}">
                                Lựa chọn ${num}
                              </span>
                            </div>

                            <div class="flex items-center gap-1.5">
                              ${isUserPick ? `
                                <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${
                                  isThisCorrect ? 'bg-emerald-600 text-white' : 'bg-rose-600 text-white'
                                }">
                                  ${isThisCorrect ? '✓ Bạn đã chọn đúng' : '✗ Lựa chọn của bạn'}
                                </span>
                              ` : ''}
                              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${
                                isThisCorrect ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' : 'bg-rose-100 text-rose-800 border border-rose-300'
                              }">
                                ${isThisCorrect ? '✓ ĐÁP ÁN ĐÚNG' : '❌ BẪY TƯ DUY'}
                              </span>
                            </div>
                          </div>

                          <p class="text-xs sm:text-[13px] leading-relaxed mt-2 ${
                            isThisCorrect ? 'text-emerald-900 font-medium' : 'text-slate-700'
                          }">
                            ${this.escapeHtml(trapText)}
                          </p>
                        </div>
                      `;
                    }).join('')}
                  </div>
                </div>

                <!-- Full Translation & Overall Explanation -->
                <div class="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm space-y-4">
                  <div class="flex items-center gap-2 pb-3 border-b border-slate-100">
                    <span class="w-8 h-8 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-bold text-xs shadow-xs">
                      📖
                    </span>
                    <div>
                      <h3 class="text-sm font-black text-slate-900">Bản Dịch Nghĩa & Phân Tích Chiến Lược</h3>
                      <p class="text-[11px] text-slate-500 font-medium">Bản dịch tiếng Việt tự nhiên và phương pháp tư duy đọc hiểu N1</p>
                    </div>
                  </div>

                  <div class="explanation-box text-xs sm:text-sm text-slate-700 leading-loose space-y-3 font-sans">
                    ${q.explanation || 'Đang cập nhật lời giải chi tiết.'}
                  </div>
                </div>

                <!-- Bottom Action Controls -->
                <div class="p-4 bg-slate-50/90 rounded-2xl border border-slate-200/80 flex flex-wrap items-center justify-between gap-3 shadow-2xs">
                  <div class="flex items-center gap-2">
                    <button type="button" id="btn-dokkai-retake-bottom" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 transition shadow-2xs flex items-center gap-1.5 cursor-pointer active:scale-95">
                      <span>🔄 Đọc lại bài này</span>
                    </button>
                    <button type="button" id="btn-dokkai-anki-export" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-white hover:bg-amber-50 text-amber-800 border border-amber-200 transition shadow-2xs flex items-center gap-1.5 cursor-pointer active:scale-95" title="Tải file text nạp câu hỏi vào Anki">
                      <span>⚡ Xuất bài đọc Anki</span>
                    </button>
                    <button type="button" id="btn-dokkai-export-vocab-bottom" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 transition shadow-2xs flex items-center gap-1.5 cursor-pointer active:scale-95" title="Tải toàn bộ từ vựng đã lưu vào Anki">
                      <span>📚 Xuất từ vựng Anki (.txt)</span>
                    </button>
                  </div>

                  <div class="flex items-center gap-2">
                    ${this.currentIndex < this.questions.length - 1 ? `
                      <button type="button" id="btn-dokkai-next-bottom" class="px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-indigo-600 to-indigo-800 hover:from-indigo-700 hover:to-indigo-900 text-white shadow-md shadow-indigo-200 transition flex items-center gap-1.5 cursor-pointer active:scale-95">
                        <span>Bài tiếp theo (Bài ${this.currentIndex + 2}) ➡</span>
                      </button>
                    ` : `
                      <button type="button" id="btn-dokkai-finish-chapter" class="px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-md shadow-emerald-200 transition flex items-center gap-1.5 cursor-pointer active:scale-95">
                        <span>🎉 Hoàn thành Chương 1!</span>
                      </button>
                    `}
                  </div>
                </div>

              </div>
            ` : ''}

          </div>

          <!-- RIGHT COLUMN: STICKY TIMER DOCK WIDGET (~25% width, position: sticky; top: 24px) -->
          <div class="lg:col-span-4 xl:col-span-3 lg:sticky lg:top-6 z-10 space-y-4">
            
            <div class="dokkai-sticky-dock bg-white/95 backdrop-blur-md rounded-3xl border border-slate-200/90 p-5 shadow-sm space-y-4">
              
              <!-- Dock Header -->
              <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                <div class="flex items-center gap-1.5 text-xs font-black text-slate-900">
                  <svg class="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  <span>ĐỒNG HỒ PHÒNG THI</span>
                </div>
                
                <span id="dokkai-dock-status-badge" class="text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                  !this.isStarted 
                    ? 'bg-slate-100 text-slate-500 border-slate-200'
                    : this.step === 2
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      : this.isTimeUp
                        ? 'bg-rose-50 text-rose-700 border-rose-200 animate-pulse'
                        : this.isTimerRunning
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : 'bg-slate-100 text-slate-600 border-slate-200'
                }">
                  ${
                    !this.isStarted 
                      ? '⏸️ Chưa bắt đầu' 
                      : this.step === 2 
                        ? '✓ Đã nộp bài' 
                        : this.isTimeUp 
                          ? '⚠️ Hết giờ' 
                          : this.isTimerRunning 
                            ? '⚡ Đang đếm giờ' 
                            : '⏸️ Tạm dừng'
                  }
                </span>
              </div>

              <!-- Giant Countdown Timer Display (Requirement 2) -->
              <div class="text-center py-1">
                <div id="dokkai-timer-display" class="font-mono text-3xl sm:text-4xl font-black tracking-wider py-2.5 rounded-2xl transition-all ${
                  this.totalTimerSeconds > 0 && this.remainingSeconds <= 30 && this.isTimerRunning && !this.isTimeUp
                    ? 'text-rose-600 bg-rose-50 border-2 border-rose-300 animate-pulse'
                    : this.isTimeUp
                      ? 'text-rose-600 bg-rose-50 border-2 border-rose-300'
                      : this.totalTimerSeconds === 0
                        ? 'text-amber-700 bg-amber-50/80 border border-amber-200'
                        : 'text-slate-900 bg-slate-50 border border-slate-200/80'
                }">
                  ${this.totalTimerSeconds > 0 ? this.formatTime(this.remainingSeconds) : `☕ ${this.formatTime(this.elapsedSeconds)}`}
                </div>

                <!-- Visual Progress Bar -->
                <div class="w-full bg-slate-100 rounded-full h-2 mt-3 overflow-hidden border border-slate-200/60">
                  <div id="dokkai-timer-progress" class="h-full transition-all duration-300 rounded-full ${
                    this.totalTimerSeconds > 0 && this.remainingSeconds <= 30
                      ? 'bg-rose-500'
                      : 'bg-gradient-to-r from-emerald-500 to-indigo-600'
                  }" style="width: ${
                    this.totalTimerSeconds > 0
                      ? Math.max(0, Math.min(100, (this.remainingSeconds / this.totalTimerSeconds) * 100))
                      : '100'
                  }%"></div>
                </div>
              </div>

              <!-- Mode Selector Buttons in Dock -->
              <div class="space-y-1.5 pt-1">
                <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Chế độ đếm giờ:</div>
                <div class="grid grid-cols-3 gap-1">
                  <button type="button" class="btn-dokkai-mode p-1.5 rounded-xl text-[11px] font-bold transition flex flex-col items-center justify-center cursor-pointer ${
                    this.timerMode === 'standard' ? 'bg-emerald-600 text-white shadow-xs' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }" data-mode="standard" ${this.isTimerRunning ? 'disabled' : ''} title="${cfg.standard.label}">
                    <span>🟢 Chuẩn</span>
                    <span class="text-[9px] font-normal opacity-90">${cfg.standard.label}</span>
                  </button>

                  <button type="button" class="btn-dokkai-mode p-1.5 rounded-xl text-[11px] font-bold transition flex flex-col items-center justify-center cursor-pointer ${
                    this.timerMode === 'hardcore' ? 'bg-rose-600 text-white shadow-xs' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }" data-mode="hardcore" ${this.isTimerRunning ? 'disabled' : ''} title="${cfg.hardcore.label}">
                    <span>🔥 Gắt</span>
                    <span class="text-[9px] font-normal opacity-90">${cfg.hardcore.label}</span>
                  </button>

                  <button type="button" class="btn-dokkai-mode p-1.5 rounded-xl text-[11px] font-bold transition flex flex-col items-center justify-center cursor-pointer ${
                    this.timerMode === 'unlimited' ? 'bg-amber-600 text-white shadow-xs' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }" data-mode="unlimited" ${this.isTimerRunning ? 'disabled' : ''} title="Không giới hạn thời gian">
                    <span>☕ Tự do</span>
                    <span class="text-[9px] font-normal opacity-90">Vô hạn</span>
                  </button>
                </div>
              </div>

              <!-- Dock Primary Action Button (Requirement 2: Sticky submit & progress) -->
              <div class="pt-2 border-t border-slate-100">
                ${
                  !this.isStarted
                    ? `
                      <button type="button" id="btn-dock-start-reading" class="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-amber-500 via-amber-600 to-indigo-600 hover:from-amber-600 hover:to-indigo-700 text-white font-black text-xs shadow-md shadow-amber-300/40 transition active:scale-95 cursor-pointer flex items-center justify-center gap-1.5">
                        <span>🚀 Bắt đầu bấm giờ</span>
                      </button>
                    `
                    : this.step === 1
                      ? `
                        <button type="button" id="btn-dock-submit-answer" class="w-full py-3 px-4 rounded-xl font-black text-xs shadow-md transition flex items-center justify-center gap-1.5 ${
                          this.selectedOption !== null
                            ? 'bg-gradient-to-r from-indigo-600 to-indigo-800 hover:from-indigo-700 hover:to-indigo-900 text-white shadow-indigo-300/50 cursor-pointer active:scale-95'
                            : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                        }" ${this.selectedOption === null ? 'disabled' : ''}>
                          <span>🎯 Chốt đáp án & Xem phân tích logic</span>
                        </button>
                        <div class="text-[10px] text-center text-slate-400 mt-1.5">
                          ${this.selectedOption !== null ? `Đã chọn lựa chọn ${this.selectedOption + 1}` : 'Vui lòng chọn 1 lựa chọn'}
                        </div>
                      `
                      : `
                        <div class="space-y-2">
                          ${this.currentIndex < this.questions.length - 1 ? `
                            <button type="button" id="btn-dock-next" class="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-800 hover:from-indigo-700 hover:to-indigo-900 text-white font-bold text-xs shadow-md transition flex items-center justify-center gap-1.5 cursor-pointer active:scale-95">
                              <span>Bài tiếp theo (Bài ${this.currentIndex + 2}) ➡</span>
                            </button>
                          ` : `
                            <button type="button" id="btn-dock-finish" class="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-700 text-white font-bold text-xs shadow-md transition flex items-center justify-center gap-1.5 cursor-pointer active:scale-95">
                              <span>🎉 Hoàn thành Chương!</span>
                            </button>
                          `}
                          <button type="button" id="btn-dock-retake" class="w-full py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs transition cursor-pointer flex items-center justify-center gap-1">
                            <span>🔄 Đọc lại bài này</span>
                          </button>
                        </div>
                      `
                }
              </div>

              <!-- Anki Vocab Harvest Status (Part 2) -->
              <div class="pt-3 border-t border-slate-100 space-y-2">
                <div class="flex items-center justify-between text-[11px]">
                  <span class="font-bold text-slate-600 flex items-center gap-1">
                    <span>⚡ Thu hoạch Anki:</span>
                  </span>
                  <span id="dokkai-vocab-harvest-badge" class="font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded-full border border-indigo-200">
                    ${this.savedVocab.size} từ đã lưu
                  </span>
                </div>
                <button type="button" id="btn-dock-export-vocab" class="w-full py-2 px-3 rounded-xl bg-slate-50 hover:bg-indigo-50 text-indigo-700 hover:text-indigo-900 border border-indigo-200 text-xs font-bold transition flex items-center justify-center gap-1.5 cursor-pointer">
                  <span>📥 Tải file nạp Anki (.txt)</span>
                </button>
              </div>

              <!-- Mini Question Navigator in Dock -->
              <div class="pt-3 border-t border-slate-100">
                <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Danh sách bài đọc:</div>
                <div class="grid grid-cols-4 gap-1.5">
                  ${this.questions.map((item, idx) => {
                    const hist = this.userAnswersHistory[item.id];
                    const isCurrent = idx === this.currentIndex;
                    return `
                      <button type="button" class="btn-dock-goto-page py-1.5 rounded-lg text-xs font-bold transition flex flex-col items-center justify-center cursor-pointer ${
                        isCurrent
                          ? 'bg-indigo-600 text-white shadow-xs'
                          : hist
                            ? hist.isCorrect
                              ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                              : 'bg-rose-100 text-rose-800 border border-rose-300'
                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                      }" data-index="${idx}">
                        <span>${idx + 1}</span>
                        <span class="text-[8px] font-normal leading-none mt-0.5">
                          ${isCurrent ? 'Đang đọc' : hist ? (hist.isCorrect ? '✓ Đúng' : '✗ Sai') : 'Chưa làm'}
                        </span>
                      </button>
                    `;
                  }).join('')}
                </div>
              </div>

            </div>

          </div>

        </div>

        <!-- Floating Tooltip Container for N1 Vocab (Part 2) -->
        <div id="dokkai-vocab-tooltip-box" class="hidden fixed z-50 p-3.5 bg-slate-900/95 backdrop-blur-md text-white rounded-2xl shadow-2xl border border-slate-700/80 max-w-xs space-y-2 text-xs transition-opacity pointer-events-auto">
          <!-- Populated dynamically on hover / tap -->
        </div>

      </div>
    `;

    this.bindEvents();
    this.updateTimerDisplay();
  }

  // ==============================================================
  // EVENT BINDINGS
  // ==============================================================

  bindEvents() {
    // Modal Start Button
    document.getElementById('btn-dokkai-start-reading-modal')?.addEventListener('click', () => {
      this.startReading();
    });

    // Dock Start Button
    document.getElementById('btn-dock-start-reading')?.addEventListener('click', () => {
      this.startReading();
    });

    // Option cards click
    const optButtons = this.containerEl.querySelectorAll('.btn-dokkai-option');
    optButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.getAttribute('data-opt-idx'), 10);
        this.selectOption(idx);
      });
    });

    // Submit buttons (in Left Column & in Right Dock)
    document.getElementById('btn-dokkai-submit')?.addEventListener('click', () => this.submitAnswer());
    document.getElementById('btn-dock-submit-answer')?.addEventListener('click', () => this.submitAnswer());

    // Dock Next & Retake & Finish buttons
    document.getElementById('btn-dock-next')?.addEventListener('click', () => this.goToQuestion(this.currentIndex + 1));
    document.getElementById('btn-dock-retake')?.addEventListener('click', () => this.retakeCurrentQuestion());
    document.getElementById('btn-dock-finish')?.addEventListener('click', () => {
      this.stopTimer();
      if (this.app && typeof this.app.showToast === 'function') {
        this.app.showToast('🎉 Chúc mừng bạn đã hoàn thành trọn vẹn Chương 1: 対比・逆接!', 'success');
      }
      setTimeout(() => {
        if (this.app && typeof this.app.switchView === 'function') {
          this.app.switchView('HOME');
        }
      }, 1000);
    });

    // Dock Mini Navigator
    const dockNavButtons = this.containerEl.querySelectorAll('.btn-dock-goto-page');
    dockNavButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.getAttribute('data-index'), 10);
        this.goToQuestion(idx);
      });
    });

    // Pagination buttons (Top)
    document.getElementById('btn-dokkai-prev')?.addEventListener('click', () => this.goToQuestion(this.currentIndex - 1));
    document.getElementById('btn-dokkai-next')?.addEventListener('click', () => this.goToQuestion(this.currentIndex + 1));

    const pageButtons = this.containerEl.querySelectorAll('.btn-dokkai-page');
    pageButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.getAttribute('data-index'), 10);
        this.goToQuestion(idx);
      });
    });

    // Back to Home button
    document.getElementById('btn-dokkai-back-home')?.addEventListener('click', () => {
      this.stopTimer();
      if (this.app && typeof this.app.switchView === 'function') {
        this.app.switchView('HOME');
      }
    });

    // Retake buttons
    document.getElementById('btn-dokkai-retake-top')?.addEventListener('click', () => this.retakeCurrentQuestion());
    document.getElementById('btn-dokkai-retake-bottom')?.addEventListener('click', () => this.retakeCurrentQuestion());

    // Next question buttons in Step 2
    document.getElementById('btn-dokkai-next-top')?.addEventListener('click', () => this.goToQuestion(this.currentIndex + 1));
    document.getElementById('btn-dokkai-next-bottom')?.addEventListener('click', () => this.goToQuestion(this.currentIndex + 1));

    // Finish chapter button
    document.getElementById('btn-dokkai-finish-chapter')?.addEventListener('click', () => {
      this.stopTimer();
      if (this.app && typeof this.app.showToast === 'function') {
        this.app.showToast('🎉 Chúc mừng bạn đã hoàn thành trọn vẹn Chương 1: 対比・逆接!', 'success');
      }
      setTimeout(() => {
        if (this.app && typeof this.app.switchView === 'function') {
          this.app.switchView('HOME');
        }
      }, 1000);
    });

    // Anki export single dokkai question
    document.getElementById('btn-dokkai-anki-export')?.addEventListener('click', () => {
      this.exportCurrentToAnki();
    });

    // Anki export vocab buttons (Dock & Bottom)
    document.getElementById('btn-dock-export-vocab')?.addEventListener('click', () => {
      this.exportVocabToAnki();
    });
    document.getElementById('btn-dokkai-export-vocab-bottom')?.addEventListener('click', () => {
      this.exportVocabToAnki();
    });

    // Modal Mode selector buttons
    const modalModeButtons = this.containerEl.querySelectorAll('.btn-dokkai-modal-mode');
    modalModeButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const mode = btn.getAttribute('data-mode');
        this.setTimerMode(mode);
      });
    });

    // Dock Mode selector buttons
    const dockModeButtons = this.containerEl.querySelectorAll('.btn-dokkai-mode');
    dockModeButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const mode = btn.getAttribute('data-mode');
        this.setTimerMode(mode);
      });
    });

    // ==============================================================
    // STEP 2: VOCABULARY TOOLTIP & SELECTION LISTENERS
    // ==============================================================
    if (this.step === 2) {
      this.bindVocabTooltipEvents();
      this.bindSelectionHarvestEvents();
    }
  }

  bindVocabTooltipEvents() {
    const tooltipBox = document.getElementById('dokkai-vocab-tooltip-box');
    const vocabWords = this.containerEl.querySelectorAll('.dokkai-vocab-word');

    const hideTooltip = () => {
      if (tooltipBox) tooltipBox.classList.add('hidden');
    };

    vocabWords.forEach(span => {
      const showTooltipForSpan = (e) => {
        if (!tooltipBox) return;
        const word = span.getAttribute('data-word');
        const reading = span.getAttribute('data-reading');
        const hanviet = span.getAttribute('data-hanviet');
        const meaning = span.getAttribute('data-meaning');
        const isSaved = this.savedVocab.has(word);

        tooltipBox.innerHTML = `
          <div class="space-y-2">
            <div class="flex items-center justify-between gap-2 border-b border-slate-700/80 pb-1.5">
              <span class="font-bold text-amber-300 text-sm">${word}</span>
              <span class="text-slate-300 font-mono text-[11px]">${reading ? `【${reading}】` : ''}</span>
            </div>
            <div class="text-[11px] text-slate-300">
              <span class="text-indigo-300 font-semibold">Hán-Việt:</span> ${hanviet || '--'}
            </div>
            <div class="text-[11px] text-slate-200 leading-relaxed">
              <span class="text-indigo-300 font-semibold">Nghĩa:</span> ${meaning || '--'}
            </div>
            <button type="button" id="btn-tooltip-save-action" class="w-full py-1.5 px-2 rounded-xl font-bold text-[11px] transition flex items-center justify-center gap-1 cursor-pointer active:scale-95 ${
              isSaved
                ? 'bg-emerald-600 hover:bg-emerald-700 text-white'
                : 'bg-indigo-600 hover:bg-indigo-700 text-white'
            }">
              <span>${isSaved ? '✓ Đã lưu Anki (Nhấn để hủy)' : '⚡ Lưu vào Anki'}</span>
            </button>
          </div>
        `;

        const rect = span.getBoundingClientRect();
        tooltipBox.classList.remove('hidden');

        // Position tooltip nicely above or below
        const tooltipWidth = 260;
        let left = rect.left + window.scrollX + (rect.width / 2) - (tooltipWidth / 2);
        left = Math.max(10, Math.min(window.innerWidth - tooltipWidth - 20, left));
        let top = rect.top + window.scrollY - 130;
        if (rect.top < 150) {
          top = rect.bottom + window.scrollY + 8;
        }

        tooltipBox.style.left = `${left}px`;
        tooltipBox.style.top = `${top}px`;
        tooltipBox.style.width = `${tooltipWidth}px`;

        const btnSave = document.getElementById('btn-tooltip-save-action');
        if (btnSave) {
          btnSave.onclick = (event) => {
            event.stopPropagation();
            this.toggleSaveVocab({ word, reading, hanviet, meaning });
            hideTooltip();
          };
        }
      };

      span.addEventListener('mouseenter', showTooltipForSpan);
      span.addEventListener('click', (e) => {
        e.stopPropagation();
        showTooltipForSpan(e);
      });
    });

    document.addEventListener('click', (e) => {
      if (tooltipBox && !tooltipBox.contains(e.target) && !e.target.closest('.dokkai-vocab-word')) {
        hideTooltip();
      }
    }, { once: false });
  }

  bindSelectionHarvestEvents() {
    const passageEl = document.getElementById('dokkai-passage-container');
    const selectionToolbar = document.getElementById('dokkai-selection-toolbar');
    const selectionTextEl = document.getElementById('dokkai-selection-text');
    const btnSaveSelected = document.getElementById('btn-save-selected-to-anki');

    if (!passageEl || !selectionToolbar) return;

    let selectedPhrase = '';

    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection ? selection.toString().trim() : '';

      if (text.length >= 1 && text.length <= 40 && passageEl.contains(selection.anchorNode)) {
        selectedPhrase = text;
        if (selectionTextEl) selectionTextEl.textContent = `"${text}"`;
        selectionToolbar.classList.remove('hidden');
      } else {
        selectedPhrase = '';
        selectionToolbar.classList.add('hidden');
      }
    };

    passageEl.addEventListener('mouseup', handleSelection);
    passageEl.addEventListener('touchend', handleSelection);

    if (btnSaveSelected) {
      btnSaveSelected.onclick = () => {
        if (selectedPhrase) {
          this.saveSelectedTextToAnki(selectedPhrase);
          selectionToolbar.classList.add('hidden');
        }
      };
    }
  }

  exportCurrentToAnki() {
    const q = this.getCurrentQuestion();
    if (!q) return;

    const optLines = (q.options || []).map((o, i) => `${i + 1}. ${o}`).join('<br>');
    const frontText = `<b>【Đọc hiểu N1 - ${q.chapter}】</b><br>${q.title}<br><br><div style="text-align:left; line-height:1.8;">${q.passage.replace(/\n\n/g, '<br><br>')}</div><br><b>${q.question}</b><br><br>${optLines}`;
    const backText = `<b>【Đáp án đúng】: Phương án ${this.getCorrectAnswerNumber(q)}</b><br><br>${q.explanation || ''}`;
    const tags = `Koala_Dokkai_N1 ${q.chapter.replace(/[:：]/g, '_')}`;

    const tsvContent = `${frontText}\t${backText}\t${tags}\n`;
    const blob = new Blob([tsvContent], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Koala_Dokkai_${q.id}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    if (this.app && typeof this.app.showToast === 'function') {
      this.app.showToast('Đã tải file thẻ Anki (.txt) thành công!', 'success');
    }
  }
}
