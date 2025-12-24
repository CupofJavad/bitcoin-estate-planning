"""Enhanced error handling utilities.

Patterns inspired by:
- Bitcoin Core: Comprehensive error classification
- BTCPay Server: User-friendly error messages
- eigenwallet/core: Robust error recovery
"""

import logging
from typing import Dict, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorCategory(str, Enum):
    """Error categories for better error handling."""
    VALIDATION = "validation"
    NETWORK = "network"
    API = "api"
    SECURITY = "security"
    RATE_LIMIT = "rate_limit"
    CACHE = "cache"
    UNKNOWN = "unknown"


class BitcoinServiceError(Exception):
    """Base exception for Bitcoin service errors."""

    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        user_message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize error.

        Args:
            message: Internal error message (for logging)
            category: Error category
            user_message: User-friendly error message
            details: Additional error details
        """
        super().__init__(message)
        self.category = category
        self.user_message = user_message or self._get_default_user_message(category)
        self.details = details or {}

    def _get_default_user_message(self, category: ErrorCategory) -> str:
        """Get default user-friendly message for category."""
        messages = {
            ErrorCategory.VALIDATION: "Invalid input. Please check and try again.",
            ErrorCategory.NETWORK: "Network error. Please try again later.",
            ErrorCategory.API: "Service temporarily unavailable. Please try again later.",
            ErrorCategory.SECURITY: "Security validation failed.",
            ErrorCategory.RATE_LIMIT: "Too many requests. Please wait a moment.",
            ErrorCategory.CACHE: "Cache error. Please try again.",
            ErrorCategory.UNKNOWN: "An error occurred. Please try again.",
        }
        return messages.get(category, messages[ErrorCategory.UNKNOWN])

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for API responses."""
        return {
            "error": self.user_message,
            "category": self.category.value,
            "details": self.details,
        }


def handle_bitcoin_error(
    error: Exception, context: Optional[str] = None
) -> BitcoinServiceError:
    """Handle and classify Bitcoin-related errors.

    Args:
        error: The exception that occurred
        context: Additional context about where error occurred

    Returns:
        Classified BitcoinServiceError
    """
    error_str = str(error).lower()

    # Classify error
    if "timeout" in error_str or "connection" in error_str:
        category = ErrorCategory.NETWORK
    elif "rate limit" in error_str or "429" in error_str:
        category = ErrorCategory.RATE_LIMIT
    elif "invalid" in error_str or "validation" in error_str:
        category = ErrorCategory.VALIDATION
    elif "https" in error_str or "ssl" in error_str or "certificate" in error_str:
        category = ErrorCategory.SECURITY
    elif "api" in error_str or "http" in error_str:
        category = ErrorCategory.API
    else:
        category = ErrorCategory.UNKNOWN

    # Log error with context
    logger.error(
        f"Bitcoin service error [{category.value}]: {str(error)}"
        + (f" (context: {context})" if context else "")
    )

    return BitcoinServiceError(
        message=str(error),
        category=category,
        details={"context": context} if context else {},
    )


def log_security_event(
    event_type: str, address: Optional[str] = None, details: Optional[Dict] = None
) -> None:
    """Log security-relevant events.

    Args:
        event_type: Type of security event
        address: Bitcoin address (if relevant)
        details: Additional details
    """
    log_data = {
        "event_type": event_type,
        "address": address[:10] + "..." if address else None,  # Partial address only
        "details": details or {},
    }
    logger.warning(f"Security event: {log_data}")

