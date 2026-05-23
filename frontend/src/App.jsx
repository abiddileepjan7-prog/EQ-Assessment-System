import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import AssessmentPage from './pages/AssessmentPage';
import LoadingPage from './pages/LoadingPage';
import ResultsPage from './pages/ResultsPage';

function App() {
  return (
    <Router>
      <div className="gradient-bg" />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/assessment/:id" element={<AssessmentPage />} />
        <Route path="/loading/:id" element={<LoadingPage />} />
        <Route path="/results/:id" element={<ResultsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
