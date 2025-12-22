import React, { useState, useEffect, useCallback } from 'react';
import clsx from 'clsx';
import styles from './Search.module.css';
import Highlight from './Highlight';

// Debounce utility function
const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

const Search = ({ placeholder = "Search the book..." }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [error, setError] = useState(null);

  // Debounced query to prevent excessive API calls
  const debouncedQuery = useDebounce(query, 300);

  // Simple cache to store recent search results
  const [cache, setCache] = useState({});

  // Handle search input changes
  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
  };

  // Effect to handle debounced search
  useEffect(() => {
    // Get suggestions if query is long enough but not too long
    if (debouncedQuery.length >= 1 && debouncedQuery.length < 20) {
      fetchSuggestions(debouncedQuery);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }

    // Perform search if query is long enough
    if (debouncedQuery.length >= 2) {
      performSearch(debouncedQuery);
      setShowResults(true);
    } else {
      setResults([]);
      setShowResults(false);
    }
  }, [debouncedQuery]);

  // Fetch search suggestions
  const fetchSuggestions = async (searchQuery) => {
    setIsLoadingSuggestions(true);

    try {
      const response = await fetch(`/api/search/suggest?q=${encodeURIComponent(searchQuery)}&limit=5`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 429) {
          // Rate limited - use fallback suggestions
          console.warn('Rate limited for suggestions, using fallback');
        } else {
          throw new Error(`Suggestions API error: ${response.status}`);
        }
      }

      let suggestionsData = [];
      if (response.ok) {
        const data = await response.json();
        suggestionsData = data.suggestions || [];
      } else {
        // Fallback to mock suggestions if API fails
        suggestionsData = [
          `${searchQuery} artificial intelligence`,
          `${searchQuery} machine learning`,
          `${searchQuery} neural networks`,
          `${searchQuery} deep learning`,
          `${searchQuery} algorithms`,
        ].filter(suggestion => suggestion.toLowerCase().includes(searchQuery.toLowerCase()));
      }

      setSuggestions(suggestionsData);
      setShowSuggestions(true);
    } catch (err) {
      console.error('Suggestions error:', err);
      // Fallback to mock suggestions if API fails
      const mockSuggestions = [
        `${searchQuery} artificial intelligence`,
        `${searchQuery} machine learning`,
        `${searchQuery} neural networks`,
        `${searchQuery} deep learning`,
        `${searchQuery} algorithms`,
      ].filter(suggestion => suggestion.toLowerCase().includes(searchQuery.toLowerCase()));

      setSuggestions(mockSuggestions.slice(0, 5)); // Limit to 5 suggestions
    } finally {
      setIsLoadingSuggestions(false);
    }
  };

  // State for pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalResults, setTotalResults] = useState(0);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [hasPrevPage, setHasPrevPage] = useState(false);
  const itemsPerPage = 10;

  // Perform search API call
  const performSearch = async (searchQuery, page = 1) => {
    // Check if result is in cache for this specific page
    const cacheKey = `${searchQuery}_page_${page}`;
    if (cache[cacheKey]) {
      setResults(cache[cacheKey].results || []);
      setTotalResults(cache[cacheKey].total || 0);
      setCurrentPage(cache[cacheKey].page || 1);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery,
          limit: itemsPerPage,
          offset: (page - 1) * itemsPerPage,
          filters: {}
        }),
      });

      // Handle different response statuses gracefully
      if (response.status === 503) {
        // Service unavailable - likely backend issue
        setError("Search service is temporarily unavailable. Please try again later.");
        console.warn('Search service unavailable');
        return;
      } else if (response.status === 429) {
        // Rate limited
        setError("Too many search requests. Please wait before searching again.");
        return;
      } else if (!response.ok) {
        if (response.status >= 500) {
          // Server error - backend issue
          setError("Search service is experiencing issues. Content browsing is still available.");
          console.error(`Search API server error: ${response.status}`);
        } else {
          // Client error
          throw new Error(`Search API error: ${response.status}`);
        }
        return;
      }

      const data = await response.json();
      const resultsData = data.results || [];
      const total = data.total_count || resultsData.length;

      // Add to cache
      setCache(prevCache => ({
        ...prevCache,
        [cacheKey]: {
          results: resultsData,
          total: total,
          page: page
        }
      }));

      setResults(resultsData);
      setTotalResults(total);
      setCurrentPage(page);
      setHasNextPage((page * itemsPerPage) < total);
      setHasPrevPage(page > 1);
      setShowResults(true);
    } catch (err) {
      // Handle network errors and other exceptions
      if (err.name === 'TypeError' && err.message.includes('fetch')) {
        // Network error - backend is likely down
        setError("Unable to connect to search service. Please check your connection.");
        console.error('Network error during search:', err);
      } else {
        setError(err.message);
        console.error('Search error:', err);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Navigate to next page
  const goToNextPage = () => {
    const nextPage = currentPage + 1;
    performSearch(debouncedQuery, nextPage);
  };

  // Navigate to previous page
  const goToPreviousPage = () => {
    const prevPage = Math.max(1, currentPage - 1);
    performSearch(debouncedQuery, prevPage);
  };

  // Navigate to specific page
  const goToPage = (page) => {
    performSearch(debouncedQuery, page);
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.length >= 2) {
      performSearch(query);
    }
  };

  // Handle clicking outside to close results
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest(`.${styles.searchContainer}`)) {
        setShowResults(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

  return (
    <div className={styles.searchContainer}>
      <form onSubmit={handleSubmit} className={styles.searchForm}>
        <div className={styles.searchInputWrapper}>
          <input
            type="text"
            value={query}
            onChange={handleInputChange}
            placeholder={placeholder}
            className={styles.searchInput}
            onFocus={() => {
              if (query.length >= 1) setShowSuggestions(true);
              if (query.length >= 2) setShowResults(true);
            }}
          />
          {isLoading && (
            <div className={styles.loadingSpinner}>
              <div className={styles.spinner}></div>
            </div>
          )}
        </div>
      </form>

      {/* Suggestions dropdown */}
      {showSuggestions && suggestions.length > 0 && !showResults && (
        <div className={styles.suggestionsDropdown}>
          <ul className={styles.suggestionsList}>
            {suggestions.map((suggestion, index) => (
              <li key={index} className={styles.suggestionItem}>
                <button
                  className={styles.suggestionButton}
                  onClick={() => {
                    setQuery(suggestion);
                    setShowSuggestions(false);
                    if (suggestion.length >= 2) {
                      performSearch(suggestion);
                      setShowResults(true);
                    }
                  }}
                >
                  {suggestion}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Search results */}
      {showResults && (
        <div className={styles.searchResults}>
          {error && (
            <div className={styles.error}>
              Error: {error}
            </div>
          )}
          {results.length > 0 ? (
            <ul className={styles.resultsList}>
              {results.map((result, index) => (
                <li key={index} className={styles.resultItem}>
                  <a
                    href={result.url_path}
                    className={styles.resultLink}
                    onClick={() => {
                      setShowResults(false);
                      setShowSuggestions(false);
                    }}
                  >
                    <div className={styles.resultHeader}>
                      <h4 className={styles.resultTitle}>
                        <Highlight text={result.title} query={query} />
                      </h4>
                      {result.relevance_score !== undefined && (
                        <span className={styles.relevanceScore}>
                          {Math.round(result.relevance_score * 100)}%
                        </span>
                      )}
                    </div>
                    <p className={styles.resultPreview}>
                      <Highlight text={result.preview} query={query} />
                    </p>
                    <span className={styles.resultPath}>{result.url_path}</span>
                    {result.tags && result.tags.length > 0 && (
                      <div className={styles.resultTags}>
                        {result.tags.map((tag, tagIndex) => (
                          <span key={tagIndex} className={styles.tag}>
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </a>
                </li>
              ))}
            </ul>
          ) : query.length >= 2 && !isLoading ? (
            <div className={styles.noResults}>
              No results found for "{query}"
            </div>
          ) : null}

          {/* Pagination controls */}
          {results.length > 0 && totalResults > itemsPerPage && (
            <div className={styles.pagination}>
              <div className={styles.paginationInfo}>
                Showing {(currentPage - 1) * itemsPerPage + 1}-{Math.min(currentPage * itemsPerPage, totalResults)} of {totalResults} results
              </div>
              <div className={styles.paginationControls}>
                <button
                  className={clsx(styles.paginationButton, !hasPrevPage && styles.disabled)}
                  onClick={goToPreviousPage}
                  disabled={!hasPrevPage}
                >
                  Previous
                </button>

                {/* Page number buttons */}
                {Array.from({ length: Math.min(5, Math.ceil(totalResults / itemsPerPage)) }, (_, i) => {
                  const pageNum = Math.max(1, Math.min(
                    Math.ceil(totalResults / itemsPerPage) - 4,
                    Math.max(currentPage - 2, Math.min(currentPage + 2, Math.ceil(totalResults / itemsPerPage) - 2), 1)
                  ) + i);

                  // Only render if the page number is valid and within range
                  if (pageNum > 0 && pageNum <= Math.ceil(totalResults / itemsPerPage)) {
                    return (
                      <button
                        key={pageNum}
                        className={clsx(styles.paginationButton, styles.pageNumber, currentPage === pageNum && styles.active)}
                        onClick={() => goToPage(pageNum)}
                      >
                        {pageNum}
                      </button>
                    );
                  }
                  return null;
                })}

                <button
                  className={clsx(styles.paginationButton, !hasNextPage && styles.disabled)}
                  onClick={goToNextPage}
                  disabled={!hasNextPage}
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Search;