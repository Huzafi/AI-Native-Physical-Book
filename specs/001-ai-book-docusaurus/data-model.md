# Data Model: AI-Native Book with Docusaurus

## Entities

### Book Content
- **id**: string (unique identifier for the content)
- **title**: string (chapter/section title)
- **slug**: string (URL-friendly identifier)
- **content**: string (MDX content)
- **chapter_number**: integer (position in book hierarchy)
- **section_number**: integer (position within chapter)
- **parent_id**: string (optional, for nested sections)
- **created_at**: datetime
- **updated_at**: datetime
- **metadata**: JSON object (additional content metadata)

### AI Knowledge Base (Vector Store)
- **content_id**: string (reference to Book Content)
- **chunk_text**: string (text chunk for embedding)
- **embedding**: vector (vector representation of content)
- **metadata**: JSON object (content metadata for retrieval)

### Search Index
- **id**: string (unique identifier)
- **title**: string (content title)
- **content_preview**: string (shortened content for search results)
- **url_path**: string (path to content)
- **tags**: array of strings (content tags for filtering)
- **last_indexed**: datetime

### Translation Set
- **id**: string (unique identifier)
- **content_id**: string (reference to Book Content)
- **language_code**: string (e.g., 'ur' for Urdu)
- **translated_title**: string
- **translated_content**: string (translated MDX content)
- **summary**: string (optional summary in target language)
- **created_at**: datetime

### User Session (Temporary)
- **session_id**: string (temporary session identifier)
- **last_read_position**: JSON object (chapter/section/paragraph position)
- **preferences**: JSON object (reader preferences like language selection)
- **created_at**: datetime
- **expires_at**: datetime (short-lived session)

## Relationships

1. **Book Content** → **AI Knowledge Base**: One-to-Many (one content can have multiple chunks)
2. **Book Content** → **Search Index**: One-to-One (each content has one search index entry)
3. **Book Content** → **Translation Set**: One-to-Many (one content can have multiple translations)
4. **User Session** (temporary, not persisted)

## Validation Rules

### Book Content
- Title must be 1-200 characters
- Slug must be URL-friendly (alphanumeric, hyphens only)
- Content must be valid MDX format
- Chapter and section numbers must be positive integers
- Chapter numbers must be unique within a book

### AI Knowledge Base
- Content_id must reference an existing Book Content
- Chunk_text must be 50-1000 characters
- Embedding must be a valid vector representation

### Translation Set
- Language_code must be a valid ISO 639-1 or 639-2 code
- Content_id must reference an existing Book Content
- Each content_id can have only one translation per language_code

### Search Index
- URL path must be unique
- Content preview must be 50-300 characters