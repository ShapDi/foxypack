from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True, kw_only=True)
class AnswersBase:
    """Common base class for answer models."""

    pass


@dataclass(slots=True, kw_only=True)
class AnswersAnalysis(AnswersBase):
    """Base model for analysis metadata."""

    url: str
    social_platform: str
    type_content: str


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


@dataclass(slots=True, kw_only=True)
class AnswersSocialContent(AnswersStatistics):
    """Model for social content entities, such as video/post/reel."""

    system_id: str
    title: str
    views: int
    publish_date: date | None
    analysis_status: AnswersAnalysis
