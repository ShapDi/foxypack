from __future__ import annotations
from abc import ABC, abstractmethod
from foxypack.foxypack_abc.answers import (
    AnswersAnalysis,
    AnswersStatistics,
)
from foxypack.exceptions import (
    DenialAsynchronousServiceException,
)


class FoxyStat(ABC):
    @abstractmethod
    def get_stat(self, answers_analysis: AnswersAnalysis) -> AnswersStatistics:
        raise DenialAsynchronousServiceException(self.__class__)

    @abstractmethod
    async def get_stat_async(
        self, answers_analysis: AnswersAnalysis
    ) -> AnswersStatistics:
        raise DenialAsynchronousServiceException(self.__class__)
