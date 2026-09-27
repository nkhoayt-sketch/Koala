/**
 * Export and Clipboard utility for wrong answers report & AnkiConnect API
 */

/**
 * Strips HTML tags like <u> or <b> from string for clean text export
 */
export function stripHtml(html) {
  if (!html) return '';
  const tmp = document.createElement('DIV');
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || '';
}

/**
 * Builds a clean, organized text report of wrong answers
 */
export function buildMistakesReport(dayTitle, questions, userAnswers) {
  const wrongQuestions = questions.filter(q => {
    const userChoice = userAnswers[q.id];
    return userChoice === undefined || userChoice !== q.answer;
  });

  if (wrongQuestions.length === 0) {
    return null;
  }

  const dateStr = new Date().toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });

  let report = `====================================================\n`;
  report += ` BÁO CÁO CÂU LÀM SAI - ${dayTitle}\n`;
  report += ` Thời gian: ${dateStr}\n`;
  report += ` Số câu làm sai: ${wrongQuestions.length}/${questions.length} câu\n`;
  report += `====================================================\n\n`;

  wrongQuestions.forEach((q, idx) => {
    const userChoiceIndex = userAnswers[q.id];
    const userChoiceText = userChoiceIndex !== undefined 
      ? `(${userChoiceIndex + 1}) ${q.options[userChoiceIndex]}` 
      : '(Chưa chọn)';
    const correctText = `(${q.answer + 1}) ${q.options[q.answer]}`;

    report += `【Câu ${q.number || idx + 1}】[${q.section}]\n`;
    if (q.passage) {
      report += `[Đoạn văn]:\n${stripHtml(q.passage)}\n\n`;
    }
    report += `• Câu hỏi: ${stripHtml(q.question)}\n`;
    report += `• Lựa chọn đã chọn : ❌ ${userChoiceText}\n`;
    report += `• Đáp án chính xác : ✅ ${correctText}\n`;
    report += `• Giải thích chi tiết:\n${q.explanation.trim()}\n`;
    report += `----------------------------------------------------\n\n`;
  });

  report += `\n* Mẹo học tập: Hãy nhập danh sách này vào Anki hoặc ôn tập lại sau 24 giờ để ghi nhớ lâu dài!`;

  return report;
}

/**
 * Copies text string to clipboard with modern API and legacy fallback
 */
export async function copyTextToClipboard(text) {
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      console.warn('navigator.clipboard failed, trying fallback...', err);
    }
  }

  // Fallback for older browsers or non-https localhost
  const textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.style.position = 'fixed';
  textArea.style.left = '-999999px';
  textArea.style.top = '-999999px';
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    const successful = document.execCommand('copy');
    document.body.removeChild(textArea);
    return successful;
  } catch (err) {
    document.body.removeChild(textArea);
    console.error('execCommand copy failed:', err);
    return false;
  }
}

/**
 * Direct Integration with AnkiConnect API (http://localhost:8765)
 * Adds all wrong questions directly to Anki deck 'JLPT N1 Weakness'
 */
export async function sendMistakesToAnkiConnect(dayTitle, questions, userAnswers) {
  const wrongQuestions = questions.filter(q => {
    const userChoice = userAnswers[q.id];
    return userChoice === undefined || userChoice !== q.answer;
  });

  if (wrongQuestions.length === 0) {
    return { success: true, count: 0, message: 'no_mistakes' };
  }

  const ankiUrl = 'http://localhost:8765';
  const deckName = 'JLPT N1 Weakness';

  try {
    // Step 1: Ensure deck exists
    await fetch(ankiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'createDeck',
        version: 6,
        params: { deck: deckName }
      })
    });

    // Step 2: Build Notes array
    const notes = wrongQuestions.map((q) => {
      const userChoiceIndex = userAnswers[q.id];
      const userChoiceText = userChoiceIndex !== undefined 
        ? `(${userChoiceIndex + 1}) ${q.options[userChoiceIndex]}` 
        : '(Chưa chọn)';

      const frontHtml = `
        <div style="font-family: 'Noto Sans JP', sans-serif; font-size: 15px; color: #1e293b; line-height: 1.8;">
          <div style="font-size: 12px; font-weight: bold; color: #4f46e5; margin-bottom: 8px;">
            [${q.section}] Câu ${q.number}
          </div>
          ${q.passage ? `<div style="background:#f8fafc; border-left:3px solid #6366f1; padding:8px 12px; margin-bottom:12px; font-size:13px; line-height:1.7;">${q.passage}</div>` : ''}
          <div style="font-size: 17px; font-weight: 600; margin-bottom: 12px;">
            ${q.question}
          </div>
          <div style="background:#f1f5f9; padding:10px 14px; border-radius:8px;">
            <ol style="margin: 0; padding-left: 20px;">
              ${q.options.map((opt, i) => `<li>${opt}</li>`).join('')}
            </ol>
          </div>
        </div>
      `;

      const backHtml = `
        <div style="font-family: 'Noto Sans JP', sans-serif; font-size: 14px; line-height: 1.8;">
          <div style="font-size: 15px; font-weight: bold; color: #059669; padding: 6px 12px; background: #ecfdf5; border-radius: 6px; margin-bottom: 10px;">
            ✅ Đáp án đúng: (${q.answer + 1}) ${q.options[q.answer]}
          </div>
          <div style="font-size: 13px; color: #e11d48; margin-bottom: 12px;">
            ❌ Lựa chọn của bạn: ${userChoiceText}
          </div>
          <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px; white-space: pre-line; color: #1e293b;">
            ${q.explanation}
          </div>
        </div>
      `;

      return {
        deckName: deckName,
        modelName: 'Basic',
        fields: {
          Front: frontHtml,
          Back: backHtml
        },
        tags: ['JLPT_N1', '20Ngay_N1', 'Weakness', `Day_${q.day || 1}`]
      };
    });

    // Step 3: Send notes to Anki
    const response = await fetch(ankiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'addNotes',
        version: 6,
        params: { notes }
      })
    });

    if (!response.ok) {
      throw new Error(`AnkiConnect returned status ${response.status}`);
    }

    const data = await response.json();
    if (data.error) {
      throw new Error(data.error);
    }

    const addedCount = Array.isArray(data.result) ? data.result.filter(id => id !== null).length : wrongQuestions.length;

    return {
      success: true,
      count: addedCount,
      totalMistakes: wrongQuestions.length,
      deckName: deckName
    };
  } catch (err) {
    console.warn('AnkiConnect API error:', err);
    return {
      success: false,
      error: err.message || 'connection_failed'
    };
  }
}
