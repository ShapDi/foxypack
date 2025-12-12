import pytest

from foxypack import (
    FoxyStat,
    AnswersAnalysis,
    DenialAsynchronousServiceException,
    AnswersStatistics,
    DenialSynchronousServiceException, FoxyPack, InternalCollectionException, DenialAnalyticsException,
)

from datetime import date, datetime, timedelta
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


def test_foxypack_with_analysis():
    """Тест кейс проверяет добавление анализатора FoxyAnalysis в FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis())

    assert len(foxypack.queue_foxy_analysis) == 1
    assert isinstance(foxypack.queue_foxy_analysis[0], FakeAnalysis)
    assert len(foxypack.queue_foxy_stat) == 0


def test_foxypack_with_stat():
    """Тест кейс проверяет добавление статистики FoxyStat в FoxyPack"""
    foxypack = FoxyPack().with_foxy_stat(FakeStat())

    assert len(foxypack.queue_foxy_stat) == 1
    assert isinstance(foxypack.queue_foxy_stat[0], FakeStat)
    assert len(foxypack.queue_foxy_analysis) == 0


def test_foxypack_with_both():
    """Тест кейс проверяет добавление и анализатора и статистики в FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())

    assert len(foxypack.queue_foxy_analysis) == 1
    assert len(foxypack.queue_foxy_stat) == 1
    assert isinstance(foxypack.queue_foxy_analysis[0], FakeAnalysis)
    assert isinstance(foxypack.queue_foxy_stat[0], FakeStat)


def test_foxypack_chain_multiple():
    """Тест кейс проверяет цепочное добавление нескольких анализаторов"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_analysis(FakeAnalysis())

    assert len(foxypack.queue_foxy_analysis) == 2
    assert len(foxypack.queue_foxy_stat) == 0


def test_foxypack_get_analysis_channel():
    """Тест кейс проверяет получение анализа для канала через FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis())
    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")

    assert analysis is not None
    assert analysis.url == "https://fakesocialmedia.com/qsgqsdrr"
    assert analysis.social_platform == "FakeSocialMedia"
    assert analysis.type_content == "channel"


def test_foxypack_get_analysis_video():
    """Тест кейс проверяет получение анализа для видео контента через FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis())
    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs")

    assert analysis is not None
    assert analysis.url == "https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
    assert analysis.social_platform == "FakeSocialMedia"
    assert analysis.type_content == "video"


def test_foxypack_get_analysis_invalid_url():
    """Тест кейс проверяет обработку невалидного URL через FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis())
    analysis = foxypack.get_analysis("https://invalidmedia.com/qsgqsdr?content_id=video_fdasfdgfs")

    assert analysis is None


def test_foxypack_get_analysis_no_analyzers():
    """Тест кейс проверяет поведение FoxyPack без анализаторов"""
    foxypack = FoxyPack()
    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")

    assert analysis is None


def test_foxypack_get_analysis_multiple_analyzers_first_success():
    """Тест кейс проверяет работу цепочки анализаторов, где первый падает, а второй успешен"""

    class FailingFakeAnalysis(FakeAnalysis):
        def get_analysis(self, url: str):
            raise DenialAnalyticsException(url)

    foxypack = FoxyPack().with_foxy_analysis(FailingFakeAnalysis()).with_foxy_analysis(FakeAnalysis())
    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")

    assert analysis is not None
    assert analysis.url == "https://fakesocialmedia.com/qsgqsdrr"
    assert analysis.social_platform == "FakeSocialMedia"
    assert analysis.type_content == "channel"


def test_foxypack_get_analysis_multiple_analyzers_all_fail():
    """Тест кейс проверяет работу цепочки анализаторов, где все анализаторы падают"""

    class FailingFakeAnalysis(FakeAnalysis):
        def get_analysis(self, url: str):
            raise DenialAnalyticsException(url)

    foxypack = FoxyPack().with_foxy_analysis(FailingFakeAnalysis()).with_foxy_analysis(FailingFakeAnalysis())
    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")

    assert analysis is None


def test_foxypack_get_statistics_full_flow():
    """Тест кейс проверяет полный поток работы FoxyPack: анализ + статистика для канала"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"
    assert statistics.title == "Tech Reviews Channel"
    assert statistics.subscribers == 15400
    assert statistics.creation_date == date(2020, 3, 15)


def test_foxypack_get_statistics_video_content():
    """Тест кейс проверяет полный поток работы FoxyPack: анализ + статистика для видео"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs")

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContent)
    assert statistics.system_id == "VID_001"
    assert statistics.title == "New Smartphone Review 2024"
    assert statistics.views == 125000
    assert statistics.publish_date == date(2024, 1, 15)


