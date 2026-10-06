/**
 * Koala JLPT Hub - Shin Kanzen Master Dokkai N1 Engine
 * Single-column layout, Adaptive Timer, 2-Step Logic Mastery (Highlighting + Trap Breakdown)
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
    this.step = 1; // 1: Reading & Timer, 2: Logic Highlights & Trap Breakdown
    this.selectedOption = null; // 0, 1, 2, 3
    this.userAnswersHistory = {}; // { questionId: { selectedOption, isCorrect, timeSpent } }

    // Timer State
    this.timerMode = 'standard'; // 'standard' | 'hardcore' | 'unlimited'
    this.totalTimerSeconds = 180;
    this.remainingSeconds = 180;
    this.elapsedSeconds = 0;
    this.timerInterval = null;
    this.isTimerRunning = false;
    this.isTimeUp = false;
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
    this.renderTimerBar();
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

    this.render();
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

    // Trigger visual shake on reading card
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
    const timerBadgeEl = document.getElementById('dokkai-timer-badge');
    const timerProgressEl = document.getElementById('dokkai-timer-progress');
    const timeUpWarningEl = document.getElementById('dokkai-timeup-warning');

    if (!timerDisplayEl) return;

    if (this.totalTimerSeconds > 0) {
      // Countdown
      timerDisplayEl.textContent = this.formatTime(this.remainingSeconds);
      if (timerProgressEl) {
        const pct = Math.max(0, Math.min(100, (this.remainingSeconds / this.totalTimerSeconds) * 100));
        timerProgressEl.style.width = `${pct}%`;
      }

      if (this.remainingSeconds <= 30 && !this.isTimeUp) {
        timerBadgeEl?.classList.remove('bg-indigo-50', 'text-indigo-700', 'border-indigo-200');
        timerBadgeEl?.classList.add('bg-rose-50', 'text-rose-600', 'border-rose-300', 'animate-pulse');
      }
    } else {
      // Unlimited mode: counts upward
      timerDisplayEl.textContent = `☕ ${this.formatTime(this.elapsedSeconds)}`;
      if (timerProgressEl) timerProgressEl.style.width = '100%';
    }

    if (this.isTimeUp && timeUpWarningEl) {
      timeUpWarningEl.classList.remove('hidden');
    }
  }

  // ==============================================================
  // STEP 2: LOGIC HIGHLIGHTING PROCESSOR
  // ==============================================================

  /**
   * Escape HTML special characters for text output
   */
  escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /**
   * Produce passage with 3-color highlights in Step 2:
   * 1. counterPremise -> Blue
   * 2. turningPoint -> Yellow
   * 3. authorConclusion -> Rose/Red
   */
  buildHighlightedPassage(passage, logicHighlights = {}) {
    if (!passage) return '';
    if (this.step !== 2 || !logicHighlights) {
      // Step 1: Clean, unhighlighted black-and-white text
      return passage
        .split('\n\n')
        .map(para => `<p class="mb-5 last:mb-0">${this.escapeHtml(para)}</p>`)
        .join('');
    }

    let text = passage;

    const { counterPremise, turningPoint, authorConclusion } = logicHighlights;

    // Placeholders to prevent overlapping nested replacements
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

    // Now escape the remaining text by paragraph
    let paragraphs = text.split('\n\n').map(p => this.escapeHtml(p));
    let combined = paragraphs.map(para => `<p class="mb-5 last:mb-0">${para}</p>`).join('');

    // Restore tokens
    if (replacedBlue) combined = combined.replace(tokenBlue, replacedBlue);
    if (replacedYellow) combined = combined.replace(tokenYellow, replacedYellow);
    if (replacedRed) combined = combined.replace(tokenRed, replacedRed);

    return combined;
  }

  // ==============================================================
  // USER ACTIONS
  // ==============================================================

  selectOption(optIdx) {
    if (this.step === 2) return; // Locked in Step 2
    this.selectedOption = optIdx;

    // Auto-start timer on first choice selection if user forgot to press start
    if (!this.isTimerRunning && !this.isTimeUp) {
      this.startTimer();
    }

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
    // Normalize answer: support both 0-indexed (0..3) and 1-indexed (1..4)
    const isCorrect = this.isAnswerCorrect(this.selectedOption, q.answer, q.trapBreakdown);

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

  isAnswerCorrect(userChoiceIdx, answerVal, trapBreakdown) {
    // 1. Direct index compare: 0-indexed or 1-indexed
    if (userChoiceIdx === answerVal) return true;
    if (userChoiceIdx + 1 === answerVal) return true;

    // 2. Fallback check: check if trapBreakdown for this option has 'ĐÁP ÁN ĐÚNG'
    if (trapBreakdown) {
      const optKey = `opt${userChoiceIdx + 1}`;
      if (trapBreakdown[optKey] && (trapBreakdown[optKey].includes('ĐÁP ÁN ĐÚNG') || trapBreakdown[optKey].includes('Đáp án đúng'))) {
        return true;
      }
    }
    return false;
  }

  goToQuestion(index) {
    if (index < 0 || index >= this.questions.length) return;
    this.currentIndex = index;
    this.resetQuestionState();
    this.render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  retakeCurrentQuestion() {
    this.resetQuestionState();
    this.render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ==============================================================
  // RENDER MAIN SINGLE-COLUMN VIEW
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
    const isCorrect = isAnswered && this.isAnswerCorrect(this.selectedOption, q.answer, q.trapBreakdown);

    this.containerEl.innerHTML = `
      <div class="dokkai-single-column max-w-4xl mx-auto px-3 sm:px-6 py-6 sm:py-8 space-y-6 sm:space-y-8 animate-fade-in font-sans">
        
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
            <button type="button" id="btn-dokkai-prev" class="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition disabled:opacity-30 disabled:cursor-not-allowed" ${this.currentIndex === 0 ? 'disabled' : ''} title="Bài trước">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
            </button>
            <div class="flex items-center gap-1">
              ${this.questions.map((item, idx) => `
                <button type="button" class="btn-dokkai-page w-7 h-7 rounded-xl text-xs font-bold transition flex items-center justify-center ${
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
            <button type="button" id="btn-dokkai-next" class="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition disabled:opacity-30 disabled:cursor-not-allowed" ${this.currentIndex === this.questions.length - 1 ? 'disabled' : ''} title="Bài tiếp">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </button>
          </div>
        </div>

        <!-- Adaptive Timer & Mode Controls Toolbar -->
        <div id="dokkai-timer-toolbar" class="bg-white rounded-2xl border border-slate-200/90 p-4 shadow-2xs">
          ${this.renderTimerToolbarHtml(cfg)}
        </div>

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
              <button type="button" id="btn-dokkai-retake-top" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 transition flex items-center gap-1.5 shadow-2xs">
                <span>🔄 Làm lại</span>
              </button>
              ${this.currentIndex < this.questions.length - 1 ? `
                <button type="button" id="btn-dokkai-next-top" class="px-4 py-1.5 rounded-xl text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white transition flex items-center gap-1.5 shadow-xs">
                  <span>Bài tiếp theo ➡</span>
                </button>
              ` : ''}
            </div>
          </div>
        ` : ''}

        <!-- Reading Passage Card (Single-Column top) -->
        <div id="dokkai-reading-card" class="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-9 shadow-sm transition-card relative">
          
          <!-- Card Header & Legend -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 mb-5 border-b border-slate-100">
            <div class="flex items-center gap-2">
              <span class="w-8 h-8 rounded-xl bg-slate-100 text-slate-700 flex items-center justify-center font-bold text-xs">
                📄
              </span>
              <div>
                <h2 class="text-xs font-bold text-slate-400 uppercase tracking-wider">Văn bản bài đọc gốc</h2>
                <div class="text-[11px] text-slate-500 font-medium">Cỡ chữ 17px • Giãn dòng thoáng • Tiếng Nhật N1 chuẩn mực</div>
              </div>
            </div>

            <!-- Legend (Step 2 Only) -->
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
              </div>
            ` : `
              <div class="text-[11px] font-semibold text-slate-400 flex items-center gap-1">
                <span>🛡️ Bước 1: Đọc tự lực không gợi ý</span>
              </div>
            `}
          </div>

          <!-- Passage Content -->
          <div class="dokkai-passage-text font-jp text-slate-800 text-base sm:text-[17px] leading-[2.3] tracking-wide select-text">
            ${this.buildHighlightedPassage(q.passage, q.logicHighlights)}
          </div>

        </div>

        <!-- Question & 4 Options Section (Neatly underneath) -->
        <div class="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm space-y-6">
          
          <!-- Question Title -->
          <div class="space-y-1">
            <div class="text-xs font-bold text-indigo-700 uppercase tracking-wider flex items-center gap-1.5">
              <span>❓ CÂU HỎI ĐỌC HIỂU</span>
            </div>
            <h3 class="font-jp text-base sm:text-lg font-bold text-slate-900 leading-snug">
              ${this.escapeHtml(q.question)}
            </h3>
          </div>

          <!-- 4 Options Stack -->
          <div class="options-stack space-y-3">
            ${(q.options || []).map((opt, optIdx) => {
              const isSelected = this.selectedOption === optIdx;
              const isThisCorrect = isAnswered && this.isAnswerCorrect(optIdx, q.answer, q.trapBreakdown);
              const isSelectedAndWrong = isAnswered && isSelected && !isThisCorrect;

              let optionStyle = 'border-slate-200 bg-white hover:border-indigo-300 hover:bg-slate-50/70 text-slate-800';
              let badgeStyle = 'bg-slate-100 text-slate-600 border-slate-200';

              if (this.step === 1) {
                if (isSelected) {
                  optionStyle = 'border-indigo-600 bg-indigo-50/70 text-indigo-950 ring-2 ring-indigo-500/20 shadow-xs font-semibold';
                  badgeStyle = 'bg-indigo-600 text-white border-indigo-600 shadow-xs';
                }
              } else {
                // Step 2 post-submit
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
                <button type="button" class="btn-dokkai-option w-full text-left p-4 sm:p-5 rounded-2xl border-2 transition-all flex items-start gap-3.5 group cursor-pointer ${optionStyle}" data-opt-idx="${optIdx}" ${this.step === 2 ? 'disabled' : ''}>
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

          <!-- Step 1 Action Button -->
          ${this.step === 1 ? `
            <div class="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3">
              <div class="text-xs text-slate-500">
                ${this.selectedOption !== null 
                  ? `<span class="font-bold text-indigo-700">Đã chọn phương án ${this.selectedOption + 1}.</span> Nhấn nút bên cạnh để chốt đáp án & mở highlight mổ xẻ.`
                  : 'Hãy đọc kỹ văn bản, chọn 1 phương án để mở khóa phân tích.'}
              </div>

              <button type="button" id="btn-dokkai-submit" class="w-full sm:w-auto px-7 py-3.5 rounded-xl font-bold text-xs shadow-md transition flex items-center justify-center gap-2 ${
                this.selectedOption !== null
                  ? 'bg-gradient-to-r from-indigo-600 to-indigo-800 hover:from-indigo-700 hover:to-indigo-900 text-white shadow-indigo-200 cursor-pointer active:scale-95'
                  : 'bg-slate-200 text-slate-400 cursor-not-allowed'
              }" ${this.selectedOption === null ? 'disabled' : ''}>
                <span>🎯 Chốt đáp án & Mổ xẻ logic</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
              </button>
            </div>
          ` : ''}

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
                  const isThisCorrect = this.isAnswerCorrect(num - 1, q.answer, q.trapBreakdown);
                  const isUserPick = this.selectedOption === (num - 1);

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
                <button type="button" id="btn-dokkai-anki-export" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-white hover:bg-amber-50 text-amber-800 border border-amber-200 transition shadow-2xs flex items-center gap-1.5 cursor-pointer active:scale-95" title="Tải file text nạp vào Anki">
                  <span>⚡ Tải thẻ Anki (.txt)</span>
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
    `;

    this.bindEvents();
    this.updateTimerDisplay();
  }

  renderTimerToolbarHtml(cfg) {
    return `
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <!-- Left: Timer Mode Selector (disabled when running) -->
        <div class="flex flex-wrap items-center gap-1.5">
          <span class="text-xs font-bold text-slate-500 mr-1 flex items-center gap-1">
            <svg class="w-3.5 h-3.5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Thời gian:
          </span>

          <button type="button" class="btn-dokkai-mode px-3 py-1.5 rounded-xl text-xs font-bold transition flex items-center gap-1 ${
            this.timerMode === 'standard'
              ? 'bg-emerald-600 text-white shadow-xs'
              : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
          }" data-mode="standard" ${this.isTimerRunning ? 'disabled' : ''}>
            ${cfg.standard.badge}
          </button>

          <button type="button" class="btn-dokkai-mode px-3 py-1.5 rounded-xl text-xs font-bold transition flex items-center gap-1 ${
            this.timerMode === 'hardcore'
              ? 'bg-rose-600 text-white shadow-xs'
              : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
          }" data-mode="hardcore" ${this.isTimerRunning ? 'disabled' : ''}>
            ${cfg.hardcore.badge}
          </button>

          <button type="button" class="btn-dokkai-mode px-3 py-1.5 rounded-xl text-xs font-bold transition flex items-center gap-1 ${
            this.timerMode === 'unlimited'
              ? 'bg-amber-600 text-white shadow-xs'
              : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
          }" data-mode="unlimited" ${this.isTimerRunning ? 'disabled' : ''}>
            ${cfg.unlimited.badge}
          </button>
        </div>

        <!-- Right: Countdown Clock Display & Start / Status -->
        <div class="flex items-center gap-2.5 w-full sm:w-auto justify-between sm:justify-end">
          <div id="dokkai-timer-badge" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200 shadow-2xs flex items-center gap-2">
            <span class="w-2 h-2 rounded-full ${this.isTimerRunning ? 'bg-emerald-500 animate-ping' : 'bg-slate-400'}"></span>
            <span id="dokkai-timer-display" class="font-mono text-sm font-extrabold tracking-wider">
              ${this.totalTimerSeconds > 0 ? this.formatTime(this.remainingSeconds) : '☕ 00:00'}
            </span>
          </div>

          ${!this.isTimerRunning && this.step === 1 ? `
            <button type="button" id="btn-dokkai-start-timer" class="px-4 py-1.5 rounded-xl text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white transition shadow-xs flex items-center gap-1.5 active:scale-95 cursor-pointer">
              <span>🚀 Bắt đầu đọc</span>
            </button>
          ` : this.isTimerRunning ? `
            <span class="text-[11px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-lg border border-emerald-200">
              Đang tính giờ...
            </span>
          ` : `
            <span class="text-[11px] font-semibold text-slate-500 bg-slate-100 px-2 py-1 rounded-lg">
              Đã chốt kết quả
            </span>
          `}
        </div>
      </div>

      <!-- Linear progress bar -->
      <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden mt-3">
        <div id="dokkai-timer-progress" class="bg-gradient-to-r from-indigo-500 to-indigo-600 h-full rounded-full transition-all duration-500" style="width: 100%"></div>
      </div>

      <!-- Timeup warning banner -->
      <div id="dokkai-timeup-warning" class="hidden mt-2 p-2 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 font-bold text-center">
        ⚠️ ĐÃ HẾT THỜI GIAN TIÊU CHUẨN! Vui lòng chọn đáp án và ấn "Chốt đáp án & Mổ xẻ logic" ngay!
      </div>
    `;
  }

  renderTimerBar() {
    const toolbar = document.getElementById('dokkai-timer-toolbar');
    if (!toolbar) return;
    const q = this.getCurrentQuestion();
    const qType = (q && q.mondaiType) || 'short';
    const cfg = TIMER_CONFIGS[qType] || TIMER_CONFIGS.short;
    toolbar.innerHTML = this.renderTimerToolbarHtml(cfg);
    this.bindTimerEvents();
  }

  // ==============================================================
  // EVENT BINDINGS
  // ==============================================================

  bindEvents() {
    this.bindTimerEvents();

    // Option cards click
    const optButtons = this.containerEl.querySelectorAll('.btn-dokkai-option');
    optButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.getAttribute('data-opt-idx'), 10);
        this.selectOption(idx);
      });
    });

    // Submit button in Step 1
    const submitBtn = document.getElementById('btn-dokkai-submit');
    if (submitBtn) {
      submitBtn.addEventListener('click', () => this.submitAnswer());
    }

    // Pagination buttons
    const prevBtn = document.getElementById('btn-dokkai-prev');
    if (prevBtn) {
      prevBtn.addEventListener('click', () => this.goToQuestion(this.currentIndex - 1));
    }
    const nextBtn = document.getElementById('btn-dokkai-next');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => this.goToQuestion(this.currentIndex + 1));
    }

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
      }, 1200);
    });

    // Anki export single dokkai question
    document.getElementById('btn-dokkai-anki-export')?.addEventListener('click', () => {
      this.exportCurrentToAnki();
    });
  }

  bindTimerEvents() {
    // Mode switcher buttons
    const modeButtons = this.containerEl.querySelectorAll('.btn-dokkai-mode');
    modeButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const mode = btn.getAttribute('data-mode');
        this.setTimerMode(mode);
      });
    });

    // Start timer button
    const startBtn = document.getElementById('btn-dokkai-start-timer');
    if (startBtn) {
      startBtn.addEventListener('click', () => this.startTimer());
    }
  }

  exportCurrentToAnki() {
    const q = this.getCurrentQuestion();
    if (!q) return;

    const optLines = (q.options || []).map((o, i) => `${i + 1}. ${o}`).join('<br>');
    const frontText = `<b>【Đọc hiểu N1 - ${q.chapter}】</b><br>${q.title}<br><br><div style="text-align:left; line-height:1.8;">${q.passage.replace(/\n\n/g, '<br><br>')}</div><br><b>${q.question}</b><br><br>${optLines}`;
    const backText = `<b>【Đáp án đúng】: Phương án ${q.answer}</b><br><br>${q.explanation || ''}`;
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
