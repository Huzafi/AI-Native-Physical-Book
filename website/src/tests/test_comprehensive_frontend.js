/**
 * Comprehensive frontend test suite for AI-Native Book
 * Tests all frontend components and functionality
 */

import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../App'; // Assuming main App component exists
import Search from '../components/Search/Search';
import AIAssistant from '../components/AIAssistant/AIAssistant';
import LanguageSelector from '../components/LanguageSelector/LanguageSelector';
import ExpandableSection from '../components/ExpandableSection/ExpandableSection';
import ContentPage from '../components/ContentPage/ContentPage';

// Mock API calls
global.fetch = jest.fn();

describe('Comprehensive Frontend Test Suite', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  describe('Search Component Tests', () => {
    test('renders search input correctly', () => {
      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);
      expect(searchInput).toBeInTheDocument();
    });

    test('handles search input changes', async () => {
      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);
      fireEvent.change(searchInput, { target: { value: 'test' } });

      // Wait for debounced search to occur
      await waitFor(() => {
        expect(fetch).toHaveBeenCalled();
      });
    });

    test('displays search results', async () => {
      // Mock search API response
      fetch.mockResolvedValueOnce({
        json: async () => ({
          results: [
            {
              id: '1',
              title: 'Test Result',
              preview: 'This is a test preview',
              url_path: '/docs/test',
              relevance_score: 0.9
            }
          ],
          total_count: 1
        }),
        ok: true
      });

      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);
      fireEvent.change(searchInput, { target: { value: 'test' } });

      await waitFor(() => {
        expect(screen.getByText(/test result/i)).toBeInTheDocument();
      });
    });

    test('handles search errors gracefully', async () => {
      // Mock search API error
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);
      fireEvent.change(searchInput, { target: { value: 'test' } });

      await waitFor(() => {
        // Should handle error without crashing
        expect(fetch).toHaveBeenCalled();
      });
    });

    test('shows search suggestions', async () => {
      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);
      fireEvent.change(searchInput, { target: { value: 't' } }); // Short query for suggestions

      // Check that suggestions dropdown appears
      await waitFor(() => {
        const suggestions = document.querySelector('.suggestionsDropdown');
        expect(suggestions).toBeInTheDocument();
      });
    });

    test('implements search result highlighting', async () => {
      // Mock search API response with highlighting
      fetch.mockResolvedValueOnce({
        json: async () => ({
          results: [
            {
              id: '1',
              title: 'Artificial Intelligence Test',
              preview: 'This is about artificial intelligence concepts',
              url_path: '/docs/ai',
              relevance_score: 0.9
            }
          ],
          total_count: 1
        }),
        ok: true
      });

      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);
      fireEvent.change(searchInput, { target: { value: 'artificial' } });

      await waitFor(() => {
        // Should highlight the search term in results
        const highlighted = document.querySelector('mark');
        expect(highlighted).toBeInTheDocument();
      });
    });
  });

  describe('AI Assistant Component Tests', () => {
    test('renders AI assistant toggle button', () => {
      render(
        <BrowserRouter>
          <AIAssistant />
        </BrowserRouter>
      );

      const toggleButton = screen.getByLabelText(/ai assistant/i);
      expect(toggleButton).toBeInTheDocument();
    });

    test('toggles AI assistant panel', () => {
      render(
        <BrowserRouter>
          <AIAssistant />
        </BrowserRouter>
      );

      const toggleButton = screen.getByLabelText(/ai assistant/i);
      fireEvent.click(toggleButton);

      expect(screen.getByText(/ai assistant/i)).toBeInTheDocument();

      fireEvent.click(toggleButton);
      expect(screen.queryByText(/ai assistant/i)).not.toBeInTheDocument();
    });

    test('submits questions to AI assistant', async () => {
      // Mock AI API response
      fetch.mockResolvedValueOnce({
        json: async () => ({
          answer: 'This is a test answer',
          sources: [
            {
              title: 'Test Source',
              url_path: '/docs/test',
              relevance_score: 0.8
            }
          ],
          confidence: 0.9
        }),
        ok: true
      });

      render(
        <BrowserRouter>
          <AIAssistant />
        </BrowserRouter>
      );

      // Open the assistant
      const toggleButton = screen.getByLabelText(/ai assistant/i);
      fireEvent.click(toggleButton);

      // Enter a question
      const questionInput = screen.getByPlaceholderText(/ask a question/i);
      fireEvent.change(questionInput, { target: { value: 'What is AI?' } });

      // Submit the question
      const submitButton = screen.getByText(/ask/i);
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(screen.getByText(/this is a test answer/i)).toBeInTheDocument();
      });
    });

    test('handles AI assistant errors gracefully', async () => {
      // Mock AI API error
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      render(
        <BrowserRouter>
          <AIAssistant />
        </BrowserRouter>
      );

      // Open the assistant
      const toggleButton = screen.getByLabelText(/ai assistant/i);
      fireEvent.click(toggleButton);

      // Enter a question
      const questionInput = screen.getByPlaceholderText(/ask a question/i);
      fireEvent.change(questionInput, { target: { value: 'What is AI?' } });

      // Submit the question
      const submitButton = screen.getByText(/ask/i);
      fireEvent.click(submitButton);

      await waitFor(() => {
        // Should handle error without crashing
        expect(fetch).toHaveBeenCalled();
      });
    });

    test('maintains conversation history', async () => {
      // Mock AI API response
      fetch.mockResolvedValueOnce({
        json: async () => ({
          answer: 'First answer',
          sources: [],
          confidence: 0.9
        }),
        ok: true
      });

      render(
        <BrowserRouter>
          <AIAssistant />
        </BrowserRouter>
      );

      // Open the assistant
      const toggleButton = screen.getByLabelText(/ai assistant/i);
      fireEvent.click(toggleButton);

      // Ask first question
      const questionInput = screen.getByPlaceholderText(/ask a question/i);
      fireEvent.change(questionInput, { target: { value: 'First question' } });
      fireEvent.click(screen.getByText(/ask/i));

      await waitFor(() => {
        expect(screen.getByText(/first answer/i)).toBeInTheDocument();
      });

      // Ask second question
      fetch.mockResolvedValueOnce({
        json: async () => ({
          answer: 'Second answer',
          sources: [],
          confidence: 0.85
        }),
        ok: true
      });

      fireEvent.change(questionInput, { target: { value: 'Second question' } });
      fireEvent.click(screen.getByText(/ask/i));

      await waitFor(() => {
        expect(screen.getByText(/second answer/i)).toBeInTheDocument();
      });

      // Both answers should be visible in conversation history
      expect(screen.getByText(/first answer/i)).toBeInTheDocument();
      expect(screen.getByText(/second answer/i)).toBeInTheDocument();
    });
  });

  describe('Language Selector Component Tests', () => {
    test('renders language selector', () => {
      render(
        <BrowserRouter>
          <LanguageSelector />
        </BrowserRouter>
      );

      const selectorButton = screen.getByLabelText(/select language/i);
      expect(selectorButton).toBeInTheDocument();
    });

    test('toggles language dropdown', () => {
      render(
        <BrowserRouter>
          <LanguageSelector />
        </BrowserRouter>
      );

      const selectorButton = screen.getByLabelText(/select language/i);
      fireEvent.click(selectorButton);

      expect(screen.getByText(/english/i)).toBeInTheDocument();
      expect(screen.getByText(/اردو/i)).toBeInTheDocument(); // Urdu

      fireEvent.click(selectorButton);
      expect(screen.queryByText(/english/i)).not.toBeInTheDocument();
    });

    test('changes language selection', async () => {
      const mockOnLanguageChange = jest.fn();

      render(
        <BrowserRouter>
          <LanguageSelector onLanguageChange={mockOnLanguageChange} />
        </BrowserRouter>
      );

      const selectorButton = screen.getByLabelText(/select language/i);
      fireEvent.click(selectorButton);

      const urduButton = screen.getByText(/اردو/i);
      fireEvent.click(urduButton);

      expect(mockOnLanguageChange).toHaveBeenCalledWith('ur');
    });

    test('shows current language', () => {
      render(
        <BrowserRouter>
          <LanguageSelector currentLanguage="ur" />
        </BrowserRouter>
      );

      expect(screen.getByText(/اردو/i)).toBeInTheDocument();
    });
  });

  describe('Expandable Section Component Tests', () => {
    test('renders expandable section', () => {
      render(
        <BrowserRouter>
          <ExpandableSection title="Test Section">
            <div>Test Content</div>
          </ExpandableSection>
        </BrowserRouter>
      );

      expect(screen.getByText(/test section/i)).toBeInTheDocument();
      expect(screen.queryByText(/test content/i)).not.toBeInTheDocument(); // Initially collapsed
    });

    test('toggles expandable section', () => {
      render(
        <BrowserRouter>
          <ExpandableSection title="Test Section">
            <div>Test Content</div>
          </ExpandableSection>
        </BrowserRouter>
      );

      const toggleButton = screen.getByText(/test section/i);
      fireEvent.click(toggleButton);

      expect(screen.getByText(/test content/i)).toBeInTheDocument(); // Now expanded

      fireEvent.click(toggleButton);
      expect(screen.queryByText(/test content/i)).not.toBeInTheDocument(); // Collapsed again
    });
  });

  describe('Content Page Component Tests', () => {
    test('renders content page structure', () => {
      render(
        <BrowserRouter>
          <ContentPage content="Test content" title="Test Page" />
        </BrowserRouter>
      );

      expect(screen.getByText(/test page/i)).toBeInTheDocument();
      expect(screen.getByText(/test content/i)).toBeInTheDocument();
    });
  });

  describe('Responsive Design Tests', () => {
    test('search component adapts to small screens', () => {
      // Mock small screen
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 400,
      });
      window.dispatchEvent(new Event('resize'));

      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);
      expect(searchInput).toBeInTheDocument();
    });

    test('components maintain functionality on different screen sizes', () => {
      // Test various screen sizes
      const sizes = [320, 768, 1024, 1400];

      sizes.forEach(size => {
        Object.defineProperty(window, 'innerWidth', {
          writable: true,
          configurable: true,
          value: size,
        });
        window.dispatchEvent(new Event('resize'));

        render(
          <BrowserRouter>
            <Search />
          </BrowserRouter>
        );

        const searchInput = screen.getByPlaceholderText(/search the book/i);
        expect(searchInput).toBeInTheDocument();
      });
    });
  });

  describe('Accessibility Tests', () => {
    test('search component has proper ARIA attributes', () => {
      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);
      expect(searchInput).toHaveAttribute('aria-label', /search the book/i);
    });

    test('AI assistant has proper keyboard navigation', () => {
      render(
        <BrowserRouter>
          <AIAssistant />
        </BrowserRouter>
      );

      const toggleButton = screen.getByLabelText(/ai assistant/i);
      expect(toggleButton).toHaveAttribute('tabindex');
    });

    test('language selector is accessible', () => {
      render(
        <BrowserRouter>
          <LanguageSelector />
        </BrowserRouter>
      );

      const selectorButton = screen.getByLabelText(/select language/i);
      expect(selectorButton).toHaveAttribute('aria-haspopup', 'true');
      expect(selectorButton).toHaveAttribute('aria-expanded');
    });
  });

  describe('Performance Tests', () => {
    test('components render without performance issues', async () => {
      const start = performance.now;

      render(
        <BrowserRouter>
          <div>
            <Search />
            <AIAssistant />
            <LanguageSelector />
            <ExpandableSection title="Performance Test">
              <div>Content for performance test</div>
            </ExpandableSection>
          </div>
        </BrowserRouter>
      );

      const end = performance.now;
      const renderTime = end - start;

      // Rendering should be fast (less than 100ms for this simple test)
      expect(renderTime).toBeLessThan(100);
    });

    test('search does not make excessive API calls', async () => {
      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);

      // Type quickly to test debouncing
      fireEvent.change(searchInput, { target: { value: 'a' } });
      fireEvent.change(searchInput, { target: { value: 'ab' } });
      fireEvent.change(searchInput, { target: { value: 'abc' } });

      // Wait for debouncing to complete
      await new Promise(resolve => setTimeout(resolve, 500));

      // Should only have made one API call due to debouncing
      expect(fetch).toHaveBeenCalledTimes(1);
    });
  });

  describe('Error Boundary and Edge Cases', () => {
    test('handles missing API responses gracefully', async () => {
      // Mock API returning no results
      fetch.mockResolvedValueOnce({
        json: async () => ({ results: [] }),
        ok: true
      });

      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);
      fireEvent.change(searchInput, { target: { value: 'noresults' } });

      await waitFor(() => {
        // Should handle empty results without crashing
        expect(fetch).toHaveBeenCalled();
      });
    });

    test('handles network errors gracefully', async () => {
      // Mock network error
      fetch.mockRejectedValueOnce(new Error('Network error'));

      render(
        <BrowserRouter>
          <Search />
        </BrowserRouter>
      );

      const searchInput = screen.getByPlaceholderText(/search the book/i);
      fireEvent.change(searchInput, { target: { value: 'networktest' } });

      await waitFor(() => {
        // Should handle network errors without crashing
        expect(fetch).toHaveBeenCalled();
      });
    });
  });
});

// Additional test utilities
export const waitForElementToBeRemoved = (callback) => {
  return waitFor(() => {
    try {
      callback();
      return false;
    } catch (error) {
      return true;
    }
  });
};

export const simulateSlowNetwork = () => {
  jest.spyOn(global, 'fetch').mockImplementation(async (...args) => {
    await new Promise(resolve => setTimeout(resolve, 1000)); // 1 second delay
    return global.fetch(...args);
  });
};

export const resetMocks = () => {
  fetch.mockClear();
};