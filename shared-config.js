// Shared configuration between frontend and backend
// This file can be used by both Node.js (backend) and browser (frontend) environments

const sharedConfig = {
  // API endpoints
  API_BASE_URL: process.env.REACT_APP_API_URL || process.env.API_URL || 'http://localhost:8000',

  // Content settings
  CONTENT_PAGE_SIZE: 20,
  DEFAULT_LANGUAGE: 'en',
  SUPPORTED_LANGUAGES: ['en', 'ur'], // English and Urdu

  // Search settings
  DEFAULT_SEARCH_LIMIT: 10,
  MAX_SEARCH_LIMIT: 50,

  // AI assistant settings
  AI_RATE_LIMIT: 20, // requests per hour per IP
  SEARCH_RATE_LIMIT: 100, // requests per hour per IP
  AI_RESPONSE_TIMEOUT: 30000, // 30 seconds in milliseconds

  // Performance settings
  PAGE_LOAD_TIMEOUT: 2000, // 2 seconds in milliseconds for page load
  AI_RESPONSE_TIME_GOAL: 5000, // 5 seconds goal for AI responses
  SEARCH_RESPONSE_TIME_GOAL: 3000, // 3 seconds goal for search responses

  // Content structure
  CONTENT_SLUG_PATTERN: /^[a-zA-Z0-9_-]+$/,

  // Error codes
  ERROR_CODES: {
    CONTENT_NOT_FOUND: 'CONTENT_NOT_FOUND',
    SEARCH_ERROR: 'SEARCH_ERROR',
    AI_SERVICE_UNAVAILABLE: 'AI_SERVICE_UNAVAILABLE',
    RATE_LIMIT_EXCEEDED: 'RATE_LIMIT_EXCEEDED',
    VALIDATION_ERROR: 'VALIDATION_ERROR'
  }
};

module.exports = sharedConfig;