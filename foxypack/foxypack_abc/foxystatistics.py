from abc import ABC, abstractmethod
from typing import Any

from foxypack.foxypack_abc.answers import (
    AnswersAnalysis,
    AnswersStatistics,
)


class FoxyStatistics(ABC):
    """Abstract class for collecting media content statistics"""

    @abstractmethod
    def get_statistics(
        self, answers_analysis: AnswersAnalysis
    ) -> AnswersStatistics: ...

    @abstractmethod
    async def get_statistics_async(
        self, answers_analysis: AnswersAnalysis
    ) -> AnswersStatistics: ...

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FoxyStatistics):
            return False

        if type(self) is not type(other):
            return False

        return True

    def __hash__(self) -> int:
        name_bytes = self.__class__.__name__.encode("utf-8")
        hash_value = int.from_bytes(name_bytes, "big")
        return hash_value
