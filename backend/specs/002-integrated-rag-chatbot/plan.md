# Implementation Plan: Integrated RAG Chatbot for Published Book

**Branch**: `002-integrated-rag-chatbot` | **Date**: 2025-12-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-integrated-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a high-accuracy RAG (Retrieval-Augmented Generation) chatbot embedded within a published book environment. The system will use Cohere APIs to answer queries strictly from book content or user-selected text, while ensuring scalability, security, and compliance with free-tier infrastructure constraints. The solution will include full-book querying capabilities and an isolation mode for user-selected text queries, with strict context boundaries to prevent external content leakage.

## Technical Context

**Language/Version**: Python 3.11 (with JavaScript for any frontend embedding needs)
**Primary Dependencies**: FastAPI, Cohere SDK, Qdrant client, asyncpg (for Neon Postgres), Pydantic, SQLAlchemy
**Storage**: Neon Serverless Postgres for structured data, Qdrant Cloud Free Tier for vector storage
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server (cloud deployment), with web-based frontend embedding
**Project Type**: Web application (backend API with potential frontend integration)
**Performance Goals**: Response time under 2 seconds for 95% of queries, 95%+ accuracy on book content queries
**Constraints**: Qdrant Cloud Free Tier limitations (1GB storage, 1M vectors), Neon Serverless resource constraints, Cohere API rate limits
**Scale/Scope**: Single book instance with multiple users, optimized for cost-effective serverless operation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification
- [x] Accuracy in responses based on book's content and user-selected text (Principle I)
- [x] User-centric design for seamless integration and interactivity (Principle II)
- [x] Scalability and efficiency using serverless and cloud-free tiers (Principle III)
- [x] Security and privacy in handling user queries and data (Principle IV)
- [x] Adaptability to alternative APIs and tools (Principle V)
- [x] Code quality: Clean, modular, well-documented (Principle VI)
- [x] Use Cohere API for generation and embeddings, not OpenAI (Standard)
- [x] Backend built with FastAPI for API endpoints (Standard)
- [x] Database: Neon Serverless Postgres for structured data storage (Standard)
- [x] Vector database: Qdrant Cloud Free Tier for retrieval (Standard)
- [x] No use of OpenAI APIs; strictly Cohere for LLM interactions (Constraint)
- [x] Free-tier limitations: Optimize for Qdrant free tier storage and Neon serverless scalability (Constraint)

## Project Structure

### Documentation (this feature)

```text
specs/002-integrated-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # Data models for book content, queries, responses
│   ├── services/        # RAG orchestration, embedding, generation services
│   ├── api/             # FastAPI endpoints for querying
│   ├── utils/           # Utility functions for text processing, citations
│   └── config/          # Configuration for Cohere, Qdrant, Neon
├── tests/
│   ├── unit/            # Unit tests for individual components
│   ├── integration/     # Integration tests for RAG pipeline
│   └── contract/        # Contract tests for API endpoints
├── scripts/             # Scripts for data ingestion and vectorization
└── requirements.txt     # Python dependencies
```

**Structure Decision**: Web application backend structure chosen to support the RAG chatbot API. The backend will handle all RAG operations (retrieval, generation, citation) and provide API endpoints for frontend integration. The structure separates concerns into models, services, API endpoints, and utilities to maintain clean architecture and support the constitutional requirements of modularity and testability.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
