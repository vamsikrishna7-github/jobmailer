'use client';

import { useState } from 'react';

export default function ResultsDisplay({ email, coverLetterUrl, onSendEmail, onBack, onReset, loading }) {
  const [emailData, setEmailData] = useState({
    subject: '',
    body: email
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEmailData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSendEmail = (e) => {
    e.preventDefault();
    onSendEmail(emailData);
  };

  const downloadCoverLetter = () => {
    if (coverLetterUrl) {
      const link = document.createElement('a');
      link.href = coverLetterUrl;
      link.download = 'cover_letter.pdf';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div>
      <h3 className="text-xl font-semibold mb-6 text-gray-900">Step 3: Review & Send</h3>
      
      {/* Generated Email */}
      <div className="border-b pb-6 mb-6">
        <h4 className="text-lg font-medium text-gray-900 mb-4">Generated Email</h4>
        <div className="bg-gray-50 p-4 rounded-lg">
          <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">{email}</pre>
        </div>
      </div>

      {/* Cover Letter Download */}
      {coverLetterUrl && (
        <div className="border-b pb-6 mb-6">
          <h4 className="text-lg font-medium text-gray-900 mb-4">Cover Letter PDF</h4>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-green-600">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              <span className="text-sm font-medium">Cover letter generated successfully</span>
            </div>
            <button
              onClick={downloadCoverLetter}
              className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
            >
              Download PDF
            </button>
          </div>
        </div>
      )}

      {/* Email Sending Form */}
      <div className="border-b pb-6 mb-6">
        <h4 className="text-lg font-medium text-gray-900 mb-4">Send Email</h4>
        <form onSubmit={handleSendEmail} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Subject
            </label>
            <input
              type="text"
              name="subject"
              value={emailData.subject}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Application for [Position] at [Company]"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Body
            </label>
            <textarea
              name="body"
              value={emailData.body}
              onChange={handleInputChange}
              rows={8}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
            >
              {loading ? 'Sending...' : 'Send Email'}
            </button>
          </div>
        </form>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-between pt-6">
        <div className="flex space-x-4">
          <button
            onClick={onBack}
            className="bg-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Back to Job Details
          </button>
          <button
            onClick={onReset}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Start Over
          </button>
        </div>
        <div className="text-sm text-gray-500">
          <p>✅ Email generated with AI</p>
          <p>✅ Cover letter PDF created</p>
          <p>✅ Ready to send with resume attachment</p>
        </div>
      </div>
    </div>
  );
}
