import urllib.parse
from urllib.parse import parse_qs

import pytest

from foxypack import FoxyAnalysis, AnswersAnalysis, DenialAnalyticsException
import urllib.parse
from urllib.parse import urlparse, parse_qs
import uuid

from foxypack import FoxyAnalysis, AnswersAnalysis
from foxypack.exceptions import DenialAnalyticsException

# https://fakesocialmedia.com
# https://fakesocialmedia.com/qsgqsdrr
# https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs
# https://fakesocialmedia.com/qsgqsdr?content_id=image_fdasfdgfs
# https://fakesocialmedia.com/qsgqsdr?content_id=text_fdasfdgfs

class FakeAnalysis(FoxyAnalysis):

    def get_type_content(self, url: str) -> str:
        """Определяет тип контента на основе параметра content_id в URL"""

        parsed_url = urllib.parse.urlparse(url)

        query_params = parse_qs(parsed_url.query)

        if 'content_id' in query_params:
            content_id = query_params['content_id'][0]

            parts = content_id.split('_', 1)

            if len(parts) >= 1:
                content_type = parts[0]  # Первая часть - тип контента

                # Сопоставляем тип с ожидаемыми значениями
                if content_type == 'video':
                    return "video"
                elif content_type == 'image':
                    return "image"
                elif content_type == 'text':
                    return "text"
                elif content_type == 'audio':
                    return "audio"
                elif content_type == 'document':
                    return "document"
                else:
                    return "unknown"

        path = parsed_url.path
        if not path or path == '/':
            return "homepage"
        else:
            return "channel"

    def get_analysis(self, url: str) -> AnswersAnalysis:
        """Основной метод получения анализа URL"""
        if not url or not url.strip():
            raise DenialAnalyticsException(url if url else "empty_url")

        parsed_url = urllib.parse.urlparse(url)

        domain = parsed_url.netloc.lower()
        if domain not in ["fakesocialmedia.com", "www.fakesocialmedia.com"]:
            raise DenialAnalyticsException(url)

        query_params = parse_qs(parsed_url.query)

        type_content = self.get_type_content(url)

        content_id_value = None
        if 'content_id' in query_params:
            content_id_value = query_params['content_id'][0]
        return AnswersAnalysis(
            url=url,
            social_platform="FakeSocialMedia",
            type_content=type_content
        )

def test_fake_analysis_channel():
    fake_analysis = FakeAnalysis().get_analysis("https://fakesocialmedia.com/qsgqsdrr")
    assert fake_analysis.url == 'https://fakesocialmedia.com/qsgqsdrr'
    assert fake_analysis.social_platform == 'FakeSocialMedia'
    assert fake_analysis.type_content == 'channel'


def test_fake_analysis_video():
    fake_analysis = FakeAnalysis().get_analysis("https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs")
    assert fake_analysis.url == 'https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs'
    assert fake_analysis.social_platform == 'FakeSocialMedia'
    assert fake_analysis.type_content == 'video'


def test_invalid_link_analysis():
    with pytest.raises(DenialAnalyticsException):
        FakeAnalysis().get_analysis("https://invalidmedia.com/qsgqsdr?content_id=video_fdasfdgfs")