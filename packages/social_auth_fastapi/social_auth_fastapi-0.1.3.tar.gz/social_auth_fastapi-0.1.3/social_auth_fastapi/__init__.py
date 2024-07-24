#!/usr/bin/env python3
from typing import Optional

from fastapi import FastAPI
from loguru import logger

from .conf import settings
from .models.base import create_table
from .routers import router


async def register_auth_social_init(
    app: FastAPI,
    engine,
    db_session,
    token_secret_key: Optional[str] = None,
    token_algorithm: Optional[str] = None,
    token_expire_seconds: Optional[int] = None,
    token_refresh_expire_seconds: Optional[int] = None,
):
    """
    Start initialization

    :return:
    """
    settings.ENGINE = engine
    settings.DB_SESSION = db_session

    if token_secret_key:
        settings.TOKEN_SECRET_KEY = token_secret_key

    if token_algorithm:
        settings.TOKEN_ALGORITHM = token_algorithm

    if token_expire_seconds:
        settings.TOKEN_EXPIRE_SECONDS = token_expire_seconds

    if token_refresh_expire_seconds:
        settings.TOKEN_REFRESH_EXPIRE_SECONDS = token_refresh_expire_seconds

    # Create database table
    logger.warning('Creating table first...')
    await create_table()
    logger.success('Create table successful')
    app.include_router(router)
