import urllib.parse
from urllib.parse import parse_qs

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
        # Парсим URL
        parsed_url = urllib.parse.urlparse(url)

        # Извлекаем параметры запроса с помощью parse_qs
        query_params = parse_qs(parsed_url.query)

        # Проверяем наличие параметра content_id
        if 'content_id' in query_params:
            content_id = query_params['content_id'][0]

            # Определяем тип контента по префиксу в content_id
            # Предполагаем, что content_id имеет формат "тип_идентификатор"
            parts = content_id.split('_', 1)  # Разделяем только по первому '_'

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

        # Если нет параметра content_id, это может быть:
        path = parsed_url.path
        if not path or path == '/':
            return "homepage"  # Главная страница
        else:
            return "channel"  # Страница канала/пользователя

    def get_analysis(self, url: str) -> AnswersAnalysis:
        """Основной метод получения анализа URL"""
        if not url or not url.strip():
            raise DenialAnalyticsException(url if url else "empty_url")

        # Парсим URL
        parsed_url = urllib.parse.urlparse(url)

        # Проверяем, что это наша социальная сеть
        domain = parsed_url.netloc.lower()
        if domain not in ["fakesocialmedia.com", "www.fakesocialmedia.com"]:
            raise DenialAnalyticsException(url)

        # Извлекаем параметры запроса для дополнительной информации
        query_params = parse_qs(parsed_url.query)

        # Определяем тип контента
        type_content = self.get_type_content(url)

        # Дополнительная логика: если есть content_id, можно извлечь ID
        content_id_value = None
        if 'content_id' in query_params:
            content_id_value = query_params['content_id'][0]
            # Можно добавить логирование или дополнительную обработку

        # Создаем и возвращаем объект анализа
        return AnswersAnalysis(
            url=url,
            social_platform="FakeSocialMedia",
            type_content=type_content
        )