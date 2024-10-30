import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HeroPage from './components/HeroPage';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Dashboard from './components/Dashboard';
import Support from './components/Support';
import LoanAnalytics from './components/LoanAnalytics';
import LoanApplication from './components/LoanApplication';
import PrivacyConfirmation from './components/PrivacyConfirmation';
import LoanResult from './components/LoanResult';
import LoadingDecision from './components/LoadingDecision';
import AboutUs from './components/AboutUs';
import './styles/styles.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<HeroPage />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/support" element={<Support />} />
          <Route path="/loan-dashboard" element={<LoanAnalytics />} />
          <Route path="/loan-application" element={<LoanApplication />} />
          <Route path="/privacy-confirmation" element={<PrivacyConfirmation />} />
          <Route path="/loan-result" element={<LoanResult />} />
          <Route path="/loading-decision" element={<LoadingDecision />} />
          <Route path="/about" element={<AboutUs />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
