from datetime import date

import pytest

from foxypack import FoxyPack
from foxypack.exceptions import (
    ConfigurationError,
    FoxyError,
    UnsupportedOperationError,
)
from foxypack.foxypack_abc.answers import (
    AnswersSocialContent,
    AnswersSocialContainer,
)
from tests.foxypack_abc.test_foxyanalysis import FakeAnalysis
from tests.foxypack_abc.test_foxystatistics import FakeStatistics


def test_foxypack_empty_initialization():
    foxypack = FoxyPack()

    assert foxypack._queue_foxy_analysis == set()
    assert foxypack._queue_foxy_statistics == set()


def test_foxypack_with_module_analysis_only():
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=None,
    )

    assert len(foxypack._queue_foxy_analysis) == 1
    assert len(foxypack._queue_foxy_statistics) == 0

    analysis = next(iter(foxypack._queue_foxy_analysis))
    assert isinstance(analysis, FakeAnalysis)


def test_foxypack_with_module_analysis_and_statistics():
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=FakeStatistics(),
    )

    assert len(foxypack._queue_foxy_analysis) == 1
    assert len(foxypack._queue_foxy_statistics) == 1

    analysis = next(iter(foxypack._queue_foxy_analysis))
    stat = next(iter(foxypack._queue_foxy_statistics))

    assert isinstance(analysis, FakeAnalysis)
    assert isinstance(stat, FakeStatistics)


def test_foxypack_with_same_analysis_class_deduplicates_in_set():
    foxypack = FoxyPack()
    foxypack.with_module(FakeAnalysis(), None)
    foxypack.with_module(FakeAnalysis(), None)

    assert len(foxypack._queue_foxy_analysis) == 1


def test_foxypack_get_analysis_channel():
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=None,
    )

    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")

    assert analysis is not None
    assert analysis.url == "https://fakesocialmedia.com/qsgqsdrr"
    assert analysis.social_platform == "FakeSocialMedia"
    assert analysis.type_content == "channel"


def test_foxypack_get_analysis_video():
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=None,
    )

    analysis = foxypack.get_analysis(
        "https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
    )

    assert analysis is not None
    assert analysis.url == "https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
    assert analysis.social_platform == "FakeSocialMedia"
    assert analysis.type_content == "video"


def test_foxypack_get_analysis_invalid_url_raises_unsupported():
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=None,
    )

    with pytest.raises(UnsupportedOperationError):
        foxypack.get_analysis(
            "https://invalidmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
        )


def test_foxypack_get_analysis_no_analyzers_raises_configuration():
    foxypack = FoxyPack()

    with pytest.raises(ConfigurationError):
        foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")


def test_foxypack_get_analysis_multiple_analyzers_first_fails_second_succeeds():
    class FailingFakeAnalysis(FakeAnalysis):
        def get_analysis(self, url: str):
            raise FoxyError("analysis failed")

    foxypack = FoxyPack(
        queue_foxy_analysis={FailingFakeAnalysis(), FakeAnalysis()}
    )

    analysis = foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")

    assert analysis is not None
    assert analysis.url == "https://fakesocialmedia.com/qsgqsdrr"
    assert analysis.social_platform == "FakeSocialMedia"
    assert analysis.type_content == "channel"


def test_foxypack_get_analysis_multiple_analyzers_all_fail():
    class FailingFakeAnalysis(FakeAnalysis):
        def get_analysis(self, url: str):
            raise FoxyError("analysis failed")

    foxypack = FoxyPack(queue_foxy_analysis={FailingFakeAnalysis()})

    with pytest.raises(UnsupportedOperationError):
        foxypack.get_analysis("https://fakesocialmedia.com/qsgqsdrr")


def test_foxypack_get_statistics_full_flow():
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=FakeStatistics(),
    )

    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"
    assert statistics.title == "Tech Reviews Channel"
    assert statistics.subscribers == 15400
    assert statistics.creation_date == date(2020, 3, 15)


