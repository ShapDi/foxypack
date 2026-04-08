from abc import ABC, abstractmethod


from foxypack.foxypack_abc.answers import AnswersAnalysis


class FoxyAnalysis(ABC):
    """Abstract class for analysis media content statistics"""

    @abstractmethod
    def get_analysis(self, url: str) -> AnswersAnalysis: ...

    def __eq__(self, other):
        if not isinstance(other, FoxyAnalysis):
            return False

        if type(self) is not type(other):
            return False

        return True

    def __hash__(self):
        name_bytes = self.__class__.__name__.encode("utf-8")
        hash_value = int.from_bytes(name_bytes, "big")
        return hash_value
