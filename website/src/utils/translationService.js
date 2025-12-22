/**
 * Service for handling translation functionality
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Simple in-memory cache for translations
const translationCache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

/**
 * Check if cached translation is still valid
 */
const isCacheValid = (cacheEntry) => {
  if (!cacheEntry) return false;
  const now = Date.now();
  return (now - cacheEntry.timestamp) < CACHE_DURATION;
};

/**
 * Fetch translation for specific content and language
 */
export const fetchTranslation = async (contentId, languageCode) => {
  const cacheKey = `${contentId}_${languageCode}`;

  // Check cache first
  const cached = translationCache.get(cacheKey);
  if (cached && isCacheValid(cached)) {
    return cached.data;
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/translation/${contentId}/${languageCode}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      if (response.status === 404) {
        // Cache the "not found" result
        translationCache.set(cacheKey, {
          data: null,
          timestamp: Date.now()
        });
        return null; // Translation doesn't exist
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Cache the successful result
    translationCache.set(cacheKey, {
      data: data,
      timestamp: Date.now()
    });

    return data;
  } catch (error) {
    console.error('Error fetching translation:', error);

    // If there was an error but we have a cached result, return it
    const fallback = translationCache.get(cacheKey);
    if (fallback && isCacheValid(fallback)) {
      return fallback.data;
    }

    throw error;
  }
};

/**
 * Fetch all translations for a specific content
 */
export const fetchTranslationsForContent = async (contentId) => {
  const cacheKey = `translations_${contentId}`;

  // Check cache first
  const cached = translationCache.get(cacheKey);
  if (cached && isCacheValid(cached)) {
    return cached.data;
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/translation/${contentId}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Cache the result
    translationCache.set(cacheKey, {
      data: data,
      timestamp: Date.now()
    });

    return data;
  } catch (error) {
    console.error('Error fetching translations for content:', error);

    // If there was an error but we have a cached result, return it
    const fallback = translationCache.get(cacheKey);
    if (fallback && isCacheValid(fallback)) {
      return fallback.data;
    }

    throw error;
  }
};

/**
 * Get translation progress for a language
 */
export const getTranslationProgress = async (languageCode) => {
  const cacheKey = `progress_${languageCode}`;

  // Check cache first
  const cached = translationCache.get(cacheKey);
  if (cached && isCacheValid(cached)) {
    return cached.data;
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/translation/progress/${languageCode}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Cache the result (with a longer cache duration for progress data)
    translationCache.set(cacheKey, {
      data: data,
      timestamp: Date.now()
    });

    return data;
  } catch (error) {
    console.error('Error fetching translation progress:', error);

    // If there was an error but we have a cached result, return it
    const fallback = translationCache.get(cacheKey);
    if (fallback && isCacheValid(fallback)) {
      return fallback.data;
    }

    throw error;
  }
};

/**
 * Create a new translation
 */
export const createTranslation = async (contentId, languageCode, translationData) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/translation/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content_id: contentId,
          language_code: languageCode,
          translated_title: translationData.translatedTitle,
          translated_content: translationData.translatedContent,
          summary: translationData.summary
        }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Clear related cache entries
    translationCache.delete(`${contentId}_${languageCode}`);
    translationCache.delete(`translations_${contentId}`);

    return data;
  } catch (error) {
    console.error('Error creating translation:', error);
    throw error;
  }
};

/**
 * Update an existing translation
 */
export const updateTranslation = async (contentId, languageCode, translationData) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/translation/${contentId}/${languageCode}`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          translated_title: translationData.translatedTitle,
          translated_content: translationData.translatedContent,
          summary: translationData.summary
        }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Clear related cache entries
    translationCache.delete(`${contentId}_${languageCode}`);
    translationCache.delete(`translations_${contentId}`);

    return data;
  } catch (error) {
    console.error('Error updating translation:', error);
    throw error;
  }
};

/**
 * Check if translation is available for content and language
 */
export const isTranslationAvailable = async (contentId, languageCode) => {
  try {
    const translation = await fetchTranslation(contentId, languageCode);
    return !!translation;
  } catch (error) {
    console.error('Error checking translation availability:', error);
    return false;
  }
};

/**
 * Validate translation quality and content
 */
export const validateTranslation = (translationData, originalContent = '') => {
  const errors = [];

  // Check if required fields exist
  if (!translationData.translated_title || translationData.translated_title.trim().length === 0) {
    errors.push('Translated title is required');
  }

  if (!translationData.translated_content || translationData.translated_content.trim().length === 0) {
    errors.push('Translated content is required');
  }

  // Check if translation is too short compared to original (may indicate poor quality)
  if (originalContent && translationData.translated_content) {
    const originalLength = originalContent.length;
    const translatedLength = translationData.translated_content.length;

    // If translated content is less than 30% of original, flag as potentially low quality
    if (originalLength > 0 && translatedLength / originalLength < 0.3) {
      errors.push('Translated content appears to be significantly shorter than original, which may indicate low quality');
    }
  }

  // Check for potential machine translation artifacts or quality issues
  if (translationData.translated_content) {
    // Check for repeated characters that might indicate encoding issues
    if (/(.)\1{5,}/.test(translationData.translated_content)) {
      errors.push('Translation contains repeated characters that may indicate encoding issues');
    }

    // Check for unusual character sequences
    if (/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(translationData.translated_content)) {
      errors.push('Translation contains control characters that may indicate processing errors');
    }
  }

  return {
    isValid: errors.length === 0,
    errors: errors
  };
};

/**
 * Get content with fallback mechanism
 * If translation is not available, return original content
 */
export const getContentWithFallback = async (contentId, originalTitle, originalContent, targetLanguage) => {
  if (targetLanguage === 'en') {
    // For English, always return original content
    return {
      title: originalTitle,
      content: originalContent,
      language: 'en',
      hasTranslation: false
    };
  }

  try {
    // Try to get translation
    const translation = await fetchTranslation(contentId, targetLanguage);

    if (translation && translation.translated_content) {
      // Translation is available
      return {
        title: translation.translated_title || originalTitle,
        content: translation.translated_content,
        language: targetLanguage,
        hasTranslation: true,
        summary: translation.summary
      };
    } else {
      // Translation not available, fallback to original
      console.warn(`Translation not available for content ${contentId} in language ${targetLanguage}, falling back to original`);
      return {
        title: originalTitle,
        content: originalContent,
        language: 'en', // Indicate that we're showing English content
        hasTranslation: false
      };
    }
  } catch (error) {
    console.error(`Error getting translation for ${contentId} in ${targetLanguage}:`, error);
    // On error, fallback to original content
    return {
      title: originalTitle,
      content: originalContent,
      language: 'en',
      hasTranslation: false
    };
  }
};