"""
Custom exceptions for AI Practice Platform

Provides structured error handling throughout the application.
"""

from typing import Optional, Dict, Any


class PlatformException(Exception):
    """Base exception for all platform errors"""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "PLATFORM_ERROR"
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.message,
            "code": self.error_code,
            "details": self.details
        }


# =============================================================================
# Validation Errors
# =============================================================================

class ValidationError(PlatformException):
    """Raised when input validation fails"""

    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict] = None):
        super().__init__(message, "VALIDATION_ERROR", details)
        self.field = field


class InvalidEmailError(ValidationError):
    """Raised when email format is invalid"""

    def __init__(self, email: str):
        super().__init__(
            f"Invalid email format: {email}",
            field="email",
            details={"provided_value": email}
        )


class InvalidSectorError(ValidationError):
    """Raised when sector is not supported"""

    def __init__(self, sector: str, valid_sectors: list):
        super().__init__(
            f"Invalid sector: {sector}",
            field="sector",
            details={"provided_value": sector, "valid_sectors": valid_sectors}
        )


class MissingFieldError(ValidationError):
    """Raised when a required field is missing"""

    def __init__(self, field: str):
        super().__init__(f"Required field missing: {field}", field=field)


# =============================================================================
# Assessment Errors
# =============================================================================

class AssessmentError(PlatformException):
    """Base exception for assessment-related errors"""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "ASSESSMENT_ERROR", details)


class AssessmentNotFoundError(AssessmentError):
    """Raised when an assessment cannot be found"""

    def __init__(self, assessment_id: str):
        super().__init__(
            f"Assessment not found: {assessment_id}",
            details={"assessment_id": assessment_id}
        )


class NoActiveAssessmentError(AssessmentError):
    """Raised when no active assessment session exists"""

    def __init__(self):
        super().__init__("No active assessment session")


# =============================================================================
# Chat Errors
# =============================================================================

class ChatError(PlatformException):
    """Base exception for chat-related errors"""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "CHAT_ERROR", details)


class NoChatSessionError(ChatError):
    """Raised when no active chat session exists"""

    def __init__(self):
        super().__init__("No active chat session")


class ChatSessionNotFoundError(ChatError):
    """Raised when a chat session cannot be found"""

    def __init__(self, session_id: str):
        super().__init__(
            f"Chat session not found: {session_id}",
            details={"session_id": session_id}
        )


# =============================================================================
# AI/Claude Errors
# =============================================================================

class ClaudeAPIError(PlatformException):
    """Base exception for Claude API errors"""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "CLAUDE_API_ERROR", details)


class ClaudeUnavailableError(ClaudeAPIError):
    """Raised when Claude API is not available"""

    def __init__(self):
        super().__init__(
            "Claude API is not available. Please check your API key configuration."
        )


class ClaudeRateLimitError(ClaudeAPIError):
    """Raised when Claude API rate limit is exceeded"""

    def __init__(self, retry_after: Optional[int] = None):
        super().__init__(
            "Claude API rate limit exceeded",
            details={"retry_after_seconds": retry_after}
        )


class ClaudeTimeoutError(ClaudeAPIError):
    """Raised when Claude API request times out"""

    def __init__(self, timeout_seconds: int):
        super().__init__(
            f"Claude API request timed out after {timeout_seconds} seconds",
            details={"timeout_seconds": timeout_seconds}
        )


# =============================================================================
# Document Errors
# =============================================================================

class DocumentError(PlatformException):
    """Base exception for document-related errors"""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "DOCUMENT_ERROR", details)


class DocumentNotFoundError(DocumentError):
    """Raised when a document cannot be found"""

    def __init__(self, doc_id: str):
        super().__init__(
            f"Document not found: {doc_id}",
            details={"document_id": doc_id}
        )


class DocumentGenerationError(DocumentError):
    """Raised when document generation fails"""

    def __init__(self, doc_type: str, reason: str):
        super().__init__(
            f"Failed to generate {doc_type}: {reason}",
            details={"document_type": doc_type, "reason": reason}
        )


# =============================================================================
# Framework Errors
# =============================================================================

class FrameworkError(PlatformException):
    """Base exception for framework-related errors"""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "FRAMEWORK_ERROR", details)


class FrameworkGenerationError(FrameworkError):
    """Raised when framework generation fails"""

    def __init__(self, framework_type: str, reason: str):
        super().__init__(
            f"Failed to generate {framework_type} framework: {reason}",
            details={"framework_type": framework_type, "reason": reason}
        )


# =============================================================================
# Rate Limiting Errors
# =============================================================================

class RateLimitError(PlatformException):
    """Raised when rate limit is exceeded"""

    def __init__(self, limit: int, window: str, retry_after: Optional[int] = None):
        super().__init__(
            f"Rate limit exceeded: {limit} requests per {window}",
            "RATE_LIMIT_EXCEEDED",
            {"limit": limit, "window": window, "retry_after_seconds": retry_after}
        )
