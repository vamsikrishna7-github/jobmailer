'use client';

import { useState } from 'react';
import ProfileForm from './ProfileForm';
import JobApplicationForm from './JobApplicationForm';
import ResultsDisplay from './ResultsDisplay';
import { createProfile, generateEmail, generateCoverLetter, sendEmailWithResumeAndCoverLetter } from '../../config/api';

export default function JobMailerForm() {
  const [currentStep, setCurrentStep] = useState(1);
  const [profileData, setProfileData] = useState(null);
  const [generatedEmail, setGeneratedEmail] = useState(null);
  const [coverLetterUrl, setCoverLetterUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleProfileSubmit = async (data) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await createProfile(data);
      setProfileData({ ...data, id: result.profile_id });
      setCurrentStep(2);
    } catch (err) {
      setError(err.message || 'Failed to create profile');
    } finally {
      setLoading(false);
    }
  };

  const handleJobApplicationSubmit = async (jobData) => {
    setLoading(true);
    setError(null);
    
    try {
      const requestData = {
        profile_id: profileData.id,
        ...jobData
      };

      // Generate email
      const emailResult = await generateEmail(requestData);
      setGeneratedEmail(emailResult.email_text);

      // Generate cover letter PDF
      try {
        const coverLetterBlob = await generateCoverLetter(requestData);
        const url = URL.createObjectURL(coverLetterBlob);
        setCoverLetterUrl(url);
      } catch (coverLetterError) {
        console.warn('Cover letter generation failed:', coverLetterError);
        // Continue without cover letter
      }

      setCurrentStep(3);
    } catch (err) {
      setError(err.message || 'Failed to generate email and cover letter');
    } finally {
      setLoading(false);
    }
  };

  const handleSendEmail = async (emailData) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await sendEmailWithResumeAndCoverLetter({
        profile_id: profileData.id,
        ...emailData
      });
      
      alert('Email sent successfully! Check your inbox.');
    } catch (err) {
      setError(err.message || 'Failed to send email');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setCurrentStep(1);
    setProfileData(null);
    setGeneratedEmail(null);
    setCoverLetterUrl(null);
    setError(null);
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 p-8 animate-fadeIn">
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
            Job Application Workflow
          </h2>
          <div className="flex space-x-3">
            <div className={`w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-500 ${
              currentStep >= 1 
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg scale-110' 
                : 'bg-white/20 text-gray-400 border border-white/30'
            }`}>
              1
            </div>
            <div className={`w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-500 ${
              currentStep >= 2 
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg scale-110' 
                : 'bg-white/20 text-gray-400 border border-white/30'
            }`}>
              2
            </div>
            <div className={`w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-500 ${
              currentStep >= 3 
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg scale-110' 
                : 'bg-white/20 text-gray-400 border border-white/30'
            }`}>
              3
            </div>
          </div>
        </div>
        <div className="flex justify-between text-sm text-gray-300 font-medium">
          <span className="flex items-center">
            <span className="mr-2">👤</span>
            Profile Setup
          </span>
          <span className="flex items-center">
            <span className="mr-2">📝</span>
            Job Application
          </span>
          <span className="flex items-center">
            <span className="mr-2">🚀</span>
            Results & Send
          </span>
        </div>
      </div>

      {error && (
        <div className="bg-red-500/20 border border-red-500/50 text-red-300 px-6 py-4 rounded-xl mb-6 animate-slideInDown">
          <div className="flex items-center">
            <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        </div>
      )}

      {loading && (
        <div className="flex items-center justify-center py-12 animate-pulse">
          <div className="flex flex-col items-center">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-white/20 border-t-blue-500 mb-4"></div>
            <span className="text-gray-300 font-medium">Processing your request...</span>
          </div>
        </div>
      )}

      {currentStep === 1 && (
        <ProfileForm onSubmit={handleProfileSubmit} loading={loading} />
      )}

      {currentStep === 2 && profileData && (
        <JobApplicationForm 
          onSubmit={handleJobApplicationSubmit} 
          loading={loading}
          onBack={() => setCurrentStep(1)}
        />
      )}

      {currentStep === 3 && generatedEmail && (
        <ResultsDisplay 
          email={generatedEmail}
          coverLetterUrl={coverLetterUrl}
          onSendEmail={handleSendEmail}
          onBack={() => setCurrentStep(2)}
          onReset={resetForm}
          loading={loading}
        />
      )}
    </div>
  );
}
