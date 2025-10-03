from abc import ABC, abstractmethod

from foxypack.answers import AnswersStatistics, AnswersAnalysis


class FoxyStat(ABC):
    @abstractmethod
    def get_stat(self, url) -> AnswersStatistics | None:
        pass

    @abstractmethod
    async def get_stat_async(self, url: str, answers_analysis: AnswersAnalysis) -> AnswersStatistics | None:
        pass

