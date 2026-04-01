class FoxyException(Exception):
    """Base exception for all Foxy-related errors."""

    pass


class InvalidUsageException(FoxyException):
    """Raised when the Foxy API is used incorrectly."""

    pass


class ConfigurationException(FoxyException):
    """Raised when configuration is invalid or incomplete."""

    pass


class UnsupportedOperationException(FoxyException):
    """Raised when an operation is not supported."""

    pass


class ImplementationContractException(FoxyException):
    """
    Raised when an implementation violates the expected contract.
    """

    pass


class CollectionException(FoxyException):
    """Base exception for data collection errors."""

    pass


class ServiceUnavailableException(CollectionException):
    """Raised when an external service is unavailable."""

    pass


class TimeoutException(CollectionException):
    """Raised when an operation times out."""

    pass


class ContentBlockedException(FoxyException):
    """Raised when content is blocked by the platform."""

    pass


class ContentAccessException(FoxyException):
    """
    Base exception for content that exists but is not accessible to the parser.
    Not caused by platform blocking.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class ContentNotFoundException(ContentAccessException):
    """Raised when content does not exist (404-like case)."""

    pass


class ContentPrivateException(ContentAccessException):
    """Raised when content is private or requires authentication."""

    pass


class ContentRegionRestrictedException(ContentAccessException):
    """Raised when content is unavailable in the parser's region."""

    pass
