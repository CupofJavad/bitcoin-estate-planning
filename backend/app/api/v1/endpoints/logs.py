"""Error logging endpoint for frontend error tracking."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

router = APIRouter()


class ErrorLogRequest(BaseModel):
    """Error log request model."""
    timestamp: str
    level: str  # error, warning, info, debug
    message: str
    error: Optional[Dict[str, Any]] = None
    context: Dict[str, Any]
    request: Optional[Dict[str, Any]] = None
    response: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


@router.post("/logs/error")
async def log_error(error_log: ErrorLogRequest):
    """
    Log an error from the frontend.
    
    This endpoint receives error logs from the frontend and stores them
    for debugging and analysis.
    """
    try:
        # In production, you would store this in a database or logging service
        # For now, we'll just log it to the backend logs
        
        import logging
        logger = logging.getLogger("frontend_errors")
        
        log_data = {
            "timestamp": error_log.timestamp,
            "level": error_log.level,
            "message": error_log.message,
            "error": error_log.error,
            "context": error_log.context,
            "request": error_log.request,
            "response": error_log.response,
            "metadata": error_log.metadata,
        }
        
        if error_log.level == "error":
            logger.error(f"Frontend Error: {error_log.message}", extra=log_data)
        elif error_log.level == "warning":
            logger.warning(f"Frontend Warning: {error_log.message}", extra=log_data)
        else:
            logger.info(f"Frontend Log: {error_log.message}", extra=log_data)
        
        return {"status": "logged", "timestamp": datetime.utcnow().isoformat()}
    
    except Exception as e:
        # Don't fail if logging fails
        import logging
        logger = logging.getLogger("frontend_errors")
        logger.error(f"Failed to log frontend error: {e}")
        return {"status": "error", "message": str(e)}


@router.get("/logs/errors")
async def get_error_logs(
    limit: int = 100,
    level: Optional[str] = None,
):
    """
    Get error logs (for debugging purposes).
    
    In production, this would query a database or logging service.
    For now, this is a placeholder.
    """
    # TODO: Implement actual log retrieval from database
    return {
        "logs": [],
        "message": "Log retrieval not yet implemented. Logs are currently only written to backend logs.",
    }

