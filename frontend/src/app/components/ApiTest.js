'use client';

import { useState } from 'react';
import { checkHealth } from '../../config/api';

export default function ApiTest() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const testApiConnection = async () => {
    setLoading(true);
    setError(null);
    setStatus(null);

    try {
      const result = await checkHealth();
      setStatus('success');
      console.log('API Health Check:', result);
    } catch (err) {
      setError(err.message);
      setStatus('error');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 p-8 mb-8 animate-fadeIn">
      <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
        <span className="mr-3 text-3xl">🔗</span>
        API Connection Status
      </h3>
      <div className="flex items-center space-x-6">
        <button
          onClick={testApiConnection}
          disabled={loading}
          className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl hover:from-green-600 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 transition-all duration-300 transform hover:scale-105 font-semibold flex items-center space-x-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
              <span>Testing...</span>
            </>
          ) : (
            <>
              <span>🔍</span>
              <span>Test Connection</span>
            </>
          )}
        </button>
        
        {status === 'success' && (
          <div className="flex items-center text-green-400 animate-slideInRight">
            <svg className="w-6 h-6 mr-3 animate-bounce" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            <span className="text-lg font-semibold">Connected Successfully</span>
          </div>
        )}
        
        {status === 'error' && (
          <div className="flex items-center text-red-400 animate-slideInRight">
            <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span className="text-lg font-semibold">Connection Failed</span>
          </div>
        )}
      </div>
      
      {error && (
        <div className="mt-6 p-4 bg-red-500/20 border border-red-500/50 text-red-300 rounded-xl animate-slideInDown">
          <div className="flex items-start">
            <svg className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div>
              <strong className="block">Connection Error:</strong>
              <span className="text-sm opacity-90">{error}</span>
            </div>
          </div>
        </div>
      )}
      
      <div className="mt-6 p-4 bg-white/5 rounded-xl border border-white/10">
        <h4 className="text-white font-semibold mb-3">API Configuration</h4>
        <div className="space-y-2 text-sm text-gray-300">
          <p><strong className="text-blue-400">Base URL:</strong> https://jobmailer-dezw.onrender.com</p>
          <p><strong className="text-blue-400">Health Check:</strong> /api/health/</p>
          <p><strong className="text-blue-400">Status:</strong> Production Ready</p>
        </div>
      </div>
    </div>
  );
}
