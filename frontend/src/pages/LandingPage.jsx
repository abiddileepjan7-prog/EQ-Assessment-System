import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { startAssessment } from '../services/api';
import heroImage from '../assets/hero.png';

export default function LandingPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    name: '',
    age: '25',
    gender: 'prefer_not',
    profession: '',
  });

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await startAssessment({
        ...formData,
        age: parseInt(formData.age, 10),
      });
<<<<<<< HEAD

      navigate(`/assessment/${data.assessment_id}`);
=======
      navigate(`/assessment/${data.assessment_id}`, { 
        state: { scenario: data.scenario, questions: data.questions } 
      });
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
    } catch (err) {
      console.error(err);
      setError('Could not start the assessment. Confirm the backend is running on port 8000.');
      setLoading(false);
    }
  };

  return (
<<<<<<< HEAD
    <main className="landing-shell">
      <section className="landing-visual" aria-label="Emotional intelligence assessment">
        <motion.div
          className="landing-copy"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.55 }}
        >
          <p className="landing-kicker">EQ Assessment</p>
          <h1>Emotional intelligence assessment</h1>
          <p className="landing-subtitle">
            Personalized scenarios for measuring awareness, regulation, empathy, and resilience.
          </p>
        </motion.div>

        <motion.div
          className="landing-image-wrap"
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.15, duration: 0.6 }}
        >
          <img src={heroImage} alt="" className="landing-image" />
        </motion.div>
      </section>

      <motion.section
        className="landing-form-panel"
        initial={{ opacity: 0, x: 24 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.1, duration: 0.55 }}
      >
        <div className="form-header">
          <p>Start profile</p>
          <h2>Tell us who you are</h2>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            className="landing-error"
=======
    <div className="min-h-screen relative flex items-center justify-center p-4 md:p-8">
      
      {/* Background Gradient Mesh */}
      <div className="gradient-bg"></div>

      <div className="max-w-[1400px] w-full mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center relative z-10">
        
        {/* Left Side: Hero Text & Logo */}
        <motion.div 
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="flex flex-col items-center lg:items-start text-center lg:text-left"
        >
          <img 
            src="https://media.tenor.com/_1YrEWVq8_MAAAAj/mew.gif" 
            alt="Blissey Logo" 
            className="mb-8"
            style={{ width: '160px', height: '160px', objectFit: 'contain' }} 
          />
          <h1 className="text-5xl md:text-7xl font-bold tracking-tighter text-white mb-4">
            Blissey<span className="text-[var(--color-accent)]">.</span>
          </h1>
          <h2 className="text-xl md:text-3xl font-light tracking-tight text-[var(--color-text-secondary)] mb-6">
            The AI-Powered Emotional Intelligence Assessment
          </h2>
          <p className="text-base md:text-lg text-[var(--color-text-muted)] max-w-lg leading-loose mt-4">
            Evaluate your EQ through adaptive, profession-specific scenarios generated and analyzed in real-time by advanced NLP models.
          </p>
        </motion.div>

        {/* Right Side: Form Card */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
          className="glass-card w-full relative z-10"
          style={{ padding: '3rem' }}
        >
          <div 
            className="border-b border-[var(--color-border)]"
            style={{ paddingBottom: '1.75rem', marginBottom: '2.5rem' }}
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
          >
            <h3 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">
              Begin your assessment
            </h3>
            <p className="text-[var(--color-text-secondary)] text-base mt-3">
              Enter your details to generate a customized, highly-tailored scenario.
            </p>
          </div>

<<<<<<< HEAD
        <form onSubmit={handleSubmit} className="landing-form">
          <label className="field-group" htmlFor="name">
            <span>Full name</span>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="Abid Dileep Jan"
            />
          </label>

          <div className="form-row">
            <label className="field-group" htmlFor="age">
              <span>Age</span>
              <input
                type="number"
                id="age"
                name="age"
                value={formData.age}
                onChange={handleChange}
                required
                min="16"
                max="99"
                placeholder="29"
=======
          {error && (
            <motion.div 
              initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="mb-8 p-4 rounded-xl border text-sm font-medium"
              style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', borderColor: 'rgba(239, 68, 68, 0.3)', color: '#ef4444' }}
            >
              {error}
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-6 w-full">
            
            {/* Full Name Input */}
            <div className="flex flex-col gap-2">
              <label htmlFor="name" className="text-xs uppercase tracking-widest font-semibold text-[var(--color-text-secondary)] ml-1">
                Full Name
              </label>
              <input
                type="text" id="name" name="name"
                value={formData.name} onChange={handleChange} required
                placeholder="John Doe"
                className="input-field"
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
              />
            </label>

<<<<<<< HEAD
            <label className="field-group" htmlFor="gender">
              <span>Gender</span>
              <select
                id="gender"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                required
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="non_binary">Non-binary</option>
                <option value="prefer_not">Prefer not to say</option>
              </select>
            </label>
          </div>

          <label className="field-group" htmlFor="profession">
            <span>Profession / job title</span>
            <input
              type="text"
              id="profession"
              name="profession"
              value={formData.profession}
              onChange={handleChange}
              required
              placeholder="Machine Learning Engineer"
            />
          </label>

          <button type="submit" disabled={loading} className="landing-submit">
            {loading ? (
              <span className="loading-label">
                <span className="spinner" />
                Generating scenario
              </span>
            ) : (
              'Start assessment'
            )}
          </button>
        </form>
      </motion.section>
    </main>
=======
            {/* Profession Input */}
            <div className="flex flex-col gap-2">
              <label htmlFor="profession" className="text-xs uppercase tracking-widest font-semibold text-[var(--color-text-secondary)] ml-1">
                Profession / Job Title
              </label>
              <input
                type="text" id="profession" name="profession"
                value={formData.profession} onChange={handleChange} required
                placeholder="e.g. Software Engineer, Nurse"
                className="input-field"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Age Input */}
              <div className="flex flex-col gap-2">
                <label htmlFor="age" className="text-xs uppercase tracking-widest font-semibold text-[var(--color-text-secondary)] ml-1">
                  Age
                </label>
                <input
                  type="number" id="age" name="age"
                  value={formData.age} onChange={handleChange} required
                  min="16" max="99" placeholder="25"
                  className="input-field"
                />
              </div>

              {/* Gender Input */}
              <div className="flex flex-col gap-2">
                <label htmlFor="gender" className="text-xs uppercase tracking-widest font-semibold text-[var(--color-text-secondary)] ml-1">
                  Gender
                </label>
                <div className="relative">
                  <select
                    id="gender" name="gender"
                    value={formData.gender} onChange={handleChange} required
                    className="input-field appearance-none cursor-pointer w-full"
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="non_binary">Non-binary</option>
                    <option value="prefer_not">Prefer not to say</option>
                  </select>
                  <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-[var(--color-text-secondary)]">
                    <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                      <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/>
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6">
              <button 
                type="submit" 
                disabled={loading}
                className="btn-primary w-full flex justify-center items-center h-14"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-3">
                    <svg className="animate-spin h-6 w-6 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating Scenario...
                  </span>
                ) : (
                  "Start Assessment"
                )}
              </button>
            </div>
          </form>
        </motion.div>
      </div>
    </div>
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
  );
}
