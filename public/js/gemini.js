/**
 * Gemini Prompt Generator and Modal Handler for Deep-dive Explanation
 */
import { copyTextToClipboard } from './export.js';

function stripHtml(html) {
  const tmp = document.createElement('DIV');
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || '';
}

/**
 * Builds a structured, high-quality prompt for Gemini / ChatGPT
 */
export function buildGeminiPrompt(q) {
  const cleanQuestion = stripHtml(q.question);
  const correctOptionText = q.options[q.answer];

  let prompt = `Bạn là một chuyên gia khảo thí và giáo viên luyện thi tiếng Nhật JLPT N1 cao cấp. Hãy giúp tôi phân tích chuyên sâu câu hỏi luyện thi N1 sau đây:\n\n`;
  prompt += `【PHẦN THI】: ${q.section}\n`;
  if (q.passage) {
    prompt += `【NGỮ CẢNH ĐOẠN VĂN】:\n${stripHtml(q.passage)}\n\n`;
  }
  prompt += `【CÂU HỎI TIẾNG NHẬT】: ${cleanQuestion}\n`;
  prompt += `【CÁC LỰA CHỌN】:\n`;
  q.options.forEach((opt, idx) => {
    prompt += `  ${idx + 1}. ${opt}\n`;
  });
  prompt += `\n【ĐÁP ÁN ĐÚNG】: Lựa chọn (${q.answer + 1}) ${correctOptionText}\n\n`;
  prompt += `【YÊU CẦU GIẢI THÍCH CHI TIẾT】:\n`;
  prompt += `1. Giải thích cụ thể TẠI SAO 3 phương án còn lại là SAI (chỉ rõ sai do sai nghĩa, sai sắc thái, sai cách kết hợp ngữ pháp hay sai văn cảnh).\n`;
  prompt += `2. Phân tích sắc thái chuyên sâu của điểm ngữ pháp / từ vựng N1 này (ngữ cảnh sử dụng trang trọng, văn phong viết, hoặc bẫy đề thi JLPT N1 thường lừa thí sinh).\n`;
  prompt += `3. Cho thêm 1 ví dụ thực tế tương tự (kèm phiên âm Hiragana và dịch nghĩa) để tôi có thể ghi nhớ lâu và tự tin áp dụng trong bài thi thật.\n`;

  return prompt;
}

/**
 * Generates an instant quick-analysis text based on the question's explanation and wrong options
 */
export function buildInstantExplanation(q) {
  const wrongOptions = q.options
    .map((opt, idx) => ({ text: opt, index: idx + 1 }))
    .filter((_, idx) => idx !== q.answer);

  return {
    correctOption: `(${q.answer + 1}) ${q.options[q.answer]}`,
    wrongOptions: wrongOptions,
    summary: q.explanation
  };
}

/**
 * Modal UI Controller for Gemini Explanation
 */
export class GeminiModal {
  constructor() {
    this.modalEl = document.getElementById('gemini-modal');
    this.backdropEl = document.getElementById('gemini-modal-backdrop');
    this.closeBtn = document.getElementById('btn-close-gemini-modal');
    this.copyPromptBtn = document.getElementById('btn-copy-gemini-prompt');
    this.openWebBtn = document.getElementById('btn-open-gemini-web');
    this.promptTextarea = document.getElementById('gemini-prompt-text');
    this.modalQuestionNumber = document.getElementById('gemini-modal-q-num');
    this.modalSection = document.getElementById('gemini-modal-section');
    this.instantAnalysisEl = document.getElementById('gemini-instant-analysis');

    this.currentPrompt = '';
    this.bindEvents();
  }

  bindEvents() {
    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => this.close());
    }
    if (this.backdropEl) {
      this.backdropEl.addEventListener('click', () => this.close());
    }

    // Escape key closes modal
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !this.modalEl.classList.contains('hidden')) {
        this.close();
      }
    });

    // Copy Prompt
    if (this.copyPromptBtn) {
      this.copyPromptBtn.addEventListener('click', async () => {
        if (!this.currentPrompt) return;
        const ok = await copyTextToClipboard(this.currentPrompt);
        if (ok) {
          window.dispatchEvent(new CustomEvent('app:toast', {
            detail: { message: 'Đã sao chép Prompt & Câu hỏi vào Clipboard! Bạn có thể dán vào Gemini ngay.', type: 'success' }
          }));
        }
      });
    }

    // Open Gemini Web
    if (this.openWebBtn) {
      this.openWebBtn.addEventListener('click', () => {
        window.open('https://gemini.google.com/app', '_blank', 'noopener,noreferrer');
      });
    }
  }

  open(question) {
    if (!this.modalEl) return;

    this.currentPrompt = buildGeminiPrompt(question);

    if (this.modalQuestionNumber) {
      this.modalQuestionNumber.textContent = `Câu ${question.number}`;
    }
    if (this.modalSection) {
      this.modalSection.textContent = question.section;
    }
    if (this.promptTextarea) {
      this.promptTextarea.value = this.currentPrompt;
    }

    // Populate Instant Analysis Box
    if (this.instantAnalysisEl) {
      const instant = buildInstantExplanation(question);
      this.instantAnalysisEl.innerHTML = `
        <div class="space-y-3">
          <div class="p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-xs">
            <span class="font-bold text-emerald-800">✅ Đáp án chính xác:</span>
            <span class="font-jp text-emerald-950 ml-1.5 font-semibold">${instant.correctOption}</span>
          </div>

          <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
            <span class="font-bold text-slate-700">❌ 3 phương án còn lại cần phân tích sâu:</span>
            <div class="flex flex-wrap gap-1.5 mt-1.5">
              ${instant.wrongOptions.map(opt => `
                <span class="px-2 py-0.5 rounded bg-rose-50 text-rose-700 border border-rose-200 font-jp font-medium">
                  (${opt.index}) ${opt.text}
                </span>
              `).join('')}
            </div>
          </div>

          <div class="p-3 bg-amber-50 rounded-xl border border-amber-200 text-xs">
            <span class="font-bold text-amber-900 block mb-1">💡 Tóm tắt kiến thức cốt lõi:</span>
            <p class="font-jp text-slate-800 leading-relaxed whitespace-pre-line">${instant.summary}</p>
          </div>
        </div>
      `;
    }

    this.modalEl.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  }

  close() {
    if (!this.modalEl) return;
    this.modalEl.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }
}
