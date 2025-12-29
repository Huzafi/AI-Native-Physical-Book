// Performance optimization utilities for the AI-Native Book

class PerformanceManager {
  constructor() {
    this.pageLoadStartTime = Date.now();
    this.metrics = {
      pageLoadTime: 0,
      domContentLoaded: 0,
      resourcesLoaded: 0,
      interactiveTime: 0
    };
  }

  // Measure page load performance
  measurePageLoad() {
    if (document.readyState === 'complete') {
      this.metrics.pageLoadTime = Date.now() - this.pageLoadStartTime;
      this.reportPerformance();
    } else {
      window.addEventListener('load', () => {
        this.metrics.pageLoadTime = Date.now() - this.pageLoadStartTime;
        this.reportPerformance();
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      this.metrics.domContentLoaded = Date.now() - this.pageLoadStartTime;
    });
  }

  // Report performance metrics
  reportPerformance() {
    // Log performance metrics to console (in development)
    if (process.env.NODE_ENV !== 'production') {
      console.group('📖 Page Performance Metrics');
      console.log(`Page Load Time: ${this.metrics.pageLoadTime}ms`);
      console.log(`DOM Content Loaded: ${this.metrics.domContentLoaded}ms`);
      console.groupEnd();
    }

    // In production, you might send these metrics to an analytics service
    if (process.env.NODE_ENV === 'production') {
      // Send metrics to analytics service
      this.sendPerformanceMetrics();
    }
  }

  // Send performance metrics to analytics
  sendPerformanceMetrics() {
    // Implementation would send metrics to your analytics service
    // This is a placeholder for actual implementation
    if ('sendBeacon' in navigator) {
      const perfData = {
        pageLoadTime: this.metrics.pageLoadTime,
        path: window.location.pathname,
        timestamp: Date.now(),
        userAgent: navigator.userAgent
      };

      // navigator.sendBeacon('/api/performance', JSON.stringify(perfData));
    }
  }

  // Lazy load images
  setupLazyLoading() {
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            if (img.dataset.src) {
              img.src = img.dataset.src;
              img.removeAttribute('data-src');
              img.classList.remove('lazy');
            }
            if (img.dataset.srcset) {
              img.srcset = img.dataset.srcset;
              img.removeAttribute('data-srcset');
            }
            observer.unobserve(img);
          }
        });
      });

      document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
      });
    }
  }

  // Optimize content rendering
  optimizeContentRendering() {
    // Defer non-critical CSS
    this.deferNonCriticalCSS();

    // Optimize font loading
    this.optimizeFontLoading();
  }

  // Defer non-critical CSS
  deferNonCriticalCSS() {
    // This would move non-critical CSS to be loaded after initial render
    // Implementation would depend on your specific CSS structure
  }

  // Optimize font loading
  optimizeFontLoading() {
    // Preload critical fonts
    const fontLinks = document.querySelectorAll('link[rel="preload"][as="font"]');
    fontLinks.forEach(link => {
      link.onload = () => {
        link.parentElement.classList.add('fonts-loaded');
      };
    });
  }

  // Implement resource caching
  setupResourceCaching() {
    // This would implement caching strategies for API calls and resources
    // Using localStorage, sessionStorage, or service workers as appropriate
    this.setupAPICache();
  }

  // Set up API response caching
  setupAPICache() {
    const cache = new Map();
    const cacheTimeout = 5 * 60 * 1000; // 5 minutes

    // Override fetch to add caching
    const originalFetch = window.fetch;
    window.fetch = async (...args) => {
      const [resource, config] = args;

      // Only cache GET requests
      if (!config || !config.method || config.method === 'GET') {
        const cacheKey = `${resource}_${JSON.stringify(config)}`;

        // Check if we have a cached response
        if (cache.has(cacheKey)) {
          const cached = cache.get(cacheKey);
          if (Date.now() - cached.timestamp < cacheTimeout) {
            return Promise.resolve(cached.response);
          } else {
            // Remove expired cache
            cache.delete(cacheKey);
          }
        }
      }

      // Make the actual request
      const response = await originalFetch(...args);

      // Cache GET responses
      if (!config || !config.method || config.method === 'GET') {
        const cacheKey = `${resource}_${JSON.stringify(config)}`;
        // Clone the response before caching
        const responseClone = response.clone();
        cache.set(cacheKey, {
          response: responseClone,
          timestamp: Date.now()
        });
      }

      return response;
    };
  }

  // Initialize performance optimizations
  initialize() {
    this.measurePageLoad();
    this.setupLazyLoading();
    this.optimizeContentRendering();
    this.setupResourceCaching();

    // Monitor for performance issues
    this.setupPerformanceMonitoring();
  }

  // Set up performance monitoring
  setupPerformanceMonitoring() {
    // Monitor for long tasks that might block the main thread
    if ('performance' in window && 'getEntriesByType' in performance) {
      // Monitor for long tasks (>50ms)
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          if (entry.duration > 50) {
            console.warn('Long task detected:', entry);
            // In production, you might send this to an error tracking service
          }
        });
      });

      observer.observe({ entryTypes: ['longtask'] });
    }
  }
}

// Initialize performance manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  const perfManager = new PerformanceManager();
  perfManager.initialize();
});

// Export for use in React components
export default PerformanceManager;