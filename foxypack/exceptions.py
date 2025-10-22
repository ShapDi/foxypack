from __future__ import annotations
from typing_extensions import override
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .foxypack_abc.foxystat import FoxyStat


class DenialSychronService(Exception):
    name_foxystat_subclass: "type[FoxyStat]"

    def __init__(self, name_foxystat_subclass: "type[FoxyStat]") -> None:
        super().__init__()
        self.name_foxystat_subclass = name_foxystat_subclass

    @override
    def __str__(self) -> str:
        return f"{self.name_foxystat_subclass} does not provide data in a synchronous style"


class DenialAsynchronousService(Exception):
    name_foxystat_subclass: "type[FoxyStat]"

    def __init__(self, name_foxystat_subclass: "type[FoxyStat]") -> None:
        super().__init__()
        self.name_foxystat_subclass = name_foxystat_subclass

    @override
    def __str__(self) -> str:
        return f"{self.name_foxystat_subclass} does not provide asynchronous-style data"
