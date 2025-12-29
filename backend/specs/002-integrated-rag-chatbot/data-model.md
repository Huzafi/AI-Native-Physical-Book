# Data Model: Integrated RAG Chatbot for Published Book

## Entities

### BookContent
- **id**: UUID (Primary Key)
- **title**: String (Book title)
- **author**: String (Book author)
- **isbn**: String (ISBN identifier, optional)
- **content**: Text (Full book content)
- **created_at**: DateTime (Timestamp of ingestion)
- **updated_at**: DateTime (Timestamp of last update)

### BookSection
- **id**: UUID (Primary Key)
- **book_id**: UUID (Foreign Key to BookContent)
- **section_title**: String (Title of the section/chapter)
- **content**: Text (Content of the section)
- **page_start**: Integer (Starting page number)
- **page_end**: Integer (Ending page number)
- **section_order**: Integer (Order of the section in the book)
- **vector_id**: String (ID in Qdrant vector store)
- **created_at**: DateTime (Timestamp of creation)

### Query
- **id**: UUID (Primary Key)
- **query_text**: Text (User's original query)
- **query_embedding**: JSON (Embedding vector stored as JSON)
- **query_type**: Enum (FULL_BOOK or USER_SELECTION)
- **user_selected_text**: Text (Optional text selected by user for isolation mode)
- **book_id**: UUID (Foreign Key to BookContent, null if user selection mode)
- **session_id**: String (ID to group related queries)
- **created_at**: DateTime (Timestamp of query)

### Response
- **id**: UUID (Primary Key)
- **query_id**: UUID (Foreign Key to Query)
- **response_text**: Text (Generated response)
- **citations**: JSON (List of citations with section/page info)
- **retrieved_chunks**: JSON (List of retrieved chunk IDs from vector store)
- **confidence_score**: Float (Confidence score of the response)
- **created_at**: DateTime (Timestamp of response generation)

### Citation
- **id**: UUID (Primary Key)
- **response_id**: UUID (Foreign Key to Response)
- **section_id**: UUID (Foreign Key to BookSection)
- **text_snippet**: Text (Short text snippet from the cited section)
- **page_number**: Integer (Page number of the citation)
- **confidence**: Float (Confidence of the citation relevance)

## Relationships

- BookContent (1) → BookSection (Many): One book can have many sections
- BookContent (Many) → Query (Many): Queries can be related to a specific book
- Query (1) → Response (1): Each query generates one response
- Response (1) → Citation (Many): Each response can have multiple citations
- BookSection (1) → Citation (Many): Citations reference specific sections

## Validation Rules

- BookContent: Title and author are required
- BookSection: Must have content, section_title, and be associated with a book
- Query: query_text is required; if query_type is USER_SELECTION, user_selected_text is required
- Response: Must be associated with a query and have response_text
- Citation: Must reference a valid response and section, with required text_snippet and page_number

## State Transitions

- BookContent: INGESTING → PROCESSED → AVAILABLE (for querying)
- Query: RECEIVED → EMBEDDING → RETRIEVING → GENERATING → COMPLETED
- Response: GENERATING → COMPLETED → CITED (citations added)