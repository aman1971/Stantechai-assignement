from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional
from math import ceil

T = TypeVar('T')

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number (starts from 1)")
    page_size: int = Field(10, ge=1, le=100, description="Items per page")

class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    pagination: PaginationMeta

def paginate_query(query, page: int, page_size: int):
    """
    Paginate a SQLAlchemy query
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        items: List of paginated items
        pagination_meta: Pagination metadata
    """
    total_items = query.count()
    total_pages = ceil(total_items / page_size) if total_items > 0 else 0
    
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    pagination_meta = PaginationMeta(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )
    
    return items, pagination_meta

