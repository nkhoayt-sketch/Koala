import { QuizEngine } from './quiz.js';
import { DokkaiEngine } from './dokkai.js';
import { storage } from './storage.js';

class App {
  constructor() {
    this.currentView = 'HOME'; // 'HOME' | 'TEST'
    this.currentCourse = 'n1'; // 'n1' | 'n2' | 'n1_dokkai'
    this.daysIndex = [];
    this.n2Exams = [];
    this.currentDay = 1;
    this.currentN2Exam = null;
    this.currentDokkaiChapter = null;
    this.activeN2Scope = 'vocab_grammar'; // 'vocab_grammar' | 'full'
    this.pendingN2ExamMeta = null;

    this.quizEngine = null;
    this.dokkaiEngine = null;
    this.currentQuestionIndex = 0;
    this.isSidebarCollapsed = localStorage.getItem('n1_quiz_sidebar_collapsed') === 'true';
    this.isPaletteCollapsed = false;

    this.initElements();
  }

  initElements() {
    // View navigation elements
    this.homeViewEl = document.getElementById('home-view');
    this.testViewEl = document.getElementById('test-view');
    this.btnHeaderHome = document.getElementById('btn-header-home');
    this.btnSidebarBrand = document.getElementById('btn-sidebar-brand');
    this.btnSidebarHome = document.getElementById('btn-sidebar-home');
    this.headerHomeInfo = document.getElementById('header-home-info');
    this.headerTestInfo = document.getElementById('header-test-info');
    this.headerDivider = document.getElementById('header-divider');
    this.homeHeaderControls = document.getElementById('home-header-controls');
    this.testHeaderControls = document.getElementById('test-header-controls');

    // Home Dashboard elements
    this.homeN1DaysQuicklist = document.getElementById('home-n1-days-quicklist');
    this.homeN2ReadyList = document.getElementById('home-n2-ready-list');
    this.btnHomeOpenN2Modal = document.getElementById('btn-home-open-n2-modal');

    // N2 Exam Picker Modal elements
    this.n2PickerModal = document.getElementById('n2-picker-modal');
    this.n2PickerBackdrop = document.getElementById('n2-picker-backdrop');
    this.btnCloseN2Picker = document.getElementById('btn-close-n2-picker');
    this.btnCancelN2Picker = document.getElementById('btn-cancel-n2-picker');
    this.n2PickerReadyList = document.getElementById('n2-picker-ready-list');
    this.n2PickerOtherList = document.getElementById('n2-picker-other-list');

    // Header elements
    this.headerLevelBadge = document.getElementById('header-level-badge');
    this.dayTitleEl = document.getElementById('header-day-title');
    this.dayDescEl = document.getElementById('header-day-desc');
    this.headerScopeBtn = document.getElementById('btn-change-scope');
    this.headerScopeLabel = document.getElementById('header-scope-label');
    this.progressBarFillEl = document.getElementById('progress-bar-fill');
    this.progressTextEl = document.getElementById('progress-text');
    this.btnToggleSidebar = document.getElementById('btn-toggle-sidebar');
    this.mobileMenuBtn = document.getElementById('btn-mobile-menu') || this.btnToggleSidebar;
    this.headerPaletteBtn = document.getElementById('btn-header-palette');

    // Sidebar core elements
    this.sidebarEl = document.getElementById('sidebar');
    this.sidebarBackdrop = document.getElementById('sidebar-backdrop');
    this.collapseSidebarBtn = document.getElementById('btn-collapse-sidebar');
    this.expandSidebarFloatingBtn = document.getElementById('btn-expand-sidebar-floating');
    this.toastContainer = document.getElementById('toast-container');

    // Search elements
    this.searchInput = document.getElementById('sidebar-search-input');
    this.clearSearchBtn = document.getElementById('btn-clear-search');
    this.searchEmptyState = document.getElementById('search-empty-state');

    // Palette Accordion elements
    this.paletteSection = document.getElementById('sidebar-palette-section');
    this.btnTogglePalette = document.getElementById('btn-toggle-palette');
    this.paletteBody = document.getElementById('palette-body');
    this.paletteChevron = document.getElementById('palette-chevron');
    this.paletteActiveTitle = document.getElementById('palette-active-title');
    this.paletteActiveCount = document.getElementById('palette-active-count');

    // Tree Menu lists
    this.sidebarDaysListEl = document.getElementById('sidebar-days-list');
    this.sidebarN2ListEl = document.getElementById('sidebar-n2-list');
    this.n1AvailableCountTag = document.getElementById('n1-available-count-tag');
    this.n2AvailableCountTag = document.getElementById('n2-available-count-tag');

    // Container & Mode elements
    this.quizContainerEl = document.getElementById('quiz-container');
    this.mainEl = document.getElementById('main-content');
    this.btnModePractice = document.getElementById('btn-mode-practice');
    this.btnModeExam = document.getElementById('btn-mode-exam');

    // Pre-test Modal elements (3 Checkboxes & Summary)
    this.pretestModal = document.getElementById('pretest-modal');
    this.pretestModalBackdrop = document.getElementById('pretest-modal-backdrop');
    this.btnClosePretestModal = document.getElementById('btn-close-pretest-modal');
    this.btnCancelPretest = document.getElementById('btn-cancel-pretest');
    this.btnStartPretest = document.getElementById('btn-start-pretest');
    this.pretestModalTitle = document.getElementById('pretest-modal-title');
    this.pretestModalLevel = document.getElementById('pretest-modal-level');

    // History Review Banner & Review Buttons
    this.pretestHistoryBanner = document.getElementById('pretest-history-banner');
    this.pretestHistoryDate = document.getElementById('pretest-history-date');
    this.pretestHistoryScore = document.getElementById('pretest-history-score');
    this.btnPretestReviewBanner = document.getElementById('btn-pretest-review-banner');
    this.btnPretestReviewBtn = document.getElementById('btn-pretest-review-btn');
    this.btnPretestRetake = document.getElementById('btn-pretest-retake');

    this.cbPretestVocab = document.getElementById('pretest-cb-vocab');
    this.cbPretestReading = document.getElementById('pretest-cb-reading');
    this.cbPretestListening = document.getElementById('pretest-cb-listening');
    this.cbCardVocab = document.getElementById('pretest-cb-card-vocab');
    this.cbCardReading = document.getElementById('pretest-cb-card-reading');
    this.cbCardListening = document.getElementById('pretest-cb-card-listening');
    this.pretestSummaryParts = document.getElementById('pretest-summary-parts');
    this.pretestSummaryQuestions = document.getElementById('pretest-summary-questions');
    this.pretestSummaryTime = document.getElementById('pretest-summary-time');

    this.pretestModeCardPractice = document.getElementById('pretest-mode-card-practice');
    this.pretestModeCardExam = document.getElementById('pretest-mode-card-exam');
  }

  async init() {
    this.quizEngine = new QuizEngine(this.quizContainerEl, (stats) => this.onProgressUpdate(stats));
    this.dokkaiEngine = new DokkaiEngine(this.quizContainerEl, this);

    // Restore Sidebar Collapsed state
    if (this.isSidebarCollapsed) {
      this.setSidebarCollapsed(true, false);
    }

    // Restore Mode UI
    const currentMode = this.quizEngine.mode;
    this.updateModeUI(currentMode);

    this.bindGlobalEvents();
    this.initAccordion();
    this.initSearch();

    try {
      // Load both N1 and N2 indices in parallel (independent error handling)
      const [n1Res, n2Res] = await Promise.allSettled([
        fetch('data/days-index.json'),
        fetch('data/n2-index.json')
      ]);

      // N1 data
      try {
        if (n1Res.status === 'fulfilled' && n1Res.value.ok) {
          this.daysIndex = await n1Res.value.json();
        }
      } catch (e) {
        console.warn('Không thể nạp dữ liệu N1:', e);
        this.daysIndex = [];
      }

      // N2 data
      try {
        if (n2Res.status === 'fulfilled' && n2Res.value.ok) {
          const parsed = await n2Res.value.json();
          this.n2Exams = Array.isArray(parsed) ? parsed : [];
        }
      } catch (e) {
        console.warn('Không thể nạp dữ liệu N2:', e);
        this.n2Exams = [];
      }

      // Ensure safe defaults
      if (!Array.isArray(this.daysIndex)) this.daysIndex = [];
      if (!Array.isArray(this.n2Exams)) this.n2Exams = [];

      this.renderN1List();
      this.renderN2List();
      this.renderHomeDashboard();

      // Check current URL route (/dokkai/shinkanzen or default to HOME)
      this.initRouting();
    } catch (err) {
      console.error('Lỗi khởi tạo ứng dụng:', err);
      // Ensure safe fallback so the app still loads
      if (!Array.isArray(this.daysIndex)) this.daysIndex = [];
      if (!Array.isArray(this.n2Exams)) this.n2Exams = [];
      try {
        this.renderN1List();
        this.renderN2List();
        this.renderHomeDashboard();
        this.switchView('HOME');
      } catch (innerErr) {
        console.error('Lỗi render fallback:', innerErr);
      }
      if (this.quizContainerEl) {
        this.quizContainerEl.innerHTML = `
          <div class="p-8 text-center text-rose-600 bg-rose-50 rounded-2xl border border-rose-200">
            <p class="font-bold">Đã xảy ra lỗi khi nạp dữ liệu.</p>
            <p class="text-sm text-slate-600 mt-2">${err.message}</p>
          </div>
        `;
      }
    }
  }

  initRouting() {
    window.addEventListener('popstate', () => {
      this.handleRoute();
    });
    this.handleRoute();
  }

  handleRoute() {
    const path = (window.location.pathname || '').toLowerCase();
    const hash = (window.location.hash || '').toLowerCase();

    if (path.includes('/dokkai/shinkanzen') || path.includes('/dokkai') || hash.includes('dokkai')) {
      const chapterId = (path.includes('ch02') || hash.includes('ch02')) ? 'skz_ch02' : (path.includes('ch01') || hash.includes('ch01')) ? 'skz_ch01' : 'all';
      this.openDokkaiHub(chapterId);
    } else {
      if (this.currentView !== 'HOME') {
        this.switchView('HOME');
      }
    }
  }

