from dataclasses import dataclass
from typing import Optional, Self

from foxypack.exceptions import FoxyError, ConfigurationError, UnsupportedOperationError
from foxypack.foxypack_abc.foxyanalysis import FoxyAnalysis
from foxypack.foxypack_abc.foxystatistics import FoxyStatistics
from foxypack.foxypack_abc.answers import AnswersAnalysis, AnswersStatistics

@dataclass
class FoxyPackModule:
    foxy_analysis: FoxyAnalysis
    foxy_statistics: Optional[FoxyStatistics]


class FoxyPack:
    """A class for creating a common parser for a set of social media"""

    def __init__(
        self,
        queue_foxy_analysis: set[FoxyAnalysis] | None = None,
        queue_foxy_statistics: set[FoxyStatistics] | None = None,
    ) -> None:
        self._queue_foxy_analysis = queue_foxy_analysis or set()
        self._queue_foxy_statistics = queue_foxy_statistics or set()

    def with_module(self, foxypack_module: FoxyPackModule) -> Self:
        self._queue_foxy_analysis.add(foxypack_module.foxy_analysis)
        if foxypack_module.foxy_statistics:
            self._queue_foxy_statistics.add(foxypack_module.foxy_statistics)
        return self

    def get_analysis(self, url: str) -> AnswersAnalysis:
        if not self._queue_foxy_analysis:
            raise ConfigurationError()
        for foxy_analysis in self._queue_foxy_analysis:
            try:
                result_analysis = foxy_analysis.get_analysis(url=url)
                return result_analysis
            except FoxyError:
                continue
        raise UnsupportedOperationError()

    def get_statistics(self, url: str) -> AnswersStatistics:
        answers_analysis = self.get_analysis(url)
        if not self._queue_foxy_statistics:
            raise ConfigurationError()
        for foxy_stat in self._queue_foxy_statistics:
            try:
                result_analysis = foxy_stat.get_statistics(
                    answers_analysis=answers_analysis
                )
                return result_analysis
            except FoxyError:
                continue
        raise UnsupportedOperationError()

    async def get_statistics_async(self, url: str) -> AnswersStatistics:
        answers_analysis = self.get_analysis(url)
        if not self._queue_foxy_statistics:
            raise ConfigurationError()
        for foxy_stat in self._queue_foxy_statistics:
            try:
                result_analysis = await foxy_stat.get_statistics_async(
                    answers_analysis=answers_analysis
                )
                return result_analysis
            except FoxyError:
                continue
        raise UnsupportedOperationError()
