/**
 * LocalStorage Manager for Koala JLPT Hub
 * Supports Section-based Exam History & Independent Retake
 */
const STORAGE_PREFIX = 'n1_quiz_v1_';

export const storage = {
  /**
   * Get answers object for a day/scope: { [questionId]: optionIndex }
   */
  getAnswers(day) {
    try {
      const raw = localStorage.getItem(`${STORAGE_PREFIX}answers_day_${day}`);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      console.error('Failed to load answers from localStorage:', e);
      return {};
    }
  },

  /**
   * Save a single answer
   */
  saveAnswer(day, questionId, optionIndex) {
    try {
      const answers = this.getAnswers(day);
      answers[questionId] = optionIndex;
      localStorage.setItem(`${STORAGE_PREFIX}answers_day_${day}`, JSON.stringify(answers));
      return answers;
    } catch (e) {
      console.error('Failed to save answer to localStorage:', e);
      return {};
    }
  },

  /**
   * Get flagged questions for a day: { [questionId]: true }
   */
  getFlags(day) {
    try {
      const raw = localStorage.getItem(`${STORAGE_PREFIX}flags_day_${day}`);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      console.error('Failed to load flags from localStorage:', e);
      return {};
    }
  },

  /**
   * Toggle flag state for a question
   */
  toggleFlag(day, questionId) {
    try {
      const flags = this.getFlags(day);
      if (flags[questionId]) {
        delete flags[questionId];
      } else {
        flags[questionId] = true;
      }
      localStorage.setItem(`${STORAGE_PREFIX}flags_day_${day}`, JSON.stringify(flags));
      return !!flags[questionId];
    } catch (e) {
      console.error('Failed to toggle flag in localStorage:', e);
      return false;
    }
  },

  /**
   * Get submission status & score for a day/scope
   */
  getSubmission(day) {
    try {
      const raw = localStorage.getItem(`${STORAGE_PREFIX}submission_day_${day}`);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      console.error('Failed to load submission status:', e);
      return null;
    }
  },

  /**
   * Save submission status & score
   */
  saveSubmission(day, data) {
    try {
      localStorage.setItem(`${STORAGE_PREFIX}submission_day_${day}`, JSON.stringify(data));
    } catch (e) {
      console.error('Failed to save submission:', e);
    }
  },

  /**
   * Reset all progress for a given day/scope key
   */
  resetDay(day) {
    try {
      localStorage.removeItem(`${STORAGE_PREFIX}answers_day_${day}`);
      localStorage.removeItem(`${STORAGE_PREFIX}flags_day_${day}`);
      localStorage.removeItem(`${STORAGE_PREFIX}submission_day_${day}`);
    } catch (e) {
      console.error('Failed to reset day:', e);
    }
  },

  /**
   * Get all exam history records from koala_exam_history
   * @returns {Object} { [examId]: record }
   */
  getExamHistory() {
    try {
      const raw = localStorage.getItem('koala_exam_history');
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      console.error('Failed to load exam history:', e);
      return {};
    }
  },

  /**
   * Normalize an exam record to ensure section-based schema
   */
  normalizeExamRecord(record, examId) {
    if (!record) return null;
    const strId = String(examId || record.examId || '');

    // Already follows new structure
    if (record.sections && record.overall) {
      return record;
    }

    // Convert legacy record to section-based structure
    const isN2 = strId.startsWith('n2');
    const sections = {};

    if (isN2) {
      const isGoi = (record.totalQuestions || 0) <= 54;
      sections.goi_bunpou = {
        completed: isGoi || (record.totalQuestions || 0) > 54,
        score: isGoi ? (record.lastScore || 0) : Math.min(record.lastScore || 0, 51),
        total: 51,
        userAnswers: record.userAnswers || {},
        completedAt: record.completedAt || null
      };
      sections.dokkai = {
        completed: !isGoi && (record.totalQuestions || 0) > 54,
        score: !isGoi ? Math.max(0, (record.lastScore || 0) - 51) : 0,
        total: 20,
        userAnswers: {},
        completedAt: !isGoi ? record.completedAt : null
      };
      sections.choukai = {
        completed: false,
        score: 0,
        total: 30,
        userAnswers: {},
        completedAt: null
      };
    } else {
      sections.general = {
        completed: true,
        score: Number(record.lastScore) || 0,
        total: Number(record.totalQuestions) || 45,
        userAnswers: record.userAnswers || {},
        completedAt: record.completedAt || null
      };
    }

    record.sections = sections;
    record.overall = {
      totalScore: Number(record.lastScore) || 0,
      totalQuestions: Number(record.totalQuestions) || 0,
      lastUpdated: record.completedAt || new Date().toISOString()
    };

    return record;
  },

  /**
   * Get history record for a specific exam
   * Supports examId variations: 'n2_2023_12', 'n2-2023-12', 'n1_day01', '1'
   * @param {string|number} examId
   */
  getExamHistoryRecord(examId) {
    if (!examId && examId !== 0) return null;
    const history = this.getExamHistory();
    const strId = String(examId);

    let rawRecord = null;
    if (history[strId]) rawRecord = history[strId];
    else if (history[strId.replace(/_/g, '-')]) rawRecord = history[strId.replace(/_/g, '-')];
    else if (history[strId.replace(/-/g, '_')]) rawRecord = history[strId.replace(/-/g, '_')];
    else if (!isNaN(examId)) {
      const dayKey = `n1_day${String(examId).padStart(2, '0')}`;
      if (history[dayKey]) rawRecord = history[dayKey];
    }

    if (!rawRecord) return null;
    return this.normalizeExamRecord(rawRecord, strId);
  },

  /**
   * Save an exam completion record into koala_exam_history (Section-based)
   * @param {string} examId
   * @param {Object} record { examId, sections, lastScore, totalQuestions, completedAt, userAnswers, flaggedQuestions }
   * @param {Object} options { isN2, scopes }
   */
  saveExamHistoryRecord(examId, record, options = {}) {
    try {
      const history = this.getExamHistory();
      const strId = String(examId);
      const underId = strId.replace(/-/g, '_');
      const hyphenId = strId.replace(/_/g, '-');

      const existing = this.getExamHistoryRecord(examId);
      const isN2 = strId.startsWith('n2') || !!(options && options.isN2);

      let sections = {};

      if (isN2) {
        sections = {
          goi_bunpou: {
            completed: false,
            score: 0,
            total: 51,
            userAnswers: {},
            completedAt: null
          },
          dokkai: {
            completed: false,
            score: 0,
            total: 20,
            userAnswers: {},
            completedAt: null
          },
          choukai: {
            completed: false,
            score: 0,
            total: 30,
            userAnswers: {},
            completedAt: null
          }
        };

        // Preserve previous sections
        if (existing && existing.sections) {
          for (const sKey of ['goi_bunpou', 'dokkai', 'choukai']) {
            if (existing.sections[sKey]) {
              sections[sKey] = { ...sections[sKey], ...existing.sections[sKey] };
            }
          }
        }

        // Apply incoming updates
        if (record.sections) {
          for (const sKey of Object.keys(record.sections)) {
            const incoming = record.sections[sKey];
            if (incoming) {
              const currentTotal = incoming.total || sections[sKey]?.total || 0;
              sections[sKey] = {
                completed: incoming.completed !== undefined ? incoming.completed : true,
                score: Number(incoming.score) || 0,
                total: currentTotal,
                userAnswers: incoming.userAnswers ? { ...(sections[sKey]?.userAnswers || {}), ...incoming.userAnswers } : (sections[sKey]?.userAnswers || {}),
                completedAt: incoming.completedAt || record.completedAt || new Date().toISOString()
              };
            }
          }
        } else if (record.lastScore !== undefined) {
          // Fallback if sections object wasn't passed directly: default to goi_bunpou
          sections.goi_bunpou = {
            completed: true,
            score: Number(record.lastScore) || 0,
            total: Number(record.totalQuestions) || 51,
            userAnswers: record.userAnswers || {},
            completedAt: record.completedAt || new Date().toISOString()
          };
        }
      } else {
        // N1 Days
        sections = {
          general: {
            completed: true,
            score: Number(record.lastScore) || 0,
            total: Number(record.totalQuestions) || 45,
            userAnswers: record.userAnswers || {},
            completedAt: record.completedAt || new Date().toISOString()
          }
        };
      }

      // Calculate overall statistics
      let totalScore = 0;
      let totalQuestions = 0;
      const combinedAnswers = {};
      let lastCompletedAt = null;

      for (const sKey of Object.keys(sections)) {
        const s = sections[sKey];
        if (s && s.completed) {
          totalScore += Number(s.score) || 0;
          totalQuestions += Number(s.total) || 0;
          if (s.userAnswers) {
            Object.assign(combinedAnswers, s.userAnswers);
          }
          if (s.completedAt) {
            lastCompletedAt = s.completedAt;
          }
        }
      }

      const overall = {
        totalScore,
        totalQuestions,
        lastUpdated: lastCompletedAt || record.completedAt || new Date().toISOString()
      };

      const cleanRecord = {
        examId: underId,
        sections,
        overall,
        // Compatibility properties
        lastScore: totalScore,
        totalQuestions: totalQuestions,
        percentage: totalQuestions > 0 ? Math.round((totalScore / totalQuestions) * 100) : 0,
        completedAt: overall.lastUpdated,
        userAnswers: combinedAnswers,
        flaggedQuestions: Array.isArray(record.flaggedQuestions) ? record.flaggedQuestions : (existing?.flaggedQuestions || [])
      };

      history[strId] = cleanRecord;
      history[underId] = cleanRecord;
      history[hyphenId] = cleanRecord;

      localStorage.setItem('koala_exam_history', JSON.stringify(history));
      return cleanRecord;
    } catch (e) {
      console.error('Failed to save exam history record:', e);
      return null;
    }
  },

  /**
   * Reset ONLY selected sections while preserving other completed sections
   * @param {string|number} examId
   * @param {string[]} sectionKeys e.g. ['dokkai'] or ['goi_bunpou']
   */
  resetExamSection(examId, sectionKeys = []) {
    try {
      const history = this.getExamHistory();
      const strId = String(examId);
      const underId = strId.replace(/-/g, '_');
      const hyphenId = strId.replace(/_/g, '-');
      const existing = this.getExamHistoryRecord(examId);

      if (!existing) return null;

      const keyMap = {
        vocab_grammar: 'goi_bunpou',
        reading: 'dokkai',
        listening: 'choukai',
        goi_bunpou: 'goi_bunpou',
        dokkai: 'dokkai',
        choukai: 'choukai'
      };

      const normalizedKeys = sectionKeys.map(k => keyMap[k] || k);

      if (existing.sections) {
        for (const sKey of normalizedKeys) {
          if (existing.sections[sKey]) {
            existing.sections[sKey] = {
              completed: false,
              score: 0,
              total: existing.sections[sKey].total || 0,
              userAnswers: {},
              completedAt: null
            };
          }
        }
      }

      // Recalculate overall
      let totalScore = 0;
      let totalQuestions = 0;
      const remainingAnswers = {};
      let lastCompletedAt = null;

      if (existing.sections) {
        for (const sKey of Object.keys(existing.sections)) {
          const s = existing.sections[sKey];
          if (s && s.completed) {
            totalScore += Number(s.score) || 0;
            totalQuestions += Number(s.total) || 0;
            if (s.userAnswers) {
              Object.assign(remainingAnswers, s.userAnswers);
            }
            if (s.completedAt) {
              lastCompletedAt = s.completedAt;
            }
          }
        }
      }

      existing.overall = {
        totalScore,
        totalQuestions,
        lastUpdated: lastCompletedAt || new Date().toISOString()
      };

      existing.lastScore = totalScore;
      existing.totalQuestions = totalQuestions;
      existing.percentage = totalQuestions > 0 ? Math.round((totalScore / totalQuestions) * 100) : 0;
      existing.completedAt = existing.overall.lastUpdated;
      existing.userAnswers = remainingAnswers;

      // Clear local storage for the reset sections
      const baseId = strId;
      for (const sKey of normalizedKeys) {
        if (sKey === 'goi_bunpou') {
          this.resetDay(`${baseId}_vocab_grammar`);
          localStorage.removeItem(`n1_quiz_exam_seconds_${baseId}_vocab_grammar`);
        } else if (sKey === 'dokkai') {
          this.resetDay(`${baseId}_reading`);
          localStorage.removeItem(`n1_quiz_exam_seconds_${baseId}_reading`);
        } else if (sKey === 'choukai') {
          this.resetDay(`${baseId}_listening`);
          localStorage.removeItem(`n1_quiz_exam_seconds_${baseId}_listening`);
        }
      }

      // If all sections are reset
      const hasAnyRemaining = existing.sections && Object.values(existing.sections).some(s => s.completed);
      if (!hasAnyRemaining) {
        this.resetDay(baseId);
        this.resetDay(`${baseId}_full`);
        localStorage.removeItem(`n1_quiz_exam_seconds_${baseId}`);
        localStorage.removeItem(`n1_quiz_exam_seconds_${baseId}_full`);
      }

      history[strId] = existing;
      history[underId] = existing;
      history[hyphenId] = existing;

      localStorage.setItem('koala_exam_history', JSON.stringify(history));
      return existing;
    } catch (e) {
      console.error('Failed to reset exam section:', e);
      return null;
    }
  },

  /**
   * Remove a specific exam record completely from koala_exam_history
   * @param {string|number} examId
   */
  removeExamHistoryRecord(examId) {
    try {
      const history = this.getExamHistory();
      const strId = String(examId);
      delete history[strId];
      delete history[strId.replace(/-/g, '_')];
      delete history[strId.replace(/_/g, '-')];
      if (!isNaN(examId)) {
        delete history[`n1_day${String(examId).padStart(2, '0')}`];
      }
      localStorage.setItem('koala_exam_history', JSON.stringify(history));
    } catch (e) {
      console.error('Failed to remove exam history record:', e);
    }
  },

  /**
   * Get human readable display names for sections
   */
  getSectionDisplayNames(keys = []) {
    const map = {
      goi_bunpou: 'Ngữ pháp (Từ vựng & Ngữ pháp)',
      vocab_grammar: 'Ngữ pháp (Từ vựng & Ngữ pháp)',
      dokkai: 'Đọc hiểu',
      reading: 'Đọc hiểu',
      choukai: 'Nghe hiểu',
      listening: 'Nghe hiểu'
    };
    if (!keys || keys.length === 0) return 'phần thi được chọn';
    const names = keys.map(k => map[k] || k);
    return names.join(', ');
  },

  /**
   * Format composite badge for dashboard cards according to Requirement 4
   * e.g. "Ngữ pháp: 42/51 | Đọc hiểu: Chưa làm"
   */
  formatExamHistoryBadge(history, examMeta = null) {
    if (!history) return 'Chưa làm';

    if (history.sections && (history.sections.goi_bunpou || history.sections.dokkai || history.sections.choukai)) {
      const gb = history.sections.goi_bunpou;
      const dk = history.sections.dokkai;
      const ck = history.sections.choukai;

      const hasAny = gb?.completed || dk?.completed || ck?.completed;
      if (!hasAny) return 'Chưa làm';

      const parts = [];
      const gbText = gb?.completed ? `${gb.score}/${gb.total}` : 'Chưa làm';
      const dkText = dk?.completed ? `${dk.score}/${dk.total}` : 'Chưa làm';

      parts.push(`Ngữ pháp: ${gbText}`);
      parts.push(`Đọc hiểu: ${dkText}`);

      if (ck?.completed || examMeta?.audio || examMeta?.listeningCount) {
        const ckText = ck?.completed ? `${ck.score}/${ck.total}` : 'Chưa làm';
        parts.push(`Nghe hiểu: ${ckText}`);
      }

      return parts.join(' | ');
    }

    if (history.lastScore !== undefined && history.totalQuestions) {
      return `Đã làm: ${history.lastScore}/${history.totalQuestions} (${history.percentage}%)`;
    }

    return 'Chưa làm';
  }
};
