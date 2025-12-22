import os
import re
from sqlalchemy.orm import Session
from typing import List
import logging
from app.models.book_content import BookContent
from app.models.search_index import SearchIndex
from app.services.content_service import content_service

logger = logging.getLogger(__name__)

class ContentIndexingService:
    def __init__(self):
        pass

    def index_content_from_files(self, db: Session, docs_path: str = "website/docs"):
        """Index content from MDX files in the docs directory."""
        indexed_count = 0

        # Walk through the docs directory
        for root, dirs, files in os.walk(docs_path):
            for file in files:
                if file.endswith('.mdx'):
                    file_path = os.path.join(root, file)
                    self._process_mdx_file(db, file_path)
                    indexed_count += 1

        logger.info(f"Indexed {indexed_count} MDX files from {docs_path}")
        return indexed_count

    def _process_mdx_file(self, db: Session, file_path: str):
        """Process a single MDX file and create content entries."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter and content
        frontmatter, mdx_content = self._extract_frontmatter(content)

        # Extract title from frontmatter or content
        title = frontmatter.get('title', self._extract_title_from_content(mdx_content))
        slug = frontmatter.get('slug', self._generate_slug_from_path(file_path))

        # Extract chapter and section numbers from path
        chapter_number, section_number = self._extract_chapter_section_numbers(file_path)

        # Create content entry
        content_obj = content_service.create_content(
            db=db,
            title=title,
            slug=slug,
            content=mdx_content,
            chapter_number=chapter_number,
            section_number=section_number,
            metadata=frontmatter
        )

        # Create search index entry
        search_preview = self._create_search_preview(mdx_content)
        search_index = SearchIndex(
            title=title,
            content_preview=search_preview,
            url_path=slug,
            tags=frontmatter.get('tags', [])
        )
        db.add(search_index)
        db.commit()

        logger.info(f"Indexed content: {title} ({slug})")

    def _extract_frontmatter(self, content: str) -> tuple:
        """Extract frontmatter from MDX content."""
        frontmatter = {}

        # Look for frontmatter between --- delimiters
        if content.startswith('---'):
            end_frontmatter = content.find('---', 3)
            if end_frontmatter != -1:
                frontmatter_str = content[3:end_frontmatter].strip()
                frontmatter = self._parse_frontmatter(frontmatter_str)
                content = content[end_frontmatter + 3:].strip()

        return frontmatter, content

    def _parse_frontmatter(self, frontmatter_str: str) -> dict:
        """Parse frontmatter string into a dictionary."""
        frontmatter = {}
        for line in frontmatter_str.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')  # Remove quotes
                frontmatter[key] = value
        return frontmatter

    def _extract_title_from_content(self, content: str) -> str:
        """Extract title from content if not in frontmatter."""
        # Look for the first heading
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()  # Remove '# ' prefix
        return "Untitled"

    def _generate_slug_from_path(self, file_path: str) -> str:
        """Generate slug from file path."""
        # Remove file extension and website/docs prefix
        relative_path = file_path.replace('website/docs/', '').replace('.mdx', '')
        # Replace path separators with hyphens
        slug = relative_path.replace('/', '-').replace('\\', '-')
        # Ensure it's URL-friendly
        slug = re.sub(r'[^a-zA-Z0-9_-]', '-', slug)
        return slug

    def _extract_chapter_section_numbers(self, file_path: str) -> tuple:
        """Extract chapter and section numbers from file path."""
        # Look for patterns like chapter-1/section-2.mdx
        path_parts = file_path.replace('website/docs/', '').split('/')
        chapter_number = 0
        section_number = 0

        # Extract chapter number
        for part in path_parts:
            if part.startswith('chapter-'):
                try:
                    chapter_number = int(part.split('-')[1])
                    break
                except (ValueError, IndexError):
                    continue

        # Extract section number from filename
        filename = os.path.basename(file_path).replace('.mdx', '')
        if filename.startswith('section-'):
            try:
                section_number = int(filename.split('-')[1])
            except (ValueError, IndexError):
                pass

        return chapter_number, section_number

    def _create_search_preview(self, content: str, length: int = 200) -> str:
        """Create a preview snippet for search results."""
        # Remove markdown formatting and limit length
        clean_content = re.sub(r'\[.*?\]\(.*?\)', '', content)  # Remove links
        clean_content = re.sub(r'`.*?`', '', clean_content)  # Remove code blocks
        clean_content = re.sub(r'#+\s*', '', clean_content)  # Remove headers

        if len(clean_content) > length:
            clean_content = clean_content[:length] + "..."

        return clean_content.strip()

# Create a global instance
content_indexing_service = ContentIndexingService()