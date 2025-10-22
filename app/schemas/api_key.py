from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class APIKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Name/description for the API key")

class APIKeyResponse(BaseModel):
    id: int
    key: str
    name: str
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime] = None

    class Config:
        from_attributes = True

