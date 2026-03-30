from __future__ import annotations

from typing import TYPE_CHECKING
from typing_extensions import deprecated

if TYPE_CHECKING:
    from .foxypack_abc.foxystat import FoxyStat

@deprecated("This exception is deprecated and will be removed in a future release. Use exceptions nested from the FoxyException instead.")
class DenialAnalyticsException(Exception):
    def __init__(self, url: str) -> None:
        super().__init__(f"The provided URL '{url}' is not supported")


@deprecated("This exception is deprecated and will be removed in a future release. Use exceptions nested from the FoxyException instead.")
class InternalCollectionException(Exception):
    pass


@deprecated("This exception is deprecated and will be removed in a future release. Use exceptions nested from the FoxyException instead.")
class DenialSynchronousServiceException(InternalCollectionException):
    def __init__(self, foxystat_subclass: type[FoxyStat]) -> None:
        super().__init__()
        self.foxystat_subclass = foxystat_subclass

    def __str__(self) -> str:
        return (
            f"{self.foxystat_subclass.__name__} does not provide data in a synchronous execution mode"
        )


@deprecated("This exception is deprecated and will be removed in a future release. Use exceptions nested from the FoxyException instead.")
class DenialAsynchronousServiceException(InternalCollectionException):
    def __init__(self, foxystat_subclass: type[FoxyStat]) -> None:
        super().__init__()
        self.foxystat_subclass = foxystat_subclass

    def __str__(self) -> str:
        return (
            f"{self.foxystat_subclass.__name__} does not provide data in an asynchronous execution mode"
        )

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
