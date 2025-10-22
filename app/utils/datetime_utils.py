from datetime import datetime, timedelta
from typing import Optional

def get_current_timestamp() -> datetime:
    """Get current timestamp"""
    return datetime.now()

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string"""
    return dt.strftime(format_str)

def add_days(dt: datetime, days: int) -> datetime:
    """Add days to a datetime"""
    return dt + timedelta(days=days)

def is_expired(expiry_date: Optional[datetime]) -> bool:
    """Check if a date has expired"""
    if not expiry_date:
        return False
    return datetime.now() > expiry_date

