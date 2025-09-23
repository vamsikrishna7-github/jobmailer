'use client';

import { useState } from 'react';

export default function JobApplicationForm({ onSubmit, onBack, loading }) {
  const [formData, setFormData] = useState({
    hr_email: '',
    company: '',
    role: '',
    job_description: '',
    recipient_name: 'Hiring Manager',
    company_address: '',
    company_city_state_zip: '',
    previous_company: '',
    key_skills: '',
    specific_achievements: '',
    company_interest: '',
    personal_qualities: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div>
      <h3 className="text-xl font-semibold mb-6 text-gray-900">Step 2: Job Application Details</h3>
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Job Information */}
        <div className="border-b pb-6">
          <h4 className="text-lg font-medium text-gray-900 mb-4">Job Information</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                HR Email *
              </label>
              <input
                type="email"
                name="hr_email"
                value={formData.hr_email}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="hr@company.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Company Name *
              </label>
              <input
                type="text"
                name="company"
                value={formData.company}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Tech Corp"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Role *
              </label>
              <input
                type="text"
                name="role"
                value={formData.role}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Senior Software Engineer"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Recipient Name
              </label>
              <input
                type="text"
                name="recipient_name"
                value={formData.recipient_name}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="John Smith"
              />
            </div>
          </div>
          <div className="mt-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Description
            </label>
            <textarea
              name="job_description"
              value={formData.job_description}
              onChange={handleInputChange}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Describe the job requirements, responsibilities, and what you're looking for in a candidate..."
            />
          </div>
        </div>

        {/* Company Address */}
        <div className="border-b pb-6">
          <h4 className="text-lg font-medium text-gray-900 mb-4">Company Address (Optional)</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Street Address
              </label>
              <input
                type="text"
                name="company_address"
                value={formData.company_address}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="123 Tech Street"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                City, State, Zip
              </label>
              <input
                type="text"
                name="company_city_state_zip"
                value={formData.company_city_state_zip}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="San Francisco, CA 94105"
              />
            </div>
          </div>
        </div>

        {/* Enhanced Details */}
        <div className="border-b pb-6">
          <h4 className="text-lg font-medium text-gray-900 mb-4">Enhanced Application Details (Optional)</h4>
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Previous Company
              </label>
              <input
                type="text"
                name="previous_company"
                value={formData.previous_company}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="TechStart Inc."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Key Skills to Highlight
              </label>
              <input
                type="text"
                name="key_skills"
                value={formData.key_skills}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Python, Django, React, PostgreSQL, AWS, Docker"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Specific Achievements
              </label>
              <textarea
                name="specific_achievements"
                value={formData.specific_achievements}
                onChange={handleInputChange}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Led a team of 5 developers to build a scalable e-commerce platform serving 50,000+ users. Implemented CI/CD pipelines that reduced deployment time by 60%."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                What Excites You About This Opportunity
              </label>
              <textarea
                name="company_interest"
                value={formData.company_interest}
                onChange={handleInputChange}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Tech Corp's innovative approach to cloud-native applications and commitment to developer experience"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Personal Qualities
              </label>
              <input
                type="text"
                name="personal_qualities"
                value={formData.personal_qualities}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="strong problem-solving abilities, collaborative mindset, and passion for clean code"
              />
            </div>
          </div>
        </div>

        <div className="flex justify-between pt-6">
          <button
            type="button"
            onClick={onBack}
            className="bg-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Back
          </button>
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? 'Generating...' : 'Generate Email & Cover Letter'}
          </button>
        </div>
      </form>
    </div>
  );
}