  initAccordion() {
    // Palette accordion toggle
    if (this.btnTogglePalette && this.paletteBody) {
      this.btnTogglePalette.addEventListener('click', () => {
        this.isPaletteCollapsed = !this.isPaletteCollapsed;
        if (this.isPaletteCollapsed) {
          this.paletteBody.classList.add('hidden');
          if (this.paletteChevron) this.paletteChevron.classList.remove('rotate-180');
        } else {
          this.paletteBody.classList.remove('hidden');
          if (this.paletteChevron) this.paletteChevron.classList.add('rotate-180');
        }
      });
    }

    // Category accordion toggles
    const categoryToggles = document.querySelectorAll('.tree-category-toggle');
    categoryToggles.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-target');
        const content = document.getElementById(targetId);
        const chevron = btn.querySelector('.tree-chevron');
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

    // Subfolder accordion toggles
    const subfolderToggles = document.querySelectorAll('.tree-subfolder-toggle');
    subfolderToggles.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-target');
        const content = document.getElementById(targetId);
        const chevron = btn.querySelector('.tree-chevron');
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

  initSearch() {
    if (!this.searchInput) return;

    this.searchInput.addEventListener('input', (e) => {
      const query = e.target.value.trim().toLowerCase();
      this.handleSearchFilter(query);
    });

    if (this.clearSearchBtn) {
      this.clearSearchBtn.addEventListener('click', () => {
        this.searchInput.value = '';
        this.handleSearchFilter('');
        this.searchInput.focus();
      });
    }
  }

  handleSearchFilter(query) {
    if (this.clearSearchBtn) {
      if (query.length > 0) {
        this.clearSearchBtn.classList.remove('hidden');
      } else {
        this.clearSearchBtn.classList.add('hidden');
      }
    }

    let matchCount = 0;

    // Filter N1 Day Items
    const n1Items = document.querySelectorAll('#sidebar-days-list li');
    n1Items.forEach(li => {
      const text = li.textContent.toLowerCase();
      if (!query || text.includes(query)) {
        li.classList.remove('hidden');
        matchCount++;
      } else {
        li.classList.add('hidden');
      }
    });

    // Filter N2 Exam Items
    const n2Items = document.querySelectorAll('#sidebar-n2-list li');
    n2Items.forEach(li => {
      const text = li.textContent.toLowerCase();
      if (!query || text.includes(query)) {
        li.classList.remove('hidden');
        matchCount++;
      } else {
        li.classList.add('hidden');
      }
    });

    // Filter Shin Kanzen Dokkai Items
    const dokkaiItems = document.querySelectorAll('#sidebar-dokkai-list li');
    dokkaiItems.forEach(li => {
      const text = li.textContent.toLowerCase();
      if (!query || text.includes(query)) {
        li.classList.remove('hidden');
        matchCount++;
      } else {
        li.classList.add('hidden');
      }
    });

    // If searching, auto-expand categories so matched results are visible
    if (query.length > 0) {
      document.querySelectorAll('.tree-category-content, .tree-subfolder-content').forEach(c => {
        c.classList.remove('hidden');
      });
      document.querySelectorAll('.tree-chevron').forEach(ch => {
        ch.classList.add('rotate-180');
      });
    }

    // Empty state
    if (this.searchEmptyState) {
      if (query.length > 0 && matchCount === 0) {
        this.searchEmptyState.classList.remove('hidden');
      } else {
        this.searchEmptyState.classList.add('hidden');
      }
    }
  }

  renderN1List() {
    if (!this.sidebarDaysListEl) return;

    if (this.n1AvailableCountTag && this.daysIndex.length > 0) {
      const availCount = this.daysIndex.filter(d => d.available).length;
      this.n1AvailableCountTag.textContent = `${availCount}/20`;
    }

    this.sidebarDaysListEl.innerHTML = this.daysIndex.map(item => {
      const isActive = this.currentCourse === 'n1' && item.day === this.currentDay;
      const isAvailable = item.available;
      const dayKey = `n1_day${String(item.day).padStart(2, '0')}`;
      const history = storage.getExamHistoryRecord(dayKey) || storage.getExamHistoryRecord(item.day);
      const isDone = !!history;

      return `
        <li>
          <button 
            type="button" 
            class="nav-tree-item w-full text-left px-3 py-2 rounded-xl transition flex items-center justify-between group ${
              isActive 
                ? 'is-active' 
                : isAvailable
                  ? 'text-slate-700 hover:bg-slate-100 hover:text-indigo-600 font-medium'
                  : 'text-slate-400 hover:bg-slate-50 cursor-pointer'
            }"
            data-day="${item.day}"
            data-available="${isAvailable}">
            <div class="flex items-center gap-2 truncate">
              <span class="inline-flex items-center justify-center w-5 h-5 rounded-md text-[11px] font-bold ${
                isActive ? 'bg-white/20 text-white' : isAvailable ? 'bg-indigo-50 text-indigo-700' : 'bg-slate-100 text-slate-400'
              }">
                ${item.day}
              </span>
              <span class="truncate text-xs font-semibold">${item.title}</span>
            </div>

            <div class="shrink-0 flex items-center gap-1.5 ml-2">
              <span class="active-indicator w-2 h-2 rounded-full hidden"></span>
              ${isDone ? `
                <span class="text-[9px] font-bold px-1.5 py-0.5 rounded-full ${isActive ? 'bg-white text-emerald-800' : 'bg-emerald-100 text-emerald-800 border border-emerald-200'}">
                  ✓ ${history.lastScore}/${history.totalQuestions}
                </span>
              ` : isAvailable ? `
                <span class="text-[9px] font-medium px-1.5 py-0.5 rounded ${isActive ? 'text-white/80' : 'text-slate-400'}">
                  Chưa làm
                </span>
              ` : `
                <span class="text-[9px] px-1 py-0.2 rounded font-normal ${
                  isActive ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-400'
                }">
                  Chờ
                </span>
              `}
            </div>
          </button>
        </li>
      `;
    }).join('');

    // Bind clicks
    const dayButtons = this.sidebarDaysListEl.querySelectorAll('.nav-tree-item');
    dayButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const day = parseInt(btn.getAttribute('data-day'), 10);
        const available = btn.getAttribute('data-available') === 'true';
        this.selectDay(day, available);
      });
    });
  }

  renderN2List() {
    if (!this.sidebarN2ListEl) return;
    if (!Array.isArray(this.n2Exams)) this.n2Exams = [];

    if (this.n2AvailableCountTag) {
      this.n2AvailableCountTag.textContent = `${this.n2Exams.length} đợt thi`;
    }

    this.sidebarN2ListEl.innerHTML = this.n2Exams.map(item => {
      const isActive = this.currentCourse === 'n2' && this.currentN2Exam && this.currentN2Exam.id === item.id;
      const isAvailable = item.available;
      const history = storage.getExamHistoryRecord(item.id);
      const isDone = !!history && ((history.overall?.totalQuestions > 0) || (history.sections && Object.values(history.sections).some(s => s && s.completed)));
      const badgeTitle = isDone ? storage.formatExamHistoryBadge(history, item) : 'Chưa làm';

      return `
        <li>
          <button 
            type="button" 
            class="nav-tree-item w-full text-left px-3 py-2 rounded-xl transition flex items-center justify-between group ${
              isActive 
                ? 'is-active' 
                : isAvailable
                  ? 'text-slate-700 hover:bg-slate-100 hover:text-indigo-600 font-medium'
                  : 'text-slate-400 hover:bg-slate-50 cursor-pointer'
            }"
            data-exam-id="${item.id}"
            data-available="${isAvailable}">
            <div class="flex items-center gap-2 truncate">
              <span class="inline-flex items-center justify-center px-1.5 py-0.5 rounded-md text-[10px] font-bold ${
                isActive ? 'bg-white/20 text-white' : 'bg-rose-50 text-rose-700 border border-rose-100'
              }">
                ${item.month < 10 ? '0' + item.month : item.month}/${item.year}
              </span>
              <span class="truncate text-xs font-semibold">${item.title}</span>
            </div>

            <div class="shrink-0 flex items-center gap-1.5 ml-2">
              <span class="active-indicator w-2 h-2 rounded-full hidden"></span>
              ${isDone ? `
                <span class="text-[9px] font-bold px-1.5 py-0.5 rounded-full ${isActive ? 'bg-white text-emerald-800' : 'bg-emerald-100 text-emerald-800 border border-emerald-200'}" title="${badgeTitle}">
                  ✓ ${history.overall?.totalScore ?? history.lastScore}/${history.overall?.totalQuestions ?? history.totalQuestions}
                </span>
              ` : `
                <span class="text-[9px] font-medium px-1.5 py-0.5 rounded ${isActive ? 'text-white/80' : 'text-slate-400'}">
                  Chưa làm
                </span>
              `}
            </div>
          </button>
        </li>
      `;
    }).join('');

    // Bind clicks
    const examButtons = this.sidebarN2ListEl.querySelectorAll('.nav-tree-item');
    examButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const examId = btn.getAttribute('data-exam-id');
        const examMeta = this.n2Exams.find(e => e.id === examId);
        if (examMeta) {
          this.openPretestModal(examMeta);
        }
      });
    });
  }

  switchView(viewName) {
    this.currentView = viewName;

    if (viewName === 'HOME') {
      // Fully hide sidebar + related elements — Home is full-width dashboard
      if (this.sidebarEl) this.sidebarEl.classList.add('!hidden');
      if (this.sidebarBackdrop) this.sidebarBackdrop.classList.add('hidden');
      if (this.expandSidebarFloatingBtn) this.expandSidebarFloatingBtn.classList.add('hidden');
      const btnToggleSidebar = document.getElementById('btn-toggle-sidebar');
      if (btnToggleSidebar) btnToggleSidebar.classList.add('hidden');
      // Remove sidebar left-padding from main content
      if (this.mainEl) {
        this.mainEl.classList.remove('lg:pl-72');
        this.mainEl.classList.add('lg:pl-0');
      }
      const bottomBar = document.getElementById('bottom-action-bar');
      if (bottomBar) {
        bottomBar.classList.remove('lg:pl-72');
        bottomBar.classList.add('lg:pl-0');
      }

      if (this.homeViewEl) this.homeViewEl.classList.remove('hidden');
      if (this.testViewEl) this.testViewEl.classList.add('hidden');
      // Hide redundant breadcrumb — logo alone is sufficient on Home
      if (this.headerHomeInfo) this.headerHomeInfo.classList.add('hidden');
      if (this.headerTestInfo) this.headerTestInfo.classList.add('hidden');
      if (this.headerDivider) this.headerDivider.classList.add('hidden');
      if (this.homeHeaderControls) this.homeHeaderControls.classList.remove('hidden');
      if (this.testHeaderControls) this.testHeaderControls.classList.add('hidden');

      // Pause quiz timer if active when viewing Home
      if (this.quizEngine) {
        this.quizEngine.pauseTimer();
      }
      if (this.dokkaiEngine) {
        this.dokkaiEngine.stopTimer();
      }

      // Reset URL route back to root if coming from Dokkai
      const currentPath = (window.location.pathname || '').toLowerCase();
      if (currentPath.includes('/dokkai') || (window.location.hash || '').includes('dokkai')) {
        try {
          history.pushState({ view: 'home' }, '', '/');
        } catch (e) {
          window.location.hash = '';
        }
      }

      // Reset sidebar palette header & stats
      if (this.paletteActiveTitle) {
        this.paletteActiveTitle.textContent = 'Chưa chọn bài thi';
      }
      if (this.paletteActiveCount) {
        this.paletteActiveCount.textContent = '--';
      }

      const paletteGrid = document.getElementById('question-palette-grid');
      if (paletteGrid) {
        paletteGrid.innerHTML = `
          <div class="col-span-5 py-6 text-center text-[11px] text-slate-400 leading-relaxed px-2">
            <span>Chọn một bài thi từ Trang Chủ hoặc Menu để xem ma trận câu hỏi</span>
          </div>
        `;
      }
      const statAnswered = document.getElementById('palette-stat-answered');
      const statFlagged = document.getElementById('palette-stat-flagged');
      const statUnanswered = document.getElementById('palette-stat-unanswered');
      if (statAnswered) statAnswered.textContent = '0';
      if (statFlagged) statFlagged.textContent = '0';
      if (statUnanswered) statUnanswered.textContent = '--';

      // Remove active highlights in sidebar tree items
      const activeNavItems = document.querySelectorAll('.nav-tree-item.is-active');
      activeNavItems.forEach(el => el.classList.remove('is-active'));

      // Smooth scroll to top
      window.scrollTo({ top: 0, behavior: 'smooth' });
      if (this.mainEl) this.mainEl.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      // viewName === 'TEST'
      // Restore sidebar visibility
      if (this.sidebarEl) this.sidebarEl.classList.remove('!hidden');
      const btnToggleSidebar = document.getElementById('btn-toggle-sidebar');
      if (btnToggleSidebar) btnToggleSidebar.classList.remove('hidden');
      // Re-apply sidebar collapsed/expanded state (uses setSidebarCollapsed to manage pl-72)
      this.setSidebarCollapsed(false, false);

      if (this.homeViewEl) this.homeViewEl.classList.add('hidden');
      if (this.testViewEl) this.testViewEl.classList.remove('hidden');
      if (this.headerHomeInfo) this.headerHomeInfo.classList.add('hidden');
      if (this.headerTestInfo) this.headerTestInfo.classList.remove('hidden');
      if (this.headerDivider) this.headerDivider.classList.remove('hidden');
      if (this.homeHeaderControls) this.homeHeaderControls.classList.add('hidden');
      
      if (this.currentCourse === 'n1_dokkai') {
        if (this.testHeaderControls) this.testHeaderControls.classList.add('hidden');
      } else {
        if (this.testHeaderControls) this.testHeaderControls.classList.remove('hidden');
      }

      // Resume timer if in exam mode and not submitted
      if (this.currentCourse !== 'n1_dokkai' && this.quizEngine && this.quizEngine.mode === 'exam' && !this.quizEngine.isSubmitted) {
        this.quizEngine.startTimer();
      }

      window.scrollTo({ top: 0, behavior: 'smooth' });
      if (this.mainEl) this.mainEl.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  renderHomeDashboard() {
    if (!Array.isArray(this.daysIndex)) this.daysIndex = [];
    if (!Array.isArray(this.n2Exams)) this.n2Exams = [];

    const n1HomeCountEl = document.getElementById('home-n1-ready-count-text');
    if (n1HomeCountEl && this.daysIndex.length > 0) {
      const availCount = this.daysIndex.filter(d => d.available).length;
      n1HomeCountEl.textContent = `${availCount}/20 Ngày đã sẵn sàng`;
    }

    const n2HomeCountBadge = document.getElementById('home-n2-ready-count-badge');
    if (n2HomeCountBadge && this.n2Exams.length > 0) {
      const availN2Count = this.n2Exams.filter(e => e.standardized || e.available).length;
      n2HomeCountBadge.textContent = `${availN2Count} đề hoàn thiện • ${this.n2Exams.length} đợt thi`;
    }

    // 1. Render N1 Days Quicklist on Card 1
    if (this.homeN1DaysQuicklist && this.daysIndex.length > 0) {
      this.homeN1DaysQuicklist.innerHTML = this.daysIndex.map(item => {
        const isAvail = item.available;
        const dayKey = `n1_day${String(item.day).padStart(2, '0')}`;
        const history = storage.getExamHistoryRecord(dayKey) || storage.getExamHistoryRecord(item.day);
        const isDone = !!history;
        return `
          <button type="button" 
                  class="btn-quick-day px-2.5 py-1.5 rounded-xl text-xs font-bold transition flex items-center gap-1.5 ${
                    isDone
                      ? 'bg-emerald-50 hover:bg-emerald-600 text-emerald-800 hover:text-white border border-emerald-200 shadow-2xs cursor-pointer active:scale-95'
                      : isAvail 
                        ? 'bg-indigo-50 hover:bg-indigo-600 text-indigo-700 hover:text-white border border-indigo-100 shadow-2xs cursor-pointer active:scale-95' 
                        : 'bg-slate-100 text-slate-400 border border-slate-200/60 cursor-not-allowed'
                  }"
                  data-day="${item.day}"
                  data-available="${isAvail}"
                  ${isAvail ? '' : 'disabled'}
                  title="${isDone ? `Đã làm: ${history.lastScore}/${history.totalQuestions} (${history.percentage}%)` : isAvail ? `Làm bài ${item.title}` : 'Đang cập nhật'}">
            <span>Ngày ${item.day}</span>
            ${isDone 
              ? `<span class="text-[10px] font-bold text-emerald-600">✓</span>` 
              : isAvail 
                ? '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>' 
                : ''}
          </button>
        `;
      }).join('');

      this.homeN1DaysQuicklist.querySelectorAll('.btn-quick-day').forEach(btn => {
        btn.addEventListener('click', () => {
          const day = parseInt(btn.getAttribute('data-day'), 10);
          const avail = btn.getAttribute('data-available') === 'true';
          if (avail) {
            this.selectDay(day, true);
          }
        });
      });
    }

    // Card 1 primary CTA button
    const btnHomeStartN1 = document.querySelector('.btn-home-start-n1');
    if (btnHomeStartN1) {
      btnHomeStartN1.addEventListener('click', () => {
        this.selectDay(1, true);
      });
    }

    // 2. Render N2 Ready List on Card 2 (Top recent 4-5 exams: 12/2025, 07/2025, 12/2024, 07/2024, 12/2023)
    if (this.homeN2ReadyList && this.n2Exams.length > 0) {
      const readyExams = this.n2Exams.filter(e => e.standardized || e.available).slice(0, 4);
      this.homeN2ReadyList.innerHTML = readyExams.map(exam => {
        const history = storage.getExamHistoryRecord(exam.id);
        const isDone = !!history && ((history.overall?.totalQuestions > 0) || (history.sections && Object.values(history.sections).some(s => s && s.completed)));
        const badgeText = isDone ? storage.formatExamHistoryBadge(history, exam) : 'Chưa làm';
        return `
          <button type="button" 
                  class="btn-home-launch-exam w-full p-2.5 rounded-xl border border-slate-200 hover:border-rose-300 bg-slate-50/80 hover:bg-rose-50/40 text-left transition flex items-center justify-between group active:scale-98"
                  data-exam-id="${exam.id}">
            <div class="flex items-center gap-2.5">
              <span class="w-7 h-7 rounded-lg ${isDone ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'} font-bold text-xs flex items-center justify-center shrink-0">
                ${exam.month < 10 ? '0' + exam.month : exam.month}
              </span>
              <div>
                <div class="text-xs font-bold text-slate-800 group-hover:text-rose-700 transition flex items-center gap-1.5">
                  <span>${exam.title}</span>
                </div>
                <div class="text-[10px] text-slate-400 mt-0.5 flex flex-wrap items-center gap-2">
                  <span>${exam.listeningCount ? `${exam.totalQuestions} câu • Đầy đủ 3 phần (có Audio 🎧)` : `${exam.totalQuestions || 56} câu • Split-View`}</span>
                  ${isDone ? `
                    <span class="inline-flex items-center gap-1 text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                      ✓ ${badgeText}
                    </span>
                  ` : `
                    <span class="inline-flex items-center text-[10px] font-medium px-1.5 py-0.2 rounded-full bg-slate-100 text-slate-500 border border-slate-200">
                      Chưa làm
                    </span>
                  `}
                </div>
              </div>
            </div>
            <span class="text-xs font-bold ${isDone ? 'text-emerald-700 group-hover:text-emerald-800' : 'text-rose-600 group-hover:text-rose-700'} group-hover:translate-x-0.5 transition flex items-center gap-1 shrink-0 ml-2">
              <span>${isDone ? 'Xem lại' : 'Làm đề'}</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </span>
          </button>
        `;
      }).join('');

      this.homeN2ReadyList.querySelectorAll('.btn-home-launch-exam').forEach(btn => {
        btn.addEventListener('click', () => {
          const examId = btn.getAttribute('data-exam-id');
          const examMeta = this.n2Exams.find(e => e.id === examId);
          if (examMeta) {
            this.openPretestModal(examMeta);
          }
        });
      });
    }

    // 3. Populate N2 Picker Modal
    if (this.n2PickerReadyList && this.n2Exams.length > 0) {
      // All standardized exams with full question set & audio (2010 - 2025)
      const readyExams = this.n2Exams.filter(e => e.standardized || e.available);
      this.n2PickerReadyList.innerHTML = readyExams.map(exam => {
        const history = storage.getExamHistoryRecord(exam.id);
        const isDone = !!history && ((history.overall?.totalQuestions > 0) || (history.sections && Object.values(history.sections).some(s => s && s.completed)));
        const badgeText = isDone ? storage.formatExamHistoryBadge(history, exam) : 'Chưa làm';
        return `
          <div class="p-3.5 sm:p-4 rounded-2xl border-2 border-rose-300 bg-gradient-to-br from-rose-50/70 via-white to-amber-50/40 shadow-xs hover:shadow-md transition flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div class="space-y-1">
              <div class="flex flex-wrap items-center gap-2">
                <span class="text-xs font-bold px-2 py-0.5 rounded-md bg-rose-600 text-white shadow-xs">
                  ${exam.month < 10 ? '0' + exam.month : exam.month}/${exam.year}
                </span>
                <span class="text-sm font-bold text-slate-900">${exam.title}</span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 border border-amber-300 shadow-xs flex items-center gap-1">
                  ⭐ Đã chuẩn hóa 100%
                </span>
                ${isDone ? `
                  <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">
                    ✓ ${badgeText}
                  </span>
                ` : `
                  <span class="text-xs font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-500 border border-slate-200">
                    Chưa làm
                  </span>
                `}
              </div>
              <p class="text-xs text-slate-600 font-medium leading-relaxed">
                ${exam.totalQuestions} câu hỏi • Đầy đủ Từ vựng, Đọc hiểu (Split-View) & Nghe hiểu (kèm Audio 🎧)
              </p>
            </div>
            <button type="button" class="btn-picker-select-exam shrink-0 px-4 py-2 rounded-xl bg-gradient-to-r from-rose-600 via-rose-700 to-red-600 hover:from-rose-700 hover:to-red-700 active:scale-95 text-white text-xs font-bold shadow-md shadow-rose-300/60 transition flex items-center justify-center gap-1.5 cursor-pointer" data-exam-id="${exam.id}">
              <span>${isDone ? 'Làm lại 🚀' : 'Làm đề này 🚀'}</span>
            </button>
          </div>
        `;
      }).join('');

      this.n2PickerReadyList.querySelectorAll('.btn-picker-select-exam').forEach(btn => {
        btn.addEventListener('click', () => {
          const examId = btn.getAttribute('data-exam-id');
          const examMeta = this.n2Exams.find(e => e.id === examId);
          this.closeN2PickerModal();
          if (examMeta) {
            this.openPretestModal(examMeta);
          }
        });
      });
    }

    if (this.n2PickerOtherList && this.n2Exams.length > 0) {
      const otherExams = this.n2Exams.filter(e => !e.standardized && !e.available);
      if (otherExams.length === 0) {
        const otherSectionContainer = this.n2PickerOtherList.closest('div');
        if (otherSectionContainer) {
          otherSectionContainer.classList.add('hidden');
        }
      }
      this.n2PickerOtherList.innerHTML = otherExams.map(exam => {
        const history = storage.getExamHistoryRecord(exam.id);
        const isDone = !!history && ((history.overall?.totalQuestions > 0) || (history.sections && Object.values(history.sections).some(s => s && s.completed)));
        const badgeText = isDone ? storage.formatExamHistoryBadge(history, exam) : 'Chưa làm';
        return `
          <div class="px-3 py-2 rounded-xl bg-white border border-slate-100 flex items-center justify-between text-xs hover:bg-slate-50/70 transition">
            <div class="flex items-center gap-2">
              <span class="font-semibold text-slate-700">${exam.title}</span>
              <span class="text-[10px] text-slate-400">(${exam.totalQuestions || 56} câu)</span>
              ${isDone ? `
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                  ✓ ${badgeText}
                </span>
              ` : `
                <span class="text-[10px] font-medium px-1.5 py-0.2 rounded bg-slate-100 text-slate-400">
                  Chưa làm
                </span>
              `}
            </div>
            <button type="button" class="btn-picker-select-exam text-[11px] font-semibold text-indigo-600 hover:text-indigo-800 px-2.5 py-1 rounded-lg bg-indigo-50 hover:bg-indigo-100 transition cursor-pointer" data-exam-id="${exam.id}">
              Thử nghiệm
            </button>
          </div>
        `;
      }).join('');

      this.n2PickerOtherList.querySelectorAll('.btn-picker-select-exam').forEach(btn => {
        btn.addEventListener('click', () => {
          const examId = btn.getAttribute('data-exam-id');
          const examMeta = this.n2Exams.find(e => e.id === examId);
          this.closeN2PickerModal();
          if (examMeta) {
            this.openPretestModal(examMeta);
          }
        });
      });
    }
  }

  openN2PickerModal() {
    if (this.n2PickerModal) {
      this.n2PickerModal.classList.remove('hidden');
    }
  }

  closeN2PickerModal() {
    if (this.n2PickerModal) {
      this.n2PickerModal.classList.add('hidden');
    }
  }

  async selectDay(day, available) {
    if (!available) {
      this.showToast(`Ngày ${day} hiện đang được cập nhật câu hỏi mới. Vui lòng chọn Ngày 1 để làm bài thử!`, 'info');
      return;
    }

    if (this.currentView === 'TEST' && this.currentDay === day && this.currentCourse === 'n1') return;

    this.currentCourse = 'n1';
    this.currentDay = day;
    this.currentN2Exam = null;
    this.currentQuestionIndex = 0;
    if (this.quizEngine) {
      this.quizEngine.currentQuestionIndex = 0;
    }

    this.switchView('TEST');
    this.renderN1List();
    this.renderN2List();
    await this.loadDay(day);

    this.toggleMobileSidebar(false);
  }

  async loadDay(dayNumber) {
    this.currentQuestionIndex = 0;
    if (this.quizEngine) {
      this.quizEngine.currentQuestionIndex = 0;
    }
    window.scrollTo({ top: 0, behavior: 'instant' });

    const dayMeta = this.daysIndex.find(d => d.day === dayNumber);
    const fileName = dayMeta && dayMeta.file ? dayMeta.file : `data/day${String(dayNumber).padStart(2, '0')}.json`;

    // Loading indicator
    this.quizContainerEl.innerHTML = `
      <div class="flex flex-col items-center justify-center py-20">
        <div class="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
        <p class="mt-4 text-sm font-medium text-slate-500">Đang tải dữ liệu ${dayMeta ? dayMeta.title : 'Ngày ' + dayNumber}...</p>
      </div>
    `;

    try {
      const res = await fetch(fileName);
      if (!res.ok) throw new Error(`Không thể tìm thấy tệp dữ liệu: ${fileName}`);
      const dayData = await res.json();

      // Update Header Info
      if (this.headerLevelBadge) {
        this.headerLevelBadge.textContent = 'N1';
        this.headerLevelBadge.className = 'px-2 py-0.5 rounded-md text-[11px] font-bold bg-indigo-100 text-indigo-700';
      }
      if (this.dayTitleEl) this.dayTitleEl.textContent = dayData.title || `第${dayNumber}日`;
      if (this.dayDescEl) this.dayDescEl.textContent = dayData.description || 'Luyện tập JLPT N1 文字・語彙・文法';
      if (this.headerScopeBtn) this.headerScopeBtn.classList.add('hidden');

      // Update Palette title
      if (this.paletteActiveTitle) {
        this.paletteActiveTitle.textContent = dayData.title || `第${dayNumber}日`;
      }

      this.quizEngine.loadDay(dayData, { scope: 'full' });

      // Highlight active tree item
      this.renderN1List();
      this.renderN2List();
    } catch (err) {
      console.error(`Lỗi tải ngày ${dayNumber}:`, err);
      this.quizContainerEl.innerHTML = `
        <div class="p-8 text-center text-rose-600 bg-rose-50 rounded-2xl border border-rose-200 max-w-lg mx-auto">
          <p class="font-bold">Chưa thể tải dữ liệu cho ngày này</p>
          <p class="text-sm text-slate-600 mt-2">${err.message}</p>
        </div>
      `;
    }
  }

  // Pre-test Modal Methods
  openPretestModal(examMeta) {
    this.pendingN2ExamMeta = examMeta;
    if (!this.pretestModal) return;

    if (this.pretestModalTitle) this.pretestModalTitle.textContent = examMeta.title;
    if (this.pretestModalLevel) this.pretestModalLevel.textContent = examMeta.level || 'JLPT N2';

    const history = storage.getExamHistoryRecord(examMeta.id);
    const hasAnyCompleted = history && history.sections && Object.values(history.sections).some(s => s && s.completed);

    // Show or hide History Review Banner & Buttons
    if (this.pretestHistoryBanner) {
      if (hasAnyCompleted) {
        this.pretestHistoryBanner.classList.remove('hidden');
        if (this.pretestHistoryDate) this.pretestHistoryDate.textContent = history.completedAt || history.overall?.lastUpdated || '--';
        if (this.pretestHistoryScore) {
          const totalScore = history.overall?.totalScore ?? history.lastScore ?? 0;
          const totalQuestions = history.overall?.totalQuestions ?? history.totalQuestions ?? 0;
          const pct = totalQuestions > 0 ? Math.round((totalScore / totalQuestions) * 100) : 0;
          this.pretestHistoryScore.textContent = `${totalScore}/${totalQuestions} (${pct}%)`;
        }

        const sectionsContainer = document.getElementById('pretest-history-sections');
        if (sectionsContainer && history.sections) {
          const secGoi = history.sections.goi_bunpou;
          const secDokkai = history.sections.dokkai;
          const secChoukai = history.sections.choukai;

          sectionsContainer.innerHTML = `
            <div class="p-2.5 rounded-xl ${secGoi?.completed ? 'bg-white border border-emerald-200' : 'bg-slate-50 border border-slate-200/70'} flex flex-col justify-between gap-1.5">
              <div>
                <div class="text-[11px] font-bold text-slate-800">1. Từ vựng & Ngữ pháp</div>
                <div class="text-xs ${secGoi?.completed ? 'font-extrabold text-emerald-700' : 'text-slate-400 font-medium'} mt-0.5">
                  ${secGoi?.completed ? `✓ ${secGoi.score}/${secGoi.total} câu` : 'Chưa làm'}
                </div>
              </div>
              ${secGoi?.completed ? `
                <button type="button" class="btn-review-section text-[10px] font-bold text-indigo-700 hover:text-indigo-900 bg-indigo-50 hover:bg-indigo-100 px-2 py-1 rounded-lg transition self-start cursor-pointer flex items-center gap-1" data-section="vocab_grammar">
                  <span>🔍 Xem lại</span>
                </button>
              ` : ''}
            </div>

            <div class="p-2.5 rounded-xl ${secDokkai?.completed ? 'bg-white border border-emerald-200' : 'bg-slate-50 border border-slate-200/70'} flex flex-col justify-between gap-1.5">
              <div>
                <div class="text-[11px] font-bold text-slate-800">2. Đọc hiểu</div>
                <div class="text-xs ${secDokkai?.completed ? 'font-extrabold text-emerald-700' : 'text-slate-400 font-medium'} mt-0.5">
                  ${secDokkai?.completed ? `✓ ${secDokkai.score}/${secDokkai.total} câu` : 'Chưa làm'}
                </div>
              </div>
              ${secDokkai?.completed ? `
                <button type="button" class="btn-review-section text-[10px] font-bold text-indigo-700 hover:text-indigo-900 bg-indigo-50 hover:bg-indigo-100 px-2 py-1 rounded-lg transition self-start cursor-pointer flex items-center gap-1" data-section="reading">
                  <span>🔍 Xem lại</span>
                </button>
              ` : ''}
            </div>

            <div class="p-2.5 rounded-xl ${secChoukai?.completed ? 'bg-white border border-emerald-200' : 'bg-slate-50 border border-slate-200/70'} flex flex-col justify-between gap-1.5">
              <div>
                <div class="text-[11px] font-bold text-slate-800">3. Nghe hiểu</div>
                <div class="text-xs ${secChoukai?.completed ? 'font-extrabold text-emerald-700' : 'text-slate-400 font-medium'} mt-0.5">
                  ${secChoukai?.completed ? `✓ ${secChoukai.score}/${secChoukai.total} câu` : 'Chưa làm'}
                </div>
              </div>
              ${secChoukai?.completed ? `
                <button type="button" class="btn-review-section text-[10px] font-bold text-indigo-700 hover:text-indigo-900 bg-indigo-50 hover:bg-indigo-100 px-2 py-1 rounded-lg transition self-start cursor-pointer flex items-center gap-1" data-section="listening">
                  <span>🔍 Xem lại</span>
                </button>
              ` : ''}
            </div>
          `;

          sectionsContainer.querySelectorAll('.btn-review-section').forEach(btn => {
            btn.addEventListener('click', (e) => {
              e.stopPropagation();
              const sec = btn.getAttribute('data-section');
              this.reviewOldExam(examMeta, {
                vocab_grammar: sec === 'vocab_grammar',
                reading: sec === 'reading',
                listening: sec === 'listening'
              });
            });
          });
        }
      } else {
        this.pretestHistoryBanner.classList.add('hidden');
      }
    }

    const vocabCountBadge = document.getElementById('pretest-vocab-count-badge');
    const vocabTimeBadge = document.getElementById('pretest-vocab-time-badge');
    const readingCountBadge = document.getElementById('pretest-reading-count-badge');
    const readingTimeBadge = document.getElementById('pretest-reading-time-badge');

    const vCount = examMeta.vocabGrammarCount || 51;
    const rCount = examMeta.readingCount || (examMeta.totalQuestions ? Math.max(0, examMeta.totalQuestions - vCount) : 5);

    if (vocabCountBadge) vocabCountBadge.textContent = `📝 ${vCount} câu hỏi`;
    if (vocabTimeBadge) vocabTimeBadge.textContent = `⏱️ Đề xuất: ${examMeta.durations?.vocab_grammar || 35} phút`;
    if (readingCountBadge) readingCountBadge.textContent = `📝 ${rCount} câu hỏi`;
    if (readingTimeBadge) readingTimeBadge.textContent = `⏱️ Thời gian: 70 phút`;

    const listeningBadge = document.getElementById('pretest-listening-count-badge');
    const listeningTag = document.getElementById('pretest-listening-tag');
    const lCount = examMeta.listeningCount || (examMeta.audio ? 30 : 0);
    if (examMeta.audio) {
      if (listeningBadge) listeningBadge.textContent = `🎧 ${lCount} câu hỏi • Sẵn sàng audio`;
      if (listeningTag) {
        listeningTag.textContent = 'Sẵn sàng audio 🎧';
        listeningTag.className = 'text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200';
      }
    } else {
      if (listeningBadge) listeningBadge.textContent = '🎧 Đang cập nhật audio';
      if (listeningTag) {
        listeningTag.textContent = 'Sắp ra mắt';
        listeningTag.className = 'text-[10px] font-semibold px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200';
      }
    }

    // USER REQUIREMENT: Default setting is ALWAYS Checkbox 1 (言語知識) checked, reading and listening unchecked
    if (this.cbPretestVocab) this.cbPretestVocab.checked = true;
    if (this.cbPretestReading) this.cbPretestReading.checked = false;
    if (this.cbPretestListening) this.cbPretestListening.checked = false;

    this.updatePretestCalculations(examMeta);

    // Mode defaults to current engine mode
    this.setPretestModeSelection(this.quizEngine ? this.quizEngine.mode || 'practice' : 'practice');

    this.pretestModal.classList.remove('hidden');
  }

  closePretestModal() {
    if (this.pretestModal) {
      this.pretestModal.classList.add('hidden');
    }
  }

  updatePretestCalculations(examMeta = this.pendingN2ExamMeta) {
    if (!this.cbPretestVocab || !this.cbPretestReading || !this.cbPretestListening) return;

    // Guard: Prevent unchecking all 3 checkboxes (at least one must remain active)
    if (!this.cbPretestVocab.checked && !this.cbPretestReading.checked && !this.cbPretestListening.checked) {
      this.cbPretestVocab.checked = true;
    }

    const hasVocab = this.cbPretestVocab.checked;
    const hasReading = this.cbPretestReading.checked;
    const hasListening = this.cbPretestListening.checked;

    // Update Checkbox Card Styling
    const activeClass = 'relative flex items-start gap-3.5 p-3.5 rounded-2xl border-2 border-indigo-600 bg-indigo-50/60 cursor-pointer transition select-none shadow-xs';
    const inactiveClass = 'relative flex items-start gap-3.5 p-3.5 rounded-2xl border-2 border-slate-200 bg-white cursor-pointer transition hover:border-slate-300 select-none';

    if (this.cbCardVocab) this.cbCardVocab.className = hasVocab ? activeClass : inactiveClass;
    if (this.cbCardReading) this.cbCardReading.className = hasReading ? activeClass : inactiveClass;
    if (this.cbCardListening) this.cbCardListening.className = hasListening ? activeClass : (inactiveClass + ' opacity-85 hover:opacity-100');

    // Calculate Question Counts
    const meta = examMeta || this.pendingN2ExamMeta || {};
    const vocabCount = meta.vocabGrammarCount || 51;
    const readingCount = meta.readingCount || (meta.totalQuestions ? Math.max(0, meta.totalQuestions - vocabCount) : 20);
    const listeningCount = meta.listeningCount || (meta.audio ? 30 : 0);

    let totalQuestions = 0;
    if (hasVocab) totalQuestions += vocabCount;
    if (hasReading) totalQuestions += readingCount;
    if (hasListening) totalQuestions += listeningCount;

    // Calculate Countdown Durations
    let durationMinutes = 35;
    let partsSummary = 'Chỉ Từ vựng & Ngữ pháp';

    if (hasVocab && hasReading && hasListening) {
      durationMinutes = 155;
      partsSummary = 'Toàn bộ bài thi (Từ vựng, Ngữ pháp, Đọc hiểu & Nghe hiểu)';
    } else if (hasVocab && hasReading) {
      durationMinutes = 105;
      partsSummary = 'Từ vựng, Ngữ pháp & Đọc hiểu (Thi viết chuẩn)';
    } else if (hasVocab && hasListening) {
      durationMinutes = 85;
      partsSummary = 'Từ vựng, Ngữ pháp & Nghe hiểu';
    } else if (hasReading && hasListening) {
      durationMinutes = 120;
      partsSummary = 'Đọc hiểu & Nghe hiểu';
    } else if (hasVocab) {
      durationMinutes = meta.durations?.vocab_grammar || 35;
      partsSummary = 'Chỉ Từ vựng & Ngữ pháp (文字・語彙・文法)';
    } else if (hasReading) {
      durationMinutes = 70;
      partsSummary = 'Chỉ làm Đọc hiểu (読解)';
    } else if (hasListening) {
      durationMinutes = 50;
      partsSummary = 'Chỉ làm Nghe hiểu (聴解)';
    }

    if (this.pretestSummaryParts) this.pretestSummaryParts.textContent = partsSummary;
    if (this.pretestSummaryQuestions) this.pretestSummaryQuestions.textContent = `${totalQuestions} câu`;
    if (this.pretestSummaryTime) this.pretestSummaryTime.textContent = `${durationMinutes} phút`;

    // Smart Footer Buttons according to Requirement 4:
    // - If selected sections are all completed -> Show "Làm lại phần đã chọn" and "Xem lại phần này", Hide "Bắt đầu làm bài"
    // - If selected sections are not yet completed -> Show "Bắt đầu làm bài", Hide "Làm lại" and "Xem lại"
    // - If combination of completed and uncompleted -> Show "Bắt đầu làm bài" (primary) and "Làm lại"
    const history = meta.id ? storage.getExamHistoryRecord(meta.id) : null;
    const secGoi = !!history?.sections?.goi_bunpou?.completed;
    const secDokkai = !!history?.sections?.dokkai?.completed;
    const secChoukai = !!history?.sections?.choukai?.completed;

    const allSelectedCompleted = 
      (!hasVocab || secGoi) && 
      (!hasReading || secDokkai) && 
      (!hasListening || secChoukai) &&
      (hasVocab || hasReading || hasListening) &&
      ((hasVocab && secGoi) || (hasReading && secDokkai) || (hasListening && secChoukai));

    const anySelectedCompleted = 
      (hasVocab && secGoi) || 
      (hasReading && secDokkai) || 
      (hasListening && secChoukai);

    if (allSelectedCompleted) {
      if (this.btnStartPretest) this.btnStartPretest.classList.add('hidden');
      if (this.btnPretestRetake) {
        this.btnPretestRetake.classList.remove('hidden');
        this.btnPretestRetake.innerHTML = `<span>🔄 Làm lại phần đã chọn</span>`;
      }
      if (this.btnPretestReviewBtn) {
        this.btnPretestReviewBtn.classList.remove('hidden');
        this.btnPretestReviewBtn.innerHTML = `<span>🔍 Xem lại phần này</span>`;
      }
    } else {
      if (this.btnStartPretest) {
        this.btnStartPretest.classList.remove('hidden');
        this.btnStartPretest.innerHTML = `<span>🚀 Bắt đầu làm bài</span>`;
      }
      if (this.btnPretestRetake) {
        if (anySelectedCompleted) {
          this.btnPretestRetake.classList.remove('hidden');
          this.btnPretestRetake.innerHTML = `<span>🔄 Làm lại phần đã chọn</span>`;
        } else {
          this.btnPretestRetake.classList.add('hidden');
        }
      }
      if (this.btnPretestReviewBtn) {
        if (anySelectedCompleted) {
          this.btnPretestReviewBtn.classList.remove('hidden');
          this.btnPretestReviewBtn.innerHTML = `<span>🔍 Xem lại phần đã xong</span>`;
        } else {
          this.btnPretestReviewBtn.classList.add('hidden');
        }
      }
    }
  }

  setPretestModeSelection(mode) {
    const practiceCard = document.getElementById('pretest-mode-card-practice');
    const examCard = document.getElementById('pretest-mode-card-exam');
    const practiceRadio = document.querySelector('input[name="pretest-mode"][value="practice"]');
    const examRadio = document.querySelector('input[name="pretest-mode"][value="exam"]');

    if (mode === 'practice') {
      if (practiceRadio) practiceRadio.checked = true;
      if (practiceCard) practiceCard.className = 'flex items-start gap-3 p-3.5 rounded-2xl border-2 border-indigo-600 bg-indigo-50/50 cursor-pointer transition select-none';
      if (examCard) examCard.className = 'flex items-start gap-3 p-3.5 rounded-2xl border-2 border-slate-200 bg-white cursor-pointer transition select-none hover:border-slate-300';
    } else {
      if (examRadio) examRadio.checked = true;
      if (examCard) examCard.className = 'flex items-start gap-3 p-3.5 rounded-2xl border-2 border-indigo-600 bg-indigo-50/50 cursor-pointer transition select-none';
      if (practiceCard) practiceCard.className = 'flex items-start gap-3 p-3.5 rounded-2xl border-2 border-slate-200 bg-white cursor-pointer transition select-none hover:border-slate-300';
    }
  }

  async confirmPretestStart() {
    const scopes = {
      vocab_grammar: this.cbPretestVocab ? this.cbPretestVocab.checked : true,
      reading: this.cbPretestReading ? this.cbPretestReading.checked : false,
      listening: this.cbPretestListening ? this.cbPretestListening.checked : false
    };
    const selectedMode = document.querySelector('input[name="pretest-mode"]:checked')?.value || 'practice';

    this.closePretestModal();
    this.currentQuestionIndex = 0;
    if (this.quizEngine) {
      this.quizEngine.currentQuestionIndex = 0;
    }
    if (this.pendingN2ExamMeta) {
      this.switchView('TEST');
      await this.loadN2Exam(this.pendingN2ExamMeta, scopes, selectedMode);
    }
  }

  async retakeExam(examMeta = this.pendingN2ExamMeta) {
    if (!examMeta) return;

    const scopes = {
      vocab_grammar: this.cbPretestVocab ? this.cbPretestVocab.checked : true,
      reading: this.cbPretestReading ? this.cbPretestReading.checked : false,
      listening: this.cbPretestListening ? this.cbPretestListening.checked : false
    };

    const sectionKeys = [];
    if (scopes.vocab_grammar) sectionKeys.push('goi_bunpou');
    if (scopes.reading) sectionKeys.push('dokkai');
    if (scopes.listening) sectionKeys.push('choukai');
    if (sectionKeys.length === 0) sectionKeys.push('goi_bunpou');

    const sectionNames = storage.getSectionDisplayNames(sectionKeys);
    const proceed = confirm(`Làm lại phần ${sectionNames}? Kết quả của các phần thi khác vẫn sẽ được giữ nguyên.`);
    if (!proceed) return;

    // 1. Reset ONLY selected sections in storage
    storage.resetExamSection(examMeta.id, sectionKeys);

    // 2. Dispatch event to update home dashboard and sidebar
    window.dispatchEvent(new CustomEvent('koala:exam-reset', { detail: { examId: examMeta.id, sections: sectionKeys } }));

    // 3. Reset quizEngine internal state if it matches this exam
    if (this.quizEngine) {
      this.quizEngine.userAnswers = {};
      this.quizEngine.userFlags = {};
      this.quizEngine.isSubmitted = false;
      this.quizEngine.scoreResult = null;
      this.quizEngine.currentQuestionIndex = 0;
    }

    this.closePretestModal();
    this.currentQuestionIndex = 0;

    const selectedMode = document.querySelector('input[name="pretest-mode"]:checked')?.value || 'practice';

    this.switchView('TEST');
    await this.loadN2Exam(examMeta, scopes, selectedMode);
    this.showToast(`Bắt đầu làm lại phần ${sectionNames} (${examMeta.title})!`, 'info');
  }

  async reviewOldExam(examMeta = this.pendingN2ExamMeta, reviewScopes = null) {
    if (!examMeta) return;
    const history = storage.getExamHistoryRecord(examMeta.id);
    this.closePretestModal();

    this.currentQuestionIndex = 0;
    if (this.quizEngine) {
      this.quizEngine.currentQuestionIndex = 0;
    }

    let scopes;
    if (reviewScopes) {
      scopes = reviewScopes;
    } else {
      // Default: review all sections that have completed: true
      const hasGoi = !!history?.sections?.goi_bunpou?.completed;
      const hasDokkai = !!history?.sections?.dokkai?.completed;
      const hasChoukai = !!history?.sections?.choukai?.completed;

      scopes = {
        vocab_grammar: hasGoi || (!hasDokkai && !hasChoukai),
        reading: hasDokkai,
        listening: hasChoukai
      };
    }

    this.switchView('TEST');
    await this.loadN2Exam(examMeta, scopes, 'practice', { reviewMode: true, historyRecord: history });
    const activeSectionKeys = [];
    if (scopes.vocab_grammar) activeSectionKeys.push('goi_bunpou');
    if (scopes.reading) activeSectionKeys.push('dokkai');
    if (scopes.listening) activeSectionKeys.push('choukai');
    const scopeNames = storage.getSectionDisplayNames(activeSectionKeys);
    this.showToast(`Đang xem lại kết quả bài làm: ${examMeta.title} (${scopeNames})`, 'info');
  }

  async loadN2Exam(examMeta, scopes = { vocab_grammar: true, reading: false, listening: false }, mode = 'practice', extraOptions = {}) {
    this.currentCourse = 'n2';
    this.currentN2Exam = examMeta;
    this.activeN2Scopes = typeof scopes === 'object'
      ? scopes
      : { vocab_grammar: scopes !== 'reading', reading: scopes === 'reading' || scopes === 'full', listening: false };
    this.currentQuestionIndex = 0;
    if (this.quizEngine) {
      this.quizEngine.currentQuestionIndex = 0;
    }
    window.scrollTo({ top: 0, behavior: 'instant' });

    // Loading indicator
    this.quizContainerEl.innerHTML = `
      <div class="flex flex-col items-center justify-center py-20">
        <div class="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
        <p class="mt-4 text-sm font-medium text-slate-500">Đang tải đề thi ${examMeta.title}...</p>
      </div>
    `;

    try {
      const res = await fetch(examMeta.file);
      if (!res.ok) throw new Error(`Không thể tìm thấy tệp đề thi: ${examMeta.file}`);
      const examData = await res.json();

      // Update Header Info
      if (this.headerLevelBadge) {
        this.headerLevelBadge.textContent = 'N2';
        this.headerLevelBadge.className = 'px-2 py-0.5 rounded-md text-[11px] font-bold bg-rose-100 text-rose-700';
      }
      if (this.dayTitleEl) this.dayTitleEl.textContent = examData.title;
      if (this.dayDescEl) this.dayDescEl.textContent = examData.description || 'Đề thi chính thức JLPT N2';

      // Load into QuizEngine with chosen scopes, mode, and extraOptions (e.g. reviewMode)
      this.quizEngine.loadDay(examData, { scopes: this.activeN2Scopes, mode, ...extraOptions });

      // Update Palette title
      if (this.paletteActiveTitle) {
        this.paletteActiveTitle.textContent = examData.title;
      }

      // Update Header Scope Button Label
      if (this.headerScopeBtn && this.headerScopeLabel) {
        this.headerScopeBtn.classList.remove('hidden');
        const questionCount = this.quizEngine.dayData.questions.length;
        if (this.activeN2Scopes.vocab_grammar && this.activeN2Scopes.reading && this.activeN2Scopes.listening) {
          this.headerScopeLabel.textContent = `Toàn bộ bài thi (${questionCount} câu + Nghe)`;
        } else if (this.activeN2Scopes.vocab_grammar && this.activeN2Scopes.reading) {
          this.headerScopeLabel.textContent = `Từ vựng, Ngữ pháp & Đọc hiểu (${questionCount} câu)`;
        } else if (this.activeN2Scopes.vocab_grammar && this.activeN2Scopes.listening) {
          this.headerScopeLabel.textContent = `Từ vựng, Ngữ pháp & Nghe (${questionCount} câu)`;
        } else if (this.activeN2Scopes.reading && this.activeN2Scopes.listening) {
          this.headerScopeLabel.textContent = `Đọc hiểu & Nghe (${questionCount} câu)`;
        } else if (this.activeN2Scopes.reading) {
          this.headerScopeLabel.textContent = `Chỉ Đọc hiểu (${questionCount} câu)`;
        } else if (this.activeN2Scopes.listening) {
          this.headerScopeLabel.textContent = `Chỉ Nghe hiểu (${questionCount} câu)`;
        } else {
          this.headerScopeLabel.textContent = `Chỉ Từ vựng & Ngữ pháp (${questionCount} câu)`;
        }
      }

      this.updateModeUI(mode);
      this.renderN1List();
      this.renderN2List();
      this.toggleMobileSidebar(false);

      if (!extraOptions.reviewMode) {
        let scopeLabel = 'Chỉ Từ vựng & Ngữ pháp';
        if (this.activeN2Scopes.vocab_grammar && this.activeN2Scopes.reading && this.activeN2Scopes.listening) scopeLabel = 'Toàn bộ bài thi (Từ vựng, Đọc hiểu & Nghe)';
        else if (this.activeN2Scopes.vocab_grammar && this.activeN2Scopes.reading) scopeLabel = 'Từ vựng, Ngữ pháp & Đọc hiểu';
        else if (this.activeN2Scopes.reading) scopeLabel = 'Chỉ Đọc hiểu';
        else if (this.activeN2Scopes.listening) scopeLabel = 'Chỉ Nghe hiểu';
        this.showToast(`Đã nạp đề ${examMeta.title} (${scopeLabel})!`, 'success');
      }
    } catch (err) {
      console.error(`Lỗi nạp đề thi N2:`, err);
      this.quizContainerEl.innerHTML = `
        <div class="p-8 text-center text-rose-600 bg-rose-50 rounded-2xl border border-rose-200 max-w-lg mx-auto">
          <p class="font-bold">Chưa thể tải dữ liệu đề thi này</p>
          <p class="text-sm text-slate-600 mt-2">${err.message}</p>
        </div>
      `;
    }
  }

  async openDokkaiHub(chapterFilter = 'all') {
    this.currentCourse = 'n1_dokkai';
    this.currentDokkaiChapter = chapterFilter;
    this.currentDay = null;
    this.currentN2Exam = null;
    this.currentQuestionIndex = 0;

    const currentPath = (window.location.pathname || '').toLowerCase();
    const targetPath = '/dokkai/shinkanzen';
    if (!currentPath.includes(targetPath)) {
      try {
        history.pushState({ view: 'dokkai_hub', chapterFilter }, '', targetPath);
      } catch (e) {
        window.location.hash = 'dokkai/shinkanzen';
      }
    }

    if (this.quizEngine) {
      this.quizEngine.pauseTimer();
      this.quizEngine.currentQuestionIndex = 0;
    }

    this.switchView('TEST');

    // Update Header Info
    if (this.headerLevelBadge) {
      this.headerLevelBadge.textContent = 'Dokkai N1';
      this.headerLevelBadge.className = 'px-2 py-0.5 rounded-md text-[11px] font-bold bg-amber-100 text-amber-800 border border-amber-300';
    }
    if (this.dayTitleEl) {
      this.dayTitleEl.textContent = 'Shin Kanzen Master 読解 N1 • Kho Luyện Đề Tự Do';
    }
    if (this.dayDescEl) {
      this.dayDescEl.textContent = 'Luyện tư duy bóc tách cấu trúc đoạn văn, nhận diện cú lật chuyển ý và phá bẫy phương án';
    }
    if (this.headerScopeBtn) {
      this.headerScopeBtn.classList.add('hidden');
    }
    if (this.paletteActiveTitle) {
      this.paletteActiveTitle.textContent = 'Shin Kanzen Dokkai N1';
    }
    if (this.paletteActiveCount) {
      this.paletteActiveCount.textContent = '8 bài tự do';
    }

    // Hide normal test header controls
    if (this.testHeaderControls) {
      this.testHeaderControls.classList.add('hidden');
    }

    // Palette grid in sidebar for Dokkai
    const paletteGrid = document.getElementById('question-palette-grid');
    if (paletteGrid) {
      paletteGrid.innerHTML = `
        <div class="col-span-5 py-5 text-center text-[11px] text-slate-500 leading-relaxed px-2">
          <span class="font-bold text-amber-700">📖 Shin Kanzen N1</span>
          <p class="text-[10px] text-slate-400 mt-1">Kho Luyện Đề Tự Do (8 bài đọc)</p>
        </div>
      `;
    }

    if (!this.dokkaiEngine) {
      this.dokkaiEngine = new DokkaiEngine(this.quizContainerEl, this);
    }

    await this.dokkaiEngine.showHub(chapterFilter);

    // Highlight active sidebar item
    document.querySelectorAll('.nav-tree-item.is-active').forEach(el => el.classList.remove('is-active'));
    const activeBtn = document.getElementById(chapterFilter === 'skz_ch02' ? 'btn-sidebar-dokkai-ch02' : chapterFilter === 'skz_ch01' ? 'btn-sidebar-dokkai-ch01' : 'btn-sidebar-dokkai-hub');
    if (activeBtn) activeBtn.classList.add('is-active');

    this.toggleMobileSidebar(false);
  }

  async loadDokkaiChapter(chapterId = 'ch01') {
    this.currentCourse = 'n1_dokkai';
    this.currentDokkaiChapter = chapterId;
    this.currentDay = null;
    this.currentN2Exam = null;
    this.currentQuestionIndex = 0;

    // Push URL route: /dokkai/shinkanzen or /dokkai/shinkanzen/ch02
    const currentPath = (window.location.pathname || '').toLowerCase();
    const targetPath = chapterId === 'ch02' ? '/dokkai/shinkanzen/ch02' : '/dokkai/shinkanzen';
    if (!currentPath.includes(targetPath)) {
      try {
        history.pushState({ view: 'dokkai', chapterId }, '', targetPath);
      } catch (e) {
        window.location.hash = `dokkai/shinkanzen/${chapterId}`;
      }
    }

    if (this.quizEngine) {
      this.quizEngine.pauseTimer();
      this.quizEngine.currentQuestionIndex = 0;
    }

    this.switchView('TEST');

    // Update Header Info
    if (this.headerLevelBadge) {
      this.headerLevelBadge.textContent = 'Dokkai N1';
      this.headerLevelBadge.className = 'px-2 py-0.5 rounded-md text-[11px] font-bold bg-amber-100 text-amber-800 border border-amber-300';
    }
    if (this.dayTitleEl) {
      this.dayTitleEl.textContent = chapterId === 'ch02' 
        ? 'Shin Kanzen Master: 第2章：言い換え・比喩' 
        : 'Shin Kanzen Master: 第1章：対比・逆接';
    }
    if (this.dayDescEl) {
      this.dayDescEl.textContent = chapterId === 'ch02'
        ? 'Cách diễn đạt tương đương & Hình ảnh ẩn dụ: Nắm bắt cách tác giả diễn giải lại luận điểm cốt lõi'
        : 'Cấu trúc tương phản & nghịch lý: Bóc tách tiền đề số đông, bắt cú lật tư duy';
    }
    if (this.headerScopeBtn) {
      this.headerScopeBtn.classList.add('hidden');
    }
    if (this.paletteActiveTitle) {
      this.paletteActiveTitle.textContent = 'Shin Kanzen Dokkai N1';
    }
    if (this.paletteActiveCount) {
      this.paletteActiveCount.textContent = chapterId === 'ch02' ? 'Chương 2 (4 bài)' : 'Chương 1 (4 bài)';
    }

    // Hide normal test header controls
    if (this.testHeaderControls) {
      this.testHeaderControls.classList.add('hidden');
    }

    // Palette grid in sidebar for Dokkai
    const paletteGrid = document.getElementById('question-palette-grid');
    if (paletteGrid) {
      paletteGrid.innerHTML = `
        <div class="col-span-5 py-5 text-center text-[11px] text-slate-500 leading-relaxed px-2">
          <span class="font-bold text-amber-700">📖 Shin Kanzen N1</span>
          <p class="text-[10px] text-slate-400 mt-1">${chapterId === 'ch02' ? 'Chương 2: 言い換え・比喩' : 'Chương 1: 対比・逆接'}</p>
        </div>
      `;
    }

    // Loading indicator
    this.quizContainerEl.innerHTML = `
      <div class="flex flex-col items-center justify-center py-20">
        <div class="w-10 h-10 border-4 border-amber-200 border-t-amber-600 rounded-full animate-spin"></div>
        <p class="mt-4 text-sm font-medium text-slate-600">Đang tải giáo trình Shin Kanzen Dokkai N1 (${chapterId === 'ch02' ? 'Chương 2' : 'Chương 1'})...</p>
      </div>
    `;

    try {
      let res = await fetch(`data/n1_dokkai/shinkanzen_${chapterId}.json`);
      if (!res.ok) {
        res = await fetch(`public/data/n1_dokkai/shinkanzen_${chapterId}.json`);
      }
      if (!res.ok) throw new Error(`Không thể tìm thấy tệp dữ liệu: shinkanzen_${chapterId}.json`);
      const chapterData = await res.json();

      if (!this.dokkaiEngine) {
        this.dokkaiEngine = new DokkaiEngine(this.quizContainerEl, this);
      }
      this.dokkaiEngine.loadChapter(chapterData);

      // Highlight active sidebar item
      document.querySelectorAll('.nav-tree-item.is-active').forEach(el => el.classList.remove('is-active'));
      const activeBtn = document.getElementById(`btn-sidebar-dokkai-${chapterId}`);
      if (activeBtn) activeBtn.classList.add('is-active');

      this.toggleMobileSidebar(false);
    } catch (err) {
      console.error('Lỗi nạp bài đọc Dokkai:', err);
      this.quizContainerEl.innerHTML = `
        <div class="p-8 text-center text-rose-600 bg-rose-50 rounded-2xl border border-rose-200 max-w-lg mx-auto">
          <p class="font-bold">Chưa thể tải dữ liệu bài đọc</p>
          <p class="text-sm text-slate-600 mt-2">${err.message}</p>
        </div>
      `;
    }
  }

  onProgressUpdate({ answered, total, percent }) {
    if (this.progressBarFillEl) {
      this.progressBarFillEl.style.width = `${percent}%`;
    }
    if (this.progressTextEl) {
      this.progressTextEl.textContent = `${answered}/${total} câu (${percent}%)`;
    }
    if (this.paletteActiveCount) {
      this.paletteActiveCount.textContent = `${answered}/${total}`;
    }
  }

  setSidebarCollapsed(collapsed, showToast = true) {
    this.isSidebarCollapsed = collapsed;
    localStorage.setItem('n1_quiz_sidebar_collapsed', collapsed ? 'true' : 'false');

    const bottomBar = document.getElementById('quiz-bottom-bar');

    if (collapsed) {
      this.sidebarEl.classList.add('lg:-translate-x-full');
      if (this.mainEl) {
        this.mainEl.classList.remove('lg:pl-72');
        this.mainEl.classList.add('lg:pl-0');
      }
      if (bottomBar) {
        bottomBar.classList.remove('lg:pl-72');
        bottomBar.classList.add('lg:pl-0');
      }
      if (this.expandSidebarFloatingBtn) {
        this.expandSidebarFloatingBtn.classList.remove('hidden');
      }
      if (showToast) {
        this.showToast('Đã thu gọn Sidebar để mở rộng tối đa khung làm bài!', 'info');
      }
    } else {
      this.sidebarEl.classList.remove('lg:-translate-x-full');
      if (this.mainEl) {
        this.mainEl.classList.remove('lg:pl-0');
        this.mainEl.classList.add('lg:pl-72');
      }
      if (bottomBar) {
        bottomBar.classList.remove('lg:pl-0');
        bottomBar.classList.add('lg:pl-72');
      }
      if (this.expandSidebarFloatingBtn) {
        this.expandSidebarFloatingBtn.classList.add('hidden');
      }
    }
  }

  updateModeUI(mode) {
    if (!this.btnModePractice || !this.btnModeExam) return;
    if (mode === 'exam') {
      this.btnModeExam.className = 'px-3 py-1 rounded-lg text-xs font-bold bg-white text-indigo-700 shadow-xs transition';
      this.btnModePractice.className = 'px-3 py-1 rounded-lg text-xs font-semibold text-slate-500 hover:text-slate-900 transition';
    } else {
      this.btnModePractice.className = 'px-3 py-1 rounded-lg text-xs font-bold bg-white text-indigo-700 shadow-xs transition';
      this.btnModeExam.className = 'px-3 py-1 rounded-lg text-xs font-semibold text-slate-500 hover:text-slate-900 transition';
    }
  }

  bindGlobalEvents() {
    // Custom toast events
    window.addEventListener('app:toast', (e) => {
      const { message, type } = e.detail;
      this.showToast(message, type);
    });

    // Home Navigation Events
    if (this.btnHeaderHome) {
      this.btnHeaderHome.addEventListener('click', () => {
        this.switchView('HOME');
      });
    }
    if (this.btnSidebarBrand) {
      this.btnSidebarBrand.addEventListener('click', () => {
        this.switchView('HOME');
        this.toggleMobileSidebar(false);
      });
    }
    if (this.btnSidebarHome) {
      this.btnSidebarHome.addEventListener('click', () => {
        this.switchView('HOME');
        this.toggleMobileSidebar(false);
      });
    }

    // Shin Kanzen Dokkai N1 Events
    const cardDokkai = document.getElementById('card-shinkanzen-dokkai');
    if (cardDokkai) {
      cardDokkai.addEventListener('click', (e) => {
        // Prevent double trigger if clicked on the child buttons
        if (e.target.closest('#btn-home-start-dokkai-ch01') || e.target.closest('#btn-home-start-dokkai-ch02') || e.target.closest('#btn-home-start-dokkai-hub')) return;
        this.openDokkaiHub('all');
      });
    }

    const btnHomeDokkaiHub = document.getElementById('btn-home-start-dokkai-hub');
    if (btnHomeDokkaiHub) {
      btnHomeDokkaiHub.addEventListener('click', () => {
        this.openDokkaiHub('all');
      });
    }

    const btnHomeDokkaiCh01 = document.getElementById('btn-home-start-dokkai-ch01');
    if (btnHomeDokkaiCh01) {
      btnHomeDokkaiCh01.addEventListener('click', () => {
        this.openDokkaiHub('skz_ch01');
      });
    }

    const btnHomeDokkaiCh02 = document.getElementById('btn-home-start-dokkai-ch02');
    if (btnHomeDokkaiCh02) {
      btnHomeDokkaiCh02.addEventListener('click', () => {
        this.openDokkaiHub('skz_ch02');
      });
    }

    const btnSidebarDokkaiHub = document.getElementById('btn-sidebar-dokkai-hub');
    if (btnSidebarDokkaiHub) {
      btnSidebarDokkaiHub.addEventListener('click', () => {
        this.openDokkaiHub('all');
      });
    }

    const btnSidebarDokkaiCh01 = document.getElementById('btn-sidebar-dokkai-ch01');
    if (btnSidebarDokkaiCh01) {
      btnSidebarDokkaiCh01.addEventListener('click', () => {
        this.openDokkaiHub('skz_ch01');
      });
    }

    const btnSidebarDokkaiCh02 = document.getElementById('btn-sidebar-dokkai-ch02');
    if (btnSidebarDokkaiCh02) {
      btnSidebarDokkaiCh02.addEventListener('click', () => {
        this.openDokkaiHub('skz_ch02');
      });
    }

    const btnHeroDokkai = document.getElementById('btn-hero-dokkai');
    if (btnHeroDokkai) {
      btnHeroDokkai.addEventListener('click', () => {
        this.openDokkaiHub('all');
      });
    }

    // N2 Exam Picker Modal Events
    if (this.btnHomeOpenN2Modal) {
      this.btnHomeOpenN2Modal.addEventListener('click', () => {
        this.openN2PickerModal();
      });
    }
    if (this.btnCloseN2Picker) {
      this.btnCloseN2Picker.addEventListener('click', () => {
        this.closeN2PickerModal();
      });
    }
    if (this.btnCancelN2Picker) {
      this.btnCancelN2Picker.addEventListener('click', () => {
        this.closeN2PickerModal();
      });
    }
    if (this.n2PickerBackdrop) {
      this.n2PickerBackdrop.addEventListener('click', () => {
        this.closeN2PickerModal();
      });
    }

    // Header Scope button (Change scope / exam mode)
    if (this.headerScopeBtn) {
      this.headerScopeBtn.addEventListener('click', () => {
        if (this.currentN2Exam) {
          this.openPretestModal(this.currentN2Exam);
        }
      });
    }

    // Pre-test Modal Events
    if (this.btnClosePretestModal) {
      this.btnClosePretestModal.addEventListener('click', () => this.closePretestModal());
    }
    if (this.btnCancelPretest) {
      this.btnCancelPretest.addEventListener('click', () => this.closePretestModal());
    }
    if (this.pretestModalBackdrop) {
      this.pretestModalBackdrop.addEventListener('click', () => this.closePretestModal());
    }
    if (this.btnStartPretest) {
      this.btnStartPretest.addEventListener('click', () => this.confirmPretestStart());
    }
    if (this.btnPretestRetake) {
      this.btnPretestRetake.addEventListener('click', () => this.retakeExam(this.pendingN2ExamMeta));
    }
    if (this.btnPretestReviewBtn) {
      this.btnPretestReviewBtn.addEventListener('click', () => {
        const scopes = {
          vocab_grammar: this.cbPretestVocab ? this.cbPretestVocab.checked : true,
          reading: this.cbPretestReading ? this.cbPretestReading.checked : false,
          listening: this.cbPretestListening ? this.cbPretestListening.checked : false
        };
        this.reviewOldExam(this.pendingN2ExamMeta, scopes);
      });
    }
    if (this.btnPretestReviewBanner) {
      this.btnPretestReviewBanner.addEventListener('click', () => this.reviewOldExam(this.pendingN2ExamMeta));
    }

    // Reactive listeners to update Home Dashboard & Sidebar upon submission/reset
    window.addEventListener('koala:exam-submitted', () => {
      this.renderHomeDashboard();
      this.renderN1List();
      this.renderN2List();
    });
    window.addEventListener('koala:exam-reset', () => {
      this.renderHomeDashboard();
      this.renderN1List();
      this.renderN2List();
    });

    // Pre-test Checkbox change events
    if (this.cbPretestVocab) {
      this.cbPretestVocab.addEventListener('change', () => this.updatePretestCalculations());
    }
    if (this.cbPretestReading) {
      this.cbPretestReading.addEventListener('change', () => this.updatePretestCalculations());
    }
    if (this.cbPretestListening) {
      this.cbPretestListening.addEventListener('change', () => this.updatePretestCalculations());
    }

    // Mode cards selection in modal
    if (this.pretestModeCardPractice) {
      this.pretestModeCardPractice.addEventListener('click', () => this.setPretestModeSelection('practice'));
    }
    if (this.pretestModeCardExam) {
      this.pretestModeCardExam.addEventListener('click', () => this.setPretestModeSelection('exam'));
    }

    // Header universal sidebar toggle button (Desktop & Mobile)
    if (this.btnToggleSidebar) {
      this.btnToggleSidebar.addEventListener('click', () => {
        if (window.innerWidth < 1024) {
          const isOpen = !this.sidebarEl.classList.contains('-translate-x-full');
          this.toggleMobileSidebar(!isOpen);
        } else {
          this.setSidebarCollapsed(!this.isSidebarCollapsed, true);
        }
      });
    }

    // Mobile sidebar toggle fallback
    if (this.mobileMenuBtn && this.mobileMenuBtn !== this.btnToggleSidebar) {
      this.mobileMenuBtn.addEventListener('click', () => {
        this.toggleMobileSidebar(true);
      });
    }

    // Header palette quick button on mobile
    if (this.headerPaletteBtn) {
      this.headerPaletteBtn.addEventListener('click', () => {
        this.setSidebarCollapsed(false, false);
        this.toggleMobileSidebar(true);
        // Expand palette if collapsed
        if (this.isPaletteCollapsed && this.btnTogglePalette) {
          this.btnTogglePalette.click();
        }
      });
    }

    if (this.sidebarBackdrop) {
      this.sidebarBackdrop.addEventListener('click', () => {
        this.toggleMobileSidebar(false);
      });
    }

    // Sidebar collapse & expand buttons
    if (this.collapseSidebarBtn) {
      this.collapseSidebarBtn.addEventListener('click', () => {
        this.setSidebarCollapsed(true, true);
      });
    }
    if (this.expandSidebarFloatingBtn) {
      this.expandSidebarFloatingBtn.addEventListener('click', () => {
        this.setSidebarCollapsed(false, true);
      });
    }

    // Mode Toggle buttons on Header
    if (this.btnModePractice) {
      this.btnModePractice.addEventListener('click', () => {
        this.quizEngine.setMode('practice');
        this.updateModeUI('practice');
      });
    }
    if (this.btnModeExam) {
      this.btnModeExam.addEventListener('click', () => {
        this.quizEngine.setMode('exam');
        this.updateModeUI('exam');
      });
    }
  }

  toggleMobileSidebar(open) {
    if (!this.sidebarEl || !this.sidebarBackdrop) return;
    if (open) {
      this.sidebarEl.classList.remove('-translate-x-full');
      this.sidebarBackdrop.classList.remove('hidden');
    } else {
      this.sidebarEl.classList.add('-translate-x-full');
      this.sidebarBackdrop.classList.add('hidden');
    }
  }

  showToast(message, type = 'info') {
    if (!this.toastContainer) return;

    const toast = document.createElement('div');
    const bgColors = {
      success: 'bg-emerald-900/95 border-emerald-500/40 text-emerald-100',
      error: 'bg-rose-900/95 border-rose-500/40 text-rose-100',
      warning: 'bg-amber-900/95 border-amber-500/40 text-amber-100',
      info: 'bg-slate-900/95 border-slate-700/80 text-white'
    };

    const icons = {
      success: `<svg class="w-4 h-4 text-emerald-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`,
      error: `<svg class="w-4 h-4 text-rose-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>`,
      warning: `<svg class="w-4 h-4 text-amber-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`,
      info: `<svg class="w-4 h-4 text-indigo-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`
    };

    toast.className = `flex items-center gap-3 px-4 py-3 rounded-2xl border backdrop-blur-md shadow-xl text-sm max-w-md pointer-events-auto animate-toast ${bgColors[type] || bgColors.info}`;
    toast.innerHTML = `
      ${icons[type] || icons.info}
      <span class="flex-1 font-medium leading-snug">${message}</span>
    `;

    this.toastContainer.appendChild(toast);

    const displayDuration = (type === 'warning' || message.length > 50) ? 5500 : 3800;

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px) scale(0.95)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, displayDuration);
  }
}

// Bootstrap app on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  const app = new App();
  app.init();
});
