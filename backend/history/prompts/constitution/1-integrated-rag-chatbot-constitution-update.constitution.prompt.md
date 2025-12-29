---
id: 1
title: integrated-rag-chatbot-constitution-update
stage: constitution
date_iso: 2025-12-27
surface: agent
model: Qwen Code
feature: none
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - rag-chatbot
  - project-setup
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests_yaml: []
prompt_text: |
  /sp.constitution
  Project: Integrated RAG Chatbot Development for a Published Book
  Core principles:

  Accuracy in responses based on book's content and user-selected text
  User-centric design for seamless integration and interactivity within the book
  Scalability and efficiency using serverless and cloud-free tiers
  Security and privacy in handling user queries and data
  Adaptability to alternative APIs and tools (e.g., Cohere instead of OpenAI)
  Key standards:
  Use Cohere API for generation and embeddings, not OpenAI
  Implement with SpecifyKit Plus and Qwen CLI for high-quality development
  Backend built with FastAPI for API endpoints
  Database: Neon Serverless Postgres for structured data storage
  Vector database: Qdrant Cloud Free Tier for retrieval
  Responses must be contextually relevant, citing book sections where applicable
  Support for queries on full book content or user-selected text only
  Code quality: Clean, modular, well-documented with comments and README
  Testing: Unit tests for core functions, integration tests for RAG pipeline
  Constraints:
  No use of OpenAI APIs; strictly Cohere for LLM interactions
  Free-tier limitations: Optimize for Qdrant free tier storage and Neon serverless scalability
  Deployment: Embeddable in published book format (e.g., web-based or interactive e-book)
  Development tools: SpecifyKit Plus for specifications, Qwen CLI for CLI-based workflows
  Language: Python for backend, with JavaScript if needed for frontend embedding
  Success criteria:
  Chatbot accurately answers 95%+ of test queries on book content
  Handles user-selected text isolation without leaking external context
  Successfully embedded and functional in a sample published book environment
  Zero critical bugs in production simulation
  Positive user feedback on response quality and speed
response_text: |
  Created and updated the project constitution for the Integrated RAG Chatbot Development project. The constitution includes six core principles:
  
  1. Accuracy in Responses - ensuring all responses are grounded in book content
  2. User-Centric Design - focusing on seamless integration and interactivity
  3. Scalability and Efficiency - leveraging serverless and cloud-free technologies
  4. Security and Privacy - protecting user data and queries
  5. Adaptability to Alternative APIs - supporting interchangeable AI services
  6. Quality Code and Documentation - maintaining clean, well-documented code
  
  The constitution also defines standards, constraints, and success criteria specific to the project. Additionally, I updated the template files (plan-template.md, spec-template.md, tasks-template.md) to align with the new constitution, adding compliance checks and requirements that reflect the new principles.
outcome: |
  The project constitution has been successfully created and all relevant template files have been updated to align with the new principles. The constitution will now guide all development practices for the Integrated RAG Chatbot project.
evaluation: |
  The constitution has been created with clear principles, standards, constraints, and success criteria. Template files have been updated to incorporate constitution checks. The next step would be to implement features according to these principles.
---

# Integrated RAG Chatbot Development Constitution

## Core Principles

### I. Accuracy in Responses
All responses must be grounded in the book's content and user-selected text. The system must ensure factual accuracy and avoid hallucinations by strictly referencing provided source material. Responses should cite specific book sections where applicable to maintain trust and verifiability.

### II. User-Centric Design
Prioritize seamless integration and interactivity within the book experience. The chatbot interface must be intuitive, responsive, and enhance the reading experience without disruption. All features should be designed with the end-user's reading journey in mind.

### III. Scalability and Efficiency
Leverage serverless and cloud-free tier technologies to ensure cost-effective scaling. The architecture must optimize resource usage while maintaining performance under varying loads. Efficiency in API calls, storage, and computation is paramount for sustainable operation.

### IV. Security and Privacy
Protect user queries and data with robust security measures. All data handling must comply with privacy regulations and best practices. User interactions should be secured end-to-end with minimal data retention policies.

### V. Adaptability to Alternative APIs
Design the system to support interchangeable AI services (e.g., Cohere instead of OpenAI). The architecture must allow for API switching without major refactoring, ensuring resilience against vendor changes or API availability issues.

### VI. Quality Code and Documentation
Maintain clean, modular, well-documented code with comprehensive comments and README files. All components should be testable, maintainable, and follow established coding standards to ensure long-term project health.

## Standards

### Technology Stack
- Use Cohere API for generation and embeddings, not OpenAI
- Implement with SpecifyKit Plus and Qwen CLI for high-quality development
- Backend built with FastAPI for API endpoints
- Database: Neon Serverless Postgres for structured data storage
- Vector database: Qdrant Cloud Free Tier for retrieval

### Implementation Requirements
- Responses must be contextually relevant, citing book sections where applicable
- Support for queries on full book content or user-selected text only
- Code quality: Clean, modular, well-documented with comments and README
- Testing: Unit tests for core functions, integration tests for RAG pipeline

## Constraints

### API Limitations
- No use of OpenAI APIs; strictly Cohere for LLM interactions
- Free-tier limitations: Optimize for Qdrant free tier storage and Neon serverless scalability

### Deployment Requirements
- Deployment: Embeddable in published book format (e.g., web-based or interactive e-book)
- Development tools: SpecifyKit Plus for specifications, Qwen CLI for CLI-based workflows
- Language: Python for backend, with JavaScript if needed for frontend embedding

## Success Criteria

### Performance Metrics
- Chatbot accurately answers 95%+ of test queries on book content
- Handles user-selected text isolation without leaking external context
- Successfully embedded and functional in a sample published book environment
- Zero critical bugs in production simulation
- Positive user feedback on response quality and speed

## Governance

This constitution governs all development practices for the Integrated RAG Chatbot project. All features, changes, and implementations must align with these principles. Amendments to this constitution require documentation of the change, approval from project stakeholders, and a migration plan for existing code.

All pull requests and code reviews must verify compliance with these principles. Deviations must be explicitly justified and approved. Use the project documentation for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2025-12-27