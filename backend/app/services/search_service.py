from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.models.search_index import SearchIndex
from app.models.book_content import BookContent
import logging
import re

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        pass

    def index_content(self, db: Session, content_id: str, title: str, content: str, url_path: str, tags: List[str] = None) -> bool:
        """Index content for search."""
        try:
            # Clean and prepare content for indexing
            clean_content = self._clean_content(content)
            preview = self._create_preview(clean_content)

            # Check if index entry already exists
            existing_index = db.query(SearchIndex).filter(SearchIndex.url_path == url_path).first()

            if existing_index:
                # Update existing index
                existing_index.title = title
                existing_index.content_preview = preview
                existing_index.tags = tags or []
            else:
                # Create new index entry
                search_index = SearchIndex(
                    title=title,
                    content_preview=preview,
                    url_path=url_path,
                    tags=tags or []
                )
                db.add(search_index)

            db.commit()
            logger.info(f"Successfully indexed content: {url_path}")
            return True
        except Exception as e:
            logger.error(f"Error indexing content {url_path}: {str(e)}")
            db.rollback()
            return False

    def index_all_content(self, db: Session) -> int:
        """Index all existing content in the database."""
        try:
            # Get all book content
            all_content = db.query(BookContent).all()
            indexed_count = 0

            for content in all_content:
                success = self.index_content(
                    db=db,
                    content_id=content.id,
                    title=content.title,
                    content=content.content,
                    url_path=f"/docs/{content.slug}",
                    tags=[]  # Extract from metadata if available
                )
                if success:
                    indexed_count += 1

            logger.info(f"Indexed {indexed_count} content items")
            return indexed_count
        except Exception as e:
            logger.error(f"Error indexing all content: {str(e)}")
            return 0

    def search(self, db: Session, query: str, limit: int = 10, offset: int = 0, filters: Dict[str, Any] = None, include_highlights: bool = True) -> List[Dict[str, Any]]:
        """Search for content based on query string."""
        try:
            # Basic full-text search using SQL LIKE operator
            # In a real implementation, you'd use a proper search engine like Elasticsearch or PostgreSQL full-text search
            search_query = db.query(SearchIndex)

            # Apply text search
            if query:
                # Search in title and content preview
                search_query = search_query.filter(
                    SearchIndex.title.ilike(f'%{query}%') |
                    SearchIndex.content_preview.ilike(f'%{query}%')
                )

            # Apply filters
            if filters:
                if 'tags' in filters and filters['tags']:
                    # Filter by tags - find any records that have any of the provided tags
                    search_query = search_query.filter(
                        SearchIndex.tags.overlap(filters['tags'])
                    )

                if 'chapter' in filters:
                    # This is a simplified approach - in a real implementation you'd need to join with BookContent
                    # to filter by chapter number from the content metadata
                    chapter_filter = f"chapter-{filters['chapter']}"
                    search_query = search_query.filter(
                        SearchIndex.url_path.ilike(f'%{chapter_filter}%')
                    )

            # Execute query and get results with offset and limit
            results = search_query.offset(offset).limit(limit).all()

            # Format results
            formatted_results = []
            for result in results:
                preview = result.content_preview[:200] + "..." if len(result.content_preview) > 200 else result.content_preview

                # Add highlights if requested
                if include_highlights:
                    preview = self._highlight_matches(preview, query)

                formatted_results.append({
                    "id": self._extract_content_id_from_path(result.url_path),  # Would need to store content_id in index
                    "title": self._highlight_matches(result.title, query) if include_highlights else result.title,
                    "url_path": result.url_path,
                    "preview": preview,
                    "relevance_score": self._calculate_relevance_score(query, result.title, result.content_preview),
                    "tags": result.tags,
                    "created_at": result.created_at.isoformat() if result.created_at else None,
                    "updated_at": result.updated_at.isoformat() if result.updated_at else None
                })

            # Sort by relevance score
            formatted_results.sort(key=lambda x: x["relevance_score"], reverse=True)

            return formatted_results
        except Exception as e:
            logger.error(f"Error searching: {str(e)}")
            return []

    def get_total_search_count(self, db: Session, query: str, filters: Dict[str, Any] = None) -> int:
        """Get total count of search results."""
        try:
            # Basic full-text search using SQL LIKE operator
            search_query = db.query(SearchIndex)

            # Apply text search
            if query:
                # Search in title and content preview
                search_query = search_query.filter(
                    SearchIndex.title.ilike(f'%{query}%') |
                    SearchIndex.content_preview.ilike(f'%{query}%')
                )

            # Apply filters
            if filters:
                if 'tags' in filters and filters['tags']:
                    # Filter by tags - find any records that have any of the provided tags
                    search_query = search_query.filter(
                        SearchIndex.tags.overlap(filters['tags'])
                    )

                if 'chapter' in filters:
                    # This is a simplified approach - in a real implementation you'd need to join with BookContent
                    # to filter by chapter number from the content metadata
                    chapter_filter = f"chapter-{filters['chapter']}"
                    search_query = search_query.filter(
                        SearchIndex.url_path.ilike(f'%{chapter_filter}%')
                    )

            # Return count
            return search_query.count()
        except Exception as e:
            logger.error(f"Error getting search count: {str(e)}")
            return 0

    def _highlight_matches(self, text: str, query: str) -> str:
        """Highlight query matches in text."""
        if not query:
            return text

        import re
        # Escape special regex characters in query
        escaped_query = re.escape(query)
        # Create a regex pattern that matches the query (case-insensitive)
        pattern = f'({escaped_query})'
        # Replace matches with highlighted version
        highlighted_text = re.sub(pattern, r'<mark>\1</mark>', text, flags=re.IGNORECASE)
        return highlighted_text

    def get_suggestions(self, db: Session, query: str, limit: int = 5) -> List[str]:
        """Get search suggestions for auto-complete based on titles and content."""
        try:
            # Search for titles that start with or contain the query
            suggestions = set()  # Use set to avoid duplicates

            # Search in titles for exact matches first
            title_matches = db.query(SearchIndex.title).filter(
                SearchIndex.title.ilike(f'{query}%')
            ).distinct().limit(limit).all()

            for title, in title_matches:
                suggestions.add(title)

            # If we don't have enough suggestions, also search for partial matches
            if len(suggestions) < limit:
                partial_matches = db.query(SearchIndex.title).filter(
                    SearchIndex.title.ilike(f'%{query}%')
                ).distinct().limit(limit - len(suggestions)).all()

                for title, in partial_matches:
                    suggestions.add(title)

            # Convert to list and limit the results
            suggestions_list = list(suggestions)[:limit]

            # Sort by relevance (titles that start with query first)
            suggestions_list.sort(key=lambda x: (not x.lower().startswith(query.lower()), x.lower()))

            return suggestions_list
        except Exception as e:
            logger.error(f"Error getting suggestions: {str(e)}")
            # Return a few sample suggestions in case of error
            return [f"{query} basics", f"{query} concepts", f"{query} examples"][:limit]

    def _clean_content(self, content: str) -> str:
        """Clean content by removing markdown formatting."""
        # Remove markdown links
        clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        # Remove markdown bold/italic
        clean = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', clean)
        clean = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', clean)
        # Remove code blocks
        clean = re.sub(r'`([^`]+)`', r'\1', clean)
        clean = re.sub(r'```[\s\S]*?```', '', clean)
        # Remove headers
        clean = re.sub(r'^#+\s*', '', clean, flags=re.MULTILINE)
        # Remove extra whitespace
        clean = re.sub(r'\s+', ' ', clean)
        return clean.strip()

    def _create_preview(self, content: str, length: int = 300) -> str:
        """Create a preview snippet for search results."""
        if len(content) <= length:
            return content
        else:
            # Find a good breaking point (sentence end or word boundary)
            preview = content[:length]
            last_sentence = preview.rfind('.')
            last_space = preview.rfind(' ')

            if last_sentence > length * 0.7:  # If sentence end is reasonably close to the limit
                preview = content[:last_sentence + 1]
            elif last_space > length * 0.8:  # If word boundary is close to the limit
                preview = content[:last_space]

            return preview.strip() + "..."

    def _calculate_relevance_score(self, query: str, title: str, content: str) -> float:
        """Calculate a basic relevance score."""
        query_lower = query.lower()
        title_lower = title.lower()
        content_lower = content.lower()

        score = 0.0

        # Higher weight for matches in title
        if query_lower in title_lower:
            score += 0.7 * query_lower.count(query_lower)

        # Lower weight for matches in content
        if query_lower in content_lower:
            score += 0.3 * min(content_lower.count(query_lower), 5)  # Cap content matches

        # Normalize score between 0 and 1
        return min(score, 1.0)

    def _extract_content_id_from_path(self, path: str) -> str:
        """Extract content ID from URL path (placeholder implementation)."""
        # In a real implementation, you'd store the content_id in the search index
        # This is a simplified approach
        return path.replace('/docs/', '').replace('/', '-')

# Create a global instance
search_service = SearchService()