from foxypack import (
    FoxyStat,
    AnswersAnalysis,
    DenialAsynchronousServiceException,
    AnswersStatistics,
    DenialSynchronousServiceException,
)


class FakeStat(FoxyStat):
    def get_statistics(self, answers_analysis: AnswersAnalysis) -> AnswersStatistics:
        raise DenialSynchronousServiceException(self.__class__)

    async def get_statistics_async(
        self, answers_analysis: AnswersAnalysis
    ) -> AnswersStatistics:
        raise DenialAsynchronousServiceException(self.__class__)
