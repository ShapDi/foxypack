import pytest

from foxypack import (
    FoxyStat,
    AnswersAnalysis,
    DenialAsynchronousServiceException,
    AnswersStatistics,
    DenialSynchronousServiceException,
    FoxyPack,
    InternalCollectionException,
    DenialAnalyticsException,
)

from datetime import date, timedelta
from typing import Union
import random
from urllib.parse import urlparse, parse_qs

from foxypack.foxypack_abc.answers import AnswersSocialContent, AnswersSocialContainer
from tests.foxypack_abc.test_foxyanalysis import FakeAnalysis


class FakeStat(FoxyStat):
    def __init__(self):
        self.fake_containers = {
            "qsgqsdrr": {
                "system_id": "CH_001",
                "title": "Tech Reviews Channel",
                "subscribers": 15400,
                "creation_date": date(2020, 3, 15),
            },
            "programming": {
                "system_id": "CH_002",
                "title": "Code Masters",
                "subscribers": 89200,
                "creation_date": date(2019, 7, 22),
            },
            "gaming": {
                "system_id": "CH_003",
                "title": "Game Zone",
                "subscribers": 231500,
                "creation_date": date(2021, 1, 10),
            },
        }

        self.fake_content = {
            "video_fdasfdgfs": {
                "system_id": "VID_001",
                "title": "New Smartphone Review 2024",
                "views": 125000,
                "publish_date": date(2024, 1, 15),
            },
            "image_abc123": {
                "system_id": "IMG_001",
                "title": "Sunset Landscape Photography",
                "views": 8700,
                "publish_date": date(2023, 12, 5),
            },
            "text_xyz789": {
                "system_id": "TXT_001",
                "title": "Machine Learning Trends",
                "views": 4300,
                "publish_date": date(2024, 2, 20),
            },
            "audio_sound123": {
                "system_id": "AUD_001",
                "title": "Morning Meditation",
                "views": 15600,
                "publish_date": date(2023, 11, 30),
            },
        }

        self.random_titles = [
            "Awesome Content",
            "Daily Update",
            "Special Edition",
            "Behind the Scenes",
            "Exclusive Interview",
            "Tutorial Guide",
            "News Update",
            "Community Spotlight",
            "Weekly Recap",
        ]

    @staticmethod
    def _extract_content_id(url: str) -> Union[str, None]:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        if "content_id" in query_params:
            return query_params["content_id"][0]
        path = parsed_url.path.strip("/")
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
            "creation_date": date.today() - timedelta(days=random.randint(30, 365 * 3)),
        }

    def _generate_fake_content_data(self, content_id: str) -> dict:
        for key, data in self.fake_content.items():
            if content_id.startswith(key.split("_")[0]):
                return data
        if content_id.startswith("video_"):
            content_type = "video"
            base_views = random.randint(50000, 500000)
        else:
            content_type = "unknown"
            base_views = random.randint(100, 10000)
        return {
            "system_id": f"{content_type[:3].upper()}_{random.randint(100, 999):03d}",
            "title": f"{content_type.capitalize()} - {random.choice(self.random_titles)}",
            "views": base_views + random.randint(-base_views // 10, base_views // 10),
            "publish_date": date.today() - timedelta(days=random.randint(1, 90)),
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
                analysis_status=answers_analysis,
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
                analysis_status=answers_analysis,
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
        type_content="channel",
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


def test_foxypack_with_analysis():
    """Test case verifies adding FoxyAnalysis analyzer to FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis())

    assert len(foxypack._queue_foxy_analysis) == 1
    assert isinstance(foxypack._queue_foxy_analysis[0], FakeAnalysis)
    assert len(foxypack._queue_foxy_stat) == 0


def test_foxypack_with_stat():
    """Test case verifies adding FoxyStat statistics to FoxyPack"""
    foxypack = FoxyPack().with_foxy_stat(FakeStat())

    assert len(foxypack._queue_foxy_stat) == 1
    assert isinstance(foxypack._queue_foxy_stat[0], FakeStat)
    assert len(foxypack._queue_foxy_analysis) == 0


def test_foxypack_with_both():
    """Test case verifies adding both analyzer and statistics to FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())

    assert len(foxypack._queue_foxy_analysis) == 1
    assert len(foxypack._queue_foxy_stat) == 1
    assert isinstance(foxypack._queue_foxy_analysis[0], FakeAnalysis)
    assert isinstance(foxypack._queue_foxy_stat[0], FakeStat)


def test_foxypack_chain_multiple():
    """Test case verifies chaining addition of multiple analyzers"""
    foxypack = (
        FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_analysis(FakeAnalysis())
    )

    assert len(foxypack._queue_foxy_analysis) == 2
    assert len(foxypack._queue_foxy_stat) == 0


def test_foxypack_get_analysis_channel():
    """Test case verifies getting analysis for a channel through FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis())
    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")

    assert analysis is not None
    assert analysis.url == "https://fakesocialmedia.com/qsgqsdrr"
    assert analysis.social_platform == "FakeSocialMedia"
    assert analysis.type_content == "channel"


def test_foxypack_get_analysis_video():
    """Test case verifies getting analysis for video content through FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis())
    analysis = foxypack.get_analysis(
        "https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
    )

    assert analysis is not None
    assert (
        analysis.url == "https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
    )
    assert analysis.social_platform == "FakeSocialMedia"
    assert analysis.type_content == "video"