def test_foxypack_get_statistics_no_analysis():
    """Тест кейс проверяет получение статистики без анализаторов в FoxyPack"""
    foxypack = FoxyPack().with_foxy_stat(FakeStat())
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is None


def test_foxypack_get_statistics_no_stats():
    """Тест кейс проверяет получение статистики без статистических обработчиков в FoxyPack"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis())
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is None


def test_foxypack_get_statistics_invalid_url():
    """Тест кейс проверяет обработку невалидного URL при получении статистики"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = foxypack.get_statistics("https://invalidmedia.com/qsgqsdrr")

    assert statistics is None


def test_foxypack_get_statistics_multiple_stats_first_success():
    """Тест кейс проверяет работу цепочки статистических обработчиков в FoxyPack"""

    class FailingFakeStat(FakeStat):
        def get_statistics(self, answers_analysis):
            raise InternalCollectionException()

    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FailingFakeStat()).with_foxy_stat(
        FakeStat())
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"


def test_foxypack_get_statistics_multiple_stats_all_fail():
    """Тест кейс проверяет работу FoxyPack когда все статистические обработчики падают"""

    class FailingFakeStat(FakeStat):
        def get_statistics(self, answers_analysis):
            raise InternalCollectionException()

    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FailingFakeStat()).with_foxy_stat(
        FailingFakeStat())
    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is None


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_full_flow():
    """Тест кейс проверяет асинхронный полный поток работы FoxyPack для канала"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = await foxypack.get_statistics_async("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"
    assert statistics.title == "Tech Reviews Channel"
    assert statistics.subscribers == 15400
    assert statistics.creation_date == date(2020, 3, 15)


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_video_content():
    """Тест кейс проверяет асинхронный полный поток работы FoxyPack для видео"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = await foxypack.get_statistics_async("https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs")

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContent)
    assert statistics.system_id == "VID_001"
    assert statistics.title == "New Smartphone Review 2024"
    assert statistics.views == 125000
    assert statistics.publish_date == date(2024, 1, 15)


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_no_analysis():
    """Тест кейс проверяет асинхронное получение статистики без анализаторов"""
    foxypack = FoxyPack().with_foxy_stat(FakeStat())
    statistics = await foxypack.get_statistics_async("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is None


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_invalid_url():
    """Тест кейс проверяет асинхронную обработку невалидного URL"""
    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())
    statistics = await foxypack.get_statistics_async("https://invalidmedia.com/qsgqsdrr")

    assert statistics is None


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_multiple_stats():
    """Тест кейс проверяет асинхронную работу цепочки статистических обработчиков"""

    class FailingFakeStat(FakeStat):
        async def get_statistics_async(self, answers_analysis):
            raise InternalCollectionException()

    foxypack = FoxyPack().with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FailingFakeStat()).with_foxy_stat(
        FakeStat())
    statistics = await foxypack.get_statistics_async("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"


def test_foxypack_empty_initialization():
    """Тест кейс проверяет инициализацию пустого FoxyPack"""
    foxypack = FoxyPack()

    assert foxypack.queue_foxy_analysis == []
    assert foxypack.queue_foxy_stat == []


def test_foxypack_with_initial_queues():
    """Тест кейс проверяет инициализацию FoxyPack с предустановленными очередями"""
    initial_analysis = [FakeAnalysis(), FakeAnalysis()]
    initial_stats = [FakeStat()]

    foxypack = FoxyPack(queue_foxy_analysis=initial_analysis, queue_foxy_stat=initial_stats)

    assert len(foxypack.queue_foxy_analysis) == 2
    assert len(foxypack.queue_foxy_stat) == 1


def test_foxypack_with_initial_queues_and_adding_more():
    """Тест кейс проверяет добавление новых обработчиков в предустановленный FoxyPack"""
    initial_analysis = [FakeAnalysis()]
    initial_stats = [FakeStat()]

    foxypack = FoxyPack(queue_foxy_analysis=initial_analysis, queue_foxy_stat=initial_stats)
    foxypack.with_foxy_analysis(FakeAnalysis()).with_foxy_stat(FakeStat())

    assert len(foxypack.queue_foxy_analysis) == 2
    assert len(foxypack.queue_foxy_stat) == 2