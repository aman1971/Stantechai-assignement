from fastapi import HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import api_key_service

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(
    api_key: str = Depends(api_key_header),
    db: Session = Depends(get_db)
):
    """Verify API key from header"""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is missing"
        )
    
    db_api_key = api_key_service.get_api_key_by_key(db, api_key)
    
    if not db_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    api_key_service.update_last_used(db, db_api_key)
    return db_api_key

