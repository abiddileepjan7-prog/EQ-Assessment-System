<<<<<<< HEAD
import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
=======
import { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { submitResponses } from '../services/api';
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096

export default function LoadingPage() {
  const { id } = useParams();
  const navigate = useNavigate();
<<<<<<< HEAD

  useEffect(() => {
    const redirectTimer = setTimeout(() => {
      navigate(`/results/${id}`);
    }, 1200);

    return () => clearTimeout(redirectTimer);
  }, [id, navigate]);

  return (
    <main className="processing-shell">
      <section className="processing-panel">
        <p className="section-kicker">Processing</p>
        <h1>Preparing your results</h1>
        <p>Your assessment profile will open automatically.</p>
      </section>
    </main>
=======
  const location = useLocation();
  const [step, setStep] = useState(0);

  const steps = [
    "Initializing Transformer Models...",
    "Running Emotion & Sentiment Analysis...",
    "Scanning for Behavioral Indicators...",
    "Calculating EQ Dimensions...",
    "Generating AI Feedback Profile..."
  ];

  useEffect(() => {
    // If user arrived here without responses, kick them back
    if (!location.state?.formattedResponses) {
      navigate(`/assessment/${id}`);
      return;
    }

    // Cycle through steps quickly for visual flair
    const interval = setInterval(() => {
      setStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 1200);

    // The actual API call
    const processAssessment = async () => {
      try {
        await submitResponses(id, location.state.formattedResponses);
        // Clear interval and show final step
        clearInterval(interval);
        setStep(steps.length - 1);
        
        // Brief pause for effect, then to results
        setTimeout(() => {
          navigate(`/results/${id}`);
        }, 1000);

      } catch (err) {
        clearInterval(interval);
        // Retrieve scenario/questions that were passed from AssessmentPage (if available)
        const passBackState = location.state?.scenario && location.state?.questions 
          ? { scenario: location.state.scenario, questions: location.state.questions } 
          : {};

        // Handle Validation Errors by bouncing back to Assessment
        if (err.response && err.response.status === 400 && err.response.data.details) {
          const validationErrors = {};
          err.response.data.details.forEach(detail => {
            validationErrors[detail.question_id] = detail.message;
          });
          navigate(`/assessment/${id}`, { 
            state: { 
              ...passBackState,
              validationErrors, 
              globalError: "Some responses need attention. Please see the warnings below." 
            } 
          });
        } else {
          navigate(`/assessment/${id}`, { 
            state: { ...passBackState, globalError: "Failed to submit responses. Please try again." } 
          });
        }
      }
    };

    processAssessment();

    return () => clearInterval(interval);
  }, [id, navigate, location.state]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-black relative overflow-hidden">
      {/* Background ambient glow */}
      <div className="absolute w-[500px] h-[500px] bg-emerald-500/10 blur-[120px] rounded-full top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none" />

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="p-12 max-w-xl w-full flex flex-col items-center text-center relative z-10"
      >
        {/* Pulsing ring behind Mew */}
        <div className="relative w-40 h-40 mb-10 flex items-center justify-center">
          <motion.div 
            animate={{ 
              scale: [1, 1.2, 1],
              opacity: [0.3, 0.6, 0.3]
            }}
            transition={{ 
              duration: 2, 
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="absolute inset-0 rounded-full border-2 border-emerald-500/30 bg-emerald-500/5 blur-sm"
          />
          <img 
            src="https://media.tenor.com/6S9w6LQV48wAAAAi/mew-spinning.gif" 
            alt="Analyzing" 
            className="relative z-10"
            style={{ width: '100%', height: '100%', objectFit: 'contain', filter: 'drop-shadow(0 0 30px rgba(16, 185, 129, 0.4))' }} 
          />
        </div>

        <h2 className="text-3xl font-extrabold mb-8 tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-200">
          AI Analysis in Progress
        </h2>
        
        {/* Progress Bar Track */}
        <div className="w-full h-1 bg-white/10 rounded-full mb-8 overflow-hidden relative">
          <motion.div 
            className="absolute top-0 left-0 h-full bg-emerald-500"
            initial={{ width: "0%" }}
            animate={{ width: `${(step / (steps.length - 1)) * 100}%` }}
            transition={{ duration: 0.5, ease: "easeInOut" }}
          />
        </div>

        <div className="h-8 overflow-hidden w-full relative">
          <AnimatePresence mode="wait">
            <motion.p 
              key={step}
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -20, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="text-emerald-300/80 font-medium tracking-wide uppercase text-sm absolute w-full"
            >
              {steps[step]}
            </motion.p>
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
  );
}