def test_foxypack_get_analysis_invalid_url():
    """Test case verifies handling of invalid URL through FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis())
    analysis = foxypack.get_analysis(
        "https://invalidmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
    )

    assert analysis is None


def test_foxypack_get_analysis_no_analyzers():
    """Test case verifies behavior of FoxyPack without analyzers"""
    foxypack = FoxyPack()
    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")

    assert analysis is None


def test_foxypack_get_analysis_multiple_analyzers_first_success():
    """Test case verifies analyzer chain operation where the first one fails and the second succeeds"""

    class FailingFakeAnalysis(FakeAnalysis):
        def get_analysis(self, url: str):
            raise DenialAnalyticsException(url)

    foxypack = (
        FoxyPack()
        .with_foxy_analysis(FailingFakeAnalysis())
        .with_foxy_analysis(FakeAnalysis())
    )
    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")

    assert analysis is not None
    assert analysis.url == "https://fakesocialmedia.com/qsgqsdrr"
    assert analysis.social_platform == "FakeSocialMedia"
    assert analysis.type_content == "channel"


def test_foxypack_get_analysis_multiple_analyzers_all_fail():
    """Test case verifies analyzer chain operation where all analyzers fail"""

    class FailingFakeAnalysis(FakeAnalysis):
        def get_analysis(self, url: str):
            raise DenialAnalyticsException(url)

    foxypack = (
        FoxyPack()
        .with_foxy_analysis(FailingFakeAnalysis())
        .with_foxy_analysis(FailingFakeAnalysis())
    )
    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")

    assert analysis is None


def test_foxypack_get_statistics_full_flow():
    """Test case verifies the full workflow of FoxyPack: analysis + statistics for channel"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"
    assert statistics.title == "Tech Reviews Channel"
    assert statistics.subscribers == 15400
    assert statistics.creation_date == date(2020, 3, 15)


def test_foxypack_get_statistics_video_content():
    """Test case verifies the full workflow of FoxyPack: analysis + statistics for video"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = foxypack.get_statistics(
        "https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
    )

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContent)
    assert statistics.system_id == "VID_001"
    assert statistics.title == "New Smartphone Review 2024"
    assert statistics.views == 125000
    assert statistics.publish_date == date(2024, 1, 15)


def test_foxypack_get_statistics_no_analysis():
    """Test case verifies getting statistics without analyzers in FoxyPack"""
    foxypack = FoxyPack().with_foxy_stat(FakeStat())
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is None


def test_foxypack_get_statistics_no_stats():
    """Test case verifies getting statistics without statistical handlers in FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis())
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is None


