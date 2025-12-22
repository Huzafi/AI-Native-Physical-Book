# AI-Native Book on Physical & AI Humanoids Constitution

## Core Principles

### Book-First
The project prioritizes creating a book-like reading experience over building a platform. All features must enhance the book-like nature of the experience, not turn it into a dashboard or tool. The reader should feel like they are reading a real book, not interacting with a generator or SaaS application.

### Reader-Centric
All development decisions must prioritize the reader's experience of exploring ideas over data input or configuration. The reader never fills forms, signs up, or configures options. The book should be readable end-to-end without interruption, with interactions that feel optional and lightweight.

### AI-Native Content
Content must be presented from an AI perspective, showing perception → reasoning → action loops, comparing human intelligence vs machine intelligence, and presenting futures where AI and humans coexist. This does not mean auto-generation but explaining systems from an AI perspective.

### Docusaurus-First
The project uses Docusaurus as the primary technology stack for frontend development. All frontend functionality must be implemented using Docusaurus capabilities, with content in Markdown/MDX format, and small reusable React components inside MDX files.

### Minimal Interactivity
All interactive elements must be lightweight and never interrupt the reading flow. Interactions should be optional (expandable explanations, visual diagrams, reflection prompts) that enhance rather than disrupt the reading experience. The book should be fully readable without clicking anything.

### Static-First Architecture
The project prioritizes static content delivery with minimal backend intelligence. Any optional backend functionality must remain invisible to the reader and not affect the core book reading experience. Performance and simplicity take precedence over dynamic features.

## Technology Constraints

Frontend: Docusaurus only
Content: Markdown / MDX
Components: Small reusable React components inside MDX
Backend (optional): Minimal, invisible to reader
All code must follow the project's performance standards: page load < 3 seconds on low-end devices, no heavy client-side computation, no unnecessary JavaScript.

## UI/Design Standards

The UI must follow book-like design principles: centered layout with readable width, soft and calm color palette, minimal animations (scroll, expand, fade only), and mobile-first reading experience. Chapter design must be short, clear, concept-focused, using simple language with real-world analogies, including optional expandable sections, at least one visual or conceptual diagram, and avoiding long code blocks or heavy technical depth.

## Governance

This constitution supersedes all other development practices. All features must answer: "Does this enhance the reading experience?" All PRs and reviews must verify compliance with book-first principles. Any new feature that moves the project toward a platform or generator rather than a book requires explicit constitutional amendment. All changes must be small, testable, and reference code precisely.

**Version**: 1.0.0 | **Ratified**: 2025-12-15 | **Last Amended**: 2025-12-15
