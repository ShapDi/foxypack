from __future__ import annotations



from abc import ABC, abstractmethod
from foxypack.foxypack_abc.answers import (
    AnswersAnalysis,
    AnswersStatistics,
)
from foxypack.exceptions import (
    DenialSynchronousServiceException,
    DenialAsynchronousServiceException,
)


class FoxyStat(ABC):
    @abstractmethod
    def get_statistics(self, answers_analysis: AnswersAnalysis) -> AnswersStatistics:
        raise DenialSynchronousServiceException(self.__class__)

    @abstractmethod
    async def get_statistics_async(
        self, answers_analysis: AnswersAnalysis
    ) -> AnswersStatistics:
        raise DenialAsynchronousServiceException(self.__class__)

# print(urllib.parse.urlparse("https://fakesocialmedia.com/qsgqsdrr"))
# print(urllib.parse.urlparse("https://fakesocialmedia.com/qsgqsdr?content_id=fdasfdgfs&content_id=fdasfdgfs"))
# captured_value = parse_qs(urllib.parse.urlparse("https://fakesocialmedia.com/qsgqsdr?content_id=fdasfdgfs&content_id=fdasfdgfs").query)
# print(captured_value)
# captured_value = parse_qs(urllib.parse.urlparse("https://fakesocialmedia.com/qsgqsdrr").query)
# print(captured_value)