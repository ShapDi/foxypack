from typing import Any, Dict, Optional


class FoxyError(Exception):
    """Base exception for all Foxy-related errors."""

    def __init__(
        self,
        message: str = "",
        *,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.cause = cause

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | details={self.details}"
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        """Structured representation for logging or API responses."""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
            "cause": repr(self.cause) if self.cause else None,
        }


class InvalidUsageError(FoxyError):
    """Raised when the Foxy API is used incorrectly."""


class ConfigurationError(FoxyError):
    """Raised when configuration is invalid or incomplete."""


class UnsupportedOperationError(FoxyError):
    """Raised when an operation is not supported."""


class ImplementationContractError(FoxyError):
    """
    Raised when an implementation violates the expected contract.
    """


class CollectionError(FoxyError):
    """Base exception for data collection errors."""


class ServiceUnavailableError(CollectionError):
    """Raised when an external service is unavailable."""

    def __init__(
        self,
        message: str = "External service unavailable",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)


class TimeoutError(CollectionError):
    """Raised when an operation times out."""

    def __init__(
        self,
        message: str = "Operation timed out",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)


class ContentBlockedError(FoxyError):
    """Raised when content is blocked by the platform."""


class ContentAccessError(FoxyError):
    """
    Base exception for content that exists but is not accessible to the parser.
    Not caused by platform blocking.
    """

    def __init__(
        self,
        message: str = "",
        *,
        content_id: Optional[str] = None,
        url: Optional[str] = None,
        platform: Optional[str] = None,
        cause: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        base_details = {
            "content_id": content_id,
            "url": url,
            "platform": platform,
        }

        base_details = {k: v for k, v in base_details.items() if v is not None}

        if details:
            base_details.update(details)

        super().__init__(
            message,
            details=base_details,
            cause=cause,
        )

        self.content_id = content_id
        self.url = url
        self.platform = platform


class ContentNotFoundError(ContentAccessError):
    """Raised when content does not exist (404-like case)."""


class ContentPrivateError(ContentAccessError):
    """Raised when content is private or requires authentication."""


class ContentRegionRestrictedError(ContentAccessError):
    """Raised when content is unavailable in the parser's region."""
