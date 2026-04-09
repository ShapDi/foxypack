from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from typing import Any


@dataclass(slots=True, kw_only=True)
class AnswersBase:
    """Common base class for answer models."""

    def to_dict(self) -> dict[str, Any]:
        """Convert model to plain dict."""
        return asdict(self)


@dataclass(slots=True, kw_only=True)
class AnswersAnalysis(AnswersBase):
    """Base model for analysis metadata."""

    url: str
    social_platform: str
    type_content: str

    def __post_init__(self) -> None:
        if not self.url or not self.url.strip():
            raise ValueError("url must not be empty")

        if not self.social_platform or not self.social_platform.strip():
            raise ValueError("social_platform must not be empty")

        if not self.type_content or not self.type_content.strip():
            raise ValueError("type_content must not be empty")


@dataclass(slots=True, kw_only=True)
class AnswersStatistics(AnswersBase):
    """Base model for statistics answers."""
    pass


@dataclass(slots=True, kw_only=True)
class AnswersSocialContainer(AnswersStatistics):
    """Model for social container entities, such as channel/group/account."""

    system_id: str
    title: str
    subscribers: int
    creation_date: date | None
    analysis_status: AnswersAnalysis

    def __post_init__(self) -> None:
        if not self.system_id or not self.system_id.strip():
            raise ValueError("system_id must not be empty")

        if not self.title or not self.title.strip():
            raise ValueError("title must not be empty")

        if self.subscribers < 0:
            raise ValueError("subscribers must be >= 0")


@dataclass(slots=True, kw_only=True)
class AnswersSocialContent(AnswersStatistics):
    """Model for social content entities, such as video/post/reel."""

    system_id: str
    title: str
    views: int
    publish_date: date | None
    analysis_status: AnswersAnalysis

    def __post_init__(self) -> None:
        if not self.system_id or not self.system_id.strip():
            raise ValueError("system_id must not be empty")

        if not self.title or not self.title.strip():
            raise ValueError("title must not be empty")

        if self.views < 0:
            raise ValueError("views must be >= 0")