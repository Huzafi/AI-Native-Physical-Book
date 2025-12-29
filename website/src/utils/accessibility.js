// Accessibility utilities for the AI-Native Book

class AccessibilityManager {
  constructor() {
    this.fontSizeMultiplier = 1;
    this.isHighContrast = false;
    this.isReducedMotion = this.checkReducedMotionPreference();
  }

  // Check if user prefers reduced motion
  checkReducedMotionPreference() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  // Toggle high contrast mode
  toggleHighContrast() {
    this.isHighContrast = !this.isHighContrast;

    if (this.isHighContrast) {
      document.body.classList.add('high-contrast-mode');
    } else {
      document.body.classList.remove('high-contrast-mode');
    }

    this.updateAccessibilitySettings();
  }

  // Adjust font size
  adjustFontSize(multiplier) {
    this.fontSizeMultiplier = Math.max(0.8, Math.min(1.5, this.fontSizeMultiplier + multiplier));
    document.body.style.fontSize = `${16 * this.fontSizeMultiplier}px`;

    this.updateAccessibilitySettings();
  }

  // Initialize accessibility settings from localStorage
  initializeFromStorage() {
    const settings = localStorage.getItem('accessibility-settings');
    if (settings) {
      const parsed = JSON.parse(settings);
      this.fontSizeMultiplier = parsed.fontSizeMultiplier || 1;
      this.isHighContrast = parsed.isHighContrast || false;

      // Apply settings
      document.body.style.fontSize = `${16 * this.fontSizeMultiplier}px`;
      if (this.isHighContrast) {
        document.body.classList.add('high-contrast-mode');
      }
    }
  }

  // Save accessibility settings to localStorage
  updateAccessibilitySettings() {
    const settings = {
      fontSizeMultiplier: this.fontSizeMultiplier,
      isHighContrast: this.isHighContrast,
      timestamp: Date.now()
    };

    localStorage.setItem('accessibility-settings', JSON.stringify(settings));
  }

  // Set up keyboard navigation enhancements
  setupKeyboardNavigation() {
    // Add skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link';
    skipLink.style.cssText = `
      position: absolute;
      top: -40px;
      left: 6px;
      background: #000;
      color: #fff;
      padding: 8px;
      text-decoration: none;
      z-index: 1000;
    `;

    skipLink.addEventListener('focus', () => {
      skipLink.style.top = '6px';
    });

    skipLink.addEventListener('blur', () => {
      skipLink.style.top = '-40px';
    });

    document.body.insertBefore(skipLink, document.body.firstChild);
  }

  // Initialize accessibility features
  initialize() {
    this.initializeFromStorage();
    this.setupKeyboardNavigation();

    // Listen for reduced motion preference changes
    window.matchMedia('(prefers-reduced-motion: reduce)')
      .addEventListener('change', (e) => {
        this.isReducedMotion = e.matches;
      });
  }
}

// Initialize accessibility manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  const accessibilityManager = new AccessibilityManager();
  accessibilityManager.initialize();
});

// Export for use in React components
export default AccessibilityManager;