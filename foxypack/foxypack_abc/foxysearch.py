from dataclasses import dataclass, field
from typing import Any, List, Optional
from abc import ABC, abstractmethod


@dataclass
class SearchFilters:
    sort_by: Any = None
    upload_date: Any = None
    content_type: Any = None


@dataclass
class SearchResult:
    platform: str
    url: str
    _raw: Any = field(default=None, repr=False)   # оригинальный объект платформы


class PlatformSearcher(ABC):
    """Базовый интерфейс поиска."""

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Имя платформы"""
        ...

    @abstractmethod
    def search(
        self,
        query: str,
        filters: Optional[SearchFilters] = None,
        max_results: int = 20,
    ) -> List[SearchResult]:
        """
        Поиск по ключевым словам.
        Возвращает список результатов с метаданными и ссылками.
        """
        ...