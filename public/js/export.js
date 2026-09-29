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
 * Collects and classifies questions for Anki export:
 * - All wrong questions (userChoice === undefined || userChoice !== q.answer)
 * - All flagged questions (isFlagged === true), whether correct or wrong
 * Deduplicated by question ID.
 * Returns items, totalCount, wrongCount, flaggedCount.
 */
export function collectQuestionsForAnki(questions = [], userAnswers = {}, userFlags = {}) {
  const seenIds = new Set();
  const collected = [];
  let wrongCount = 0;
  let flaggedCount = 0;

  questions.forEach((q, idx) => {
    const qid = q.id !== undefined && q.id !== null ? String(q.id) : `q_${idx}`;
    const userChoice = userAnswers ? userAnswers[q.id] : undefined;
    const isAnswered = userChoice !== undefined && userChoice !== null;
    const isCorrect = isAnswered && userChoice === q.answer;
    const isWrong = !isAnswered || userChoice !== q.answer;
    const isFlagged = !!(userFlags && userFlags[q.id]);

    if (isWrong || isFlagged) {
      if (!seenIds.has(qid)) {
        seenIds.add(qid);

        let classification = 'wrong';
        let tag = 'JLPT_Wrong';
        let label = 'Câu làm sai';

        if (isFlagged && isWrong) {
          classification = 'flagged_wrong';
          tag = 'JLPT_Flagged_Wrong';
          label = 'Vừa đánh dấu khó vừa làm sai';
        } else if (isFlagged && isCorrect) {
          classification = 'flagged_correct';
          tag = 'JLPT_Flagged_Correct';
          label = 'Đánh dấu khó (làm đúng)';
        }

        if (isWrong) wrongCount++;
        if (isFlagged) flaggedCount++;

        collected.push({
          question: q,
          userChoice,
          isAnswered,
          isCorrect,
          isWrong,
          isFlagged,
          classification,
          tag,
          label
        });
      }
    }
  });

  return {
    items: collected,
    totalCount: collected.length,
    wrongCount,
    flaggedCount
  };
}

/**
 * Builds a clean, organized text report of wrong & flagged questions for Anki / study review
 */
export function buildMistakesReport(dayTitle, questions = [], userAnswers = {}, userFlags = {}, options = {}) {
  const collection = collectQuestionsForAnki(questions, userAnswers, userFlags);

  if (collection.totalCount === 0) {
    return null;
  }

  const isN2 = (options && options.level === 'N2') ||
    (typeof dayTitle === 'string' && /N2/i.test(dayTitle)) ||
    (questions && questions.length > 0 && questions[0].id && String(questions[0].id).toLowerCase().includes('n2'));
  const targetDeck = (options && options.deckName) || (isN2 ? 'Koala_JLPT::N2_Review' : 'Koala_JLPT::N1_Review');

  const dateStr = new Date().toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });

  let report = `====================================================\n`;
  report += ` BÁO CÁO ÔN TẬP ANKI - ${dayTitle}\n`;
  report += ` Khuyến nghị Deck: ${targetDeck}\n`;
  report += ` Thời gian: ${dateStr}\n`;
  report += ` Đã trích xuất: ${collection.totalCount} câu (gồm ${collection.wrongCount} câu sai và ${collection.flaggedCount} câu đánh dấu khó)\n`;
  report += `====================================================\n\n`;

  collection.items.forEach((item, idx) => {
    const q = item.question;
    const userChoiceIndex = item.userChoice;
    const userChoiceText = item.isAnswered
      ? `(${userChoiceIndex + 1}) ${q.options[userChoiceIndex] || ''}` 
      : '(Chưa chọn)';
    const correctText = `(${q.answer + 1}) ${q.options[q.answer] || ''}`;

    report += `【Câu ${q.number || idx + 1}】[${q.section || 'JLPT'}] [Tag: #${item.tag}]\n`;
    report += `• Nhãn phân loại   : 🏷️ ${item.label}\n`;
    if (q.passage) {
      report += `[Đoạn văn]:\n${stripHtml(q.passage)}\n\n`;
    }
    report += `• Câu hỏi         : ${stripHtml(q.question)}\n`;
    if (item.isCorrect) {
      report += `• Lựa chọn đã chọn : ✅ ${userChoiceText} (Làm đúng - đã đánh dấu khó)\n`;
    } else {
      report += `• Lựa chọn đã chọn : ❌ ${userChoiceText}\n`;
    }
    report += `• Đáp án chính xác : ✅ ${correctText}\n`;
    report += `• Giải thích chi tiết:\n${(q.explanation || '').trim()}\n`;
    report += `----------------------------------------------------\n\n`;
  });

  report += `\n* Mẹo học tập: Hãy nhập danh sách này vào Anki (Deck: ${targetDeck}) hoặc ôn tập lại sau 24 giờ để ghi nhớ lâu dài!`;

  return {
    text: report,
    totalCount: collection.totalCount,
    wrongCount: collection.wrongCount,
    flaggedCount: collection.flaggedCount,
    deckName: targetDeck,
    items: collection.items,
    toString() {
      return this.text;
    }
  };
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
 * Adds wrong & flagged questions to Anki deck:
 * - 'Koala_JLPT::N1_Review' for N1
 * - 'Koala_JLPT::N2_Review' for N2
 */
