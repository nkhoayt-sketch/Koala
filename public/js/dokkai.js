import { storage } from './storage.js';

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

    this.viewMode = 'hub'; // 'hub' | 'reader'
    this.filterChapter = 'all'; // 'all' | 'skz_ch01' | 'skz_ch02'
    this.cachedChapters = {};
    this.allPassages = [];

    this.chapterData = null;
    this.questions = [];
    this.currentIndex = 0;

    // State per question
    this.step = 1; // 1: Reading & Timer, 2: Logic Highlights & Trap Breakdown
    this.isStarted = false; // Blur/Lock overlay before user clicks Start in modal
    this.selectedOption = null; // 0, 1, 2, 3
    this.userAnswersHistory = {}; // { [questionId]: { selectedOption, selectedAnswer, isCompleted, isCorrect, timeSpent, completedAt } }

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
   * Preload all chapter JSON files (ch01 to ch06) and assemble the flattened passage registry
   */
  async ensureDataLoaded() {
    if (this.allPassages.length >= 24 && Object.keys(this.cachedChapters).length >= 6) {
      return;
    }

    try {
      const fetchWithFallback = async (chId) => {
        const candidatePaths = [
          `/data/n1_dokkai/shinkanzen_${chId}.json`,
          `data/n1_dokkai/shinkanzen_${chId}.json`,
          `public/data/n1_dokkai/shinkanzen_${chId}.json`
        ];

        let lastErr = null;
        for (const p of candidatePaths) {
          try {
            const r = await fetch(p);
            if (r.ok) {
              return await r.json();
            }
          } catch (err) {
            lastErr = err;
          }
        }
        console.error(`Lỗi nạp bài đọc shinkanzen_${chId}.json:`, lastErr || 'File not found');
        return null;
      };

      const chapterIds = ['ch01', 'ch02', 'ch03', 'ch04', 'ch05', 'ch06'];
      const results = await Promise.all(
        chapterIds.map(chId => fetchWithFallback(chId))
      );

      chapterIds.forEach((chId, idx) => {
        const data = results[idx];
        if (data) {
          const key = `skz_${chId}`;
          this.cachedChapters[key] = data;
        }
      });

      this.buildAllPassagesList();
    } catch (e) {
      console.error('Lỗi nạp bài đọc Dokkai (toàn cục):', e);
    }
  }

  buildAllPassagesList() {
    this.allPassages = [];
    const chKeys = ['skz_ch01', 'skz_ch02', 'skz_ch03', 'skz_ch04', 'skz_ch05', 'skz_ch06'];
    chKeys.forEach(chKey => {
      const chData = this.cachedChapters[chKey];
      if (!chData) return;
      const qs = chData.questions || [];
      qs.forEach((q, idx) => {
        this.allPassages.push({
          id: q.id,
          chapterKey: chKey,
          chapterId: chData.chapterId || chKey,
          chapterTitle: chData.chapter || q.chapter,
          title: q.title || `${chData.chapter} - 練習 ${idx + 1}`,
          mondaiType: q.mondaiType || 'short',
          question: q.question,
          passage: q.passage,
          passageExcerpt: (q.passage || '').slice(0, 130).replace(/\n+/g, ' ').trim() + '...',
          qData: q,
          indexInChapter: idx,
          chapterData: chData
        });
      });
    });
  }

  /**
   * Display the Dokkai Selection Grid (Hub View)
   */
  async showHub(filterTab = 'all') {
    this.stopTimer();
    await this.ensureDataLoaded();
    this.loadPersistedProgress();
    this.viewMode = 'hub';
    if (filterTab) this.filterChapter = filterTab;
    this.render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /**
   * Open a specific passage directly from the Hub grid
   */
  async openPassage(passageId) {
    await this.ensureDataLoaded();
    this.loadPersistedProgress();

    const target = this.allPassages.find(p => p.id === passageId);
    if (!target) {
      console.warn('Passage not found:', passageId);
      return;
    }

    this.chapterData = target.chapterData;
    this.questions = target.chapterData.questions || [];
    this.currentIndex = target.indexInChapter;
    this.viewMode = 'reader';

    const hist = this.userAnswersHistory[passageId];
    if (hist && hist.isCompleted) {
      this.step = 2;
      this.isStarted = true;
      this.selectedOption = hist.selectedOption !== undefined ? hist.selectedOption : (hist.selectedAnswer - 1);
      this.elapsedSeconds = hist.timeSpent || 0;
      this.stopTimer();
    } else {
      this.resetQuestionState();
    }

    this.render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /**
   * Load chapter data and initialize reading with saved LocalStorage state
   */
  loadChapter(chapterData, initialIndex = 0) {
    this.viewMode = 'reader';
    this.chapterData = chapterData;
    this.questions = chapterData.questions || [];
    this.currentIndex = Math.max(0, Math.min(initialIndex, this.questions.length - 1));

    if (chapterData.chapterId === 'ch01' || chapterData.chapter?.includes('第1章')) {
      this.cachedChapters.skz_ch01 = chapterData;
    } else if (chapterData.chapterId === 'ch02' || chapterData.chapter?.includes('第2章')) {
      this.cachedChapters.skz_ch02 = chapterData;
    }
    this.buildAllPassagesList();

    // Load persisted progress from LocalStorage
    this.loadPersistedProgress();

    // Check if the initial question was already completed
    const currentQ = this.getCurrentQuestion();
    if (currentQ && this.userAnswersHistory[currentQ.id]?.isCompleted) {
      const saved = this.userAnswersHistory[currentQ.id];
      this.step = 2;
      this.isStarted = true;
      this.selectedOption = saved.selectedOption;
      this.elapsedSeconds = saved.timeSpent || 0;
      this.stopTimer();
    } else {
      this.resetQuestionState();
    }

    this.render();
  }

  loadPersistedProgress() {
    try {
      const savedProgress = storage.getDokkaiProgress();
      if (savedProgress && typeof savedProgress === 'object') {
        Object.entries(savedProgress).forEach(([id, item]) => {
          if (item && item.isCompleted) {
            this.userAnswersHistory[id] = {
              selectedOption: item.selectedAnswer !== undefined ? (item.selectedAnswer - 1) : item.selectedOption,
              selectedAnswer: item.selectedAnswer,
              isCompleted: true,
              isCorrect: !!item.isCorrect,
              timeSpent: item.timeSpent || 0,
              completedAt: item.completedAt
            };
          }
        });
      }
    } catch (e) {
      console.warn('Could not restore dokkai progress from localStorage:', e);
    }
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
  // STEP 2: LOGIC HIGHLIGHTING PROCESSOR (PURE JAPANESE TEXT)
  // ==============================================================

  escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  buildHighlightedPassage(passage, logicHighlights = {}) {
    if (!passage) return '';
    if (this.step !== 2 || !logicHighlights) {
      // Step 1: Clean, unhighlighted authentic text for pure reading practice
      return passage
        .split('\n\n')
        .map(para => `<p class="mb-5 last:mb-0">${this.escapeHtml(para)}</p>`)
        .join('');
    }

    // Step 2: Full logic highlights (3 colors) without internal tooltips (Mazii/Yomitan friendly)
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
    const selectedAnswer = this.selectedOption + 1; // 1-based answer index

    // Update in-memory state
    this.userAnswersHistory[q.id] = {
      selectedOption: this.selectedOption,
      selectedAnswer,
      isCompleted: true,
      isCorrect,
      timeSpent: this.elapsedSeconds,
      completedAt: new Date().toISOString()
    };

    // Instant per-passage LocalStorage persistence (PHẦN 1: LocalStorage Per-Item Persistence)
    storage.saveDokkaiPassageProgress(q.id, {
      selectedAnswer,
      isCorrect,
      timeSpent: this.elapsedSeconds,
      completedAt: new Date().toISOString()
    });

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
    if (q && this.userAnswersHistory[q.id]?.isCompleted) {
      const hist = this.userAnswersHistory[q.id];
      this.step = 2;
      this.isStarted = true;
      this.selectedOption = hist.selectedOption !== undefined ? hist.selectedOption : (hist.selectedAnswer - 1);
      this.elapsedSeconds = hist.timeSpent || 0;
      this.stopTimer();
    } else {
      this.resetQuestionState();
    }
    this.render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  retakeCurrentQuestion() {
    const q = this.getCurrentQuestion();
    if (q) {
      delete this.userAnswersHistory[q.id];
      storage.removeDokkaiPassageProgress(q.id);
    }
    this.resetQuestionState();
    this.render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ==============================================================
  // RENDER DISPATCHER
  // ==============================================================

  render() {
    if (!this.containerEl) return;
    if (this.viewMode === 'hub') {
      this.renderHub();
    } else {
      this.renderReader();
    }
  }

  // ==============================================================
  // DOKKAI SELECTION GRID (ON-DEMAND HUB VIEW)
  // ==============================================================

  renderHub() {
    const progressMap = storage.getDokkaiProgress();
    const totalCount = this.allPassages.length;
    let doneCount = 0;
    let correctCount = 0;

    this.allPassages.forEach(p => {
      const h = progressMap[p.id] || this.userAnswersHistory[p.id];
      if (h && h.isCompleted) {
        doneCount++;
        if (h.isCorrect) correctCount++;
      }
    });

    const wrongCount = doneCount - correctCount;
    const progressPct = totalCount > 0 ? Math.round((doneCount / totalCount) * 100) : 0;

    const chaptersMeta = [
      { key: 'all', label: 'Tất cả bài học', color: 'bg-slate-900', lightColor: 'bg-slate-100 text-slate-700' },
      { key: 'skz_ch01', label: '第1章: 対比', color: 'bg-amber-600', lightColor: 'bg-amber-100 text-amber-800' },
      { key: 'skz_ch02', label: '第2章: 言い換え', color: 'bg-indigo-600', lightColor: 'bg-indigo-100 text-indigo-800' },
      { key: 'skz_ch03', label: '第3章: 主張', color: 'bg-emerald-600', lightColor: 'bg-emerald-100 text-emerald-800' },
      { key: 'skz_ch04', label: '第4章: 指示語', color: 'bg-teal-600', lightColor: 'bg-teal-100 text-teal-800' },
      { key: 'skz_ch05', label: '第5章: 理由', color: 'bg-rose-600', lightColor: 'bg-rose-100 text-rose-800' },
      { key: 'skz_ch06', label: '第6章: 実践', color: 'bg-purple-600', lightColor: 'bg-purple-100 text-purple-800' },
    ];

    const chStyleMap = {
      skz_ch01: { num: '第1章', style: 'bg-amber-50 text-amber-800 border-amber-200' },
      skz_ch02: { num: '第2章', style: 'bg-indigo-50 text-indigo-700 border-indigo-200' },
      skz_ch03: { num: '第3章', style: 'bg-emerald-50 text-emerald-800 border-emerald-200' },
      skz_ch04: { num: '第4章', style: 'bg-teal-50 text-teal-800 border-teal-200' },
      skz_ch05: { num: '第5章', style: 'bg-rose-50 text-rose-800 border-rose-200' },
      skz_ch06: { num: '第6章', style: 'bg-purple-50 text-purple-800 border-purple-200' },
    };

    const filteredPassages = this.filterChapter === 'all'
      ? this.allPassages
      : this.allPassages.filter(p => p.chapterKey === this.filterChapter);

    this.containerEl.innerHTML = `
      <div class="dokkai-hub-view max-w-7xl mx-auto px-3 sm:px-6 py-6 space-y-6 animate-fade-in font-sans">
        
        <!-- Header Banner -->
        <div class="bg-gradient-to-br from-white via-amber-50/30 to-indigo-50/40 rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div class="space-y-3">
              <div class="flex flex-wrap items-center gap-2">
                <button type="button" id="btn-dokkai-hub-back-home" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold text-slate-700 bg-white hover:bg-slate-100 border border-slate-200/90 shadow-2xs hover:shadow-xs transition active:scale-95 cursor-pointer" title="Quay lại Trang Chủ">
                  <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
                  <span>Trang Chủ</span>
                </button>
                <span class="px-2.5 py-1 rounded-full text-xs font-extrabold bg-amber-100 text-amber-900 border border-amber-300">
                  📖 Dokkai N1 (Shin Kanzen Master)
                </span>
                <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 flex items-center gap-1">
                  <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  🟢 Kho Luyện Đề Tự Do (${totalCount} bài • 6 chương)
                </span>
                <span class="px-2 py-0.5 rounded-md text-[11px] font-bold bg-slate-100 text-slate-600">
                  🔓 100% Không khóa tuần tự
                </span>
              </div>

              <div>
                <h1 class="text-xl sm:text-2xl lg:text-3xl font-black text-slate-900 tracking-tight font-jp">
                  Dokkai N1 • 新完全マスター読解 自由練習ハブ
                </h1>
                <p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-3xl leading-relaxed">
                  Kho luyện đọc hiểu Dokkai N1 toàn diện với 24 bài đọc thực chiến thuộc 6 chương. Luyện tư duy bóc tách cấu trúc, phản xạ bắt bẫy và làm chủ thời gian thi thật mà không bị gò bó thứ tự.
                </p>
              </div>
            </div>

            <!-- Hub Stats Mini Card -->
            <div class="bg-white/90 backdrop-blur-md rounded-2xl border border-slate-200 p-4 sm:p-5 shrink-0 shadow-xs space-y-3 min-w-[260px]">
              <div class="flex items-center justify-between text-xs font-bold text-slate-700 pb-2 border-b border-slate-100">
                <span>Tiến độ cá nhân</span>
                <span class="font-mono text-indigo-600">${doneCount}/${totalCount} bài (${progressPct}%)</span>
              </div>

              <div class="grid grid-cols-3 gap-2 text-center">
                <div class="bg-emerald-50 rounded-xl p-2 border border-emerald-200">
                  <div class="text-base font-black text-emerald-700">${correctCount}</div>
                  <div class="text-[10px] font-bold text-emerald-800">Đúng</div>
                </div>
                <div class="bg-rose-50 rounded-xl p-2 border border-rose-200">
                  <div class="text-base font-black text-rose-700">${wrongCount}</div>
                  <div class="text-[10px] font-bold text-rose-800">Sai</div>
                </div>
                <div class="bg-slate-50 rounded-xl p-2 border border-slate-200">
                  <div class="text-base font-black text-slate-700">${totalCount - doneCount}</div>
                  <div class="text-[10px] font-bold text-slate-600">Chưa làm</div>
                </div>
              </div>

              <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden border border-slate-200/60">
                <div class="h-full bg-gradient-to-r from-emerald-500 to-indigo-600 rounded-full transition-all duration-500" style="width: ${progressPct}%"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Filter Tabs -->
        <div class="flex flex-wrap items-center gap-2 pb-2 border-b border-slate-200/80">
          <span class="text-xs font-bold text-slate-500 mr-1 flex items-center gap-1">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/></svg>
            Lọc theo chương:
          </span>

          ${chaptersMeta.map(ch => {
            const count = ch.key === 'all' ? totalCount : this.allPassages.filter(p => p.chapterKey === ch.key).length;
            const isActive = this.filterChapter === ch.key;
            return `
              <button type="button" class="btn-dokkai-hub-tab px-3.5 py-2 rounded-2xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                isActive
                  ? `${ch.color} text-white shadow-xs`
                  : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200'
              }" data-tab="${ch.key}">
                <span>${ch.label}</span>
                <span class="px-1.5 py-0.2 rounded-full text-[10px] ${isActive ? 'bg-white/20 text-white' : ch.lightColor}">${count}</span>
              </button>
            `;
          }).join('')}
        </div>

        <!-- Lessons Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-4 gap-4 sm:gap-5">
          ${filteredPassages.map(item => {
            const hist = progressMap[item.id] || this.userAnswersHistory[item.id];
            const isDone = hist && hist.isCompleted;
            const isCorrect = isDone && hist.isCorrect;
            const timeSpentText = isDone ? this.formatTime(hist.timeSpent || 0) : '';

            const qType = item.mondaiType || 'short';
            const cfg = TIMER_CONFIGS[qType] || TIMER_CONFIGS.short;
            const typeBadgeText = `${cfg.name.split(' ')[0]} (${cfg.standard.label})`;
            const chMeta = chStyleMap[item.chapterKey] || { num: 'Bài đọc', style: 'bg-slate-100 text-slate-700 border-slate-200' };

            let statusBadge = `
              <span class="px-2.5 py-0.8 rounded-full text-[11px] font-bold bg-slate-100 text-slate-500 border border-slate-200">
                Chưa làm
              </span>
            `;
            if (isDone) {
              if (isCorrect) {
                statusBadge = `
                  <span class="px-2.5 py-0.8 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-300 flex items-center gap-1">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                    <span>✓ Hoàn thành (Đúng) • ${timeSpentText}</span>
                  </span>
                `;
              } else {
                statusBadge = `
                  <span class="px-2.5 py-0.8 rounded-full text-[11px] font-bold bg-rose-50 text-rose-800 border border-rose-300 flex items-center gap-1">
                    <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                    <span>✕ Đã làm (Sai) • ${timeSpentText}</span>
                  </span>
                `;
              }
            }

            return `
              <div class="dokkai-hub-card group bg-white rounded-3xl border ${
                isDone 
                  ? (isCorrect ? 'border-emerald-200/90 hover:border-emerald-400 bg-emerald-50/10' : 'border-rose-200/90 hover:border-rose-400 bg-rose-50/10') 
                  : 'border-slate-200/90 hover:border-amber-400'
              } p-5 shadow-sm hover:shadow-md transition-all flex flex-col justify-between cursor-pointer" data-passage-id="${item.id}">
                
                <div class="space-y-3">
                  <!-- Badges & Status -->
                  <div class="flex flex-wrap items-center justify-between gap-1.5">
                    <div class="flex items-center gap-1">
                      <span class="px-2 py-0.5 rounded-md text-[10px] font-extrabold border ${chMeta.style}">
                        ${chMeta.num}
                      </span>
                      <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-slate-100 text-slate-600">
                        ${typeBadgeText}
                      </span>
                    </div>
                    ${statusBadge}
                  </div>

                    <div>
                      <h3 class="font-jp text-base font-black text-slate-900 group-hover:text-amber-700 transition leading-snug">
                        ${this.escapeHtml(item.title)}
                      </h3>
                      <p class="text-[11px] text-slate-400 mt-0.5 font-medium truncate">
                        ${item.chapterTitle}
                      </p>
                    </div>

                  <!-- Japanese Excerpt -->
                  <div class="font-jp text-xs text-slate-600 leading-relaxed bg-slate-50/90 p-3 rounded-2xl border border-slate-100 line-clamp-3 select-none">
                    ${this.escapeHtml(item.passageExcerpt)}
                  </div>

                  <!-- Question preview -->
                  <div class="text-[11px] font-medium text-slate-500 flex items-center gap-1 pt-0.5">
                    <span class="text-amber-700 font-bold shrink-0">❓ Hỏi:</span>
                    <span class="truncate font-jp">${this.escapeHtml(item.question)}</span>
                  </div>
                </div>

                <!-- Launch Button -->
                <div class="pt-4 mt-3 border-t border-slate-100">
                  ${!isDone ? `
                    <button type="button" class="btn-card-launch w-full py-2.5 px-3 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 active:scale-98 text-white font-bold text-xs shadow-xs transition flex items-center justify-center gap-1.5 cursor-pointer">
                      <span>Luyện tập ngay 🚀</span>
                    </button>
                  ` : isCorrect ? `
                    <button type="button" class="btn-card-launch w-full py-2.5 px-3 rounded-xl bg-emerald-50 hover:bg-emerald-100 active:scale-98 text-emerald-800 font-bold text-xs border border-emerald-300 transition flex items-center justify-center gap-1.5 cursor-pointer">
                      <span>Xem lại phân tích 🔍</span>
                    </button>
                  ` : `
                    <button type="button" class="btn-card-launch w-full py-2.5 px-3 rounded-xl bg-rose-50 hover:bg-rose-100 active:scale-98 text-rose-800 font-bold text-xs border border-rose-300 transition flex items-center justify-center gap-1.5 cursor-pointer">
                      <span>Mổ xẻ nguyên nhân sai 🔍</span>
                    </button>
                  `}
                </div>

              </div>
            `;
          }).join('')}
        </div>

      </div>
    `;

    this.bindHubEvents();
  }

  bindHubEvents() {
    // Back to Home
    document.getElementById('btn-dokkai-hub-back-home')?.addEventListener('click', () => {
      if (this.app && typeof this.app.switchView === 'function') {
        this.app.switchView('HOME');
      }
    });

    // Tab buttons
    const tabButtons = this.containerEl.querySelectorAll('.btn-dokkai-hub-tab');
    tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const tab = btn.getAttribute('data-tab');
        this.filterChapter = tab;
        this.renderHub();
      });
    });

    // Passage card clicks
    const cards = this.containerEl.querySelectorAll('.dokkai-hub-card');
    cards.forEach(card => {
      card.addEventListener('click', () => {
        const passageId = card.getAttribute('data-passage-id');
        if (passageId) {
          this.openPassage(passageId);
        }
      });
    });
  }

  // ==============================================================
  // RENDER MAIN 2-COLUMN WORKSPACE (READER VIEW)
  // ==============================================================

  renderReader() {
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

    // Requirement 1: Pure Japanese title according to book
    const japaneseTitle = q.title || `第1章：対比・逆接 - 練習 ${this.currentIndex + 1}`;

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
              <button type="button" id="btn-dokkai-back-hub" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-xl text-xs font-bold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 shadow-2xs hover:shadow-xs transition active:scale-95 cursor-pointer" title="Quay lại Kho Luyện Đề Tự Do">
                <span>📋 Kho bài đọc</span>
              </button>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-extrabold bg-indigo-50 text-indigo-700 border border-indigo-200">
                📖 Dokkai N1 (Shin Kanzen Master)
              </span>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-50 text-amber-800 border border-amber-200">
                ${q.chapter || '第1章：対比・逆接'}
              </span>
              <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-slate-100 text-slate-600">
                ${typeLabel}
              </span>
            </div>
            <h1 class="text-lg sm:text-xl font-black text-slate-900 tracking-tight font-jp">
              ${this.escapeHtml(japaneseTitle)}
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

          <!-- LEFT COLUMN: Reading, Questions, and Step 2 Analysis (~75%) -->
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
              
              <!-- PRE-START BLUR OVERLAY MODAL (Single centralized start button) -->
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

                    <!-- Single Primary Start Button -->
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
                  
                  <!-- Card Header: Clean Title Without Meta Text (Requirement 4) -->
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 mb-5 border-b border-slate-100">
                    <div class="flex items-center gap-2">
                      <span class="w-8 h-8 rounded-xl bg-slate-100 text-slate-700 flex items-center justify-center font-bold text-xs">
                        📄
                      </span>
                      <h2 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Văn bản bài đọc gốc</h2>
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
                        <span>${this.isStarted ? '⚡ Bước 1: Đọc tự lực & tư duy độc lập' : '🛡️ Bài đọc được che mờ chống lộ đề'}</span>
                      </div>
                    `}
                  </div>

                  <!-- Pure Authentic Japanese Passage Content (Requirement 3: Clean, Extension Friendly) -->
                  <div id="dokkai-passage-container" class="dokkai-passage-text font-jp text-slate-800 text-base sm:text-[17px] leading-[2.3] tracking-wide select-text relative">
                    ${this.buildHighlightedPassage(q.passage, q.logicHighlights)}
                  </div>

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
                      // Strictly single correct answer: (optIdx + 1) === correctNum
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
                      // Strictly single correct answer: only num === correctNum gets isThisCorrect = true
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
                      <span>🔄 Làm lại bài này</span>
                    </button>
                    <button type="button" id="btn-dokkai-back-hub-bottom" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 transition shadow-2xs flex items-center gap-1.5 cursor-pointer active:scale-95">
                      <span>📋 Chọn bài khác</span>
                    </button>
                    <button type="button" id="btn-dokkai-anki-export" class="px-4 py-2.5 rounded-xl text-xs font-bold bg-white hover:bg-amber-50 text-amber-800 border border-amber-200 transition shadow-2xs flex items-center gap-1.5 cursor-pointer active:scale-95" title="Tải file text nạp câu hỏi vào Anki">
                      <span>⚡ Xuất bài đọc Anki (.txt)</span>
                    </button>
                  </div>

                  <div class="flex items-center gap-2">
                    ${this.currentIndex < this.questions.length - 1 ? `
                      <button type="button" id="btn-dokkai-next-bottom" class="px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-indigo-600 to-indigo-800 hover:from-indigo-700 hover:to-indigo-900 text-white shadow-md shadow-indigo-200 transition flex items-center gap-1.5 cursor-pointer active:scale-95">
                        <span>Bài tiếp theo (Bài ${this.currentIndex + 2}) ➡</span>
                      </button>
                    ` : `
                      <button type="button" id="btn-dokkai-finish-chapter" class="px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-md shadow-emerald-200 transition flex items-center gap-1.5 cursor-pointer active:scale-95">
                        <span>🎉 Trở về Kho Luyện Đề</span>
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

              <!-- Giant Countdown Timer Display -->
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

              <!-- Dock Primary Action Button (Requirement 2: No duplicate start button!) -->
              <div class="pt-2 border-t border-slate-100">
                ${
                  !this.isStarted
                    ? `
                      <div class="p-3 rounded-xl bg-slate-50 border border-dashed border-slate-200 text-center text-xs text-slate-500 font-medium">
                        <span>👈 Bấm nút ở khung bài đọc để bắt đầu tính giờ</span>
                      </div>
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
                          <button type="button" id="btn-dock-retake" class="w-full py-2.5 px-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs transition cursor-pointer flex items-center justify-center gap-1.5 shadow-2xs active:scale-95">
                            <span>🔄 Làm lại bài này</span>
                          </button>
                          <button type="button" id="btn-dock-back-hub" class="w-full py-2.5 px-3 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold text-xs border border-indigo-200 transition cursor-pointer flex items-center justify-center gap-1.5 shadow-2xs active:scale-95">
                            <span>📋 Chọn bài khác</span>
                          </button>
                          ${this.currentIndex < this.questions.length - 1 ? `
                            <button type="button" id="btn-dock-next" class="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-800 hover:from-indigo-700 hover:to-indigo-900 text-white font-bold text-xs shadow-md transition flex items-center justify-center gap-1.5 cursor-pointer active:scale-95">
                              <span>Bài tiếp theo (Bài ${this.currentIndex + 2}) ➡</span>
                            </button>
                          ` : ''}
                        </div>
                      `
                }
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

      </div>
    `;

    this.bindEvents();
    this.updateTimerDisplay();
  }

  // ==============================================================
  // EVENT BINDINGS
  // ==============================================================

  bindEvents() {
    // Modal Start Button (Single Primary trigger)
    document.getElementById('btn-dokkai-start-reading-modal')?.addEventListener('click', () => {
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

    // Back to Dokkai Hub buttons
    document.getElementById('btn-dokkai-back-hub')?.addEventListener('click', () => this.showHub());
    document.getElementById('btn-dokkai-back-hub-bottom')?.addEventListener('click', () => this.showHub());
    document.getElementById('btn-dock-back-hub')?.addEventListener('click', () => this.showHub());

    // Retake buttons
    document.getElementById('btn-dokkai-retake-top')?.addEventListener('click', () => this.retakeCurrentQuestion());
    document.getElementById('btn-dokkai-retake-bottom')?.addEventListener('click', () => this.retakeCurrentQuestion());

    // Next question buttons in Step 2
    document.getElementById('btn-dokkai-next-top')?.addEventListener('click', () => this.goToQuestion(this.currentIndex + 1));
    document.getElementById('btn-dokkai-next-bottom')?.addEventListener('click', () => this.goToQuestion(this.currentIndex + 1));

    // Finish chapter button (Returns to Hub)
    document.getElementById('btn-dokkai-finish-chapter')?.addEventListener('click', () => {
      this.stopTimer();
      if (this.app && typeof this.app.showToast === 'function') {
        this.app.showToast('🎉 Bạn đã hoàn thành các bài trong chương này!', 'success');
      }
      this.showHub();
    });

    // Anki export single dokkai question
    document.getElementById('btn-dokkai-anki-export')?.addEventListener('click', () => {
      this.exportCurrentToAnki();
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
