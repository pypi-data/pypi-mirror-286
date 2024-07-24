#!/usr/bin/env python3
import sys

from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends
from loguru import logger
from sqlalchemy import URL, event, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from conf import settings
from core.models import MappedBase
from core.utils.timezone import timezone


def create_engine_and_session(url: str | URL):
    try:
        # Database engine
        engine = create_async_engine(url, echo=settings.DB_ECHO, future=True, pool_pre_ping=True)
    except Exception as e:
        logger.error('❌ Database link failed {}', e)
        sys.exit()
    else:
        db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session


async_engine, async_db_session = create_engine_and_session(settings.SQLALCHEMY_DATABASE_URI)


async def check_db():
    async with async_db_session() as db:
        try:
            await db.execute(text('SELECT 1'))
        except Exception as se:
            await db.rollback()
            raise se
        finally:
            await db.close()


async def get_db() -> AsyncSession:
    """Session Builder"""
    session = async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()


# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]


async def create_table():
    """Create database table"""
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


def timestamptz_encoder(v):
    if isinstance(v, (int, float)):
        v = v / 1000 if len(str(v)) == 13 else v
        return timezone.f_timestamp(v).isoformat()
    if isinstance(v, datetime):
        return timezone.f_datetime(v).isoformat()
    if isinstance(v, str):
        return datetime.fromisoformat(v).astimezone(UTC).isoformat()
    raise ValueError


@event.listens_for(async_engine.sync_engine, 'connect')
def register_custom_timestamptz_types(dbapi_con, *args):
    dbapi_con.run_async(
        lambda connection: connection.set_type_codec(
            typename='timestamptz', schema='pg_catalog', encoder=timestamptz_encoder, decoder=lambda x: x
        )
    )
