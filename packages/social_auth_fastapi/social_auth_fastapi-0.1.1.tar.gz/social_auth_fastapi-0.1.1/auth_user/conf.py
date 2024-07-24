#!/usr/bin/env python3

import secrets
from enum import Enum
from functools import lru_cache
from typing import Optional, Any

from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    """Possible log levels."""

    NOTSET = 'NOTSET'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    FATAL = 'FATAL'


class SettingsSocial(BaseSettings):
    # Env Config
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None

    GITHUB_CLIENT_ID: str | None = None
    GITHUB_CLIENT_SECRET: str | None = None

    # DateTime
    DATETIME_TIMEZONE: str = 'UTC/GTM'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    # Token
    TOKEN_SECRET_KEY: str = secrets.token_urlsafe(32)
    TOKEN_ALGORITHM: str = 'HS256'  # algorithm
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24  # Expiration time, unit: seconds 60 * 60 * 24 * 1
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Refresh expiration time, unit: seconds

    # DB
    ENGINE: Optional[Any] = None
    DB_SESSION: Optional[Any] = None


@lru_cache
def get_settings() -> SettingsSocial:
    """Read configuration optimization writing method"""
    return SettingsSocial()


settings = get_settings()
