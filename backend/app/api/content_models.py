from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Translation(BaseModel):
    language_code: str
    title: str
    content: str
    summary: Optional[str] = None

class ContentResponse(BaseModel):
    id: str
    title: str
    slug: str
    content: str
    chapter_number: int
    section_number: int
    parent_id: Optional[str] = None
    metadata: dict = {}
    translations: List[Translation] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

class ContentListResponse(BaseModel):
    id: str
    title: str
    slug: str
    chapter_number: int
    section_number: int
    url_path: str
    preview: str
    tags: List[str]
    reading_time: int
    available_translations: List[str] = []

class ContentListPaginatedResponse(BaseModel):
    items: List[ContentListResponse]
    pagination: dict

class TableOfContentsChapter(BaseModel):
    id: str
    number: int
    title: str
    url_path: str
    sections: List[dict]

class TableOfContentsResponse(BaseModel):
    title: str
    chapters: List[TableOfContentsChapter]

class ReadingProgressRequest(BaseModel):
    session_id: str
    content_id: str
    position: dict

class ReadingProgressResponse(BaseModel):
    status: str
    expires_at: datetime

class ReadingProgressGetResponse(BaseModel):
    position: dict
    preferences: dict