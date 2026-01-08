---
name: card-component
description: Create modern, accessible card components with advanced effects. Use when user wants card layouts, grid systems, or content containers.
---

# Modern Card Component Design

## Instructions
Create card components with these features:

### 1. **Shadow Effects & Depth**
   - Layered box shadows for depth
   - Elevation on hover
   - Soft, natural shadow progression
   - Inner shadows for inset effects

### 2. **Hover Animations**
   - Smooth scale transforms
   - Lift effects (translateY)
   - Border glow transitions
   - Image zoom effects
   - Content reveal animations

### 3. **Responsive Grid Layouts**
   - CSS Grid for modern layouts
   - Flexbox for card internals
   - Mobile-first approach
   - Breakpoint strategy (mobile, tablet, desktop)
   - Auto-fit and minmax for flexibility

### 4. **Image Optimization**
   - Lazy loading with loading="lazy"
   - Responsive images with srcset
   - Aspect ratio preservation
   - Object-fit for proper scaling
   - Placeholder/skeleton loading states

### 5. **Accessibility Best Practices**
   - Semantic HTML (article, section, figure)
   - ARIA labels where needed
   - Keyboard navigation support
   - Focus visible states
   - Sufficient color contrast
   - Screen reader friendly content

## Example Code

### Basic Card Structure (HTML)
```html
<article class="card" role="article" tabindex="0">
  <figure class="card__image-wrapper">
    <img
      src="image.jpg"
      srcset="image-320w.jpg 320w, image-640w.jpg 640w, image-1024w.jpg 1024w"
      sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw"
      alt="Descriptive alt text"
      loading="lazy"
      class="card__image"
    />
  </figure>

  <div class="card__content">
    <h3 class="card__title">Card Title</h3>
    <p class="card__description">Card description text goes here.</p>
    <a href="#" class="card__link" aria-label="Read more about Card Title">
      Read More
    </a>
  </div>
</article>
```

### Card Styles (CSS)
```css
/* Base Card Styles */
.card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);

  /* Layered shadows for depth */
  box-shadow:
    0 4px 6px rgba(0, 0, 0, 0.1),
    0 8px 16px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);

  /* Accessibility */
  position: relative;
  cursor: pointer;
}

/* Focus state for keyboard navigation */
.card:focus {
  outline: 2px solid #f39c12;
  outline-offset: 4px;
}

/* Hover effects */
.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow:
    0 8px 12px rgba(0, 0, 0, 0.15),
    0 16px 32px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(243, 156, 18, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border-color: rgba(243, 156, 18, 0.5);
}

/* Image wrapper with aspect ratio */
.card__image-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  margin: 0;
  background: rgba(0, 0, 0, 0.2);
}

/* Image optimization */
.card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.4s ease;
}

/* Image zoom on card hover */
.card:hover .card__image {
  transform: scale(1.1);
}

/* Card content area */
.card__content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.card__title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  line-height: 1.3;
}

.card__description {
  font-size: 0.95rem;
  color: #b0b0b0;
  line-height: 1.6;
  margin: 0;
}

.card__link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #f39c12;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  margin-top: auto;
}

.card__link:hover {
  color: #e08a0f;
  transform: translateX(4px);
}

.card__link:focus {
  outline: 2px solid #f39c12;
  outline-offset: 2px;
  border-radius: 4px;
}
```

### Responsive Grid Layout
```css
/* Grid container */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Tablet breakpoint */
@media (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2.5rem;
  }
}

/* Desktop breakpoint */
@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 3rem;
  }
}

/* Large desktop - max 4 columns */
@media (min-width: 1440px) {
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Mobile optimization */
@media (max-width: 767px) {
  .card-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    padding: 1rem;
  }

  .card__content {
    padding: 1rem;
  }
}
```

### Loading Skeleton (Optional)
```css
/* Skeleton loading state */
.card--loading {
  pointer-events: none;
}

.card--loading .card__image-wrapper {
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.05) 25%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.05) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.card--loading .card__title,
.card--loading .card__description {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: transparent;
}
```

### Advanced Card Variants

#### Glass Card (Enhanced Glassmorphism)
```css
.card--glass {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}
```

#### Gradient Border Card
```css
.card--gradient-border {
  position: relative;
  background: #1a1a1a;
  border: none;
}

.card--gradient-border::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  padding: 2px;
  background: linear-gradient(135deg, #f39c12, #e74c3c, #9b59b6);
  -webkit-mask:
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

#### Horizontal Card Layout
```css
.card--horizontal {
  display: flex;
  flex-direction: row;
}

.card--horizontal .card__image-wrapper {
  flex: 0 0 40%;
  aspect-ratio: 4 / 3;
}

.card--horizontal .card__content {
  flex: 1;
}

@media (max-width: 767px) {
  .card--horizontal {
    flex-direction: column;
  }

  .card--horizontal .card__image-wrapper {
    flex: 1;
    aspect-ratio: 16 / 9;
  }
}
```

## React Component Example

```jsx
import React from 'react';
import './Card.css';

const Card = ({
  image,
  imageAlt,
  title,
  description,
  link,
  loading = false,
  variant = 'default'
}) => {
  return (
    <article
      className={`card card--${variant} ${loading ? 'card--loading' : ''}`}
      role="article"
      tabIndex={0}
    >
      <figure className="card__image-wrapper">
        <img
          src={image}
          srcSet={`${image}?w=320 320w, ${image}?w=640 640w, ${image}?w=1024 1024w`}
          sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw"
          alt={imageAlt}
          loading="lazy"
          className="card__image"
        />
      </figure>

      <div className="card__content">
        <h3 className="card__title">{title}</h3>
        <p className="card__description">{description}</p>
        <a
          href={link}
          className="card__link"
          aria-label={`Read more about ${title}`}
        >
          Read More →
        </a>
      </div>
    </article>
  );
};

export default Card;
```

## Accessibility Checklist

- ✅ Use semantic HTML (`<article>`, `<figure>`, `<h3>`)
- ✅ Provide descriptive alt text for images
- ✅ Include ARIA labels for links
- ✅ Support keyboard navigation (tabindex, focus states)
- ✅ Ensure sufficient color contrast (WCAG AA minimum)
- ✅ Add focus-visible styles for keyboard users
- ✅ Use relative units (rem, em) for scalability
- ✅ Test with screen readers
- ✅ Provide skip links if needed
- ✅ Ensure touch targets are at least 44x44px

## Performance Tips

1. **Lazy Loading**: Use `loading="lazy"` for images below the fold
2. **Responsive Images**: Implement srcset and sizes attributes
3. **CSS Containment**: Use `contain: layout style paint` for better rendering
4. **Will-change**: Add `will-change: transform` sparingly for animated elements
5. **Reduce Repaints**: Use transform and opacity for animations
6. **Optimize Images**: Compress and serve WebP/AVIF formats
7. **Critical CSS**: Inline critical card styles for above-the-fold content

## Common Use Cases

- Blog post cards
- Product cards for e-commerce
- Team member profiles
- Portfolio items
- Feature highlights
- Testimonial cards
- Pricing cards
- Event cards
