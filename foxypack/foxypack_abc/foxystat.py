from __future__ import annotations

from abc import ABC, abstractmethod

from foxypack.foxypack_abc.answers import (
    AnswersAnalysis,
    AnswersStatistics,
)


class FoxyStat(ABC):
    """Abstract class for collecting media content statistics"""

    @abstractmethod
    def get_statistics(self, answers_analysis: AnswersAnalysis) -> AnswersStatistics:
        ...

    @abstractmethod
    async def get_statistics_async(
        self, answers_analysis: AnswersAnalysis
    ) -> AnswersStatistics:
        ...
