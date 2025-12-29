// Utility functions for tracking and managing reading position

const READING_POSITION_KEY = 'ai-book-reading-position';
const SESSION_ID_KEY = 'ai-book-session-id';

class ReadingPositionTracker {
  constructor() {
    this.sessionId = this.getSessionId();
    this.readingPosition = this.getStoredPosition();
  }

  // Generate or retrieve a session ID
  getSessionId() {
    let sessionId = localStorage.getItem(SESSION_ID_KEY);
    if (!sessionId) {
      sessionId = this.generateSessionId();
      localStorage.setItem(SESSION_ID_KEY, sessionId);
    }
    return sessionId;
  }

  // Generate a random session ID
  generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
  }

  // Get stored reading position from localStorage
  getStoredPosition() {
    try {
      const stored = localStorage.getItem(READING_POSITION_KEY);
      return stored ? JSON.parse(stored) : {};
    } catch (error) {
      console.warn('Error reading stored position:', error);
      return {};
    }
  }

  // Save reading position to localStorage
  savePosition(contentId, position) {
    const positionData = {
      contentId,
      position,
      timestamp: Date.now(),
      sessionId: this.sessionId
    };

    this.readingPosition[contentId] = positionData;
    localStorage.setItem(READING_POSITION_KEY, JSON.stringify(this.readingPosition));
  }

  // Get reading position for a specific content
  getPosition(contentId) {
    return this.readingPosition[contentId] || null;
  }

  // Clear stored reading position
  clearPosition(contentId) {
    if (contentId) {
      delete this.readingPosition[contentId];
    } else {
      this.readingPosition = {};
    }
    localStorage.setItem(READING_POSITION_KEY, JSON.stringify(this.readingPosition));
  }

  // Send reading progress to backend API
  async saveProgressToAPI(contentId, position) {
    try {
      const response = await fetch('/api/content/reading-progress', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: this.sessionId,
          content_id: contentId,
          position: position
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error saving reading progress to API:', error);
      // Fallback to local storage if API fails
      this.savePosition(contentId, position);
      return { status: 'saved locally', error: error.message };
    }
  }

  // Get reading progress from backend API
  async getProgressFromAPI() {
    try {
      const response = await fetch(`/api/content/reading-progress/${this.sessionId}`);
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting reading progress from API:', error);
      // Fallback to local storage if API fails
      return { position: this.getStoredPosition() };
    }
  }
}

// Create a singleton instance
const readingPositionTracker = new ReadingPositionTracker();

export default readingPositionTracker;