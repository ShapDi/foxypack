from abc import ABC
from typing import Generator

from foxypack import FoxyStat


class EntitiesFoundGenerator(Generator):
    pass


class FoxySearch(ABC):
    def __init__(self, statistics_engine: FoxyStat) -> None:
        self.statistics_engine = statistics_engine

    def get_search_fox(self):
        pass