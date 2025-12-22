import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './AIAssistant.module.css';
import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';

const AIAssistant = ({ contextContentId = null }) => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isOpen, setIsOpen] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [currentContextId, setCurrentContextId] = useState(contextContentId);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [conversationHistory]);

  // Effect to get current content ID from URL if not provided
  useEffect(() => {
    if (!contextContentId) {
      // Extract content ID from current URL path
      const pathParts = window.location.pathname.split('/');
      if (pathParts.length >= 3 && pathParts[1] === 'docs') {
        // Convert URL slug to content ID format (e.g., /docs/chapter-1/perception -> chapter-1-perception)
        const contentId = pathParts.slice(2).join('-');
        setCurrentContextId(contentId);
      }
    } else {
      setCurrentContextId(contextContentId);
    }
  }, [contextContentId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Handle question submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);

    try {
      // Add question to conversation history
      const newQuestion = {
        id: Date.now(),
        type: 'question',
        content: question,
        timestamp: new Date()
      };

      setConversationHistory(prev => [...prev, newQuestion]);

      // Call AI assistant API
      const response = await fetch('/api/ai-assistant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          context_content_id: currentContextId,
          include_sources: true
        }),
      });

      // Handle different response statuses gracefully
      if (response.status === 503) {
        // Service unavailable - AI service is down
        setError("AI assistant service is temporarily unavailable. Please try again later.");
        console.warn('AI assistant service unavailable');
        return;
      } else if (response.status === 429) {
        // Rate limited
        setError("You've reached the limit for AI assistant questions. Please try again later.");
        return;
      } else if (!response.ok) {
        if (response.status >= 500) {
          // Server error - AI service issue
          setError("AI assistant is experiencing issues. The book content is still fully accessible.");
          console.error(`AI API server error: ${response.status}`);
          return;
        } else {
          // Client error
          throw new Error(`AI API error: ${response.status}`);
        }
      }

      const data = await response.json();

      // Add answer to conversation history
      const newAnswer = {
        id: Date.now() + 1,
        type: 'answer',
        content: data.answer,
        sources: data.sources || [],
        confidence: data.confidence,
        timestamp: new Date()
      };

      setConversationHistory(prev => [...prev, newAnswer]);
      setQuestion('');
    } catch (err) {
      setError(err.message);
      console.error('AI assistant error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Toggle assistant visibility
  const toggleAssistant = () => {
    setIsOpen(!isOpen);
  };

  // Clear conversation
  const clearConversation = () => {
    setConversationHistory([]);
    setAnswer('');
    setSources([]);
  };

  return (
    <div className={styles.aiAssistantContainer}>
      {/* AI Assistant Toggle Button */}
      <button
        className={clsx(styles.toggleButton, {
          [styles.toggleButtonOpen]: isOpen
        })}
        onClick={toggleAssistant}
        aria-label={isOpen ? "Close AI Assistant" : "Open AI Assistant"}
      >
        {isOpen ? '✕' : '🤖'}
      </button>

      {/* AI Assistant Panel */}
      {isOpen && (
        <div className={styles.aiAssistantPanel}>
          <div className={styles.panelHeader}>
            <h3 className={styles.panelTitle}>AI Assistant</h3>
            <button
              className={styles.closeButton}
              onClick={toggleAssistant}
              aria-label="Close AI Assistant"
            >
              ✕
            </button>
          </div>

          <div className={styles.conversationHistory}>
            {conversationHistory.length === 0 ? (
              <div className={styles.welcomeMessage}>
                <p>Ask me anything about the book content!</p>
                <p className={styles.hint}>I can answer questions based only on the book's content.</p>
              </div>
            ) : (
              <div className={styles.messagesContainer}>
                {conversationHistory.map((message) => (
                  <div
                    key={message.id}
                    className={clsx(styles.message, {
                      [styles.questionMessage]: message.type === 'question',
                      [styles.answerMessage]: message.type === 'answer'
                    })}
                  >
                    <div className={styles.messageContent}>
                      {message.content}
                    </div>
                    {message.type === 'answer' && message.sources && message.sources.length > 0 && (
                      <div className={styles.sources}>
                        <h5>Sources:</h5>
                        <ul>
                          {message.sources.slice(0, 3).map((source, idx) => (
                            <li key={idx}>
                              <a href={source.url_path} target="_blank" rel="noopener noreferrer">
                                {source.title}
                              </a>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
                {isLoading && (
                  <div className={styles.loadingMessage}>
                    <LoadingSpinner size="small" label="Thinking..." />
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {error && (
            <div className={styles.error}>
              Error: {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className={styles.questionForm}>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question about the book..."
              className={styles.questionInput}
              disabled={isLoading}
            />
            <button
              type="submit"
              className={styles.submitButton}
              disabled={!question.trim() || isLoading}
            >
              {isLoading ? '...' : 'Ask'}
            </button>
          </form>

          {conversationHistory.length > 0 && (
            <button
              className={styles.clearButton}
              onClick={clearConversation}
            >
              Clear Conversation
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default AIAssistant;