from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.api_key import APIKeyCreate, APIKeyResponse
from app.services import api_key_service

router = APIRouter(prefix="/api-keys", tags=["api-keys"])

@router.post("/generate", response_model=APIKeyResponse, status_code=201)
def generate_api_key(
    api_key_data: APIKeyCreate,
    db: Session = Depends(get_db)
):
    """Generate a new API key"""
    return api_key_service.create_api_key(db, api_key_data)

@router.get("/", response_model=List[APIKeyResponse])
def list_api_keys(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all API keys"""
    return api_key_service.get_all_api_keys(db, skip, limit)

@router.delete("/{key_id}", status_code=204)
def deactivate_api_key(
    key_id: int,
    db: Session = Depends(get_db)
):
    """Deactivate an API key"""
    if not api_key_service.deactivate_api_key(db, key_id):
        raise HTTPException(status_code=404, detail="API Key not found")
    return None

