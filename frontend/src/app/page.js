'use client';

import { useState, useEffect } from 'react';
import JobMailerForm from './components/JobMailerForm';
import Header from './components/Header';
import Footer from './components/Footer';
import ApiTest from './components/ApiTest';
import ProfileManager from './components/ProfileManager';

export default function Home() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  const sections = [
    { id: 'dashboard', label: 'Dashboard', icon: '🏠' },
    { id: 'profile', label: 'Profile', icon: '👤' },
    { id: 'applications', label: 'Applications', icon: '📝' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <Header activeSection={activeSection} setActiveSection={setActiveSection} sections={sections} />
      
      <main className="container mx-auto px-4 py-8 transition-all duration-700 ease-in-out">
        <div className={`max-w-6xl mx-auto transition-all duration-500 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          
          {activeSection === 'dashboard' && (
            <div className="animate-fadeIn">
              <div className="text-center mb-12">
                <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent mb-6 animate-slideInUp">
                  JobMailer Pro
                </h1>
                <p className="text-xl text-gray-300 mb-12 animate-slideInUp animation-delay-200">
                  AI-powered professional job applications
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
                  <div className="group bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl border border-white/20 hover:scale-105 transition-all duration-300 animate-slideInUp animation-delay-300">
                    <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">✨</div>
                    <h3 className="text-xl font-semibold mb-3 text-white">AI Email Generation</h3>
                    <p className="text-gray-300">Intelligent, personalized job application emails</p>
                  </div>
                  <div className="group bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl border border-white/20 hover:scale-105 transition-all duration-300 animate-slideInUp animation-delay-400">
                    <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">📄</div>
                    <h3 className="text-xl font-semibold mb-3 text-white">Cover Letters</h3>
                    <p className="text-gray-300">Professional PDF cover letters with attachments</p>
                  </div>
                  <div className="group bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl border border-white/20 hover:scale-105 transition-all duration-300 animate-slideInUp animation-delay-500">
                    <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">🚀</div>
                    <h3 className="text-xl font-semibold mb-3 text-white">Complete Workflow</h3>
                    <p className="text-gray-300">End-to-end application management</p>
                  </div>
                </div>
              </div>
              
              <div className="space-y-8">
                <ApiTest />
                <JobMailerForm />
              </div>
            </div>
          )}

          {activeSection === 'profile' && (
            <div className="animate-fadeIn">
              <ProfileManager />
            </div>
          )}

          {activeSection === 'applications' && (
            <div className="animate-fadeIn">
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 p-8">
                <h2 className="text-3xl font-bold text-white mb-6">Application History</h2>
                <p className="text-gray-300">Track and manage your job applications here.</p>
                <div className="mt-8 p-6 bg-white/5 rounded-xl border border-white/10">
                  <p className="text-gray-400 text-center">Application tracking coming soon...</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
