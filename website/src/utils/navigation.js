// Navigation utilities for smooth transitions between book sections

class NavigationManager {
  constructor() {
    this.isTransitioning = false;
    this.transitionDuration = 300; // ms
  }

  // Smooth scroll to element with ID
  smoothScrollTo(targetId, offset = 0) {
    if (this.isTransitioning) return;

    const element = document.getElementById(targetId);
    if (!element) return;

    this.isTransitioning = true;

    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - offset;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });

    // Reset transition flag after duration
    setTimeout(() => {
      this.isTransitioning = false;
    }, this.transitionDuration);
  }

  // Navigate to next section
  navigateNext() {
    const currentSection = this.getCurrentSection();
    const nextSection = this.getNextSection(currentSection);

    if (nextSection) {
      this.navigateToSection(nextSection);
    }
  }

  // Navigate to previous section
  navigatePrev() {
    const currentSection = this.getCurrentSection();
    const prevSection = this.getPrevSection(currentSection);

    if (prevSection) {
      this.navigateToSection(prevSection);
    }
  }

  // Get current section based on scroll position
  getCurrentSection() {
    const sections = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    const scrollPosition = window.scrollY + window.innerHeight / 2;

    for (let i = sections.length - 1; i >= 0; i--) {
      const section = sections[i];
      const sectionTop = section.offsetTop;

      if (scrollPosition >= sectionTop) {
        return section;
      }
    }

    return sections[0] || null;
  }

  // Get next section
  getNextSection(currentSection) {
    if (!currentSection) return null;

    const allSections = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
    const currentIndex = allSections.indexOf(currentSection);

    return allSections[currentIndex + 1] || null;
  }

  // Get previous section
  getPrevSection(currentSection) {
    if (!currentSection) return null;

    const allSections = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
    const currentIndex = allSections.indexOf(currentSection);

    return allSections[currentIndex - 1] || null;
  }

  // Navigate to specific section
  navigateToSection(section) {
    if (!section || this.isTransitioning) return;

    this.isTransitioning = true;
    const targetId = section.id || this.generateIdFromText(section.textContent);

    // If section doesn't have an ID, create one temporarily
    if (!section.id) {
      section.id = targetId;
    }

    this.smoothScrollTo(targetId, 60); // 60px offset for fixed header

    // Remove temporary ID after navigation
    setTimeout(() => {
      if (section.id === targetId) {
        section.removeAttribute('id');
      }
      this.isTransitioning = false;
    }, this.transitionDuration);
  }

  // Generate ID from text content
  generateIdFromText(text) {
    return text
      .toLowerCase()
      .replace(/[^\w\s-]/g, '') // Remove special characters
      .replace(/\s+/g, '-') // Replace spaces with hyphens
      .trim();
  }

  // Set up keyboard shortcuts for navigation
  setupKeyboardShortcuts() {
    document.addEventListener('keydown', (event) => {
      // Skip if focusing on input elements
      if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        return;
      }

      switch (event.key) {
        case 'ArrowRight':
          event.preventDefault();
          this.navigateNext();
          break;
        case 'ArrowLeft':
          event.preventDefault();
          this.navigatePrev();
          break;
        case 'PageDown':
          event.preventDefault();
          window.scrollBy({ top: window.innerHeight * 0.8, behavior: 'smooth' });
          break;
        case 'PageUp':
          event.preventDefault();
          window.scrollBy({ top: -window.innerHeight * 0.8, behavior: 'smooth' });
          break;
      }
    });
  }

  // Initialize navigation manager
  initialize() {
    this.setupKeyboardShortcuts();

    // Set up intersection observers for section tracking
    this.setupSectionTracking();
  }

  // Set up intersection observers for section tracking
  setupSectionTracking() {
    const sections = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    const options = {
      rootMargin: '-30% 0px -70% 0px', // Trigger when section is in middle of viewport
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Highlight current section in sidebar or TOC
          this.highlightCurrentSection(entry.target);
        }
      });
    }, options);

    sections.forEach(section => observer.observe(section));
  }

  // Highlight current section in UI
  highlightCurrentSection(currentSection) {
    // Remove previous highlights
    document.querySelectorAll('.section-highlighted').forEach(el => {
      el.classList.remove('section-highlighted');
    });

    // Add highlight to current section
    currentSection.classList.add('section-highlighted');

    // You could also update a progress indicator or sidebar here
    this.updateProgressIndicator(currentSection);
  }

  // Update progress indicator
  updateProgressIndicator(currentSection) {
    const progressContainer = document.querySelector('.reading-progress');
    if (progressContainer) {
      const allSections = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
      const currentIndex = Array.from(allSections).indexOf(currentSection);
      const progressPercent = (currentIndex / allSections.length) * 100;

      progressContainer.style.width = `${progressPercent}%`;
    }
  }
}

// Initialize navigation manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  const navManager = new NavigationManager();
  navManager.initialize();
});

// Export for use in React components
export default NavigationManager;