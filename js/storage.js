/**
 * LocalStorage Manager for N1 Quiz
 */
const STORAGE_PREFIX = 'n1_quiz_v1_';

export const storage = {
  /**
   * Get answers object for a day: { [questionId]: optionIndex }
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
   * Get submission status & score for a day
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
   * Reset all progress for a given day
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
   * Get history record for a specific exam
   * Supports examId variations like 'n2_2023_12' or 'n2-2023-12' or 'n1_day01' or '1'
   * @param {string|number} examId
   */
  getExamHistoryRecord(examId) {
    if (!examId && examId !== 0) return null;
    const history = this.getExamHistory();
    const strId = String(examId);

    if (history[strId]) return history[strId];

    const hyphenId = strId.replace(/_/g, '-');
    if (history[hyphenId]) return history[hyphenId];

    const underId = strId.replace(/-/g, '_');
    if (history[underId]) return history[underId];

    // Day numeric mapping e.g. 1 -> n1_day01
    if (!isNaN(examId)) {
      const dayKey = `n1_day${String(examId).padStart(2, '0')}`;
      if (history[dayKey]) return history[dayKey];
    }

    return null;
  },

  /**
   * Save an exam completion record into koala_exam_history
   * @param {string} examId
   * @param {Object} record { examId, lastScore, totalQuestions, percentage, completedAt, userAnswers, flaggedQuestions }
   */
  saveExamHistoryRecord(examId, record) {
    try {
      const history = this.getExamHistory();
      const strId = String(examId);
      const cleanRecord = {
        examId: strId,
        lastScore: Number(record.lastScore) || 0,
        totalQuestions: Number(record.totalQuestions) || 0,
        percentage: Number(record.percentage) || 0,
        completedAt: record.completedAt || '',
        userAnswers: record.userAnswers || {},
        flaggedQuestions: Array.isArray(record.flaggedQuestions) ? record.flaggedQuestions : []
      };

      history[strId] = cleanRecord;
      const underId = strId.replace(/-/g, '_');
      history[underId] = cleanRecord;
      const hyphenId = strId.replace(/_/g, '-');
      history[hyphenId] = cleanRecord;

      localStorage.setItem('koala_exam_history', JSON.stringify(history));
      return cleanRecord;
    } catch (e) {
      console.error('Failed to save exam history record:', e);
      return null;
    }
  },

  /**
   * Remove a specific exam record from koala_exam_history
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
  }
};
