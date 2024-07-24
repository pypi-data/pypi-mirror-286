import functools

import asyncpg

from loguru import logger
from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database.db_postgres import async_db_session


async def acquire_lock(db: AsyncSession, lock_id):
    await db.execute(text(f'SELECT pg_advisory_lock({lock_id})'))


async def release_lock(db: AsyncSession, lock_id):
    await db.execute(text(f'SELECT pg_advisory_unlock({lock_id})'))


def pg_advisory_lock(lock_id):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with async_db_session.begin() as db:
                try:
                    # TODO: Check again if there are too many requests at the same time and lead to deadlock time
                    await acquire_lock(db, lock_id)
                    result = await func(*args, **kwargs, db=db)
                finally:
                    try:
                        await release_lock(db, lock_id)
                    except asyncpg.exceptions.PostgresError as e:
                        logger.error(f'Error pg_advisory_unlock: {e}')
                return result

        return wrapper

    return decorator
