// API Configuration
export const API_CONFIG = {
  BASE_URL: 'https://jobmailer-dezw.onrender.com',
  ENDPOINTS: {
    HEALTH: '/api/health/',
    CREATE_PROFILE: '/api/create-profile/',
    GET_PROFILE: '/api/get-profile/',
    GENERATE_EMAIL: '/api/generate-email-enhanced/',
    GENERATE_COVER_LETTER: '/api/generate-cover-letter-pdf/',
    SEND_EMAIL_WITH_RESUME: '/api/send-email-with-resume/',
    SEND_EMAIL_WITH_RESUME_AND_COVER_LETTER: '/api/send-email-with-resume-and-cover-letter/',
  }
};

// API Helper Functions
export const apiCall = async (endpoint, options = {}) => {
  const url = `${API_CONFIG.BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const config = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    // Handle different response types
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/pdf')) {
      return response.blob();
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// Specific API functions
export const createProfile = async (profileData) => {
  const formData = new FormData();
  
  Object.keys(profileData).forEach(key => {
    if (profileData[key] !== null && profileData[key] !== undefined) {
      formData.append(key, profileData[key]);
    }
  });

  return apiCall(API_CONFIG.ENDPOINTS.CREATE_PROFILE, {
    method: 'POST',
    headers: {}, // Remove Content-Type for FormData
    body: formData,
  });
};

export const getProfile = async (profileId) => {
  return apiCall(`${API_CONFIG.ENDPOINTS.GET_PROFILE}${profileId}/`);
};

export const generateEmail = async (data) => {
  return apiCall(API_CONFIG.ENDPOINTS.GENERATE_EMAIL, {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const generateCoverLetter = async (data) => {
  return apiCall(API_CONFIG.ENDPOINTS.GENERATE_COVER_LETTER, {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const sendEmailWithResume = async (data) => {
  return apiCall(API_CONFIG.ENDPOINTS.SEND_EMAIL_WITH_RESUME, {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const sendEmailWithResumeAndCoverLetter = async (data) => {
  return apiCall(API_CONFIG.ENDPOINTS.SEND_EMAIL_WITH_RESUME_AND_COVER_LETTER, {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const checkHealth = async () => {
  return apiCall(API_CONFIG.ENDPOINTS.HEALTH);
};
