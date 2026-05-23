<<<<<<< HEAD
import { useEffect, useMemo, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { getQuestions, submitResponses } from '../services/api';
=======
import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import api, { submitResponses } from '../services/api';
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096

export default function AssessmentPage() {
  const { id } = useParams();
  const navigate = useNavigate();
<<<<<<< HEAD

=======
  const location = useLocation();
  
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [scenario, setScenario] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
<<<<<<< HEAD
  const [errors, setErrors] = useState({});
  const [globalError, setGlobalError] = useState('');
=======
  // State to hold validation errors: { [question_id]: "error message" }
  const [errors, setErrors] = useState(location.state?.validationErrors || {});
  const [globalError, setGlobalError] = useState(location.state?.globalError || '');
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096

  useEffect(() => {
    // If data was passed via router state (from LandingPage or LoadingPage bounce-back), use it directly
    if (location.state?.scenario && location.state?.questions) {
      setScenario(location.state.scenario);
      setQuestions(location.state.questions);
      
      // Initialize answers state
      const initialAnswers = {};
      location.state.questions.forEach(q => {
        initialAnswers[q.id] = '';
      });
      setAnswers(initialAnswers);
      setLoading(false);
      return;
    }

    // Fallback: fetch from API if no state was passed (e.g. direct URL navigation)
    const fetchQuestions = async () => {
      try {
<<<<<<< HEAD
        const data = await getQuestions(id);
        setScenario(data.scenario);
        setQuestions(data.questions);

=======
        const response = await api.get(`/api/assessment/${id}/questions/`);
        setScenario(response.data.scenario);
        setQuestions(response.data.questions);
        
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
        const initialAnswers = {};
        data.questions.forEach((question) => {
          initialAnswers[question.id] = '';
        });
        setAnswers(initialAnswers);
      } catch {
        setGlobalError('Failed to load assessment. It may not exist.');
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [id]);

  const currentQuestion = questions[currentIndex];
  const answeredCount = useMemo(
    () => questions.filter((question) => (answers[question.id] || '').trim().length > 0).length,
    [answers, questions],
  );
  const progress = questions.length ? ((currentIndex + 1) / questions.length) * 100 : 0;

  const handleAnswerChange = (questionId, text) => {
    setAnswers((previous) => ({ ...previous, [questionId]: text }));
    if (errors[questionId]) {
      setErrors((previous) => ({ ...previous, [questionId]: null }));
    }
  };

  const goToPrevious = () => {
    setGlobalError('');
    setCurrentIndex((index) => Math.max(0, index - 1));
  };

  const goToNext = () => {
    setGlobalError('');
    setCurrentIndex((index) => Math.min(questions.length - 1, index + 1));
  };

  const goToQuestion = (index) => {
    setGlobalError('');
    setCurrentIndex(index);
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setErrors({});
    setGlobalError('');

    const formattedResponses = questions.map((question) => ({
      question_id: question.id,
      user_answer: answers[question.id] || '',
    }));

<<<<<<< HEAD
    try {
      await submitResponses(id, formattedResponses);
      navigate(`/loading/${id}`);
    } catch (err) {
      if (err.response && err.response.status === 400 && err.response.data.details) {
        const validationErrors = {};
        err.response.data.details.forEach((detail) => {
          validationErrors[detail.question_id] = detail.message;
        });
        setErrors(validationErrors);

        const firstInvalidIndex = questions.findIndex((question) => validationErrors[question.id]);
        if (firstInvalidIndex >= 0) {
          setCurrentIndex(firstInvalidIndex);
        }

        setGlobalError('Some responses need attention before submission.');
      } else {
        setGlobalError('Failed to submit responses. Please try again.');
      }
    } finally {
      setSubmitting(false);
    }
=======
    // Instantly navigate to the Loading page with the responses. 
    // The Loading page will handle the actual API call!
    navigate(`/loading/${id}`, { state: { formattedResponses, scenario, questions } });
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
  };

  if (loading) {
    return (
      <div className="assessment-loading">
        <div className="spinner" />
      </div>
    );
  }

  if (globalError && !scenario) {
    return (
      <div className="assessment-loading">
        <div className="assessment-error">{globalError}</div>
      </div>
    );
  }

  return (
    <main className="assessment-shell">
      <section className="scenario-panel">
        <p className="section-kicker">Scenario</p>
        <h1>Your situation</h1>
        <p>{scenario?.text}</p>
      </section>

      <section className="question-flow-panel">
        <div className="flow-topline">
          <div>
            <p className="section-kicker">Question {currentIndex + 1} of {questions.length}</p>
            <h2>Answer one step at a time</h2>
          </div>
          <div className="answer-count">{answeredCount}/{questions.length}</div>
        </div>

        <div className="progress-track" aria-hidden="true">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>

<<<<<<< HEAD
        <div className="question-jump-list" aria-label="Question navigation">
          {questions.map((question, index) => {
            const hasAnswer = (answers[question.id] || '').trim().length > 0;
            const hasError = Boolean(errors[question.id]);
            const isActive = index === currentIndex;

            return (
              <button
                key={question.id}
                type="button"
                className={[
                  'question-jump-button',
                  isActive ? 'active' : '',
                  hasAnswer ? 'answered' : '',
                  hasError ? 'has-error' : '',
                ].filter(Boolean).join(' ')}
                onClick={() => goToQuestion(index)}
                disabled={submitting}
                aria-current={isActive ? 'step' : undefined}
                aria-label={`Go to question ${index + 1}`}
              >
                {index + 1}
              </button>
            );
          })}
        </div>

        {globalError && <div className="assessment-error">{globalError}</div>}

        <AnimatePresence mode="wait">
          {currentQuestion && (
            <motion.div
              key={currentQuestion.id}
              className={`question-step ${errors[currentQuestion.id] ? 'question-step-error' : ''}`}
              initial={{ opacity: 0, x: 24 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -24 }}
              transition={{ duration: 0.22 }}
            >
              <div className="question-number">{currentIndex + 1}</div>
              <h3>{currentQuestion.question_text}</h3>
              <textarea
                value={answers[currentQuestion.id] || ''}
                onChange={(event) => handleAnswerChange(currentQuestion.id, event.target.value)}
                placeholder="Write your response here..."
                autoFocus
=======
      {/* Questions List */}
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '3rem', alignItems: 'center' }}>
        {questions.map((q, index) => (
          <motion.div 
            key={q.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="rounded-3xl border transition-colors shadow-sm"
            style={{ 
              padding: '2.5rem 2rem', 
              backgroundColor: errors[q.id] ? 'rgba(239, 68, 68, 0.05)' : 'var(--color-bg-card)',
              borderColor: errors[q.id] ? 'rgba(239, 68, 68, 0.5)' : 'var(--color-border)',
              width: '100%',
              maxWidth: '700px',
              margin: '0 auto'
            }}
          >
            <div className="flex flex-col md:flex-row md:items-start gap-4 mb-6 text-left">
              <div className="flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg border" style={{ backgroundColor: 'var(--color-accent-glow)', color: 'var(--color-accent)', borderColor: 'var(--color-accent)' }}>
                {q.order}
              </div>
              <div className="pt-1">
                <h3 className="text-lg md:text-xl font-medium text-white leading-relaxed" style={{ marginBottom: '1.25rem' }}>
                  {q.question_text}
                </h3>
                <p className="text-xs uppercase tracking-widest font-semibold" style={{ color: 'var(--color-accent)', marginTop: '0.5rem', marginBottom: '2.5rem' }}>
                  Analyzing: {q.eq_dimension.replace('_', ' ')}
                </p>
              </div>
            </div>

            <div className="mt-8 w-full">
              <textarea
                value={answers[q.id]}
                onChange={(e) => handleAnswerChange(q.id, e.target.value)}
                placeholder="Type your detailed response here... (Minimum 10 characters)"
                className="w-full resize-y transition-all text-base md:text-lg leading-relaxed text-left"
                style={{
                  minHeight: '140px',
                  padding: '1.5rem',
                  backgroundColor: '#000000',
                  border: '1px solid',
                  borderColor: errors[q.id] ? 'rgba(239, 68, 68, 0.5)' : 'var(--color-border)',
                  borderRadius: '16px',
                  color: 'white',
                  outline: 'none'
                }}
                onFocus={(e) => {
                  if (!errors[q.id]) e.target.style.borderColor = 'var(--color-accent)';
                  e.target.style.boxShadow = errors[q.id] ? '0 0 0 2px rgba(239, 68, 68, 0.2)' : '0 0 0 2px var(--color-accent-glow)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = errors[q.id] ? 'rgba(239, 68, 68, 0.5)' : 'var(--color-border)';
                  e.target.style.boxShadow = 'none';
                }}
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
              />

              {errors[currentQuestion.id] && (
                <p className="question-error-text">{errors[currentQuestion.id]}</p>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        <div className="question-actions">
          <button
            type="button"
            className="flow-button secondary"
            onClick={goToPrevious}
            disabled={currentIndex === 0 || submitting}
          >
            Back
          </button>

          {currentIndex < questions.length - 1 ? (
            <button
              type="button"
              className="flow-button primary"
              onClick={goToNext}
              disabled={submitting}
            >
              Next
            </button>
          ) : (
            <button
              type="button"
              className="flow-button primary"
              onClick={handleSubmit}
              disabled={submitting}
            >
              {submitting ? 'Submitting...' : 'Submit assessment'}
            </button>
          )}
        </div>
      </section>
    </main>
  );
}