export async function sendMistakesToAnkiConnect(dayTitle, questions = [], userAnswers = {}, userFlags = {}, options = {}) {
  const collection = collectQuestionsForAnki(questions, userAnswers, userFlags);

  // Automatically detect level from options, title, or question IDs
  const isN2 = (options && options.level === 'N2') ||
    (typeof dayTitle === 'string' && /N2/i.test(dayTitle)) ||
    (questions && questions.length > 0 && questions[0].id && String(questions[0].id).toLowerCase().includes('n2'));

  const defaultDeck = isN2 ? 'Koala_JLPT::N2_Review' : 'Koala_JLPT::N1_Review';
  const deckName = (options && options.deckName) ? options.deckName : defaultDeck;

  if (collection.totalCount === 0) {
    return {
      success: true,
      count: 0,
      totalCount: 0,
      wrongCount: 0,
      flaggedCount: 0,
      deckName: deckName,
      message: 'no_cards'
    };
  }

  const ankiUrl = 'http://localhost:8765';

  try {
    // Step 1: Ensure deck exists (Anki creates parent deck 'Koala_JLPT' and child deck automatically via '::')
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
    const notes = collection.items.map((item) => {
      const q = item.question;
      const userChoiceIndex = item.userChoice;
      const userChoiceText = item.isAnswered
        ? `(${userChoiceIndex + 1}) ${q.options[userChoiceIndex] || ''}` 
        : '(Chưa chọn)';

      let badgeBg = '#f1f5f9';
      let badgeColor = '#475569';
      let badgeBorder = '#cbd5e1';
      let badgeIcon = '❌';

      if (item.classification === 'flagged_wrong') {
        badgeBg = '#fee2e2';
        badgeColor = '#b91c1c';
        badgeBorder = '#fca5a5';
        badgeIcon = '⚠️';
      } else if (item.classification === 'flagged_correct') {
        badgeBg = '#fef3c7';
        badgeColor = '#b45309';
        badgeBorder = '#fde68a';
        badgeIcon = '⭐';
      }

      const frontHtml = `
        <div style="font-family: 'Noto Sans JP', sans-serif; font-size: 15px; color: #1e293b; line-height: 1.8;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 12px; font-weight: bold; color: #4f46e5;">
              [${q.section || 'JLPT'}] Câu ${q.number || ''}
            </span>
            <span style="font-size: 11px; font-weight: bold; padding: 2px 8px; border-radius: 4px; background: ${badgeBg}; color: ${badgeColor}; border: 1px solid ${badgeBorder};">
              ${badgeIcon} ${item.label}
            </span>
          </div>
          ${q.passage ? `<div style="background:#f8fafc; border-left:3px solid #6366f1; padding:8px 12px; margin-bottom:12px; font-size:13px; line-height:1.7;">${q.passage}</div>` : ''}
          <div style="font-size: 17px; font-weight: 600; margin-bottom: 12px;">
            ${q.question}
          </div>
          <div style="background:#f1f5f9; padding:10px 14px; border-radius:8px;">
            <ol style="margin: 0; padding-left: 20px;">
              ${(q.options || []).map((opt) => `<li>${opt}</li>`).join('')}
            </ol>
          </div>
        </div>
      `;

      let userChoiceHtml = '';
      if (item.isCorrect) {
        userChoiceHtml = `
          <div style="font-size: 13px; color: #059669; margin-bottom: 12px; background: #ecfdf5; padding: 6px 10px; border-radius: 6px; border: 1px solid #a7f3d0;">
            ⭐ Bạn đã làm đúng: ${userChoiceText} (Được gắn cờ câu khó để ôn tập lại)
          </div>
        `;
      } else {
        userChoiceHtml = `
          <div style="font-size: 13px; color: #e11d48; margin-bottom: 12px; background: #fff1f2; padding: 6px 10px; border-radius: 6px; border: 1px solid #fecdd3;">
            ❌ Lựa chọn của bạn: ${userChoiceText}
          </div>
        `;
      }

      const backHtml = `
        <div style="font-family: 'Noto Sans JP', sans-serif; font-size: 14px; line-height: 1.8;">
          <div style="font-size: 15px; font-weight: bold; color: #059669; padding: 6px 12px; background: #ecfdf5; border-radius: 6px; margin-bottom: 10px;">
            ✅ Đáp án đúng: (${q.answer + 1}) ${q.options[q.answer] || ''}
          </div>
          ${userChoiceHtml}
          <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px; white-space: pre-line; color: #1e293b;">
            ${q.explanation || ''}
          </div>
          <div style="margin-top: 10px; font-size: 11px; color: #64748b;">
            🏷️ Nhãn thẻ: <strong>${item.tag}</strong>
          </div>
        </div>
      `;

      const noteTags = [
        'Koala_JLPT',
        isN2 ? 'JLPT_N2' : 'JLPT_N1',
        item.tag
      ];
      if (q.section) {
        noteTags.push(q.section.replace(/\s+/g, '_'));
      }
      if (q.day) {
        noteTags.push(`Day_${q.day}`);
      }

      return {
        deckName: deckName,
        modelName: 'Basic',
        fields: {
          Front: frontHtml,
          Back: backHtml
        },
        tags: noteTags
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

    const addedCount = Array.isArray(data.result) ? data.result.filter(id => id !== null).length : collection.totalCount;

    return {
      success: true,
      count: addedCount,
      totalCount: collection.totalCount,
      wrongCount: collection.wrongCount,
      flaggedCount: collection.flaggedCount,
      deckName: deckName
    };
  } catch (err) {
    console.warn('AnkiConnect API error:', err);
    return {
      success: false,
      totalCount: collection.totalCount,
      wrongCount: collection.wrongCount,
      flaggedCount: collection.flaggedCount,
      deckName: deckName,
      error: err.message || 'connection_failed'
    };
  }
}

/**
 * Generates and downloads a standard Anki TSV text file (.txt) for wrong and flagged questions.
 * Format:
 * - Column 1 (Front): Question content + passage + options (1, 2, 3, 4)
 * - Column 2 (Back): Correct answer + user choice + explanation (HTML formatted with <br>, <b>)
 * - Column 3 (Tags): Exam/Day tags + classification tags (e.g. Koala_N1_Day02, Koala_N2_Review, JLPT_Wrong)
 */
export function downloadAnkiTxtFile(dayTitle, questions = [], userAnswers = {}, userFlags = {}, options = {}) {
  const collection = collectQuestionsForAnki(questions, userAnswers, userFlags);
  if (collection.totalCount === 0) {
    return {
      success: false,
      totalCount: 0,
      wrongCount: 0,
      flaggedCount: 0
    };
  }

  const isN2 = (options && options.level === 'N2') ||
    (typeof dayTitle === 'string' && /N2/i.test(dayTitle)) ||
    (questions && questions.length > 0 && questions[0].id && String(questions[0].id).toLowerCase().includes('n2'));

  const cleanTitle = (dayTitle || '').trim();
  const dayMatch = cleanTitle.match(/(?:day|第)?0?(\d+)/i);
  const examTag = isN2
    ? 'Koala_N2_Review'
    : (dayMatch ? `Koala_N1_Day${dayMatch[1].padStart(2, '0')}` : 'Koala_N1_Review');

  const targetDeck = (options && options.deckName) || (isN2 ? 'Koala_JLPT::N2_Review' : 'Koala_JLPT::N1_Review');

  // Anki Standard Headers for automatic tab recognition, HTML rendering and tag column
  let tsvContent = `#separator:tab\n#html:true\n#tags column:3\n`;

  collection.items.forEach((item, idx) => {
    const q = item.question;

    // --- Column 1: Front (Question + Passage + Options 1-4) ---
    let frontHtml = '';
    if (q.section) {
      frontHtml += `<b>[${q.section}]</b><br>`;
    }
    if (q.passage) {
      const cleanPassage = q.passage.trim().replace(/\r?\n/g, '<br>');
      frontHtml += `<b>[Đoạn văn]:</b><br><div style="padding:8px 10px;background:#f8fafc;border-left:3px solid #6366f1;border-radius:4px;margin:6px 0;line-height:1.6;">${cleanPassage}</div><br>`;
    }
    
    const questionText = q.question || '';
    frontHtml += questionText;

    if (Array.isArray(q.options) && q.options.length > 0) {
      frontHtml += '<br><br>' + q.options.map((opt, oIdx) => `(${oIdx + 1}) ${opt}`).join('<br>');
    }

    // --- Column 2: Back (Correct Answer + User Choice + Explanation) ---
    const correctOptText = (Array.isArray(q.options) && q.options[q.answer] !== undefined)
      ? `(${q.answer + 1}) ${q.options[q.answer]}`
      : `(${q.answer + 1})`;

    let backHtml = `<b>Đáp án đúng:</b> ${correctOptText}`;

    if (item.userChoice !== undefined && item.userChoice !== null) {
      const userOptText = (Array.isArray(q.options) && q.options[item.userChoice] !== undefined)
        ? `(${item.userChoice + 1}) ${q.options[item.userChoice]}`
        : `(${item.userChoice + 1})`;
      if (item.isCorrect) {
        backHtml += `<br><b>Lựa chọn của bạn:</b> ${userOptText} (✅ Làm đúng - Đánh dấu khó 🚩)`;
      } else {
        backHtml += `<br><b>Lựa chọn của bạn:</b> ${userOptText} (❌ Làm sai)`;
      }
    } else {
      backHtml += `<br><b>Lựa chọn của bạn:</b> (Chưa chọn)`;
    }

    if (item.label) {
      backHtml += `<br><b>Phân loại:</b> ${item.label}`;
    }

    if (q.explanation && q.explanation.trim()) {
      const cleanExp = q.explanation.trim().replace(/\r?\n/g, '<br>');
      backHtml += `<br><br><b>Giải thích chi tiết:</b><br>${cleanExp}`;
    }

    // --- Column 3: Tags ---
    const tagList = [examTag, item.tag, 'Koala_JLPT'];
    const tags = tagList.filter(Boolean).join(' ');

    // Normalize: Replace literal tabs with space and literal newlines with <br> to keep strictly 1 line per card
    const cleanFront = frontHtml.replace(/\t/g, ' ').replace(/[\r\n]+/g, '<br>');
    const cleanBack = backHtml.replace(/\t/g, ' ').replace(/[\r\n]+/g, '<br>');
    const cleanTags = tags.replace(/[\t\r\n]+/g, ' ');

    tsvContent += `${cleanFront}\t${cleanBack}\t${cleanTags}\n`;
  });

  const filename = options.filename || 'Koala_Anki_Export.txt';

  // Trigger browser download via Blob
  try {
    const blob = new Blob(['\uFEFF' + tsvContent], { type: 'text/tab-separated-values;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  } catch (err) {
    console.error('Download Anki txt error:', err);
  }

  return {
    success: true,
    totalCount: collection.totalCount,
    wrongCount: collection.wrongCount,
    flaggedCount: collection.flaggedCount,
    filename,
    deckName: targetDeck
  };
}

