# Implementation Plan: AI-Native Book with Docusaurus

**Branch**: `001-ai-book-docusaurus` | **Date**: 2025-12-16 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/001-ai-book-docusaurus/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The AI-Native Book with Docusaurus project implements a book-first reading experience with Docusaurus as the primary frontend technology. The system provides structured book content with chapter navigation, search functionality, and interactive elements (expandable sections, visuals, callouts) that enhance reading without interrupting flow. An optional AI assistant powered by RAG technology provides answers based only on book content, remaining invisible during normal reading. The architecture follows a static-first approach with minimal backend services (FastAPI + Qdrant + Neon) that support search and AI features while gracefully degrading to static content when unavailable.

## Technical Context

**Language/Version**: Node.js (for Docusaurus), Python 3.11 (for FastAPI backend), JavaScript/TypeScript
**Primary Dependencies**: Docusaurus, React, FastAPI, Qdrant, Neon PostgreSQL
**Storage**: Markdown/MDX files for content, Qdrant for vector search, Neon PostgreSQL for metadata
**Testing**: Jest for frontend, pytest for backend
**Target Platform**: Web (server-rendered static site with optional API interactions)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Page load < 2 seconds for 95% of requests, AI responses within 5 seconds, search results within 3 seconds
**Constraints**: Static-first architecture, minimal JavaScript, no user authentication required, reader-centric experience
**Scale/Scope**: Support for horizontal scaling with load balancing, 99% uptime for static content delivery

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Book-First Principle
✅ PASS: The design prioritizes creating a book-like reading experience with clear chapter/section hierarchy. All features enhance the book-like nature rather than turning it into a platform.

### Reader-Centric Principle
✅ PASS: The design prioritizes the reader's experience of exploring ideas. No forms, signups, or configuration options required. Interactive elements are optional and lightweight.

### AI-Native Content Principle
✅ PASS: The content will be presented from an AI perspective, showing perception → reasoning → action loops, comparing human intelligence vs machine intelligence.

### Docusaurus-First Principle
✅ PASS: Docusaurus is the primary technology stack for frontend development with content in Markdown/MDX format and small reusable React components inside MDX files.

### Minimal Interactivity Principle
✅ PASS: Interactive elements (expandable sections, visuals, callouts) are lightweight and optional, enhancing rather than disrupting the reading experience. The book is fully readable without clicking anything.

### Static-First Architecture Principle
✅ PASS: The architecture prioritizes static content delivery with minimal backend intelligence. Backend functionality (FastAPI + Qdrant + Neon) remains invisible to the reader and doesn't affect core reading experience.

### Performance Standards
✅ PASS: Performance goals align with constitution requirements: page load < 3 seconds, minimal client-side computation, and minimal JavaScript.

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-book-docusaurus/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure for AI-Native Book
website/
├── docusaurus.config.js     # Docusaurus configuration
├── package.json            # Frontend dependencies
├── src/
│   ├── components/         # React components for interactive elements
│   │   ├── ExpandableSection/
│   │   ├── VisualDiagrams/
│   │   └── Callouts/
│   ├── pages/              # Custom pages if needed
│   ├── css/                # Custom styles
│   └── theme/              # Custom theme components
├── docs/                   # Book content in MDX format organized by chapters
│   ├── intro.mdx
│   ├── chapter-1/
│   │   ├── section-1.mdx
│   │   └── section-2.mdx
│   └── chapter-n/
├── static/                 # Static assets
└── tests/                  # Frontend tests

backend/
├── app/
│   ├── main.py             # FastAPI application entry point
│   ├── models/             # Data models
│   ├── api/                # API endpoints for search and AI assistant
│   │   ├── search.py
│   │   └── ai_assistant.py
│   ├── services/           # Business logic
│   │   ├── search_service.py
│   │   └── rag_service.py
│   └── database/           # Database connection and setup
├── requirements.txt        # Backend dependencies
├── alembic/                # Database migrations
└── tests/                  # Backend tests

# Shared resources
specs/                      # Feature specifications
.history/                   # Prompt history records
.templates/                 # Template files
```

**Structure Decision**: Web application structure selected with separate frontend (Docusaurus-based website) and backend (FastAPI API) components. The frontend serves static content with Docusaurus while the backend provides optional services for search and AI features. This structure supports the static-first architecture while allowing for optional backend intelligence as specified in the requirements.

## Phase 0: Outline & Research

Completed research to resolve all technical unknowns:

- **Technology Stack**: Confirmed Docusaurus for frontend, FastAPI + Qdrant + Neon for backend
- **Architecture Pattern**: Validated static-first approach with optional backend services
- **Interactive Elements**: Resolved implementation approach for expandable sections, visuals, and callouts within MDX
- **AI Integration**: Confirmed RAG approach using vector database for content-based responses
- **Content Structure**: Validated MDX format for rich, interactive documentation

**Output**: research.md with all technical decisions documented

## Phase 1: Design & Contracts

Completed design artifacts:

- **Data Model**: Created data-model.md with entities for Book Content, AI Knowledge Base, Search Index, Translation Set, and User Session
- **API Contracts**: Created API contracts in /contracts/ directory (search-api.md and content-api.md)
- **Quickstart Guide**: Created quickstart.md with setup and deployment instructions
- **Agent Context**: Updated agent context with new technology stack information

**Output**: data-model.md, quickstart.md, /contracts/*, and updated agent context

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
