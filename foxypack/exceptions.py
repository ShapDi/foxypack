from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import override


if TYPE_CHECKING:
    from .foxypack_abc.foxystat import FoxyStat


class InternalCollectionException(Exception):
    pass


class DenialSynchronousServiceException(InternalCollectionException):
    def __init__(self, name_foxystat_subclass: type[FoxyStat]) -> None:
        super().__init__()
        self.name_foxystat_subclass = name_foxystat_subclass

    @override
    def __str__(self) -> str:
        return f"{self.name_foxystat_subclass.__name__} does not provide data in a synchronous style"


class DenialAsynchronousServiceException(InternalCollectionException):
    def __init__(self, name_foxystat_subclass: type[FoxyStat]) -> None:
        super().__init__()
        self.name_foxystat_subclass = name_foxystat_subclass

    @override
    def __str__(self) -> str:
        return f"{self.name_foxystat_subclass.__name__} does not provide asynchronous-style data"
