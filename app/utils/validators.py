import re
from typing import Optional

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_string_length(value: str, min_length: int = 1, max_length: Optional[int] = None) -> bool:
    """Validate string length"""
    if len(value) < min_length:
        return False
    if max_length and len(value) > max_length:
        return False
    return True

def sanitize_string(value: str) -> str:
    """Remove extra whitespace from string"""
    return " ".join(value.split())

