from pydantic import BaseModel
from typing_extensions import TypeVar


class AnswersAnalysis(BaseModel):
    answer_id: str
    url: str
    social_platform: str
    type_content: str


AnalysisType = TypeVar("AnalysisType", bound=AnswersAnalysis)


class AnswersStatistics(BaseModel):
    answer_id: str


StatisticsType = TypeVar("StatisticsType", bound=AnswersStatistics)