def test_foxypack_get_statistics_video_content():
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=FakeStatistics(),
    )

    statistics = foxypack.get_statistics(
        "https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs"
    )

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContent)
    assert statistics.system_id == "VID_001"
    assert statistics.title == "New Smartphone Review 2024"
    assert statistics.views == 125000
    assert statistics.publish_date == date(2024, 1, 15)


def test_foxypack_get_statistics_no_analysis_raises_configuration():
    foxypack = FoxyPack(queue_foxy_statistics={FakeStatistics()})

    with pytest.raises(ConfigurationError):
        foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")


def test_foxypack_get_statistics_no_stats_raises_configuration():
    foxypack = FoxyPack(queue_foxy_analysis={FakeAnalysis()})

    with pytest.raises(ConfigurationError):
        foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")


def test_foxypack_get_statistics_invalid_url_raises_unsupported():
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=FakeStatistics(),
    )

    with pytest.raises(UnsupportedOperationError):
        foxypack.get_statistics("https://invalidmedia.com/qsgqsdrr")


def test_foxypack_get_statistics_multiple_stats_first_fails_second_succeeds():
    class FailingFakeStat(FakeStatistics):
        def get_statistics(self, answers_analysis):
            raise FoxyError("stats failed")

    foxypack = FoxyPack(
        queue_foxy_analysis={FakeAnalysis()},
        queue_foxy_statistics={FailingFakeStat(), FakeStatistics()},
    )

    statistics = foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"


def test_foxypack_get_statistics_multiple_stats_all_fail():
    class FailingFakeStat(FakeStatistics):
        def get_statistics(self, answers_analysis):
            raise FoxyError("stats failed")

    foxypack = FoxyPack(
        queue_foxy_analysis={FakeAnalysis()},
        queue_foxy_statistics={FailingFakeStat()},
    )

    with pytest.raises(UnsupportedOperationError):
        foxypack.get_statistics("https://fakesocialmedia.com/qsgqsdrr")


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_full_flow():
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=FakeStatistics(),
    )

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
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=FakeStatistics(),
    )

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
async def test_foxypack_get_statistics_async_no_analysis_raises_configuration():
    foxypack = FoxyPack(queue_foxy_statistics={FakeStatistics()})

    with pytest.raises(ConfigurationError):
        await foxypack.get_statistics_async("https://fakesocialmedia.com/qsgqsdrr")


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_invalid_url_raises_unsupported():
    foxypack = FoxyPack().with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=FakeStatistics(),
    )

    with pytest.raises(UnsupportedOperationError):
        await foxypack.get_statistics_async("https://invalidmedia.com/qsgqsdrr")


@pytest.mark.asyncio
async def test_foxypack_get_statistics_async_multiple_stats():
    class FailingFakeStat(FakeStatistics):
        async def get_statistics_async(self, answers_analysis):
            raise FoxyError("stats failed")

    foxypack = FoxyPack(
        queue_foxy_analysis={FakeAnalysis()},
        queue_foxy_statistics={FailingFakeStat(), FakeStatistics()},
    )

    statistics = await foxypack.get_statistics_async(
        "https://fakesocialmedia.com/qsgqsdrr"
    )

    assert statistics is not None
    assert isinstance(statistics, AnswersSocialContainer)
    assert statistics.system_id == "CH_001"


def test_foxypack_with_initial_queues():
    initial_analysis = {FakeAnalysis()}
    initial_stats = {FakeStatistics()}

    foxypack = FoxyPack(
        queue_foxy_analysis=initial_analysis,
        queue_foxy_statistics=initial_stats,
    )

    assert len(foxypack._queue_foxy_analysis) == 1
    assert len(foxypack._queue_foxy_statistics) == 1


def test_foxypack_with_initial_queues_and_adding_more_deduplicates_same_classes():
    initial_analysis = {FakeAnalysis()}
    initial_stats = {FakeStatistics()}

    foxypack = FoxyPack(
        queue_foxy_analysis=initial_analysis,
        queue_foxy_statistics=initial_stats,
    )

    foxypack.with_module(
        foxy_analysis=FakeAnalysis(),
        foxy_statistics=FakeStatistics(),
    )

    assert len(foxypack._queue_foxy_analysis) == 1
    assert len(foxypack._queue_foxy_statistics) == 1