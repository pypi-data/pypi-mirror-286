#!/usr/bin/env python3
from __future__ import annotations

import inspect
import logging
import sys

from typing import Any

from loguru import logger

from conf import settings


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def record_formatter(record: dict[str, Any]) -> str:  # pragma: no cover
    log_format = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> '
        '| <level>{level: <8}</level> '
        '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> '
        '- <level>{message}</level>\n'
    )

    if record['exception']:
        log_format = f'{log_format}'

    return log_format


def register_logging() -> None:  # pragma: no cover
    """Configures logging."""
    intercept_handler = InterceptHandler()

    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith('uvicorn.'):
            logging.getLogger(logger_name).handlers = []
        if logger_name.startswith('taskiq.'):
            logging.getLogger(logger_name).root.handlers = [intercept_handler]

    # change handler for default uvicorn logger
    logging.getLogger('uvicorn').handlers = [intercept_handler]
    logging.getLogger('uvicorn.access').handlers = [intercept_handler]

    # set logs output, level and format
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=record_formatter,  # type: ignore
    )
