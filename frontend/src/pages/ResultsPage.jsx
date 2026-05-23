import { useEffect, useMemo, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getResults } from '../services/api';
import RadarChart from '../components/charts/RadarChart';

const DIMENSIONS = [
  ['Self Awareness', 'self_awareness_score'],
  ['Self Regulation', 'self_regulation_score'],
  ['Empathy', 'empathy_score'],
  ['Social Skills', 'social_skills_score'],
  ['Motivation', 'motivation_score'],
  ['Stress Management', 'stress_management_score'],
  ['Conflict Resolution', 'conflict_resolution_score'],
  ['Adaptability', 'adaptability_score'],
  ['Resilience', 'resilience_score'],
];

export default function ResultsPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [assessment, setAssessment] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchResults = async () => {
      try {
        setAssessment(await getResults(id));
      } catch (err) {
        console.error(err);
        setError('Failed to load results. They may still be processing.');
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [id]);

  const result = assessment?.result;
  const dimensionRows = useMemo(() => {
    if (!result) return [];
    return DIMENSIONS.map(([label, key]) => ({
      label,
      key,
      score: Math.round(Number(result[key] || 0)),
    })).sort((a, b) => b.score - a.score);
  }, [result]);

  if (loading) {
    return (
      <main className="results-loading">
        <p>Loading results...</p>
      </main>
    );
  }

  if (error || !assessment || !result) {
    return (
      <main className="results-loading">
        <section className="assessment-error">{error || 'Results not available.'}</section>
        <button onClick={() => navigate('/')} className="flow-button secondary">Return Home</button>
      </main>
    );
  }

  const roundedScore = Math.round(Number(result.overall_eq_score || 0));
  const level = assessment.eq_level ? assessment.eq_level.replace('_', ' ') : 'completed';

  return (
    <main className="results-shell">
      <section className="results-hero">
        <div>
          <p className="section-kicker">Assessment Complete</p>
          <h1>Your results</h1>
          <p className="results-subtitle">
            A score profile based on your written responses.
          </p>
        </div>

        <div className="score-tile">
          <span>{roundedScore}</span>
          <p>Overall score / 100</p>
        </div>
      </section>

      <section className="results-summary-grid">
        <div className="metric-card">
          <p>Assessment level</p>
          <strong>{level}</strong>
        </div>
        <div className="metric-card">
          <p>Highest area</p>
          <strong>{dimensionRows[0]?.label}</strong>
        </div>
        <div className="metric-card">
          <p>Lowest area</p>
          <strong>{dimensionRows[dimensionRows.length - 1]?.label}</strong>
        </div>
      </section>

      <section className="results-main-grid">
        <article className="results-card chart-card">
          <div className="card-heading">
            <p className="section-kicker">Radar View</p>
            <h2>Dimension profile</h2>
          </div>
          <div className="chart-frame">
            <RadarChart resultData={result} />
          </div>
        </article>
      </section>

      <section className="results-card dimension-table-card">
        <div className="card-heading">
          <p className="section-kicker">Score Breakdown</p>
          <h2>All areas</h2>
        </div>

        <div className="dimension-list">
          {dimensionRows.map((row) => (
            <div className="dimension-row" key={row.key}>
              <div className="dimension-row-label">
                <span>{row.label}</span>
                <strong>{row.score}</strong>
              </div>
              <div className="dimension-meter" aria-hidden="true">
                <div style={{ width: `${row.score}%` }} />
              </div>
            </div>
          ))}
        </div>
      </section>

<<<<<<< HEAD
      <div className="results-actions">
        <button onClick={() => navigate('/')} className="flow-button secondary">
          Take another assessment
=======
      {/* Details Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginBottom: '4rem' }}>
        
        {/* Strengths */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass-card"
          style={{ padding: '2rem' }}
        >
          <div className="flex items-center gap-3" style={{ marginBottom: '1.5rem' }}>
            <div className="w-8 h-8 rounded-full flex items-center justify-center font-bold" style={{ backgroundColor: 'var(--color-accent-glow)', color: 'var(--color-accent)' }}>
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" /></svg>
            </div>
            <h3 className="text-xl font-medium text-white">Core Strengths</h3>
          </div>
          <ul style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {result.strengths.map((s, i) => (
              <li key={i} className="flex items-start gap-3" style={{ color: 'var(--color-text-secondary)' }}>
                <span className="mt-1" style={{ color: 'var(--color-accent)' }}>•</span> {s}
              </li>
            ))}
          </ul>
        </motion.div>

        {/* Weaknesses */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="glass-card"
          style={{ padding: '2rem' }}
        >
          <div className="flex items-center gap-3" style={{ marginBottom: '1.5rem' }}>
            <div className="w-8 h-8 rounded-full flex items-center justify-center font-bold" style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', color: '#ef4444' }}>
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            </div>
            <h3 className="text-xl font-medium text-white">Growth Areas</h3>
          </div>
          <ul style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {result.weaknesses.map((w, i) => (
              <li key={i} className="flex items-start gap-3" style={{ color: 'var(--color-text-secondary)' }}>
                <span className="mt-1" style={{ color: '#ef4444' }}>•</span> {w}
              </li>
            ))}
          </ul>
        </motion.div>

        {/* Recommendations */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="glass-card"
          style={{ padding: '2rem' }}
        >
          <div className="flex items-center gap-3" style={{ marginBottom: '1.5rem' }}>
            <div className="w-8 h-8 rounded-full flex items-center justify-center font-bold" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6' }}>
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </div>
            <h3 className="text-xl font-medium text-white">Action Plan</h3>
          </div>
          <ul style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {result.recommendations.map((r, i) => (
              <li key={i} className="flex items-start gap-3 text-sm leading-relaxed" style={{ color: 'var(--color-text-secondary)' }}>
                <span className="mt-0.5 font-mono" style={{ color: '#3b82f6' }}>{i+1}.</span> {r}
              </li>
            ))}
          </ul>
        </motion.div>

      </div>

      <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', flexWrap: 'wrap' }}>
        <button 
          onClick={() => {
            const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            window.open(`${baseUrl}/api/assessment/${id}/report/`, '_blank');
          }} 
          className="btn-primary"
        >
          Download PDF Report
        </button>
        <button onClick={() => navigate('/')} className="btn-secondary">
          Take Another Assessment
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
        </button>
      </div>
    </main>
  );
}
