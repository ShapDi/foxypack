import pytest

from foxypack import (
    FoxyStat,
    AnswersAnalysis,
    DenialAsynchronousServiceException,
    AnswersStatistics,
    DenialSynchronousServiceException,
)

from datetime import date, datetime, timedelta
from typing import Union
import random
from urllib.parse import urlparse, parse_qs

from foxypack.foxypack_abc.answers import AnswersSocialContent, AnswersSocialContainer


class FakeStat(FoxyStat):
    def __init__(self):
        self.fake_containers = {
            "qsgqsdrr": {
                "system_id": "CH_001",
                "title": "Tech Reviews Channel",
                "subscribers": 15400,
                "creation_date": date(2020, 3, 15)
            },
            "programming": {
                "system_id": "CH_002",
                "title": "Code Masters",
                "subscribers": 89200,
                "creation_date": date(2019, 7, 22)
            },
            "gaming": {
                "system_id": "CH_003",
                "title": "Game Zone",
                "subscribers": 231500,
                "creation_date": date(2021, 1, 10)
            }
        }

        self.fake_content = {
            "video_fdasfdgfs": {
                "system_id": "VID_001",
                "title": "New Smartphone Review 2024",
                "views": 125000,
                "publish_date": date(2024, 1, 15)
            },
            "image_abc123": {
                "system_id": "IMG_001",
                "title": "Sunset Landscape Photography",
                "views": 8700,
                "publish_date": date(2023, 12, 5)
            },
            "text_xyz789": {
                "system_id": "TXT_001",
                "title": "Machine Learning Trends",
                "views": 4300,
                "publish_date": date(2024, 2, 20)
            },
            "audio_sound123": {
                "system_id": "AUD_001",
                "title": "Morning Meditation",
                "views": 15600,
                "publish_date": date(2023, 11, 30)
            }
        }

        self.random_titles = [
            "Awesome Content", "Daily Update", "Special Edition",
            "Behind the Scenes", "Exclusive Interview", "Tutorial Guide",
            "News Update", "Community Spotlight", "Weekly Recap"
        ]

    def _extract_content_id(self, url: str) -> Union[str, None]:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        if 'content_id' in query_params:
            return query_params['content_id'][0]
        path = parsed_url.path.strip('/')
        if path:
            return path
        return None

    def _generate_fake_container_data(self, channel_code: str) -> dict:
        if channel_code in self.fake_containers:
            return self.fake_containers[channel_code]
        return {
            "system_id": f"CH_{random.randint(100, 999):03d}",
            "title": random.choice(self.random_titles),
            "subscribers": random.randint(100, 1000000),
            "creation_date": date.today() - timedelta(days=random.randint(30, 365 * 3))
        }

    def _generate_fake_content_data(self, content_id: str) -> dict:
        for key, data in self.fake_content.items():
            if content_id.startswith(key.split('_')[0]):
                return data
        if content_id.startswith('video_'):
            content_type = "video"
            base_views = random.randint(50000, 500000)
        elif content_id.startswith('image_'):
            content_type = "image"
            base_views = random.randint(1000, 50000)
        elif content_id.startswith('text_'):
            content_type = "text"
            base_views = random.randint(500, 20000)
        elif content_id.startswith('audio_'):
            content_type = "audio"
            base_views = random.randint(10000, 100000)
        else:
            content_type = "unknown"
            base_views = random.randint(100, 10000)
        return {
            "system_id": f"{content_type[:3].upper()}_{random.randint(100, 999):03d}",
            "title": f"{content_type.capitalize()} - {random.choice(self.random_titles)}",
            "views": base_views + random.randint(-base_views // 10, base_views // 10),
            "publish_date": date.today() - timedelta(days=random.randint(1, 90))
        }

    def get_statistics(self, answers_analysis: AnswersAnalysis) -> AnswersStatistics:
        if not answers_analysis:
            raise DenialSynchronousServiceException(self.__class__)
        content_id = self._extract_content_id(answers_analysis.url)
        if answers_analysis.type_content in ["channel", "homepage"]:
            channel_code = content_id if content_id else "home"
            fake_data = self._generate_fake_container_data(channel_code)
            return AnswersSocialContainer(
                system_id=fake_data["system_id"],
                title=fake_data["title"],
                subscribers=fake_data["subscribers"],
                creation_date=fake_data["creation_date"],
                analysis_status=answers_analysis
            )
        else:
            if not content_id:
                content_id = f"{answers_analysis.type_content}_generated_{random.randint(1000, 9999)}"
            fake_data = self._generate_fake_content_data(content_id)
            return AnswersSocialContent(
                system_id=fake_data["system_id"],
                title=fake_data["title"],
                views=fake_data["views"],
                publish_date=fake_data["publish_date"],
                analysis_status=answers_analysis
            )

    async def get_statistics_async(
            self, answers_analysis: AnswersAnalysis
    ) -> AnswersStatistics:
        if not answers_analysis:
            raise DenialAsynchronousServiceException(self.__class__)
        import asyncio
        await asyncio.sleep(0.1)
        return self.get_statistics(answers_analysis)


def test_fake_stat_container_sync():
    fake_stat = FakeStat()
    analysis = AnswersAnalysis(
        url="https://fakesocialmedia.com/qsgqsdrr",
        social_platform="FakeSocialMedia",
        type_content="channel"
    )

    result = fake_stat.get_statistics(analysis)

    assert result.analysis_status.url == "https://fakesocialmedia.com/qsgqsdrr"
    assert result.analysis_status.social_platform == "FakeSocialMedia"
    assert result.analysis_status.type_content == "channel"
    assert isinstance(result, AnswersSocialContainer)
    assert result.system_id == "CH_001"
    assert result.title == "Tech Reviews Channel"
    assert result.subscribers == 15400
    assert result.creation_date == date(2020, 3, 15)


def test_fake_stat_video_sync():
    fake_stat = FakeStat()
    analysis = AnswersAnalysis(
        url="https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs",
        social_platform="FakeSocialMedia",
        type_content="video"
    )

    result = fake_stat.get_statistics(analysis)

    assert result.analysis_status.url == "https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
    assert result.analysis_status.social_platform == "FakeSocialMedia"
    assert result.analysis_status.type_content == "video"
    assert isinstance(result, AnswersSocialContent)
    assert result.system_id == "VID_001"
    assert result.title == "New Smartphone Review 2024"
    assert result.views == 125000
    assert result.publish_date == date(2024, 1, 15)


def test_fake_stat_image_sync():
    fake_stat = FakeStat()
    analysis = AnswersAnalysis(
        url="https://fakesocialmedia.com/qsgqsdr?content_id=image_abc123",
        social_platform="FakeSocialMedia",
        type_content="image"
    )

    result = fake_stat.get_statistics(analysis)

    assert isinstance(result, AnswersSocialContent)
    assert result.system_id == "IMG_001"
    assert result.title == "Sunset Landscape Photography"
    assert result.views == 8700
    assert result.publish_date == date(2023, 12, 5)


def test_fake_stat_text_sync():
    fake_stat = FakeStat()
    analysis = AnswersAnalysis(
        url="https://fakesocialmedia.com/qsgqsdr?content_id=text_xyz789",
        social_platform="FakeSocialMedia",
        type_content="text"
    )

    result = fake_stat.get_statistics(analysis)

    assert isinstance(result, AnswersSocialContent)
    assert result.system_id == "TXT_001"
    assert result.title == "Machine Learning Trends"
    assert result.views == 4300
    assert result.publish_date == date(2024, 2, 20)


def test_fake_stat_homepage_sync():
    fake_stat = FakeStat()
    analysis = AnswersAnalysis(
        url="https://fakesocialmedia.com/",
        social_platform="FakeSocialMedia",
        type_content="homepage"
    )

    result = fake_stat.get_statistics(analysis)

    assert isinstance(result, AnswersSocialContainer)
    assert result.system_id.startswith("CH_")
    assert isinstance(result.subscribers, int)
    assert result.subscribers > 0
    assert isinstance(result.creation_date, date)


def test_fake_stat_unknown_channel_sync():
    fake_stat = FakeStat()
    analysis = AnswersAnalysis(
        url="https://fakesocialmedia.com/unknownchannel",
        social_platform="FakeSocialMedia",
        type_content="channel"
    )

    result = fake_stat.get_statistics(analysis)

    assert isinstance(result, AnswersSocialContainer)
    assert result.system_id.startswith("CH_")
    assert isinstance(result.title, str)
    assert len(result.title) > 0
    assert isinstance(result.subscribers, int)
    assert isinstance(result.creation_date, date)


def test_fake_stat_unknown_content_sync():
    fake_stat = FakeStat()

    analysis = AnswersAnalysis(
        url="https://fakesocialmedia.com/qsgqsdr?content_id=brandnew_video_12345",
        social_platform="FakeSocialMedia",
        type_content="video"
    )

    result = fake_stat.get_statistics(analysis)

    assert isinstance(result, AnswersSocialContent)
    assert result.system_id.startswith("UNK_")
    assert "Brandnew" in result.title or "Unknown" in result.title
    assert isinstance(result.views, int)
    assert isinstance(result.publish_date, date)


def test_fake_stat_empty_analysis():
    fake_stat = FakeStat()

    with pytest.raises(DenialSynchronousServiceException):
        fake_stat.get_statistics(None)


@pytest.mark.asyncio
async def test_fake_stat_container_async():
    fake_stat = FakeStat()
    analysis = AnswersAnalysis(
        url="https://fakesocialmedia.com/qsgqsdrr",
        social_platform="FakeSocialMedia",
        type_content="channel"
    )

    result = await fake_stat.get_statistics_async(analysis)

    assert isinstance(result, AnswersSocialContainer)
    assert result.system_id == "CH_001"
    assert result.title == "Tech Reviews Channel"
    assert result.subscribers == 15400
    assert result.creation_date == date(2020, 3, 15)


@pytest.mark.asyncio
async def test_fake_stat_video_async():
    fake_stat = FakeStat()
    analysis = AnswersAnalysis(
        url="https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs",
        social_platform="FakeSocialMedia",
        type_content="video"
    )

    result = await fake_stat.get_statistics_async(analysis)

    assert isinstance(result, AnswersSocialContent)
    assert result.system_id == "VID_001"
    assert result.title == "New Smartphone Review 2024"
    assert result.views == 125000
    assert result.publish_date == date(2024, 1, 15)


@pytest.mark.asyncio
async def test_fake_stat_empty_analysis_async():
    fake_stat = FakeStat()

    with pytest.raises(DenialAsynchronousServiceException):
        await fake_stat.get_statistics_async(None)


def test_fake_stat_multiple_calls():
    fake_stat = FakeStat()

    analysis1 = AnswersAnalysis(
        url="https://fakesocialmedia.com/qsgqsdrr",
        social_platform="FakeSocialMedia",
        type_content="channel"
    )

    analysis2 = AnswersAnalysis(
        url="https://fakesocialmedia.com/programming",
        social_platform="FakeSocialMedia",
        type_content="channel"
    )

    result1 = fake_stat.get_statistics(analysis1)
    result2 = fake_stat.get_statistics(analysis2)

    assert result1.system_id == "CH_001"
    assert result2.system_id == "CH_002"
    assert result1.title == "Tech Reviews Channel"
    assert result2.title == "Code Masters"
    assert result1.subscribers == 15400
    assert result2.subscribers == 89200


def test_fake_stat_different_answer_ids():
    fake_stat = FakeStat()

    analysis = AnswersAnalysis(
        url="https://fakesocialmedia.com/qsgqsdrr",
        social_platform="FakeSocialMedia",
        type_content="channel"
    )

    result1 = fake_stat.get_statistics(analysis)
    result2 = fake_stat.get_statistics(analysis)

    assert result1.answer_id != result2.answer_id
    assert result1.analysis_status.answer_id == result2.analysis_status.answer_id