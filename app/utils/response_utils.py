from typing import Dict, Any, Optional

def success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Create a standardized success response"""
    return {
        "success": True,
        "message": message,
        "data": data
    }

def error_response(message: str, error_code: Optional[str] = None) -> Dict[str, Any]:
    """Create a standardized error response"""
    response = {
        "success": False,
        "message": message
    }
    if error_code:
        response["error_code"] = error_code
    return response

