/**
 * Translation Caching Service for AI-Native Book
 * Provides caching for translation content to improve performance
 */

class TranslationCache {
  constructor(maxSize = 100, ttl = 300000) { // 5 minutes default TTL
    this.cache = new Map();
    this.maxSize = maxSize;
    this.ttl = ttl; // Time to live in milliseconds
  }

  /**
   * Get a translation from cache
   * @param {string} key - Cache key (e.g., contentId:languageCode)
   * @returns {Object|null} Cached translation or null if not found/expired
   */
  get(key) {
    if (!this.cache.has(key)) {
      return null;
    }

    const entry = this.cache.get(key);
    const now = Date.now();

    // Check if entry has expired
    if (now - entry.timestamp > this.ttl) {
      this.cache.delete(key);
      return null;
    }

    return entry.value;
  }

  /**
   * Set a translation in cache
   * @param {string} key - Cache key
   * @param {Object} value - Translation object
   */
  set(key, value) {
    // If cache is at max size, remove oldest entry
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }

    this.cache.set(key, {
      value: value,
      timestamp: Date.now()
    });
  }

  /**
   * Delete a specific entry from cache
   * @param {string} key - Cache key to delete
   */
  delete(key) {
    this.cache.delete(key);
  }

  /**
   * Clear the entire cache
   */
  clear() {
    this.cache.clear();
  }

  /**
   * Get cache statistics
   * @returns {Object} Cache statistics
   */
  getStats() {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      ttl: this.ttl
    };
  }

  /**
   * Clean up expired entries
   */
  cleanup() {
    const now = Date.now();
    for (const [key, entry] of this.cache.entries()) {
      if (now - entry.timestamp > this.ttl) {
        this.cache.delete(key);
      }
    }
  }
}

// Singleton instance
const translationCache = new TranslationCache();

/**
 * Get translation with caching
 * @param {string} contentId - ID of the content to translate
 * @param {string} languageCode - Language code (e.g., 'ur' for Urdu)
 * @returns {Promise<Object|null>} Translation object or null
 */
const getTranslationWithCache = async (contentId, languageCode) => {
  const cacheKey = `${contentId}:${languageCode}`;

  // Try to get from cache first
  const cached = translationCache.get(cacheKey);
  if (cached) {
    return cached;
  }

  try {
    // Fetch from API
    const response = await fetch(`/api/translations/${contentId}?lang=${languageCode}`);

    if (!response.ok) {
      throw new Error(`Translation API error: ${response.status}`);
    }

    const translation = await response.json();

    // Cache the result
    translationCache.set(cacheKey, translation);

    return translation;
  } catch (error) {
    console.error('Error fetching translation:', error);
    return null;
  }
};

/**
 * Preload translations for better performance
 * @param {Array} contentIds - Array of content IDs to preload
 * @param {string} languageCode - Language code to preload
 */
const preloadTranslations = async (contentIds, languageCode) => {
  const promises = contentIds.map(contentId =>
    getTranslationWithCache(contentId, languageCode)
  );

  await Promise.allSettled(promises);
};

/**
 * Clear specific translations from cache
 * @param {string} contentId - Content ID to clear (or null for all)
 * @param {string} languageCode - Language code to clear (or null for all)
 */
const clearTranslationCache = (contentId = null, languageCode = null) => {
  if (!contentId && !languageCode) {
    translationCache.clear();
  } else if (contentId && !languageCode) {
    // Clear all languages for specific content
    for (const key of translationCache.cache.keys()) {
      if (key.startsWith(`${contentId}:`)) {
        translationCache.delete(key);
      }
    }
  } else if (!contentId && languageCode) {
    // Clear specific language for all content
    for (const key of translationCache.cache.keys()) {
      if (key.endsWith(`:${languageCode}`)) {
        translationCache.delete(key);
      }
    }
  } else {
    // Clear specific content and language
    translationCache.delete(`${contentId}:${languageCode}`);
  }
};

export {
  translationCache,
  getTranslationWithCache,
  preloadTranslations,
  clearTranslationCache
};

export default translationCache;