from __future__ import annotations


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
