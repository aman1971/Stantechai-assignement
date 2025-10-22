from sqlalchemy.orm import Session
from app.models.api_key import APIKey
from app.schemas.api_key import APIKeyCreate
import secrets
from datetime import datetime

def generate_api_key() -> str:
    """Generate a secure random API key"""
    return secrets.token_urlsafe(48)

def create_api_key(db: Session, api_key_data: APIKeyCreate) -> APIKey:
    """Create a new API key"""
    key = generate_api_key()
    db_api_key = APIKey(
        key=key,
        name=api_key_data.name,
        is_active=True
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key

def get_api_key_by_key(db: Session, key: str) -> APIKey:
    """Get API key by key string"""
    return db.query(APIKey).filter(APIKey.key == key, APIKey.is_active == True).first()

def update_last_used(db: Session, api_key: APIKey):
    """Update last used timestamp"""
    api_key.last_used_at = datetime.now()
    db.commit()

def get_all_api_keys(db: Session, skip: int = 0, limit: int = 100):
    """Get all API keys"""
    return db.query(APIKey).offset(skip).limit(limit).all()

def deactivate_api_key(db: Session, key_id: int):
    """Deactivate an API key"""
    api_key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if api_key:
        api_key.is_active = False
        db.commit()
        return True
    return False

