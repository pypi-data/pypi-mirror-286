#!/usr/bin/env python3
import re
import time

from pathlib import Path

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from core.common.i18n import i18n 


class AccessMiddleware(BaseHTTPMiddleware):
    """Record request logging middleware"""

    @staticmethod
    def get_language(lang_code):
        if not lang_code:
            return 'en_US'
        languages = re.findall(r'([a-z]{2}-[A-Z]{2}|[a-z]{2})(;q=\d.\d{1,3})?', lang_code)
        languages = sorted(languages, key=lambda x: x[1], reverse=True)  # sort the priority, no priority comes last
        translation_directory = Path('locale')
        translation_files = [i.name for i in translation_directory.iterdir()]
        explicit_priority = None

        for lang in languages:
            lang_folder = lang[0].replace('-', '_')
            if lang_folder in translation_files:
                if not lang[1]:  # languages without quality value having the highest priority 1
                    return lang_folder
                elif not explicit_priority:  # set language with explicit priority <= priority 1
                    explicit_priority = lang[0]

        # Return language with explicit priority or default value
        return explicit_priority if explicit_priority else 'en_US'

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        lang_code: str | None = request.headers.get('Accept-Language', None)
        i18n.set_language(language=self.get_language(lang_code)) 
        start = time.perf_counter()
        response: Response = await call_next(request)
        elapsed = time.perf_counter() - start
        response.headers['X-performance'] = f'{elapsed:0.5f}s'
        logger.info(f'{response.status_code} {request.client.host} {request.method} {request.url} {elapsed}')
        return response