def test_foxypack_get_statistics_invalid_url():
    """Test case verifies handling of invalid URL when getting statistics"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = foxypack.get_statistics("https://invalidmedia.com/qsgqsdrr")

    assert statistics is None


def test_foxypack_get_statistics_multiple_stats_first_success():
    """Test case verifies the operation of the statistical handler chain in FoxyPack"""

    class FailingFakeStat(FakeStat):
        def get_statistics(self, answers_analysis):
            raise InternalCollectionException()

    foxypack = (
        FoxyPack()
        .with_foxy_analysis(FakeAnalysis())
        .with_foxy_stat(FailingFakeStat())
        .with_foxy_stat(FakeStat())
    )
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"


def test_foxypack_get_statistics_multiple_stats_all_fail():
    """Test case verifies FoxyPack operation when all statistical handlers fail"""

    class FailingFakeStat(FakeStat):
        def get_statistics(self, answers_analysis):
            raise InternalCollectionException()

    foxypack = (
        FoxyPack()
        .with_foxy_analysis(FakeAnalysis())
        .with_foxy_stat(FailingFakeStat())
        .with_foxy_stat(FailingFakeStat())
    )
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is None


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_full_flow():
    """Test case verifies asynchronous full workflow of FoxyPack for channel"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = await foxypack.get_statistics_async(
        "https://fakesocialmedia.com/qsgqsdrr"
    )

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"
    assert statistics.title == "Tech Reviews Channel"
    assert statistics.subscribers == 15400
    assert statistics.creation_date == date(2020, 3, 15)


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_video_content():
    """Test case verifies asynchronous full workflow of FoxyPack for video"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = await foxypack.get_statistics_async(
        "https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
    )

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContent)
    assert statistics.system_id == "VID_001"
    assert statistics.title == "New Smartphone Review 2024"
    assert statistics.views == 125000
    assert statistics.publish_date == date(2024, 1, 15)


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_no_analysis():
    """Test case verifies asynchronous statistics retrieval without analyzers"""
    foxypack = FoxyPack().with_foxy_stat(FakeStat())
    statistics = await foxypack.get_statistics_async(
        "https://fakesocialmedia.com/qsgqsdrr"
    )

    assert statistics is None


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_invalid_url():
    """Test case verifies asynchronous handling of invalid URL"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = await foxypack.get_statistics_async(
        "https://invalidmedia.com/qsgqsdrr"
    )

    assert statistics is None


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_multiple_stats():
    """Test case verifies asynchronous operation of statistical handler chain"""

    class FailingFakeStat(FakeStat):
        async def get_statistics_async(self, answers_analysis):
            raise InternalCollectionException()

    foxypack = (
        FoxyPack()
        .with_foxy_analysis(FakeAnalysis())
        .with_foxy_stat(FailingFakeStat())
        .with_foxy_stat(FakeStat())
    )
    statistics = await foxypack.get_statistics_async(
        "https://fakesocialmedia.com/qsgqsdrr"
    )

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"


def test_foxypack_empty_initialization():
    """Test case verifies empty FoxyPack initialization"""
    foxypack = FoxyPack()

    assert foxypack._queue_foxy_analysis == []
    assert foxypack._queue_foxy_stat == []


def test_foxypack_with_initial_queues():
    """Test case verifies FoxyPack initialization with preset queues"""
    initial_analysis = [FakeAnalysis(), FakeAnalysis()]
    initial_stats = [FakeStat()]

    foxypack = FoxyPack(
        queue_foxy_analysis=initial_analysis, queue_foxy_stat=initial_stats
    )

    assert len(foxypack._queue_foxy_analysis) == 2
    assert len(foxypack._queue_foxy_stat) == 1


def test_foxypack_with_initial_queues_and_adding_more():
    """Test case verifies adding new handlers to a preset FoxyPack"""
    initial_analysis = [FakeAnalysis()]
    initial_stats = [FakeStat()]

    foxypack = FoxyPack(
        queue_foxy_analysis=initial_analysis, queue_foxy_stat=initial_stats
    )
    foxypack.with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())

    assert len(foxypack._queue_foxy_analysis) == 2
    assert len(foxypack._queue_foxy_stat) == 2
