# Research Summary: Integrated RAG Chatbot for Published Book

## Decision: Use Cohere API for RAG Implementation
**Rationale**: The project constitution explicitly requires using Cohere API for generation and embeddings, not OpenAI. Cohere provides reliable, enterprise-grade models with good performance for RAG applications. The API is well-documented and supports both embedding generation and text generation needed for our RAG pipeline.

**Alternatives considered**: 
- OpenAI API (rejected due to constitutional constraint)
- Self-hosted models like Hugging Face transformers (rejected due to free-tier and scalability constraints)
- Other commercial APIs like AI21 (rejected due to constitutional constraint)

## Decision: Qdrant Vector Database for Embedding Storage
**Rationale**: The project constitution requires using Qdrant Cloud Free Tier for retrieval. Qdrant is a high-performance vector database that supports semantic search, which is essential for RAG applications. The free tier provides 1GB storage and 1M vectors, which should be sufficient for most book content.

**Alternatives considered**:
- Pinecone (rejected due to constitutional constraint)
- Weaviate (rejected due to constitutional constraint)
- Chroma (rejected due to constitutional constraint)

## Decision: Neon Serverless Postgres for Metadata Storage
**Rationale**: The project constitution requires using Neon Serverless Postgres for structured data storage. This will store metadata about book sections, citations, and query logs. Neon's serverless architecture aligns with the scalability and efficiency principles.

**Alternatives considered**:
- Traditional PostgreSQL (rejected due to constitutional constraint)
- MongoDB (rejected due to constitutional constraint)

## Decision: FastAPI for Backend Framework
**Rationale**: The project constitution requires using FastAPI for API endpoints. FastAPI provides high performance, automatic API documentation, and excellent support for async operations, which are important for RAG applications that involve multiple API calls.

**Alternatives considered**:
- Flask (rejected due to constitutional constraint)
- Django (rejected due to constitutional constraint)

## Decision: Embedding Chunking Strategy
**Rationale**: For book content, we'll use a sliding window approach with overlapping chunks to preserve context across chunk boundaries. This will help ensure that queries spanning multiple chunks can still get accurate answers. Chunks will be approximately 512-1024 tokens to balance retrieval accuracy with computational efficiency.

**Alternatives considered**:
- Fixed-length chunks without overlap (rejected due to potential context loss)
- Sentence-level chunks (rejected due to potential for very short chunks)
- Paragraph-level chunks (rejected due to potential for very long chunks)

## Decision: Citation Format
**Rationale**: Citations will include the chapter/section name, page number (if available), and a short text snippet. This provides users with clear references to verify the information and find the original context in the book.

**Alternatives considered**:
- Just page numbers (rejected due to lack of context)
- Just section names (rejected due to potential ambiguity)